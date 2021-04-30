from traitlets.config import LoggingConfigurable
from nbgrader.api import MissingEntry
import pandas as pd


class GradeTaskExporter(LoggingConfigurable):

    def __init__(self, gradebook):
        self.gb = gradebook

    def get_columns(self):
        columns = []
        assignments = sorted(self.gb.assignments, key=lambda x: x.name)
        for assignment in assignments:
            for notebook in assignment.notebooks:
                for gradecell in notebook.grade_cells:
                    name = gradecell.name
                    if name.startswith('test_'):
                        name = gradecell.name[5:]
                    columns.append((assignment.name, notebook.name, name))
        return columns

    def make_table(self):
        data = []

        assignments = sorted(self.gb.assignments, key=lambda x: x.name)
        columns = ['Student ID'] + ['.'.join(col) for col in self.get_columns()]

        for student in self.gb.students:
            row = [student.id]
            for assignment in assignments:
                for notebook in assignment.notebooks:
                    for gradecell in notebook.grade_cells:
                        score = 0
                        try:
                            submission = self.gb.find_grade(gradecell.name, notebook.name, assignment.name, student.id)
                            score = submission.score
                        except MissingEntry:
                            pass
                        finally:
                            row.append(score)

            data.append(row)

        table = pd.DataFrame(data, columns=columns)
        table['Total'] = table.sum(axis=1, numeric_only=True)
        return table

class GradeSelectedAssignmentExporter(LoggingConfigurable):
    
    def __init__(self, gradebook, selected_assignments):
        self.gb = gradebook
        self.selected_assignments = selected_assignments

    def make_table(self):
        data = []
        
        assignments = sorted(self.selected_assignments)
        columns = ['Student ID'] + [assignment for assignment in assignments]

        for student in self.gb.students:
            row = [student.id]
            for assignment in assignments:
                score = 0
                try:
                    submission = self.gb.find_submission(assignment, student.id)
                    score = submission.score                     
                except MissingEntry:
                    pass
                finally:
                    row.append(score)
                
            data.append(row)
            
        table = pd.DataFrame(data, columns=columns)        
        table['Total'] = table.sum(axis=1, numeric_only=True)
        return table

class GradeAssignmentExporter(LoggingConfigurable):

    def __init__(self, gradebook):
        self.gb = gradebook

    def make_table(self):
        data = []

        assignments = sorted(self.gb.assignments, key=lambda x: x.name)
        columns = ['Student ID'] + [assignment.name for assignment in assignments]

        for student in self.gb.students:
            row = [student.id]
            for assignment in assignments:
                score = 0
                try:
                    submission = self.gb.find_submission(assignment.name, student.id)
                    score = submission.score
                except MissingEntry:
                    pass
                finally:
                    row.append(score)

            data.append(row)

        table = pd.DataFrame(data, columns=columns)
        table['Total'] = table.sum(axis=1, numeric_only=True)
        return table


class GradeNotebookExporter(LoggingConfigurable):

    def __init__(self, gradebook):
        self.gb = gradebook

    def get_columns(self):
        columns = []
        assignments = sorted(self.gb.assignments, key=lambda x: x.name)
        for assignment in assignments:
            for notebook in assignment.notebooks:
                columns.append((assignment.name, notebook.name))
        return columns

    def make_table(self):
        data = []

        assignments = sorted(self.gb.assignments, key=lambda x: x.name)
        columns = ['Student ID'] + ['.'.join(col) for col in self.get_columns()]

        for student in self.gb.students:
            row = [student.id]
            for assignment in assignments:
                for notebook in assignment.notebooks:
                    score = 0
                    try:
                        submission = self.gb.find_submission_notebook(notebook.name, assignment.name, student.id)
                        score = submission.score
                    except MissingEntry:
                        pass
                    finally:
                        row.append(score)

            data.append(row)

        table = pd.DataFrame(data, columns=columns)
        table['Total'] = table.sum(axis=1, numeric_only=True)
        return table
