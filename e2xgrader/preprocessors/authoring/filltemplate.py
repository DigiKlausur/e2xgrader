import re
import os
import nbformat
from .preprocessor import Preprocessor


class FillTemplate(Preprocessor):

    def __init__(self):
        self.__pattern = re.compile(r'({{\s*(\w+)\s*}})')

    def replace(self, nb, replacements):
        replaced = nbformat.v4.new_notebook()
        variables = []
        for cell in nb.cells:
            source = cell.source
            variables = self.__pattern.findall(source)
            new_cell = cell.copy()
            for variable in variables:
                new_cell.source = new_cell.source.replace(variable[0], replacements[variable[1]])
            replaced.cells.append(new_cell)
        return replaced

    def preprocess(self, resources):
        template_path = os.path.join(
            resources['tmp_dir'],
            'template',
            resources['template'],
            '{}.ipynb'.format(resources['template'])
        )

        template_nb = nbformat.read(template_path, as_version=4)
        template_nb = self.replace(template_nb, resources['template-options'])
        nbformat.write(template_nb, template_path)
