import os
import shutil
from .preprocessor import Preprocessor


class RemoveExercise(Preprocessor):
    def preprocess(self, resources):
        base_path = os.path.join(
            resources["course_prefix"], resources["source_dir"], resources["assignment"]
        )
        exercise_files = os.path.join(
            base_path, "{}_files".format(resources["exercise"])
        )
        if os.path.exists(exercise_files):
            shutil.rmtree(exercise_files)
        exercise_nb = os.path.join(base_path, "{}.ipynb".format(resources["exercise"]))
        if os.path.exists(exercise_nb):
            os.remove(exercise_nb)
