import os
import json

from tornado import web
from nbgrader.server_extensions.formgrader.base import check_xsrf

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

from multiprocessing import Process, Value
from ctypes import c_wchar_p

autograde_assignment = Value(c_wchar_p, "")


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


class GetNotebook(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        assignment_object = self.api.gradebook.find_assignment(assignment_id)
        notebooks = []
        for assignment in assignment_object.notebooks:
            notebooks.append(assignment.name)
        self.write(json.dumps(notebooks))


class FindUpdatedCells(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        notebook_id = self.get_argument("notebook_id")
        updated_cells = self.api.list_updated_cells(notebook_id, assignment_id)
        self.write(json.dumps(updated_cells))


class UpdateNotebook(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        notebook_id = self.get_argument("notebook_id")
        cells = self.get_argument("cells")
        cells = eval(cells.split()[0])
        checksum_id = []
        for cell in cells:
            checksum_single = self.api.update_cell_content(
                cell, notebook_id, assignment_id
            )
            checksum_id.append(checksum_single)
            self.api.gradebook.update_or_create_source_cell(
                name=cell,
                notebook=notebook_id,
                assignment=assignment_id,
                checksum=checksum_single,
            )
        self.write(json.dumps(checksum_id))


class ListCells(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        notebook = self.api.gradebook.find_assignment(assignment_id).notebooks[0].name
        cells = self.api.list_autograde_testcells(notebook, assignment_id)
        self.write(json.dumps(cells))


class AutogradeLog(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        try:
            with open(
                os.path.join(os.getcwd(), "log", assignment_id + ".txt")
            ) as json_file:
                autograde_log = json_file.read()
        except FileNotFoundError:
            autograde_log = "Autograding required."
        result = {"autograde_log": autograde_log}
        self.write(json.dumps(result))


class StudentNum(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        students = self.api.get_submitted_students(assignment_id)
        result = {"student_num": str(len(students))}
        self.write(json.dumps(result))


class AutogradeAll(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        autograde_assignment.value = str(assignment_id)
        p = Process(target=self.api.autograde_all, args=(assignment_id,))
        p.start()


class AutogradeCells(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        selected_cells = self.get_argument("cell_ids")
        selected_cells = str(selected_cells).split(",")
        autograde_assignment.value = str(assignment_id)
        p = Process(
            target=self.api.autograde_cells,
            args=(
                assignment_id,
                selected_cells,
            ),
        )
        p.start()


class AutogradingStop(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        self.api.autograde_stop.value = True


class AutogradingProgess(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument("assignment_id")
        try:
            with open(
                os.path.join(os.getcwd(), "log", assignment_id + ".txt")
            ) as json_file:
                data = json.load(json_file)
                autograde_log = data["time"]
        except FileNotFoundError:
            autograde_log = "Autograding required."
        result = {
            "autograde_idx": self.api.autograde_idx.value,
            "autograde_total": self.api.autograde_total.value,
            "autograde_flag": self.api.autograde_flag.value,
            "autograde_log": autograde_log,
            "autograde_assignment": autograde_assignment.value,
        }
        self.write(json.dumps(result))


class GenerateAllFeedbackHandlerHide(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def post(self, assignment_id):
        self.write(json.dumps(self.api.generate_feedback(assignment_id, hidecells=True)))


class GenerateFeedbackHandlerHide(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def post(self, assignment_id, student_id):
        self.write(
            json.dumps(self.api.generate_feedback(assignment_id, student_id, hidecells=True))
        )


formgrade_handlers = [
    (r"/formgrader/api/solution_cells/([^/]+)/([^/]+)", SolutionCellCollectionHandler),
    (
        r"/formgrader/api/submitted_tasks/([^/]+)/([^/]+)/([^/]+)",
        SubmittedTaskCollectionHandler,
    ),
    (r"/formgrader/api/get_notebook/?", GetNotebook),
    (r"/formgrader/api/find_updated_cell/?", FindUpdatedCells),
    (r"/formgrader/api/update_notebook/?", UpdateNotebook),
    (r"/formgrader/api/student_num/?", StudentNum),
    (r"/formgrader/api/autograde_all/?", AutogradeAll),
    (r"/formgrader/api/autograde_cells/?", AutogradeCells),
    (r"/formgrader/api/autograding_log/?", AutogradeLog),
    (r"/formgrader/api/list_cells/?", ListCells),
    (r"/formgrader/api/autograding_progress/?", AutogradingProgess),
    (r"/formgrader/api/autograding_stop/?", AutogradingStop),
    (
        r"/formgrader/api/assignment/([^/]+)/generate_feedback_hide",
        GenerateAllFeedbackHandlerHide,
    ),
    (
        r"/formgrader/api/assignment/([^/]+)/([^/]+)/generate_feedback_hide",
        GenerateFeedbackHandlerHide,
    ),
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
