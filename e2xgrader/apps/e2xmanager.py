from typing import Dict, List

from notebook.nbextensions import (
    disable_nbextension,
    disable_nbextension_python,
    enable_nbextension,
    enable_nbextension_python,
    install_nbextension_python,
    uninstall_nbextension_python,
)
from notebook.serverextensions import ToggleServerExtensionApp

from .. import _jupyter_nbextension_paths

NBGRADER_FORMGRADER = "nbgrader.server_extensions.formgrader"
NBGRADER_ASSIGNMENT_LIST = "nbgrader.server_extensions.assignment_list"
NBGRADER_VALIDATE_ASSIGNMENT = "nbgrader.server_extensions.validate_assignment"
E2XGRADER_TEACHER = "e2xgrader.server_extensions.teacher"
E2XGRADER_STUDENT = "e2xgrader.server_extensions.student"
E2XGRADER_STUDENT_EXAM = "e2xgrader.server_extensions.student_exam"


class BaseExtensionManager:
    def install_nbextensions(self, module, sys_prefix=True, user=False):
        install_nbextension_python(
            module=module, sys_prefix=sys_prefix, user=user, overwrite=True
        )
        disable_nbextension_python(module=module, sys_prefix=sys_prefix, user=user)

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

    def disable_serverextension_py(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = False
        toggler.toggle_server_extension_python(module)


class E2xExtensionManager(BaseExtensionManager):
    def discover_nbextensions(self, section: str) -> List[Dict[str, str]]:
        extensions = list()
        for nbextension in _jupyter_nbextension_paths():
            if (
                f"{section}_notebook" in nbextension["dest"]
                or f"{section}_tree" in nbextension["dest"]
            ):
                extensions.append(
                    dict(require=nbextension["require"], section=nbextension["section"])
                )
        return extensions

    def deactivate(self, sys_prefix=True, user=False):
        for module in ["nbgrader", "e2xgrader"]:
            self.disable_serverextension_py(module, sys_prefix=sys_prefix, user=user)
            self.install_nbextensions(module, sys_prefix=sys_prefix, user=user)
            uninstall_nbextension_python(module, sys_prefix=sys_prefix, user=user)

    def activate_common(self, sys_prefix=True, user=False):
        self.enable_serverextension_py("nbgrader", sys_prefix=sys_prefix, user=user)
        self.disable_serverextension(NBGRADER_FORMGRADER)
        self.disable_serverextension(NBGRADER_ASSIGNMENT_LIST)
        self.disable_serverextension(NBGRADER_VALIDATE_ASSIGNMENT)
        self.install_nbextensions("nbgrader", sys_prefix=sys_prefix, user=user)

        self.enable_serverextension_py("e2xgrader", sys_prefix=sys_prefix, user=user)
        self.install_nbextensions("e2xgrader", sys_prefix=sys_prefix, user=user)

    def activate_teacher(self, sys_prefix=True, user=False):
        print(f"Activate teacher mode with sys_prefix = {sys_prefix} and user = {user}")
        self.activate_common(sys_prefix=sys_prefix, user=user)

        # Configure nbgrader nbextensions
        enable_nbextension_python("nbgrader", sys_prefix=sys_prefix, user=user)
        disable_nbextension(
            require="create_assignment/main",
            section="notebook",
            sys_prefix=sys_prefix,
            user=user,
        )

        # Enable e2xgrader nbextensions
        for nbextension in self.discover_nbextensions("teacher"):
            enable_nbextension(**nbextension, sys_prefix=sys_prefix, user=user)

        # Disable e2xgrader server extensions for other mode
        self.disable_serverextension(E2XGRADER_STUDENT)
        self.disable_serverextension(E2XGRADER_STUDENT_EXAM)

    def activate_student(self, sys_prefix=True, user=False):
        print(f"Activate student mode with sys_prefix = {sys_prefix} and user = {user}")
        self.activate_common(sys_prefix=sys_prefix, user=user)

        # Configure nbgrader nbextensions
        enable_nbextension(
            require="assignment_list/main",
            section="tree",
            sys_prefix=sys_prefix,
            user=user,
        )

        # Enable e2xgrader nbextensions
        for nbextension in self.discover_nbextensions("student"):
            enable_nbextension(**nbextension, sys_prefix=sys_prefix, user=user)

        # Disable e2xgrader server extensions for other mode
        self.disable_serverextension(E2XGRADER_TEACHER)
        self.disable_serverextension(E2XGRADER_STUDENT_EXAM)

    def activate_student_exam(self, sys_prefix=True, user=False):
        print(
            f"Activate student exam mode with sys_prefix = {sys_prefix} and user = {user}"
        )
        self.activate_common(sys_prefix=sys_prefix, user=user)

        # Configure nbgrader nbextensions
        enable_nbextension(
            require="assignment_list/main",
            section="tree",
            sys_prefix=sys_prefix,
            user=user,
        )

        # Enable e2xgrader nbextensions
        for nbextension in self.discover_nbextensions("student_exam"):
            enable_nbextension(**nbextension, sys_prefix=sys_prefix, user=user)

        # Disable e2xgrader server extensions for other mode
        self.disable_serverextension(E2XGRADER_TEACHER)
        self.disable_serverextension(E2XGRADER_STUDENT)
