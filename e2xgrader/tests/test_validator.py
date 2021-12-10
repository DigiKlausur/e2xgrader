import os
import unittest
from tempfile import TemporaryDirectory
from e2xgrader.validator import E2XValidator

import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell


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

    def create_extra_cell(self, type, grade_id, points):
        cell = new_markdown_cell()
        cell.metadata = {
            "deletable": False,
            "extended_cell": {"type": type},
            "nbgrader": {
                "checksum": "e7782309d16b2c16c2023b59460213df",
                "grade": True,
                "grade_id": grade_id,
                "locked": False,
                "points": points,
                "schema_version": 3,
                "solution": True,
                "task": False,
            },
        }
        return cell

    def test_validate_pass_singlechoice_cell(self):
        singlechoice_cell = self.create_extra_cell("singlechoice", "sc_1", 5)
        singlechoice_cell.metadata["extended_cell"]["choice"] = ["0"]

        nb = new_notebook()
        nb.cells.append(singlechoice_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert len(result) == 0

    def test_validate_fail_singlechoice_cell(self):
        singlechoice_cell = self.create_extra_cell("singlechoice", "sc_1", 5)
        singlechoice_cell.metadata["extended_cell"]["choice"] = []

        nb = new_notebook()
        nb.cells.append(singlechoice_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert "failed" in result
        assert len(result["failed"]) == 1
        assert result["failed"][0]["error"] == self.error_msg

    def test_validate_pass_multiplechoice_cell(self):
        multiplechoice_cell = self.create_extra_cell("multiplechoice", "mc_1", 5)
        multiplechoice_cell.metadata["extended_cell"]["choice"] = ["0", "1"]

        nb = new_notebook()
        nb.cells.append(multiplechoice_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert len(result) == 0

    def test_validate_fail_multiplechoice_cell(self):
        multiplechoice_cell = self.create_extra_cell("multiplechoice", "mc_1", 5)
        multiplechoice_cell.metadata["extended_cell"]["choice"] = []

        nb = new_notebook()
        nb.cells.append(multiplechoice_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert "failed" in result
        assert len(result["failed"]) == 1
        assert result["failed"][0]["error"] == self.error_msg

    def test_validate_pass_attachment_cell(self):
        attachment_cell = self.create_extra_cell("attachments", "at_1", 5)
        attachment_cell["attachments"] = {"test.png": {"image/png": "byte64randomdata"}}

        nb = new_notebook()
        nb.cells.append(attachment_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert len(result) == 0

    def test_validate_fail_attachment_cell(self):
        attachment_cell = self.create_extra_cell("attachments", "at_1", 5)

        nb = new_notebook()
        nb.cells.append(attachment_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert "failed" in result
        assert len(result["failed"]) == 1
        assert result["failed"][0]["error"] == self.error_msg

    def test_pass_other_extra_cells(self):
        extra_cell = self.create_extra_cell("mytype", "ec_1", 5)

        nb = new_notebook()
        nb.cells.append(extra_cell)
        filepath = self.save_notebook(nb)

        result = self.validator.validate(filepath)

        assert len(result) == 0

    def tearDown(self):
        self.tmp_dir.cleanup()
