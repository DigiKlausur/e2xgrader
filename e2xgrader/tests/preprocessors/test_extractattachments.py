import unittest
from copy import deepcopy

from nbformat.v4 import new_notebook

from e2xgrader.models import PresetModel
from e2xgrader.preprocessors import ExtractAttachments

from ..test_utils.test_utils import create_temp_course


class TestExtractAttachments(unittest.TestCase):
    def testPreprocessStandardCell(self):
        tmp_dir, coursedir = create_temp_course()
        nb = new_notebook()
        nb.cells = PresetModel(coursedir).get_question_preset("Single Choice")

        processed_nb = deepcopy(nb)
        processed_nb, _ = ExtractAttachments().preprocess(
            processed_nb,
            {
                "metadata": {"path": coursedir.root},
                "outputs": {},
                "output_files_dir": coursedir.root,
            },
        )

        self.assertDictEqual(nb, processed_nb)
        tmp_dir.cleanup()

    def testPreprocessDiagramCell(self):
        tmp_dir, coursedir = create_temp_course()
        nb = new_notebook()
        nb.cells = PresetModel(coursedir).get_question_preset("Diagram")

        processed_nb = deepcopy(nb)
        processed_nb, _ = ExtractAttachments().preprocess(
            processed_nb,
            {
                "metadata": {"path": coursedir.root},
                "outputs": {},
                "output_files_dir": coursedir.root,
            },
        )

        attachment_string = "![diagram](attachment:diagram.png)"

        for processed_cell, cell in zip(processed_nb.cells, nb.cells):
            if attachment_string in cell.source:
                assert attachment_string not in processed_cell.source
                assert "<a href=" in processed_cell.source
                assert "diagram.png" in processed_cell.attachments

        tmp_dir.cleanup()
