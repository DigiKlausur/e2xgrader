import unittest
from unittest.mock import patch

from jupyter_core.application import NoStart

from e2xgrader.apps.deactivatemodeapp import DeactivateModeApp
from e2xgrader.utils.mode import E2xGraderMode


class TestDeactivateModeApp(unittest.TestCase):

    def setUp(self):
        self.app = DeactivateModeApp()
        self.app.initialize([])

    def test_fail_with_args(self):
        with self.assertRaises(SystemExit):
            self.app.initialize(["arg"])
            self.app.start()

    @patch("e2xgrader.apps.togglemodeapp.ToggleModeApp.activate_mode")
    def test_deactivate_mode(self, mock_activate_mode):
        self.app.initialize([])
        try:
            self.app.start()
        except NoStart:
            pass
        finally:
            self.assertEqual(self.app.mode, E2xGraderMode.INACTIVE.value)
            mock_activate_mode.assert_called_once()
