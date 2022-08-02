from logging import Logger
from typing import Optional, Tuple

from nbformat.notebooknode import NotebookNode
from nbgrader.utils import get_partial_grade, is_solution

from .base import BaseGrader


class CodeGrader(BaseGrader):
    def extract_grade(self, text, log: Logger = None):
        delimiter_start = "### BEGIN GRADE"
        delimiter_end = "### END GRADE"
        inside = False

        points = None

        grade_lines = []

        for line in text.split("\n"):
            if line.startswith(delimiter_start):
                inside = True
            elif line.startswith(delimiter_end):
                inside = False
                break
            elif inside:
                grade_lines.append(line)

        if len(grade_lines) > 0 and not inside:
            # Try casting result to float
            try:
                points = float("".join(grade_lines))
            except ValueError:
                pass
        return points

    def determine_grade(
        self, cell: NotebookNode, log: Logger = None
    ) -> Tuple[Optional[float], float]:
        max_points = float(cell.metadata["nbgrader"]["points"])

        if not self.cell_changed(cell):
            return 0, max_points
        elif is_solution(cell):
            return None, max_points

        for output in cell.outputs:
            # option 1: error, return 0
            if (
                output.output_type == "error"
                or output.output_type == "stream"
                and output.name == "stderr"
            ):
                return 0, max_points
            if output.output_type == "execute_result":
                partial_grade = get_partial_grade(output, max_points, log)
                return partial_grade, max_points
            if output.output_type == "stream" and output.name == "stdout":
                partial_grade = self.extract_grade(output.text, log)
                if partial_grade is not None:
                    return partial_grade, max_points

        return max_points, max_points
