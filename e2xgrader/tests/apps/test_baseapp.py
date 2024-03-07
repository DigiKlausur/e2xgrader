import unittest
from unittest.mock import patch

from traitlets import TraitError

from e2xgrader.apps.baseapp import E2xGrader
from e2xgrader.utils.mode import E2xGraderMode


class TestE2xGrader(unittest.TestCase):

    def setUp(self):
        self.app = E2xGrader()
        self.app.initialize([])

    def test_set_invalid_mode(self):
        with self.assertRaises(TraitError):
            self.app.mode = "mode_that_does_not_exist"

    def test_non_matching_mode_causes_log_error(self):
        with patch(
            "e2xgrader.apps.baseapp.infer_e2xgrader_mode"
        ) as mock_infer_e2xgrader_mode:
            mock_infer_e2xgrader_mode.side_effect = ValueError("error")
            with patch("e2xgrader.apps.baseapp.E2xGrader.log") as mock_log:
                self.app.initialize([])
                mock_log.error.assert_called_once_with("error")
                self.assertEqual(self.app.mode, E2xGraderMode.INVALID.value)
