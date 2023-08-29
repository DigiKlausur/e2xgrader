import unittest

from e2xgrader.preprocessors import ClearHiddenTests
from e2xgrader.tests.test_utils.cells import (
    new_autograder_test_cell,
    new_multiplechoice_cell,
)
from e2xgrader.utils.extra_cells import get_choices


class TestClearHiddenTests(unittest.TestCase):
    def test_choice_cell(self):
        source = """### Multiplechoice Question
        - Choice 1
        - Choice 2
        - Choice 3"""
        cell = new_multiplechoice_cell(
            source=source,
            choice=["1", "2"],
            num_of_choices=3,
        )

        assert len(get_choices(cell)) == 2
        assert all([i in get_choices(cell) for i in [1, 2]])

        processed_cell, _ = ClearHiddenTests().preprocess_cell(cell, {}, 0)
        assert len(get_choices(processed_cell)) == 0
        assert processed_cell.source == source

    def test_code_cell(self):
        cell = new_autograder_test_cell(
            source="""### BEGIN HIDDEN TESTS
        assert 1 == 1
        ###END HIDDEN TESTS"""
        )

        processed_cell, _ = ClearHiddenTests().preprocess_cell(cell, {}, 0)
        assert processed_cell.source == ""
