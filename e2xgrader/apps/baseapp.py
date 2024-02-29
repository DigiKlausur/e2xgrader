from jupyter_core.application import JupyterApp
from traitlets import Bool, Enum

from ..utils.mode import infer_e2xgrader_mode


class E2xGrader(JupyterApp):

    sys_prefix = Bool(False, help="Install extensions to sys.prefix", config=True)

    user = Bool(False, help="Install extensions to the user space", config=True)

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
