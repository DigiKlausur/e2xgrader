from nbgrader.apps import NbGrader


def get_nbgrader_config():
    nbgrader = NbGrader()
    nbgrader.initialize([])
    return nbgrader.config
