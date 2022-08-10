import unittest

import nbformat

from e2xgrader.models import PresetModel, TaskModel
from e2xgrader.utils.nbgrader_cells import (
    get_points,
    get_tasks,
    get_valid_name,
    is_description,
    is_solution_cell,
)

from ..test_utils.test_utils import add_question_to_task, create_temp_course


class TestNbgraderCells(unittest.TestCase):
    def setUp(self):
        tmp_dir, coursedir = create_temp_course()
        self.coursedir = coursedir
        self.tmp_dir = tmp_dir

    def test_get_valid_name(self):
        valid_name = "Abcdef182_-"
        assert get_valid_name(valid_name) == valid_name

        invalid_name = "Abc $$$ 123"
        assert get_valid_name(invalid_name) == "Abc_____123"

        no_char_name = "123"
        assert get_valid_name(no_char_name) == "Task_" + no_char_name

    def test_get_tasks_from_empty_notebook(self):
        model = TaskModel(self.coursedir)
        res = model.new(name="TestTask", pool="TestPool")
        assert res["success"]

        nb = nbformat.read(res["path"], as_version=nbformat.NO_CONVERT)
        assert len(get_tasks(nb)) == 0

    def test_get_tasks_from_notebook_with_tasks(self):
        model = TaskModel(self.coursedir)
        res = model.new(name="TestTask", pool="TestPool")
        assert res["success"]
        add_question_to_task(
            self.coursedir, res["path"], "Freetext", grade_id="task1", points=10
        )
        nb = nbformat.read(res["path"], as_version=nbformat.NO_CONVERT)
        assert len(get_tasks(nb)) == 1
        assert len(get_tasks(nb)[0]) == 2

        add_question_to_task(
            self.coursedir, res["path"], "Multiple Choice", grade_id="task2", points=10
        )
        nb = nbformat.read(res["path"], as_version=nbformat.NO_CONVERT)
        assert len(get_tasks(nb)) == 2
        assert len(get_tasks(nb)[1]) == 1

    def test_is_solution_cell(self):
        model = PresetModel(self.coursedir)
        freetext = model.get_question_preset("Freetext")
        assert not is_solution_cell(freetext[0])
        assert is_solution_cell(freetext[1])

    def test_is_description_cell(self):
        model = PresetModel(self.coursedir)
        freetext = model.get_question_preset("Freetext")
        assert is_description(freetext[0])
        assert not is_description(freetext[1])

    def test_get_points(self):
        model = TaskModel(self.coursedir)
        res = model.new(name="TestTask", pool="TestPool")
        assert res["success"]
        add_question_to_task(
            self.coursedir, res["path"], "Freetext", grade_id="task1", points=10
        )
        nb = nbformat.read(res["path"], as_version=nbformat.NO_CONVERT)
        assert get_points(nb.cells[0]) == 0
        assert get_points(nb.cells[1]) == 0
        assert get_points(nb.cells[2]) == 10

    def tearDown(self):
        self.tmp_dir.cleanup()
