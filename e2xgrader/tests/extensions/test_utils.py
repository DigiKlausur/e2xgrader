import unittest
from unittest.mock import MagicMock, patch

from e2xgrader.extensions.utils import (
    get_nbextension_utils,
    get_notebook_config_manager,
    is_installed,
)


class TestIsInstalled(unittest.TestCase):

    def test_installed(self):
        self.assertTrue(is_installed("e2xgrader"), "e2xgrader should be installed")

    def test_not_installed(self):
        self.assertFalse(
            is_installed("e2xgradeeer"),
            "Non existing package e2xgradeeer should not be installed",
        )


class TestGetNbextensionUtils(unittest.TestCase):

    def test_nbclassic_is_installed(self):

        with patch("e2xgrader.extensions.utils.is_installed") as mock_is_installed:
            mock_is_installed.side_effect = lambda package: package == "nbclassic"
            with patch(
                "e2xgrader.extensions.utils.import_module"
            ) as mock_import_module:
                mock_import_module.return_value = MagicMock()
                get_nbextension_utils()
                mock_import_module.assert_called_once_with("nbclassic.nbextensions")

    def test_notebook_is_installed(self):
        with patch(
            "e2xgrader.extensions.utils.get_notebook_major_version"
        ) as mock_get_notebook_major_version:
            mock_get_notebook_major_version.return_value = 6
            with patch("e2xgrader.extensions.utils.is_installed") as mock_is_installed:
                mock_is_installed.side_effect = lambda package: package == "notebook"
                with patch(
                    "e2xgrader.extensions.utils.import_module"
                ) as mock_import_module:
                    mock_import_module.return_value = MagicMock()
                    get_nbextension_utils()
                    mock_import_module.assert_called_once_with("notebook.nbextensions")

    def test_not_installed(self):
        with patch("e2xgrader.extensions.utils.is_installed") as mock_is_installed:
            mock_is_installed.return_value = False
            self.assertIsNone(get_nbextension_utils())


class TestGetNotebookConfigManager(unittest.TestCase):

    def test_get_notebook_config_manager_is_not_installed(self):
        with patch("e2xgrader.extensions.utils.is_installed") as mock_is_installed:
            mock_is_installed.return_value = False
            config_manager = get_notebook_config_manager()
            self.assertIsNone(config_manager)

    def test_get_notebook_config_manager_from_jupyter_server(self):
        with patch("e2xgrader.extensions.utils.is_installed") as mock_is_installed:
            mock_is_installed.side_effect = lambda package: package == "jupyter_server"
            with patch(
                "e2xgrader.extensions.utils.import_module"
            ) as mock_import_module:
                mock_import_module.return_value = MagicMock()
                mock_import_module.return_value.BaseJSONConfigManager = "config_manager"
                config_manager = get_notebook_config_manager()
                mock_import_module.assert_called_once_with(
                    "jupyter_server.config_manager"
                )
                self.assertEqual(config_manager, "config_manager")

    def test_get_notebook_config_manager_from_notebook(self):
        with patch(
            "e2xgrader.extensions.utils.get_notebook_major_version"
        ) as mock_get_notebook_major_version:
            mock_get_notebook_major_version.return_value = 6
            with patch("e2xgrader.extensions.utils.is_installed") as mock_is_installed:
                mock_is_installed.side_effect = lambda package: package == "notebook"
                with patch(
                    "e2xgrader.extensions.utils.import_module"
                ) as mock_import_module:
                    mock_import_module.return_value = MagicMock()
                    mock_import_module.return_value.BaseJSONConfigManager = (
                        "config_manager"
                    )
                    config_manager = get_notebook_config_manager()
                    mock_import_module.assert_called_once_with(
                        "notebook.services.config.manager"
                    )
                    self.assertEqual(config_manager, "config_manager")
