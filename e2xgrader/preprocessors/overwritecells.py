import json
from typing import Tuple

from nbconvert.exporters.exporter import ResourcesDict
from nbformat.notebooknode import NotebookNode
from nbgrader.api import MissingEntry
from nbgrader.preprocessors import OverwriteCells as NbgraderOverwriteCells

from ..utils.extra_cells import is_multiplechoice, is_singlechoice


class OverwriteCells(NbgraderOverwriteCells):
    def preprocess_cell(
        self, cell: NotebookNode, resources: ResourcesDict, cell_index: int
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if not (is_singlechoice(cell) or is_multiplechoice(cell)):
            return super().preprocess_cell(cell, resources, cell_index)

        grade_id = cell.metadata.get("nbgrader", {}).get("grade_id", None)
        if grade_id is None:
            return cell, resources
        try:
            source_cell = self.gradebook.find_source_cell(
                grade_id, self.notebook_id, self.assignment_id
            )
        except MissingEntry:
            self.log.warning(f"Cell {grade_id} does not exist in database")
            del cell.metadata.nbgrader["grade_id"]
            return cell, resources

        cell.metadata.extended_cell.source = json.loads(source_cell.source)

        return cell, resources
