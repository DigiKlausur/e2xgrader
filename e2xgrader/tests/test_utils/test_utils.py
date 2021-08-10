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

def add_header_to_template(coursedir, path, header_source):
    presetmodel = PresetModel(coursedir)
    nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
    header_cells = presetmodel.get_template_preset('Header')
    header_cells[0].source = header_source
    nb.cells.extend(header_cells)
    nbformat.write(nb, path)
    return path

def add_footer_to_template(coursedir, path, footer_source):
    presetmodel = PresetModel(coursedir)
    nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
    footer_cells = presetmodel.get_template_preset('Footer')
    footer_cells[0].source = footer_source
    nb.cells.extend(footer_cells)
    nbformat.write(nb, path)
    return path
