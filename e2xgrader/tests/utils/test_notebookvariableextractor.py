import unittest

from e2xgrader.models import TemplateModel
from e2xgrader.utils import NotebookVariableExtractor

from ..test_utils.test_utils import (
    create_temp_course,
    add_template_with_header,
    add_header_to_template,
    add_footer_to_template,
)


class TestNotebookVariableExtractor(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.coursedir = coursedir

    def test_extract_variables_single_cell(self):
        path = add_template_with_header(
            self.coursedir,
            "TestTemplate",
            "# Template\n{{variable1}}\n\n{{variable_2}}\n\n{{ variable_3}}",
        )

        variables = NotebookVariableExtractor().extract(path)

        assert len(variables) == 3
        for variable in ["variable1", "variable_2", "variable_3"]:
            assert variable in variables, f"{variable} not found"

    def test_extract_variables_multiple_cells(self):
        res = TemplateModel(self.coursedir).new(name="TestTemplate")
        path = res["path"]

        add_header_to_template(
            self.coursedir, path, "{{ header_variable_1 }}\n{{header_variable_2}}"
        )
        add_footer_to_template(
            self.coursedir, path, "{{ footer_variable_1 }}\n{{footer_variable_2}}"
        )

        variables = NotebookVariableExtractor().extract(path)

        assert len(variables) == 4
        for variable in [
            "header_variable_1",
            "header_variable_2",
            "footer_variable_1",
            "footer_variable_2",
        ]:
            assert variable in variables, f"{variable} not found"

    def test_extract_no_variables(self):
        path = add_template_with_header(self.coursedir, "TestTemplate", "# Template")

        variables = NotebookVariableExtractor().extract(path)

        assert len(variables) == 0

    def tearDown(self):
        self.tmp_dir.cleanup()
