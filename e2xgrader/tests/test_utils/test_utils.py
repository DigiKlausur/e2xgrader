import nbformat
from tempfile import TemporaryDirectory
from nbgrader.coursedir import CourseDirectory

from e2xgrader.models import TemplateModel, PresetModel


def createTempCourse():
    tmp_dir = TemporaryDirectory()
    coursedir = CourseDirectory()
    coursedir.root = tmp_dir.name
    return tmp_dir, coursedir

def add_template_with_header(coursedir, name, header_source):
    templatemodel = TemplateModel(coursedir)
    presetmodel = PresetModel(coursedir)
    res = templatemodel.new(name=name)
    
    nb = nbformat.read(res['path'], as_version=nbformat.NO_CONVERT)
    header_cells = presetmodel.get_template_preset('Header')
    header_cells[0].source = header_source
    nb.cells = header_cells
    nbformat.write(nb, res['path'])
    return res['path']
