import unittest
from unittest.mock import patch

from e2xgrader.apps.baseapp import get_jupyter_config_path


class TestGetJupyterConfigPath(unittest.TestCase):

    def test_get_jupyter_config_path_user(self):
        with patch(
            "e2xgrader.apps.baseapp.jupyter_config_dir"
        ) as mock_jupyter_config_dir:
            mock_jupyter_config_dir.return_value = "/home/user/.jupyter"
            result = get_jupyter_config_path(user=True)
            self.assertEqual(result, "/home/user/.jupyter")

    def test_get_jupyter_config_path_user_and_sys_prefix(self):
        with self.assertRaises(ValueError):
            get_jupyter_config_path(user=True, sys_prefix=True)
