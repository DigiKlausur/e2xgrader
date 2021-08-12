import unittest
import os
import random as rd

from os.path import join as pjoin

from .base import BaseTest
from e2xgrader.preprocessors.authoring import CopyFiles, CopyNotebooks
from e2xgrader.models import TaskModel, TemplateModel


class TestCopyFiles(BaseTest):
    def setUp(self):
        super().setUp()
        self.createTasks()
        self.createTemplate()

    def setUpResources(self):
        super().setUpResources()
        self.resources.update(
            {
                "tasks": [
                    {"pool": "TestPool", "task": "TestTask1"},
                    {"pool": "TestPool", "task": "TestTask2"},
                ],
                "template": "TestTemplate",
                "assignment": "TestAssignment",
                "exercise": "TestExercise",
            }
        )

    def createTasks(self):
        self.taskmodel = TaskModel(self.coursedir)
        for task_dict in self.resources["tasks"]:
            self.taskmodel.new(pool=task_dict["pool"], name=task_dict["task"])

    def createTemplate(self):
        self.templatemodel = TemplateModel(self.coursedir)
        self.templatemodel.new(name=self.resources["template"])

    def test_copy_identical_files(self):
        # Create files with the same name and same content for each task
        pool_path = pjoin(self.resources["course_prefix"], "pools")
        rand_data = str([rd.randint(1, 100000) for _ in range(1000)])

        for task_dict in self.resources["tasks"]:
            data_path = pjoin(pool_path, task_dict["pool"], task_dict["task"], "data")
            with open(pjoin(data_path, "randfile"), "w") as f:
                f.write(rand_data)

        res = CopyNotebooks().preprocess(self.resources)
        res = CopyFiles().preprocess(res)
        # Make sure exercise folder is created
        file_path = pjoin(
            self.resources["course_prefix"],
            self.resources["source_dir"],
            self.resources["assignment"],
            f"{self.resources['exercise']}_files",
        )
        data_path = pjoin(file_path, "data")
        assert os.path.exists(file_path)
        assert os.path.exists(data_path)
        data_files = os.listdir(data_path)
        assert len(data_files) == 1
        assert data_files[0] == "randfile"

    def test_copy_different_files(self):
        # Create files with the same name but different content for each task
        pool_path = pjoin(self.resources["course_prefix"], "pools")

        for task_dict in self.resources["tasks"]:
            data_path = pjoin(pool_path, task_dict["pool"], task_dict["task"], "data")
            with open(pjoin(data_path, "randfile"), "w") as f:
                f.write(str([rd.randint(1, 100000) for _ in range(1000)]))

        res = CopyNotebooks().preprocess(self.resources)
        res = CopyFiles().preprocess(res)
        # Make sure exercise folder is created
        file_path = pjoin(
            self.resources["course_prefix"],
            self.resources["source_dir"],
            self.resources["assignment"],
            f"{self.resources['exercise']}_files",
        )
        data_path = pjoin(file_path, "data")
        assert os.path.exists(file_path)
        assert os.path.exists(data_path)
        data_files = os.listdir(data_path)
        assert len(data_files) == len(self.resources["tasks"])
        assert "randfile" in data_files
        for i in range(len(self.resources["tasks"]) - 1):
            assert f"randfile_{i+1}" in data_files
