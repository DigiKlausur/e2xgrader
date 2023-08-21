from .base import BaseExtensionManager
from .utils import get_serverextension_toggle

NBGRADER_ASSIGNMENT_LIST = "nbgrader.server_extensions.assignment_list"
NBGRADER_FORMGRADER = "nbgrader.server_extensions.formgrader"
NBGRADER_VALIDATE_ASSIGNMENT = "nbgrader.server_extensions.validate_assignment"
NBGRADER_COURSE_LIST = "nbgrader.server_extensions.course_list"
NBGRADER_EXTENSIONS = [
    NBGRADER_ASSIGNMENT_LIST,
    NBGRADER_COURSE_LIST,
    NBGRADER_FORMGRADER,
    NBGRADER_VALIDATE_ASSIGNMENT,
]

E2XGRADER_TEACHER = "e2xgrader.server_extensions.teacher"
E2XGRADER_STUDENT = "e2xgrader.server_extensions.student"
E2XGRADER_STUDENT_EXAM = "e2xgrader.server_extensions.student_exam"
E2XGRADER_EXTENSIONS = [E2XGRADER_TEACHER, E2XGRADER_STUDENT, E2XGRADER_STUDENT_EXAM]

toggle_server_extension_python = get_serverextension_toggle()


class ServerExtensionManager(BaseExtensionManager):
    def __init__(self):
        super().__init__()
        if toggle_server_extension_python is None:
            self.log.warn("No server extension toggler found!")

    def deactivate(self, sys_prefix: bool = True, user: bool = False) -> None:
        for import_name in E2XGRADER_EXTENSIONS + NBGRADER_EXTENSIONS:
            toggle_server_extension_python(
                import_name=import_name, enabled=False, sys_prefix=sys_prefix, user=user
            )

    def activate_teacher(self, sys_prefix: bool = True, user: bool = False) -> None:
        kwargs = dict(sys_prefix=sys_prefix, user=user)
        self.deactivate(**kwargs)
        for import_name in [E2XGRADER_TEACHER, NBGRADER_COURSE_LIST]:
            toggle_server_extension_python(
                import_name=import_name, enabled=True, **kwargs
            )

    def activate_student(self, sys_prefix: bool = True, user: bool = False) -> None:
        kwargs = dict(sys_prefix=sys_prefix, user=user)
        self.deactivate(**kwargs)
        for import_name in [E2XGRADER_STUDENT, NBGRADER_COURSE_LIST]:
            toggle_server_extension_python(
                import_name=import_name, enabled=True, **kwargs
            )

    def activate_student_exam(self, sys_prefix=True, user=False):
        kwargs = dict(sys_prefix=sys_prefix, user=user)
        self.deactivate(**kwargs)
        for import_name in [E2XGRADER_STUDENT_EXAM, NBGRADER_COURSE_LIST]:
            toggle_server_extension_python(
                import_name=import_name, enabled=True, **kwargs
            )
