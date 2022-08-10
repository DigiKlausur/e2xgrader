from logging import Logger
from typing import Optional, Tuple

from nbformat.notebooknode import NotebookNode

from ..utils.extra_cells import get_choices, get_instructor_choices, get_num_of_choices
from .base import BaseGrader


class MultipleChoiceGrader(BaseGrader):
    def determine_grade(
        self, cell: NotebookNode, log: Logger = None
    ) -> Tuple[Optional[float], float]:
        max_points = float(cell.metadata["nbgrader"]["points"])
        student_choices = get_choices(cell)
        instructor_choices = get_instructor_choices(cell)
        option_points = max_points / get_num_of_choices(cell)

        points = 0

        for i in range(get_num_of_choices(cell)):
            if ((i in student_choices) and (i in instructor_choices)) or (
                (i not in student_choices) and (i not in instructor_choices)
            ):
                points += option_points
            else:
                points -= option_points

        return max(0, round(points, 1)), max_points
