from traitlets import Unicode
import os
import nbformat
from .basemodel import BaseModel


class PresetModel(BaseModel):

    task_preset_path = Unicode(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'server_extensions/formgrader/presets/questions/'
        )
    ).tag(config=True)

    template_preset_path = Unicode(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'server_extensions/formgrader/presets/template/'
        )
    ).tag(config=True)

    def list_presets(self, preset_path):
        presets = []
        for item in os.listdir(preset_path):
            if '.ipynb_checkpoints' in item:
                continue
            if os.path.isfile(os.path.join(preset_path, item)) and \
               item.endswith('.ipynb'):
                presets.append(os.path.splitext(item)[0])
        return sorted(presets)

    def get_preset(self, preset_path, preset_name):
        path = os.path.join(preset_path, '{}.ipynb'.format(preset_name))
        if os.path.isfile(path):
            nb = nbformat.read(path, as_version=4)
            return nb.cells

    def list_question_presets(self):
        return self.list_presets(self.task_preset_path)

    def get_question_preset(self, preset_name):
        return self.get_preset(self.task_preset_path, preset_name)

    def list_template_presets(self):
        return self.list_presets(self.template_preset_path)

    def get_template_preset(self, preset_name):
        return self.get_preset(self.template_preset_path, preset_name)
