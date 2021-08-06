import os
import nbformat
from textwrap import dedent
from .preprocessor import Preprocessor
from ...utils.nbgrader_cells import get_task_info, get_points


class AddTaskHeader(Preprocessor):

    def get_header(self, idx, points):
        header = nbformat.v4.new_markdown_cell()
        header.metadata['nbgrader'] = {
            'grade_id': 'taskheader_{}'.format(idx),
            'locked': True,
            'solution': False,
            'grade': False,
            'task': False,
            'schema_version': 3
        }
        header.source = dedent("""
        ---

        # Task {}

        **[{} Point(s)]**
        """.format(idx, points))
        return header

    def get_sub_header(self, idx, sub_idx, points):
        header = nbformat.v4.new_markdown_cell()
        header.metadata['nbgrader'] = {
            'grade_id': 'taskheader_{}_{}'.format(idx, sub_idx),
            'locked': True,
            'solution': False,
            'grade': False,
            'task': False,
            'schema_version': 3
        }
        header.source = dedent("""
        ## Task {}.{}

        **[{} Point(s)]**
        """.format(idx, sub_idx, points))
        return header

    def add_headers(self, nb, idx):
        total_points = sum([get_points(cell) for cell in nb.cells])
        task = get_task_info(nb)

        if len(task['subtasks']) < 1:
            return nb

        new_cells = []
        header = self.get_header(idx, total_points)
        new_cells.append(header)
        if 'header' in task:
            new_cells.append(nb.cells[task['header']])

        if len(task['subtasks']) == 1:
            new_cells.extend([nb.cells[i] for i in task['subtasks'][0]])
            if 'other' in task:
                new_cells.extend([nb.cells[i] for i in task['other']])
            nb.cells = new_cells
            return nb

        if len(task['subtasks']) > 1:
            for sub_idx, subtask in enumerate(task['subtasks']):
                points = sum([get_points(nb.cells[i]) for i in subtask])
                new_cells.append(self.get_sub_header(idx, sub_idx+1, points))
                new_cells.extend([nb.cells[i] for i in subtask])

        if 'other' in task:
            new_cells.extend([nb.cells[i] for i in task['other']])
        nb.cells = new_cells
        return nb

    def preprocess(self, resources):
        if not resources['exercise_options']['task-headers']:
            return
        idx = 0
        for task_dict in resources['tasks']:
            task = os.path.join(task_dict['pool'], task_dict['task'])
            task_path = os.path.join(
                resources['tmp_dir'],
                'tasks',
                task
            )
            notebooks = [file for file in os.listdir(task_path)
                         if file.endswith('.ipynb')]
            for nb_file in notebooks:
                idx += 1
                task_nb = nbformat.read(os.path.join(task_path, nb_file),
                                        as_version=4)
                task_nb = self.add_headers(task_nb, idx)
                nbformat.write(task_nb, os.path.join(task_path, nb_file))
