import re
import base64
import pickle
from . import NbGraderPreprocessor

class Unscramble(NbGraderPreprocessor):

    def __init__(self, **kw):
        self.__pattern = re.compile('{{([^{]+)}}')
        self.log.info('Init Unscramble')

    def preprocess(self, nb, resources):
        if 'scramble_config' not in nb.metadata:
            return nb, resources

        byte_config = nb.metadata.scramble_config.config
        config = pickle.loads(base64.b85decode(byte_config))

        for cell in nb.cells:
            matches = self.__pattern.findall(cell.source)
            for m in matches:
                if m.strip() in config:
                    cell.source = cell.source.replace('{{' + m + '}}', str(config[m.strip()]))

        nb.cells = nb.cells[1:]
        return nb, resources