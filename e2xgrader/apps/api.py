import os
from traitlets.config import Config
from nbgrader.apps.api import NbGraderAPI
from nbgrader.api import BaseCell, Grade, GradeCell, MissingEntry
from nbgrader.utils import as_timezone, to_numeric_tz, temp_attrs, capture_log
from nbgrader.converters import GenerateFeedback


class E2xAPI(NbGraderAPI):
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
            num_submissions = len(gb.notebook_submissions(notebook_id, assignment_id))
            notebook_id = gb.find_notebook(notebook_id, assignment_id).id

            for cell_name in (
                gb.db.query(BaseCell.name)
                .filter(BaseCell.type == "SolutionCell")
                .filter(BaseCell.notebook_id == notebook_id)
            ):

                solution_cell = {
                    "name": cell_name[0],
                    "avg_score": 0,
                    "max_score": 0,
                    "needs_manual_grade": 0,
                    "autograded": 0,
                }
                grade_ids = (
                    gb.db.query(BaseCell.id)
                    .filter(BaseCell.type == "GradeCell")
                    .filter(BaseCell.notebook_id == notebook_id)
                    .filter(BaseCell.name.contains(cell_name[0]))
                    .all()
                )
                if len(grade_ids) < 1:
                    continue

                if (
                    not gb.db.query(BaseCell.id)
                    .filter(BaseCell.type == "GradeCell")
                    .filter(BaseCell.notebook_id == notebook_id)
                    .filter(BaseCell.name == cell_name[0])
                    .first()
                ):
                    solution_cell["autograded"] = 1

                for grade_id in grade_ids:
                    solution_cell["max_score"] += (
                        gb.db.query(GradeCell.max_score)
                        .filter(GradeCell.id == grade_id[0])
                        .first()[0]
                    )
                    for manual_score, auto_score, needs_manual_grade in gb.db.query(
                        Grade.manual_score, Grade.auto_score, Grade.needs_manual_grade
                    ).filter(Grade.cell_id == grade_id[0]):
                        solution_cell["needs_manual_grade"] = max(
                            solution_cell["needs_manual_grade"], needs_manual_grade
                        )
                        if manual_score:
                            solution_cell["avg_score"] += manual_score
                        elif auto_score:
                            solution_cell["avg_score"] += auto_score
                if num_submissions > 0:
                    solution_cell["avg_score"] /= num_submissions

                solution_cells.append(solution_cell)
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
        with self.gradebook as gb:
            notebook_uid = gb.find_notebook(notebook_id, assignment_id).id
            manual = (
                gb.db.query(BaseCell.id)
                .filter(BaseCell.notebook_id == notebook_uid)
                .filter(BaseCell.type == "GradeCell")
                .filter(BaseCell.name == task_id)
                .first()
            )
            grade_ids = (
                gb.db.query(BaseCell.id)
                .filter(BaseCell.notebook_id == notebook_uid)
                .filter(BaseCell.type == "GradeCell")
                .filter(BaseCell.name.contains(task_id))
                .all()
            )

            submissions = []

            for idx, submitted_notebook in enumerate(
                gb.notebook_submissions(notebook_id, assignment_id)
            ):
                submission = {
                    "id": submitted_notebook.id,
                    "student": submitted_notebook.student.id,
                    "first_name": submitted_notebook.student.first_name,
                    "last_name": submitted_notebook.student.last_name,
                    "score": 0,
                    "max_score": 0,
                    "needs_manual_grade": 0,
                    "failed_tests": 0,
                    "index": idx,
                }
                for grade_id in grade_ids:
                    grade, max_score = (
                        gb.db.query(Grade, GradeCell.max_score)
                        .filter(Grade.notebook_id == submitted_notebook.id)
                        .filter(Grade.cell_id == grade_id[0])
                        .filter(GradeCell.id == grade_id[0])
                        .first()
                    )
                    submission["max_score"] += max_score
                    if grade.manual_score is not None:
                        submission["score"] += grade.manual_score
                    elif grade.auto_score is not None:
                        submission["score"] += grade.auto_score
                        if grade.auto_score < max_score and not manual:
                            submission["failed_tests"] = 1
                    submission["needs_manual_grade"] = max(
                        submission["needs_manual_grade"], grade.needs_manual_grade
                    )

                submissions.append(submission)

        submissions.sort(key=lambda x: x["id"])
        for idx, submission in enumerate(submissions):
            submission["index"] = idx

        return submissions

    def get_assignment(self, assignment_id, released=None):
        """Get information about an assignment given its name.
        Arguments
        ---------
        assignment_id: string
            The name of the assignment
        released: list
            (Optional) A set of names of released assignments, obtained via
            self.get_released_assignments().
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

    def generate_feedback(
        self, assignment_id, student_id=None, force=True, hidecells=False
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
        c.HTMLExporter.template_file = "feedback.tpl"
        c.FilterTests.hide_cells = hidecells
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
