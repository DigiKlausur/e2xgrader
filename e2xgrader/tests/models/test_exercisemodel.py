import os
import unittest

from os.path import join as pjoin

from e2xgrader.converters import GenerateExercise
from e2xgrader.models import ExerciseModel, TaskModel

from ..test_utils.test_utils import (
    create_temp_course,
    add_question_to_task,
    add_template_with_header,
)


class TestExerciseModel(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.model = ExerciseModel(coursedir)
        self.converter = GenerateExercise(coursedir=coursedir)
        self.assignment = "DummyAssignment"
        self.exercise = "DummyExercise"
        pool_name = "DummyPool"
        template_name = "DummyTemplate"
        task_name = "DummyTask"
        res = TaskModel(coursedir).new(pool=pool_name, name=task_name)
        add_question_to_task(
            coursedir, res["path"], "Freetext", grade_id="DummyId", points=10
        )
        add_template_with_header(
            coursedir, template_name, "# {{ exercise_name }} \n {{ semester}}"
        )

        self.resources = {
            "assignment": self.assignment,
            "exercise": self.exercise,
            "template": template_name,
            "template-options": {
                "exercise_name": "DummyExercise",
                "semester": "DummySemester",
            },
            "tasks": [{"pool": pool_name, "task": task_name}],
            "exercise_options": {"kernel": "python3", "task-headers": False},
        }

    def test_list_empty(self):
        msg = "Model should not list anything in an empty course"
        assert len(self.model.list(assignment=self.assignment)) == 0, msg

    def test_list_not_empty(self):
        self.converter.convert(self.resources)

        res = self.model.list(assignment=self.assignment)

        assert len(res) == 1, "Model should list exercise after creation"
        assert res[0]["name"] == self.exercise
        assert res[0]["assignment"] == self.assignment

    def test_get(self):
        self.converter.convert(self.resources)

        res = self.model.get(name=self.exercise, assignment=self.assignment)
        assert res["name"] == self.exercise
        assert res["assignment"] == self.assignment

    def test_remove(self):
        self.converter.convert(self.resources)

        res = self.model.list(assignment=self.assignment)
        assert len(res) == 1, "Model should list exercise after creation"

        self.model.remove(assignment=self.assignment, name=self.exercise)

        res = self.model.list(assignment=self.assignment)
        assert len(res) == 0, "Model should not list exercise after deletion"

    def tearDown(self):
        self.tmp_dir.cleanup()
