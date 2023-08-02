import typing
from collections import defaultdict
from textwrap import dedent

import pandas as pd
from e2xcore.api import E2xAPI
from e2xcore.utils.utils import get_nbgrader_config
from nbgrader.api import Grade
from traitlets import Bool, List, Unicode
from traitlets.config import LoggingConfigurable


class GradeExporter(LoggingConfigurable):
    assignments = List(
        trait=Unicode(),
        default_value=[],
        help="The assignments for which grades should be exported",
    )

    tasks = Bool(
        default_value=False,
        help="Whether to include scores per cell or not. Defaults to False.",
    )

    notebooks = Bool(
        default_value=True,
        help=dedent(
            """
            Whether to include scores per notebook or not. 
            Can only be False if tasks is False. Defaults to True.
        """
        ),
    )

    include_max_score = Bool(
        default_value=False,
        help=dedent(
            """
            Whether to include a row with the maximum score or not.
            If True a row named "max_score" will be added. Defaults to False.
        """
        ),
    )

    normalize = Bool(
        default_value=False,
        help=dedent(
            """
            Whether to divide all scores by the maximum score or not.
            Defaults to False.
        """
        ),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = E2xAPI(config=get_nbgrader_config())

    def get_assignment_ids(self) -> typing.List[str]:
        if len(self.assignments) > 0:
            return self.assignments
        else:
            return [
                assignment["name"]
                for assignment in self.api.get_assignments(include_score=False)
            ]

    def get_grades(self) -> pd.DataFrame:
        data = defaultdict(lambda: defaultdict(float))
        assignments = self.get_assignment_ids()
        for assignment_id in assignments:
            for notebook in self.api.get_notebooks(assignment_id):
                notebook_id = notebook["name"]
                # Get the maximum score
                if self.include_max_score or self.normalize:
                    for key, value in self.max_score(assignment_id, notebook).items():
                        data[key].update(value)
                for submission in self.api.get_notebook_submissions(
                    assignment_id=assignment_id, notebook_id=notebook_id
                ):
                    if self.tasks:
                        grades = self.task_grades(assignment_id, submission)
                        for key, value in grades.items():
                            data[key].update(value)
                    elif self.notebooks:
                        data[(assignment_id, notebook_id)][
                            submission["student"]
                        ] = submission["score"]
                    else:
                        data[assignment_id][submission["student"]] += submission[
                            "score"
                        ]
        grades = pd.DataFrame.from_dict(data, orient="index").T
        if self.normalize:
            grades = grades.div(grades.loc["max_score"]).drop("max_score")
        return grades[sorted(grades.columns)]

    def max_score(
        self, assignment_id: str, notebook: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Dict[str, float]]:
        data = defaultdict(dict)
        assignment = self.api.get_assignment(assignment_id, include_score=False)
        if assignment["num_submissions"] < 1 or notebook["max_score"] == 0:
            return data
        if self.tasks:
            with self.api.gradebook as gb:
                for grade in gb.find_notebook(
                    name=notebook["name"], assignment=assignment_id
                ).grade_cells:
                    grade_id = self.normalize_grade_id(grade)
                    data[(assignment_id, notebook["name"], grade_id)][
                        "max_score"
                    ] = grade.max_score
        elif self.notebooks:
            data[(assignment_id, notebook["name"])]["max_score"] = notebook["max_score"]
        else:
            data[assignment_id]["max_score"] = self.api.get_assignment(
                assignment_id, include_score=False
            )["max_score"]
        return data

    def task_grades(
        self, assignment_id: str, submission: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Dict[str, float]]:
        data = defaultdict(dict)
        with self.api.gradebook as gb:
            nb = gb.find_submission_notebook_by_id(submission["id"])
            for grade in nb.grades:
                grade_id = self.normalize_grade_id(grade)
                data[(assignment_id, submission["name"], grade_id)][
                    submission["student"]
                ] = grade.score
        return data

    def normalize_grade_id(self, grade: Grade) -> str:
        return grade.name[5:] if grade.name.startswith("test_") else grade.name
