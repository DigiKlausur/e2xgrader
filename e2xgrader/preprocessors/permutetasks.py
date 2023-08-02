import random
from copy import deepcopy

from e2xcore.utils.nbgrader_cells import get_tasks, grade_id
from nbformat.v4 import new_notebook
from nbgrader.preprocessors import NbGraderPreprocessor


class PermuteTasks(NbGraderPreprocessor):
    def __init__(self, **kw):
        self.rand = random.Random()
        if kw and "seed" in kw:
            self.rand = random.Random(kw["seed"])

    def permute(self, nb):
        permuted_nb = new_notebook()
        # Get indices of tasks
        tasks = get_tasks(nb)
        # Shuffle tasks
        shuffled_tasks = deepcopy(tasks)
        random.shuffle(shuffled_tasks)
        # Record original order
        original_order = []

        cursor = 0

        for task in tasks:
            # Add all cells between cursor and current task
            for idx in range(cursor, task[0]):
                permuted_nb.cells.append(nb.cells[idx])
            # Get next task
            next_task = shuffled_tasks.pop(0)
            original_order.append(grade_id(nb.cells[task[0]]))
            # Add cells of the next task
            permuted_nb.cells.extend([nb.cells[idx] for idx in next_task])
            # Set the cursor to the idx after the inserted task
            cursor = task[-1] + 1

        # Add remaining cells at the bottom of the notebook
        permuted_nb.cells.extend(
            [nb.cells[idx] for idx in range(cursor, len(nb.cells))]
        )
        # Save order
        permuted_nb.metadata["original_order"] = original_order

        return permuted_nb

    def preprocess(self, nb, resources):
        return self.permute(nb), resources
