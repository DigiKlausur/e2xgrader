import os
import unittest

from os.path import join as pjoin

from e2xgrader.models import AssignmentModel
from ..test_utils.test_utils import createTempCourse



class TestTemplateModel(unittest.TestCase):

    def setUp(self):
        tmp_dir, coursedir = createTempCourse()
        self.tmp_dir = tmp_dir
        self.model = AssignmentModel(coursedir)

    def test_list_empty(self):
        assert len(self.model.list()) == 0, 'Model should not list anything in an empty course'

    def tearDown(self):
        self.tmp_dir.cleanup()
