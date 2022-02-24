import os

import glob

from nbconvert.exporters.html import HTMLExporter
from nbgrader.server_extensions.formgrader import handlers as nbgrader_handlers

from .filters import Highlight2HTMLwithLineNumbers, RenderExtraCell


class E2xExporter(HTMLExporter):
    """
    My custom exporter
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs and "config" in kwargs and "HTMLExporter" in kwargs["config"]:
            self.template_file = kwargs["config"].HTMLExporter.template_file
        self.template_path.extend(
            [
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "server_extensions",
                        "formgrader",
                        "templates",
                    )
                )
            ]
            + [nbgrader_handlers.template_path]
        )

    def _template_file_default(self):
        return "formgrade.tpl"

    def discover_annotations(self, resources):
        resources["annotations"] = []
        if "metadata" not in resources or "path" not in resources["metadata"]:
            return

        path = resources["metadata"]["path"]

        for annoation in glob.glob(os.path.join(path, "annotations", "*.png")):
            resources["annotations"].append(
                os.path.splitext(os.path.basename(annoation))[0]
            )

    def from_notebook_node(self, nb, resources=None, **kw):
        self.discover_annotations(resources)

        langinfo = nb.metadata.get("language_info", {})
        lexer = langinfo.get("pygments_lexer", langinfo.get("name", None))
        self.register_filter("highlight_code_with_linenumbers", self.filters.get(
            "highlight_code_with_linenumbers",
            Highlight2HTMLwithLineNumbers(pygments_lexer=lexer, parent=self),
        ))

        self.register_filter("render_extracell", self.filters.get(
            "render_extracell",
            RenderExtraCell(parent=self)
        ))
        return super(E2xExporter, self).from_notebook_node(nb, resources, **kw)
