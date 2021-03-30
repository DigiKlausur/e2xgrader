"""Tornado handlers for nbgrader assignment list web service."""

import os
import json
import contextlib
import traceback

from tornado import web

from notebook.utils import url_path_join as ujoin

from nbgrader.exchange import ExchangeFactory
from nbgrader.coursedir import CourseDirectory
from nbgrader.auth import Authenticator

from nbgrader.server_extensions.assignment_list.handlers import AssignmentList, default_handlers, BaseAssignmentHandler

static = os.path.join(os.path.dirname(__file__), 'static')


@contextlib.contextmanager
def chdir(dirname):
    currdir = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(currdir)


class E2xAssignmentList(AssignmentList):

    def submit_assignment(self, course_id, assignment_id):
        with self.get_assignment_dir_config() as config:
            try:
                config = self.load_config()
                config.CourseDirectory.course_id = course_id
                config.CourseDirectory.assignment_id = assignment_id

                coursedir = CourseDirectory(config=config)
                authenticator = Authenticator(config=config)
                submit = ExchangeFactory(config=config).Submit(
                    coursedir=coursedir,
                    authenticator=authenticator,
                    config=config)

                retval = submit.start()
                hashcode = 'Exchange not set up for hashcode'
                timestamp = 'Exchange not set up for timestamp'
                if retval and len(retval) == 2:
                    hashcode, timestamp = retval

            except Exception:
                self.log.error(traceback.format_exc())
                retvalue = {
                    "success": False,
                    "value": traceback.format_exc()
                }

            else:
                retvalue = {
                    "success": True,
                    "hashcode": hashcode,
                    "timestamp": timestamp
                }

        self.log.info(retvalue)

        return retvalue


class AssignmentActionHandler(BaseAssignmentHandler):

    @web.authenticated
    def post(self, action):
        if action == 'fetch':
            assignment_id = self.get_argument('assignment_id')
            course_id = self.get_argument('course_id')
            self.manager.fetch_assignment(course_id, assignment_id)
            self.finish(json.dumps(self.manager.list_assignments(course_id=course_id)))
        elif action == 'submit':
            assignment_id = self.get_argument('assignment_id')
            course_id = self.get_argument('course_id')
            output = self.manager.submit_assignment(course_id, assignment_id)
            if output['success']:
                response = self.manager.list_assignments(course_id=course_id)
                response['hashcode'] = output['hashcode']
                response['timestamp'] = output['timestamp']
                self.finish(json.dumps(response))
            else:
                self.finish(json.dumps(output))
        elif action == 'fetch_feedback':
            assignment_id = self.get_argument('assignment_id')
            course_id = self.get_argument('course_id')
            self.manager.fetch_feedback(course_id, assignment_id)
            self.finish(json.dumps(self.manager.list_assignments(course_id=course_id)))


# -----------------------------------------------------------------------------
#  URL to handler mappings
# -----------------------------------------------------------------------------


_assignment_action_regex = r"(?P<action>fetch|submit|fetch_feedback)"

e2x_default_handlers = [
    (r"/assignments/%s" % _assignment_action_regex, AssignmentActionHandler),
]


def load_jupyter_server_extension(nbapp):
    """Load the nbserver"""
    nbapp.log.info("Loading the assignment_list e2xgrader serverextension")
    webapp = nbapp.web_app
    webapp.settings['assignment_list_manager'] = E2xAssignmentList(parent=nbapp)
    base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", [
        (ujoin(base_url, pat), handler)
        for pat, handler in e2x_default_handlers + default_handlers
    ])
