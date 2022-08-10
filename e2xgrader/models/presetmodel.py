import os

import nbformat
from traitlets import Unicode

from .basemodel import BaseModel


class PresetModel(BaseModel):

    task_preset_path = Unicode(
        os.path.join(os.path.dirname(__file__), "presets", "questions")
    ).tag(config=True)

    template_preset_path = Unicode(
        os.path.join(
            os.path.dirname(__file__),
            "presets",
            "template",
        )
    ).tag(config=True)

    extra_task_preset_path = Unicode(default_value=None, allow_none=True).tag(
        config=True
    )

    extra_template_preset_path = Unicode(default_value=None, allow_none=True).tag(
        config=True
    )

    def list_presets(self, preset_path):
        presets = []
        for item in os.listdir(preset_path):
            if ".ipynb_checkpoints" in item:
                continue
            if os.path.isfile(os.path.join(preset_path, item)) and item.endswith(
                ".ipynb"
            ):
                presets.append(os.path.splitext(item)[0])
        return sorted(presets)

    def get_preset(self, preset_path, preset_name):
        path = os.path.join(preset_path, "{}.ipynb".format(preset_name))
        if os.path.isfile(path):
            nb = nbformat.read(path, as_version=4)
            return nb.cells

    def list_question_presets(self):
        presets = self.list_presets(self.task_preset_path)
        if self.extra_task_preset_path is not None:
            presets.extend(self.list_presets(self.extra_task_preset_path))
        return presets

    def get_question_preset(self, preset_name):
        if preset_name in self.list_presets(self.task_preset_path):
            return self.get_preset(self.task_preset_path, preset_name)
        elif self.extra_task_preset_path is not None:
            return self.get_preset(self.extra_task_preset_path, preset_name)

    def list_template_presets(self):
        presets = self.list_presets(self.template_preset_path)
        if self.extra_template_preset_path is not None:
            presets.extend(self.list_presets(self.extra_task_preset_path))
        return presets

    def get_template_preset(self, preset_name):
        if preset_name in self.list_presets(self.template_preset_path):
            return self.get_preset(self.template_preset_path, preset_name)
        elif self.extra_template_preset_path is not None:
            return self.get_preset(self.extra_template_preset_path, preset_name)
