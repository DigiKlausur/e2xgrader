import os
import nbformat
import unittest

from os.path import join as pjoin

from e2xgrader.models import PresetModel
from ..test_utils.test_utils import createTempCourse



class TestPresetModel(unittest.TestCase):

    def setUp(self):
        tmp_dir, coursedir = createTempCourse()
        self.tmp_dir = tmp_dir
        self.model = PresetModel(coursedir)

    def test_list_question_presets(self):
        presets = ['Code (Autograded)', 'Code (Manual)',
                   'Freetext', 'Multiple Choice',  'Single Choice']
        questions = self.model.list_question_presets()
        for preset in presets:
            assert preset in questions, f'Preset {preset} not found'

    def test_get_question_preset(self):
        question_presets = self.model.list_question_presets()

        for preset in question_presets:
            question_cells = self.model.get_question_preset(preset)
            assert all([isinstance(cell, nbformat.notebooknode.NotebookNode) for cell in question_cells])

    def test_list_template_presets(self):
        presets = ['Header', 'Footer', 'Group Info', 'Student Info']
        template_presets = self.model.list_template_presets()
        for preset in presets:
            assert preset in template_presets, f'Preset {preset} not found'

    def test_get_template_preset(self):
        template_presets = self.model.list_template_presets()

        for preset in template_presets:
            template_cells = self.model.get_template_preset(preset)
            assert all([isinstance(cell, nbformat.notebooknode.NotebookNode) for cell in template_cells])

    def test_get_invalid_preset(self):
        assert self.model.get_question_preset('Invalid Name') is None
        assert self.model.get_template_preset('Invalid Name') is None

    def tearDown(self):
        self.tmp_dir.cleanup()
