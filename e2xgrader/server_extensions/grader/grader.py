# coding: utf-8

import os

from traitlets import default
from tornado import web
from jinja2 import Environment, FileSystemLoader
from notebook.utils import url_path_join as ujoin

from . import handlers, apihandlers
from nbgrader.apps.baseapp import NbGrader

class GraderExtension(NbGrader):

    name = u'grader'
    description = u'Create a jupyter notebook assignment'

    @default("classes")
    def _classes_default(self):
        classes = super(GraderExtension, self)._classes_default()
        return classes

    def build_extra_config(self):
        extra_config = super(GraderExtension, self).build_extra_config()

        return extra_config

    def init_tornado_settings(self, webapp):
        # Init jinja environment
        jinja_env = Environment(loader=FileSystemLoader([handlers.template_path]))

        # Configure the formgrader settings
        tornado_settings = dict(
            grader_url_prefix=os.path.relpath(self.coursedir.root, self.parent.notebook_dir),
            grader_coursedir=self.coursedir,
            grader_authenticator=self.authenticator,
            grader_gradebook=None,
            grader_db_url=self.coursedir.db_url,
            grader_jinja2_env_ui=jinja_env,
        )

        webapp.settings.update(tornado_settings)

    def init_handlers(self, webapp):
        h = []
        h.extend(handlers.default_handlers)
        h.extend(apihandlers.default_handlers)
        h.extend([
            (r"/grader/static/(.*)", web.StaticFileHandler, {'path': handlers.static_path}),
            (r"/grader/.*", handlers.Template404)
        ])

        def rewrite(x):
            pat = ujoin(webapp.settings['base_url'], x[0].lstrip('/'))
            return (pat,) + x[1:]

        webapp.add_handlers(".*$", [rewrite(x) for x in h])

    def start(self):
        raise NotImplementedError


def load_jupyter_server_extension(nbapp):
    """Load the formgrader extension"""
    nbapp.log.info("Loading the Grader serverextension")
    webapp = nbapp.web_app
    taskcreator = GraderExtension(parent=nbapp)
    taskcreator.log = nbapp.log
    taskcreator.initialize([])
    taskcreator.init_tornado_settings(webapp)
    taskcreator.init_handlers(webapp)