import unittest
from unittest.mock import patch

from e2xgrader.utils.mode import (
    infer_e2xgrader_mode,
    infer_nbextension_mode,
    infer_serverextension_mode,
)


class TestInferE2xGraderMode(unittest.TestCase):

    @patch("e2xgrader.utils.mode.infer_nbextension_mode")
    @patch("e2xgrader.utils.mode.infer_serverextension_mode")
    def test_infer_e2xgrader_mode(
        self, mock_infer_serverextension_mode, mock_infer_nbextension_mode
    ):
        for mode in ["teacher", "student", "student_exam", "None"]:
            mock_infer_serverextension_mode.return_value = mode
            mock_infer_nbextension_mode.return_value = mode
            self.assertEqual(infer_e2xgrader_mode(), mode)

    @patch("e2xgrader.utils.mode.infer_nbextension_mode")
    @patch("e2xgrader.utils.mode.infer_serverextension_mode")
    def test_infer_e2xgrader_fails(
        self, mock_infer_serverextension_mode, mock_infer_nbextension_mode
    ):
        mock_infer_serverextension_mode.return_value = "teacher"
        mock_infer_nbextension_mode.return_value = "student"
        with self.assertRaises(ValueError):
            infer_e2xgrader_mode()


class TestInferNbExtensionMode(unittest.TestCase):

    @patch("e2xgrader.utils.mode.get_nbextension_config")
    def test_infer_nbextension_mode(self, mock_get_nbextension_config):
        mock_get_nbextension_config.return_value = {
            "tree": {"load_extensions": {"teacher_tree/main": True}},
            "notebook": {"load_extensions": {"teacher_notebook/main": True}},
        }
        self.assertEqual(infer_nbextension_mode(), "teacher")

    @patch("e2xgrader.utils.mode.get_nbextension_config")
    def test_infer_nbextension_mode_fails_with_multiple_modes_activated(
        self, mock_get_nbextension_config
    ):
        mock_get_nbextension_config.return_value = {
            "tree": {
                "load_extensions": {
                    "teacher_tree/main": True,
                    "student_tree/main": True,
                }
            },
            "notebook": {
                "load_extensions": {
                    "student_notebook/main": True,
                    "teacher_notebook/main": True,
                }
            },
        }
        with self.assertRaises(ValueError):
            infer_nbextension_mode()

    @patch("e2xgrader.utils.mode.get_nbextension_config")
    def test_infer_nbextension_mode_fails_with_tree_and_notebook_mismatch(
        self, mock_get_nbextension_config
    ):
        mock_get_nbextension_config.return_value = {
            "tree": {"load_extensions": {"teacher_tree/main": True}},
            "notebook": {"load_extensions": {"student_notebook/main": True}},
        }
        with self.assertRaises(ValueError):
            infer_nbextension_mode()

    @patch("e2xgrader.utils.mode.get_nbextension_config")
    def test_infer_nbextension_mode_fails_with_different_number_of_modes_activated(
        self, mock_get_nbextension_config
    ):
        mock_get_nbextension_config.return_value = {
            "tree": {
                "load_extensions": {
                    "teacher_tree/main": True,
                    "student_tree/main": True,
                }
            },
            "notebook": {
                "load_extensions": {
                    "student_notebook/main": True,
                }
            },
        }
        with self.assertRaises(ValueError):
            infer_nbextension_mode()


class TestInferServerExtensionMode(unittest.TestCase):

    @patch("e2xgrader.utils.mode.get_serverextension_config")
    def test_infer_serverextension_mode(self, mock_get_serverextension_config):
        mock_get_serverextension_config.return_value = {
            "e2xgrader.server_extensions.teacher": True,
        }
        self.assertEqual(infer_serverextension_mode(), "teacher")

    @patch("e2xgrader.utils.mode.get_serverextension_config")
    def test_infer_serverextension_mode_with_no_mode_activated(
        self, mock_get_serverextension_config
    ):
        mock_get_serverextension_config.return_value = {}
        self.assertEqual(infer_serverextension_mode(), "None")

    @patch("e2xgrader.utils.mode.get_serverextension_config")
    def test_infer_serverextension_mode_fails_with_multiple_modes_activated(
        self, mock_get_serverextension_config
    ):
        mock_get_serverextension_config.return_value = {
            "nbgrader.server_extensions.formgrader": True,
            "nbgrader.server_extensions.validate_assignment": True,
            "nbgrader.server_extensions.assignment_list": True,
            "nbgrader.server_extensions.course_list": True,
            "e2xgrader.server_extensions.teacher": True,
            "e2xgrader.server_extensions.student": True,
            "e2xgrader.server_extensions.student_exam": True,
        }
        with self.assertRaises(ValueError):
            infer_serverextension_mode()
