import os
import sys
from binascii import a2b_base64

from nbgrader.preprocessors import NbGraderPreprocessor
from traitlets import Set, Unicode

from ..utils.extra_cells import is_attachment_cell, is_diagram


class ExtractAttachments(NbGraderPreprocessor):
    subdirectory = Unicode("attachments").tag(config=True)

    output_filename_template = Unicode("attach_{cell_index}_{name}").tag(config=True)

    extract_output_types = Set(
        {"image/png", "image/jpeg", "image/svg+xml", "application/pdf"}
    ).tag(config=True)

    def preprocess(self, nb, resources):
        # Get files directory if it has been specified
        self.path = os.path.join(resources["metadata"]["path"], self.subdirectory)
        os.makedirs(self.path, exist_ok=True)

        for cell_index, cell in enumerate(nb.cells):
            cell, resources = self.preprocess_cell(cell, resources, cell_index)

        return nb, resources

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Apply a transformation on each cell,

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """

        if not (is_attachment_cell(cell) or is_diagram(cell)):
            return cell, resources

        if is_diagram(cell):
            # Remove the attachment line from source
            cell.source = cell.source.replace("![diagram](attachment:diagram.png)", "")

        # Get files directory if it has been specified
        output_files_dir = resources.get("output_files_dir", None)

        # Make sure outputs key exists
        if not isinstance(resources["outputs"], dict):
            resources["outputs"] = {}

        to_delete = []

        # Loop through all of the attachments in the cell
        for name, attach in cell.get("attachments", {}).items():
            for mime, data in attach.items():
                if mime not in self.extract_output_types:
                    continue

                # Binary files are base64-encoded, SVG is already XML
                if mime in {"image/png", "image/jpeg", "application/pdf"}:
                    # data is b64-encoded as text (str, unicode),
                    # we want the original bytes
                    data = a2b_base64(data)
                elif sys.platform == "win32":
                    data = data.replace("\n", "\r\n").encode("UTF-8")
                else:
                    data = data.encode("UTF-8")

                filename = self.output_filename_template.format(
                    cell_index=cell_index,
                    name=name,
                )
                link = os.path.join(self.subdirectory, filename)

                if output_files_dir is not None:
                    filename = os.path.join(self.path, filename)

                if name.endswith(".gif") and mime == "image/png":
                    filename = filename.replace(".gif", ".png")

                # Write the attachments to a file and add a link

                with open(filename, "wb") as f:
                    f.write(data)

                if "image" in mime:
                    cell.source += f'\n<a href="{link}"><img src="{link}"></a>\n'
                else:
                    cell.source += f'\n<a href="{link}">{name}</a>\n'
                if not is_diagram(cell):
                    to_delete.append(name)

                # now we need to change the cell source so that it links to the
                # filename instead of `attachment:`
                attach_str = "attachment:" + name
                if attach_str in cell.source:
                    cell.source = cell.source.replace(attach_str, filename)

        for name in to_delete:
            del cell.attachments[name]

        return cell, resources
