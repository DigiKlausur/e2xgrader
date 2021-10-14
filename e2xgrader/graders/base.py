from traitlets.config import LoggingConfigurable
from nbformat.notebooknode import NotebookNode
from logging import Logger
from typing import Optional, Tuple
from nbgrader.utils import is_solution, compute_checksum


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
