import os
from stat import (
    S_IRUSR, S_IWUSR, S_IXUSR,
    S_IRGRP, S_IWGRP, S_IXGRP,
    S_IROTH, S_IWOTH, S_IXOTH,
    S_ISGID, ST_MODE
)

from nbgrader.exchange.default import ExchangeReleaseAssignment

from .exchange import E2xExchange


class E2xExchangeReleaseAssignment(E2xExchange, ExchangeReleaseAssignment):

    def init_dest(self):
        if self.coursedir.course_id == '':
            self.fail("No course id specified. Re-run with --course flag.")

        self.course_path = os.path.join(self.root, self.coursedir.course_id)
        self.outbound_path = os.path.join(self.course_path, self.outbound_directory)
        self.inbound_path = os.path.join(self.course_path, self.inbound_directory)
        self.dest_path = os.path.join(self.outbound_path, self.coursedir.assignment_id)
        # 0755
        # groupshared: +2040
        self.ensure_directory(
            self.course_path,
            S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH|((S_ISGID|S_IWGRP) if self.coursedir.groupshared else 0)
        )
        # 0755
        # groupshared: +2040
        self.ensure_directory(
            self.outbound_path,
            S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH|((S_ISGID|S_IWGRP) if self.coursedir.groupshared else 0)
        )
        # 0733 with set GID so student submission will have the instructors group
        # groupshared: +0040
        self.ensure_directory(
            self.inbound_path,
            S_ISGID|S_IRUSR|S_IWUSR|S_IXUSR|S_IWGRP|S_IXGRP|S_IWOTH|S_IXOTH|(S_IRGRP if self.coursedir.groupshared else 0)
        )

    def copy_files(self):
        if os.path.isdir(self.dest_path):
            if self.force:
                self.log.info("Overwriting files: {} {}".format(
                    self.coursedir.course_id, self.coursedir.assignment_id
                ))
                shutil.rmtree(self.dest_path)
            else:
                self.fail("Destination already exists, add --force to overwrite: {} {}".format(
                    self.coursedir.course_id, self.coursedir.assignment_id
                ))
        self.log.info("Source: {}".format(self.src_path))
        self.log.info("Destination: {}".format(self.dest_path))
        self.do_copy(self.src_path, self.dest_path)
        self.set_perms(
            self.dest_path,
            fileperms=(S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH|(S_IWGRP if self.coursedir.groupshared else 0)),
            dirperms=(S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH|((S_ISGID|S_IWGRP) if self.coursedir.groupshared else 0)))

        if self.personalized_outbound:
            # Make assignment directory writable so that spawner can create it (K8s)
            os.chmod(self.dest_path,
                (S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IWGRP|S_IXGRP|S_IROTH|S_IWOTH|S_IXOTH))
        self.log.info("Released as: {} {}".format(self.coursedir.course_id, self.coursedir.assignment_id))