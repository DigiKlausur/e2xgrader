# e2xgrader

[![PyPi](https://img.shields.io/pypi/v/e2xgrader)](https://pypi.org/project/e2xgrader)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=DigiKlausur_e2xgrader&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=DigiKlausur_e2xgrader)
[![Docs](https://img.shields.io/readthedocs/e2xgrader)](https://e2xgrader.readthedocs.io)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

e2xgrader is an add-on for nbgrader that adds functionality for teachers and students.
e2xgrader introduces new cell types and tools for graders (per question grading view, authoring component, pen-based grading) and students (assignment toolbar, exam toolbar, restricted notebook extension).
Please refer to the [documentation](https://e2xgrader.readthedocs.io) for further information.

_Currently e2xgrader works with notebook<7 or nbclassic. We are working on porting the notebook extension to lab extensions_

## Screenshots

A multiple choice cell:
![multiplechoice](docs/source/user_docs/cells/img/mc_render.png)
<br/>

An annotated student answer:
![annotation](docs/source/user_docs/img/annotate_answer.png)
<br/>

A per question grading view for teachers:
![task_view](docs/source/user_docs/img/task_view.png)
<br/>

A help extension to make docs and other files available to students:
![help_extension](docs/source/user_docs/img/help_tab.png)
<br/>

An assignment toolbar for students:
![assignment_toolbar](docs/source/user_docs/img/assignment_toolbar_md.png)
<br/>

An exam toolbar for students:
![exam_toolbar](docs/source/user_docs/img/exam_toolbar.png)
<br/>

## JupyterCon 2023 Talk

[![e2xgrader: An Add on for Improved Grading and Teaching with Jupyter Notebooks at Scale | JupyterCon 2023](https://img.youtube.com/vi/fc3Tvr_jm3w/hqdefault.jpg)](https://www.youtube.com/watch?v=fc3Tvr_jm3w "e2xgrader: An Add on for Improved Grading and Teaching with Jupyter Notebooks at Scale | JupyterCon 2023")

## Install

To install e2xgrader, execute:

```bash
pip install e2xgrader
```

## Change Mode

e2xgrader comes in three different modes, `teacher`, `student` and `student_exam`.
You can switch between them:

```bash
e2xgrader activate teacher --sys-prefix
e2xgrader activate student --sys-prefix
e2xgrader activate student_exam --sys-prefix
```

## Uninstall

To uninstall, execute:

```bash
e2xgrader deactivate --sys-prefix
pip uninstall e2xgrader
```
