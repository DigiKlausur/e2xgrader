from nbconvert.filters.highlight import Highlight2HTML, _pygments_highlight


class Highlight2HTMLwithLineNumbers(Highlight2HTML):
    def __call__(self, source, language=None, metadata=None):
        """
        Return a syntax-highlighted version of the input source as html output.
        Same as Highlight2HTML but with inline line numbers

        Parameters
        ----------
        source : str
            source of the cell to highlight
        language : str
            language to highlight the syntax of
        metadata : NotebookNode cell metadata
            metadata of the cell to highlight
        """
        from pygments.formatters import HtmlFormatter

        if not language:
            language = self.pygments_lexer

        return _pygments_highlight(
            source if len(source) > 0 else " ",
            # needed to help post processors:
            HtmlFormatter(cssclass=" highlight hl-" + language, linenos="inline"),
            language,
            metadata,
        )
