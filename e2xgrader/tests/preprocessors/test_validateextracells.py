import unittest

from e2xauthoring.managers import PresetManager
from nbformat.v4 import new_markdown_cell, new_notebook
from nbgrader.nbgraderformat import ValidationError

from e2xgrader.preprocessors import ValidateExtraCells

from ..test_utils.test_utils import create_temp_course


class TestClearSolutions(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.nb = new_notebook()
        self.nb.cells = PresetManager(coursedir).get_question_preset("Single Choice")
        tmp_dir.cleanup()

    def test_invalid_notebook_with_extra_cells(self):
        with self.assertRaises(ValidationError):
            ValidateExtraCells().preprocess(self.nb, {})

    def test_valid_notebook_with_extra_cells(self):
        self.nb.cells[0].metadata.extended_cell.choice = ["1"]
        ValidateExtraCells().preprocess(self.nb, {})

    def test_valid_notebook_without_extra_cells(self):
        self.nb.cells = [new_markdown_cell()]
        ValidateExtraCells().preprocess(self.nb, {})
