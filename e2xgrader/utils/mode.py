from enum import Enum
from typing import Dict

from jupyter_core.paths import jupyter_config_path

from .. import _jupyter_server_extension_paths
from ..extensions.utils import get_notebook_config_manager


class E2xGraderMode(Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    STUDENT_EXAM = "student_exam"
    INVALID = "invalid"
    INACTIVE = "inactive"


def get_serverextension_config() -> Dict[str, bool]:
    """
    Retrieves the server extension configuration from the Jupyter notebook configuration files.

    Returns:
        A dictionary containing the server extension configuration, where the keys are the
        extension names and the values are boolean values indicating whether the extension
        is enabled or not.
    """
    config = dict()
    for path in jupyter_config_path():
        contextmanager = get_notebook_config_manager()(config_dir=path)
        config.update(contextmanager.get("jupyter_notebook_config"))
    return config.get("NotebookApp", dict()).get("nbserver_extensions", dict())


def infer_serverextension_mode() -> str:
    """
    Infer the server extension mode based on the configuration.

    Returns:
        str: The server extension mode. Possible values are:
            - "None" if no server extension is active.
            - The name of the active server extension if only one is active.

    Raises:
        ValueError: If more than one server extension is active.
    """
    config = get_serverextension_config()
    active = []
    for extension in _jupyter_server_extension_paths():
        is_active = config.get(extension["module"], False)
        if is_active:
            active.append(extension["module"].split(".")[-1])
    if len(active) == 0:
        return E2xGraderMode.INACTIVE.value
    elif len(active) == 1:
        return active[0]
    raise ValueError("More than one mode is active" f"The current config is {config}")


def infer_e2xgrader_mode() -> str:
    """
    Infer the mode of e2xgrader.

    Returns:
        str: The mode of e2xgrader.

    """
    return infer_serverextension_mode()
