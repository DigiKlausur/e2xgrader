import os

from e2xgrader_base_app import BaseApp
from nbgrader.apps.baseapp import NbGrader
from nbgrader.server_extensions.formgrader.apihandlers import default_handlers


class NbGraderApi(NbGrader, BaseApp):
    def __init__(self, **kwargs):
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def load_app(self):
        self.log.info("Loading the nbgrader api app")
        self.initialize([])

        course_dir = self.coursedir.root
        notebook_dir = self.parent.notebook_dir
        relpath = os.path.relpath(course_dir, notebook_dir)
        if relpath.startswith("../"):
            nbgrader_bad_setup = True
            self.log.error(
                "The course directory root is not a subdirectory of the notebook "
                "server root. This means that nbgrader will not work correctly. "
                "If you want to use nbgrader, please ensure the course directory "
                "root is in a subdirectory of the notebook root: %s",
                notebook_dir,
            )
        else:
            nbgrader_bad_setup = False

        tornado_settings = dict(
            nbgrader_url_prefix=os.path.relpath(
                self.coursedir.root, self.parent.notebook_dir
            ),
            nbgrader_coursedir=self.coursedir,
            nbgrader_authenticator=self.authenticator,
            nbgrader_gradebook=None,
            nbgrader_db_url=self.coursedir.db_url,
            nbgrader_bad_setup=nbgrader_bad_setup,
        )

        self.update_tornado_settings(tornado_settings)
        self.add_handlers(default_handlers)
