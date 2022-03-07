from .base import BaseGrader
from nbformat.notebooknode import NotebookNode
from logging import Logger
from typing import Optional, Tuple
from ..utils.extra_cells import get_form_answers


class FormCellGrader(BaseGrader):
    def determine_grade(
        self, cell: NotebookNode, log: Logger = None
    ) -> Tuple[Optional[float], float]:
        max_points = float(cell.metadata["nbgrader"]["points"])

        return None, max_points
