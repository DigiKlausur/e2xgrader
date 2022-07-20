import os
from importlib import import_module

from jinja2 import Environment, FileSystemLoader
from jupyter_core.paths import jupyter_config_path
from nbgrader.apps import NbGrader
from traitlets import Any, List, TraitError, validate
from traitlets.config import Application

from .apps.nbgraderapi import NbGraderApi


class E2xGrader(Application):

    apps = List(
        trait=Any(),
        default_value=[NbGraderApi],
    ).tag(config=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = self.parent.log
        self.load_config()
        self.log.info(self.apps)
        self.initialize_jinja_environment()
        self.initialize_apps()

    @validate("apps")
    def validate_apps(self, proposal):
        apps = []
        for app in proposal["value"]:
            if isinstance(app, str):
                module, klass = app.rsplit(".", 1)
                app = getattr(import_module(module), klass)
            if not callable(app):
                raise TraitError("apps must be callable")
            apps.append(app)
        return apps

    def initialize_apps(self):
        for app in self.apps:
            app(parent=self.parent).load_app()

    def initialize_jinja_environment(self):
        root_path = os.path.dirname(__file__)
        self.parent.web_app.settings["e2xgrader"] = {
            "jinja_env": Environment(loader=FileSystemLoader([]))
        }

    def load_config(self):
        app = NbGrader()
        app.load_config_file()
        self.config = app.config


def load_jupyter_server_extension(nbapp):
    """Load the e2xgrader serverextension"""
    nbapp.log.info("Loading the e2xgrader serverextension")
    e2xgrader = E2xGrader(parent=nbapp)
