from ..extensions import E2xExtensionManager
from ..utils.mode import infer_e2xgrader_mode
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
        self.log.info(f"Activated mode {self.mode}. ")
        try:
            mode = infer_e2xgrader_mode()
            if mode != self.mode:
                self.log.warning(
                    f"The activated mode {self.mode} does not match the infered mode {mode}. \n"
                    f"The mode {mode} may be activated on a higher level."
                )
        except ValueError as e:
            self.log.error(str(e))

    def start(self) -> None:
        super().start()
        if self.sys_prefix and self.user:
            self.fail("Cannot install in both sys-prefix and user space")
