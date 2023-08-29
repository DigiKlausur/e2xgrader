import base64
import pickle
import unittest
from copy import deepcopy

from nbformat.v4 import new_notebook

from e2xgrader.preprocessors import Unscramble
from e2xgrader.tests.test_utils.cells import (
    new_manually_graded_code_cell,
    new_manually_graded_markdown_cell,
    new_readonly_code_cell,
)


class TestUnscramble(unittest.TestCase):
    def setUp(self) -> None:
        self.config = dict(myvar1="5", myvar2="Hello", somevar="Goodbye!")

        self.nb = new_notebook(
            metadata=dict(
                scramble_config=dict(
                    seed=1289341782, config=base64.b85encode(pickle.dumps(self.config))
                )
            )
        )

        self.nb.cells.extend(
            [
                new_manually_graded_markdown_cell(
                    source="Here we want to replace {{ myvar1   }}!"
                ),
                new_readonly_code_cell(source="# Here we want to replace {{myvar2 }}"),
                new_manually_graded_code_cell(
                    source=(
                        "# Here we want to replace everything {{myvar1}} "
                        "{{ myvar2 }} and {{ somevar }}"
                    )
                ),
            ]
        )

    def test_unscramble(self):
        nb = deepcopy(self.nb)
        processed_nb, _ = Unscramble().preprocess(nb, {})
        for cell in processed_nb.cells:
            # Make sure none of the original names are there anymore
            assert all([key not in cell.source for key in self.config.keys()])
        for original_cell, processed_cell in zip(self.nb.cells, processed_nb.cells):
            for key, value in self.config.items():
                if key in original_cell:
                    assert key not in processed_cell
                    assert value in processed_cell

    def test_no_scramble_config(self):
        nb = deepcopy(self.nb)
        del nb.metadata["scramble_config"]
        processed_nb, _ = Unscramble().preprocess(nb, {})
        for original_cell, processed_cell in zip(self.nb.cells, processed_nb.cells):
            assert original_cell.source == processed_cell.source
