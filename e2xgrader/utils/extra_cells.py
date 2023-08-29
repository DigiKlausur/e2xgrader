def is_extra_cell(cell):
    """Returns True if the cell is a form cell."""
    if "nbgrader" not in cell.metadata:
        return False
    return "extended_cell" in cell.metadata


def is_attachment_cell(cell):
    return is_extra_cell(cell) and cell.metadata.extended_cell.type == "attachments"


def is_singlechoice(cell):
    return is_extra_cell(cell) and cell.metadata.extended_cell.type == "singlechoice"


def is_multiplechoice(cell):
    return is_extra_cell(cell) and cell.metadata.extended_cell.type == "multiplechoice"


def is_diagram(cell):
    return is_extra_cell(cell) and cell.metadata.extended_cell.type == "diagram"


def get_options(cell):
    if is_extra_cell(cell) and "options" in cell.metadata.extended_cell:
        return {
            key: value["value"]
            for key, value in cell.metadata.extended_cell["options"].items()
        }
    return dict()


def get_choices(cell):
    if is_singlechoice(cell) or is_multiplechoice(cell):
        choice = cell.metadata.extended_cell.get("choice", [])
        return [int(i) for i in choice]
    return []


def get_num_of_choices(cell):
    if is_multiplechoice(cell):
        return cell.metadata.extended_cell.num_of_choices


def get_instructor_choices(cell):
    if (
        (is_singlechoice(cell) or is_multiplechoice(cell))
        and ("source" in cell.metadata.extended_cell)
        and ("choice" in cell.metadata.extended_cell.source)
    ):
        return [int(i) for i in cell.metadata.extended_cell.source.choice]
    return []


def clear_choices(cell):
    if is_extra_cell(cell):
        cell.metadata.extended_cell.choice = []


def has_solution(cell):
    if is_singlechoice(cell) or is_multiplechoice(cell):
        return "source" in cell.metadata.extended_cell
    return False
