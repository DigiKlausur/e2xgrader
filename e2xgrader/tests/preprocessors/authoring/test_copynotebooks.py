import unittest
import os

from os.path import join as pjoin

from .base import BaseTest
from e2xgrader.preprocessors.authoring import CopyNotebooks
from e2xgrader.models import TaskModel, TemplateModel


class TestCopyNotebooks(BaseTest):

    def setUp(self):
        super().setUp()
        self.createTasks()
        self.createTemplate()

    def setUpResources(self):
        super().setUpResources()
        self.resources.update({
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
        })

    def createTasks(self):
        self.taskmodel = TaskModel(self.coursedir)
        for task_dict in self.resources['tasks']:
            self.taskmodel.new(pool=task_dict['pool'], name=task_dict['task'])
            
    def createTemplate(self):
        self.templatemodel = TemplateModel(self.coursedir)
        self.templatemodel.new(name=self.resources['template'])

    def test_copy(self):
        res = CopyNotebooks().preprocess(self.resources)
        assert os.path.exists(pjoin(self.tmp_dir.name, 'tasks')), 'Tasks folder does not exists'
        assert os.path.exists(pjoin(self.tmp_dir.name, 'template')), 'Template folder does not exists'
        for task_dict in self.resources['tasks']:
            assert os.path.exists(pjoin(self.tmp_dir.name, 'tasks', task_dict['pool'], task_dict['task']))
