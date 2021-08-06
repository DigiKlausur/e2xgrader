import os
import nbformat
import shutil
from .basemodel import BaseModel
from traitlets import Unicode


class TemplateModel(BaseModel):

    directory = Unicode(
        'templates',
        help='The directory where the templates go.'
    )

    def __init__(self, course_prefix):
        super().__init__(course_prefix)
        os.makedirs(self.base_path(), exist_ok=True)

    def new(self, **kwargs):
        name = kwargs['name']
        if (self.is_valid_name(name)):
            path = os.path.join(self.base_path(), name)
            if (os.path.exists(path)):
                return {
                    'success': False,
                    'error': f'A template with the name {name} already exists!'
                }
            else:
                self.log.info('Creating a new template')
                self.log.info(name)
                os.makedirs(os.path.join(self.base_path(), name, 'img'), exist_ok=True)
                os.makedirs(os.path.join(self.base_path(), name, 'data'), exist_ok=True)
                filename = '{}.ipynb'.format(name)
                nb = nbformat.v4.new_notebook()
                nb.metadata['nbassignment'] = {
                    'type': 'template'
                }
                path = os.path.join(self.base_path(), name, filename)
                nbformat.write(nb, path)
                return {
                    'success': True,
                    'path': os.path.join('notebooks', path)
                }
        else:
            return {
                'success': False,
                'error': 'Invalid name'
            }

    def remove(self, **kwargs):
        name = kwargs['name']
        shutil.rmtree(os.path.join(self.base_path(), name))

    def list(self, **kwargs):
        templatefolders = os.listdir(self.base_path())
        templates = []
        for templatefolder in templatefolders:
            if templatefolder.startswith('.'):
                continue
            templates.append({
                'name': templatefolder,
                'link': os.path.join('tree', self.base_path(), templatefolder)
            })

        return templates
