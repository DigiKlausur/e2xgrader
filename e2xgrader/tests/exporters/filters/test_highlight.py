import unittest

from bs4 import BeautifulSoup

from e2xgrader.exporters.filters import Highlight2HTMLwithLineNumbers


class TestHighlight2HTMLwithLineNumbers(unittest.TestCase):
    def test_insert_line_numbers(self):
        source = "line 1\nline 2\nline 3"
        highlighter = Highlight2HTMLwithLineNumbers()
        html = highlighter.__call__(source)

        soup = BeautifulSoup(html, features="html.parser")
        line_numbers = soup.find_all("span", attrs={"class": "linenos"})
        assert len(line_numbers) == len(source.split("\n"))

    def test_insert_line_numbers_with_language(self):
        source = "line 1\nline 2\nline 3"
        highlighter = Highlight2HTMLwithLineNumbers()
        html = highlighter(source, language="ipython3")

        soup = BeautifulSoup(html, features="html.parser")
        line_numbers = soup.find_all("span", attrs={"class": "linenos"})
        assert len(line_numbers) == len(source.split("\n"))
