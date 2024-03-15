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

from .utils import create_course_dir


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

    def get_exchange_submit(
        self,
        course_dir: CourseDirectory = None,
        personalized_feedback: bool = True,
        personalized_inbound: bool = True,
        personalized_outbound: bool = False,
    ) -> E2xExchangeSubmit:
        """
        Get an instance of E2xExchangeSubmit with the specified parameters.

        Args:
            course_dir (CourseDirectory): The course directory. Defaults to None.
                If None, a new coursedir is created.
            personalized_feedback (bool, optional):
                Flag indicating whether personalized feedback is enabled. Defaults to True.
            personalized_inbound (bool, optional):
                Flag indicating whether personalized inbound is enabled. Defaults to True.
            personalized_outbound (bool, optional):
                Flag indicating whether personalized outbound is enabled. Defaults to False.

        Returns:
            E2xExchangeSubmit: An instance of E2xExchangeSubmit.
        """
        if course_dir is None:
            course_dir = create_course_dir(self.temp_dirs["course_dir"].name)

        E2xExchangeSubmit.personalized_feedback = personalized_feedback
        E2xExchangeSubmit.personalized_inbound = personalized_inbound
        E2xExchangeSubmit.personalized_outbound = personalized_outbound
        submit = E2xExchangeSubmit()
        submit.authenticator = DummyAuthenticator()
        submit.set_timestamp()

        submit.coursedir = course_dir
        submit.assignment_dir = self.temp_dirs["assignment_dir"].name
        submit.cache = self.temp_dirs["cache_dir"].name
        submit.root = self.temp_dirs["exchange_dir"].name
        return submit

    def create_dummy_assignment(
        self, assignment_dir: str, assignment_id: str = "assignment1"
    ) -> None:
        os.makedirs(os.path.join(assignment_dir, assignment_id))
        os.makedirs(
            os.path.join(
                assignment_dir,
                assignment_id,
                ".ipynb_checkpoints",
            )
        )
        nb = new_notebook(cells=[new_markdown_cell("test")])
        nbformat.write(
            nb,
            os.path.join(
                assignment_dir,
                assignment_id,
                "test.ipynb",
            ),
        )
        nbformat.write(
            nb,
            os.path.join(
                assignment_dir,
                assignment_id,
                ".ipynb_checkpoints",
                "test2.ipynb",
            ),
        )
        with open(
            os.path.join(
                assignment_dir,
                assignment_id,
                "test.txt",
            ),
            "w",
        ) as f:
            f.write("test")

    def tearDown(self):
        for temp_dir in self.temp_dirs.values():
            temp_dir.cleanup()

    def test_init_dest_without_personalized_inbound(self):
        submit = self.get_exchange_submit(
            personalized_inbound=False,
        )
        expected_inbound_path = os.path.join(
            submit.root, submit.coursedir.course_id, submit.inbound_directory
        )
        os.makedirs(expected_inbound_path)
        submit.init_dest()

        self.assertEqual(submit.inbound_path, expected_inbound_path)

    def test_init_dest_with_personalized_inbound(self):
        submit = self.get_exchange_submit(
            personalized_inbound=True,
        )
        submit.init_dest()

        expected_inbound_path = os.path.join(
            submit.root,
            submit.coursedir.course_id,
            submit.inbound_directory,
            get_username(),
        )
        self.assertEqual(submit.inbound_path, expected_inbound_path)

    def test_init_dest_without_existing_inbound(self):
        submit = self.get_exchange_submit(
            personalized_inbound=False,
        )
        with self.assertRaises(ExchangeError):
            submit.init_dest()

    def test_init_dest_without_course_id(self):
        submit = self.get_exchange_submit(
            course_dir=create_course_dir(
                root=self.temp_dirs["course_dir"].name, course_id=""
            )
        )
        with self.assertRaises(ExchangeError):
            submit.init_dest()

    def test_init_dest_without_access(self):
        submit = self.get_exchange_submit()
        submit.authenticator = DummyAuthenticator(has_access=False)
        with self.assertRaises(ExchangeError):
            submit.init_dest()

    def test_init_release_returns_error_if_no_release_dir(self):
        submit = self.get_exchange_submit()
        with self.assertRaises(ExchangeError):
            submit.init_release()

    def test_init_release_returns_error_if_no_course_id(self):
        submit = self.get_exchange_submit(
            course_dir=create_course_dir(
                root=self.temp_dirs["course_dir"].name, course_id=""
            )
        )
        with self.assertRaises(ExchangeError):
            submit.init_release()

    def test_init_release_without_personalized_outbound(self):
        submit = self.get_exchange_submit(
            personalized_outbound=False,
        )

        expected_release_path = os.path.join(
            submit.root,
            submit.coursedir.course_id,
            submit.outbound_directory,
            submit.coursedir.assignment_id,
        )
        os.makedirs(expected_release_path)
        submit.init_release()
        self.assertEqual(submit.release_path, expected_release_path)

    def test_init_release_with_personalized_outbound(self):
        submit = self.get_exchange_submit(
            personalized_outbound=True,
        )

        expected_release_path = os.path.join(
            submit.root,
            submit.coursedir.course_id,
            submit.outbound_directory,
            get_username(),
            submit.coursedir.assignment_id,
        )
        os.makedirs(expected_release_path)
        submit.init_release()

        self.assertEqual(submit.release_path, expected_release_path)

    def test_set_assignment_filename_without_student_id(self):
        submit = self.get_exchange_submit(
            course_dir=create_course_dir(
                root=self.temp_dirs["course_dir"].name, student_id="*"
            )
        )

        submit.set_assignment_filename()
        self.assertIn(submit.coursedir.assignment_id, submit.assignment_filename)
        self.assertIn(get_username(), submit.assignment_filename)
        self.assertIn(submit.timestamp, submit.assignment_filename)

    def test_set_assignment_filename_with_student_id(self):
        submit = self.get_exchange_submit(
            course_dir=create_course_dir(
                root=self.temp_dirs["course_dir"].name, student_id="student1"
            )
        )
        submit.set_assignment_filename()
        self.assertIn(submit.coursedir.assignment_id, submit.assignment_filename)
        self.assertIn("student1", submit.assignment_filename)
        self.assertIn(submit.timestamp, submit.assignment_filename)

    def test_set_assignment_filename_with_invalid_student_id(self):
        submit = self.get_exchange_submit(
            course_dir=create_course_dir(
                root=self.temp_dirs["course_dir"].name, student_id="student1*"
            )
        )

        with self.assertRaises(ExchangeError):
            submit.set_assignment_filename()

    def test_set_assignment_filename_without_random_string(self):
        submit = self.get_exchange_submit()
        submit.add_random_string = False
        submit.set_assignment_filename()
        self.assertEqual(
            submit.assignment_filename,
            f"{get_username()}+{submit.coursedir.assignment_id}+{submit.timestamp}",
        )

    def test_submit_with_student_exam_mode_calls_create_exam_files(self):
        self.create_dummy_assignment(self.temp_dirs["assignment_dir"].name)
        submit = self.get_exchange_submit()
        os.makedirs(
            os.path.join(
                submit.root,
                submit.coursedir.course_id,
                submit.inbound_directory,
            )
        )
        os.makedirs(
            os.path.join(
                submit.root,
                submit.coursedir.course_id,
                submit.outbound_directory,
                submit.coursedir.assignment_id,
            )
        )

        with patch(
            "e2xgrader.exchange.submit.infer_e2xgrader_mode"
        ) as mock_infer, patch.object(
            submit, "create_exam_files"
        ) as mock_create_exam_files:
            mock_infer.return_value = E2xGraderMode.STUDENT_EXAM.value
            submit.start()
            mock_create_exam_files.assert_called_once()

    def test_submit_with_student_assignment_mode_does_not_call_create_exam_files(self):
        self.create_dummy_assignment(self.temp_dirs["assignment_dir"].name)
        submit = self.get_exchange_submit()
        os.makedirs(
            os.path.join(
                submit.root,
                submit.coursedir.course_id,
                submit.inbound_directory,
            )
        )
        os.makedirs(
            os.path.join(
                submit.root,
                submit.coursedir.course_id,
                submit.outbound_directory,
                submit.coursedir.assignment_id,
            )
        )

        with patch(
            "e2xgrader.exchange.submit.infer_e2xgrader_mode"
        ) as mock_infer, patch.object(
            submit, "create_exam_files"
        ) as mock_create_exam_files:
            mock_infer.return_value = E2xGraderMode.STUDENT.value
            submit.start()
            mock_create_exam_files.assert_not_called()

    def test_submit_with_student_exam_mode_creates_exam_files(self):
        self.create_dummy_assignment(self.temp_dirs["assignment_dir"].name)
        submit = self.get_exchange_submit()
        submit.add_random_string = False
        inbound_path = os.path.join(
            submit.root,
            submit.coursedir.course_id,
            submit.inbound_directory,
        )
        outbound_path = os.path.join(
            submit.root,
            submit.coursedir.course_id,
            submit.outbound_directory,
            submit.coursedir.assignment_id,
        )
        os.makedirs(inbound_path)
        os.makedirs(outbound_path)

        with patch("e2xgrader.exchange.submit.infer_e2xgrader_mode") as mock_infer:
            mock_infer.return_value = E2xGraderMode.STUDENT_EXAM.value
            submit.start()

            inbound_path = os.path.join(submit.inbound_path, submit.assignment_filename)
            cache_path = os.path.join(submit.cache_path, submit.assignment_filename)

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
        submit = self.get_exchange_submit()
        with patch("e2xgrader.exchange.submit.sys.platform", "win32"):
            with self.assertRaises(ExchangeError):
                submit.start()
