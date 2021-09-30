#!/usr/bin/env python
# coding: utf-8

from nbgrader.apps import GenerateFeedbackApp
from nbgrader.apps.generatefeedbackapp import aliases, flags

aliases['hidecell'] = 'Generate.hidecell'

class E2xGenerateFeedbackApp(GenerateFeedbackApp):
    aliases = aliases
    flags = flags
