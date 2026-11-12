import os

from e2xcore import BaseApp
from nbgrader.apps.baseapp import NbGrader
from nbgrader.server_extensions.formgrader.apihandlers import default_handlers
from traitlets import Bool


class NbGraderApi(NbGrader, BaseApp):
    # nbgrader >= 0.9: the formgrader pages read `formgrader.debug` (AttributeError without it).
    debug = Bool(
        False,
        help="Show the loaded configuration in 'Formgrader -> Manage Assignments'.",
    ).tag(config=True)

    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)
        self.root_dir = self.parent.root_dir

    @property
    def url_prefix(self):
        relpath = os.path.relpath(self.coursedir.root, self.root_dir)
        return relpath

    def load_app(self):
        self.log.info("Loading the nbgrader api app")
        self.initialize([])

        relpath = self.url_prefix
        if relpath.startswith("../"):
            nbgrader_bad_setup = True
            self.log.error(
                "The course directory root is not a subdirectory of the notebook "
                "server root. This means that nbgrader will not work correctly. "
                "If you want to use nbgrader, please ensure the course directory "
                "root is in a subdirectory of the notebook root: %s",
                self.root_dir,
            )
        else:
            nbgrader_bad_setup = False

        # Save which kind of application is running : Jupyterlab like or classic Notebook
        self.webapp.settings["is_jlab"] = self.name != "jupyter-notebook"

        tornado_settings = dict(
            nbgrader_url_prefix=self.url_prefix,
            nbgrader_formgrader=self,
            nbgrader_coursedir=self.coursedir,
            nbgrader_authenticator=self.authenticator,
            nbgrader_gradebook=None,
            nbgrader_db_url=self.coursedir.db_url,
            nbgrader_bad_setup=nbgrader_bad_setup,
            # nbgrader >= 0.9: the formgrader handler resets its config to this on each
            # request (KeyError without it).
            initial_config=self.config,
        )

        self.update_tornado_settings(tornado_settings)
        self.add_handlers(default_handlers)
