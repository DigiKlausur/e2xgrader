import unittest
from unittest.mock import patch

from e2xgrader.apps.togglemodeapp import ToggleModeApp


class TestToggleModeApp(unittest.TestCase):

    def setUp(self):
        self.app = ToggleModeApp()
        self.app.initialize([])

    def test_fail_both_sys_prefix_and_user(self):
        self.app.sys_prefix = True
        self.app.user = True
        with self.assertRaises(SystemExit):
            self.app.start()

    def test_activate_mode(self):
        with patch(
            "e2xgrader.apps.togglemodeapp.E2xExtensionManager"
        ) as mock_extension_manager:

            self.app.mode = "teacher"
            self.app.activate_mode()
            mock_extension_manager.return_value.activate_teacher.assert_called_once_with(
                sys_prefix=False, user=False
            )

            self.app.mode = "student"
            self.app.activate_mode()
            mock_extension_manager.return_value.activate_student.assert_called_once_with(
                sys_prefix=False, user=False
            )

            self.app.mode = "student_exam"
            self.app.activate_mode()
            mock_extension_manager.return_value.activate_student_exam.assert_called_once_with(
                sys_prefix=False, user=False
            )

            self.app.mode = "None"
            self.app.activate_mode()
            mock_extension_manager.return_value.deactivate.assert_called_once_with(
                sys_prefix=False, user=False
            )

    def test_non_matching_mode_causes_log_error(self):
        with patch("e2xgrader.apps.togglemodeapp.E2xExtensionManager"):
            with patch(
                "e2xgrader.apps.togglemodeapp.infer_e2xgrader_mode"
            ) as mock_infer_e2xgrader_mode:
                mock_infer_e2xgrader_mode.side_effect = ValueError("error")
                with patch(
                    "e2xgrader.apps.togglemodeapp.ToggleModeApp.log"
                ) as mock_log:
                    self.app.initialize([])
                    self.app.activate_mode()
                    mock_log.error.assert_called_once_with("error")

    def test_flags(self):
        with patch("e2xgrader.apps.togglemodeapp.E2xExtensionManager"):
            self.app.initialize(["--sys-prefix"])
            self.assertTrue(self.app.sys_prefix)
            self.app.initialize(["--user"])
            self.assertTrue(self.app.user)
