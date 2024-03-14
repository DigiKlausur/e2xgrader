import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook
from nbgrader.auth import Authenticator
from nbgrader.coursedir import CourseDirectory
from nbgrader.exchange.abc.exchange import ExchangeError
from nbgrader.utils import get_username

from e2xgrader.exchange.submit import E2xExchangeSubmit
from e2xgrader.utils.mode import E2xGraderMode


class DummyAuthenticator(Authenticator):

    def __init__(self, has_access=True):
        self._has_access = has_access

    def has_access(self, student_id, course_id):
        return self._has_access


class TestE2xExchangeSubmit(unittest.TestCase):

    def setUp(self):

        self.temp_dirs = dict(
            assignment_dir=TemporaryDirectory(),
            course_dir=TemporaryDirectory(),
            exchange_dir=TemporaryDirectory(),
            cache_dir=TemporaryDirectory(),
        )

        self.submit = E2xExchangeSubmit()
        self.submit.authenticator = DummyAuthenticator()
        self.submit.set_timestamp()

        self.submit.assignment_dir = self.temp_dirs["assignment_dir"].name
        self.submit.cache = self.temp_dirs["cache_dir"].name
        self.submit.root = self.temp_dirs["exchange_dir"].name
        self.submit.coursedir = CourseDirectory()
        self.submit.coursedir.root = self.temp_dirs["course_dir"].name
        self.submit.coursedir.course_id = "testcourse"
        self.submit.coursedir.student_id = get_username()
        self.submit.coursedir.assignment_id = "assignment1"

    def create_dummy_assignment(self):
        os.makedirs(
            os.path.join(
                self.submit.assignment_dir, self.submit.coursedir.assignment_id
            )
        )
        os.makedirs(
            os.path.join(
                self.submit.assignment_dir,
                self.submit.coursedir.assignment_id,
                ".ipynb_checkpoints",
            )
        )
        nb = new_notebook(cells=[new_markdown_cell("test")])
        nbformat.write(
            nb,
            os.path.join(
                self.submit.assignment_dir,
                self.submit.coursedir.assignment_id,
                "test.ipynb",
            ),
        )
        nbformat.write(
            nb,
            os.path.join(
                self.submit.assignment_dir,
                self.submit.coursedir.assignment_id,
                ".ipynb_checkpoints",
                "test2.ipynb",
            ),
        )
        with open(
            os.path.join(
                self.submit.assignment_dir,
                self.submit.coursedir.assignment_id,
                "test.txt",
            ),
            "w",
        ) as f:
            f.write("test")

    def tearDown(self):
        for temp_dir in self.temp_dirs.values():
            temp_dir.cleanup()

    def test_init_dest_without_personalized_inbound(self):
        os.makedirs(os.path.join(self.submit.root, "testcourse", "inbound"))
        self.submit.init_dest()

        expected_inbound_path = os.path.join(self.submit.root, "testcourse", "inbound")
        self.assertEqual(self.submit.inbound_path, expected_inbound_path)

    def test_init_dest_with_personalized_inbound(self):
        self.submit.personalized_inbound = True
        self.submit.init_dest()

        expected_inbound_path = os.path.join(
            self.submit.root, "testcourse", "inbound", get_username()
        )
        self.assertEqual(self.submit.inbound_path, expected_inbound_path)

    def test_init_dest_without_existing_inbound(self):
        with self.assertRaises(ExchangeError):
            self.submit.init_dest()

    def test_init_dest_without_course_id(self):
        self.submit.coursedir.course_id = ""
        with self.assertRaises(ExchangeError):
            self.submit.init_dest()

    def test_init_dest_without_access(self):
        self.submit.authenticator = DummyAuthenticator(False)
        with self.assertRaises(ExchangeError):
            self.submit.init_dest()

    def test_init_release_returns_error_if_no_release_dir(self):
        with self.assertRaises(ExchangeError):
            self.submit.init_release()

    def test_init_release_returns_error_if_no_course_id(self):
        self.submit.coursedir.course_id = ""
        with self.assertRaises(ExchangeError):
            self.submit.init_release()

    def test_init_release_without_personalized_outbound(self):
        os.makedirs(
            os.path.join(self.submit.root, "testcourse", "outbound", "assignment1")
        )
        self.submit.init_release()

        expected_release_path = os.path.join(
            self.submit.root, "testcourse", "outbound", "assignment1"
        )
        self.assertEqual(self.submit.release_path, expected_release_path)

    def test_init_release_with_personalized_outbound(self):
        self.submit.personalized_outbound = True
        expected_release_path = os.path.join(
            self.submit.root, "testcourse", "outbound", get_username(), "assignment1"
        )
        os.makedirs(expected_release_path)
        self.submit.init_release()

        self.assertEqual(self.submit.release_path, expected_release_path)

    def test_set_assignment_filename_without_student_id(self):
        self.submit.coursedir.student_id = "*"
        self.submit.set_assignment_filename()
        self.assertIn("assignment1", self.submit.assignment_filename)
        self.assertIn(get_username(), self.submit.assignment_filename)
        self.assertIn(self.submit.timestamp, self.submit.assignment_filename)

    def test_set_assignment_filename_with_student_id(self):
        self.submit.coursedir.student_id = "student1"
        self.submit.set_assignment_filename()
        self.assertIn("assignment1", self.submit.assignment_filename)
        self.assertIn("student1", self.submit.assignment_filename)
        self.assertIn(self.submit.timestamp, self.submit.assignment_filename)

    def test_set_assignment_filename_with_invalid_student_id(self):
        self.submit.coursedir.student_id = "student1*"
        with self.assertRaises(ExchangeError):
            self.submit.set_assignment_filename()

    def test_set_assignment_filename_without_random_string(self):
        self.submit.add_random_string = False
        self.submit.set_assignment_filename()
        self.assertEqual(
            self.submit.assignment_filename,
            f"{get_username()}+assignment1+{self.submit.timestamp}",
        )

    def test_submit_with_student_exam_mode_calls_create_exam_files(self):
        self.create_dummy_assignment()
        os.makedirs(
            os.path.join(
                self.submit.root,
                self.submit.coursedir.course_id,
                self.submit.inbound_directory,
            )
        )
        os.makedirs(
            os.path.join(
                self.submit.root,
                self.submit.coursedir.course_id,
                self.submit.outbound_directory,
                self.submit.coursedir.assignment_id,
            )
        )

        with patch(
            "e2xgrader.exchange.submit.infer_e2xgrader_mode"
        ) as mock_infer, patch.object(
            self.submit, "create_exam_files"
        ) as mock_create_exam_files:
            mock_infer.return_value = E2xGraderMode.STUDENT_EXAM.value
            self.submit.start()
            mock_create_exam_files.assert_called_once()

    def test_submit_with_student_assignment_mode_does_not_call_create_exam_files(self):
        self.create_dummy_assignment()
        os.makedirs(
            os.path.join(
                self.submit.root,
                self.submit.coursedir.course_id,
                self.submit.inbound_directory,
            )
        )
        os.makedirs(
            os.path.join(
                self.submit.root,
                self.submit.coursedir.course_id,
                self.submit.outbound_directory,
                self.submit.coursedir.assignment_id,
            )
        )

        with patch(
            "e2xgrader.exchange.submit.infer_e2xgrader_mode"
        ) as mock_infer, patch.object(
            self.submit, "create_exam_files"
        ) as mock_create_exam_files:
            mock_infer.return_value = E2xGraderMode.STUDENT.value
            self.submit.start()
            mock_create_exam_files.assert_not_called()

    def test_submit_with_student_exam_mode_creates_exam_files(self):
        self.create_dummy_assignment()
        self.submit.add_random_string = False
        inbound_path = os.path.join(
            self.submit.root,
            self.submit.coursedir.course_id,
            self.submit.inbound_directory,
        )
        outbound_path = os.path.join(
            self.submit.root,
            self.submit.coursedir.course_id,
            self.submit.outbound_directory,
            self.submit.coursedir.assignment_id,
        )
        os.makedirs(inbound_path)
        os.makedirs(outbound_path)

        with patch("e2xgrader.exchange.submit.infer_e2xgrader_mode") as mock_infer:
            mock_infer.return_value = E2xGraderMode.STUDENT_EXAM.value
            self.submit.start()

            inbound_path = os.path.join(
                self.submit.inbound_path, self.submit.assignment_filename
            )
            cache_path = os.path.join(
                self.submit.cache_path, self.submit.assignment_filename
            )

            for assignment_path in [inbound_path, cache_path]:
                assert os.path.exists(assignment_path)

                assert os.path.isfile(os.path.join(assignment_path, "SHA1SUM.txt"))
                assert os.path.isfile(os.path.join(assignment_path, "test.ipynb"))
                assert os.path.isfile(
                    os.path.join(assignment_path, "test_hashcode.html")
                )
                assert os.path.isfile(os.path.join(assignment_path, "test.txt"))
                assert os.path.isfile(
                    os.path.join(assignment_path, f"{get_username()}_info.txt")
                )

                # Make sure the files are in the hashcode file
                with open(os.path.join(assignment_path, "SHA1SUM.txt"), "r") as f:
                    content = f.read()
                    self.assertIn("test.ipynb", content)
                    self.assertIn("test.txt", content)
                    self.assertNotIn("test_hashcode.html", content)
                    self.assertNotIn(f"{get_username()}_info.txt", content)
                    self.assertNotIn("SHA1SUM.txt", content)
                    self.assertNotIn(".ipynb_checkpoints", content)

    def test_start_fails_with_win32(self):
        with patch("e2xgrader.exchange.submit.sys.platform", "win32"):
            with self.assertRaises(ExchangeError):
                self.submit.start()
