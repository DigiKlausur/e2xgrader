import unittest
from nbformat.v4 import new_markdown_cell
from e2xgrader.preprocessors import ClearSolutions


class TestClearSolutions(unittest.TestCase):
    def test_markdown_cell(self):
        cell = new_markdown_cell()

        cell.metadata = {
            "nbgrader": {
                "grade": False,
                "grade_id": "text_solution",
                "solution": True,
                "locked": False,
                "schema_version": 3,
                "task": False,
            }
        }

        cell.source = "This is the answer!"

        processed_cell, resources = ClearSolutions().preprocess_cell(
            cell, {"language": "python"}, 0
        )
        assert processed_cell.source == "YOUR ANSWER HERE"

    def test_extra_cell(self):
        cell = new_markdown_cell()

        cell.metadata = {
            "extended_cell": {},
            "nbgrader": {
                "grade": False,
                "grade_id": "text_solution",
                "solution": True,
                "locked": False,
                "schema_version": 3,
                "task": False,
            },
        }

        cell.source = "MY SOURCE"
        processed_cell, resources = ClearSolutions().preprocess_cell(
            cell, {"language": "python"}, 0
        )
        assert processed_cell.source == "MY SOURCE"
