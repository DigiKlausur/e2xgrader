import json

from nbgrader.server_extensions.formgrader.base import BaseApiHandler
from ...apps.api import E2xAPI
from tornado import web
from nbgrader.server_extensions.formgrader.base import check_xsrf


class E2xBaseApiHandler(BaseApiHandler):
    @property
    def api(self):
        level = self.log.level
        api = E2xAPI(self.coursedir, self.authenticator, parent=self.coursedir.parent)
        api.log_level = level
        return api


class BaseApiManageHandler(BaseApiHandler):
    def initialize(self, model_cls):
        self.__model = model_cls(self.coursedir)

    @web.authenticated
    @check_xsrf
    def post(self, **kwargs):
        self.write(self.__model.new(**kwargs))

    @web.authenticated
    @check_xsrf
    def delete(self, **kwargs):
        self.__model.remove(**kwargs)
        self.write({"status": True})

    @web.authenticated
    @check_xsrf
    def get(self, **kwargs):
        self.write(json.dumps(self.__model.get(**kwargs)))

    @web.authenticated
    @check_xsrf
    def put(self, **kwargs):
        self.write(self.__model.new(**kwargs))


class BaseApiListHandler(BaseApiHandler):
    def initialize(self, model_cls):
        self.__model = model_cls(self.coursedir)

    @web.authenticated
    @check_xsrf
    def get(self, **kwargs):
        self.write(json.dumps(self.__model.list(**kwargs)))
