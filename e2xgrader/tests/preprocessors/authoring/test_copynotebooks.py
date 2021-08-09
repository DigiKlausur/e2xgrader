import unittest
import os

from os.path import join as pjoin
from tempfile import TemporaryDirectory
from nbgrader.coursedir import CourseDirectory
from e2xgrader.preprocessors.authoring import CopyNotebooks
from e2xgrader.models import TaskModel, TemplateModel


class TestCopyNotebooks(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        self.resources = {
            'tasks': [
                {
                    'pool': 'TestPool',
                    'task': 'TestTask1'
                },
                {
                    'pool': 'TestPool',
                    'task': 'TestTask2'
                }
            ],
            'template': 'TestTemplate',
            'tmp_dir': self.tmp_dir.name
        }
        self.createTempCourse()
        self.createTasks()
        self.createTemplate()

    def createTempCourse(self):
        self.course_tmp_dir = TemporaryDirectory()
        self.coursedir = CourseDirectory()
        self.coursedir.root = self.course_tmp_dir.name
        self.resources['course_prefix'] = self.coursedir.root

    def createTasks(self):
        self.taskmodel = TaskModel(self.coursedir)
        for task_dict in self.resources['tasks']:
            self.taskmodel.new(pool=task_dict['pool'], name=task_dict['task'])
            
    def createTemplate(self):
        self.templatemodel = TemplateModel(self.coursedir)
        self.templatemodel.new(name=self.resources['template'])

    def tearDown(self):
        # Remove temporary directories
        self.tmp_dir.cleanup()
        self.course_tmp_dir.cleanup()

    def test_copy(self):
        res = CopyNotebooks().preprocess(self.resources)
        assert os.path.exists(pjoin(self.tmp_dir.name, 'tasks')), 'Tasks folder does not exists'
        assert os.path.exists(pjoin(self.tmp_dir.name, 'template')), 'Template folder does not exists'
        for task_dict in self.resources['tasks']:
            assert os.path.exists(pjoin(self.tmp_dir.name, 'tasks', task_dict['pool'], task_dict['task']))
