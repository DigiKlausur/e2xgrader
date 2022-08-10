import unittest

from nbformat.v4 import new_code_cell, new_markdown_cell

from e2xgrader.preprocessors import ClearHiddenTests
from e2xgrader.utils.extra_cells import get_choices


class TestClearHiddenTests(unittest.TestCase):
    def test_choice_cell(self):
        cell = new_markdown_cell()

        cell.metadata = {
            "extended_cell": {
                "choice": ["1", "2"],
                "num_of_choices": 3,
                "type": "multiplechoice",
            },
            "nbgrader": {
                "grade": True,
                "grade_id": "Potato_B",
                "locked": False,
                "points": 5,
                "schema_version": 3,
                "solution": True,
                "task": False,
            },
        }

        cell.source = """### Multiplechoice Question
                         - Choice 1
                         - Choice 2
                         - Choice 3"""

        assert len(get_choices(cell)) == 2
        assert all([i in get_choices(cell) for i in [1, 2]])

        processed_cell, resources = ClearHiddenTests().preprocess_cell(cell, {}, 0)
        assert len(get_choices(processed_cell)) == 0

    def test_code_cell(self):
        cell = new_code_cell()

        cell.metadata = {
            "nbgrader": {
                "grade": True,
                "grade_id": "Potato_B",
                "locked": False,
                "points": 5,
                "schema_version": 3,
                "solution": False,
                "task": False,
            },
        }

        cell.source = """### BEGIN HIDDEN TESTS
        assert 1 == 1
        ###END HIDDEN TESTS"""

        processed_cell, resources = ClearHiddenTests().preprocess_cell(cell, {}, 0)
        assert processed_cell.source == ""
