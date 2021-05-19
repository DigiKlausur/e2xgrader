import json
import os

from tornado import web
from nbgrader.server_extensions.formgrader.base import check_xsrf

from .base import E2xBaseApiHandler as BaseApiHandler
from e2xgrader.apps.api import E2xGradebook
from multiprocessing import Process, Value
from ctypes import c_wchar_p

autograde_assignment = Value(c_wchar_p, '')


class ListCells(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        gb = E2xGradebook(self.api.coursedir.db_url)
        notebook = self.api.gradebook.find_assignment(assignment_id).notebooks[0].name
        cells = gb.list_autograde_testcells(notebook, assignment_id)
        self.write(json.dumps(cells))


class AutogradeLog(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        try:
            with open(os.path.join(os.getcwd(), 'log', assignment_id + '.txt')) as json_file:
                autograde_log = json_file.read()
        except FileNotFoundError:
            autograde_log = 'Autograding required.'
        else:
            raise Exception("Error while accessing log file.")
        result = {'autograde_log' : autograde_log}
        self.write(json.dumps(result))


class AutogradeAll(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        autograde_assignment.value = str(assignment_id)
        p = Process(target = self.api.autograde_all, args = (assignment_id,))
        p.start()


class AutogradeCells(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        selected_cells = self.get_argument('cell_ids')
        selected_cells = str(selected_cells).split(",")
        print(selected_cells)
        autograde_assignment.value = str(assignment_id)
        p = Process(target = self.api.autograde_cells, args = (assignment_id, selected_cells,))
        p.start()


class AutogradingProgess(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        try:
            with open(os.path.join(os.getcwd(), 'log/') + assignment_id + '.txt') as json_file:
                data = json.load(json_file)
                autograde_log = data['time']
        except:
            autograde_log = 'Autograding required.'
        result = {'autograde_idx' : self.api.autograde_idx.value,
                  'autograde_total' : self.api.autograde_total.value,
                  'autograde_flag' : self.api.autograde_flag.value,
                  'autograde_log' : autograde_log,
                  'autograde_assignment' : autograde_assignment.value}
        self.write(json.dumps(result))


class UpdateNotebook(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        notebook_id = self.get_argument('notebook_id')
        cells = self.get_argument('cells')
        cells = eval(cells.split()[0])
        db_url = 'sqlite:///' + os.path.join(os.getcwd(), 'gradebook.db')
        gb = E2xGradebook(db_url)
        checksum_id = []
        for cell in cells:
            checksum_single = gb.update_cell_content(cell, notebook_id, assignment_id)
            checksum_id.append(checksum_single)
            gb.update_or_create_source_cell(name = cell, notebook = notebook_id, assignment = assignment_id, checksum = checksum_single)
        self.write(json.dumps(checksum_id))


class FindUpdatedCells(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        notebook_id = self.get_argument('notebook_id')
        db_url = 'sqlite:///' + os.path.join(os.getcwd(), 'gradebook.db')
        gb = E2xGradebook(db_url)
        updated_cells = gb.list_updated_cells(notebook_id, assignment_id)
        self.write(json.dumps(updated_cells))


class GetNotebook(BaseApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        assignment_id = self.get_argument('assignment_id')
        db_url = 'sqlite:///' + os.path.join(os.getcwd(), 'gradebook.db')
        gb = E2xGradebook(db_url)
        assignment_object = gb.find_assignment(assignment_id)
        notebooks = []
        for assignment in assignment_object.notebooks:
            notebooks.append(assignment.name)
        self.write(json.dumps(notebooks))


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


default_handlers = [
    (r"/formgrader/api/solution_cells/([^/]+)/([^/]+)", SolutionCellCollectionHandler),
    (r"/formgrader/api/submitted_tasks/([^/]+)/([^/]+)/([^/]+)", SubmittedTaskCollectionHandler),
    (r'/formgrader/api/get_notebook/?', GetNotebook),
    (r'/formgrader/api/find_updated_cell/?', FindUpdatedCells),
    (r'/formgrader/api/update_notebook/?', UpdateNotebook),
    (r'/formgrader/api/autograde_all/?', AutogradeAll),
    (r'/formgrader/api/autograde_cells/?', AutogradeCells),
    (r'/formgrader/api/autograding_log/?', AutogradeLog),
    (r'/formgrader/api/list_cells/?', ListCells),
    (r'/formgrader/api/autograding_progress/?', AutogradingProgess),
]
