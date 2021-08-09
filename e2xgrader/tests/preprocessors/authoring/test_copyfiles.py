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
            'assignment': 'TestAssignment',
            'exercise': 'TestExercise'
        })

    def createTasks(self):
        self.taskmodel = TaskModel(self.coursedir)
        for task_dict in self.resources['tasks']:
            self.taskmodel.new(pool=task_dict['pool'], name=task_dict['task'])
            
    def createTemplate(self):
        self.templatemodel = TemplateModel(self.coursedir)
        self.templatemodel.new(name=self.resources['template'])

    def createSameFiles(self):
        pool_path = pjoin(self.resources['course_prefix'], 'pools')
        rand_data = str([rd.randint(1, 100000) for _ in range(1000)])

        for task_dict in self.resources['tasks']:
            data_path = pjoin(pool_path, task_dict['pool'], task_dict['task'], 'data')
            with open(pjoin(data_path, 'randfile'), 'w') as f:
                f.write(rand_data)

    def test_copy(self):
        self.createSameFiles()
        res = CopyNotebooks().preprocess(self.resources)
        res = CopyFiles().preprocess(res)
        # Make sure exercise folder is created
        file_path = pjoin(self.resources['course_prefix'], 
                          self.resources['source_dir'],
                          self.resources['assignment'],
                          f"{self.resources['exercise']}_files")
        assert os.path.exists(file_path)
        assert os.path.exists(pjoin(file_path, 'data', 'randfile'))
