from typing import Dict, List

from notebook.nbextensions import (
    disable_nbextension,
    disable_nbextension_python,
    enable_nbextension,
    enable_nbextension_python,
    install_nbextension_python,
    uninstall_nbextension_python,
)

from e2xgrader import _jupyter_nbextension_paths
from e2xgrader.extension_config.base import ExtensionManager


class E2xNotebookExtensionManager(ExtensionManager):
    def discover_nbextensions(self, mode: str) -> List[Dict[str, str]]:
        extensions = list()
        for nbextension in _jupyter_nbextension_paths():
            if (
                f"{mode}_notebook" in nbextension["dest"]
                or f"{mode}_tree" in nbextension["dest"]
            ):
                extensions.append(
                    dict(require=nbextension["require"], section=nbextension["section"])
                )
        return extensions

    def enable_nbextensions(self, mode: str, sys_prefix=True, user=False) -> None:
        for nbextension in self.discover_nbextensions(mode):
            enable_nbextension(**nbextension, sys_prefix=sys_prefix, user=user)

    def install_nbextensions(self, module, sys_prefix=True, user=False):
        install_nbextension_python(
            module=module, sys_prefix=sys_prefix, user=user, overwrite=True
        )
        disable_nbextension_python(module=module, sys_prefix=sys_prefix, user=user)

    def deactivate(self, sys_prefix=True, user=False):
        for module in ["nbgrader", "e2xgrader"]:
            self.install_nbextensions(module, sys_prefix=sys_prefix, user=user)
            uninstall_nbextension_python(module, sys_prefix=sys_prefix, user=user)

    def activate_common(self, sys_prefix=True, user=False):
        self.deactivate()
        self.install_nbextensions("nbgrader", sys_prefix=sys_prefix, user=user)
        self.install_nbextensions("e2xgrader", sys_prefix=sys_prefix, user=user)

    def activate_teacher(self, sys_prefix=True, user=False):
        self.activate_common()
        self.enable_nbextensions(mode="teacher", sys_prefix=sys_prefix, user=user)
        # Configure nbgrader nbextensions
        enable_nbextension_python("nbgrader", sys_prefix=sys_prefix, user=user)
        disable_nbextension(
            require="create_assignment/main",
            section="notebook",
            sys_prefix=sys_prefix,
            user=user,
        )

    def activate_student(self, sys_prefix=True, user=False):
        self.activate_common()
        self.enable_nbextensions(mode="student", sys_prefix=sys_prefix, user=user)
        # Configure nbgrader nbextensions
        enable_nbextension(
            require="assignment_list/main",
            section="tree",
            sys_prefix=sys_prefix,
            user=user,
        )

    def activate_student_exam(self, sys_prefix=True, user=False):
        self.activate_common()
        self.enable_nbextensions(mode="student_exam", sys_prefix=sys_prefix, user=user)
        # Configure nbgrader nbextensions
        enable_nbextension(
            require="assignment_list/main",
            section="tree",
            sys_prefix=sys_prefix,
            user=user,
        )
