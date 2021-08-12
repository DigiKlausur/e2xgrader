import os
import unittest

from notebook.serverextensions import BaseJSONConfigManager, jupyter_config_path

from e2xgrader.apps import e2xgraderapp


class TestE2XGraderApp(unittest.TestCase):
    def setUp(self):
        self.serverextensions = [
            "nbgrader.server_extensions.formgrader",
            "nbgrader.server_extensions.validate_assignment",
            "nbgrader.server_extensions.assignment_list",
            "nbgrader.server_extensions.course_list",
            "e2xgrader.server_extensions.formgrader",
            "e2xgrader.server_extensions.assignment_list",
            "e2xgrader.server_extensions.e2xbase",
        ]
        self.manager = e2xgraderapp.ExtensionManager()
        self.manager.deactivate()

    def get_serverextensions(self, role):
        serverextensions = {
            "nbgrader.server_extensions.formgrader": [],
            "nbgrader.server_extensions.validate_assignment": [
                "teacher",
                "student",
                "student_exam",
            ],
            "nbgrader.server_extensions.assignment_list": [],
            "nbgrader.server_extensions.course_list": [
                "teacher",
                "student",
                "student_exam",
            ],
            "e2xgrader.server_extensions.formgrader": ["teacher"],
            "e2xgrader.server_extensions.assignment_list": [
                "teacher",
                "student",
                "student_exam",
            ],
            "e2xgrader.server_extensions.e2xbase": [
                "teacher",
                "student",
                "student_exam",
            ],
        }

        for key, value in serverextensions.items():
            serverextensions[key] = role in value

        return serverextensions

    def get_nbextensions(self, role):
        nbextensions = {
            "tree": {
                "formgrader/main": ["teacher"],
                "assignment_list/main": ["teacher", "student", "student_exam"],
                "course_list/main": ["teacher"],
                "taskcreator/main": ["teacher"],
                "restricted_tree/main": ["student_exam"],
            },
            "notebook": {
                "create_assignment/main": ["teacher"],
                "validate_assignment/main": ["teacher"],
                "extra_cells/main": ["teacher", "student", "student_exam"],
                "taskeditor/main": ["teacher"],
                "templatebar/main": ["teacher"],
                "assignment_extension/main": ["student", "student_exam"],
                "exam_view/main": ["student_exam"],
            },
        }

        for section_dict in nbextensions.values():
            for key, value in section_dict.items():
                section_dict[key] = role in value

        return nbextensions

    def test_deactivated_serverextensions(self):
        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get("jupyter_notebook_config"))
        extensions = config_dict["NotebookApp"]["nbserver_extensions"]
        for serverextension in self.serverextensions:
            assert not extensions[serverextension]

    def test_teacher_serverextensions(self):
        teacher_serverextensions = self.get_serverextensions("teacher")
        self.manager.activate_teacher()

        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get("jupyter_notebook_config"))
        extensions = config_dict["NotebookApp"]["nbserver_extensions"]
        for serverextension, status in teacher_serverextensions.items():
            assert extensions[serverextension] == status

    def test_teacher_nbextensions(self):
        teacher_nbextensions = self.get_nbextensions("teacher")
        self.manager.activate_teacher()
        for section, extensions in teacher_nbextensions.items():
            config_dict = {}
            for config_dir in jupyter_config_path():
                config_dir = os.path.join(config_dir, "nbconfig")
                cm = BaseJSONConfigManager(config_dir=config_dir)
                config_dict.update(cm.get(section))

            for extension, status in extensions.items():
                if extension in config_dict["load_extensions"]:
                    assert config_dict["load_extensions"][extension] == status
                else:
                    assert not status

    def test_student_serverextensions(self):
        student_serverextensions = self.get_serverextensions("student")
        self.manager.activate_student()

        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get("jupyter_notebook_config"))
        extensions = config_dict["NotebookApp"]["nbserver_extensions"]
        for serverextension, status in student_serverextensions.items():
            assert extensions[serverextension] == status

    def test_student_nbextensions(self):
        student_nbextensions = self.get_nbextensions("student")
        self.manager.activate_student()
        for section, extensions in student_nbextensions.items():
            config_dict = {}
            for config_dir in jupyter_config_path():
                config_dir = os.path.join(config_dir, "nbconfig")
                cm = BaseJSONConfigManager(config_dir=config_dir)
                config_dict.update(cm.get(section))

            for extension, status in extensions.items():
                if extension in config_dict["load_extensions"]:
                    assert config_dict["load_extensions"][extension] == status
                else:
                    assert not status

    def test_student_exam_serverextensions(self):
        student_serverextensions = self.get_serverextensions("student_exam")
        self.manager.activate_student_exam()

        config_dict = {}
        for config_dir in jupyter_config_path():
            cm = BaseJSONConfigManager(config_dir=config_dir)
            config_dict.update(cm.get("jupyter_notebook_config"))
        extensions = config_dict["NotebookApp"]["nbserver_extensions"]
        for serverextension, status in student_serverextensions.items():
            assert extensions[serverextension] == status

    def test_student_exam_nbextensions(self):
        student_exam_nbextensions = self.get_nbextensions("student_exam")
        self.manager.activate_student_exam()
        for section, extensions in student_exam_nbextensions.items():
            config_dict = {}
            for config_dir in jupyter_config_path():
                config_dir = os.path.join(config_dir, "nbconfig")
                cm = BaseJSONConfigManager(config_dir=config_dir)
                config_dict.update(cm.get(section))

            for extension, status in extensions.items():
                if extension in config_dict["load_extensions"]:
                    assert config_dict["load_extensions"][extension] == status
                else:
                    assert not status

    def tearDown(self):
        self.manager.deactivate()
