from traitlets.config import LoggingConfigurable
from traitlets import Unicode

class BaseModel(LoggingConfigurable):

    directory = Unicode(
        '.',
        help='The directory of the model'
    )

    def __init__(self, coursedir):
        self.coursedir = coursedir

    def base_path(self):
        return self.coursedir.format_path(self.directory, '.', '.')