import unittest

from tempfile import TemporaryDirectory
from nbgrader.coursedir import CourseDirectory


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.setUpResources()
        self.setUpCoursedir()

    def setUpResources(self):
        self.tmp_dir = TemporaryDirectory()
        self.resources = {
            'tmp_dir': self.tmp_dir.name,
            'source_dir': 'source'
        }

    def setUpCoursedir(self):
        self.course_tmp_dir = TemporaryDirectory()
        self.coursedir = CourseDirectory()
        self.coursedir.root = self.course_tmp_dir.name
        self.resources['course_prefix'] = self.coursedir.root

    def tearDown(self):
        # Remove temporary directories
        self.tmp_dir.cleanup()
        self.course_tmp_dir.cleanup()