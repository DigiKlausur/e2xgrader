from nbformat.notebooknode import NotebookNode
from nbconvert.exporters.exporter import ResourcesDict
from typing import Tuple

from nbgrader.preprocessors import ClearHiddenTests as NbgraderClearHiddenTests

from ..utils.extra_cells import is_singlechoice, is_multiplechoice, clear_choices

class ClearHiddenTests(NbgraderClearHiddenTests):

    def preprocess_cell(self, 
                        cell: NotebookNode, 
                        resources: ResourcesDict,
                        cell_index: int
                        ) -> Tuple[NotebookNode, ResourcesDict]:
        if is_singlechoice(cell) or is_multiplechoice(cell):
            clear_choices(cell)
            return cell, resources
        else:
            return super().preprocess_cell(cell, resources, cell_index)