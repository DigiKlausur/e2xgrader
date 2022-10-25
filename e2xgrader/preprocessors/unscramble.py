import base64
import pickle
import re

from nbgrader.preprocessors import NbGraderPreprocessor


class Unscramble(NbGraderPreprocessor):
    def __init__(self, **kw):
        self.__pattern = re.compile("{{([^{]+)}}")
        self.log.info("Init Unscramble")

    def preprocess(self, nb, resources):
        if "scramble_config" in nb.metadata:
            byte_config = nb.metadata.scramble_config.config
            config = pickle.loads(base64.b85decode(byte_config))

            for cell in nb.cells:
                matches = self.__pattern.findall(cell.source)
                for m in matches:
                    if m.strip() in config:
                        cell.source = cell.source.replace(
                            "{{" + m + "}}", str(config[m.strip()])
                        )

        return nb, resources
