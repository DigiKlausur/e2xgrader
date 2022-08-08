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
from e2xgrader.utils import NotebookVariableExtractor, urljoin

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


pool_regex = r"(?P<pool>[^/]+)"
name_regex = r"(?P<name>[^/]+)"
assignment_regex = r"(?P<assignment>[^/]+)"

api_url = urljoin("e2x", "authoring", "api")
default_handlers = [
    (urljoin(api_url, "presets"), PresetHandler),
    (
        urljoin(api_url, "assignments", "?"),
        BaseApiListHandler,
        dict(model_cls=AssignmentModel),
    ),
    (
        urljoin(api_url, "template", name_regex, "?"),
        BaseApiManageHandler,
        dict(model_cls=TemplateModel),
    ),
    (
        urljoin(api_url, "templates", "?"),
        BaseApiListHandler,
        dict(model_cls=TemplateModel),
    ),
    (
        urljoin(api_url, "pool", name_regex, "?"),
        BaseApiManageHandler,
        dict(model_cls=TaskPoolModel),
    ),
    (urljoin(api_url, "pools", "?"), BaseApiListHandler, dict(model_cls=TaskPoolModel)),
    (
        urljoin(api_url, "pools", pool_regex, "?"),
        BaseApiListHandler,
        dict(model_cls=TaskModel),
    ),
    (
        urljoin(api_url, "task", pool_regex, name_regex, "?"),
        BaseApiManageHandler,
        dict(model_cls=TaskModel),
    ),
    (
        urljoin(api_url, "exercise", assignment_regex, name_regex, "?"),
        BaseApiManageHandler,
        dict(model_cls=ExerciseModel),
    ),
    (
        urljoin(api_url, "assignments", assignment_regex, "?"),
        BaseApiListHandler,
        dict(model_cls=ExerciseModel),
    ),
    (urljoin(api_url, "templates", "variables"), TemplateVariableHandler),
    (urljoin(api_url, "kernelspec"), KernelSpecHandler),
    (urljoin(api_url, "generate_exercise"), GenerateExerciseHandler),
]
