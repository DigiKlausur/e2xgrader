from logging import Logger
from typing import Optional, Tuple

from nbformat.notebooknode import NotebookNode

from ..utils.extra_cells import get_choices, get_instructor_choices
from .base import BaseGrader


class SingleChoiceGrader(BaseGrader):
    def determine_grade(
        self, cell: NotebookNode, log: Logger = None
    ) -> Tuple[Optional[float], float]:
        max_points = float(cell.metadata["nbgrader"]["points"])
        student_choices = get_choices(cell)
        instructor_choices = get_instructor_choices(cell)

        if (
            (len(student_choices) > 0)
            and (len(instructor_choices) > 0)
            and (student_choices[0] == instructor_choices[0])
        ):
            return max_points, max_points

        return 0, max_points
