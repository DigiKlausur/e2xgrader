"""
A system for creating assignments.
"""

import os
import sys

def _jupyter_server_extension_paths():
    paths = [
        dict(module="e2xgrader.server_extensions.formgrader")
    ]

    return paths