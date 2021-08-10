import unittest

from e2xgrader.utils import NotebookVariableExtractor

from ..test_utils.test_utils import createTempCourse, add_template_with_header


class TestNotebookVariableExtractor(unittest.TestCase):

    def setUp(self):
        tmp_dir, coursedir = createTempCourse()
        self.tmp_dir = tmp_dir
        self.coursedir = coursedir

    def test_extract_variables(self):
        path = add_template_with_header(
            self.coursedir, 
            'TestTemplate',
            '# Template\n{{variable1}}\n\n{{variable_2}}\n\n{{ variable_3}}')

        variables = NotebookVariableExtractor().extract(path)

        assert len(variables) == 3
        for variable in ['variable1', 'variable_2', 'variable_3']:
            assert variable in variables, f'{variable} not found'

    def test_extract_no_variables(self):
        path = add_template_with_header(
            self.coursedir, 
            'TestTemplate',
            '# Template')

        variables = NotebookVariableExtractor().extract(path)

        assert len(variables) == 0

    def tearDown(self):
        self.tmp_dir.cleanup()
