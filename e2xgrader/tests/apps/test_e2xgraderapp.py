import unittest
from unittest.mock import patch

from jupyter_core.application import NoStart

from e2xgrader.apps.activatemodeapp import ActivateModeApp
from e2xgrader.apps.e2xgraderapp import E2xGraderApp


class TestE2xGraderApp(unittest.TestCase):

    def setUp(self):
        self.app = E2xGraderApp()
        self.app.initialize([])

    def test_run_without_subcommand(self):
        # When the app starts we need to make sure app.print_subcommands is called
        with patch.object(self.app, "print_subcommands") as mock_print_subcommands:
            self.app.start()
            mock_print_subcommands.assert_called_once()

    def test_run_with_subcommand_activate(self):
        # When the app starts with a subcommand we need to make sure the subcommand is called
        self.app.initialize(["activate"])
        self.assertIsInstance(self.app.subapp, ActivateModeApp)
        with patch(
            "e2xgrader.apps.activatemodeapp.ActivateModeApp.start"
        ) as mock_start:
            try:
                self.app.start()
            except NoStart:
                pass
            finally:
                mock_start.assert_called_once()

    def test_run_with_invalid_subcommand(self):
        # When the app starts with an invalid subcommand we need to make sure the app prints
        # the subcommands
        self.app.initialize(["invalid_subcommand"])
        with patch.object(self.app, "print_subcommands") as mock_print_subcommands:
            self.app.start()
            mock_print_subcommands.assert_called_once()
