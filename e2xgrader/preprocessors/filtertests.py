from typing import Tuple

from nbconvert.exporters.exporter import ResourcesDict
from nbformat.notebooknode import NotebookNode
from nbgrader.preprocessors import NbGraderPreprocessor
from nbgrader.utils import is_grade, is_solution
from traitlets import Bool, Unicode


class FilterTests(NbGraderPreprocessor):
    hide_cells = Bool(
        False, help="Hide test cells in the feedback generated for students."
    ).tag(config=True)

    test_case_stub = Unicode(
        "# This test case is hidden #",
        help="The message the test case source is replaced with",
    ).tag(config=True)

    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, cell_index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if self.hide_cells and is_grade(cell) and not is_solution(cell):
            cell.source = self.test_case_stub
        return cell, resources
