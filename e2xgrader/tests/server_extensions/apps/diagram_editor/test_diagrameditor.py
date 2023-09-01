import unittest

from traitlets.config import LoggingConfigurable

from e2xgrader.server_extensions.apps.diagram_editor import DiagramEditor


class DummyWebApp:
    @property
    def settings(self):
        return dict()


class DummyApp(LoggingConfigurable):
    root_dir = "dummy"
    name = "dummy"

    @property
    def web_app(self):
        return DummyWebApp()


class TestDiagramEditor(unittest.TestCase):
    def setUp(self) -> None:
        self.editor = DiagramEditor(parent=DummyApp())

    def test_empty_config(self):
        self.assertDictEqual(self.editor.get_diagram_config(), dict())

    def test_configure_draw_domain(self):
        domain = "myDomain"
        self.editor.drawDomain = domain
        self.assertDictEqual(self.editor.get_diagram_config(), dict(drawDomain=domain))

    def test_configure_draw_origin(self):
        domain = "myDomain"
        self.editor.drawOrigin = domain
        self.assertDictEqual(self.editor.get_diagram_config(), dict(drawOrigin=domain))

    def test_configure_libraries(self):
        libraries = ["lib1", "lib2", "lib3"]
        self.editor.libraries = libraries
        self.assertDictEqual(self.editor.get_diagram_config(), dict(libs=libraries))

    def tearDown(self) -> None:
        self.editor.drawDomain = None
        self.editor.drawOrigin = None
        self.editor.libraries = []
