import os

from nbgrader.apps.baseapp import NbGrader
from nbgrader.server_extensions.formgrader import handlers as nbgrader_handlers
from tornado import web

from e2xgrader.server_extensions.grader.apps.base.base import BaseApp

from .handlers import default_handlers


class FormgradeApp(NbGrader, BaseApp):

    template_path = os.path.join(os.path.dirname(__file__), "templates")
    static_path = os.path.join(os.path.dirname(__file__), "static")

    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def load_app(self):
        self.log.info("Loading the formgrader app")

        self.update_tornado_settings(
            dict(nbgrader_jinja2_env=self.webapp.settings["e2xgrader"]["jinja_env"])
        )
        self.add_template_path(self.template_path)
        self.add_template_path(nbgrader_handlers.template_path)
        self.add_handlers(default_handlers)
        self.add_handlers(nbgrader_handlers.default_handlers)

        static_handlers = [
            (
                r"/formgrader/static/(.*)",
                web.StaticFileHandler,
                {"path": nbgrader_handlers.static_path},
            ),
            (
                r"/e2xgrader/static/(.*)",
                web.StaticFileHandler,
                {"path": self.static_path},
            ),
        ]

        self.add_handlers(static_handlers)
