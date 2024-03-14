import base64
import glob
import os
import sys
from datetime import datetime
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
from textwrap import dedent

from nbgrader.exchange.default import ExchangeSubmit
from nbgrader.utils import check_mode, get_username
from traitlets import Type

from ..exporters import SubmissionExporter
from ..utils.mode import E2xGraderMode, infer_e2xgrader_mode
from .exchange import E2xExchange
from .hash_utils import (
    compute_hashcode_of_file,
    generate_directory_hash_file,
    truncate_hashcode,
)
from .utils import generate_student_info_file, generate_submission_html


class E2xExchangeSubmit(E2xExchange, ExchangeSubmit):

    submission_exporter_class = Type(
        SubmissionExporter,
        klass="nbconvert.exporters.HTMLExporter",
        help=dedent(
            """
            The class used for creating HTML files from exam notebooks.
            Must be a subclass of `nbconvert.exporters.HTMLExporter`.
            The exporter will receive the hashcode and timestamp as resources.
            """
        ),
    ).tag(config=True)

    def init_dest(self):
        if self.coursedir.course_id == "":
            self.fail("No course id specified. Re-run with --course flag.")
        if not self.authenticator.has_access(
            self.coursedir.student_id, self.coursedir.course_id
        ):
            self.fail("You do not have access to this course.")

        self.inbound_path = self.get_inbound_path()

        if self.personalized_inbound:
            self.create_personalized_inbound_directory()

        self.ensure_inbound_directory_exists()

        self.ensure_write_permissions()

        self.cache_path = self.get_cache_path()

        self.set_assignment_filename()

        self.timestamp_file = "timestamp.txt"

    def get_inbound_path(self):
        inbound_path = os.path.join(
            self.root, self.coursedir.course_id, self.inbound_directory
        )

        if self.personalized_inbound:
            inbound_path = os.path.join(inbound_path, get_username())

        return inbound_path

    def create_personalized_inbound_directory(self):
        if not os.path.isdir(self.inbound_path):
            self.log.warning(
                "Inbound directory doesn't exist, creating {}".format(self.inbound_path)
            )
            # 0777 with set GID so student instructors can read students' submissions
            self.ensure_directory(
                self.inbound_path,
                S_ISGID
                | S_IRUSR
                | S_IWUSR
                | S_IXUSR
                | S_IRGRP
                | S_IWGRP
                | S_IXGRP
                | S_IROTH
                | S_IWOTH
                | S_IXOTH
                | (S_IRGRP if self.coursedir.groupshared else 0),
            )

    def ensure_inbound_directory_exists(self):
        if not os.path.isdir(self.inbound_path):
            self.fail("Inbound directory doesn't exist: {}".format(self.inbound_path))

    def ensure_write_permissions(self):
        if not check_mode(self.inbound_path, write=True, execute=True):
            self.fail(
                "You don't have write permissions to the directory: {}".format(
                    self.inbound_path
                )
            )

    def get_cache_path(self):
        return os.path.join(self.cache, self.coursedir.course_id)

    def set_assignment_filename(self):
        if self.coursedir.student_id != "*":
            # An explicit student id has been specified on the command line; we use it as student_id
            if "*" in self.coursedir.student_id or "+" in self.coursedir.student_id:
                self.fail(
                    "The student ID should contain no '*' nor '+'; got {}".format(
                        self.coursedir.student_id
                    )
                )
            student_id = self.coursedir.student_id
        else:
            student_id = get_username()
        if self.add_random_string:
            random_str = base64.urlsafe_b64encode(os.urandom(9)).decode("ascii")
            self.assignment_filename = "{}+{}+{}+{}".format(
                student_id, self.coursedir.assignment_id, self.timestamp, random_str
            )
        else:
            self.assignment_filename = "{}+{}+{}".format(
                student_id, self.coursedir.assignment_id, self.timestamp
            )

    def format_timestamp(self, format: str = "%H:%M:%S") -> str:
        return datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S.%f %Z").strftime(
            format
        )

    def create_exam_files(self):
        username = get_username()
        generate_directory_hash_file(
            self.src_path,
            method="sha1",
            exclude_files=[self.timestamp_file, f"{username}_info.txt", "*.html"],
            exclude_subfolders=[".ipynb_checkpoints"],
            output_file="SHA1SUM.txt",
        )
        hashcode = truncate_hashcode(
            compute_hashcode_of_file(
                os.path.join(self.src_path, "SHA1SUM.txt"), method="sha1"
            ),
            number_of_chunks=3,
            chunk_size=4,
        )
        generate_student_info_file(
            os.path.join(self.src_path, f"{username}_info.txt"),
            username=username,
            hashcode=hashcode,
            timestamp=self.format_timestamp(),
        )

        # Discover all ipynb files in the src_path and generate HTML files for them
        exporter = self.submission_exporter_class(config=self.config)
        ipynb_files = glob.glob(os.path.join(self.src_path, "*.ipynb"))
        for ipynb_file in ipynb_files:
            generate_submission_html(
                ipynb_file,
                os.path.join(
                    self.src_path,
                    os.path.splitext(os.path.basename(ipynb_file))[0]
                    + "_hashcode.html",
                ),
                hashcode,
                self.format_timestamp(format="%Y-%m-%d %H:%M:%S"),
                exporter,
            )
        return hashcode

    def copy_files(self):
        self.init_release()

        hashcode = "No hashcode generated"

        if infer_e2xgrader_mode() == E2xGraderMode.STUDENT_EXAM.value:
            self.log.info("Exam mode detected. Generating exam files.")
            hashcode = self.create_exam_files()

        dest_path = os.path.join(self.inbound_path, self.assignment_filename)
        if self.add_random_string:
            cache_path = os.path.join(
                self.cache_path, self.assignment_filename.rsplit("+", 1)[0]
            )
        else:
            cache_path = os.path.join(self.cache_path, self.assignment_filename)

        self.log.info("Source: {}".format(self.src_path))
        self.log.info("Destination: {}".format(dest_path))

        # copy to the real location
        self.check_filename_diff()
        self.do_copy(self.src_path, dest_path)
        with open(os.path.join(dest_path, self.timestamp_file), "w") as fh:
            fh.write(self.timestamp)
        self.set_perms(
            dest_path,
            fileperms=(S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH),
            dirperms=(
                S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH
            ),
        )

        # Make this 0777=ugo=rwx so the instructor can delete later.
        # Hidden from other users by the timestamp.
        os.chmod(
            dest_path,
            S_IRUSR
            | S_IWUSR
            | S_IXUSR
            | S_IRGRP
            | S_IWGRP
            | S_IXGRP
            | S_IROTH
            | S_IWOTH
            | S_IXOTH,
        )

        # also copy to the cache
        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)
        self.do_copy(self.src_path, cache_path)
        with open(os.path.join(cache_path, self.timestamp_file), "w") as fh:
            fh.write(self.timestamp)

        self.log.info(
            "Submitted as: {} {} {}".format(
                self.coursedir.course_id,
                self.coursedir.assignment_id,
                str(self.timestamp),
            )
        )

        return hashcode.upper(), self.timestamp

    def init_release(self):
        if self.coursedir.course_id == "":
            self.fail("No course id specified. Re-run with --course flag.")

        course_path = os.path.join(self.root, self.coursedir.course_id)
        outbound_path = os.path.join(course_path, self.outbound_directory)
        if self.personalized_outbound:
            self.release_path = os.path.join(
                outbound_path,
                get_username(),
                self.coursedir.assignment_id,
            )
        else:
            self.release_path = os.path.join(
                outbound_path, self.coursedir.assignment_id
            )

        if not os.path.isdir(self.release_path):
            self.fail("Assignment not found: {}".format(self.release_path))
        if not check_mode(self.release_path, read=True, execute=True):
            self.fail(
                "You don't have read permissions for the directory: {}".format(
                    self.release_path
                )
            )

    def start(self):
        if sys.platform == "win32":
            self.fail("Sorry, the exchange is not available on Windows.")
        if not self.coursedir.groupshared:
            # This just makes sure that directory is o+rwx.  In group shared
            # case, it is up to admins to ensure that instructors can write
            # there.
            self.ensure_root()

        self.set_timestamp()
        self.init_src()
        self.init_dest()
        return self.copy_files()
