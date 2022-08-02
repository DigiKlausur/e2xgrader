from logging import Logger
from typing import Optional, Tuple

from nbformat.notebooknode import NotebookNode
from nbgrader.utils import compute_checksum, is_solution
from traitlets.config import LoggingConfigurable


class BaseGrader(LoggingConfigurable):
    def cell_changed(self, cell: NotebookNode):
        return not (
            is_solution(cell)
            and "checksum" in cell.metadata.nbgrader
            and cell.metadata.nbgrader["checksum"] == compute_checksum(cell)
        )

    def determine_grade(
        self, cell: NotebookNode, log: Logger = None
    ) -> Tuple[Optional[float], float]:
        max_points = float(cell.metadata["nbgrader"]["points"])
        return None, max_points
