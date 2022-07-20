"""
A system for creating assignments.
"""

import os
from os.path import join as pjoin


def _jupyter_nbextension_paths():
    root = os.path.dirname(__file__)
    if os.path.exists(pjoin(root, "nbextensions", "lib")):
        base_path = pjoin(root, "nbextensions", "lib")
    else:
        base_path = pjoin(root, "nbextensions", "src")

    paths = [
        dict(
            section="notebook",
            src=pjoin(base_path, "common", "extra_cells"),
            dest="extra_cells",
            require="extra_cells/main",
        ),
        dict(
            section="tree",
            src=pjoin(base_path, "teacher", "taskcreator"),
            dest="taskcreator",
            require="taskcreator/main",
        ),
        dict(
            section="tree",
            src=pjoin(base_path, "teacher", "grader"),
            dest="grader",
            require="grader/main",
        ),
        dict(
            section="notebook",
            src=pjoin(base_path, "teacher", "create_assignment"),
            dest="create_assignment",
            require="create_assignment/main",
        ),
        dict(
            section="notebook",
            src=pjoin(base_path, "teacher", "taskeditor"),
            dest="taskeditor",
            require="taskeditor/main",
        ),
        dict(
            section="notebook",
            src=pjoin(base_path, "teacher", "templatebar"),
            dest="templatebar",
            require="templatebar/main",
        ),
        dict(
            section="notebook",
            src=pjoin(base_path, "student", "assignment", "assignment_extension"),
            dest="assignment_extension",
            require="assignment_extension/main",
        ),
        dict(
            section="notebook",
            src=pjoin(base_path, "student", "exam", "exam_view"),
            dest="exam_view",
            require="exam_view/main",
        ),
        dict(
            section="tree",
            src=pjoin(base_path, "student", "exam", "restricted_tree"),
            dest="restricted_tree",
            require="restricted_tree/main",
        ),
    ]

    return paths


def _jupyter_server_extension_paths():
    paths = [
        dict(module="e2xgrader.server_extensions.formgrader"),
        dict(module="e2xgrader.server_extensions.assignment_list"),
        dict(module="e2xgrader.server_extensions.e2xbase"),
        dict(module="e2xgrader.server_extensions.grader"),
    ]

    return paths
