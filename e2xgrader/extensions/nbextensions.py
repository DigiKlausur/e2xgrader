from .base import BaseExtensionManager
from .utils import discover_nbextensions, get_nbextension_utils


class NbExtensionManager(BaseExtensionManager):
    def __init__(self):
        super().__init__()
        self.utils = get_nbextension_utils()
        if self.utils is None:
            self.log.warn(
                "Neither notebook<7 or nbclassic found. Won't install nbextensions."
            )
        self.modules = ["e2xgrader", "nbgrader"]

    def enable_nbextensions(
        self, mode: str, sys_prefix: bool = True, user: bool = False
    ) -> None:
        for nbextension in discover_nbextensions(mode):
            self.utils.enable_nbextension(
                **nbextension, sys_prefix=sys_prefix, user=user
            )

    def deactivate(self, sys_prefix: bool = True, user: bool = False) -> None:
        if self.utils is None:
            return
        for module in self.modules:
            kwargs = dict(module=module, sys_prefix=sys_prefix, user=user)
            self.utils.install_nbextension_python(**kwargs)
            self.utils.disable_nbextension_python(**kwargs)
            self.utils.uninstall_nbextension_python(**kwargs)

    def activate_common(self, sys_prefix: bool = True, user: bool = False) -> None:
        self.deactivate(sys_prefix=sys_prefix, user=user)
        for module in self.modules:
            kwargs = dict(module=module, sys_prefix=sys_prefix, user=user)
            self.utils.install_nbextension_python(**kwargs)
            self.utils.disable_nbextension_python(**kwargs)

    def activate_teacher(self, sys_prefix: bool = True, user: bool = False) -> None:
        if self.utils is None:
            return
        self.activate_common(sys_prefix=sys_prefix, user=user)
        self.enable_nbextensions(mode="teacher", sys_prefix=sys_prefix, user=user)
        self.utils.enable_nbextension_python(
            "nbgrader", sys_prefix=sys_prefix, user=user
        )
        self.utils.disable_nbextension(
            require="create_assignment/main",
            section="notebook",
            sys_prefix=sys_prefix,
            user=user,
        )

    def activate_student(self, sys_prefix: bool = True, user: bool = False) -> None:
        if self.utils is None:
            return
        self.activate_common(sys_prefix=sys_prefix, user=user)
        self.enable_nbextensions(mode="student", sys_prefix=sys_prefix, user=user)
        self.utils.enable_nbextension(
            require="assignment_list/main",
            section="tree",
            sys_prefix=sys_prefix,
            user=user,
        )

    def activate_student_exam(
        self, sys_prefix: bool = True, user: bool = False
    ) -> None:
        if self.utils is None:
            return
        self.activate_common(sys_prefix=sys_prefix, user=user)
        self.enable_nbextensions(mode="student_exam", sys_prefix=sys_prefix, user=user)
        self.utils.enable_nbextension(
            require="assignment_list/main",
            section="tree",
            sys_prefix=sys_prefix,
            user=user,
        )
