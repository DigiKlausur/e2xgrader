"""
A system for creating assignments.
"""

import os
import sys

def _jupyter_nbextension_paths():
    paths = [
        dict(
            section='notebook',
            src=os.path.join('nbextensions', 'create_assignment'),
            dest='create_assignment',
            require='create_assignment/main'
        ),
        dict(
            section='notebook',
            src=os.path.join('nbextensions', 'extra_cells'),
            dest='extra_cells',
            require='extra_cells/main'
        ),
    ]
    
    return paths

def _jupyter_server_extension_paths():
    paths = [
        dict(module="e2xgrader.server_extensions.formgrader")
    ]

    return paths