import json
import os

from jupyter_client.kernelspec import KernelSpecManager
from nbgrader.server_extensions.formgrader.apihandlers import (
    AssignmentCollectionHandler,
    AssignmentHandler,
)
from nbgrader.server_extensions.formgrader.base import check_xsrf
from tornado import web

from e2xgrader.converters import GenerateExercise
from e2xgrader.models import (
    AssignmentModel,
    ExerciseModel,
    PresetModel,
    TaskModel,
    TaskPoolModel,
    TemplateModel,
)
from e2xgrader.utils import NotebookVariableExtractor

from .base import BaseApiListHandler, BaseApiManageHandler, E2xApiHandler


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


class PresetHandler(E2xApiHandler):
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


class TemplateVariableHandler(E2xApiHandler):
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


class KernelSpecHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        self.write(json.dumps(KernelSpecManager().get_all_specs()))


class GenerateExerciseHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        resources = json.loads(self.get_argument("resources"))
        GenerateExercise(coursedir=self.coursedir).convert(resources)
        self.write({"status": True})


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
    (r"/e2xgrader/api/graders", GraderHandler),
]
