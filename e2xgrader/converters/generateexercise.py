import tempfile

from traitlets import List

from ..preprocessors.authoring import (
    AddTaskHeader,
    CopyFiles,
    CopyNotebooks,
    FillTemplate,
    GenerateTaskIDs,
    MakeExercise,
    RemoveExercise,
)
from .converter import Converter


class GenerateExercise(Converter):

    preprocessors = List(
        [
            RemoveExercise,
            CopyNotebooks,
            FillTemplate,
            CopyFiles,
            GenerateTaskIDs,
            AddTaskHeader,
            MakeExercise,
        ]
    )

    def __init__(self, coursedir, config=None):
        super(GenerateExercise, self).__init__(config=config)
        self.coursedir = coursedir

    def convert(self, resources):
        with tempfile.TemporaryDirectory() as tmp:
            resources["tmp_dir"] = tmp
            resources["course_prefix"] = self.coursedir.root
            resources["source_dir"] = self.coursedir.source_directory
            for preprocessor in self._preprocessors:
                preprocessor.preprocess(resources)
