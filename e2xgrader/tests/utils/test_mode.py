import unittest
from unittest.mock import patch

from traitlets.config import Config

from e2xgrader.utils.mode import get_e2xgrader_mode


class TestGetE2xGraderMode(unittest.TestCase):

    def mock_load_config_file(self, *args, **kwargs):
        self.config = Config({"E2xGrader": {"mode": "teacher"}})

    @patch(
        "e2xgrader.apps.baseapp.E2xGrader.load_config_file", new=mock_load_config_file
    )
    def test_get_e2xgrader_mode_teacher(self):
        mode = get_e2xgrader_mode()
        self.assertEqual(mode, "teacher")
