from typing import Any, Dict, Union

from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_code_cell, new_markdown_cell


def nbgrader_metadata(**kwargs) -> Dict[str, Union[int, str, bool]]:
    """Create an nbgrader metadata dictionary
    Updates the metadata with any keyword arguments provided

    Returns:
        Dict[str, Union[int, str, bool]]: metadata
    """
    metadata = {
        "grade": False,
        "grade_id": "cell1",
        "locked": False,
        "schema_version": 3,
        "solution": False,
        "task": False,
    }
    metadata.update(kwargs)
    return metadata


def extra_cell_metadata(
    type: str, options: Dict[str, Any] = None, **kwargs
) -> Dict[str, Any]:
    """Create an extra cell metadata dictionary
    Updates the metadata with any keyword arguments provided

    Args:
        type (str): the type of the extra cell
        options (Dict[str, Any], optional): An options dictionary. Defaults to None.

    Returns:
        Dict[str, Any]: metadata
    """
    metadata = dict(type=type, options=options if options is not None else dict())
    metadata.update(kwargs)
    return metadata


def new_autograder_test_cell(
    source: str = "", points: int = 0, grade_id: str = "test_cell"
) -> NotebookNode:
    return new_code_cell(
        source=source,
        metadata=dict(
            nbgrader=nbgrader_metadata(grade=True, points=points, grade_id=grade_id)
        ),
    )


def new_manually_graded_code_cell(
    source: str = "", grade_id: str = "autograded_answer"
) -> NotebookNode:
    return new_code_cell(
        source=source,
        metadata=dict(
            nbgrader=nbgrader_metadata(grade=True, solution=True, grade_id=grade_id)
        ),
    )


def new_autograded_code_cell(
    source: str = "", points: int = 0, grade_id: str = "manual_answer"
) -> NotebookNode:
    return new_code_cell(
        source=source,
        metadata=dict(
            nbgrader=nbgrader_metadata(
                grade=False, solution=True, points=points, grade_id=grade_id
            )
        ),
    )


def new_manually_graded_markdown_cell(
    source: str = "", points: int = 0, grade_id: str = "manual_text_answer"
) -> NotebookNode:
    return new_markdown_cell(
        source=source,
        metadata=dict(
            nbgrader=nbgrader_metadata(
                grade=True, solution=True, points=points, grade_id=grade_id
            )
        ),
    )


def new_readonly_code_cell(
    source: str = "", grade_id: str = "code_example"
) -> NotebookNode:
    return new_code_cell(
        source=source,
        metadata=dict(nbgrader=nbgrader_metadata(locked=True, grade_id=grade_id)),
    )


def new_readonly_markdown_cell(
    source: str = "", grade_id: str = "description"
) -> NotebookNode:
    return new_markdown_cell(
        source=source,
        metadata=dict(nbgrader=nbgrader_metadata(locked=True, grade_id=grade_id)),
    )


def new_singlechoice_cell(
    source: str = "", points: int = 0, grade_id: str = "singlechoice", **kwargs
) -> NotebookNode:
    cell = new_manually_graded_markdown_cell(
        source=source, grade_id=grade_id, points=points
    )
    cell.metadata["extended_cell"] = extra_cell_metadata(type="singlechoice", **kwargs)
    return cell


def new_multiplechoice_cell(
    source: str = "", points: int = 0, grade_id: str = "multiplechoice", **kwargs
) -> NotebookNode:
    cell = new_manually_graded_markdown_cell(
        source=source, grade_id=grade_id, points=points
    )
    cell.metadata["extended_cell"] = extra_cell_metadata(
        type="multiplechoice", **kwargs
    )
    return cell


def new_diagram_cell(
    source: str = "",
    points: int = 0,
    grade_id: str = "diagram",
    diagram: str = None,
    **kwargs,
):
    attachments = dict()
    if diagram is not None:
        attachments = {"diagram.png": {"image/png": diagram}}
    return new_markdown_cell(
        source=source,
        attachments=attachments,
        metadata=dict(
            nbgrader=nbgrader_metadata(
                grade=True, solution=True, points=points, grade_id=grade_id
            ),
            extended_cell=extra_cell_metadata(type="diagram", **kwargs),
        ),
    )


def new_upload_cell(
    source: str = "",
    points: int = 0,
    grade_id: str = "attachments",
    attachments: Dict[str, Dict[str, str]] = None,
    **kwargs,
):
    return new_markdown_cell(
        source=source,
        attachments=attachments if attachments is not None else dict(),
        metadata=dict(
            nbgrader=nbgrader_metadata(
                grade=True, solution=True, points=points, grade_id=grade_id
            ),
            extended_cell=extra_cell_metadata(type="attachments", **kwargs),
        ),
    )
