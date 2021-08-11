import os
import unittest

from notebook.serverextensions import BaseJSONConfigManager, jupyter_config_path

from e2xgrader.apps import e2xgraderapp


class TestE2XGraderApp(unittest.TestCase):

    def setUp(self):
        self.serverextensions = [
            'nbgrader.server_extensions.formgrader',
            'nbgrader.server_extensions.validate_assignment',
            'nbgrader.server_extensions.assignment_list',
            'nbgrader.server_extensions.course_list',
            'e2xgrader.server_extensions.formgrader',
            'e2xgrader.server_extensions.assignment_list',
            'e2xgrader.server_extensions.e2xbase'
        ]
        self.manager = e2xgraderapp.ExtensionManager()
        self.manager.deactivate()

    def test_deactivated_serverextensions(self):
        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get('jupyter_notebook_config'))
        extensions = config_dict['NotebookApp']['nbserver_extensions']
        for serverextension in self.serverextensions:
            assert not extensions[serverextension]

    def test_teacher_serverextensions(self):
        teacher_serversextensions = [
            'nbgrader.server_extensions.validate_assignment',
            'nbgrader.server_extensions.course_list',
            'e2xgrader.server_extensions.formgrader',
            'e2xgrader.server_extensions.assignment_list',
            'e2xgrader.server_extensions.e2xbase'
        ]
        self.manager.activate_teacher()

        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get('jupyter_notebook_config'))
        extensions = config_dict['NotebookApp']['nbserver_extensions']
        for serverextension in self.serverextensions:
            if serverextension in teacher_serversextensions:
                assert extensions[serverextension]
            else:
                assert not extensions[serverextension]

    def test_teacher_nbextensions(self):
        teacher_nbextensions = {
            'tree': {
                'formgrader/main': True,
                'assignment_list/main': True,
                'course_list/main': True,
                'taskcreator/main': True,
                'restricted_tree/main': False
            },
            'notebook': {
                'create_assignment/main': True,
                'validate_assignment/main': True,
                'extra_cells/main': True,
                'taskeditor/main': True,
                'templatebar/main': True,
                'assignment_extension/main': False,
                'exam_view/main': False
            }
        }
        self.manager.activate_teacher()
        for section, extensions in teacher_nbextensions.items():
            config_dict = {}
            for config_dir in jupyter_config_path():
                config_dir = os.path.join(config_dir, 'nbconfig')
                cm = BaseJSONConfigManager(config_dir=config_dir)
                config_dict.update(cm.get(section))

            for extension, status in extensions.items():
                if extension in config_dict['load_extensions']:
                    assert config_dict['load_extensions'][extension] == status
                else:
                    assert not status

    def test_student_serverextensions(self):
        student_serversextensions = [
            'nbgrader.server_extensions.validate_assignment',
            'nbgrader.server_extensions.course_list',
            'e2xgrader.server_extensions.assignment_list',
            'e2xgrader.server_extensions.e2xbase'
        ]
        self.manager.activate_student()

        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get('jupyter_notebook_config'))
        extensions = config_dict['NotebookApp']['nbserver_extensions']
        for serverextension in self.serverextensions:
            if serverextension in student_serversextensions:
                assert extensions[serverextension]
            else:
                assert not extensions[serverextension]

    def test_student_nbextensions(self):
        student_nbextensions = {
            'tree': {
                'formgrader/main': False,
                'assignment_list/main': True,
                'course_list/main': False,
                'taskcreator/main': False,
                'restricted_tree/main': False
            },
            'notebook': {
                'create_assignment/main': False,
                'validate_assignment/main': False,
                'extra_cells/main': True,
                'taskeditor/main': False,
                'templatebar/main': False,
                'assignment_extension/main': True,
                'exam_view/main': False
            }
        }
        self.manager.activate_student()
        for section, extensions in student_nbextensions.items():
            config_dict = {}
            for config_dir in jupyter_config_path():
                config_dir = os.path.join(config_dir, 'nbconfig')
                cm = BaseJSONConfigManager(config_dir=config_dir)
                config_dict.update(cm.get(section))

            for extension, status in extensions.items():
                if extension in config_dict['load_extensions']:
                    assert config_dict['load_extensions'][extension] == status
                else:
                    assert not status

    def test_student_exam_serverextensions(self):
        student_serversextensions = [
            'nbgrader.server_extensions.validate_assignment',
            'nbgrader.server_extensions.course_list',
            'e2xgrader.server_extensions.assignment_list',
            'e2xgrader.server_extensions.e2xbase'
        ]
        self.manager.activate_student_exam()

        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get('jupyter_notebook_config'))
        extensions = config_dict['NotebookApp']['nbserver_extensions']
        for serverextension in self.serverextensions:
            if serverextension in student_serversextensions:
                assert extensions[serverextension]
            else:
                assert not extensions[serverextension]

    def test_student_exam_nbextensions(self):
        student_exam_nbextensions = {
            'tree': {
                'formgrader/main': False,
                'assignment_list/main': True,
                'course_list/main': False,
                'taskcreator/main': False,
                'restricted_tree/main': True
            },
            'notebook': {
                'create_assignment/main': False,
                'validate_assignment/main': False,
                'extra_cells/main': True,
                'taskeditor/main': False,
                'templatebar/main': False,
                'assignment_extension/main': True,
                'exam_view/main': True
            }
        }
        self.manager.activate_student_exam()
        for section, extensions in student_exam_nbextensions.items():
            config_dict = {}
            for config_dir in jupyter_config_path():
                config_dir = os.path.join(config_dir, 'nbconfig')
                cm = BaseJSONConfigManager(config_dir=config_dir)
                config_dict.update(cm.get(section))

            for extension, status in extensions.items():
                if extension in config_dict['load_extensions']:
                    assert config_dict['load_extensions'][extension] == status
                else:
                    assert not status

    def tearDown(self):
        self.manager.deactivate()
