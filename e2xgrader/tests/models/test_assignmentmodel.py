import unittest

from e2xgrader.models import AssignmentModel
from ..test_utils.test_utils import create_temp_course


class TestTemplateModel(unittest.TestCase):

    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.model = AssignmentModel(coursedir)

    def test_list_empty(self):
        assert len(self.model.list()) == 0, 'Model should not list anything in an empty course'

    def tearDown(self):
        self.tmp_dir.cleanup()
