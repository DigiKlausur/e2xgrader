import os
import re
import sys
import nbformat

from tornado import web

from .base import BaseHandler, check_xsrf, check_notebook_dir

class Template404(BaseHandler):
    """Render our 404 template"""
    def prepare(self):
        raise web.HTTPError(404)

class BaseGraderHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        html = self.render(
            "grader.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == 'win32'))
        self.write(html)


class AssignmentsHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        html = self.render(
            "assignments.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == 'win32'))
        self.write(html)


class ExportGradesHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        html = self.render(
            "export_grades.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == 'win32'))
        self.write(html)

class ExportGeneralHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        html = self.render(
            "export_common.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == 'win32'))
        self.write(html)

class StudentsHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        html = self.render(
            "students.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            windows=(sys.prefix == 'win32'))
        self.write(html)



root_path = os.path.dirname(__file__)
template_path = os.path.join(root_path, 'templates')
static_path = os.path.join(root_path, 'static')

default_handlers = [
    (r"/grader/?", BaseGraderHandler),
    (r"/grader/assignments/?", AssignmentsHandler),
    (r"/grader/export_grades/?", ExportGradesHandler),
    (r"/grader/export_common/?", ExportGeneralHandler),
    (r"/grader/students/?", StudentsHandler),
]
