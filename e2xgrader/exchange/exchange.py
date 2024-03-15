from textwrap import dedent

from nbgrader.exchange.default import Exchange
from nbgrader.utils import check_directory
from traitlets import Bool, Unicode


class E2xExchange(Exchange):
    personalized_outbound = Bool(
        False,
        help=dedent(
            """
            Whether to use a personalized outbound directory per student.
            This is the directory where students fetch their assignments from.
            If this is set to True, each student will have their own version of the assignment.
            """
        ),
    ).tag(config=True)

    personalized_inbound = Bool(
        True,
        help=dedent(
            """
            Whether to use a personalized inbound directory per student.
            This is the directory where students submit their assignments to.
            If this is set to True, each student will submit their assignments 
            to their own directory.
            """
        ),
    ).tag(config=True)

    personalized_feedback = Bool(
        True,
        help=dedent(
            """
            Whether to use a personalized feedback directory per student.
            This is the directory where students receive feedback for their assignments.
            If this is set to True, each student will receive feedback in their own directory.
            """
        ),
    ).tag(config=True)

    grader = Bool(
        False,
        help=dedent(
            """
            A flag whether the current user is grader. Used for personalized-outbound
            to retrive the released assignment for one of the students,so that
            lister only shows one released assignment instead of showing all
            individualized assignments from all users
            """
        ),
    ).tag(config=True)

    outbound_directory = Unicode("outbound", help="The name of the outbound directory")

    inbound_directory = Unicode("inbound", help="The name of the inbound directory")

    feedback_directory = Unicode("feedback", help="The name of the feedback directory")

    def __init__(self, coursedir=None, authenticator=None, **kwargs):
        super().__init__(coursedir=coursedir, authenticator=authenticator, **kwargs)

        if self.personalized_outbound:
            self.outbound_directory = "personalized-outbound"

        if self.personalized_inbound:
            self.inbound_directory = "personalized-inbound"

        if self.personalized_feedback:
            self.feedback_directory = "personalized-feedback"

    def ensure_root(self):
        """
        See if the exchange directory exists and readable, fail if not.
        We do not need to make the exchange root writable by default.
        """
        if not check_directory(self.root, read=True, execute=True):
            self.fail(
                "Unreadable directory, please contact your instructor: {}".format(
                    self.root
                )
            )
