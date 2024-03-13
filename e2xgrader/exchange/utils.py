from textwrap import dedent

import nbformat
from nbconvert.exporters import HTMLExporter


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


def generate_submission_html(
    notebook_file: str,
    html_file: str,
    hashcode: str,
    timestamp: str,
    exporter: HTMLExporter,
) -> None:
    """
    Generate a submission HTML file from the given notebook file.
    This includes the hashcode and timestamp.

    Args:
        notebook_file (str): The path to the notebook file.
        html_file (str): The path to save the generated HTML file.
        hashcode (str): The hashcode to include in the generated HTML file.
        timestamp (str): The timestamp to include in the generated HTML file.
        exporter (HTMLExporter): The exporter to use for generating the HTML file.

    Returns:
        None
    """
    html, _ = exporter.from_notebook_node(
        nbformat.read(notebook_file, as_version=nbformat.NO_CONVERT),
        resources={"hashcode": hashcode, "timestamp": timestamp},
    )
    with open(html_file, "w") as f:
        f.write(html)
