from nbformat.notebooknode import NotebookNode
from nbconvert.exporters.exporter import ResourcesDict

from nbgrader.preprocessors import SaveAutoGrades as NbgraderSaveAutoGrades

from ..utils.extra_cells import determine_grade


class SaveAutoGrades(NbgraderSaveAutoGrades):

    def _add_score(self, cell: NotebookNode, resources: ResourcesDict) -> None:
        """Graders can override the autograder grades, and may need to
        manually grade written solutions anyway. This function adds
        score information to the database if it doesn't exist. It does
        NOT override the 'score' field, as this is the manual score
        that might have been provided by a grader.

        """
        # these are the fields by which we will identify the score
        # information
        grade = self.gradebook.find_grade(
            cell.metadata['nbgrader']['grade_id'],
            self.notebook_id,
            self.assignment_id,
            self.student_id)

        # determine what the grade is
        auto_score, _ = determine_grade(cell, self.log)
        grade.auto_score = auto_score

        # if there was previously a manual grade, or if there is no autograder
        # score, then we should mark this as needing review
        if (grade.manual_score is not None) or (grade.auto_score is None):
            grade.needs_manual_grade = True
        else:
            grade.needs_manual_grade = False

        self.gradebook.db.commit()
