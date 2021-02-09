import nbgrader.utils as nbutils
from typing import Tuple, Optional
from logging import Logger
from nbformat.notebooknode import NotebookNode

def is_extra_cell(cell):
    """Returns True if the cell is a form cell."""
    if 'nbgrader' not in cell.metadata:
        return False
    return 'extended_cell' in cell.metadata


def is_attachment_cell(cell):
    return is_extra_cell(cell) and cell.metadata.extended_cell.type == 'attachments'


def is_singlechoice(cell):
    return is_extra_cell(cell) and cell.metadata.extended_cell.type == 'singlechoice'


def is_multiplechoice(cell):
    return is_extra_cell(cell) and cell.metadata.extended_cell.type == 'multiplechoice'


def get_choices(cell):
    if (is_singlechoice(cell) or is_multiplechoice(cell)):
        return [int(i) for i in cell.metadata.extended_cell.choice]
    return []


def get_num_of_choices(cell):
    if is_multiplechoice(cell):
        return cell.metadata.extended_cell.num_of_choices


def get_instructor_choices(cell):
    if (is_singlechoice(cell) or is_multiplechoice(cell)) and \
       ('source' in cell.metadata.extended_cell) and \
       ('choice' in cell.metadata.extended_cell.source):
            return [int(i) for i in cell.metadata.extended_cell.source.choice]
    return []


def clear_choices(cell):
    if is_extra_cell(cell):
        cell.metadata.extended_cell.choice = []


def has_solution(cell):
    if (is_singlechoice(cell) or is_multiplechoice(cell)):
        return 'source' in cell.metadata.extended_cell
    return False

def determine_grade(cell: NotebookNode, log: Logger = None) -> Tuple[Optional[float], float]:
    if not nbutils.is_grade(cell):
        raise ValueError('cell is not a grade cell')

    if (not is_multiplechoice(cell)) or (not is_singlechoice(cell)):
        return nbutils.determine_grade(cell, log)

    max_points = float(cell.metadata['nbgrader']['points'])

    if is_singlechoice(cell):
        # Get the choices of the student
        student_choices = get_choices(cell)
        # Get the instructor choices
        instructor_choices = get_instructor_choices(cell)

        if (len(student_choices) > 0) and (len(instructor_choices) > 0) and (student_choices[0] == instructor_choices[0]):
            return max_points, max_points
        else:
            return 0, max_points

    elif is_multiplechoice(cell):
        # Get the choices of the student
        student_choices = get_choices(cell)
        # Get the weights of the answer
        instructor_choices = get_instructor_choices(cell)
        option_points = max_points / get_num_of_choices(cell)

        points = 0
        for i in range(get_num_of_choices(cell)):
            if ((i in student_choices) and (i in instructor_choices)) or \
               ((i not in student_choices) and (i not in instructor_choices)):
                points += option_points
            else:
                points -=option_points
        return max(0, points), max_points