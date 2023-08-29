import json

from nbformat.notebooknode import NotebookNode
from nbgrader import utils
from nbgrader.api import MissingEntry
from nbgrader.preprocessors import SaveCells as NbgraderSaveCells

from ..utils.extra_cells import is_multiplechoice, is_singlechoice


class SaveCells(NbgraderSaveCells):
    def _create_source_cell(self, cell: NotebookNode) -> None:
        grade_id = cell.metadata.nbgrader["grade_id"]

        try:
            source_cell = self.gradebook.find_source_cell(
                grade_id, self.notebook_id, self.assignment_id
            ).to_dict()
            del source_cell["name"]
            del source_cell["notebook"]
            del source_cell["assignment"]
        except MissingEntry:
            source_cell = {}

        source = cell.source

        if is_singlechoice(cell) or is_multiplechoice(cell):
            source = json.dumps(cell.metadata.extended_cell)

        source_cell.update(
            {
                "cell_type": cell.cell_type,
                "locked": utils.is_locked(cell),
                "source": source,
                "checksum": cell.metadata.nbgrader.get("checksum", None),
            }
        )

        self.new_source_cells[grade_id] = source_cell
