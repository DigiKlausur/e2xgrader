import unittest
from unittest.mock import patch

from jupyter_core.application import NoStart

from e2xgrader.apps.activatemodeapp import ActivateModeApp
from e2xgrader.utils.mode import E2xGraderMode


class TestActivateModeApp(unittest.TestCase):

    def setUp(self):
        self.app = ActivateModeApp()
        self.app.initialize([])

    def test_fail_without_args(self):
        with self.assertRaises(SystemExit):
            self.app.initialize([])
            self.app.start()

    def test_fail_with_invalid_mode(self):
        with self.assertRaises(SystemExit):
            self.app.initialize(["invalid_mode"])
            self.app.start()

    @patch("e2xgrader.apps.togglemodeapp.ToggleModeApp.activate_mode")
    def test_activate_mode(self, mock_activate_mode):
        try:
            self.app.initialize([E2xGraderMode.TEACHER.value])
            self.app.start()
        except NoStart:
            pass
        finally:
            self.assertEqual(self.app.mode, E2xGraderMode.TEACHER.value)
            mock_activate_mode.assert_called_once()
