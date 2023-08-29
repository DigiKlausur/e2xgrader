from textwrap import dedent
from typing import Tuple

from e2xcore.utils.e2xgrader_cells import is_extra_cell
from e2xcore.utils.nbgrader_cells import grade_id
from nbconvert.exporters.exporter import ResourcesDict
from nbformat.notebooknode import NotebookNode
from nbgrader.api import Gradebook
from nbgrader.preprocessors import SaveAutoGrades as NbgraderSaveAutoGrades
from nbgrader.utils import determine_grade
from traitlets import Dict, Instance, List, TraitError, Unicode, validate

from ..graders import BaseGrader, CodeGrader, MultipleChoiceGrader, SingleChoiceGrader


class SaveAutoGrades(NbgraderSaveAutoGrades):
    graders = Dict(
        key_trait=Unicode(),
        value_trait=Instance(klass=BaseGrader),
        default_value={
            "code": CodeGrader(),
            "singlechoice": SingleChoiceGrader(),
            "multiplechoice": MultipleChoiceGrader(),
        },
    ).tag(config=True)

    cells = List(
        [],
        help=dedent(
            """
            List of cells to save the autogrades for. If this is empty all cells will be saved.
            """
        ),
    ).tag(config=True)

    @validate("cells")
    def _validate_cells(self, proposal):
        value = proposal["value"]
        if len(value) == 1:
            elem = value[0].strip()
            if elem.startswith("[") and elem.endswith("]"):
                elem = elem[1:-1]
            value = [v.strip() for v in elem.split(",")]
        if not isinstance(value, list):
            raise TraitError("cells must be a list")
        return value

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

    def preprocess(
        self, nb: NotebookNode, resources: ResourcesDict
    ) -> Tuple[NotebookNode, ResourcesDict]:
        # pull information from the resources
        self.notebook_id = resources["nbgrader"]["notebook"]
        self.assignment_id = resources["nbgrader"]["assignment"]
        self.student_id = resources["nbgrader"]["student"]
        self.db_url = resources["nbgrader"]["db_url"]

        # connect to the database
        self.gradebook = Gradebook(self.db_url)

        with self.gradebook:
            # process the cells
            nb, resources = super(SaveAutoGrades, self).preprocess(nb, resources)

        return nb, resources

    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, cell_index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if len(self.cells) == 0 or grade_id(cell) in self.cells:
            return super().preprocess_cell(cell, resources, cell_index)
        return cell, resources
