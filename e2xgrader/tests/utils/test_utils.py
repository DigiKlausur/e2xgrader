from tempfile import TemporaryDirectory
from nbgrader.coursedir import CourseDirectory

def createTempCourse():
    tmp_dir = TemporaryDirectory()
    coursedir = CourseDirectory()
    coursedir.root = tmp_dir.name
    return tmp_dir, coursedir