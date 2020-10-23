import argparse
import sys
from textwrap import dedent
from notebook.config_manager import BaseJSONConfigManager
from jupyter_core.paths import jupyter_config_path
from notebook.serverextensions import ToggleServerExtensionApp
from notebook.nbextensions import (
    install_nbextension_python, enable_nbextension_python,
    disable_nbextension, enable_nbextension, disable_nbextension_python)


class ExtensionManager:
    
    def install_nbextensions(self, module, sys_prefix=True, user=False):
        install_nbextension_python(module=module, sys_prefix=sys_prefix,
                                   user=user, overwrite=True)
        disable_nbextension_python(module=module, sys_prefix=sys_prefix,
                                   user=user)
            
    def enable_serverextension(self, module, sys_prefix=True, user=False):
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
        
    def activate_teacher(self, sys_prefix=True, user=False):
        print(f'Activate teacher mode with sys_prefix = {sys_prefix} and user = {user}')
        # Enable server extensions
        self.enable_serverextension('nbgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('nbgrader.server_extensions.formgrader')
        self.disable_serverextension('nbgrader.server_extensions.assignment_list')
        self.enable_serverextension('e2xgrader', sys_prefix=sys_prefix, user=user)
        # Install nbextensions
        self.install_nbextensions('nbgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('e2xgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('e2xstudent', sys_prefix=sys_prefix, user=user)
        # Enable nbextensions
        enable_nbextension_python('nbgrader', sys_prefix=sys_prefix, user=user)
        disable_nbextension(require='create_assignment/main', 
                            section='notebook', sys_prefix=sys_prefix, user=user)
        enable_nbextension_python('e2xgrader', sys_prefix=sys_prefix, user=user)
        
    def activate_student(self, sys_prefix=True, user=False):
        print(f'Activate student mode with sys_prefix = {sys_prefix} and user = {user}')
        # Enable server extensions
        self.enable_serverextension('nbgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('nbgrader.server_extensions.formgrader')
        self.disable_serverextension('nbgrader.server_extensions.assignment_list')
        self.enable_serverextension('e2xgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('e2xgrader.server_extensions.formgrader')
        # Install nbextensions
        self.install_nbextensions('nbgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('e2xgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('e2xstudent', sys_prefix=sys_prefix, user=user)
        # Enable nbextensions
        enable_nbextension(require='assignment_list/main', 
                            section='tree', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='extra_cells/main', 
                            section='notebook', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='assignment_view/main', 
                            section='notebook', sys_prefix=sys_prefix, user=user)
        
    def activate_student_exam(self, sys_prefix=True, user=False):
        print(f'Activate student exam mode with sys_prefix = {sys_prefix} and user = {user}')
        # Enable server extensions
        self.enable_serverextension('nbgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('nbgrader.server_extensions.formgrader')
        self.disable_serverextension('nbgrader.server_extensions.assignment_list')
        self.enable_serverextension('e2xgrader', sys_prefix=sys_prefix, user=user)
        self.disable_serverextension('e2xgrader.server_extensions.formgrader')
        # Install nbextensions
        self.install_nbextensions('nbgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('e2xgrader', sys_prefix=sys_prefix, user=user)
        self.install_nbextensions('e2xstudent', sys_prefix=sys_prefix, user=user)
        # Enable nbextensions
        enable_nbextension(require='assignment_list/main', 
                            section='tree', sys_prefix=sys_prefix, user=user)
        enable_nbextension(require='extra_cells/main', 
                            section='notebook', sys_prefix=sys_prefix, user=user)
        enable_nbextension_python('e2xstudent', sys_prefix=sys_prefix, user=user)

class Manager:

    def __init__(self):
        self.extension_manager = ExtensionManager()
        parser = argparse.ArgumentParser(description='E2X extension manager.',
            usage=dedent('''
            	python -m e2xgrader <command> [<args>]

            	Available sub commands are:
            	  activate      activate a specific mode (teacher, student, student-exam)
            	  deactivate    deactivate all extensions

            '''))

        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()


    def activate(self):
        parser = argparse.ArgumentParser(
            description='Activate different modes',
            usage=dedent('''
            	python -m e2xgrader activate <mode> [--sys-prefix] [--user]

            	Available modes are:
            	  teacher         activate the grader and all teaching extensions
            	  student         activate the student extensions
            	  student_exam    activate the student extensions in exam mode
        	'''))
        # prefixing the argument with -- means it's optional
        parser.add_argument('mode', help='Which mode to activate, can be teacher, student or student-exam')
        parser.add_argument('--sys-prefix', action='store_true', help='If the extensions should be installed to sys.prefix')
        parser.add_argument('--user', action='store_true', help='If the extensions should be installed to the user space')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
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
        
        if len(sys.argv[2:]):
        	print('deactivate does not take additional arguments!')
        	exit(1)
        print('Deactivate!')

        
if __name__ == '__main__':
    Manager()