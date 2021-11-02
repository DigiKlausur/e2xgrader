from nbgrader.preprocessors import NbGraderPreprocessor
from nbformat.notebooknode import NotebookNode
from nbconvert.exporters.exporter import ResourcesDict
from traitlets import Bool
from typing import Tuple


class FilterTests(NbGraderPreprocessor):

    hide_cells = Bool(
        False, help="Hide test cells in the feedback generated for students."
    ).tag(config=True)

    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, cell_index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if self.hide_cells:
            if (
                cell.cell_type == "code"
                and cell.metadata.nbgrader.grade == True
                and cell.metadata.nbgrader.solution == False
            ):
                cell.source = ""
        return cell, resources
