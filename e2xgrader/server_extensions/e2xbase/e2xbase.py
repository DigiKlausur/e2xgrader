import os
from tornado import web
from notebook.utils import url_path_join as ujoin
from traitlets.config import LoggingConfigurable


class E2xBaseExtension(LoggingConfigurable):
    def get_handlers(self):
        root_path = os.path.dirname(__file__)
        static_path = os.path.join(root_path, "static")
        handlers = [
            (
                r"/e2xbase/static/(.*)",
                web.StaticFileHandler,
                {
                    "path": static_path,
                },
            ),
        ]
        return handlers


def init_handlers(webapp):
    h = E2xBaseExtension().get_handlers()

    def rewrite(x):
        pat = ujoin(webapp.settings["base_url"], x[0].lstrip("/"))
        return (pat,) + x[1:]

    webapp.add_handlers(".*$", [rewrite(x) for x in h])


def load_jupyter_server_extension(nbapp):
    nbapp.log.info("Loading the e2xgrader base serverextension")
    webapp = nbapp.web_app
    init_handlers(webapp)
