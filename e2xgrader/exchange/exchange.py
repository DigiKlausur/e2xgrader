from traitlets import Bool
from textwrap import dedent

from nbgrader.exchange.default import Exchange

class E2xExchange(Exchange):

    personalized_outbound = Bool(
        False,
        help='Whether to use a personalized outbound directory per student'
    ).tag(config=True)

    personalized_inbound = Bool(
        False,
        help='Whether to use a personalized inbound directory per student'
    ).tag(config=True)

    def ensure_root(self):
         """See if the exchange directory exists and readable, fail if not.
            We do not need to make the exchange root writable by default.
         """
        if not check_directory(self.root, read=True, execute=True):
            self.fail("Unreadable directory, please contact your instructor: {}".format(self.root))
