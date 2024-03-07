import sys
import unittest
from io import StringIO

from jupyter_core.application import NoStart

from e2xgrader.apps.showmodeapp import ShowModeApp


class TestShowModeApp(unittest.TestCase):

    def setUp(self):
        self.app = ShowModeApp()
        self.app.initialize([])
        self.caputered_stdout = StringIO()
        sys.stdout = self.caputered_stdout

    def test_show_mode(self):
        # Make sure stdout contains the mode
        try:
            self.app.start()
        except NoStart:
            pass
        finally:
            self.assertIn(self.app.mode, self.caputered_stdout.getvalue())

    def tearDown(self):
        sys.stdout = sys.__stdout__
        self.caputered_stdout.close()
