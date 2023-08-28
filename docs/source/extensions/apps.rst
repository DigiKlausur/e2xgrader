Adding Custom Web Apps
======================

To extend **e2xgrader** you can add custom server apps to it.
A custom server app can add templates, handlers and change the tornado settings of the jupyter server.

Different apps are activated in different modes. You can configure which apps should be activated in each mode via the `TeacherExtension`, `StudentExtension` and `StudentExamExtension` traits.

Creating a Simple App
---------------------

To create an app, you need to install `e2xcore` and extend the `BaseApp` class.
As an example we will build a simple app that converts student score into letter grades.

.. code-block:: python

    # File score2grade.py

    from e2xcore import BaseApp
    from nbgrader.apps.baseapp import NbGrader

    from traitlets import Dict, Unicode


    class Score2Grade(NbGrader, BaseApp):
        grading_sheme = Dict(
            key_trait=Unicode(),

        )


