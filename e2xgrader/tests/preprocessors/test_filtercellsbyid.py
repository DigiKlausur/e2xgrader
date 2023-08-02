import unittest

from e2xcore.utils.nbgrader_cells import grade_id
from nbformat.v4 import new_notebook

from e2xgrader.preprocessors import FilterCellsById
from e2xgrader.tests.test_utils.cells import (
    new_autograded_code_cell,
    new_autograder_test_cell,
    new_manually_graded_code_cell,
    new_readonly_markdown_cell,
)


class TestFilterCellsById(unittest.TestCase):
    def setUp(self):
        self.nb = new_notebook()
        self.nb.cells.append(
            new_readonly_markdown_cell(source="", grade_id="Task1_Task2_Description")
        )
        self.nb.cells.append(new_manually_graded_code_cell(source="", grade_id="Task1"))
        self.nb.cells.append(
            new_readonly_markdown_cell(source="", grade_id="Task2_Description")
        )
        self.nb.cells.append(new_autograded_code_cell(source="", grade_id="Task2"))
        self.nb.cells.append(new_autograder_test_cell(source="", grade_id="test_Task2"))
        self.nb.cells.append(new_readonly_markdown_cell(source="", grade_id="Task3"))
        self.grade_ids = [grade_id(cell) for cell in self.nb.cells]

    def test_no_keyword(self):
        processed_nb, _ = FilterCellsById().preprocess(self.nb, {})
        processed_cell_ids = [grade_id(cell) for cell in processed_nb.cells]
        assert all([idx in processed_cell_ids for idx in self.grade_ids])

    def test_empty_keyword(self):
        processed_nb, _ = FilterCellsById().preprocess(self.nb, {"keyword": ""})
        processed_cell_ids = [grade_id(cell) for cell in processed_nb.cells]
        assert all([idx in processed_cell_ids for idx in self.grade_ids])

    def test_non_empty_keyword(self):
        keyword = "Task2"
        processed_nb, _ = FilterCellsById().preprocess(self.nb, dict(keyword=keyword))
        processed_cell_ids = [grade_id(cell) for cell in processed_nb.cells]
        assert len(processed_cell_ids) == 4
        assert all([keyword in idx for idx in processed_cell_ids])
