import json
import os

from jupyter_core.paths import jupyter_config_path

from .conf import (
    E2XGRADER_EXTENSIONS,
    E2XGRADER_STUDENT,
    E2XGRADER_STUDENT_EXAM,
    E2XGRADER_TEACHER,
    NBGRADER_EXTENSIONS,
)


def discover_jupyter_server_config_file(module_name: str):
    for path in jupyter_config_path():
        config_path = os.path.join(
            path, "jupyter_server_config.d", f"{module_name}.json"
        )
        if os.path.isfile(config_path):
            return config_path


class JupyterServerConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as f:
            self.config = json.loads(f.read())

    def save_config(self):
        with open(self.config_path, "w") as f:
            f.write(json.dumps(self.config, indent=2))

    def disable_extension(self, import_path):
        self.config["ServerApp"]["jpserver_extensions"][import_path] = False

    def enable_extension(self, import_path):
        self.config["ServerApp"]["jpserver_extensions"][import_path] = True


class E2xServerExtensionManager:
    def __init__(self):
        self.nbgrader_config_path = discover_jupyter_server_config_file("nbgrader")
        self.e2xgrader_config_path = discover_jupyter_server_config_file("e2xgrader")

    def deactivate(self, **kwargs):
        if self.nbgrader_config_path is not None:
            manager = JupyterServerConfigManager(self.nbgrader_config_path)
            for extension in NBGRADER_EXTENSIONS:
                manager.disable_extension(extension)
            manager.save_config()
        if self.e2xgrader_config_path is not None:
            manager = JupyterServerConfigManager(self.e2xgrader_config_path)
            for extension in E2XGRADER_EXTENSIONS:
                manager.disable_extension(extension)
            manager.save_config()

    def activate_extension(self, import_path: str) -> None:
        if self.e2xgrader_config_path is not None:
            manager = JupyterServerConfigManager(self.e2xgrader_config_path)
            manager.enable_extension(import_path)
            manager.save_config()

    def activate_teacher(self, **kwargs):
        self.deactivate()
        self.activate_extension(E2XGRADER_TEACHER)

    def activate_student(self, **kwargs):
        self.deactivate()
        self.activate_extension(E2XGRADER_STUDENT)

    def activate_student_exam(self, **kwargs):
        self.deactivate()
        self.activate_extension(E2XGRADER_STUDENT_EXAM)
