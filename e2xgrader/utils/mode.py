import os
from enum import Enum
from typing import Dict

from jupyter_core.paths import jupyter_config_path

from .. import _jupyter_server_extension_paths
from ..extensions.utils import discover_nbextensions, get_notebook_config_manager


class E2xGraderMode(Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    STUDENT_EXAM = "student_exam"
    INVALID = "invalid"
    INACTIVE = "inactive"


def get_nbextension_config() -> Dict[str, Dict[str, bool]]:
    """
    Get the configuration for nbextensions.

    Returns:
        A dictionary containing the configuration for nbextensions.
        The dictionary has the following structure:
        {
            'tree': {
                'nbextension_name': True/False,
                ...
            },
            'notebook': {
                'nbextension_name': True/False,
                ...
            }
        }
    """
    config = dict(tree=dict(), notebook=dict())
    for path in jupyter_config_path():
        config_path = os.path.join(path, "nbconfig")
        contextmanager = get_notebook_config_manager()(config_dir=config_path)
        for key in config:
            config[key].update(contextmanager.get(key))
    return config


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


def infer_nbextension_mode() -> str:
    """
    Infer the active mode for the nbextension based on the current configuration.

    Returns:
        str: The active mode for the nbextension.

    Raises:
        ValueError: If more than one mode is active or if tree and notebook extensions don't match.
    """
    config = get_nbextension_config()
    modes = [
        E2xGraderMode.TEACHER.value,
        E2xGraderMode.STUDENT_EXAM.value,
        E2xGraderMode.STUDENT.value,
    ]
    is_active = dict(tree=[], notebook=[])
    for mode in modes:
        for extension in discover_nbextensions(mode):
            if (
                config[extension["section"]]
                .get("load_extensions", dict())
                .get(extension["require"], False)
            ):
                is_active[extension["section"]].append(mode)

    if set(is_active["tree"]) == set(is_active["notebook"]):
        if len(is_active["tree"]) == 1:
            return is_active["tree"][0]
        elif len(is_active["tree"]) == 0:
            return E2xGraderMode.INACTIVE.value
    raise ValueError(
        "More than one mode is active or tree and notebook extensions don't match\n"
        f"The current config is {config}"
    )


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

    Raises:
        ValueError: If the nbextension mode and serverextension mode do not match.
    """
    nbextension_mode = infer_nbextension_mode()
    serverextension_mode = infer_serverextension_mode()
    if nbextension_mode == serverextension_mode:
        return nbextension_mode
    raise ValueError(
        "The nbextension and serverextension mode does not match"
        f"nbextension mode is {nbextension_mode}, serverextension_mode is {serverextension_mode}"
    )
