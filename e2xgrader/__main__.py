from .apps.e2xgraderapp import Manager
from .apps.nbgraderapp import main
import sys

if __name__ == '__main__':
    if sys.argv[1:2][0] not in ['activate', 'deactivate']:
        main()
    else:
        Manager()
