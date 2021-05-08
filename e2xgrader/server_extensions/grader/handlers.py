import os
import sys

from tornado import web

from .base import BaseHandler, check_xsrf

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

class AssignmentsCommonHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id', None)
        html = self.render(
            "assignment_details.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            assignment_id = assignment_id,
            windows=(sys.prefix == 'win32'))
        self.write(html)

class GraderCommonHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id', None)
        html = self.render(
            "grading_common.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            assignment_id = assignment_id,
            windows=(sys.prefix == 'win32'))
        self.write(html)

class ExchangeCommonHandler(BaseHandler):

    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id', None)
        html = self.render(
            "exchange_common.tpl",
            url_prefix=self.url_prefix,
            base_url=self.base_url,
            assignment_id = assignment_id,
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
    (r"/grader/assignments/assignment_common/?", AssignmentsCommonHandler),
    (r"/grader/assignments/assignment_common/grading_common/?", GraderCommonHandler),
    (r"/grader/assignments/assignment_common/exchange_common/?", ExchangeCommonHandler),
    (r"/grader/students/?", StudentsHandler),
]
