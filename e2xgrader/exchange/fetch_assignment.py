import os
import glob
import nbformat

from nbgrader.exchange.default import ExchangeFetchAssignment

from ..preprocessors import Scramble, PermuteTasks


class E2xExchangeFetchAssignment(ExchangeFetchAssignment):

    def do_scrambling(self, dest, student_id):
        self.log.info(f'Scrambling for {student_id}')
        scrambler = Scramble(seed=hash(student_id))
        permuter = Scramble(seed=hash(student_id))
        for nb_path in glob.glob(os.path.join(dest, '*.ipynb')):
            nb = nbformat.read(nb_path, as_version=4)
            if len(nb.cells) > 0 and nb.cells[0].source.startswith('%% scramble'):
                resources = {}
                nb, resources = scrambler.preprocess(nb, resources)
                nb, resources = permuter.preprocess(nb, resources)
                nbformat.write(nb, nb_path)
        self.log.info('Scrambled')


    def copy_files(self):
        self.log.info("Source: {}".format(self.src_path))
        self.log.info("Destination: {}".format(self.dest_path))
        self.do_copy(self.src_path, self.dest_path)
        self.do_scrambling(self.dest_path, os.getenv('JUPYTERHUB_USER'))
        self.log.info("Fetched as: {} {}".format(self.coursedir.course_id, self.coursedir.assignment_id))