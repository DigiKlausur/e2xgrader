from importlib import import_module
from types import ModuleType
from typing import Optional


def get_notebook_config_manager() -> Optional[ModuleType]:
    return import_module("jupyter_server.config_manager").BaseJSONConfigManager


def get_serverextension_toggle() -> Optional[ModuleType]:
    def toggle_server_extension_python(**kwargs):
        module = import_module("jupyter_server.extension.serverextension")
        module.toggle_server_extension_python(**kwargs)

    return toggle_server_extension_python
