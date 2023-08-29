import sys
from argparse import ArgumentParser
from textwrap import dedent

from ..extensions import E2xExtensionManager


class Manager:
    def __init__(self):
        self.extension_manager = E2xExtensionManager()
        parser = ArgumentParser(
            description="E2X extension manager.",
            usage=dedent(
                """
                e2xgrader <command> [<args>]

                Available sub commands are:
                activate      activate a specific mode (teacher, student, student-exam)
                deactivate    deactivate all extensions"""
            ),
        )

        parser.add_argument("command", help="Subcommand to run")

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def activate(self):
        parser = ArgumentParser(
            description="Activate different modes",
            usage=dedent(
                """
                e2xgrader activate <mode> [--sys-prefix] [--user]

                Available modes are:
                teacher         activate the grader and all teaching extensions
                student         activate the student extensions
                student_exam    activate the student extensions in exam mode"""
            ),
        )
        # prefixing the argument with -- means it's optional
        parser.add_argument(
            "mode",
            help="Which mode to activate, can be teacher, student or student-exam",
        )
        parser.add_argument(
            "--sys-prefix",
            action="store_true",
            help="If the extensions should be installed to sys.prefix",
        )
        parser.add_argument(
            "--user",
            action="store_true",
            help="If the extensions should be installed to the user space",
        )

        args = parser.parse_args(sys.argv[2:])
        if not hasattr(self.extension_manager, f"activate_{args.mode}"):
            print("Unrecognized mode")
            parser.print_help()
            exit(1)
        sys_prefix = False
        user = False
        if args.sys_prefix:
            sys_prefix = True
        if args.user:
            user = True
        getattr(self.extension_manager, f"activate_{args.mode}")(
            sys_prefix=sys_prefix, user=user
        )

    def deactivate(self):
        parser = ArgumentParser(
            description="Deactivate extensions",
            usage=dedent("python -m e2xgrader deactivate [--sys-prefix] [--user]"),
        )
        # prefixing the argument with -- means it's optional
        parser.add_argument(
            "--sys-prefix",
            action="store_true",
            help="If the extensions should be uninstalled from sys.prefix",
        )
        parser.add_argument(
            "--user",
            action="store_true",
            help="If the extensions should be uninstalled from the user space",
        )

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
