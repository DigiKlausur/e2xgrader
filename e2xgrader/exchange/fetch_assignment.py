import glob
import os
from textwrap import dedent

import nbformat
from nbgrader.exchange.default import ExchangeFetchAssignment
from nbgrader.utils import check_mode

from ..preprocessors import PermuteTasks, Scramble
from .exchange import E2xExchange


class E2xExchangeFetchAssignment(E2xExchange, ExchangeFetchAssignment):
    def init_src(self):
        if self.coursedir.course_id == "":
            self.fail("No course id specified. Re-run with --course flag.")
        if not self.authenticator.has_access(
            self.coursedir.student_id, self.coursedir.course_id
        ):
            self.fail("You do not have access to this course.")

        self.course_path = os.path.join(self.root, self.coursedir.course_id)
        self.outbound_path = os.path.join(self.course_path, self.outbound_directory)
        if self.personalized_outbound:
            self.src_path = os.path.join(
                self.outbound_path,
                os.getenv("JUPYTERHUB_USER"),
                self.coursedir.assignment_id,
            )
        else:
            self.src_path = os.path.join(
                self.outbound_path, self.coursedir.assignment_id
            )

        if not os.path.isdir(self.src_path):
            self._assignment_not_found(
                self.src_path, os.path.join(self.outbound_path, "*")
            )
        if not check_mode(self.src_path, read=True, execute=True):
            self.fail(
                "You don't have read permissions for the directory: {}".format(
                    self.src_path
                )
            )

    def do_scrambling(self, dest, student_id):
        self.log.info(f"Scrambling for {student_id}")
        scrambler = Scramble(seed=hash(student_id))
        permuter = PermuteTasks(seed=hash(student_id))
        for nb_path in glob.glob(os.path.join(dest, "*.ipynb")):
            nb = nbformat.read(nb_path, as_version=4)
            if len(nb.cells) > 0 and nb.cells[0].source.startswith("%% scramble"):
                resources = {}
                nb, resources = scrambler.preprocess(nb, resources)
                nb, resources = permuter.preprocess(nb, resources)
                nbformat.write(nb, nb_path)
        self.log.info("Scrambled")

    def copy_files(self):
        self.log.info("Source: {}".format(self.src_path))
        self.log.info("Destination: {}".format(self.dest_path))
        self.do_copy(self.src_path, self.dest_path)
        self.do_scrambling(self.dest_path, os.getenv("JUPYTERHUB_USER"))
        self.log.info(
            "Fetched as: {} {}".format(
                self.coursedir.course_id, self.coursedir.assignment_id
            )
        )

    def do_copy(self, src, dest):
        if self.personalized_outbound:
            personalized_src = os.path.join(src, os.getenv("JUPYTERHUB_USER"))
            if os.path.exists(personalized_src):
                src = personalized_src
            else:
                self.log.warning(
                    dedent(
                        f"""
                    Using personalized outbound, but no directory for
                    user {os.getenv('JUPYTERHUB_USER')} exists.
                    """
                    )
                )
        super().do_copy(src, dest)
