import os
import nbformat
import shutil
from textwrap import dedent
from .basemodel import BaseModel
from traitlets import Unicode


class TaskModel(BaseModel):

    directory = Unicode("pools", help="The directory where the task pools go.")

    def new_taskbook(self, name):
        nb = nbformat.v4.new_notebook()

        nb.metadata["nbassignment"] = {"type": "task"}
        header = nbformat.v4.new_markdown_cell()

        header.source = dedent(
            """
        # {}

        Here you should give the general information about the task.

        Then add questions via the menu above.

        A task should be self contained.
        """.format(
                name
            )
        )

        header.metadata["nbgrader"] = {
            "grade_id": "{}_Header".format(name),
            "locked": True,
            "solution": False,
            "grade": False,
            "task": False,
            "schema_version": 3,
        }

        nb.cells = [header]

        return nb

    def new(self, **kwargs):
        name = kwargs["name"]
        pool = kwargs["pool"]
        if self.is_valid_name(name):
            path = os.path.join(self.base_path(), pool, name)
            if os.path.exists(path):
                return {
                    "success": False,
                    "error": f"A task with the name {name} already exists!",
                }
            else:
                base_path = os.path.join(self.base_path(), pool)
                os.makedirs(os.path.join(base_path, name, "img"), exist_ok=True)
                os.makedirs(os.path.join(base_path, name, "data"), exist_ok=True)
                filename = "{}.ipynb".format(name)
                nb = self.new_taskbook(name)
                path = os.path.join(base_path, name, filename)
                nbformat.write(nb, path)
                return {"success": True, "path": os.path.join("notebooks", path)}
        else:
            return {"success": False, "error": "Invalid name"}

    def remove(self, **kwargs):
        name = kwargs["name"]
        pool = kwargs["pool"]
        base_path = os.path.join(self.base_path(), pool)
        shutil.rmtree(os.path.join(base_path, name))

    def get(self, **kwargs):
        name = kwargs["name"]
        pool = kwargs["pool"]
        points, questions = self.__get_task_info(name, pool)
        return {
            "name": name,
            "points": points,
            "questions": questions,
            "pool": pool,
        }

    def list(self, **kwargs):
        pool = kwargs["pool"]
        base_path = os.path.join(self.base_path(), pool)
        if not os.path.exists(base_path):
            return []
        taskfolders = os.listdir(base_path)
        tasks = []
        for taskfolder in taskfolders:
            if taskfolder.startswith("."):
                continue
            points, questions = self.__get_task_info(taskfolder, pool)
            tasks.append(
                {
                    "name": taskfolder,
                    "points": points,
                    "questions": questions,
                    "pool": pool,
                    "link": os.path.join("tree", base_path, taskfolder),
                }
            )

        return tasks

    def __get_task_info(self, task, pool):
        base_path = os.path.join(self.base_path(), pool)
        notebooks = [
            file
            for file in os.listdir(os.path.join(base_path, task))
            if file.endswith(".ipynb")
        ]

        points = 0
        questions = 0

        for notebook in notebooks:
            nb = nbformat.read(os.path.join(base_path, task, notebook), as_version=4)
            for cell in nb.cells:
                if "nbgrader" in cell.metadata and cell.metadata.nbgrader.grade:
                    points += cell.metadata.nbgrader.points
                    questions += 1
        return points, questions
