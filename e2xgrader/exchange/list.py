import os
import glob
from nbgrader.exchange.default import ExchangeList
from .exchange import E2xExchange

class E2xExchangeList(E2xExchange, ExchangeList):

    def init_dest(self):
        course_id = self.coursedir.course_id if self.coursedir.course_id else '*'
        assignment_id = self.coursedir.assignment_id if self.coursedir.assignment_id else '*'
        student_id = self.coursedir.student_id if self.coursedir.student_id else '*'

        if self.inbound:
            pattern = os.path.join(self.root, course_id, self.inbound_directory, '{}+{}+*'.format(student_id, assignment_id))
        elif self.cached:
            pattern = os.path.join(self.cache, course_id, '{}+{}+*'.format(student_id, assignment_id))
        else:
            pattern = os.path.join(self.root, course_id, self.outbound_directory, '{}'.format(assignment_id))

        self.assignments = sorted(glob.glob(pattern))

    def parse_assignment(self, assignment):
        if self.inbound:
            regexp = r".*/(?P<course_id>.*)/" + self.inbound_directory + \
                     r"/(?P<student_id>[^+]*)\+(?P<assignment_id>[^+]*)\+(?P<timestamp>[^+]*)(?P<random_string>\+.*)?"
        elif self.cached:
            regexp = r".*/(?P<course_id>.*)/(?P<student_id>.*)\+(?P<assignment_id>.*)\+(?P<timestamp>.*)"
        else:
            regexp = r".*/(?P<course_id>.*)/" + self.outbound_directory + \
                     r"/(?P<assignment_id>.*)"

        m = re.match(regexp, assignment)
        if m is None:
            raise RuntimeError("Could not match '%s' with regexp '%s'", assignment, regexp)
        return m.groupdict()
