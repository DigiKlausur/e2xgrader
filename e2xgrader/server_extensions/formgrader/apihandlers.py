import os
import json
import base64

from tornado import web
from nbgrader.server_extensions.formgrader.base import check_xsrf, check_notebook_dir
from nbgrader.api import MissingEntry

from ...models import (
    PresetModel,
    AssignmentModel,
    ExerciseModel,
    TaskPoolModel,
    TaskModel,
    TemplateModel,
)
from .base import E2xBaseApiHandler as BaseApiHandler
from .base import BaseApiManageHandler, BaseApiListHandler

from ...utils import NotebookVariableExtractor
from ...converters import GenerateExercise
from jupyter_client.kernelspec import KernelSpecManager


class SolutionCellCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self, assignment_id, notebook_id):
        cells = self.api.get_solution_cell_ids(assignment_id, notebook_id)
        self.write(json.dumps(cells))


class SubmittedTaskCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self, assignment_id, notebook_id, task_id):
        submissions = self.api.get_task_submissions(assignment_id, notebook_id, task_id)
        self.write(json.dumps(submissions))


class PresetHandler(BaseApiHandler):
    def initialize(self):
        self.__model = PresetModel(self.coursedir)

    def _list_template(self):
        self.write(json.dumps(self.__model.list_template_presets()))

    def _get_template(self):
        name = self.get_argument("name")
        self.write(json.dumps(self.__model.get_template_preset(name)))

    def _list_question(self):
        self.write(json.dumps(self.__model.list_question_presets()))

    def _get_question(self):
        name = self.get_argument("name")
        self.write(json.dumps(self.__model.get_question_preset(name)))

    @web.authenticated
    @check_xsrf
    def get(self):
        action = self.get_argument("action")
        preset_type = self.get_argument("type")
        handler = getattr(self, "_{}_{}".format(action, preset_type))
        handler()


class TemplateVariableHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        template = self.get_argument("template")
        variables = NotebookVariableExtractor().extract(
            os.path.join(
                self.url_prefix, "templates", template, "{}.ipynb".format(template)
            )
        )
        self.write(json.dumps(variables))


class KernelSpecHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        self.write(json.dumps(KernelSpecManager().get_all_specs()))


class GenerateExerciseHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        resources = json.loads(self.get_argument("resources"))
        GenerateExercise(coursedir=self.coursedir).convert(resources)
        self.write({"status": True})


class GenerateAllFeedbackHandlerHide(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def post(self, assignment_id):
        self.write(
            json.dumps(self.api.generate_feedback(assignment_id, hidecells=True))
        )


class GenerateFeedbackHandlerHide(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def post(self, assignment_id, student_id):
        self.write(
            json.dumps(
                self.api.generate_feedback(assignment_id, student_id, hidecells=True)
            )
        )


class AnnotationCollectionHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        submission_id = self.get_argument("submission_id")
        try:
            notebook = self.gradebook.find_submission_notebook_by_id(submission_id)
        except MissingEntry:
            raise web.HTTPError(404)

        autograded_path = self.api.coursedir.format_path(
            nbgrader_step=self.api.coursedir.autograded_directory,
            student_id=notebook.student.id,
            assignment_id=notebook.assignment.name,
        )
        annotation_path = os.path.join(autograded_path, "annotations")
        solution_cells = [s.to_dict() for s in notebook.notebook.solution_cells]

        for solution_cell in solution_cells:
            solution_cell["submission_id"] = submission_id
            # Try loading the annotation for that cell
            try:
                with open(
                    os.path.join(annotation_path, f'{solution_cell["name"]}.png'), "rb"
                ) as f:
                    solution_cell["annotation"] = str(base64.b64encode(f.read()))[2:-1]
            except FileNotFoundError:
                solution_cell["annotation"] = None
        self.write(json.dumps(solution_cells))


class AnnotationHandler(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def put(self, solution_cell_id):
        data = self.get_json_body()
        submission_id = data.get("submission_id")
        name = data.get("name")
        try:
            notebook = self.gradebook.find_submission_notebook_by_id(submission_id)
        except MissingEntry:
            raise web.HTTPError(404)
        autograded_path = self.api.coursedir.format_path(
            nbgrader_step=self.api.coursedir.autograded_directory,
            student_id=notebook.student.id,
            assignment_id=notebook.assignment.name,
        )
        annotation_path = os.path.join(autograded_path, "annotations")

        os.makedirs(annotation_path, exist_ok=True)
        with open(os.path.join(annotation_path, f"{name}.png"), "wb") as f:
            f.write(base64.b64decode(data.get("annotation")[22:]))
        self.write(
            json.dumps(
                {
                    "id": submission_id,
                    "name": name,
                    "annotation": data.get("annotation"),
                    "notebook": notebook.notebook.name,
                    "assignment": notebook.assignment.name,
                }
            )
        )


formgrade_handlers = [
    (r"/formgrader/api/solution_cells/([^/]+)/([^/]+)", SolutionCellCollectionHandler),
    (
        r"/formgrader/api/submitted_tasks/([^/]+)/([^/]+)/([^/]+)",
        SubmittedTaskCollectionHandler,
    ),
    (
        r"/formgrader/api/assignment/([^/]+)/generate_feedback_hide",
        GenerateAllFeedbackHandlerHide,
    ),
    (
        r"/formgrader/api/assignment/([^/]+)/([^/]+)/generate_feedback_hide",
        GenerateFeedbackHandlerHide,
    ),
    (r"/formgrader/api/annotations", AnnotationCollectionHandler),
    (r"/formgrader/api/annotation/([^/]+)", AnnotationHandler),
]

nbassignment_handlers = [
    (r"/taskcreator/api/presets", PresetHandler),
    (
        r"/taskcreator/api/assignments/?",
        BaseApiListHandler,
        dict(model_cls=AssignmentModel),
    ),
    (
        r"/taskcreator/api/template/(?P<name>[^/]+)/?",
        BaseApiManageHandler,
        dict(model_cls=TemplateModel),
    ),
    (
        r"/taskcreator/api/templates/?",
        BaseApiListHandler,
        dict(model_cls=TemplateModel),
    ),
    (
        r"/taskcreator/api/pool/(?P<name>[^/]+)/?",
        BaseApiManageHandler,
        dict(model_cls=TaskPoolModel),
    ),
    (r"/taskcreator/api/pools/?", BaseApiListHandler, dict(model_cls=TaskPoolModel)),
    (
        r"/taskcreator/api/pools/(?P<pool>[^/]+)/?",
        BaseApiListHandler,
        dict(model_cls=TaskModel),
    ),
    (
        r"/taskcreator/api/task/(?P<pool>[^/]+)/(?P<name>[^/]+)/?",
        BaseApiManageHandler,
        dict(model_cls=TaskModel),
    ),
    (
        r"/taskcreator/api/exercise/(?P<assignment>[^/]+)/(?P<name>[^/]+)/?",
        BaseApiManageHandler,
        dict(model_cls=ExerciseModel),
    ),
    (
        r"/taskcreator/api/assignments/(?P<assignment>[^/]+)/?",
        BaseApiListHandler,
        dict(model_cls=ExerciseModel),
    ),
    (r"/taskcreator/api/templates/variables", TemplateVariableHandler),
    (r"/taskcreator/api/kernelspec", KernelSpecHandler),
    (r"/taskcreator/api/generate_exercise", GenerateExerciseHandler),
]

default_handlers = formgrade_handlers + nbassignment_handlers
