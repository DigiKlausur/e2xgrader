from .base import BaseExtensionManager
from .nbextensions import NbExtensionManager
from .serverextensions import ServerExtensionManager


class E2xExtensionManager(BaseExtensionManager):
    def __init__(self):
        super().__init__()
        self.managers = [NbExtensionManager(), ServerExtensionManager()]

    def deactivate(self, sys_prefix: bool = True, user: bool = False) -> None:
        for manager in self.managers:
            manager.deactivate(sys_prefix=sys_prefix, user=user)

    def activate_teacher(self, sys_prefix: bool = True, user: bool = False) -> None:
        for manager in self.managers:
            manager.activate_teacher(sys_prefix=sys_prefix, user=user)

    def activate_student(self, sys_prefix: bool = True, user: bool = False) -> None:
        for manager in self.managers:
            manager.activate_student(sys_prefix=sys_prefix, user=user)

    def activate_student_exam(
        self, sys_prefix: bool = True, user: bool = False
    ) -> None:
        for manager in self.managers:
            manager.activate_student_exam(sys_prefix=sys_prefix, user=user)
