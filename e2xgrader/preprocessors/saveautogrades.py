from nbformat.notebooknode import NotebookNode
from nbconvert.exporters.exporter import ResourcesDict

from nbgrader.preprocessors import SaveAutoGrades as NbgraderSaveAutoGrades

from ..utils.extra_cells import is_extra_cell
from nbgrader.utils import determine_grade
from ..graders import BaseGrader, MultipleChoiceGrader, SingleChoiceGrader, CodeGrader

from traitlets import Dict, Unicode, Instance


class SaveAutoGrades(NbgraderSaveAutoGrades):

    graders = Dict(
        key_trait=Unicode(),
        value_trait=Instance(klass=BaseGrader),
        default_value={
            "code": Code(),
            "singlechoice": SingleChoice(),
            "multiplechoice": MultipleChoice(),
        },
    ).tag(config=True)

    def cell_type(self, cell: NotebookNode):
        if is_extra_cell(cell):
            return cell.metadata.extended_cell.type
        return cell.cell_type

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
            cell.metadata["nbgrader"]["grade_id"],
            self.notebook_id,
            self.assignment_id,
            self.student_id,
        )

        # determine what the grade is
        if self.cell_type(cell) in self.graders:
            auto_score, _ = self.graders[self.cell_type(cell)].determine_grade(
                cell, self.log
            )
            grade.auto_score = auto_score
        else:
            auto_score, _ = determine_grade(cell, self.log)
            grade.auto_score = auto_score

        # if there was previously a manual grade, or if there is no autograder
        # score, then we should mark this as needing review
        if (grade.manual_score is not None) or (grade.auto_score is None):
            grade.needs_manual_grade = True
        else:
            grade.needs_manual_grade = False

        self.gradebook.db.commit()
