import json
import os

from jupyter_core.application import JupyterApp
from jupyter_core.paths import ENV_CONFIG_PATH, SYSTEM_CONFIG_PATH, jupyter_config_dir
from traitlets import Bool, Enum, default
from traitlets.config import Config


def get_jupyter_config_path(user: bool = False, sys_prefix: bool = False) -> str:
    """
    Get the path to the Jupyter configuration directory.

    Args:
        user (bool, optional): If True, returns the user-specific configuration directory.
            Defaults to False.
        sys_prefix (bool, optional): If True, returns the system-wide configuration directory.
            Defaults to False.

    Returns:
        str: The path to the Jupyter configuration directory.

    Raises:
        ValueError: If both user and sys_prefix are set to True.

    """
    if user and sys_prefix:
        raise ValueError("Cannot install both in user and sys_prefix")
    if sys_prefix:
        return ENV_CONFIG_PATH[0]
    if user:
        return jupyter_config_dir()
    return SYSTEM_CONFIG_PATH[1]


class E2xGrader(JupyterApp):

    sys_prefix = Bool(False, help="Install extensions to sys.prefix", config=True)

    user = Bool(False, help="Install extensions to the user space", config=True)

    mode = Enum(
        values=["teacher", "student", "student_exam", "None"],
        default_value="None",
        help="Which mode is activated, can be teacher, student or student_exam",
        config=True,
    ).tag(to_config=True)

    def fail(self, msg, *args):
        self.log.error(msg, *args)
        self.exit(1)

    @default("config_file_name")
    def _config_file_name_default(self):
        return "e2xgrader_config"

    def get_config_file_path(self) -> str:
        """
        Returns the file path of the configuration file for the app.

        The file path is determined based on the user and system prefix.
        The configuration file name is appended with the '.json' extension.

        Returns:
            str: The file path of the configuration file.
        """
        return os.path.join(
            get_jupyter_config_path(self.user, self.sys_prefix),
            f"{self.config_file_name}.json",
        )

    def write_mode_config_file(self) -> None:
        """
        Writes the mode configuration to the e2xgrader_config.json file.

        Returns:
            None
        """
        config = Config()
        config.E2xGrader.mode = self.mode
        with open(self.get_config_file_path(), "w") as f:
            json.dump(config, f, indent=2)
