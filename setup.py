#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setupbase import js_prerelease, discover_nbextensions


static_files = []
for (dirname, dirnames, filenames) in os.walk("e2xgrader/server_extensions/formgrader/static"):
    root = os.path.relpath(dirname, "e2xgrader/server_extensions/formgrader")
    for filename in filenames:
        static_files.append(os.path.join(root, filename))
for (dirname, dirnames, filenames) in os.walk("e2xgrader/server_extensions/formgrader/templates"):
    root = os.path.relpath(dirname, "e2xgrader/server_extensions/formgrader")
    for filename in filenames:
        static_files.append(os.path.join(root, filename))

base_static_files = []
for (dirname, dirnames, filenames) in os.walk("e2xgrader/server_extensions/e2xbase/static"):
    root = os.path.relpath(dirname, "e2xgrader/server_extensions/e2xbase")
    for filename in filenames:
        base_static_files.append(os.path.join(root, filename))

name = u'e2xgrader'

setup_args = dict(
    name=name,
    version='0.0.1',
    description='An addon for nbgrader',
    author='Tim Metzler',
    author_email='tim.metzler@h-brs.de',
    license='MIT',
    url='https://github.com/DigiKlausur/e2xgrader',
    keywords=['Notebooks', 'Grading', 'Homework'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    package_data={
        'e2xgrader': discover_nbextensions(name),
        'e2xgrader.server_extensions.formgrader': static_files,
        'e2xgrader.server_extensions.e2xbase': base_static_files,
    },
    entry_points={
        'console_scripts': ['e2xgrader=e2xgrader.apps.e2xgraderapp:main']
    },
    install_requires=[
        "jupyter",
        "notebook>=6.1.6",
        "nbconvert==5.6.1",
        "nbformat",
        "traitlets",
        "jupyter_core",
        "jupyter_client",
        "tornado",
        "requests",
        "beautifulsoup4",
        "pandas",
        "nbgrader",
    ],
    cmdclass={
        'build_py': js_prerelease(build_py),
    },
)

if __name__ == "__main__":
    setup(**setup_args)
