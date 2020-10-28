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