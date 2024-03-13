import os
import unittest
from tempfile import TemporaryDirectory

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

from e2xgrader.exchange.utils import (
    generate_student_info_file,
    generate_submission_html,
)
from e2xgrader.exporters import SubmissionExporter


class TestGenerateStudentInfoFile(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.directory = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generate_student_info_file(self):
        generate_student_info_file(
            os.path.join(self.directory, "student_info.txt"),
            "testuser",
            "123456",
            "2022-01-01 00:00:00",
        )
        with open(os.path.join(self.directory, "student_info.txt"), "r") as f:
            content = f.read()

        self.assertIn("Username: testuser", content)
        self.assertIn("Hashcode: 123456", content)
        self.assertIn("Timestamp: 2022-01-01 00:00:00", content)


class TestGenerateSubmissionHtml(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.directory = self.temp_dir.name
        nb = new_notebook(
            cells=[
                new_markdown_cell("This is a markdown cell"),
            ]
        )
        nbformat.write(nb, os.path.join(self.directory, "notebook.ipynb"))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generate_submission_html(self):
        exporter = SubmissionExporter()

        generate_submission_html(
            os.path.join(self.directory, "notebook.ipynb"),
            os.path.join(self.directory, "submission.html"),
            "123456",
            "2022-01-01 00:00:00",
            exporter,
        )
        with open(os.path.join(self.directory, "submission.html"), "r") as f:
            content = f.read()

        self.assertIn("This is a markdown cell", content)
        self.assertIn("2022-01-01 00:00:00", content)
        self.assertIn(exporter.exam_submitted_message, content)
        self.assertIn(exporter.your_hashcode_message, content)
        self.assertIn(exporter.verify_exam_message, content)

    def test_generate_submission_html_with_custom_messages(self):
        exporter = SubmissionExporter()
        msg1 = "Custom exam submitted message"
        msg2 = "Custom hashcode message"
        msg3 = "Custom verify exam message"
        exporter.exam_submitted_message = msg1
        exporter.your_hashcode_message = msg2
        exporter.verify_exam_message = msg3

        generate_submission_html(
            os.path.join(self.directory, "notebook.ipynb"),
            os.path.join(self.directory, "submission1.html"),
            "123456",
            "2022-01-01 00:00:00",
            exporter,
        )
        with open(os.path.join(self.directory, "submission1.html"), "r") as f:
            content = f.read()

        self.assertIn(msg1, content)
        self.assertIn(msg2, content)
        self.assertIn(msg3, content)
