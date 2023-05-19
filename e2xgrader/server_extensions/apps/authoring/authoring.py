import os

from e2xgrader_base_app import BaseApp
from nbgrader.apps.baseapp import NbGrader
from tornado import web

from .apihandlers import default_handlers as default_api_handlers
from .handlers import default_handlers


class AuthoringApp(NbGrader, BaseApp):
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    static_path = os.path.join(os.path.dirname(__file__), "static")

    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def load_app(self):
        self.log.info("Loading the e2xgrader authoring app")
        self.add_template_path(self.template_path)
        self.add_handlers(default_api_handlers)
        self.add_handlers(default_handlers)
        static_handlers = [
            (
                r"/e2x/authoring/static/(.*)",
                web.StaticFileHandler,
                {"path": self.static_path},
            ),
        ]
        self.add_handlers(static_handlers)
