from abc import abstractmethod


class ExtensionManager:
    @abstractmethod
    def deactivate(self, sys_prefix=True, user=False):
        pass

    @abstractmethod
    def activate_teacher(self, sys_prefix=True, user=False):
        pass

    @abstractmethod
    def activate_student(self, sys_prefix=True, user=False):
        pass

    @abstractmethod
    def activate_student_exam(self, sys_prefix=True, user=False):
        pass
