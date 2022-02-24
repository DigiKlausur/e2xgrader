import unittest

from e2xgrader.graders import SingleChoiceGrader

from ..test_utils.test_utils import create_singlechoice_cell


class TestSingleChoiceGrader(unittest.TestCase):
    def test_correct_answer(self):
        grader = SingleChoiceGrader()
        cell = create_singlechoice_cell("mycell", [0], [0], 10)
        points, max_points = grader.determine_grade(cell)
        assert points == max_points
        assert points == 10

    def test_incorrect_answer(self):
        grader = SingleChoiceGrader()
        cell = create_singlechoice_cell("mycell", [1], [0], 10)
        points, max_points = grader.determine_grade(cell)
        assert max_points == 10
        assert points == 0
