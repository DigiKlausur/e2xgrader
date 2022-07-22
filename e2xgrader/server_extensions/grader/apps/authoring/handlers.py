import os
import sys

from nbgrader.server_extensions.formgrader.base import (
    BaseHandler,
    check_notebook_dir,
    check_xsrf,
)
from tornado import web

from e2xgrader.models import ExerciseModel, TaskPoolModel, TemplateModel


class TaskcreatorHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        self.redirect(f"{self.base_url}/taskcreator/assignments")


class ManageAssignmentsHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        html = self.render(
            os.path.join("nbassignment", "assignments.tpl"),
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
            os.path.join("nbassignment", "exercises.tpl"),
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
            os.path.join("nbassignment", "taskpools.tpl"),
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
            os.path.join("nbassignment", "tasks.tpl"),
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
            os.path.join("nbassignment", "templates.tpl"),
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
            os.path.join("nbassignment", "editexercise.tpl"),
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
    (r"/taskcreator/?", TaskcreatorHandler),
    (r"/taskcreator/assignments/?", ManageAssignmentsHandler),
    (r"/taskcreator/assignments/(?P<assignment>[^/]+)/?", ManageExercisesHandler),
    (r"/taskcreator/pools/?", ManagePoolsHandler),
    (r"/taskcreator/pools/(?P<pool>[^/]+)/?", ManageTasksHandler),
    (r"/taskcreator/templates/?", ManageTemplatesHandler),
    (
        r"/taskcreator/assignments/(?P<assignment>[^/]+)/(?P<exercise>[^/]+)/?",
        EditExercisesHandler,
    ),
]
