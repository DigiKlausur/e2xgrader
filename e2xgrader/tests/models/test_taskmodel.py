import os
import unittest

from os.path import join as pjoin

from e2xgrader.models import TaskModel
from ..test_utils.test_utils import create_temp_course, add_question_to_task


class TestTaskModel(unittest.TestCase):

    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.tmp_dir = tmp_dir
        self.model = TaskModel(coursedir)

    def test_list_empty(self):
        pool = 'TestPool'
        assert len(self.model.list(pool=pool)) == 0, 'Model should not list anything in an empty course'

    def test_list_not_empty(self):
        names = ['TestTask', 'TestTask1', 'TestTask2']
        pool = 'TestPool'
        for name in names:
            self.model.new(name=name, pool=pool)
        assert len(self.model.list(pool=pool)) == 3
        for task in self.model.list(pool=pool):
            assert task['name'] in names

    def test_create_and_remove_valid_task(self):
        name = 'TestTask'
        pool = 'TestPool'
        res = self.model.new(name=name, pool=pool)
        assert res['success'], 'New task could not be created'
        assert os.path.exists(pjoin(self.model.base_path(), pool, name)), 'New task directory missing'
        for directory in ['img', 'data']:
            msg = f'New task subdirectory {directory} missing!'
            assert os.path.exists(pjoin(self.model.base_path(), pool, name, directory)), msg
        os.path.exists(pjoin(self.model.base_path(), pool, name, f'{name}.ipynb')), 'New task notebook missing'

        self.model.remove(name=name, pool=pool)
        assert not os.path.exists(pjoin(self.model.base_path(), pool, name)), 'Task should be deleted'

    def test_create_existing_task(self):
        name = 'TestTask'
        pool = 'TestPool'
        res = self.model.new(name=name, pool=pool)
        assert res['success'], 'New task could not be created'

        res = self.model.new(name=name, pool=pool)
        assert not res['success']
        assert res['error'] == f'A task with the name {name} already exists!'

    def test_get_task_info(self):
        name = 'TestTask'
        pool = 'TestPool'
        points = 5
        res = self.model.new(name=name, pool=pool)
        add_question_to_task(self.model.coursedir, res['path'], 'Freetext', grade_id='task1', points=points)
        res = self.model.get(name=name, pool=pool)
        assert res['name'] == name
        assert res['pool'] == pool
        assert res['questions'] == 1
        assert res['points'] == points

    def tearDown(self):
        self.tmp_dir.cleanup()
