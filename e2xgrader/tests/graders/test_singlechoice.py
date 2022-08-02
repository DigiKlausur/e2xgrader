import unittest
from typing import List

from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_markdown_cell

from e2xgrader.graders import SingleChoiceGrader


class TestSingleChoiceGrader(unittest.TestCase):
    def create_singlechoice_cell(
        self,
        grade_id: str,
        student_choices: List[int],
        instructor_choices: List[int],
        points: int = 5,
    ) -> NotebookNode:
        cell = new_markdown_cell()

        cell.metadata = {
            "nbgrader": {
                "grade": True,
                "grade_id": grade_id,
                "locked": False,
                "points": points,
                "schema_version": 3,
                "solution": True,
                "task": False,
            },
            "extended_cell": {
                "type": "singlechoice",
                "choice": student_choices,
                "source": {"choice": instructor_choices},
            },
        }

        cell.source = """
        - correct answer
        - wrong answer
        """
        return cell

    def test_correct_answer(self):
        grader = SingleChoiceGrader()
        cell = self.create_singlechoice_cell("mycell", [0], [0], 10)
        points, max_points = grader.determine_grade(cell)
        assert points == max_points
        assert points == 10

    def test_incorrect_answer(self):
        grader = SingleChoiceGrader()
        cell = self.create_singlechoice_cell("mycell", [1], [0], 10)
        points, max_points = grader.determine_grade(cell)
        assert max_points == 10
        assert points == 0
