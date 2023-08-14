"""
A system for creating assignments.
"""

import glob
import os
from os.path import join as pjoin

from .server_extensions.student import (
    _load_jupyter_server_extension as load_student_extension,
)
from .server_extensions.student_exam import (
    _load_jupyter_server_extension as load_student_exam_extension,
)
from .server_extensions.teacher import (
    _load_jupyter_server_extension as load_teacher_extension,
)


def _jupyter_nbextension_paths():
    root = os.path.dirname(__file__)
    base_path = pjoin(root, "static", "nbextensions")

    paths = []

    for section in ["notebook", "tree"]:
        for notebook_extension in glob.glob(pjoin(base_path, section, "*")):
            name = f"{os.path.split(notebook_extension)[-1]}_{section}"
            paths.append(
                dict(
                    section=section,
                    src=notebook_extension,
                    dest=name,
                    require=pjoin(name, "main"),
                )
            )

    return paths


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
