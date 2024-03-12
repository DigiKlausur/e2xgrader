from textwrap import dedent

import nbformat

from e2xgrader.exporters import E2xExporter


def create_hashcode_table(hashcode: str) -> str:
    """
    Creates an HTML table representation of a hashcode.

    Args:
        hashcode (str): The hashcode to be represented.

    Returns:
        str: The HTML table representation of the hashcode.
    """

    def td(char):
        return dedent(
            f"""
            <td
             style='border: 1px solid #999;min-width:1.8em;text-align:center;'
            >{char}</td>
            """
        ).replace("\n", " ")

    dash = "<td style='font-weight: bold;color: #999;background: #dff0d8;'>-</td>"

    cells = dash.join(
        ["".join([td(char) for char in chars]) for chars in hashcode.split("-")]
    )
    return f"<table><tr style='font-size:1.5em;'>{cells}</tr></table>"


def generate_submit_message_html(hashcode: str, timestamp: str) -> str:
    """
    Generate HTML message for successful exam submission.

    Args:
        hashcode (str): The hashcode of the exam.
        timestamp (str): The timestamp of the submission.

    Returns:
        str: The HTML message for successful exam submission.
    """

    def text(msg, font_size):
        return dedent(
            f"""
        <div
         style='font-size:{font_size}em;font-weight:bold;margin: 1em 0;'
        >{msg}</div>"""
        ).replace("\n", " ")

    return dedent(
        f"""
        <div class='alert alert-block alert-success' style='text-align:center;'>
          <div style='text-align:right;'>{timestamp}</div>
          {text('We have received your exam!', 1.75)}
          {text('Your hashcode:', 1.25)}
          {create_hashcode_table(hashcode.upper())}
          {text(
            'Verify your exam below and then close the browser and shut down your computer.', 
            1.25
           )}
        </div>
        """
    )


def append_exam_submitted_cell(
    nb: nbformat.NotebookNode, timestamp: str, hashcode: str, cell_id: str
) -> nbformat.NotebookNode:
    """
    Appends a cell to the notebook indicating that the exam has been submitted.

    Args:
        nb (nbformat.NotebookNode): The notebook to append the cell to.
        timestamp (str): The timestamp to display in the cell.
        hashcode (str): The hashcode to display in the cell.
        cell_id (str): The id to assign to the cell.

    Returns:
        nbformat.NotebookNode: The modified notebook.
    """
    alert_cell = nbformat.v4.new_markdown_cell()
    alert_cell.source = dedent(generate_submit_message_html(hashcode, timestamp))
    alert_cell.metadata = {"name": cell_id, "editable": False, "deletable": False}

    # When using notebooks with version <= 4.4 and nbformat v4.5
    # delete the new id attribute to prevent validation errors
    if nb.nbformat == 4 and nb.nbformat_minor <= 4 and "id" in alert_cell:
        del alert_cell["id"]

    nb.cells = [alert_cell] + nb.cells

    return nb


def generate_student_info_file(
    filename: str, username: str, hashcode: str, timestamp: str
) -> None:
    """
    Generate a student info file with the given username, hashcode, and timestamp.

    Args:
        filename (str): The name of the file to be generated.
        username (str): The username of the student.
        hashcode (str): The hashcode associated with the student.
        timestamp (str): The timestamp of when the file is generated.

    Returns:
        None
    """
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


def generate_exam_submitted_html(
    nb: nbformat.NotebookNode, output_file: str, timestamp: str, hashcode: str
) -> None:
    """
    Generate an HTML file with the submitted exam.

    Args:
        nb (nbformat.NotebookNode): The notebook containing the submitted exam.
        output_file (str): The path to the output HTML file.
        timestamp (str): The timestamp of the submission.
        hashcode (str): The hashcode of the submission.

    Returns:
        None
    """
    exporter = E2xExporter()
    exporter.template_name = "form"
    html, _ = exporter.from_notebook_node(
        append_exam_submitted_cell(nb, timestamp, hashcode, "info")
    )

    with open(output_file, "w") as f:
        f.write(html)
