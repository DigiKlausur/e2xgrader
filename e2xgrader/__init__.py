"""
A system for creating assignments.
"""

from .server_extensions.student import (
    _load_jupyter_server_extension as load_student_extension,
)
from .server_extensions.student_exam import (
    _load_jupyter_server_extension as load_student_exam_extension,
)
from .server_extensions.teacher import (
    _load_jupyter_server_extension as load_teacher_extension,
)

try:
    from .__version__ import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings

    warnings.warn("Importing 'e2xgrader_extensions' outside a proper installation.")
    __version__ = "dev"


def _jupyter_labextension_paths():
    return [
        {
            "src": "static/labextensions/@e2xgrader/labextension",
            "dest": "@e2xgrader/labextension",
        },
        {
            "src": "static/labextensions/@e2xgrader/cell-extension",
            "dest": "@e2xgrader/cell-extension",
        },
        {
            "src": "static/labextensions/@e2xgrader/cell-registry-extension",
            "dest": "@e2xgrader/cell-registry-extension",
        },
        {
            "src": "static/labextensions/@e2xgrader/authoring-celltoolbar-extension",
            "dest": "@e2xgrader/authoring-celltoolbar-extension",
        },
        {
            "src": "static/labextensions/@e2xgrader/help-extension",
            "dest": "@e2xgrader/help-extension",
        },
    ]


def _jupyter_server_extension_paths():
    paths = [
        dict(module="e2xgrader.server_extensions.teacher"),
        dict(module="e2xgrader.server_extensions.student"),
        dict(module="e2xgrader.server_extensions.student_exam"),
    ]

    return paths


def _jupyter_server_extension_points():
    return [dict(module="e2xgrader")]


def _load_jupyter_server_extension(app):
    load_student_extension(app)
    load_student_exam_extension(app)
    load_teacher_extension(app)
