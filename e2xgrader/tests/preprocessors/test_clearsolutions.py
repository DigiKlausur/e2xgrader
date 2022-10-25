import unittest

from nbformat.v4 import new_markdown_cell

from e2xgrader.preprocessors import ClearSolutions


class TestClearSolutions(unittest.TestCase):

    diagram_name = "diagram.png"

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
            "extended_cell": {"type": "singlechoice"},
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

    def test_diagram_cell_no_remove(self):
        cell = new_markdown_cell()

        cell.metadata = {
            "extended_cell": {"type": "diagram", "options": {"replace_diagram": False}},
            "nbgrader": {
                "grade": True,
                "grade_id": "text_solution",
                "solution": True,
                "locked": False,
                "schema_version": 3,
                "task": False,
            },
        }

        cell["attachments"] = {self.diagram_name: {}}
        processed_cell, resources = ClearSolutions().preprocess_cell(
            cell, {"language": "python"}, 0
        )
        assert self.diagram_name in cell.attachments

    def test_diagram_cell_remove(self):
        cell = new_markdown_cell()

        cell.metadata = {
            "extended_cell": {"type": "diagram", "options": {"replace_diagram": True}},
            "nbgrader": {
                "grade": True,
                "grade_id": "text_solution",
                "solution": True,
                "locked": False,
                "schema_version": 3,
                "task": False,
            },
        }

        cell["attachments"] = {self.diagram_name: {}}
        processed_cell, resources = ClearSolutions().preprocess_cell(
            cell, {"language": "python"}, 0
        )
        assert "diagram.png" not in cell.attachments
