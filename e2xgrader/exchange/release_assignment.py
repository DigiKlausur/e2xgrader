import os
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

from nbgrader.exchange.default import ExchangeReleaseAssignment

from .exchange import E2xExchange


class E2xExchangeReleaseAssignment(E2xExchange, ExchangeReleaseAssignment):
    def init_dest(self):
        if self.coursedir.course_id == "":
            self.fail("No course id specified. Re-run with --course flag.")

        self.course_path = os.path.join(self.root, self.coursedir.course_id)
        self.outbound_path = os.path.join(self.course_path, self.outbound_directory)
        self.inbound_path = os.path.join(self.course_path, self.inbound_directory)

        # 0755
        # groupshared: +2040
        self.ensure_directory(
            self.course_path,
            S_IRUSR
            | S_IWUSR
            | S_IXUSR
            | S_IRGRP
            | S_IXGRP
            | S_IROTH
            | S_IXOTH
            | ((S_ISGID | S_IWGRP) if self.coursedir.groupshared else 0),
        )

        if self.personalized_outbound:
            # the dest path is <exchange_root>/personalized-outbound/<username>/<assignment_id>
            # <username> is created by either grader via formgrader or student during spawning
            # <username> here is deterministic and has to be in the release directory
            self.dest_path = self.outbound_path

            # 0777 for personalized_outbound
            # groupshared: +2040
            self.ensure_directory(
                self.dest_path,
                S_IRUSR
                | S_IWUSR
                | S_IXUSR
                | S_IRGRP
                | S_IWGRP
                | S_IXGRP
                | S_IROTH
                | S_IWOTH
                | S_IXOTH
                | ((S_ISGID | S_IWGRP) if self.coursedir.groupshared else 0),
            )
        else:
            self.dest_path = os.path.join(
                self.outbound_path, self.coursedir.assignment_id
            )

            # 0755
            # groupshared: +2040
            self.ensure_directory(
                self.outbound_path,
                S_IRUSR
                | S_IWUSR
                | S_IXUSR
                | S_IRGRP
                | S_IXGRP
                | S_IROTH
                | S_IXOTH
                | ((S_ISGID | S_IWGRP) if self.coursedir.groupshared else 0),
            )

        # 0733 with set GID so student submission will have the instructors group
        # groupshared: +0040
        self.ensure_directory(
            self.inbound_path,
            S_ISGID
            | S_IRUSR
            | S_IWUSR
            | S_IXUSR
            | S_IWGRP
            | S_IXGRP
            | S_IWOTH
            | S_IXOTH
            | (S_IRGRP if self.coursedir.groupshared else 0),
        )

    def copy_files(self):
        if self.personalized_outbound:
            # check available users under course_path/<assignmet_dir>/<username>
            user_list = [
                user
                for user in os.listdir(self.src_path)
                if os.path.isdir(os.path.join(self.src_path, user))
                and user != self.coursedir.assignment_id
            ]
            for user in user_list:
                released_assignment_root = os.path.join(self.dest_path, user)
                released_user_assignment = os.path.join(
                    released_assignment_root, self.coursedir.assignment_id
                )
                if os.path.isdir(released_user_assignment):
                    shutil.rmtree(released_user_assignment)

                src_assignment = os.path.join(self.src_path, user)
                if os.path.isdir(src_assignment):
                    self.log.info(f"Source: {src_assignment}")
                    self.log.info(f"Destination: {released_user_assignment}")
                    self.do_copy(src_assignment, released_user_assignment)
                    self.set_released_assignment_perm(released_user_assignment)
                else:
                    self.log.info(f"Src assignment not found: {src_assignment}")
        else:
            if os.path.isdir(self.dest_path):
                if self.force:
                    self.log.info(
                        "Overwriting files: {} {}".format(
                            self.coursedir.course_id, self.coursedir.assignment_id
                        )
                    )
                    shutil.rmtree(self.dest_path)
                else:
                    self.fail(
                        "Destination already exists, add --force to overwrite: {} {}".format(
                            self.coursedir.course_id, self.coursedir.assignment_id
                        )
                    )

            self.log.info(f"Source: {self.src_path}")
            self.log.info(f"Destination: {self.dest_path}")
            self.do_copy(self.src_path, self.dest_path)
            self.set_released_assignment_perm(self.dest_path)
            self.log.info(
                "Released as: {} {}".format(
                    self.coursedir.course_id, self.coursedir.assignment_id
                )
            )

    def set_released_assignment_perm(self, path):
        self.set_perms(
            path,
            fileperms=(
                S_IRUSR
                | S_IWUSR
                | S_IRGRP
                | S_IROTH
                | (S_IWGRP if self.coursedir.groupshared else 0)
            ),
            dirperms=(
                S_IRUSR
                | S_IWUSR
                | S_IXUSR
                | S_IRGRP
                | S_IXGRP
                | S_IROTH
                | S_IXOTH
                | ((S_ISGID | S_IWGRP) if self.coursedir.groupshared else 0)
            ),
        )
