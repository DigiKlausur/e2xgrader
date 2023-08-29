from e2xcore.utils.nbgrader_cells import get_tasks, grade_id
from nbformat.v4 import new_notebook
from nbgrader.preprocessors import NbGraderPreprocessor


class UnpermuteTasks(NbGraderPreprocessor):
    def unpermute(self, nb):
        unpermuted_nb = new_notebook()
        # Get original order
        original_order = nb.metadata.original_order
        # Get indices of tasks
        tasks = get_tasks(nb)

        cursor = 0

        for task in tasks:
            # Add all cells between cursor and current task
            for idx in range(cursor, task[0]):
                unpermuted_nb.cells.append(nb.cells[idx])
            # Get name and cells of next task in the original order
            next_task_id = original_order.pop(0)
            next_task = [
                task for task in tasks if grade_id(nb.cells[task[0]]) == next_task_id
            ][0]
            # Add cells of the next task
            unpermuted_nb.cells.extend([nb.cells[idx] for idx in next_task])
            # Set the cursor to the idx after the inserted task
            cursor = task[-1] + 1

        # Add remaining cells at the bottom of the notebook
        unpermuted_nb.cells.extend(
            [nb.cells[idx] for idx in range(cursor, len(nb.cells))]
        )

        return unpermuted_nb

    def preprocess(self, nb, resources):
        if "original_order" not in nb.metadata:
            return nb, resources

        perm = nb.metadata.permutation
        keys = sorted(range(len(perm)), key=perm.__getitem__)
        reorder_cells = [nb.cells[i] for i in keys]
        nb.cells = reorder_cells
        return nb, resources
