import unittest

from e2xgrader.graders import MultipleChoiceGrader
from ..test_utils.test_utils import create_multiplechoice_cell


class TestMultipleChoiceGrader(unittest.TestCase):
    def test_correct_answer(self):
        grader = MultipleChoiceGrader()
        cell = create_multiplechoice_cell("mycell", [0], [0], 3, 10)
        points, max_points = grader.determine_grade(cell)
        assert points == max_points
        assert points == 10

    def test_partially_correct_answer(self):
        grader = MultipleChoiceGrader()
        cell = create_multiplechoice_cell("mycell", [0], [0, 1], 3, 6)
        points, max_points = grader.determine_grade(cell)
        assert points == 2

    def test_incorrect_answer(self):
        grader = MultipleChoiceGrader()
        cell = create_multiplechoice_cell("mycell", [2], [0, 1], 3, 6)
        points, max_points = grader.determine_grade(cell)
        assert points == 0
