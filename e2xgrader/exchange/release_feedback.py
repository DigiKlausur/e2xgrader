import glob
import os
import re
import shutil
from stat import (
    S_IRGRP,
    S_IROTH,
    S_IRUSR,
    S_ISGID,
    S_IWGRP,
    S_IWOTH,
    S_IWUSR,
    S_IXGRP,
    S_IXOTH,
    S_IXUSR,
)

from nbgrader.exchange.default import ExchangeReleaseFeedback
from nbgrader.utils import make_unique_key, notebook_hash

from .exchange import E2xExchange


class E2xExchangeReleaseFeedback(E2xExchange, ExchangeReleaseFeedback):
    def init_dest(self):
        """
        Create exchange feedback destination
        """

        if self.coursedir.course_id == "":
            self.fail("No course id specified. Re-run with --course flag.")

        self.course_path = os.path.join(self.root, self.coursedir.course_id)
        self.dest_path = os.path.join(self.course_path, self.feedback_directory)

        if self.personalized_feedback:
            # u+rwx, g+wx, o+wx
            self.ensure_directory(
                self.dest_path,
                (
                    S_IRUSR
                    | S_IWUSR
                    | S_IXUSR
                    | S_IWGRP
                    | S_IXGRP
                    | S_IWOTH
                    | S_IXOTH
                    | (
                        (S_IRGRP | S_IWGRP | S_ISGID)
                        if self.coursedir.groupshared
                        else 0
                    )
                ),
            )
        else:
            # 0755
            self.ensure_directory(
                self.dest_path,
                (
                    S_IRUSR
                    | S_IWUSR
                    | S_IXUSR
                    | S_IXGRP
                    | S_IXOTH
                    | (
                        (S_IRGRP | S_IWGRP | S_ISGID)
                        if self.coursedir.groupshared
                        else 0
                    )
                ),
            )

    def copy_files(self):
        """
        Overried copy_files and add personalized-feedback generation
        """
        if self.coursedir.student_id_exclude:
            exclude_students = set(self.coursedir.student_id_exclude.split(","))
        else:
            exclude_students = set()

        html_files = glob.glob(os.path.join(self.src_path, "*.html"))
        for html_file in html_files:
            if "hashcode" in html_file:
                self.log.debug("Skipping hashcode info")
                continue
            regexp = re.escape(os.path.sep).join(
                [
                    self.coursedir.format_path(
                        self.coursedir.feedback_directory,
                        "(?P<student_id>.*)",
                        self.coursedir.assignment_id,
                        escape=True,
                    ),
                    "(?P<notebook_id>.*).html",
                ]
            )

            m = re.match(regexp, html_file)
            if m is None:
                msg = "Could not match '%s' with regexp '%s'" % (html_file, regexp)
                self.log.error(msg)
                continue

            gd = m.groupdict()
            student_id = gd["student_id"]
            notebook_id = gd["notebook_id"]
            if student_id in exclude_students:
                self.log.debug("Skipping student '{}'".format(student_id))
                continue

            feedback_dir = os.path.split(html_file)[0]
            submission_dir = self.coursedir.format_path(
                self.coursedir.submitted_directory,
                student_id,
                self.coursedir.assignment_id,
            )

            if self.personalized_feedback:
                dest = os.path.join(
                    self.dest_path, student_id, self.coursedir.assignment_id
                )
                # u+rwx, g+wx, o+wx
                self.ensure_directory(
                    dest,
                    (
                        S_IRUSR
                        | S_IWUSR
                        | S_IXUSR
                        | S_IRGRP
                        | S_IXGRP
                        | S_IXOTH
                        | S_IROTH
                        | (
                            (S_IRGRP | S_IWGRP | S_ISGID)
                            if self.coursedir.groupshared
                            else 0
                        )
                    ),
                )

                dest = os.path.join(dest, notebook_id + ".html")

                self.log.info(
                    "Releasing feedback for student '{}' on assignment '{}/{}/{}' ".format(
                        student_id,
                        self.coursedir.course_id,
                        self.coursedir.assignment_id,
                        notebook_id,
                    )
                )
            else:
                timestamp = open(os.path.join(feedback_dir, "timestamp.txt")).read()
                nbfile = os.path.join(submission_dir, "{}.ipynb".format(notebook_id))
                unique_key = make_unique_key(
                    self.coursedir.course_id,
                    self.coursedir.assignment_id,
                    notebook_id,
                    student_id,
                    timestamp,
                )

                self.log.debug("Unique key is: {}".format(unique_key))
                checksum = notebook_hash(nbfile, unique_key)
                dest = os.path.join(self.dest_path, "{}.html".format(checksum))

                self.log.info(
                    "Releasing feedback for student '{}' on assignment '{}/{}/{}' ({})".format(
                        student_id,
                        self.coursedir.course_id,
                        self.coursedir.assignment_id,
                        notebook_id,
                        timestamp,
                    )
                )

            shutil.copy(html_file, dest)
            self.log.info("Feedback released to: {}".format(dest))
