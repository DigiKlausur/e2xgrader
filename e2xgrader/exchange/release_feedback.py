import os
import shutil
import glob
import re

from nbgrader.exchange.default import ExchangeReleaseFeedback

from .exchange import E2xExchange

from nbgrader.utils import notebook_hash, make_unique_key


class E2xExchangeReleaseFeedback(E2xExchange, ExchangeReleaseFeedback):

    def copy_files(self):
        if self.coursedir.student_id_exclude:
            exclude_students = set(self.coursedir.student_id_exclude.split(','))
        else:
            exclude_students = set()

        html_files = glob.glob(os.path.join(self.src_path, "*.html"))
        for html_file in html_files:
            if 'hashcode' in html_file:
                self.log.debug('Skipping hashcode info')
                continue
            regexp = re.escape(os.path.sep).join([
                self.coursedir.format_path(
                    self.coursedir.feedback_directory,
                    "(?P<student_id>.*)",
                    self.coursedir.assignment_id, escape=True),
                "(?P<notebook_id>.*).html"
            ])

            m = re.match(regexp, html_file)
            if m is None:
                msg = "Could not match '%s' with regexp '%s'" % (html_file, regexp)
                self.log.error(msg)
                continue

            gd = m.groupdict()
            student_id = gd['student_id']
            notebook_id = gd['notebook_id']
            if student_id in exclude_students:
                self.log.debug("Skipping student '{}'".format(student_id))
                continue

            feedback_dir = os.path.split(html_file)[0]
            submission_dir = self.coursedir.format_path(
                self.coursedir.submitted_directory, student_id,
                self.coursedir.assignment_id)

            timestamp = open(os.path.join(feedback_dir, 'timestamp.txt')).read()
            nbfile = os.path.join(submission_dir, "{}.ipynb".format(notebook_id))
            unique_key = make_unique_key(
                self.coursedir.course_id,
                self.coursedir.assignment_id,
                notebook_id,
                student_id,
                timestamp)

            self.log.debug("Unique key is: {}".format(unique_key))
            checksum = notebook_hash(nbfile, unique_key)
            dest = os.path.join(self.dest_path, "{}.html".format(checksum))

            self.log.info("Releasing feedback for student '{}' on assignment '{}/{}/{}' ({})".format(
                student_id, self.coursedir.course_id, self.coursedir.assignment_id, notebook_id, timestamp))
            shutil.copy(html_file, dest)
            self.log.info("Feedback released to: {}".format(dest))
