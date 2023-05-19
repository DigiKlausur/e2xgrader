import os
import sys

from nbgrader.server_extensions.formgrader.base import (
    BaseHandler,
    check_notebook_dir,
    check_xsrf,
)
from tornado import web

from e2xgrader.models import ExerciseModel, TaskPoolModel, TemplateModel
from e2xgrader.utils import urljoin

app_url = urljoin("e2x", "authoring", "app")


class TaskcreatorHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        self.redirect(urljoin(self.base_url, app_url, "assignments"))


class ManageAssignmentsHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        html = self.render(
            os.path.join("authoring", "assignments.tpl"),
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == "win32"),
        )
        self.write(html)


class ManageExercisesHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment):
        html = self.render(
            os.path.join("authoring", "exercises.tpl"),
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            assignment=assignment,
            windows=(sys.prefix == "win32"),
        )
        self.write(html)


class ManagePoolsHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        html = self.render(
            os.path.join("authoring", "taskpools.tpl"),
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == "win32"),
        )
        self.write(html)


class ManageTasksHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, pool):
        html = self.render(
            os.path.join("authoring", "tasks.tpl"),
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            pool=pool,
            windows=(sys.prefix == "win32"),
        )
        self.write(html)


class ManageTemplatesHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        html = self.render(
            os.path.join("authoring", "templates.tpl"),
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == "win32"),
        )
        self.write(html)


class EditExercisesHandler(BaseHandler):
    def initialize(self):
        self._model = ExerciseModel(self.coursedir)

    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self, assignment, exercise):
        html = self.render(
            os.path.join("authoring", "editexercise.tpl"),
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            exercise=exercise,
            assignment=assignment,
            templates=TemplateModel(self.coursedir).list(),
            pools=TaskPoolModel(self.coursedir).list(),
            windows=(sys.prefix == "win32"),
        )
        self.write(html)


default_handlers = [
    (urljoin(app_url, "?"), TaskcreatorHandler),
    (urljoin(app_url, "assignments", "?"), ManageAssignmentsHandler),
    (
        urljoin(app_url, "assignments", r"(?P<assignment>[^/]+)", "?"),
        ManageExercisesHandler,
    ),
    (urljoin(app_url, "pools", "?"), ManagePoolsHandler),
    (urljoin(app_url, "pools", r"(?P<pool>[^/]+)", "?"), ManageTasksHandler),
    (urljoin(app_url, "templates", "?"), ManageTemplatesHandler),
    (
        urljoin(
            app_url,
            "assignments",
            r"(?P<assignment>[^/]+)",
            r"(?P<exercise>[^/]+)",
            "?",
        ),
        EditExercisesHandler,
    ),
]
