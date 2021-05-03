from nbgrader.apps.api import NbGraderAPI
from nbgrader.api import BaseCell, Grade, GradeCell, Gradebook
from nbgrader import utils
import nbformat
import os
import shutil


class E2xAPI(NbGraderAPI):

    def get_solution_cell_ids(self, assignment_id, notebook_id):
        """Get information about the solution cells of a notebook
        given its name.

        Arguments
        ---------
        assignment_id: string
            The name of the assignment
        notebook_id: string
            The name of the notebook

        Returns
        -------
        solution_cells: dict
            A dictionary containing information about the solution cells

        """
        solution_cells = []
        with self.gradebook as gb:
            num_submissions = len(gb.notebook_submissions(notebook_id, assignment_id))
            notebook_id = gb.find_notebook(notebook_id, assignment_id).id

            for cell_name in gb.db.query(BaseCell.name)\
                                  .filter(BaseCell.type == 'SolutionCell')\
                                  .filter(BaseCell.notebook_id == notebook_id):

                solution_cell = {
                    'name': cell_name[0],
                    'avg_score': 0,
                    'max_score': 0,
                    'needs_manual_grade': 0,
                    'autograded': 0
                }
                grade_ids = gb.db.query(BaseCell.id)\
                              .filter(BaseCell.type == 'GradeCell')\
                              .filter(BaseCell.notebook_id == notebook_id)\
                              .filter(BaseCell.name.contains(cell_name[0]))\
                              .all()
                if len(grade_ids) < 1:
                    continue

                if not gb.db.query(BaseCell.id)\
                         .filter(BaseCell.type == 'GradeCell')\
                         .filter(BaseCell.notebook_id == notebook_id)\
                         .filter(BaseCell.name == cell_name[0])\
                         .first():
                    solution_cell['autograded'] = 1

                for grade_id in grade_ids:
                    solution_cell['max_score'] += gb.db.query(GradeCell.max_score)\
                                                        .filter(GradeCell.id == grade_id[0])\
                                                        .first()[0]
                    for manual_score, auto_score, needs_manual_grade in gb.db\
                            .query(Grade.manual_score, Grade.auto_score,
                                   Grade.needs_manual_grade)\
                            .filter(Grade.cell_id == grade_id[0]):
                        solution_cell['needs_manual_grade'] = max(solution_cell['needs_manual_grade'],
                                                                  needs_manual_grade)
                        if manual_score:
                            solution_cell['avg_score'] += manual_score
                        elif auto_score:
                            solution_cell['avg_score'] += auto_score
                if num_submissions > 0:
                    solution_cell['avg_score'] /= num_submissions

                solution_cells.append(solution_cell)
            return solution_cells

    def get_task_submissions(self, assignment_id, notebook_id, task_id):
        """Get a list of submissions for a particular notebook in an assignment.

        Arguments
        ---------
        assignment_id: string
            The name of the assignment
        notebook_id: string
            The name of the notebook
        task_id: string
            The name of the solution cell

        Returns
        -------
        submissions: list
            A list of dictionaries containing information about each submission.

        """
        with self.gradebook as gb:
            notebook_uid = gb.find_notebook(notebook_id, assignment_id).id
            manual = gb.db.query(BaseCell.id)\
                          .filter(BaseCell.notebook_id == notebook_uid)\
                          .filter(BaseCell.type == 'GradeCell')\
                          .filter(BaseCell.name == task_id)\
                          .first()
            grade_ids = gb.db.query(BaseCell.id)\
                             .filter(BaseCell.notebook_id == notebook_uid)\
                             .filter(BaseCell.type == 'GradeCell')\
                             .filter(BaseCell.name.contains(task_id))\
                             .all()

            submissions = []

            for idx, submitted_notebook in enumerate(gb.notebook_submissions(notebook_id, assignment_id)):
                submission = {
                    'id': submitted_notebook.id,
                    'student': submitted_notebook.student.id,
                    'first_name': submitted_notebook.student.first_name,
                    'last_name': submitted_notebook.student.last_name,
                    'score': 0,
                    'max_score': 0,
                    'needs_manual_grade': 0,
                    'failed_tests': 0,
                    'index': idx
                }
                for grade_id in grade_ids:
                    grade, max_score = gb.db.query(Grade, GradeCell.max_score)\
                                            .filter(Grade.notebook_id == submitted_notebook.id)\
                                            .filter(Grade.cell_id == grade_id[0])\
                                            .filter(GradeCell.id == grade_id[0])\
                                            .first()
                    submission['max_score'] += max_score
                    if grade.manual_score is not None:
                        submission['score'] += grade.manual_score
                    elif grade.auto_score is not None:
                        submission['score'] += grade.auto_score
                        if grade.auto_score < max_score and not manual:
                            submission['failed_tests'] = 1
                    submission['needs_manual_grade'] = max(submission['needs_manual_grade'],
                                                           grade.needs_manual_grade)

                submissions.append(submission)

        submissions.sort(key=lambda x: x['id'])
        for idx, submission in enumerate(submissions):
            submission['index'] = idx

        return submissions

class E2X_Gradebook(Gradebook):

    def update_grade(self, grade_cell: str, notebook: str, assignment: str, student: str, **kwargs: dict) -> None:
        """Updates grade for a submissions for a particular cell in a particular notebook in an assignment.

        Arguments
        ---------
        grade_cell: string
            The name of the grade cell
        notebook_id: string
            The name of the notebook
        assignment_id: string
            The name of the assignment
        student: string
            The id of the student
        Returns
        -------
        None
        """
        try:
            grade = self.find_grade(grade_cell, notebook, assignment, student)
        except MissingEntry:
            self.logger.warning('No grade found!')
        else:
            for attr in kwargs:
                setattr(grade, attr, kwargs[attr])
            try:
                self.db.commit()
            except (IntegrityError, FlushError) as e:
                self.logger.warning('Commit to database failed!')
                self.db.rollback()
                raise InvalidEntry(*e.args)

        return None

    def list_updated_cells(self, notebook: str, assignment: str) -> dict:
        """Lists the updated autograde cell id and content from the source directory.

        Arguments
        ---------
        notebook: string
            The name of the notebook
        assignment: string
            The name of the assignment
        Returns
        -------
        updated_cells: list
            Dictionary where the keys are the ids of the cell and the values are the content.
        """
        nb = nbformat.read("source/" + assignment + "/" + notebook + ".ipynb", as_version = 4)
        source_directory = {}
        for idx, i in enumerate(nb.cells):
            if str(nb.cells[idx]['metadata']['nbgrader']['grade']) == 'True'\
            and str(nb.cells[idx]['metadata']['nbgrader']['solution']) == 'False':
                source_directory[str(nb.cells[idx]['metadata']['nbgrader']['grade_id'])] = nb.cells[idx]['source']
        
        updated_notebook = self.find_notebook(notebook, assignment)
        source_cells = updated_notebook.source_cells
        grade_cells = updated_notebook.grade_cells

        cells = [cell.name for cell in grade_cells if cell.cell_type == "code"]
        autograde_cells = [cell for cell in source_cells if cell.name in cells and cell.locked == True]

        updated_cells = []
        for cell in autograde_cells:
            if cell.name in source_directory.keys() and cell.source != source_directory[cell.name]:
                updated_cells.append(cell.name)

        return updated_cells

    def update_cell_content(self, cell_id: str, notebook: str, assignment: str) -> str:
        """Updates cell content.

        Arguments
        ---------
        cell_id: string
            The name of the cell
        notebook: string
            The name of the notebook
        assignment: string
            The name of the assignment
        cell_content: string
            The updated content of the cell
        Returns
        -------
        checksum_id: str
            Generates new checksum id after changes.
        """
        nb = nbformat.read("source/" + assignment + "/" + notebook + ".ipynb", as_version = 4)
        for i in nb.cells:
            if i['metadata']['nbgrader']['grade_id'] == cell_id:
                cell_content = i['source']
                self.update_or_create_source_cell(name = cell_id, notebook = notebook, assignment = assignment, source = cell_content)
                self.update_or_create_source_cell(name = cell_id, notebook = notebook, assignment = assignment, checksum = utils.compute_checksum(i))

                return utils.compute_checksum(i)

        return None

    def update_cell(self, cell_id: str, notebook: str, assignment: str) -> str:
        """Updates cell content.

        Arguments
        ---------
        cell_id: string
            The name of the cell
        notebook: string
            The name of the notebook
        assignment: string
            The name of the assignment
        cell_content: string
            The updated content of the cell
        Returns
        -------
        checksum_id: str
            Generates new checksum id after changes.
        """
        nb = nbformat.read("source/" + assignment + "/" + notebook + ".ipynb", as_version = 4)
        for i in nb.cells:
            if i['metadata']['nbgrader']['grade_id'] == cell_id:
                i['source'] = cell_content
                fname = "source/" + assignment + "/" + notebook + ".ipynb"
                with open(fname, 'w') as f:
                    nbformat.write(nb, f)
                
                self.update_or_create_source_cell(name = cell_id, notebook = notebook, assignment = assignment, source = cell_content)
                self.update_or_create_source_cell(name = cell_id, notebook = notebook, assignment = assignment, checksum = utils.compute_checksum(i))

                return utils.compute_checksum(i)

        return None

    def student_autograde(self, cell_id: str, notebook: str, assignment: str) -> str:
        """Updates cell content.

        Arguments
        ---------
        cell_id: string
            The name of the cell
        notebook: string
            The name of the notebook
        assignment: string
            The name of the assignment
        Returns
        -------
        None
        """
        nb = nbformat.read("source/" + assignment + "/" + notebook + ".ipynb", as_version = 4)
        grade_id = []
        autograde_id = []
        for idx, i in enumerate(nb.cells):
            if str(nb.cells[idx]['metadata']['nbgrader']['grade']) == 'True':
                grade_id.append(str(nb.cells[idx]['metadata']['nbgrader']['grade_id']))
            if str(nb.cells[idx]['metadata']['nbgrader']['grade']) == 'True'\
            and str(nb.cells[idx]['metadata']['nbgrader']['solution']) == 'False':
                autograde_id.append(str(nb.cells[idx]['metadata']['nbgrader']['grade_id']))

        src_dir = os.getcwd() + '/gradebook.db'
        dst_dir = os.getcwd() + '/gradebook_temp.db'
        shutil.copy(src_dir,dst_dir)

        grading = {}
        for i in self.students:
            grading[i.id] = {}
            for j in grade_id:
                grade = self.find_grade(grade_cell = j, notebook = 'Assignment_1', assignment = 'Assignment_1', student = i.id)
                grading[i.id][j] = grade.score
                self.update_grade(grade_cell = j, notebook = 'Assignment_1', assignment = 'Assignment_1', student = i.id, manual_score = None)

        nbg = NbGraderAPI()

        for i in self.students:
            nbg.autograde(assignment, i.id)

        for i in grading:
            grade = self.find_grade(grade_cell = cell_id, notebook = 'Assignment_1', assignment = 'Assignment_1', student = i)
            grading[i][cell_id] = grade.auto_score

        for i in self.students:
            for j in grade_id:
                self.update_grade(grade_cell = j, notebook = 'Assignment_1', assignment = 'Assignment_1', student = i.id, manual_score = float(grading[i.id][j]))

        return None