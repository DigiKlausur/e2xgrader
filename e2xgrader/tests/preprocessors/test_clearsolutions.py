import unittest

from e2xgrader.preprocessors import ClearSolutions
from e2xgrader.tests.test_utils.cells import (
    new_diagram_cell,
    new_manually_graded_markdown_cell,
    new_singlechoice_cell,
)


class TestClearSolutions(unittest.TestCase):
    def setUp(self) -> None:
        self.resources = dict(language="python")

    def test_markdown_cell(self):
        processed_cell, _ = ClearSolutions().preprocess_cell(
            cell=new_manually_graded_markdown_cell(source="This is the answer!"),
            resources=self.resources,
            cell_index=0,
        )
        assert processed_cell.source == "YOUR ANSWER HERE"

    def test_extra_cell(self):
        source = "My original text"
        cell = new_singlechoice_cell(source=source)

        processed_cell, _ = ClearSolutions().preprocess_cell(
            cell=cell,
            resources=self.resources,
            cell_index=0,
        )
        assert processed_cell.source == source

    def test_diagram_cell_no_remove(self):
        cell = new_diagram_cell(
            options=dict(replace_diagram=dict(value=False)),
            diagram="some_base64_encoded_data",
        )
        processed_cell, _ = ClearSolutions().preprocess_cell(
            cell=cell, resources=self.resources, cell_index=0
        )
        assert "diagram.png" in processed_cell.attachments

    def test_diagram_cell_remove(self):
        cell = new_diagram_cell(
            options=dict(replace_diagram=dict(value=True)),
            diagram="some_base64_encoded_data",
        )
        processed_cell, _ = ClearSolutions().preprocess_cell(
            cell=cell, resources=self.resources, cell_index=0
        )
        assert "diagram.png" not in processed_cell.attachments
