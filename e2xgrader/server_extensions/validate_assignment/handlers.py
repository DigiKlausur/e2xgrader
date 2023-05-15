"""Tornado handlers for nbgrader assignment list web service."""

import json
import os
import traceback

from jupyter_core.paths import jupyter_config_path
from nbgrader.apps import NbGrader
from nbgrader.nbgraderformat import SchemaTooNewError, SchemaTooOldError
from nbgrader.server_extensions.validate_assignment.handlers import (
    NbGraderVersionHandler,
)
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join as ujoin
from tornado import web

from ...validator import E2XValidator

static = os.path.join(os.path.dirname(__file__), "static")


class ValidateAssignmentHandler(IPythonHandler):
    @property
    def notebook_dir(self):
        return self.settings["notebook_dir"]

    def load_config(self):
        paths = jupyter_config_path()
        paths.insert(0, os.getcwd())

        app = NbGrader()
        app.config_file_paths.append(paths)
        app.load_config_file()

        return app.config

    def validate_notebook(self, path):
        fullpath = os.path.join(self.notebook_dir, path)

        try:
            config = self.load_config()
            validator = E2XValidator(config=config)
            result = validator.validate(fullpath)

        except SchemaTooOldError:
            self.log.error(traceback.format_exc())
            msg = (
                "The notebook '{}' uses an old version "
                "of the nbgrader metadata format. Please **back up this "
                "notebook** and then update the metadata using:\n\nnbgrader update {}\n"
            ).format(fullpath, fullpath)
            self.log.error(msg)
            retvalue = {"success": False, "value": msg}

        except SchemaTooNewError:
            self.log.error(traceback.format_exc())
            msg = (
                "The notebook '{}' uses a newer version "
                "of the nbgrader metadata format. Please update your version of "
                "nbgrader to the latest version to be able to use this notebook."
            ).format(fullpath)
            self.log.error(msg)
            retvalue = {"success": False, "value": msg}

        except Exception:
            self.log.error(traceback.format_exc())
            retvalue = {"success": False, "value": traceback.format_exc()}

        else:
            retvalue = {"success": True, "value": result}

        return retvalue

    @web.authenticated
    def post(self):
        output = self.validate_notebook(self.get_argument("path"))
        self.finish(json.dumps(output))


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------

default_handlers = [
    (r"/assignments/validate", ValidateAssignmentHandler),
    (r"/nbgrader_version", NbGraderVersionHandler),
]


def load_jupyter_server_extension(nbapp):
    """Load the nbserver"""
    nbapp.log.info("Loading the validate_assignment e2xgrader serverextension")
    webapp = nbapp.web_app
    base_url = webapp.settings["base_url"]
    webapp.settings["notebook_dir"] = nbapp.notebook_dir
    webapp.add_handlers(
        ".*$", [(ujoin(base_url, pat), handler) for pat, handler in default_handlers]
    )
