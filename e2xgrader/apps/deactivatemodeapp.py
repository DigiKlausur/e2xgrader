from .togglemodeapp import ToggleModeApp


class DeactivateModeApp(ToggleModeApp):
    description = "Deactivate all e2xgrader extensions"

    def start(self) -> None:
        super().start()
        if len(self.extra_args) != 0:
            self.fail("e2xgrader deactivate does not take any arguments.")
        self.mode = "None"
        self.activate_mode()
