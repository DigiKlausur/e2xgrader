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
            with patch(
                "e2xgrader.apps.togglemodeapp.ToggleModeApp.write_mode_config_file"
            ) as mock_write_mode_config_file:

                self.app.mode = "teacher"
                self.app.activate_mode()
                mock_extension_manager.return_value.activate_teacher.assert_called_once_with(
                    sys_prefix=False, user=False
                )

                mock_write_mode_config_file.assert_called_once()

                self.app.mode = "student"
                self.app.activate_mode()
                mock_extension_manager.return_value.activate_student.assert_called_once_with(
                    sys_prefix=False, user=False
                )

                self.assertEqual(mock_write_mode_config_file.call_count, 2)

                self.app.mode = "student_exam"
                self.app.activate_mode()
                mock_extension_manager.return_value.activate_student_exam.assert_called_once_with(
                    sys_prefix=False, user=False
                )

                self.assertEqual(mock_write_mode_config_file.call_count, 3)

                self.app.mode = "None"
                self.app.activate_mode()
                mock_extension_manager.return_value.deactivate.assert_called_once_with(
                    sys_prefix=False, user=False
                )

                self.assertEqual(mock_write_mode_config_file.call_count, 4)

    def test_flags(self):
        with patch("e2xgrader.apps.togglemodeapp.E2xExtensionManager"):
            with patch(
                "e2xgrader.apps.togglemodeapp.ToggleModeApp.write_mode_config_file"
            ):
                self.app.initialize(["--sys-prefix"])
                self.assertTrue(self.app.sys_prefix)
                self.app.initialize(["--user"])
                self.assertTrue(self.app.user)
