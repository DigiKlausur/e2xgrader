from e2xcore import BaseApp

from .handlers import default_handlers


class ValidateAssignment(BaseApp):
    def load_app(self):
        self.log.info("Loading the e2x validate assignment app")
        self.add_handlers(default_handlers)
