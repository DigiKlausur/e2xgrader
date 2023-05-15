import glob
import hashlib
import os
import re

from nbgrader.exchange.default import ExchangeList
from nbgrader.utils import make_unique_key, notebook_hash

from .exchange import E2xExchange


def _checksum(path):
    m = hashlib.md5()
    m.update(open(path, "rb").read())
    return m.hexdigest()


def _get_key(info):
    return info["course_id"], info["student_id"], info["assignment_id"]


def _match_key(info, key):
    return (
        info["course_id"] == key[0]
        and info["student_id"] == key[1]
        and info["assignment_id"] == key[2]
    )


class E2xExchangeList(E2xExchange, ExchangeList):
    def init_dest(self):
        course_id = self.coursedir.course_id if self.coursedir.course_id else "*"
        assignment_id = (
            self.coursedir.assignment_id if self.coursedir.assignment_id else "*"
        )
        student_id = self.coursedir.student_id if self.coursedir.student_id else "*"

        if self.inbound:
            pattern = os.path.join(
                self.root,
                course_id,
                self.inbound_directory,
                "{}+{}+*".format(student_id, assignment_id),
            )
        elif self.cached:
            pattern = os.path.join(
                self.cache, course_id, "{}+{}+*".format(student_id, assignment_id)
            )
        else:
            if self.personalized_outbound:
                # list all assignments here
                pattern = os.path.join(
                    self.root,
                    course_id,
                    self.outbound_directory,
                    student_id,
                    "{}".format(assignment_id),
                )
            else:
                pattern = os.path.join(
                    self.root,
                    course_id,
                    self.outbound_directory,
                    "{}".format(assignment_id),
                )

        self.assignments = sorted(glob.glob(pattern))

    def parse_assignment(self, assignment):
        course_id = r".*/(?P<course_id>.*)/"
        if self.inbound:
            regexp = (
                course_id
                + self.inbound_directory
                + r"/(?P<student_id>[^+]*)\+"
                + r"(?P<assignment_id>[^+]*)\+"
                + r"(?P<timestamp>[^+]*)"
                + r"(?P<random_string>\+.*)?"
            )
        elif self.cached:
            regexp = (
                course_id
                + r"(?P<student_id>.*)\+"
                + r"(?P<assignment_id>.*)\+"
                + r"(?P<timestamp>.*)"
            )
        else:
            if self.personalized_outbound:
                regexp = (
                    course_id
                    + self.outbound_directory
                    + r"/(?P<student_id>.*)"
                    + r"/(?P<assignment_id>.*)"
                )
            else:
                regexp = course_id + self.outbound_directory + r"/(?P<assignment_id>.*)"

        m = re.match(regexp, assignment)
        if m is None:
            raise RuntimeError(
                "Could not match '%s' with regexp '%s'", assignment, regexp
            )

        return m.groupdict()

    def parse_assignments(self):
        if self.coursedir.student_id:
            courses = self.authenticator.get_student_courses(self.coursedir.student_id)
        else:
            courses = None

        assignments = []
        released_assignments = []
        for path in self.assignments:
            info = self.parse_assignment(path)
            # if grader and the assignment is already known as released assignment, skip looking
            if (
                self.personalized_outbound
                and self.grader
                and info["assignment_id"] in released_assignments
            ):
                self.log.debug(
                    "Grader role and personalized-outbound are enabled, "
                    "and the assignment is known to be released already"
                )
                continue

            if courses is not None and info["course_id"] not in courses:
                continue

            if self.path_includes_course:
                assignment_dir = os.path.join(
                    self.assignment_dir, info["course_id"], info["assignment_id"]
                )
            else:
                assignment_dir = os.path.join(
                    self.assignment_dir, info["assignment_id"]
                )

            if self.inbound or self.cached:
                info["status"] = "submitted"
                info["path"] = path
            elif os.path.exists(assignment_dir):
                info["status"] = "fetched"
                info["path"] = os.path.abspath(assignment_dir)
            else:
                info["status"] = "released"
                info["path"] = path
                # update released assignments
                if self.personalized_outbound and self.grader:
                    released_assignments.append(info["assignment_id"])

            if self.remove:
                info["status"] = "removed"

            notebooks = sorted(glob.glob(os.path.join(info["path"], "*.ipynb")))
            if not notebooks:
                self.log.warning("No notebooks found in {}".format(info["path"]))

            info["notebooks"] = []
            for notebook in notebooks:
                nb_info = {
                    "notebook_id": os.path.splitext(os.path.split(notebook)[1])[0],
                    "path": os.path.abspath(notebook),
                }
                if info["status"] != "submitted":
                    info["notebooks"].append(nb_info)
                    continue

                nb_info["has_local_feedback"] = False
                nb_info["has_exchange_feedback"] = False
                nb_info["local_feedback_path"] = None
                nb_info["feedback_updated"] = False

                # Check whether feedback has been fetched already.
                local_feedback_dir = os.path.join(
                    assignment_dir, "feedback", info["timestamp"]
                )
                local_feedback_path = os.path.join(
                    local_feedback_dir, "{0}.html".format(nb_info["notebook_id"])
                )
                has_local_feedback = os.path.isfile(local_feedback_path)
                if has_local_feedback:
                    local_feedback_checksum = _checksum(local_feedback_path)
                else:
                    local_feedback_checksum = None

                # Also look to see if there is feedback available to fetch.
                # and check whether personalized-feedback is enabled
                if self.personalized_feedback:
                    exchange_feedback_path = os.path.join(
                        self.root,
                        info["course_id"],
                        self.feedback_directory,
                        info["student_id"],
                        info["assignment_id"],
                        "{0}.html".format(nb_info["notebook_id"]),
                    )
                else:
                    unique_key = make_unique_key(
                        info["course_id"],
                        info["assignment_id"],
                        nb_info["notebook_id"],
                        info["student_id"],
                        info["timestamp"],
                    )
                    self.log.debug("Unique key is: {}".format(unique_key))
                    nb_hash = notebook_hash(notebook, unique_key)
                    exchange_feedback_path = os.path.join(
                        self.root,
                        info["course_id"],
                        self.feedback_directory,
                        "{0}.html".format(nb_hash),
                    )

                has_exchange_feedback = os.path.isfile(exchange_feedback_path)
                if not has_exchange_feedback:
                    # Try looking for legacy feedback.
                    nb_hash = notebook_hash(notebook)
                    exchange_feedback_path = os.path.join(
                        self.root,
                        info["course_id"],
                        "feedback",
                        "{0}.html".format(nb_hash),
                    )
                    has_exchange_feedback = os.path.isfile(exchange_feedback_path)
                if has_exchange_feedback:
                    exchange_feedback_checksum = _checksum(exchange_feedback_path)
                else:
                    exchange_feedback_checksum = None

                nb_info["has_local_feedback"] = has_local_feedback
                nb_info["has_exchange_feedback"] = has_exchange_feedback
                if has_local_feedback:
                    nb_info["local_feedback_path"] = local_feedback_path
                if has_local_feedback and has_exchange_feedback:
                    nb_info["feedback_updated"] = (
                        exchange_feedback_checksum != local_feedback_checksum
                    )
                info["notebooks"].append(nb_info)

            if info["status"] == "submitted":
                if info["notebooks"]:
                    # List feedback if there exists for one of the notebooks files in path
                    has_local_feedback = any(
                        [nb["has_local_feedback"] for nb in info["notebooks"]]
                    )
                    has_exchange_feedback = any(
                        [nb["has_exchange_feedback"] for nb in info["notebooks"]]
                    )
                    feedback_updated = any(
                        [nb["feedback_updated"] for nb in info["notebooks"]]
                    )
                else:
                    has_local_feedback = False
                    has_exchange_feedback = False
                    feedback_updated = False

                info["has_local_feedback"] = has_local_feedback
                info["has_exchange_feedback"] = has_exchange_feedback
                info["feedback_updated"] = feedback_updated
                if has_local_feedback:
                    info["local_feedback_path"] = os.path.join(
                        assignment_dir, "feedback", info["timestamp"]
                    )
                else:
                    info["local_feedback_path"] = None

            assignments.append(info)

        # partition the assignments into groups for course/student/assignment
        if self.inbound or self.cached:
            assignment_keys = sorted(
                list(set([_get_key(info) for info in assignments]))
            )
            assignment_submissions = []
            for key in assignment_keys:
                submissions = [x for x in assignments if _match_key(x, key)]
                submissions = sorted(submissions, key=lambda x: x["timestamp"])
                info = {
                    "course_id": key[0],
                    "student_id": key[1],
                    "assignment_id": key[2],
                    "status": submissions[0]["status"],
                    "submissions": submissions,
                }
                assignment_submissions.append(info)
            assignments = assignment_submissions

        return assignments
