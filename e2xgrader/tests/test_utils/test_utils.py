import nbformat
from nbformat import NotebookNode
from nbformat.v4 import new_markdown_cell
from tempfile import TemporaryDirectory
from typing import List
from nbgrader.coursedir import CourseDirectory
from nbgrader.utils import is_grade
from textwrap import dedent

from e2xgrader.models import TemplateModel, PresetModel


def create_temp_course():
    tmp_dir = TemporaryDirectory()
    coursedir = CourseDirectory()
    coursedir.root = tmp_dir.name
    return tmp_dir, coursedir


def add_template_with_header(coursedir, name, header_source):
    templatemodel = TemplateModel(coursedir)
    presetmodel = PresetModel(coursedir)
    res = templatemodel.new(name=name)

    nb = nbformat.read(res["path"], as_version=nbformat.NO_CONVERT)
    header_cells = presetmodel.get_template_preset("Header")
    header_cells[0].source = header_source
    nb.cells = header_cells
    nbformat.write(nb, res["path"])
    return res["path"]


def add_header_to_template(coursedir, path, header_source):
    presetmodel = PresetModel(coursedir)
    nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
    header_cells = presetmodel.get_template_preset("Header")
    header_cells[0].source = header_source
    nb.cells.extend(header_cells)
    nbformat.write(nb, path)
    return path


def add_footer_to_template(coursedir, path, footer_source):
    presetmodel = PresetModel(coursedir)
    nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
    footer_cells = presetmodel.get_template_preset("Footer")
    footer_cells[0].source = footer_source
    nb.cells.extend(footer_cells)
    nbformat.write(nb, path)
    return path


def add_question_to_task(coursedir, path, question_type, grade_id=None, points=0):
    presetmodel = PresetModel(coursedir)
    nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
    cells = presetmodel.get_question_preset(question_type)
    if grade_id is not None:
        for cell in cells:
            cell.metadata.nbgrader.grade_id = cell.metadata.nbgrader.grade_id.replace(
                "task", grade_id
            )
            if is_grade(cell):
                cell.metadata.nbgrader.points = points
    nb.cells.extend(cells)
    nbformat.write(nb, path)
    return path


def create_multiplechoice_cell(
    grade_id: str,
    student_choices: List[int],
    instructor_choices: List[int],
    num_of_choices: int,
    points: int = 5,
) -> NotebookNode:
    cell = new_markdown_cell()

    cell.metadata = {
        "nbgrader": {
            "grade": True,
            "grade_id": grade_id,
            "locked": False,
            "points": points,
            "schema_version": 3,
            "solution": True,
            "task": False,
        },
        "extended_cell": {
            "type": "multiplechoice",
            "num_of_choices": num_of_choices,
            "choice": student_choices,
            "source": {"choice": instructor_choices},
        },
    }

    cell.source = dedent(
        """
        - correct answer
        - wrong answer
        - correct answer
        """
    )
    return cell


def create_singlechoice_cell(
    grade_id: str,
    student_choices: List[int],
    instructor_choices: List[int],
    points: int = 5,
) -> NotebookNode:
    cell = new_markdown_cell()

    cell.metadata = {
        "nbgrader": {
            "grade": True,
            "grade_id": grade_id,
            "locked": False,
            "points": points,
            "schema_version": 3,
            "solution": True,
            "task": False,
        },
        "extended_cell": {
            "type": "singlechoice",
            "choice": student_choices,
            "source": {"choice": instructor_choices},
        },
    }

    cell.source = dedent(
        """
        - correct answer
        - wrong answer
        """
    )
    return cell
