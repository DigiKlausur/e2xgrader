import unittest

from nbformat.v4 import new_code_cell

from e2xgrader import preprocessors
from e2xgrader.preprocessors import FilterTests


class TestFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_source = "assert 2**2 == 4"
        self.test_cell = new_code_cell(
            source=self.original_source,
            metadata={
                "nbgrader": {
                    "grade": True,
                    "grade_id": "Potato_B",
                    "locked": False,
                    "points": 5,
                    "schema_version": 3,
                    "solution": False,
                    "task": False,
                }
            },
        )

    def test_hide_tests(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = True
        cell, _ = preprocessor.preprocess_cell(self.test_cell, {}, 0)
        assert cell.source == preprocessor.test_case_stub

    def test_show_test(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = False
        cell, _ = preprocessor.preprocess_cell(self.test_cell, {}, 0)
        assert cell.source == self.original_source

    def test_custom_test_stub(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = True
        preprocessor.test_case_stub = "My custom message"
        cell, _ = preprocessor.preprocess_cell(self.test_cell, {}, 0)
        assert cell.source == preprocessor.test_case_stub
