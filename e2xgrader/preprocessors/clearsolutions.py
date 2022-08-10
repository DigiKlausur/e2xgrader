from typing import Tuple

from nbconvert.exporters.exporter import ResourcesDict
from nbformat.notebooknode import NotebookNode
from nbgrader.preprocessors import ClearSolutions as NbgraderClearSolutions

from ..utils.extra_cells import get_options, is_diagram, is_extra_cell


class ClearSolutions(NbgraderClearSolutions):
    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, cell_index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if is_extra_cell(cell):
            if is_diagram(cell):
                # Check whether we want to remove the diagram
                options = get_options(cell)
                if options.get("replace_diagram", True):
                    del cell.attachments["diagram.png"]

            return cell, resources
        else:
            return super().preprocess_cell(cell, resources, cell_index)
