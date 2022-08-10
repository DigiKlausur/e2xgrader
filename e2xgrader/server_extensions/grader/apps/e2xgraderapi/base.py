import json

from nbgrader.server_extensions.formgrader.base import BaseApiHandler, check_xsrf
from tornado import web

from e2xgrader.apps.api import E2xAPI


class E2xApiHandler(BaseApiHandler):
    @property
    def api(self):
        level = self.log.level
        api = E2xAPI(self.coursedir, self.authenticator, parent=self.coursedir.parent)
        api.log_level = level
        return api
