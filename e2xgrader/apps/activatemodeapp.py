from .togglemodeapp import ToggleModeApp


class ActivateModeApp(ToggleModeApp):
    description = "Activate a specific mode (teacher, student, student_exam)"

    def start(self) -> None:
        super().start()
        if len(self.extra_args) != 1:
            self.fail("Exactly one mode has to be specified")
        self.mode = self.extra_args[0]
        self.activate_mode()
