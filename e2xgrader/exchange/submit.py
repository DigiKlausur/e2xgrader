import os
import base64
import sys
import nbformat
from stat import (
    S_IRUSR, S_IWUSR, S_IXUSR,
    S_IRGRP, S_IWGRP, S_IXGRP,
    S_IROTH, S_IWOTH, S_IXOTH
)
from nbgrader.exchange.default import ExchangeSubmit
from nbgrader.utils import check_mode, get_username
from .utils import (
    compute_hashcode, truncate_hashcode, append_hashcode, 
    append_timestamp, generate_html, generate_student_info)

class E2xExchangeSubmit(ExchangeSubmit):

    def copy_files(self):
        self.init_release()

        hashcode = 'No hashcode present'

        # Original notebook file
        student_notebook_file = os.path.join(self.src_path, f'{self.coursedir.assignment_id}.ipynb')

        if os.path.isfile(student_notebook_file):
            nb = nbformat.read(student_notebook_file, as_version=4)
            nb = append_timestamp(nb, self.timestamp)
            nbformat.write(nb, student_notebook_file)
            hashcode = truncate_hashcode(compute_hashcode(student_notebook_file, method='sha1'))

            username = get_username()
            generate_student_info(os.path.join(self.src_path, f'{username}_info.txt'), username, hashcode, self.timestamp)
            nb = append_hashcode(nb, hashcode)
            generate_html(nb, os.path.join(self.src_path, f'{self.coursedir.assignment_id}_hashcode.html'))
        else:
            self.log.warning('Can not generate hashcode, notebook and assignment name does not match.')

        dest_path = os.path.join(self.inbound_path, self.assignment_filename)
        if self.add_random_string:
            cache_path = os.path.join(self.cache_path, self.assignment_filename.rsplit('+', 1)[0])
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
            dirperms=(S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH))

        # Make this 0777=ugo=rwx so the instructor can delete later. Hidden from other users by the timestamp.
        os.chmod(
            dest_path,
            S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IWGRP|S_IXGRP|S_IROTH|S_IWOTH|S_IXOTH
        )

        # also copy to the cache
        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)
        self.do_copy(self.src_path, cache_path)
        with open(os.path.join(cache_path, "timestamp.txt"), "w") as fh:
            fh.write(self.timestamp)

        self.log.info("Submitted as: {} {} {}".format(
            self.coursedir.course_id, self.coursedir.assignment_id, str(self.timestamp)
        ))

        return hashcode, self.timestamp

    def start(self):
        if sys.platform == 'win32':
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