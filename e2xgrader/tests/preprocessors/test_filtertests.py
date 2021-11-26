import unittest
from nbformat.v4 import new_markdown_cell, new_code_cell, new_notebook
from nbgrader.utils import is_grade, is_solution
from e2xgrader.utils.nbgrader_cells import grade_id
from e2xgrader.preprocessors import FilterTests


class TestFilterCellsById(unittest.TestCase):
    def create_test_cell(self, grade_id, source):
        cell = new_code_cell()
        cell.metadata = {
            "nbgrader": {
                "grade": True,
                "grade_id": grade_id,
                "solution": False,
                "locked": True,
                "schema_version": 3,
                "task": False,
            }
        }
        cell.source = source
        return cell

    def create_solution_cell(self, grade_id, source, is_grade=False):
        cell = new_code_cell()
        cell.metadata = {
            "nbgrader": {
                "grade": is_grade,
                "grade_id": grade_id,
                "solution": True,
                "locked": True,
                "schema_version": 3,
                "task": False,
            }
        }
        cell.source = source
        return cell

    def test_do_not_hide(self):
        preprocessor = FilterTests()

        nb = new_notebook()
        nb.cells.append(
            self.create_solution_cell(
                grade_id="abc",
                source="""
            x = 5
            """,
                is_grade=False,
            )
        )
        nb.cells.append(
            self.create_test_cell(
                grade_id="test_abc",
                source="""
            ### BEGIN HIDDEN TESTS
            assert x == 5
            ### END HIDDEN TESTS
            """,
            )
        )
        resources = {}
        processed_nb, resources = preprocessor.preprocess(nb, resources)
        for original_cell, processed_cell in zip(nb.cells, processed_nb.cells):
            assert original_cell.source == processed_cell.source

    def test_hide(self):
        preprocessor = FilterTests()
        preprocessor.hide_cells = True

        nb = new_notebook()
        nb.cells.append(
            self.create_solution_cell(
                grade_id="abc",
                source="""
            x = 5
            """,
                is_grade=False,
            )
        )
        nb.cells.append(
            self.create_test_cell(
                grade_id="test_abc",
                source="""
            ### BEGIN HIDDEN TESTS
            assert x == 5
            ### END HIDDEN TESTS
            """,
            )
        )
        resources = {}
        processed_nb, resources = preprocessor.preprocess(nb, resources)
        for original_cell, processed_cell in zip(nb.cells, processed_nb.cells):
            if not (is_grade(original_cell) and not is_solution(original_cell)):
                # Not a test cell
                assert original_cell.source == processed_cell.source
            else:
                print(processed_cell.source)
                assert processed_cell.source == "# This test case is hidden #"
