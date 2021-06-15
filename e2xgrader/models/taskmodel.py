import os
import nbformat
import shutil
from textwrap import dedent
from .basemodel import BaseModel
from traitlets import Unicode


class TaskModel(BaseModel):

    directory = Unicode(
        'pools',
        help='The directory where the task pools go.'
    )

    def new_taskbook(self, name):
        nb = nbformat.v4.new_notebook()
        
        nb.metadata['nbassignment'] = {
            'type': 'task'
        }
        header = nbformat.v4.new_markdown_cell()
        
        header.source = dedent("""
        # {}
        
        Here you should give the general information about the task.
        
        Then add questions via the menu above.
        
        A task should be self contained.
        """.format(name))
        
        header.metadata['nbgrader'] = {
            'grade_id': '{}_Header'.format(name),
            'locked': True,
            'solution': False,
            'grade': False,
            'task': False,
            'schema_version': 3
        }
        
        nb.cells = [header]
        
        return nb

    def new(self, name, pool):
        base_path = os.path.join(self.base_path(), pool)
        os.makedirs(os.path.join(base_path, name, 'img'), exist_ok=True)
        os.makedirs(os.path.join(base_path, name, 'data'), exist_ok=True)
        filename = '{}.ipynb'.format(name)
        nb = self.new_taskbook(name)
        path = os.path.join(base_path, name, filename)
        nbformat.write(nb, path)
        return path

    def remove(self, name, pool):
        base_path = os.path.join(self.base_path(), pool)
        shutil.rmtree(os.path.join(base_path, name))
    
    def list(self, pool):
        base_path = os.path.join(self.base_path(), pool)
        taskfolders = os.listdir(base_path)
        tasks = []
        for taskfolder in taskfolders:
            if taskfolder.startswith('.'):
                continue
            points, questions = self.__get_task_info(taskfolder, pool)
            tasks.append({
                'name': taskfolder,
                'points': points,
                'questions': questions,
                'link': os.path.join('tree', base_path, taskfolder)
            })
        
        return tasks

    def __get_task_info(self, task, pool):
        base_path = os.path.join(self.base_path(), pool)
        notebooks = [file for file in os.listdir(os.path.join(base_path, task)) if file.endswith('.ipynb')]

        points = 0
        questions = 0

        for notebook in notebooks:
            nb = nbformat.read(os.path.join(base_path, task, notebook), as_version=4)
            for cell in nb.cells:
                if 'nbgrader' in cell.metadata and cell.metadata.nbgrader.grade:
                    points += cell.metadata.nbgrader.points
                    questions += 1
        return points, questions