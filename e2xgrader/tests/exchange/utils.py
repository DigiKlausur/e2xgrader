from nbgrader.coursedir import CourseDirectory


def create_course_dir(
    root: str,
    course_id: str = "testcourse",
    assignment_id: str = "assignment1",
    student_id: str = "*",
) -> CourseDirectory:
    """
    Create a CourseDirectory object with the specified parameters.

    Args:
        root (str): The root directory of the course.
        course_id (str): The ID of the course.
        assignment_id (str): The ID of the assignment.
        student_id (str, optional): The ID of the student. Defaults to "".

    Returns:
        CourseDirectory: The created CourseDirectory object.
    """
    coursedir = CourseDirectory()
    coursedir.root = root
    coursedir.course_id = course_id
    coursedir.assignment_id = assignment_id
    coursedir.student_id = student_id
    return coursedir
