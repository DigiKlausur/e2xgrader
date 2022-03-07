import nbformat
import unittest

from e2xgrader.models import PresetModel
from e2xgrader.utils.extra_cells import (
    is_extra_cell,
    is_multiplechoice,
    is_singlechoice,
    is_form,
    is_attachment_cell,
    get_choices,
    get_num_of_choices,
    clear_choices,
    has_solution,
    get_form_answers,
    get_instructor_choices,
)
from ..test_utils.test_utils import create_temp_course


class TestExtraCells(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.model = PresetModel(coursedir)
        self.multiplechoice = "Multiple Choice"
        self.singlechoice = "Single Choice"
        self.formcell = "HTML Form Cell"
        self.uploadcell = "File Upload"

    def test_extra_cell(self):
        assert not is_extra_cell(nbformat.v4.new_code_cell())

        cells = self.model.get_question_preset(self.multiplechoice)
        assert is_extra_cell(cells[0])

    def test_multiplechoice_cell(self):
        cells = self.model.get_question_preset(self.multiplechoice)
        assert is_multiplechoice(cells[0])

    def test_singlechoice_cell(self):
        cells = self.model.get_question_preset(self.singlechoice)
        assert is_singlechoice(cells[0])

    def test_form_cell(self):
        cells = self.model.get_question_preset(self.formcell)
        assert is_form(cells[0])

    def test_upload_cell(self):
        cells = self.model.get_question_preset(self.uploadcell)
        assert is_attachment_cell(cells[0])

    def test_get_form_answers(self):
        cell = self.model.get_question_preset(self.formcell)[0]
        assert len(get_form_answers(cell)) == 0

        # Add some values
        cell.metadata.extended_cell.choices = {
            "test": {"type": "number", "value": "3"},
            "select": {"type": "select", "value": "option 1"},
        }
        assert len(get_form_answers(cell)) == 2
        assert all([key in get_form_answers(cell) for key in ["test", "select"]])
        assert get_form_answers(cell)["test"]["type"] == "number"
        assert get_form_answers(cell)["test"]["value"] == "3"
        assert get_form_answers(cell)["select"]["type"] == "select"
        assert get_form_answers(cell)["select"]["value"] == "option 1"

    def test_get_choices(self):
        cells = self.model.get_question_preset(self.multiplechoice)
        assert len(get_choices(cells[0])) == 0

        cells[0].metadata.extended_cell.choice = [1, 2, 3]

        assert len(get_choices(cells[0])) == 3
        assert all([i in get_choices(cells[0]) for i in [1, 2, 3]])

        assert len(get_choices(nbformat.v4.new_code_cell())) == 0

    def test_get_instructor_choices(self):
        cell = self.model.get_question_preset(self.multiplechoice)[0]
        assert len(get_instructor_choices(cell)) == 0

        cell.metadata.extended_cell["source"] = {"choice": ["0"]}
        assert len(get_instructor_choices(cell)) == 1
        assert 0 in get_instructor_choices(cell)

        assert len(get_instructor_choices(nbformat.v4.new_code_cell())) == 0

    def test_get_num_of_choices(self):
        cells = self.model.get_question_preset(self.singlechoice)
        assert get_num_of_choices(cells[0]) is None

        cells = self.model.get_question_preset(self.multiplechoice)
        assert get_num_of_choices(cells[0]) == 3

    def test_clear_choices(self):
        cells = self.model.get_question_preset(self.multiplechoice)
        cells[0].metadata.extended_cell.choice = [1, 2, 3]

        clear_choices(cells[0])
        assert len(get_choices(cells[0])) == 0

    def test_has_solution(self):
        cells = self.model.get_question_preset(self.multiplechoice)
        assert not has_solution(cells[0])

    def tearDown(self):
        self.tmp_dir.cleanup()
