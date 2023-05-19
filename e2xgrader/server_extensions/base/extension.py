from importlib import import_module

from jinja2 import Environment, FileSystemLoader
from traitlets import Any, List, TraitError, validate
from traitlets.config import Application

from e2xgrader.utils import get_nbgrader_config


class BaseExtension(Application):
    apps = List(
        trait=Any(),
        default_value=[],
    ).tag(config=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = self.parent.log
        self.config = get_nbgrader_config()
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
        self.parent.web_app.settings["e2xgrader"] = {
            "jinja_env": Environment(loader=FileSystemLoader([]))
        }
