import os
import os.path

import glob

from traitlets import Unicode
from nbconvert.exporters.html import HTMLExporter
from jinja2 import contextfilter
from bs4 import BeautifulSoup
from nbgrader.server_extensions.formgrader import handlers as nbgrader_handlers

from ..utils import extra_cells as utils
from .filters import Highlight2HTMLwithLineNumbers


class E2xExporter(HTMLExporter):
    """
    My custom exporter
    """

    extra_cell_field = Unicode(
        "extended_cell", help="The name of the extra cell metadata field."
    )

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

    @contextfilter
    def to_choicecell(self, context, source):
        cell = context.get("cell", {})
        soup = BeautifulSoup(source, "html.parser")
        my_type = None
        if not soup.ul or not utils.is_extra_cell(cell):
            return soup.prettify().replace("\n", "")
        if utils.is_singlechoice(cell):
            my_type = "radio"
        elif utils.is_multiplechoice(cell):
            my_type = "checkbox"
        form = soup.new_tag("form")
        form["class"] = "hbrs_checkbox"

        list_elems = soup.ul.find_all("li")
        for i in range(len(list_elems)):
            div = soup.new_tag("div")
            box = soup.new_tag("input")
            box["type"] = my_type
            box["value"] = i
            box["disabled"] = "disabled"
            if i in utils.get_choices(cell):
                box["checked"] = "checked"
            div.append(box)
            children = [c for c in list_elems[i].children]
            for child in children:
                div.append(child)

            if utils.has_solution(cell):
                check = soup.new_tag("span")
                if i in utils.get_instructor_choices(cell):
                    check.string = "correct"
                    check["style"] = "color:green"
                else:
                    check.string = "false"
                    check["style"] = "color:red"
                div.append(check)
            form.append(div)
        soup.ul.replaceWith(form)
        return soup.prettify().replace("\n", "")

    def default_filters(self):
        for pair in super(E2xExporter, self).default_filters():
            yield pair
        yield ("to_choicecell", self.to_choicecell)

    def _template_file_default(self):
        return "formgrade.tpl"

    def discover_annotations(self, resources):
        path = resources["metadata"]["path"]
        resources["annotations"] = []

        for annoation in glob.glob(os.path.join(path, "annotations", "*.png")):
            resources["annotations"].append(
                os.path.splitext(os.path.basename(annoation))[0]
            )

    def from_notebook_node(self, nb, resources=None, **kw):
        self.discover_annotations(resources)
        langinfo = nb.metadata.get("language_info", {})
        lexer = langinfo.get("pygments_lexer", langinfo.get("name", None))
        highlight_code = self.filters.get(
            "highlight_code_with_linenumbers",
            Highlight2HTMLwithLineNumbers(pygments_lexer=lexer, parent=self),
        )
        self.register_filter("highlight_code_with_linenumbers", highlight_code)
        return super(E2xExporter, self).from_notebook_node(nb, resources, **kw)
