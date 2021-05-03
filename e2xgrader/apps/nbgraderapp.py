#!/usr/bin/env python
# coding: utf-8

from nbgrader.apps.nbgraderapp import NbGraderApp
from .autogradeapp import E2XAutogradeApp
from textwrap import dedent

class E2XNbGraderApp(NbGraderApp):

    subcommands = NbGraderApp.subcommands.copy()
    subcommands['autograde'] = (
            E2XAutogradeApp,
            dedent(
                """
                Autograde submitted assignments. Intended for use by instructors
                only.
                """
            ).strip())

def main():
    E2XNbGraderApp.launch_instance()