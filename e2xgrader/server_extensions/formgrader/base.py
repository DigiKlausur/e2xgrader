from nbgrader.server_extensions.formgrader.base import BaseApiHandler
from ...apps.api import E2xAPI


class E2xBaseApiHandler(BaseApiHandler):

    @property
    def api(self):
        level = self.log.level
        api = E2xAPI(self.coursedir, self.authenticator, parent=self.coursedir.parent)
        api.log_level = level
        return api