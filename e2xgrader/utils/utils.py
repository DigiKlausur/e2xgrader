import re
from typing import List
from urllib.parse import parse_qsl, urlencode, urlparse

from nbgrader.apps import NbGrader


def urljoin(*parts: List[str]) -> str:
    return re.sub(r"/+", r"/", ("/" + "/".join(parts)))


def format_url(url, params):
    parsed = urlparse(url)
    return parsed._replace(
        query=urlencode({**dict(parse_qsl(parsed.query)), **params})
    ).geturl()


def get_nbgrader_config():
    nbgrader = NbGrader()
    nbgrader.initialize([])
    return nbgrader.config
