import os

from e2xcore import BaseApp
from nbgrader.apps.baseapp import NbGrader

from .apihandlers import default_handlers


class E2xGraderApi(NbGrader, BaseApp):
    template_path = os.path.join(os.path.dirname(__file__), "templates")

    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def load_app(self):
        self.log.info("Loading the e2xgrader api app")
        self.add_template_path(self.template_path)
        self.add_handlers(default_handlers)
