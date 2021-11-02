#!/usr/bin/env python
# coding: utf-8

from nbgrader.apps.nbgraderapp import NbGraderApp
from .autogradeapp import E2xAutogradeApp
from .generatefeedbackapp import E2xGenerateFeedbackApp
from textwrap import dedent


class E2xNbGraderApp(NbGraderApp):

    subcommands = NbGraderApp.subcommands.copy()
    subcommands["autograde"] = (
        E2xAutogradeApp,
        dedent(
            """
                Autograde submitted assignments. Intended for use by instructors
                only.
                """
        ).strip(),
    )
    subcommands["generate_feedback"] = (
        E2xGenerateFeedbackApp,
        dedent(
            """
                Generate feedback (after autograding and manual grading).
                Intended for use by instructors only.
                """
        ).strip(),
    )


def main():
    E2xNbGraderApp.launch_instance()
