import os
import unittest

from os.path import join as pjoin

from e2xgrader.models import BaseModel
from ..utils.test_utils import createTempCourse



class TestBaseModel(unittest.TestCase):

    def setUp(self):
        tmp_dir, coursedir = createTempCourse()
        self.tmp_dir = tmp_dir
        self.model = BaseModel(coursedir)

    def test_base_path(self):
        assert os.path.exists(self.model.base_path())
        assert os.path.normpath(self.model.base_path()) == os.path.normpath(self.tmp_dir.name)

    def test_valid_names(self):
        valid_names = ['Test', 'T est', 'T_es t']
        for name in valid_names:
            assert self.model.is_valid_name(name=name)

    def test_invalid_names(self):
        invalid_names = [' Test', 'T$est', '11.2']
        for name in invalid_names:
            assert not self.model.is_valid_name(name=name)

    def tearDown(self):
        self.tmp_dir.cleanup()
