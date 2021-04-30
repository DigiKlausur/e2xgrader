#!/usr/bin/env python
# coding: utf-8

from nbgrader.apps import AutogradeApp
from nbgrader.apps.autogradeapp import aliases, flags

aliases['cell-id'] = 'SaveAutoGrades.cell_id'

class E2XAutogradeApp(AutogradeApp):
    aliases = aliases
    flags = flags
