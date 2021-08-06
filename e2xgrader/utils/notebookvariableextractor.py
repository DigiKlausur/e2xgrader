import re
import nbformat


class NotebookVariableExtractor:

    def __init__(self):
        self.__pattern = re.compile(r'{{\s*(\w+)\s*}}')

    def extract(self, nb_path):
        nb = nbformat.read(nb_path, as_version=4)
        variables = []
        for cell in nb.cells:
            source = cell.source
            variables.extend(self.__pattern.findall(source))
        return variables
