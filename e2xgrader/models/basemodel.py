import re

from nbgrader.apps import NbGrader
from traitlets import Unicode
from traitlets.config import LoggingConfigurable

from ..utils import get_nbgrader_config


class BaseModel(LoggingConfigurable):

    directory = Unicode(".", help="The directory of the model")

    def __init__(self, coursedir):
        self.coursedir = coursedir
        self.__pattern = re.compile(r"^\w+[\w\s]*\w+$")
        self.config = get_nbgrader_config()

    def base_path(self):
        return self.coursedir.format_path(self.directory, ".", ".")

    def is_valid_name(self, name):
        return self.__pattern.match(name) is not None
