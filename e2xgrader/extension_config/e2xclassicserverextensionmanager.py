from notebook.serverextensions import ToggleServerExtensionApp

from .conf import (
    E2XGRADER_EXTENSIONS,
    E2XGRADER_STUDENT,
    E2XGRADER_STUDENT_EXAM,
    E2XGRADER_TEACHER,
    NBGRADER_EXTENSIONS,
)


class E2xClassicServerExtensionManager:
    def enable_serverextension_py(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = True
        toggler.toggle_server_extension_python(module)

    def disable_serverextension(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = False
        toggler.toggle_server_extension(module)

    def enable_serverextension(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = True
        toggler.toggle_server_extension(module)

    def disable_serverextension_py(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = False
        toggler.toggle_server_extension_python(module)

    def deactivate(self, sys_prefix=True, user=False):
        for module in ["nbgrader", "e2xgrader"]:
            self.disable_serverextension_py(module, sys_prefix=sys_prefix, user=user)

    def activate_common(self, sys_prefix=True, user=False):
        self.deactivate(sys_prefix=sys_prefix, user=user)
        self.enable_serverextension_py("nbgrader", sys_prefix=sys_prefix, user=user)
        self.enable_serverextension_py("e2xgrader", sys_prefix=sys_prefix, user=user)
        for extension in NBGRADER_EXTENSIONS + E2XGRADER_EXTENSIONS:
            self.disable_serverextension(extension, sys_prefix=sys_prefix, user=user)

    def activate_teacher(self, sys_prefix=True, user=False):
        self.activate_common(sys_prefix=sys_prefix, user=user)
        self.enable_serverextension(E2XGRADER_TEACHER, sys_prefix=sys_prefix, user=user)

    def activate_student(self, sys_prefix=True, user=False):
        self.activate_common(sys_prefix=sys_prefix, user=user)
        self.enable_serverextension(E2XGRADER_STUDENT, sys_prefix=sys_prefix, user=user)

    def activate_student_exam(self, sys_prefix=True, user=False):
        self.activate_common(sys_prefix=sys_prefix, user=user)
        self.enable_serverextension(
            E2XGRADER_STUDENT_EXAM, sys_prefix=sys_prefix, user=user
        )
