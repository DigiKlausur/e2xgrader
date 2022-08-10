import hashlib
from textwrap import dedent

import nbformat

from e2xgrader.exporters import E2xExporter


def has_name(cell, name):
    if cell.cell_type != "markdown":
        return False
    return "name" in cell.metadata and cell.metadata.name == name


def append_alert_cell(nb, text, msg, cell_id):
    alert_cell = nbformat.v4.new_markdown_cell()
    alert_cell.source = dedent(
        f"""
        <div class="alert alert-block alert-danger">
            {msg}:
            <h1>{text}</h1>
        </div>
    """
    )
    alert_cell.metadata = {"name": cell_id, "editable": False, "deletable": False}

    # When using notebooks with version <= 4.4 and nbformat v4.5
    # delete the new id attribute to prevent validation errors
    if nb.nbformat == 4 and nb.nbformat_minor <= 4 and "id" in alert_cell:
        del alert_cell["id"]

    target_idx = -1
    for idx, cell in enumerate(nb.cells):
        if has_name(cell, cell_id):
            target_idx = idx
            break

    if target_idx != -1:
        nb.cells[target_idx] = alert_cell
    else:
        nb.cells.append(alert_cell)

    return nb


def append_hashcode(nb, hashcode, msg="Ihr Hashcode"):
    return append_alert_cell(nb, hashcode, msg, "hashcode_cell")


def append_timestamp(nb, timestamp, msg="Timestamp"):
    return append_alert_cell(nb, timestamp, msg, "timestamp_cell")


def compute_hashcode(filename, method="md5"):
    if method == "md5":
        hashcode = hashlib.md5()
    elif method == "sha1":
        hashcode = hashlib.sha1()
    else:
        raise ValueError("Currently only the methods md5 and sha1 are supported!")

    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashcode.update(chunk)

    return hashcode.hexdigest()


def truncate_hashcode(hashcode, size=20, chunk_size=5):
    hash_string = ""
    for i in range(0, size, chunk_size):
        hash_string += f"-{hashcode[i:i+chunk_size+1]}"
    return hash_string[1:]


def generate_student_info(filename, username, hashcode, timestamp):
    with open(filename, "w") as f:
        f.write(
            dedent(
                f"""
            Username: {username}
            Hashcode: {hashcode}
            Timestamp: {timestamp}
        """
            )
        )


def generate_html(nb, dest):
    exporter = E2xExporter()
    exporter.template_name = "form"
    html, _ = exporter.from_notebook_node(nb)

    with open(dest, "w") as f:
        f.write(html)
