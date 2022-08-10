import os
import unittest
from os.path import join as pjoin

from e2xgrader.converters import GenerateExercise
from e2xgrader.models import TaskModel

from ..test_utils.test_utils import (
    add_question_to_task,
    add_template_with_header,
    create_temp_course,
)


class TestGenerateExercise(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.converter = GenerateExercise(coursedir=coursedir)
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
            "assignment": "DummyAssignment",
            "exercise": "DummyExercise",
            "template": template_name,
            "template-options": {
                "exercise_name": "DummyExercise",
                "semester": "DummySemester",
            },
            "tasks": [{"pool": pool_name, "task": task_name}],
            "exercise_options": {"kernel": "python3", "task-headers": False},
        }

    def test_convert(self):
        self.converter.convert(self.resources)

        base_path = self.converter.coursedir.format_path(
            "source", assignment_id=self.resources["assignment"], student_id="."
        )

        assert os.path.exists(base_path)
        assert os.path.isfile(pjoin(base_path, f'{self.resources["exercise"]}.ipynb'))

    def test_convert_with_headers(self):
        self.resources["exercise_options"]["task-headers"] = True
        self.converter.convert(self.resources)

        base_path = self.converter.coursedir.format_path(
            "source", assignment_id=self.resources["assignment"], student_id="."
        )

        assert os.path.exists(base_path)
        assert os.path.isfile(pjoin(base_path, f'{self.resources["exercise"]}.ipynb'))

    def tearDown(self):
        self.tmp_dir.cleanup()
