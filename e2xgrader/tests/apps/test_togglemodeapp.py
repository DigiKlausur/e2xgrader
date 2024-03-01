import unittest
from unittest.mock import patch

from e2xgrader.apps.togglemodeapp import ToggleModeApp
from e2xgrader.utils.mode import E2xGraderMode


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

            self.app.mode = E2xGraderMode.TEACHER.value
            self.app.activate_mode()
            mock_extension_manager.return_value.activate_teacher.assert_called_once_with(
                sys_prefix=False, user=False
            )

            self.app.mode = E2xGraderMode.STUDENT.value
            self.app.activate_mode()
            mock_extension_manager.return_value.activate_student.assert_called_once_with(
                sys_prefix=False, user=False
            )

            self.app.mode = E2xGraderMode.STUDENT_EXAM.value
            self.app.activate_mode()
            mock_extension_manager.return_value.activate_student_exam.assert_called_once_with(
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
                    self.assertEqual(self.app.mode, E2xGraderMode.INVALID.value)

    def test_flags(self):
        with patch("e2xgrader.apps.togglemodeapp.E2xExtensionManager"):
            self.app.initialize(["--sys-prefix"])
            self.assertTrue(self.app.sys_prefix)
            self.app.initialize(["--user"])
            self.assertTrue(self.app.user)
