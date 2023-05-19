import os
import unittest
from tempfile import TemporaryDirectory

import nbformat
from nbformat.v4 import new_notebook

from e2xgrader.server_extensions.apps.validate_assignment.validator import E2XValidator
from e2xgrader.tests.test_utils.cells import (
    new_multiplechoice_cell,
    new_singlechoice_cell,
    new_upload_cell,
)


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        self.validator = E2XValidator()
        # There is no need to execute the notebook
        self.validator.preprocessors = []
        self.error_msg = "You did not provide a response."

    def save_notebook(self, nb):
        nb_name = "mynb.ipynb"
        filepath = os.path.join(self.tmp_dir.name, nb_name)
        nbformat.write(nb, filepath)
        return filepath

    def test_validate_pass_singlechoice_cell(self):
        nb = new_notebook()
        nb.cells.append(new_singlechoice_cell(choice=["0"], points=4))
        filepath = self.save_notebook(nb)
        result = self.validator.validate(filepath)

        assert len(result) == 0

    def test_validate_fail_singlechoice_cell(self):
        nb = new_notebook()
        nb.cells.append(new_singlechoice_cell(points=5))
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert "failed" in result
        assert len(result["failed"]) == 1
        assert result["failed"][0]["error"] == self.error_msg

    def test_validate_pass_multiplechoice_cell(self):
        nb = new_notebook()
        nb.cells.append(new_multiplechoice_cell(points=5, choice=["0", "1"]))
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)
        assert len(result) == 0

    def test_validate_fail_multiplechoice_cell(self):
        nb = new_notebook()
        nb.cells.append(new_multiplechoice_cell(points=5))
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)
        assert "failed" in result
        assert len(result["failed"]) == 1
        assert result["failed"][0]["error"] == self.error_msg

    def test_validate_pass_attachment_cell(self):
        nb = new_notebook()
        nb.cells.append(
            new_upload_cell(
                points=10, attachments={"test.png": {"image/png": "byte64randomdata"}}
            )
        )
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert len(result) == 0

    def test_validate_fail_attachment_cell(self):
        nb = new_notebook()
        nb.cells.append(new_upload_cell(points=3))
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert "failed" in result
        assert len(result["failed"]) == 1
        assert result["failed"][0]["error"] == self.error_msg

    def test_pass_other_extra_cells(self):
        extra_cell = new_singlechoice_cell()
        extra_cell.metadata["extended_cell"]["type"] = "sometype"

        nb = new_notebook()
        nb.cells.append(extra_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert len(result) == 0

    def tearDown(self):
        self.tmp_dir.cleanup()
