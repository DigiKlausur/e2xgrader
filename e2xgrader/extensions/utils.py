from importlib import import_module
from types import ModuleType
from typing import Dict, List, Optional

from .. import _jupyter_nbextension_paths


def is_installed(package: str) -> bool:
    try:
        import_module(package)
        return True
    except ModuleNotFoundError:
        return False


def get_notebook_major_version() -> int:
    from notebook import __version__

    return int(__version__.split(".")[0])


def get_nbextension_utils() -> Optional[ModuleType]:
    if is_installed("notebook") and get_notebook_major_version() < 7:
        return import_module("notebook.nbextensions")
    if is_installed("nbclassic"):
        return import_module("nbclassic.nbextensions")
    return None


def discover_nbextensions(mode: str) -> List[Dict[str, str]]:
    extensions = list()
    for nbextension in _jupyter_nbextension_paths():
        if (
            f"{mode}_notebook" in nbextension["dest"]
            or f"{mode}_tree" in nbextension["dest"]
        ):
            extensions.append(
                dict(require=nbextension["require"], section=nbextension["section"])
            )
    return extensions


def get_serverextension_toggler() -> Optional[ModuleType]:
    if is_installed("notebook") and get_notebook_major_version() < 7:
        module = import_module("notebook.serverextensions")
        return module.ToggleServerExtensionApp()
    if is_installed("jupyter_server"):
        module = import_module("jupyter_server.extension.serverextension")
        toggler = module.ToggleServerExtensionApp
        toggler.toggle_server_extension_python = staticmethod(
            module.toggle_server_extension_python
        )
        return toggler()
    return None


def get_serverextension_toggle() -> Optional[ModuleType]:
    if is_installed("notebook") and get_notebook_major_version() < 7:
        module = import_module("notebook.serverextensions")
        return module.toggle_serverextension_python
    if is_installed("jupyter_server"):
        module = import_module("jupyter_server.extension.serverextension")
        return module.toggle_server_extension_python
    return None
