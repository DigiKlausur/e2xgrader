from nbformat.notebooknode import NotebookNode
from nbconvert.exporters.exporter import ResourcesDict
from typing import Tuple

from nbgrader.preprocessors import ClearSolutions as NbgraderClearSolutions

from ..utils.extra_cells import is_extra_cell


class ClearSolutions(NbgraderClearSolutions):

    def preprocess_cell(self,
                        cell: NotebookNode,
                        resources: ResourcesDict,
                        cell_index: int
                        ) -> Tuple[NotebookNode, ResourcesDict]:
        if is_extra_cell(cell):
            return cell, resources
        else:
            return super().preprocess_cell(cell, resources, cell_index)
