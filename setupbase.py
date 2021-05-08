import os
import sys
from os.path import join as pjoin

try:
    from shutil import which
except ImportError:
    # which() function copied from Python 3.4.3; PSF license
    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
        conforms to the given mode on the PATH, or None if there is no such
        file.
        `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
        of os.environ.get("PATH"), or can be overridden with a custom search
        path.
        """
        # Check that a given file can be accessed with the correct mode.
        # Additionally check that `file` is not a directory, as on Windows
        # directories pass the os.access check.
        def _access_check(fn, mode):
            return (os.path.exists(fn) and os.access(fn, mode)
                    and not os.path.isdir(fn))

        # If we're given a path with a directory part, look it up directly rather
        # than referring to PATH directories. This includes checking relative to the
        # current directory, e.g. ./script
        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return None

        if path is None:
            path = os.environ.get("PATH", os.defpath)
        if not path:
            return None
        path = path.split(os.pathsep)

        if sys.platform == "win32":
            # The current directory takes precedence on Windows.
            if os.curdir not in path:
                path.insert(0, os.curdir)

            # PATHEXT is necessary to check on Windows.
            pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
            # See if the given file matches any of the expected path extensions.
            # This will allow us to short circuit when given "python.exe".
            # If it does match, only test that one, otherwise we have to try
            # others.
            if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
                files = [cmd]
            else:
                files = [cmd + ext for ext in pathext]
        else:
            # On other platforms you don't have things like PATHEXT to tell you
            # what file suffixes are executable, so just pass on cmd as-is.
            files = [cmd]

        seen = set()
        for dir in path:
            normdir = os.path.normcase(dir)
            if normdir not in seen:
                seen.add(normdir)
                for thefile in files:
                    name = os.path.join(dir, thefile)
                    if _access_check(name, mode):
                        return name
        return None


def discover_nbextensions(name):
    has_npm = which('npm') is not None
    src_path = pjoin('nbextensions', 'src')
    lib_path = pjoin('nbextensions', 'lib')
    extension_path = pjoin(name, src_path)
    extension_files = []
    for (dirname, dirnames, filenames) in os.walk(extension_path):
        root = os.path.relpath(dirname, extension_path)
        for filename in filenames:
            if filename.endswith(".pyc"):
                continue
            if has_npm:
                extension_files.append(pjoin(lib_path, root, filename))
            else:
                extension_files.append(pjoin(src_path, root, filename))

    return extension_files


def js_prerelease(command):

    """decorator for building es2015 js prior to another command"""
    class DecoratedCommand(command):
        def run(self):
            if which('npm') is not None:
                assert os.system('npm install') == 0, 'npm install failed'
                assert os.system('npm run build') == 0, 'npm build failed'
            command.run(self)
    return DecoratedCommand
