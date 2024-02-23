import json
import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from traitlets.config import Config

from e2xgrader.apps.modeswitcher import (
    E2xGraderModes,
    E2xModeSwitcher,
    InvalidModeError,
    get_e2xgrader_mode,
    get_jupyter_config_path,
)


class TestE2xModeSwitcher(unittest.TestCase):
    def setUp(self):
        self.mode_switcher = E2xModeSwitcher()
        config = Config()
        config.E2xModeSwitcher.mode = E2xGraderModes.DEACTIVATED.value

    def test_set_valid_mode_object(self):
        for mode in E2xGraderModes:
            self.mode_switcher.set_mode(mode)
            self.assertEqual(self.mode_switcher.mode, mode.value)

    def test_set_valid_mode_string(self):
        for mode in E2xGraderModes:
            self.mode_switcher.set_mode(mode.value)
            self.assertEqual(self.mode_switcher.mode, mode.value)

    def test_set_invalid_mode(self):
        with self.assertRaises(InvalidModeError):
            self.mode_switcher.mode = "invalid_mode"
        with self.assertRaises(InvalidModeError):
            self.mode_switcher.mode = 5

    @patch("e2xgrader.apps.modeswitcher.get_jupyter_config_path")
    def test_write_config_file(self, mock_get_jupyter_config_path):
        """
        Test case for the write_config_file method of the ModeSwitcher class.

        This verifies that the write_config_file method correctly writes the configuration file,
        and that the file contains the expected mode value after setting the mode to 'EXAM'.
        """
        with TemporaryDirectory() as temp_dir:
            mock_get_jupyter_config_path.return_value = temp_dir
            self.mode_switcher.write_config_file()
            self.assertTrue(os.path.exists(self.mode_switcher.get_config_file()))
            self.mode_switcher.set_mode(E2xGraderModes.EXAM)
            self.mode_switcher.write_config_file()
            with open(self.mode_switcher.get_config_file()) as f:
                config = Config(json.load(f))
                self.assertEquals(
                    E2xGraderModes.EXAM.value, config.E2xModeSwitcher.mode
                )

    @patch("e2xgrader.apps.modeswitcher.E2xModeSwitcher")
    def test_get_e2xgrader_mode(self, mock_e2x_mode_switcher):
        """
        Test case for the get_e2xgrader_mode method of the ModeSwitcher class.

        This test verifies that the get_e2xgrader_mode method returns the expected mode value
        """
        mock_e2x_mode_switcher.return_value.mode = E2xGraderModes.EXAM.value
        self.assertEqual(get_e2xgrader_mode(), E2xGraderModes.EXAM)

    def test_get_jupyter_config_path(self):
        """
        Test case for the get_jupyter_config_path function.

        This test verifies that a ValueError is raised when both the `user` and `sys_prefix`
        arguments are set to True.
        """
        with self.assertRaises(ValueError):
            get_jupyter_config_path(user=True, sys_prefix=True)
