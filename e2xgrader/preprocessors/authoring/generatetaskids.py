import glob
import os

import nbformat

from ...utils.nbgrader_cells import (
    get_task_info,
    get_valid_name,
    is_description,
    is_grade,
    is_solution,
)
from .preprocessor import Preprocessor


class GenerateTaskIDs(Preprocessor):
    def generate_ids(self, nb, name):
        task = get_task_info(nb)

        ids = []
        suffix = ord("A")

        for subtask in task["subtasks"]:
            subtask_id = "{}_{}".format(name, chr(suffix))
            ids.append(subtask_id)
            suffix += 1
            tests = 0
            headers = 0
            for idx in subtask:
                cell = nb.cells[idx]
                if is_description(cell):
                    cell.metadata.nbgrader.grade_id = "{}_Description{}".format(
                        subtask_id, headers
                    )
                    headers += 1
                elif is_solution(cell):
                    cell.metadata.nbgrader.grade_id = subtask_id
                elif is_grade(cell):
                    cell.metadata.nbgrader.grade_id = "test_{}{}".format(
                        subtask_id, tests
                    )
                    tests += 1

        if "header" in task:
            header = nb.cells[task["header"]]
            header.metadata.nbgrader.grade_id = "{}_Header".format("".join(ids))

        return nb

    def preprocess(self, resources):
        for task_dict in resources["tasks"]:
            task = os.path.join(task_dict["pool"], task_dict["task"])
            task_path = os.path.join(resources["tmp_dir"], "tasks", task)
            nb_files = glob.glob(os.path.join(task_path, "*.ipynb"))
            for nb_file in nb_files:
                nb = nbformat.read(nb_file, as_version=4)
                name = os.path.splitext(os.path.basename(nb_file))[0]
                name = get_valid_name(name)
                self.generate_ids(nb, name)
                nbformat.write(nb, nb_file)
