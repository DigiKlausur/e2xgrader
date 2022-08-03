"""
A system for creating assignments.
"""

import glob
import os
from os.path import join as pjoin


def _jupyter_nbextension_paths():
    root = os.path.dirname(__file__)
    base_path = pjoin(root, "nbextensions")
    notebook_path = pjoin(base_path, "notebook")
    tree_path = pjoin(base_path, "tree")

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
        dict(module="e2xgrader.server_extensions.assignment_list"),
        dict(module="e2xgrader.server_extensions.grader"),
    ]

    return paths
