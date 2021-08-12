from traitlets.config import LoggingConfigurable, Config
from traitlets import List
from traitlets.utils.importstring import import_item


class Converter(LoggingConfigurable):

    preprocessors = List([], help="List of preprocessors for the converter")

    def __init__(self, config=None):
        with_default_config = self.default_config()
        if config:
            with_default_config.merge(config)
        self.init_preprocessors()

    def init_preprocessors(self):
        self._preprocessors = []
        for preprocessor in self.preprocessors:
            if isinstance(preprocessor, type):
                self._preprocessors.append(preprocessor())
            else:
                self._preprocessors.append(import_item(preprocessor)())

    def default_config(self):
        return Config()

    def convert(self, resources):
        for preprocessor in self._preprocessors:
            preprocessor.preprocess(resources)
