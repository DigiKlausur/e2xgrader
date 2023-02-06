from traitlets import Unicode
from traitlets.config import LoggingConfigurable


class Preprocessor(LoggingConfigurable):
    template_path = Unicode("templates")
    task_path = Unicode("pools")

    def preprocess(self, resources):
        raise NotImplementedError
