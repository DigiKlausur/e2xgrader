import base64
import os
import statistics
from typing import Dict, List, Union

from nbgrader.api import MissingEntry
from nbgrader.apps.api import NbGraderAPI
from nbgrader.converters import GenerateFeedback
from nbgrader.utils import as_timezone, capture_log, temp_attrs, to_numeric_tz
from traitlets.config import Config


class E2xAPI(NbGraderAPI):
    def generate_feedback(
        self, assignment_id, student_id=None, force=True, hide_cells=False
    ):
        """Run ``nbgrader generate_feedback`` for a particular assignment and student.
        Arguments
        ---------
        assignment_id: string
            The name of the assignment
        student_id: string
            The name of the student (optional). If not provided, then generate
            feedback from autograded submissions.
        force: bool
            Whether to force generating feedback, even if it already exists.
        Returns
        -------
        result: dict
            A dictionary with the following keys (error and log may or may not be present):
            - success (bool): whether or not the operation completed successfully
            - error (string): formatted traceback
            - log (string): captured log output
        """
        # Because we may be using HTMLExporter.template_file in other
        # parts of the the UI, we need to make sure that the template
        # is explicitply 'feedback.tpl` here:
        c = Config()
        c.HTMLExporter.template_name = "feedback"
        c.FilterTests.hide_cells = hide_cells
        if student_id is not None:
            with temp_attrs(
                self.coursedir, assignment_id=assignment_id, student_id=student_id
            ):
                app = GenerateFeedback(coursedir=self.coursedir, parent=self)
                app.update_config(c)
                app.force = force
                return capture_log(app)
        else:
            with temp_attrs(self.coursedir, assignment_id=assignment_id):
                app = GenerateFeedback(coursedir=self.coursedir, parent=self)
                app.update_config(c)
                app.force = force
                return capture_log(app)

    def get_solution_cell_ids(self, assignment_id, notebook_id):
        """Get information about the solution cells of a notebook
        given its name.

        Arguments
        ---------
        assignment_id: string
            The name of the assignment
        notebook_id: string
            The name of the notebook

        Returns
        -------
        solution_cells: dict
            A dictionary containing information about the solution cells

        """
        solution_cells = []
        with self.gradebook as gb:
            notebook = gb.find_notebook(name=notebook_id, assignment=assignment_id)
            grades = {cell.name: cell for cell in notebook.grade_cells}

            solution_cells = []
            for cell in notebook.solution_cells:
                if cell.name in grades:
                    grade = grades[cell.name]
                    del grades[cell.name]
                else:
                    for name in grades:
                        if cell.name in name:
                            grade = grades[name]
                            del grades[name]
                            break
                solution_cells.append(
                    dict(
                        name=cell.name,
                        avg_score=statistics.mean(
                            [grade.score for grade in grade.grades]
                        ),
                        max_score=grade.max_score,
                        needs_manual_grade=int(
                            any([grade.needs_manual_grade for grade in grade.grades])
                        ),
                        autograded=int(grade.name != cell.name),
                    )
                )

        return solution_cells

    def get_task_submissions(self, assignment_id, notebook_id, task_id):
        """Get a list of submissions for a particular notebook in an assignment.

        Arguments
        ---------
        assignment_id: string
            The name of the assignment
        notebook_id: string
            The name of the notebook
        task_id: string
            The name of the solution cell

        Returns
        -------
        submissions: list
            A list of dictionaries containing information about each submission.

        """
        submissions = []
        with self.gradebook as gb:
            notebook = gb.find_notebook(notebook_id, assignment_id)
            student_idx = {
                submission.student.id: submission.id
                for submission in gb.notebook_submissions(
                    notebook=notebook_id, assignment=assignment_id
                )
            }

            grades = {cell.name: cell for cell in notebook.grade_cells}

            if task_id in grades:
                grade_cell = grades[task_id]
            else:
                for name in grades:
                    if task_id in name:
                        grade_cell = grades[name]
                        break

            for grade in grade_cell.grades:
                submissions.append(
                    dict(
                        id=student_idx[grade.student.id],
                        student=grade.student.id,
                        first_name=grade.student.first_name,
                        last_name=grade.student.last_name,
                        score=grade.score,
                        max_score=grade.max_score,
                        needs_manual_grade=grade.needs_manual_grade,
                        failed_tests=grade.failed_tests,
                    )
                )

        submissions.sort(key=lambda x: x["id"])
        for idx, submission in enumerate(submissions):
            submission["index"] = idx
        return submissions

    def get_assignment(self, assignment_id, released=None, include_score=True):
        """Get information about an assignment given its name.
        Arguments
        ---------
        assignment_id: string
            The name of the assignment
        released: list
            (Optional) A set of names of released assignments, obtained via
            self.get_released_assignments().
        include_score: bool
            (Optional) If the score of the assignment should be included
        Returns
        -------
        assignment: dict
            A dictionary containing information about the assignment
        """
        # get the set of released assignments if not given
        if not released:
            released = self.get_released_assignments()

        # check whether there is a source version of the assignment
        sourcedir = os.path.abspath(
            self.coursedir.format_path(
                self.coursedir.source_directory,
                student_id=".",
                assignment_id=assignment_id,
            )
        )
        if not os.path.isdir(sourcedir):
            return

        # see if there is information about the assignment in the database
        try:
            with self.gradebook as gb:
                db_assignment = gb.find_assignment(assignment_id)
                assignment = db_assignment.to_dict()
                if db_assignment.duedate:
                    ts = as_timezone(db_assignment.duedate, self.timezone)
                    assignment["display_duedate"] = ts.strftime(self.timestamp_format)
                    assignment["duedate_notimezone"] = ts.replace(
                        tzinfo=None
                    ).isoformat()
                else:
                    assignment["display_duedate"] = None
                    assignment["duedate_notimezone"] = None
                assignment["duedate_timezone"] = to_numeric_tz(self.timezone)

                if include_score:
                    assignment["average_code_score"] = gb.average_assignment_code_score(
                        assignment_id
                    )
                    assignment[
                        "average_written_score"
                    ] = gb.average_assignment_written_score(assignment_id)
                    assignment["average_task_score"] = gb.average_assignment_task_score(
                        assignment_id
                    )
                    assignment["average_score"] = (
                        assignment["average_code_score"]
                        + assignment["average_written_score"]
                        + assignment["average_task_score"]
                    )
                else:
                    assignment["average_code_score"] = None
                    assignment["average_written_score"] = None
                    assignment["average_score"] = None

        except MissingEntry:
            assignment = {
                "id": None,
                "name": assignment_id,
                "duedate": None,
                "display_duedate": None,
                "duedate_notimezone": None,
                "duedate_timezone": to_numeric_tz(self.timezone),
                "average_score": 0,
                "average_code_score": 0,
                "average_written_score": 0,
                "average_task_score": 0,
                "max_score": 0,
                "max_code_score": 0,
                "max_written_score": 0,
                "max_task_score": 0,
            }

        # get released status
        if not self.exchange_is_functional:
            assignment["releaseable"] = False
            assignment["status"] = "draft"
        else:
            assignment["releaseable"] = True
            if assignment_id in released:
                assignment["status"] = "released"
            else:
                assignment["status"] = "draft"

        # get source directory
        assignment["source_path"] = os.path.relpath(sourcedir, self.coursedir.root)

        # get release directory
        releasedir = os.path.abspath(
            self.coursedir.format_path(
                self.coursedir.release_directory,
                student_id=".",
                assignment_id=assignment_id,
            )
        )
        if os.path.exists(releasedir):
            assignment["release_path"] = os.path.relpath(
                releasedir, self.coursedir.root
            )
        else:
            assignment["release_path"] = None

        # number of submissions
        assignment["num_submissions"] = len(self.get_submitted_students(assignment_id))

        return assignment

    def get_assignments(self, include_score=True):
        """Get list of information about all assignments

        Arguments
        ---------
            include_score: bool
                (Optional) If the score of the assignment should be included. Defaults to True
        Returns
        -------
        assignments: list
            A list of dictionaries containing information about each assignment

        """
        released = self.get_released_assignments()

        assignments = []
        for x in self.get_source_assignments():
            assignments.append(
                self.get_assignment(x, released=released, include_score=include_score)
            )

        assignments.sort(
            key=lambda x: (
                x["duedate"] if x["duedate"] is not None else "None",
                x["name"],
            )
        )
        return assignments

    def get_annotations(self, submission_id: str) -> Union[List[Dict[str, str]], None]:
        """Get all annotations associated with a submission

        Args:
            submission_id (str): submission id

        Returns:
            Union[List[Dict[str, str]], None]: A list of solution cell dictionaries or None
                                               Each dictionary contains the submission id
                                               and annotation as a base64 encoded string
        """
        try:
            notebook = self.gradebook.find_submission_notebook_by_id(submission_id)
        except MissingEntry:
            return

        autograded_path = self.coursedir.format_path(
            nbgrader_step=self.coursedir.autograded_directory,
            student_id=notebook.student.id,
            assignment_id=notebook.assignment.name,
        )
        annotation_path = os.path.join(autograded_path, "annotations")
        solution_cells = [cell.to_dict() for cell in notebook.notebook.solution_cells]
        for solution_cell in solution_cells:
            solution_cell["submission_id"] = submission_id
            # Try loading the annotation for that cell
            try:
                with open(
                    os.path.join(annotation_path, f'{solution_cell["name"]}.png'), "rb"
                ) as f:
                    solution_cell["annotation"] = str(base64.b64encode(f.read()))[2:-1]
            except FileNotFoundError:
                solution_cell["annotation"] = None
        return solution_cells

    def save_annotation(
        self, submission_id: str, name: str, annotation: str
    ) -> Union[Dict[str, str], None]:
        """Save an annotation for a cell

        Args:
            submission_id (str): submission id
            name (str): name of the solution cell
            annotation (str): base64 encoded image

        Returns:
            Union[Dict[str, str], None]: A dictionary containing the cell information or None
        """
        try:
            notebook = self.gradebook.find_submission_notebook_by_id(submission_id)
        except MissingEntry:
            return

        autograded_path = self.coursedir.format_path(
            nbgrader_step=self.coursedir.autograded_directory,
            student_id=notebook.student.id,
            assignment_id=notebook.assignment.name,
        )
        annotation_path = os.path.join(autograded_path, "annotations")
        os.makedirs(annotation_path, exist_ok=True)
        with open(os.path.join(annotation_path, f"{name}.png"), "wb") as f:
            f.write(base64.b64decode(annotation[22:]))
        return dict(
            id=submission_id,
            name=name,
            annotation=annotation,
            notebook=notebook.notebook.name,
            assignment=notebook.assignment.name,
        )
