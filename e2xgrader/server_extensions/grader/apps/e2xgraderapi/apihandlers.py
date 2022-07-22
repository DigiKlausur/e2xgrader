import json
import os

from nbgrader.server_extensions.formgrader.apihandlers import (
    AssignmentCollectionHandler,
    AssignmentHandler,
)
from nbgrader.server_extensions.formgrader.base import check_xsrf
from tornado import web

from .base import E2xApiHandler


class E2xAssignmentCollectionHandler(E2xApiHandler, AssignmentCollectionHandler):
    """
    Inherit from E2xApiHandler to overwrite the internal NbgraderAPI with the E2xAPI
    """

    pass


class E2xAssignmentHandler(E2xApiHandler, AssignmentHandler):
    """
    Inherit from E2xApiHandler to overwrite the internal NbgraderAPI with the E2xAPI
    """

    pass


class SolutionCellCollectionHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self, assignment_id, notebook_id):
        cells = self.api.get_solution_cell_ids(assignment_id, notebook_id)
        self.write(json.dumps(cells))


class SubmittedTaskCollectionHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self, assignment_id, notebook_id, task_id):
        submissions = self.api.get_task_submissions(assignment_id, notebook_id, task_id)
        self.write(json.dumps(submissions))


class GenerateFeedbackHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def post(self, assignment_id, student_id):
        hide_cells = json.loads(self.get_argument("hide_cells", "false"))
        self.write(
            json.dumps(
                self.api.generate_feedback(
                    assignment_id, student_id, hide_cells=hide_cells
                )
            )
        )


class GenerateAllFeedbackHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def post(self, assignment_id):
        hide_cells = json.loads(self.get_argument("hide_cells", "false"))
        self.write(
            json.dumps(self.api.generate_feedback(assignment_id, hide_cells=hide_cells))
        )


class GraderHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        e2xgrader_settings = self.settings.get("e2xgrader", dict())
        grader_settings = e2xgrader_settings.get("graders", list())
        self.write(json.dumps(grader_settings))


default_handlers = [
    (r"/formgrader/api/assignments", E2xAssignmentCollectionHandler),
    (r"/formgrader/api/assignment/([^/]+)", E2xAssignmentHandler),
    (r"/formgrader/api/solution_cells/([^/]+)/([^/]+)", SolutionCellCollectionHandler),
    (
        r"/formgrader/api/submitted_tasks/([^/]+)/([^/]+)/([^/]+)",
        SubmittedTaskCollectionHandler,
    ),
    (
        r"/formgrader/api/assignment/([^/]+)/generate_feedback",
        GenerateAllFeedbackHandler,
    ),
    (
        r"/formgrader/api/assignment/([^/]+)/([^/]+)/generate_feedback",
        GenerateFeedbackHandler,
    ),
]
