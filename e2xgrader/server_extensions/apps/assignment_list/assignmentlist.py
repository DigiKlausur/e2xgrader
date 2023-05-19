from e2xgrader_base_app import BaseApp

from .handlers import default_handlers


class AssignmentList(BaseApp):
    def load_app(self):
        self.add_handlers(default_handlers)
