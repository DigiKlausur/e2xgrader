from nbgrader.exchange.default import ExchangeFetchFeedback

from .exchange import E2xExchange


class E2xExchangeFetchFeedback(E2xExchange, ExchangeFetchFeedback):
    pass