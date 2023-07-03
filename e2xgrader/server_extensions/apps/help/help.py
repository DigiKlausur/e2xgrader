import os

from e2xcore import BaseApp
from nbgrader.apps.baseapp import NbGrader
from tornado import web
from traitlets import Unicode

from .apihandlers import default_handlers


class Help(NbGrader, BaseApp):
    static_path = Unicode(
        os.path.join(os.path.dirname(__file__), "static"),
        help="path to static files shipped with package",
    )

    shared_path = Unicode(
        None, help="path to extra files served under /e2x/help/shared", allow_none=True
    ).tag(config=True)

    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def load_app(self):
        self.initialize([])
        self.log.info("Loading the e2xgrader api app")
        self.log.info(f"My paths are: {self.shared_path} and {self.static_path}")
        handlers = [
            (
                r"/e2x/help/static/(.*)",
                web.StaticFileHandler,
                {"path": self.static_path},
            ),
        ]
        if self.shared_path is not None:
            handlers.append(
                (
                    r"/e2x/help/shared/(.*)",
                    web.StaticFileHandler,
                    {"path": self.shared_path, "default_filename": "index.html"},
                )
            )
        self.update_tornado_settings(dict(e2xhelp_shared_dir=self.shared_path))
        self.add_handlers(handlers + default_handlers)
