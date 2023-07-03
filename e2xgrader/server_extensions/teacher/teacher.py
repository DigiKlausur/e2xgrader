from traitlets import Any, List

from ..apps.assignment_list import AssignmentList
from ..apps.authoring import AuthoringApp
from ..apps.e2xgraderapi import E2xGraderApi
from ..apps.formgrader import FormgradeApp
from ..apps.help import Help
from ..apps.nbgraderapi import NbGraderApi
from ..apps.validate_assignment import ValidateAssignment
from ..base import BaseExtension


class TeacherExtension(BaseExtension):
    apps = List(
        trait=Any(),
        default_value=[
            E2xGraderApi,
            NbGraderApi,
            FormgradeApp,
            AuthoringApp,
            ValidateAssignment,
            AssignmentList,
            Help,
        ],
    ).tag(config=True)


def load_jupyter_server_extension(nbapp):
    """Load the e2xgrader serverextension"""
    nbapp.log.info("Loading the e2xgrader teacher serverextension")
    TeacherExtension(parent=nbapp)
