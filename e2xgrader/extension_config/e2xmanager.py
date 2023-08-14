from .e2xclassicserverextensionmanager import E2xClassicServerExtensionManager
from .e2xnotebookextensionmanager import E2xNotebookExtensionManager
from .e2xserverextensionmanager import E2xServerExtensionManager


class E2xExtensionManager:
    def __init__(self):
        self.managers = [
            E2xNotebookExtensionManager(),
            E2xClassicServerExtensionManager(),
            E2xServerExtensionManager(),
        ]

    def deactivate(self, sys_prefix=True, user=False):
        for manager in self.managers:
            manager.deactivate(sys_prefix=sys_prefix, user=user)

    def activate_teacher(self, sys_prefix=True, user=False):
        for manager in self.managers:
            manager.activate_teacher(sys_prefix=sys_prefix, user=user)

    def activate_student(self, sys_prefix=True, user=False):
        for manager in self.managers:
            manager.activate_student(sys_prefix=sys_prefix, user=user)

    def activate_student_exam(self, sys_prefix=True, user=False):
        for manager in self.managers:
            manager.activate_student_exam(sys_prefix=sys_prefix, user=user)
