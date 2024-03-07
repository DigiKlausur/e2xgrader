from ..utils.mode import E2xGraderMode
from .togglemodeapp import ToggleModeApp


class ActivateModeApp(ToggleModeApp):
    description = "Activate a specific mode (teacher, student, student_exam)"

    def start(self) -> None:
        super().start()
        if len(self.extra_args) != 1:
            self.fail("Exactly one mode has to be specified")
        if self.extra_args[0] not in [
            E2xGraderMode.TEACHER.value,
            E2xGraderMode.STUDENT.value,
            E2xGraderMode.STUDENT_EXAM.value,
        ]:
            self.fail(
                f"Mode {self.extra_args[0]} is not a valid mode that can be activated."
            )
        self.mode = self.extra_args[0]

        self.activate_mode()
