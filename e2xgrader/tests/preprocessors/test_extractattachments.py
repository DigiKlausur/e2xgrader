import unittest
from copy import deepcopy

from e2xauthoring.managers import PresetManager
from nbformat.v4 import new_notebook

from e2xgrader.preprocessors import ExtractAttachments

from ..test_utils.test_utils import create_temp_course


class TestExtractAttachments(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir, self.coursedir = create_temp_course()
        self.resources = dict(
            metadata=dict(path=self.coursedir.root),
            outputs=dict(),
            output_files_dir=self.coursedir.root,
        )

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def testPreprocessStandardCell(self):
        nb = new_notebook()
        nb.cells = PresetManager(self.coursedir).get_question_preset("Single Choice")

        processed_nb = deepcopy(nb)
        processed_nb, _ = ExtractAttachments().preprocess(
            nb=processed_nb, resources=self.resources
        )

        self.assertDictEqual(nb, processed_nb)

    def testPreprocessDiagramCell(self):
        nb = new_notebook()
        nb.cells = PresetManager(self.coursedir).get_question_preset("Diagram")

        processed_nb = deepcopy(nb)
        processed_nb, _ = ExtractAttachments().preprocess(
            nb=processed_nb, resources=self.resources
        )

        attachment_string = "![diagram](attachment:diagram.png)"

        for processed_cell, cell in zip(processed_nb.cells, nb.cells):
            if attachment_string in cell.source:
                assert attachment_string not in processed_cell.source
                assert "<a href=" in processed_cell.source
                assert "diagram.png" in processed_cell.attachments
