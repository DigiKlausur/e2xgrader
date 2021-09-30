import os
import unittest

from os.path import join as pjoin

from e2xgrader.models import TemplateModel
from ..test_utils.test_utils import create_temp_course


class TestTemplateModel(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.model = TemplateModel(coursedir)

    def test_list_empty(self):
        assert (
            len(self.model.list()) == 0
        ), "Model should not list anything in an empty course"

    def test_list_not_empty(self):
        names = ["TestTemplate", "TestTemplate1", "TestTemplate2"]
        for name in names:
            self.model.new(name=name)
        assert len(self.model.list()) == 3
        for template in self.model.list():
            assert template["name"] in names

    def test_create_and_remove_valid_template(self):
        name = "TestTemplate"
        res = self.model.new(name=name)
        assert res["success"], "New template could not be created"
        assert os.path.exists(
            pjoin(self.model.base_path(), name)
        ), "New template directory missing"
        for directory in ["img", "data"]:
            msg = f"New template subdirectory {directory} missing!"
            assert os.path.exists(pjoin(self.model.base_path(), name, directory)), msg
        os.path.exists(
            pjoin(self.model.base_path(), name, f"{name}.ipynb")
        ), "New template notebook missing"

        self.model.remove(name=name)
        assert not os.path.exists(
            pjoin(self.model.base_path(), name)
        ), "Template should be deleted"

    def test_create_existing_template(self):
        name = "TestTemplate"
        res = self.model.new(name=name)
        assert res["success"], "New template could not be created"

        res = self.model.new(name=name)
        assert not res["success"]
        assert res["error"] == f"A template with the name {name} already exists!"

    def test_create_invalid_name(self):
        name = "$Invalid.Name"
        res = self.model.new(name=name)
        assert not res["success"]
        assert res["error"] == "Invalid name"

    def tearDown(self):
        self.tmp_dir.cleanup()
