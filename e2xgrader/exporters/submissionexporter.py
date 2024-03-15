import os
from textwrap import dedent

from nbformat.v4 import new_markdown_cell
from traitlets import Unicode

from .exporter import E2xExporter


class SubmissionExporter(E2xExporter):
    """
    Exporter class for generating HTML submission files from a Jupyter notebook exam.
    """

    hashcode_cell_template_name = Unicode(
        "hashcode_cell.html", help="The name of the hashcode cell template."
    ).tag(config=True)

    exam_submitted_message = Unicode(
        "We have received your exam!",
        help="The message to display in the hashcode cell when the exam has been submitted.",
    ).tag(config=True)

    verify_exam_message = Unicode(
        "Verify your exam below and then close the browser and shut down your computer.",
        help=dedent(
            """
            The message to display in the hashcode cell telling the student to verify their exam.
            """
        ),
    ).tag(config=True)

    your_hashcode_message = Unicode(
        "Your hashcode:",
        help="The message to display in the hashcode cell before the hashcode.",
    ).tag(config=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = "form"

    @property
    def template_paths(self):
        return super().template_paths + [
            os.path.join(os.path.dirname(__file__), "templates")
        ]

    def from_notebook_node(self, nb, resources=None, **kw):
        hashcode_template = self.environment.get_template(
            self.hashcode_cell_template_name
        )
        hashcode_cell = new_markdown_cell(
            source=hashcode_template.render(
                hashcode=resources["hashcode"].upper(),
                timestamp=resources["timestamp"],
                exam_submitted_message=self.exam_submitted_message,
                verify_exam_message=self.verify_exam_message,
                your_hashcode_message=self.your_hashcode_message,
            ).replace("\n", ""),
            metadata={"name": "exam-submitted"},
        )
        nb.cells = [hashcode_cell] + nb.cells
        return super().from_notebook_node(nb, resources=resources, **kw)
