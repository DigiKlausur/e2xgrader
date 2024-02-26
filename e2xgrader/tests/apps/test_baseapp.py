import json
import os
import unittest
from unittest.mock import patch

from traitlets import TraitError
from traitlets.config import Config

from e2xgrader.apps.baseapp import E2xGrader

from ..test_utils.test_utils import create_temp_course


class TestE2xGrader(unittest.TestCase):

    def setUp(self):
        # Start the patch of "e2xgrader.apps.baseapp.get_jupyter_config_path"
        self.tmp_dir, _ = create_temp_course()
        self.patcher = patch("e2xgrader.apps.baseapp.get_jupyter_config_path")
        self.mock_get_jupyter_config_path = self.patcher.start()
        self.mock_get_jupyter_config_path.return_value = self.tmp_dir.name

        self.app = E2xGrader()
        self.app.initialize([])
        self.config_name = f"{self.app.config_file_name}.json"

    def test_get_config_file_path(self):
        self.assertEqual(
            self.app.get_config_file_path(),
            os.path.join(self.tmp_dir.name, self.config_name),
        )

    def test_set_invalid_mode(self):
        with self.assertRaises(TraitError):
            self.app.mode = "invalid_mode"

    def test_write_mode_config_file(self):
        self.app.mode = "teacher"
        self.app.write_mode_config_file()

        assert os.path.exists(os.path.join(self.tmp_dir.name, self.config_name))

        with open(os.path.join(self.tmp_dir.name, self.config_name), "r") as f:
            saved_config = Config(json.load(f))
            self.assertEqual(saved_config.E2xGrader.mode, "teacher")

    def tearDown(self):
        self.patcher.stop()
        self.tmp_dir.cleanup()
