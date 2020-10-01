import os

from tornado import web
from nbgrader.server_extensions.formgrader.base import BaseHandler, check_xsrf

from ...exporters import GradeTaskExporter, GradeNotebookExporter, GradeAssignmentExporter

class ExportGradesHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        html = self.render(
            'export_grades.tpl',
            base_url = self.base_url
        )
        self.write(html)

class ExportAssignmentGradesHandler(BaseHandler):
    def initialize(self):
        self.__exporter = GradeAssignmentExporter(self.gradebook)

    @web.authenticated
    @check_xsrf
    def get(self):
        self.set_header('Content-Type', 'text/csv; charset="utf-8"')
        self.set_header('Content-Disposition', 'attachment; filename=grades.csv')
        self.write(self.__exporter.make_table().to_csv(index=False))
        self.finish()

class ExportNotebookGradesHandler(BaseHandler):
    def initialize(self):
        self.__exporter = GradeNotebookExporter(self.gradebook)

    @web.authenticated
    @check_xsrf
    def get(self):
        self.set_header('Content-Type', 'text/csv; charset="utf-8"')
        self.set_header('Content-Disposition', 'attachment; filename=grades.csv')
        self.write(self.__exporter.make_table().to_csv(index=False))
        self.finish()

class ExportTaskGradesHandler(BaseHandler):
    def initialize(self):
        self.__exporter = GradeTaskExporter(self.gradebook)

    @web.authenticated
    @check_xsrf
    def get(self):
        self.set_header('Content-Type', 'text/csv; charset="utf-8"')
        self.set_header('Content-Disposition', 'attachment; filename=grades.csv')
        self.write(self.__exporter.make_table().to_csv(index=False))
        self.finish()


root_path = os.path.dirname(__file__)
template_path = os.path.join(root_path, 'templates')

default_handlers = [
    (r'/e2xgrader/export_grades/?', ExportGradesHandler),
    (r'/e2xgrader/export_grades/assignments/?', ExportAssignmentGradesHandler),
    (r'/e2xgrader/export_grades/notebooks/?', ExportNotebookGradesHandler),
    (r'/e2xgrader/export_grades/tasks/?', ExportTaskGradesHandler)
]