import json

from e2xcore import BaseApp
from e2xcore.handlers import E2xApiHandler
from nbgrader.apps.baseapp import NbGrader
from nbgrader.server_extensions.formgrader.base import check_xsrf
from tornado import web
from traitlets import List, Unicode


class DiagramConfigHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        self.finish(json.dumps(self.settings.get("diagram_config", dict())))


class DiagramEditor(NbGrader, BaseApp):
    drawDomain = Unicode(
        default_value=None, allow_none=True, help="The url to drawio"
    ).tag(config=True)
    drawOrigin = Unicode(
        default_value=None, allow_none=True, help="The drawio origin"
    ).tag(config=True)
    libraries = List(default_value=[], help="A list of activated libraries").tag(
        config=True
    )

    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def get_diagram_config(self):
        # self.log.info("My drawDomain is", self.drawDomain)
        config = dict()
        if self.drawDomain:
            config["drawDomain"] = self.drawDomain
        if self.drawOrigin:
            config["drawOrigin"] = self.drawOrigin
        if len(self.libraries) > 0:
            config["libs"] = self.libraries
        return config

    def load_app(self):
        self.log.info("Loading the diagrameditor app")
        self.initialize([])
        self.update_tornado_settings(dict(diagram_config=self.get_diagram_config()))
        self.add_handlers(
            [
                (r"/e2x/diagrams/api", DiagramConfigHandler),
            ]
        )
