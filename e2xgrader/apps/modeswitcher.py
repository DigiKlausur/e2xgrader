import json
import os
from enum import Enum
from typing import Union

from jupyter_core.application import JupyterApp
from jupyter_core.paths import ENV_CONFIG_PATH, SYSTEM_CONFIG_PATH, jupyter_config_dir
from traitlets import Any, default, validate

from ..extensions import E2xExtensionManager


class E2xGraderModes(Enum):
    """
    Enum class representing the different modes in E2xGrader.

    Attributes:
        EXAM (str): Represents the student exam mode.
        ASSIGNMENT (str): Represents the student mode.
        TEACHER (str): Represents the teacher mode.
        DEACTIVATED (str): Represents the deactivated mode.
    """

    EXAM = "student_exam"
    ASSIGNMENT = "student"
    TEACHER = "teacher"
    DEACTIVATED = "None"


class InvalidModeError(Exception):
    pass


def get_jupyter_config_path(user: bool = False, sys_prefix: bool = False) -> str:
    """
    Get the path to the Jupyter configuration directory.

    Args:
        user (bool): If True, returns the path to the user-specific Jupyter configuration directory.
        sys_prefix (bool): If True, returns the path to the system-wide Jupyter configuration
            directory.

    Returns:
        str: The path to the Jupyter configuration directory.

    Raises:
        ValueError: If both user and sys_prefix are set to True.

    """
    if user and sys_prefix:
        raise ValueError("Only one of user and sys_prefix should be True")
    elif sys_prefix:
        return ENV_CONFIG_PATH[0]
    elif user:
        return jupyter_config_dir()
    return SYSTEM_CONFIG_PATH[1]


class E2xModeSwitcher(JupyterApp):
    """
    A class for managing the mode switching functionality of E2xGrader.

    Attributes:
        mode (str): The current mode of E2xGrader.
    """

    mode = Any(
        default_value=E2xGraderModes.DEACTIVATED.value,
        allow_none=True,
        config=True,
        help="The current mode of E2xGrader",
    ).tag(to_config=True)

    @default("config_file_name")
    def _config_file_name_default(self) -> str:
        return "e2xgrader_config"

    @validate("mode")
    def _validate_mode(self, proposal):
        mode = proposal["value"]
        if mode is None:
            self.log.warning("No mode is set")
        else:
            mode = self.validate_mode(mode)
        # Make sure the mode is set in the config
        self.config[self.__class__.__name__]["mode"] = mode
        return mode

    def get_config_file(self, user: bool = False, sys_prefix: bool = False):
        return os.path.join(
            get_jupyter_config_path(user=user, sys_prefix=sys_prefix),
            f"{self.config_file_name}.json",
        )

    def validate_mode(self, mode):
        valid_modes = [m.value for m in E2xGraderModes]
        if isinstance(mode, E2xGraderModes):
            mode = mode.value
        if mode not in [m.value for m in E2xGraderModes]:
            raise InvalidModeError(
                f"Invalid mode: {mode}\nValid modes are: {valid_modes}"
            )
        return mode

    def activate_mode(
        self,
        mode: Union[E2xGraderModes, str],
        user: bool = False,
        sys_prefix: bool = True,
    ):
        """
        Activate the specified mode for E2xGrader.

        Args:
            mode (Union[E2xGraderModes, str]): The mode to activate.
            user (bool, optional): Whether to activate the mode for the current user.
                Defaults to False.
            sys_prefix (bool, optional): Whether to activate the mode for the system prefix.
                Defaults to True.
        """
        mode = self.validate_mode(mode)
        self.set_mode(mode)
        extension_manager = E2xExtensionManager()
        if mode == E2xGraderModes.DEACTIVATED.value:
            extension_manager.deactivate(sys_prefix=sys_prefix, user=user)
        else:
            getattr(extension_manager, f"activate_{mode}")(
                sys_prefix=sys_prefix, user=user
            )
        self.write_config_file(user=user, sys_prefix=sys_prefix)

    def set_mode(self, mode):
        """
        Set the mode of E2xGrader.

        Args:
            mode (str): The mode to set.
        """
        self.mode = mode

    def write_config_file(self, user=False, sys_prefix=False):
        """
        Write the E2xGrader config to a JSON file.

        Args:
            user (bool, optional): Whether to write the config for the current user.
                Defaults to False.
            sys_prefix (bool, optional): Whether to write the config for the system prefix.
                Defaults to False.
        """
        config_file = self.get_config_file(user=user, sys_prefix=sys_prefix)
        self.log.info(f"Writing e2xgrader config to: {config_file}")
        with open(config_file, "w") as f:
            json.dump(self.config, f, indent=4)


def get_e2xgrader_mode() -> E2xGraderModes:
    """
    Get the current mode of E2xGrader.

    Returns:
        E2xGraderModes: The current mode of E2xGrader.
    """
    mode_switcher = E2xModeSwitcher()
    mode_switcher.initialize([])
    for m in E2xGraderModes:
        if m.value == mode_switcher.mode:
            return m
