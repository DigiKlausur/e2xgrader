import unittest

from nbformat.v4 import new_markdown_cell
from nbconvert.filters import markdown2html
from bs4 import BeautifulSoup
from e2xgrader.exporters.filters import RenderExtraCell
from ...test_utils.test_utils import (
    create_singlechoice_cell,
    create_multiplechoice_cell,
)


class TestRenderExtraCell(unittest.TestCase):
    def setUp(self):
        self.renderer = RenderExtraCell()

    def check_input_disabled(self, soup):
        for input_elem in soup.find_all("input"):
            assert input_elem["disabled"] == "disabled"
        for select_elem in soup.find_all("select"):
            assert select_elem["disabled"] == "disabled"

    def test_render_singlechoice_cell(self):
        student_choices = [0]
        cell = create_singlechoice_cell(
            grade_id="sc1", student_choices=student_choices, instructor_choices=[0]
        )
        html_source = markdown2html(cell.source)
        soup = BeautifulSoup(self.renderer(html_source, cell), "html.parser")

        # Make sure all list items are converted
        assert len(soup.find_all("input")) == len(
            BeautifulSoup(html_source, "html.parser").find_all("li")
        )

        self.check_input_disabled(soup)

        # Test all inputs
        for idx, input_elem in enumerate(soup.find_all("input")):
            assert input_elem["value"] == str(idx)
            assert input_elem["type"] == "radio"
            if idx in student_choices:
                assert input_elem["checked"] == "checked"

    def test_render_multiplechoice_cell(self):
        student_choices = [0, 1]
        cell = create_multiplechoice_cell(
            grade_id="sc1",
            student_choices=student_choices,
            instructor_choices=[0],
            num_of_choices=3,
        )
        html_source = markdown2html(cell.source)
        soup = BeautifulSoup(self.renderer(html_source, cell), "html.parser")

        # Make sure all list items are converted
        assert len(soup.find_all("input")) == len(
            BeautifulSoup(html_source, "html.parser").find_all("li")
        )

        self.check_input_disabled(soup)

        # Test all inputs
        for idx, input_elem in enumerate(soup.find_all("input")):
            assert input_elem["value"] == str(idx)
            assert input_elem["type"] == "checkbox"
            if idx in student_choices:
                assert input_elem["checked"] == "checked"

    def test_render_form_cell(self):
        html = '<input type="text" name="input1"><select name="select1"><option value="1"><option value="2"></select>'
        cell = new_markdown_cell(html)
        soup = BeautifulSoup(self.renderer.render_formcell(html, cell), "html.parser")

        self.check_input_disabled(soup)
