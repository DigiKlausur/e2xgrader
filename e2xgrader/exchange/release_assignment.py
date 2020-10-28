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