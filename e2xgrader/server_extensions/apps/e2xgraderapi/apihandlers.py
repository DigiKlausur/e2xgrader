import json

from e2xcore.handlers.base import E2xApiHandler
from nbgrader.server_extensions.formgrader.apihandlers import (
    AssignmentCollectionHandler,
    AssignmentHandler,
)
from nbgrader.server_extensions.formgrader.base import check_notebook_dir, check_xsrf
from tornado import web

from e2xgrader.exporters import GradeExporter


class E2xAssignmentCollectionHandler(E2xApiHandler, AssignmentCollectionHandler):
    """
    Inherit from E2xApiHandler to overwrite the internal NbgraderAPI with the E2xAPI
    """

    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        include_score = self.get_argument("include_score", "True").lower() == "true"
        self.write(json.dumps(self.api.get_assignments(include_score=include_score)))


class E2xAssignmentHandler(E2xApiHandler, AssignmentHandler):
    """
    Inherit from E2xApiHandler to overwrite the internal NbgraderAPI with the E2xAPI
    """

    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment_id):
        include_score = self.get_argument("include_score", "True").lower() == "true"
        assignment = self.api.get_assignment(assignment_id, include_score=include_score)
        if assignment is None:
            raise web.HTTPError(404)
        self.write(json.dumps(assignment))


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


class ExportGradesHandler(E2xApiHandler):
    def initialize(self) -> None:
        self.__exporter = GradeExporter()
        self.set_header("Content-Type", 'text/csv; charset="utf-8"')
        self.set_header("Content-Disposition", "attachment; filename=grades.csv")

    @web.authenticated
    @check_xsrf
    def get(self):
        level = self.get_argument("level", "notebook")
        if level == "task":
            self.__exporter.tasks = True
        elif level == "assignment":
            self.__exporter.notebooks = False
        normalize = self.get_argument("normalize", "false")
        if normalize.lower() == "max_score":
            self.__exporter.include_max_score = True
        else:
            self.__exporter.normalize = normalize.lower() == "true"
        self.write(self.__exporter.get_grades().to_csv())
        self.finish()


class AnnotationCollectionHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        solution_cells = self.api.get_annotations(self.get_argument("submission_id"))
        if solution_cells is None:
            raise web.HTTPError(404)
        return self.write(json.dumps(solution_cells))


class AnnotationHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def put(self, solution_cell_id):
        data = self.get_json_body()
        solution_cell = self.api.save_annotation(
            submission_id=data.get("submission_id"),
            name=data.get("name"),
            annotation=data.get("annotation"),
        )
        if solution_cell is None:
            raise web.HTTPError(404)

        self.write(json.dumps(solution_cell))


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
    (
        r"/formgrader/api/export_grades/?",
        ExportGradesHandler,
    ),
    (r"/formgrader/api/annotations", AnnotationCollectionHandler),
    (r"/formgrader/api/annotation/([^/]+)", AnnotationHandler),
]
