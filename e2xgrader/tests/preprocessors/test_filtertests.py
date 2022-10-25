import unittest

from e2xgrader.preprocessors import FilterTests

from ..test_utils.cells import (
    new_autograded_code_cell,
    new_autograder_test_cell,
    new_manually_graded_code_cell,
    new_manually_graded_markdown_cell,
    new_readonly_code_cell,
    new_readonly_markdown_cell,
)


class TestFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = "assert 2**2 == 4"

    def test_hide_tests(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = True
        cell, _ = preprocessor.preprocess_cell(
            new_autograder_test_cell(source=self.source), {}, 0
        )
        assert cell.source == preprocessor.test_case_stub

    def test_show_test(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = False
        cell, _ = preprocessor.preprocess_cell(
            new_autograder_test_cell(source=self.source), {}, 0
        )
        assert cell.source == self.source

    def test_custom_test_stub(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = True
        custom_test_stub = "My custom message"
        preprocessor.test_case_stub = custom_test_stub
        cell, _ = preprocessor.preprocess_cell(
            new_autograder_test_cell(source=self.source), {}, 0
        )
        assert cell.source == custom_test_stub

    def test_ignore_non_test_cells(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = True

        cell, _ = preprocessor.preprocess_cell(
            new_manually_graded_code_cell(source=self.source), {}, 0
        )
        assert cell.source == self.source

        cell, _ = preprocessor.preprocess_cell(
            new_autograded_code_cell(source=self.source), {}, 0
        )
        assert cell.source == self.source

        cell, _ = preprocessor.preprocess_cell(
            new_manually_graded_markdown_cell(source=self.source), {}, 0
        )
        assert cell.source == self.source

        cell, _ = preprocessor.preprocess_cell(
            new_readonly_code_cell(source=self.source), {}, 0
        )
        assert cell.source == self.source

        cell, _ = preprocessor.preprocess_cell(
            new_readonly_markdown_cell(source=self.source), {}, 0
        )
        assert cell.source == self.source
