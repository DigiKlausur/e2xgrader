from typing import List


def urljoin(*parts: List[str]) -> str:
    return ("/" + "/".join(parts)).replace("//", "/")
