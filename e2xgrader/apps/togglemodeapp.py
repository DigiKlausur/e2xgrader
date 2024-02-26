from ..extensions import E2xExtensionManager
from .baseapp import E2xGrader


class ToggleModeApp(E2xGrader):

    flags = {
        "sys-prefix": (
            {"E2xGrader": {"sys_prefix": True}},
            "Install extensions to sys.prefix",
        ),
        "user": (
            {"E2xGrader": {"user": True}},
            "Install extensions to the user space",
        ),
    }

    def activate_mode(self):
        """
        Activates the specified mode by activating the corresponding extensions
        using the E2xExtensionManager.

        If the mode is "None", it deactivates all e2xgrader extensions.
        """
        extension_manager = E2xExtensionManager()
        if self.mode == "None":
            print(
                f"Deactivating e2xgrader extensions with sys_prefix={self.sys_prefix} "
                f"and user={self.user}"
            )
            extension_manager.deactivate(sys_prefix=self.sys_prefix, user=self.user)
        else:
            print(
                f"Activating mode {self.mode} with sys_prefix={self.sys_prefix} "
                f"and user={self.user}"
            )
            getattr(extension_manager, f"activate_{self.mode}")(
                sys_prefix=self.sys_prefix, user=self.user
            )
        self.log.info(
            f"Activated mode {self.mode}. "
            f"Writing config file to {self.get_config_file_path()}"
        )
        self.write_mode_config_file()

    def start(self) -> None:
        super().start()
        if self.sys_prefix and self.user:
            self.fail("Cannot install in both sys-prefix and user space")
