import os
import unittest
from os.path import join as pjoin

from e2xgrader.models import TaskModel, TaskPoolModel

from ..test_utils.test_utils import create_temp_course


class TestTaskPoolModel(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.model = TaskPoolModel(coursedir)

    def test_create_existing_taskpool(self):
        name = "TestPool"
        res = self.model.new(name=name)
        assert res["success"], "New pool could not be created"

        res = self.model.new(name=name)
        assert not res["success"]
        assert res["error"] == f"A pool with the name {name} already exists!"

    def test_list_empty(self):
        assert (
            len(self.model.list()) == 0
        ), "Model should not list anything in an empty course"

    def test_list_not_empty(self):
        names = ["TestTaskPool", "TestTaskPool1", "TestTaskPool2"]
        for name in names:
            self.model.new(name=name)
        assert len(self.model.list()) == 3
        for task in self.model.list():
            assert task["name"] in names

    def test_create_and_remove_valid_taskpool(self):
        name = "TestTaskPool"
        res = self.model.new(name=name)
        assert res["success"], "New task pool could not be created"
        assert os.path.exists(
            pjoin(self.model.base_path(), name)
        ), "New task pool directory missing"

        self.model.remove(name=name)
        assert not os.path.exists(
            pjoin(self.model.base_path(), name)
        ), "TaskPool should be deleted"

    def test_list_pool_with_tasks(self):
        name = "TestTask"
        pool = "TestPool"
        TaskModel(self.model.coursedir).new(name=name, pool=pool)
        assert len(self.model.list()) == 1
        pools = self.model.list()
        assert pools[0]["tasks"] == 1

        assert self.model.get(name=pool)["name"] == pool
        assert self.model.get(name=pool)["tasks"] == 1

    def test_create_invalid_name(self):
        name = "$Invalid.Name"
        res = self.model.new(name=name)
        assert not res["success"]
        assert res["error"] == "Invalid name"

    def tearDown(self):
        self.tmp_dir.cleanup()
