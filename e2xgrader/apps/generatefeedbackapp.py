#!/usr/bin/env python
# coding: utf-8

from nbgrader.apps import GenerateFeedbackApp
from nbgrader.apps.generatefeedbackapp import aliases, flags

flags.update({
    'hidecells': (
        {'FilterTests': {'hide_cells': True}},
        "Hide test cells in the feedback generated for students."
    ),
})


class E2xGenerateFeedbackApp(GenerateFeedbackApp):
    aliases = aliases
    flags = flags