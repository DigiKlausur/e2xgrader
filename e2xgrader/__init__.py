"""
A system for creating assignments.
"""

import os
import sys

def _jupyter_nbextension_paths():
    paths = [
        dict(
            section='notebook',
            src=os.path.join('nbextensions', 'common', 'extra_cells'),
            dest='extra_cells',
            require='extra_cells/main'
        ),
        dict(
            section='notebook',
            src=os.path.join('nbextensions', 'teacher', 'create_assignment'),
            dest='create_assignment',
            require='create_assignment/main'
        ),
        dict(
            section='notebook',
            src=os.path.join('nbextensions', 'student', 'assignment', 'assignment_view'),
            dest='assignment_view',
            require='assignment_view/main'
        ),
        dict(
            section='notebook',
            src=os.path.join('nbextensions', 'student', 'exam', 'exam_view'),
            dest='exam_view',
            require='exam_view/main'
        ),
        dict(
            section='tree',
            src=os.path.join('nbextensions', 'student', 'exam', 'restricted_tree'),
            dest='restricted_tree',
            require='restricted_tree/main'
        ),
    ]
    
    return paths

def _jupyter_server_extension_paths():
    paths = [
        dict(module="e2xgrader.server_extensions.formgrader"),
        dict(module="e2xgrader.server_extensions.assignment_list")
    ]

    return paths