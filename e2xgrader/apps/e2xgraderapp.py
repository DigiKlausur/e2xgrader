from argparse import ArgumentParser
import sys
from textwrap import dedent
from notebook.serverextensions import ToggleServerExtensionApp
from notebook.nbextensions import (
    uninstall_nbextension_python,
    install_nbextension_python, enable_nbextension_python,
    disable_nbextension, enable_nbextension, disable_nbextension_python)


class ExtensionManager:

    def deactivate(self, sys_prefix=True, user=False):
        self.disable_serverextension_py('nbgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension_py('e2xgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('nbgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('e2xgrader', sys_prefix=sys_prefix, user=user)
        uninstall_nbextension_python(module='nbgrader', sys_prefix=sys_prefix, user=user)
        uninstall_nbextension_python(module='e2xgrader', sys_prefix=sys_prefix, user=user)

    def install_nbextensions(self, module, sys_prefix=True, user=False):
        install_nbextension_python(module=module, sys_prefix=sys_prefix,
                                   user=user, overwrite=True)
        disable_nbextension_python(module=module, sys_prefix=sys_prefix,
                                   user=user)

    def enable_serverextension_py(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = True
        toggler.toggle_server_extension_python(module)

    def disable_serverextension(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = False
        toggler.toggle_server_extension(module)

    def disable_serverextension_py(self, module, sys_prefix=True, user=False):
        toggler = ToggleServerExtensionApp()
        toggler.sys_prefix = sys_prefix
        toggler.user = user
        toggler._toggle_value = False
        toggler.toggle_server_extension_python(module)

    def activate_teacher(self, sys_prefix=True, user=False):
        print(f'Activate teacher mode with sys_prefix = {sys_prefix} and user = {user}')
        # Enable server extensions
        self.enable_serverextension_py('nbgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('nbgrader.server_extensions.formgrader')
        self.disable_serverextension('nbgrader.server_extensions.assignment_list')
        self.enable_serverextension_py('e2xgrader', sys_prefix=sys_prefix, user=user)

        # Install nbgrader nbextensions
        self.install_nbextensions('nbgrader', sys_prefix=sys_prefix, user=user)
        enable_nbextension_python('nbgrader', sys_prefix=sys_prefix, user=user)
        disable_nbextension(require='create_assignment/main',
                            section='notebook', sys_prefix=sys_prefix, user=user)

        # Install e2xgrader nbextensions
        self.install_nbextensions('e2xgrader', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='extra_cells/main',
                           section='notebook', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='create_assignment/main',
                           section='notebook', sys_prefix=sys_prefix, user=user)

    def activate_student(self, sys_prefix=True, user=False):
        print(f'Activate student mode with sys_prefix = {sys_prefix} and user = {user}')
        # Enable server extensions
        self.enable_serverextension_py('nbgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('nbgrader.server_extensions.formgrader')
        self.disable_serverextension('nbgrader.server_extensions.assignment_list')
        self.enable_serverextension_py('e2xgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('e2xgrader.server_extensions.formgrader')

        # Install nbgrader nbextensions
        self.install_nbextensions('nbgrader', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='assignment_list/main',
                           section='tree', sys_prefix=sys_prefix, user=user)

        # Install e2xgrader nbextensions
        self.install_nbextensions('e2xgrader', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='extra_cells/main',
                           section='notebook', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='assignment_extension/main',
                           section='notebook', sys_prefix=sys_prefix, user=user)

    def activate_student_exam(self, sys_prefix=True, user=False):
        print(f'Activate student exam mode with sys_prefix = {sys_prefix} and user = {user}')
        # Enable server extensions
        self.activate_student(sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='exam_view/main',
                           section='notebook', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='restricted_tree/main',
                           section='tree', sys_prefix=sys_prefix, user=user)


class Manager:

    def __init__(self):
        self.extension_manager = ExtensionManager()
        parser = ArgumentParser(description='E2X extension manager.',
                                usage=dedent('''
                                             e2xgrader <command> [<args>]

                                             Available sub commands are:
                                               activate      activate a specific mode (teacher, student, student-exam)
                                               deactivate    deactivate all extensions'''))

        parser.add_argument('command', help='Subcommand to run')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def activate(self):
        parser = ArgumentParser(description='Activate different modes',
                                usage=dedent('''
                                             e2xgrader activate <mode> [--sys-prefix] [--user]

                                             Available modes are:
                                               teacher         activate the grader and all teaching extensions
                                               student         activate the student extensions
                                               student_exam    activate the student extensions in exam mode'''))
        # prefixing the argument with -- means it's optional
        parser.add_argument('mode', help='Which mode to activate, can be teacher, student or student-exam')
        parser.add_argument('--sys-prefix', action='store_true', help='If the extensions should be installed to sys.prefix')
        parser.add_argument('--user', action='store_true', help='If the extensions should be installed to the user space')

        args = parser.parse_args(sys.argv[2:])
        if not hasattr(self.extension_manager, f'activate_{args.mode}'):
            print('Unrecognized mode')
            parser.print_help()
            exit(1)
        sys_prefix = False
        user = False
        if args.sys_prefix:
            sys_prefix = True
        if args.user:
            user = True
        getattr(self.extension_manager, f'activate_{args.mode}')(sys_prefix=sys_prefix, user=user)

    def deactivate(self):
        parser = ArgumentParser(description='Deactivate extensions',
                                usage=dedent('python -m e2xgrader deactivate [--sys-prefix] [--user]'))
        # prefixing the argument with -- means it's optional
        parser.add_argument('--sys-prefix', action='store_true',
                            help='If the extensions should be uninstalled from sys.prefix')
        parser.add_argument('--user', action='store_true',
                            help='If the extensions should be uninstalled from the user space')

        args = parser.parse_args(sys.argv[2:])

        sys_prefix = False
        user = False
        if args.sys_prefix:
            sys_prefix = True
        if args.user:
            user = True
        self.extension_manager.deactivate(sys_prefix=sys_prefix, user=user)


def main():
    Manager()
