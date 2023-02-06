import glob
import os
import shutil

from traitlets import Unicode

from .basemodel import BaseModel


class ExerciseModel(BaseModel):
    directory = Unicode("source", help="The directory where assignments go.")

    def get(self, **kwargs):
        return {"name": kwargs["name"], "assignment": kwargs["assignment"]}

    def remove(self, **kwargs):
        assignment = kwargs["assignment"]
        name = kwargs["name"]
        base_path = os.path.join(self.base_path(), assignment)
        exercise_files = os.path.join(base_path, "{}_files".format(name))
        if os.path.exists(exercise_files):
            shutil.rmtree(exercise_files)
        exercise = os.path.join(base_path, "{}.ipynb".format(name))
        if os.path.exists(exercise):
            os.remove(exercise)

    def list(self, **kwargs):
        assignment = kwargs["assignment"]
        base_path = os.path.join(self.base_path(), assignment)
        exercisenbs = glob.glob(os.path.join(base_path, "*.ipynb"))
        exercises = []
        for exercisenb in exercisenbs:
            name = os.path.split(exercisenb)[-1].replace(".ipynb", "")
            exercises.append(
                {
                    "name": name,
                    "assignment": assignment,
                    "link": os.path.join(
                        "taskcreator", "assignments", assignment, name
                    ),
                }
            )

        return exercises
