import unittest

from e2xgrader.extensions.utils import is_installed


class TestUtils(unittest.TestCase):
    def test_is_installed(self):
        self.assertTrue(is_installed("e2xgrader"), "e2xgrader should be installed")
        self.assertFalse(
            is_installed("e2xgradeeer"),
            "Non existing package e2xgradeeer should not be installed",
        )
