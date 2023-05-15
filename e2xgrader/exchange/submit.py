import base64
import os
import sys
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

import nbformat
from nbgrader.exchange.default import ExchangeSubmit
from nbgrader.utils import check_mode, get_username

from .exchange import E2xExchange
from .utils import (
    append_hashcode,
    append_timestamp,
    compute_hashcode,
    generate_html,
    generate_student_info,
    truncate_hashcode,
)


class E2xExchangeSubmit(E2xExchange, ExchangeSubmit):
    def init_dest(self):
        if self.coursedir.course_id == "":
            self.fail("No course id specified. Re-run with --course flag.")
        if not self.authenticator.has_access(
            self.coursedir.student_id, self.coursedir.course_id
        ):
            self.fail("You do not have access to this course.")

        self.inbound_path = os.path.join(
            self.root, self.coursedir.course_id, self.inbound_directory
        )

        if self.personalized_inbound:
            self.inbound_path = os.path.join(
                self.inbound_path, os.getenv("JUPYTERHUB_USER")
            )

            if not os.path.isdir(self.inbound_path):
                self.log.warning(
                    "Inbound directory doesn't exist, creating {}".format(
                        self.inbound_path
                    )
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

        if not os.path.isdir(self.inbound_path):
            self.fail("Inbound directory doesn't exist: {}".format(self.inbound_path))
        if not check_mode(self.inbound_path, write=True, execute=True):
            self.fail(
                "You don't have write permissions to the directory: {}".format(
                    self.inbound_path
                )
            )

        self.cache_path = os.path.join(self.cache, self.coursedir.course_id)
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

    def copy_files(self):
        self.init_release()

        hashcode = "No hashcode present"

        # Original notebook file
        student_notebook_file = os.path.join(
            self.src_path, f"{self.coursedir.assignment_id}.ipynb"
        )

        if os.path.isfile(student_notebook_file):
            nb = nbformat.read(student_notebook_file, as_version=nbformat.NO_CONVERT)
            nb = append_timestamp(nb, self.timestamp)
            nbformat.write(nb, student_notebook_file)
            hashcode = truncate_hashcode(
                compute_hashcode(student_notebook_file, method="sha1")
            )

            username = get_username()
            generate_student_info(
                os.path.join(self.src_path, f"{username}_info.txt"),
                username,
                hashcode,
                self.timestamp,
            )
            nb = append_hashcode(nb, hashcode)
            generate_html(
                nb,
                os.path.join(
                    self.src_path, f"{self.coursedir.assignment_id}_hashcode.html"
                ),
            )
        else:
            self.log.warning(
                "Can not generate hashcode, notebook and assignment name does not match."
            )

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
        with open(os.path.join(dest_path, "timestamp.txt"), "w") as fh:
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
        with open(os.path.join(cache_path, "timestamp.txt"), "w") as fh:
            fh.write(self.timestamp)

        self.log.info(
            "Submitted as: {} {} {}".format(
                self.coursedir.course_id,
                self.coursedir.assignment_id,
                str(self.timestamp),
            )
        )

        return hashcode, self.timestamp

    def init_release(self):
        if self.coursedir.course_id == "":
            self.fail("No course id specified. Re-run with --course flag.")

        course_path = os.path.join(self.root, self.coursedir.course_id)
        outbound_path = os.path.join(course_path, self.outbound_directory)
        if self.personalized_outbound:
            self.release_path = os.path.join(
                outbound_path,
                os.getenv("JUPYTERHUB_USER"),
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
