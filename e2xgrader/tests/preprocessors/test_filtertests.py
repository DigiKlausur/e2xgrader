import unittest
from nbformat.v4 import new_code_cell

from e2xgrader.preprocessors import FilterTests


class TestFilterTests(unittest.TestCase):
    def setUp(self):
        self.test_cell = new_code_cell(
            "#Test source",
            metadata={
                "nbgrader": {
                    "grade": True,
                    "grade_id": "some_id",
                    "solution": False,
                    "locked": True,
                    "schema_version": 3,
                    "task": 3,
                }
            },
        )

        self.solution_cell = new_code_cell(
            "#Solution source",
            metadata={
                "nbgrader": {
                    "grade": True,
                    "grade_id": "some_id",
                    "solution": True,
                    "locked": True,
                    "schema_version": 3,
                    "task": 3,
                }
            },
        )

    def test_show_tests(self):
        cell, resources = FilterTests().preprocess_cell(self.test_cell, {}, 0)
        assert cell.source == self.test_cell.source

        cell, resources = FilterTests().preprocess_cell(self.solution_cell, {}, 0)
        assert cell.source == self.solution_cell.source

    def test_hide_tests(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = True
        cell, resources = preprocessor.preprocess_cell(self.test_cell, {}, 0)
        assert cell.source == preprocessor.test_stub

        cell, resources = preprocessor.preprocess_cell(self.solution_cell, {}, 0)
        assert cell.source == self.solution_cell.source
