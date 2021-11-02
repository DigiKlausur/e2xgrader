from .apps.e2xgraderapp import Manager
from .apps.nbgraderapp import main as nbgrader_main
import sys


def main():
    if sys.argv[1:2][0] not in ["activate", "deactivate"]:
        nbgrader_main()
    else:
        Manager()


if __name__ == "__main__":
    main()
