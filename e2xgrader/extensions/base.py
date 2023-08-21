from abc import abstractmethod

from traitlets.config import LoggingConfigurable


class BaseExtensionManager(LoggingConfigurable):
    @abstractmethod
    def deactivate(self, sys_prefix: bool = True, user: bool = False) -> None:
        pass

    @abstractmethod
    def activate_teacher(self, sys_prefix: bool = True, user: bool = False) -> None:
        pass

    @abstractmethod
    def activate_student(self, sys_prefix: bool = True, user: bool = False) -> None:
        pass

    @abstractmethod
    def activate_student_exam(self, sys_prefix=True, user=False):
        pass
