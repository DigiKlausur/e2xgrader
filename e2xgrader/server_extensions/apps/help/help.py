import os

from e2xcore import BaseApp
from nbgrader.apps.baseapp import NbGrader
from tornado import web
from traitlets import List, Unicode

from .apihandlers import default_handlers


class Help(NbGrader, BaseApp):
    static_path = Unicode(
        os.path.join(os.path.dirname(__file__), "static"),
        help="path to static files shipped with package",
    ).tag(config=True)

    shared_path = Unicode(
        None, help="path to extra files served under /e2x/help/shared", allow_none=True
    ).tag(config=True)

    shared_paths = List(
        trait=Unicode(),
        default_value=[],
        help="List of paths of files served via the help app",
    ).tag(config=True)

    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def get_static_handlers(self):
        static_handlers = [
            (
                r"/e2x/help/static/base/(.*)",
                web.StaticFileHandler,
                dict(path=self.static_path, default_filename="index.html"),
            ),
        ]
        for idx, path in enumerate(self.shared_paths):
            static_handlers.append(
                (
                    f"/e2x/help/static/{idx}/(.*)",
                    web.StaticFileHandler,
                    dict(path=path, default_filename="index.html"),
                )
            )
        return static_handlers

    def load_app(self):
        self.initialize([])
        self.log.info("Loading the e2xgrader help app")

        self.update_tornado_settings(
            dict(
                e2xhelp_shared_dirs={
                    str(idx): path for idx, path in enumerate(self.shared_paths)
                }
            )
        )
        self.add_handlers(self.get_static_handlers() + default_handlers)
