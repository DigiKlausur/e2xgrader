from typing import Tuple

from nbconvert.exporters.exporter import ResourcesDict
from nbformat.notebooknode import NotebookNode
from nbgrader.preprocessors import ClearHiddenTests as NbgraderClearHiddenTests

from ..utils.extra_cells import clear_choices, is_multiplechoice, is_singlechoice


class ClearHiddenTests(NbgraderClearHiddenTests):
    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, cell_index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if is_singlechoice(cell) or is_multiplechoice(cell):
            clear_choices(cell)
            return cell, resources
        else:
            return super().preprocess_cell(cell, resources, cell_index)
