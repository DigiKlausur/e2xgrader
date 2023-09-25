from traitlets import Any, List

from ..apps.assignment_list import AssignmentList
from ..apps.diagram_editor import DiagramEditor
from ..apps.help import Help
from ..apps.validate_assignment import ValidateAssignment
from ..base import BaseExtension


class StudentExtension(BaseExtension):
    apps = List(
        trait=Any(),
        default_value=[AssignmentList, ValidateAssignment, Help, DiagramEditor],
    ).tag(config=True)


def load_jupyter_server_extension(nbapp):
    """Load the e2xgrader serverextension"""
    nbapp.log.info("Loading the e2xgrader student serverextension")
    StudentExtension(parent=nbapp)
