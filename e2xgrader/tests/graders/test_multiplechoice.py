import unittest
from typing import List

from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_markdown_cell

from e2xgrader.graders import MultipleChoiceGrader


class TestMultipleChoiceGrader(unittest.TestCase):
    def create_multiplechoice_cell(
        self,
        grade_id: str,
        student_choices: List[int],
        instructor_choices: List[int],
        num_of_choices: int,
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
                "type": "multiplechoice",
                "num_of_choices": num_of_choices,
                "choice": student_choices,
                "source": {"choice": instructor_choices},
            },
        }

        cell.source = """
        - correct answer
        - wrong answer
        - correct answer
        """
        return cell

    def test_correct_answer(self):
        grader = MultipleChoiceGrader()
        cell = self.create_multiplechoice_cell("mycell", [0], [0], 3, 10)
        points, max_points = grader.determine_grade(cell)
        assert points == max_points
        assert points == 10

    def test_partially_correct_answer(self):
        grader = MultipleChoiceGrader()
        cell = self.create_multiplechoice_cell("mycell", [0], [0, 1], 3, 6)
        points, max_points = grader.determine_grade(cell)
        assert points == 2

    def test_incorrect_answer(self):
        grader = MultipleChoiceGrader()
        cell = self.create_multiplechoice_cell("mycell", [2], [0, 1], 3, 6)
        points, max_points = grader.determine_grade(cell)
        assert points == 0
