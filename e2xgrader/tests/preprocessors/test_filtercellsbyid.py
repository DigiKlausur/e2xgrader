import unittest
from nbformat.v4 import new_markdown_cell, new_notebook

from e2xgrader.utils.nbgrader_cells import grade_id
from e2xgrader.preprocessors import FilterCellsById


class TestFilterCellsById(unittest.TestCase):
    def setUp(self):
        self.grade_ids = ["Task", "Task1", "Task12", "Task123", "Task1234", "Task12345"]
        self.nb = new_notebook()

        for idx in self.grade_ids:
            cell = new_markdown_cell()
            cell.metadata = {
                "nbgrader": {
                    "grade": False,
                    "grade_id": idx,
                    "solution": True,
                    "locked": False,
                    "schema_version": 3,
                    "task": False,
                }
            }
            self.nb.cells.append(cell)

    def test_no_keyword(self):
        resources = {}
        processed_nb, resources = FilterCellsById().preprocess(self.nb, resources)
        processed_cell_ids = [grade_id(cell) for cell in processed_nb.cells]
        assert all([idx in processed_cell_ids for idx in self.grade_ids])

    def test_empty_keyword(self):
        resources = {"keyword": ""}
        processed_nb, resources = FilterCellsById().preprocess(self.nb, resources)
        processed_cell_ids = [grade_id(cell) for cell in processed_nb.cells]
        assert all([idx in processed_cell_ids for idx in self.grade_ids])

    def test_non_empty_keyword(self):
        resources = {"keyword": "Task12345"}
        processed_nb, resources = FilterCellsById().preprocess(self.nb, resources)
        processed_cell_ids = [grade_id(cell) for cell in processed_nb.cells]
        assert len(processed_cell_ids) == 1
        assert processed_cell_ids[0] == "Task12345"

    def test_non_empty_keyword(self):
        keyword = "Task123"
        resources = {"keyword": keyword}
        processed_nb, resources = FilterCellsById().preprocess(self.nb, resources)
        processed_cell_ids = [grade_id(cell) for cell in processed_nb.cells]
        assert len(processed_cell_ids) == 3
        assert all([keyword in idx for idx in processed_cell_ids])
