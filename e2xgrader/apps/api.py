
from nbgrader.apps.api import NbGraderAPI
from nbgrader.api import BaseCell, Grade, GradeCell

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
                    avg_score = 0
                    submissions = 0
                    for manual_score, auto_score, needs_manual_grade in gb.db\
                            .query(Grade.manual_score, Grade.auto_score,\
                                   Grade.needs_manual_grade)\
                            .filter(Grade.cell_id == grade_id[0]):
                        solution_cell['needs_manual_grade'] = max(solution_cell['needs_manual_grade'], \
                                                                  needs_manual_grade)
                        if manual_score:
                            solution_cell['avg_score'] += manual_score
                        elif auto_score:
                            solution_cell['avg_score'] += auto_score
                if num_submissions > 0:
                    solution_cell['avg_score'] /= num_submissions
                            
                solution_cells.append(solution_cell)
            return solution_cells

    def get_grade_cell(self, notebook_id, solution_cell_name):
        with self.gradebook as gb:            
            grade_cell = gb.db.query(GradeCell.id, GradeCell.name, GradeCell.max_score)\
                .filter(GradeCell.notebook_id == notebook_id, GradeCell.name == solution_cell_name).first()
            if grade_cell is None:
                grade_cell = gb.db.query(GradeCell.id, GradeCell.name, GradeCell.max_score)\
                .filter(GradeCell.notebook_id == notebook_id, GradeCell.name == 'test_{}'.format(solution_cell_name)).first()
            return grade_cell


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
                    submission['needs_manual_grade'] = max(submission['needs_manual_grade'], \
                                                           grade.needs_manual_grade)
                    
                submissions.append(submission)

        submissions.sort(key=lambda x: x['id'])
        for idx, submission in enumerate(submissions):
            submission['index'] = idx
                
        return submissions