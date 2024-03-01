from textwrap import dedent

from jupyter_core.application import JupyterApp
from traitlets import Enum

from ..utils.mode import E2xGraderMode, infer_e2xgrader_mode


class E2xGrader(JupyterApp):

    mode = Enum(
        values=[mode.value for mode in E2xGraderMode],
        default_value=E2xGraderMode.INACTIVE.value,
        help=dedent(
            """
            Which mode is activated, can be teacher, student, student_exam or deactivated.
            Is set to invalid if the mode cannot be inferred.
        """
        ),
    )

    def fail(self, msg, *args):
        self.log.error(msg, *args)
        self.exit(1)

    def initialize(self, argv=None):
        try:
            mode = infer_e2xgrader_mode()
            self.mode = mode
        except ValueError as e:
            self.log.error(str(e))
            self.mode = E2xGraderMode.INVALID.value
        super().initialize(argv)
