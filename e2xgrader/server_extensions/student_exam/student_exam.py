from ..student.student import StudentExtension


class StudentExamExtension(StudentExtension):
    pass


def load_jupyter_server_extension(nbapp):
    """Load the e2xgrader serverextension"""
    nbapp.log.info("Loading the e2xgrader student exam serverextension")
    StudentExamExtension(parent=nbapp)
