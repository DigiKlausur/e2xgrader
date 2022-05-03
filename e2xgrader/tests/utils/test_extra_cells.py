import nbformat
import unittest

from e2xgrader.models import PresetModel
from e2xgrader.utils.extra_cells import (
    is_extra_cell,
    is_multiplechoice,
    is_singlechoice,
    is_diagram,
    is_attachment_cell,
    get_choices,
    get_num_of_choices,
    clear_choices,
    has_solution,
    get_options,
)
from ..test_utils.test_utils import create_temp_course


class TestExtraCells(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.model = PresetModel(coursedir)
        self.multiplechoice = "Multiple Choice"
        self.singlechoice = "Single Choice"
        self.diagram = "Diagram"
        self.attachment = "Upload Files"

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

    def test_get_choices(self):
        cells = self.model.get_question_preset(self.multiplechoice)
        assert len(get_choices(cells[0])) == 0

        cells[0].metadata.extended_cell.choice = [1, 2, 3]

        assert len(get_choices(cells[0])) == 3
        assert all([i in get_choices(cells[0]) for i in [1, 2, 3]])

        cells = self.model.get_question_preset(self.diagram)
        assert len(get_choices(cells[0])) == 0

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

        cells = self.model.get_question_preset(self.diagram)
        assert not has_solution(cells[0])

    def test_diagram_cell(self):
        cells = self.model.get_question_preset(self.diagram)
        assert is_diagram(cells[1])

    def test_attachment_cell(self):
        cells = self.model.get_question_preset(self.attachment)
        assert is_attachment_cell(cells[1])

    def test_get_options(self):
        cells = self.model.get_question_preset(self.diagram)
        assert len(get_options(cells[1])) == 0
        cells[1].metadata.extended_cell["options"] = {"key": "value"}
        assert get_options(cells[1])["key"] == "value"

    def tearDown(self):
        self.tmp_dir.cleanup()
