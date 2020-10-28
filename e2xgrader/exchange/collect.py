import os
import glob
from collections import defaultdict

from nbgrader.exchange.default.collect import ExchangeCollect, groupby
from .exchange import E2xExchange

from nbgrader.utils import check_mode, parse_utc
from nbgrader.api import Gradebook, MissingEntry


class E2xExchangeCollect(E2xExchange, ExchangeCollect):

    def init_submissions(self):
        if self.personalized_inbound:
            self.log.info('Collecting from restricted submit dirs')
            submit_dirs = [username for username in os.listdir(self.inbound_path) if '+' not in username and 
                           os.path.isdir(os.path.join(self.inbound_path, username))]
            self.log.info(f'Submission dirs: {submit_dirs}')

            usergroups = defaultdict(list)
            records = []

            for user in submit_dirs:
                submit_path = os.path.join(self.inbound_path, user)
                self.log.info(f'Assignment id: {self.coursedir.assignment_id}')
                pattern = os.path.join(submit_path, f'{user}+{self.coursedir.assignment_id}+*')
                user_records = [self._path_to_record(f) for f in glob.glob(pattern)]
                self.log.info(f'{user} has {len(user_records)} submissions.')
                for i, record in enumerate(user_records):
                    user_records[i]['filename'] = os.path.join(user, record['filename'])

                usergroups.update(groupby(user_records, lambda item: item['username']))
                records.append(user_records)           

        else:
            student_id = self.coursedir.student_id if self.coursedir.student_id else '*'
            pattern = os.path.join(self.inbound_path, '{}+{}+*'.format(student_id, self.coursedir.assignment_id))
            records = [self._path_to_record(f) for f in glob.glob(pattern)]
            usergroups = groupby(records, lambda item: item['username'])

        return records, usergroups


    def init_src(self):
        if self.coursedir.course_id == '':
            self.fail("No course id specified. Re-run with --course flag.")

        self.course_path = os.path.join(self.root, self.coursedir.course_id)
        self.inbound_path = os.path.join(self.course_path, 'inbound')
        if not os.path.isdir(self.inbound_path):
            self.fail("Course not found: {}".format(self.inbound_path))
        if not check_mode(self.inbound_path, read=True, execute=True):
            self.fail("You don't have read permissions for the directory: {}".format(self.inbound_path))

        records, usergroups = self.init_submissions()

        with Gradebook(self.coursedir.db_url, self.coursedir.course_id) as gb:
            try:
                assignment = gb.find_assignment(self.coursedir.assignment_id)
                self.duedate = assignment.duedate
            except MissingEntry:
                self.duedate = None
        if self.duedate is None or not self.before_duedate:
            self.src_records = [self._sort_by_timestamp(v)[0] for v in usergroups.values()]
        else:
            self.src_records = []
            for v in usergroups.values():
                records = self._sort_by_timestamp(v)
                records_before_duedate = [record for record in records if record['timestamp'] <= self.duedate]
                if records_before_duedate:
                    self.src_records.append(records_before_duedate[0])
                else:
                    self.src_records.append(records[0])