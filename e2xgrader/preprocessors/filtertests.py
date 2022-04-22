from nbgrader.preprocessors import NbGraderPreprocessor
from nbformat.notebooknode import NotebookNode
from nbconvert.exporters.exporter import ResourcesDict
from traitlets import Bool
from typing import Tuple
from nbgrader.utils import is_grade, is_solution


class FilterTests(NbGraderPreprocessor):

    hide_cells = Bool(
        False, help="Hide test cells in the feedback generated for students."
    ).tag(config=True)

    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, cell_index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if self.hide_cells:
            if not is_solution(cell) and is_grade(cell):
                cell.source = "# This test case is hidden #"
        return cell, resources
