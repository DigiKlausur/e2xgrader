from jupyter_core.application import JupyterApp
from traitlets import Enum

from ..utils.mode import infer_e2xgrader_mode


class E2xGrader(JupyterApp):

    mode = Enum(
        values=["teacher", "student", "student_exam", "None"],
        default_value="None",
        help="Which mode is activated, can be teacher, student or student_exam",
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
        super().initialize(argv)
