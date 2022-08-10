import unittest

from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_code_cell
from nbgrader.utils import compute_checksum

from e2xgrader.graders import BaseGrader


class TestBaseGrader(unittest.TestCase):
    def create_unchanged_code_cell(self, grade_id: str) -> NotebookNode:
        cell = new_code_cell()

        cell.metadata = {
            "nbgrader": {
                "grade": True,
                "grade_id": grade_id,
                "locked": False,
                "points": 5,
                "schema_version": 3,
                "solution": True,
                "task": False,
            }
        }

        cell.source = "YOUR CODE HERE"

        cell.metadata.nbgrader["checksum"] = compute_checksum(cell)

        return cell

    def create_changed_code_cell(self, grade_id: str) -> NotebookNode:
        cell = new_code_cell()

        cell.metadata = {
            "nbgrader": {
                "grade": True,
                "grade_id": grade_id,
                "locked": False,
                "points": 5,
                "schema_version": 3,
                "solution": True,
                "task": False,
            }
        }

        cell.source = "YOUR CODE HERE"

        cell.metadata.nbgrader["checksum"] = compute_checksum(cell)

        cell.source = "MY SOLUTION"

        return cell

    def test_cell_unchanged(self):
        assert not BaseGrader().cell_changed(
            self.create_unchanged_code_cell("mycell")
        ), "cell should not have changed"

    def test_cell_changed(self):
        assert BaseGrader().cell_changed(
            self.create_changed_code_cell("mycell")
        ), "cell should have changed"
