from textwrap import dedent

from .activatemodeapp import ActivateModeApp
from .baseapp import E2xGrader
from .deactivatemodeapp import DeactivateModeApp
from .showmodeapp import ShowModeApp


class E2xGraderApp(E2xGrader):

    subcommands = dict(
        activate=(
            ActivateModeApp,
            dedent(
                """\
                Activate a specific mode (teacher, student, student_exam)
                """
            ).strip(),
        ),
        deactivate=(
            DeactivateModeApp,
            dedent(
                """\
                Deactivate all e2xgrader extensions
                """
            ).strip(),
        ),
        show_mode=(
            ShowModeApp,
            dedent(
                """\
                Show the currently active mode
                """
            ).strip(),
        ),
    )

    def start(self) -> None:
        super().start()
        if self.subapp is None:
            print(
                "No subcommand given (run with --help for options). List of subcommands:\n"
            )
            self.print_subcommands()


def main():
    E2xGraderApp.launch_instance()
