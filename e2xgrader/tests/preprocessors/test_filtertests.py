import unittest
from nbformat.v4 import new_markdown_cell, new_notebook, new_code_cell
from e2xgrader.utils.nbgrader_cells import grade_id
from e2xgrader.preprocessors import FilterTests

class TestFilterTests(unittest.TestCase):
    check_source = "# This test case is hidden #"
    def setUp(self):
        self.grade_ids = ["Task", "Task1"]
        self.truths = [True, False]
        self.nb = new_notebook()

        for idx in self.grade_ids:
            for truth in self.truths:
                cell = new_code_cell()
                cell.metadata = {
                    "nbgrader": {
                     "grade": truth,
                     "grade_id": str(idx) + str(truth),
                     "locked": True,
                     "points": 10,
                     "schema_version": 3,
                     "solution": False,
                     "task": False
                    }
                }
                cell.source = [
                "#THIS IS A TEST CELL!!!\n",
                "\n",
                "### BEGIN HIDDEN TESTS\n",
                "# Test cell.",
                "### END HIDDEN TESTS"
                ]
                self.nb.cells.append(cell)

    def hide_cells_true(self):
        ft = FilterTests()
        ft.hide_cells = True
        for cell in self.nb.cells:
            processed_cell, resources = ft.preprocess_cell(cell, None, None)
            assert processed_cell.source == self.check_source

    def hide_cells_false(self):
        ft1 = FilterTests()
        ft1.hide_cells = False
        for cell in self.nb.cells:
            processed_cell, resources = ft1.preprocess_cell(cell, None, None)
            assert processed_cell.source != self.check_source
