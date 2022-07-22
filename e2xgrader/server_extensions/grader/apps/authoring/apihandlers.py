import json
import os

from jupyter_client.kernelspec import KernelSpecManager
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

from ..e2xgraderapi.base import E2xApiHandler


class BaseApiManageHandler(E2xApiHandler):
    def initialize(self, model_cls):
        self.__model = model_cls(self.coursedir)

    @web.authenticated
    @check_xsrf
    def post(self, **kwargs):
        self.write(self.__model.new(**kwargs))

    @web.authenticated
    @check_xsrf
    def delete(self, **kwargs):
        self.__model.remove(**kwargs)
        self.write({"status": True})

    @web.authenticated
    @check_xsrf
    def get(self, **kwargs):
        self.write(json.dumps(self.__model.get(**kwargs)))

    @web.authenticated
    @check_xsrf
    def put(self, **kwargs):
        self.write(self.__model.new(**kwargs))


class BaseApiListHandler(E2xApiHandler):
    def initialize(self, model_cls):
        self.__model = model_cls(self.coursedir)

    @web.authenticated
    @check_xsrf
    def get(self, **kwargs):
        self.write(json.dumps(self.__model.list(**kwargs)))


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


default_handlers = [
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
