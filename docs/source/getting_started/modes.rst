.. _e2xgrader_modes:

==========================
Activating Different Modes
==========================

e2xgrader comes with 3 modes.

To activate a mode use the e2xgrader CLI, where `<mode>` is the mode you want to activate:

.. code-block:: sh

   e2xgrader activate <mode> --sys-prefix

To deactivate all e2xgrader modes:

.. code-block:: sh

   e2xgrader deactivate --sys-prefix

Teacher Mode
------------

In teacher mode the `formgrader` interface is available. Custom cells and authoring tools are activated, too.

Activate Teacher Mode
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   e2xgrader activate teacher --sys-prefix

Don't forget to edit your `nbgrader_config.py` afterwards (see :ref:`configure_e2xgrader`).

Student Assignment Mode
-----------------------

Activate Student Assignment Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In student mode the `assignmentlist` extension is activated. Custom cells are activated to.
Additionally a toolbar is added for students that indicates which cells are solution cells and should be edited by the student.
Copying, pasting and deleting of nbgrader cells is deactivated.

.. code-block:: sh

   e2xgrader activate student --sys-prefix

Student Exam Mode
-----------------

In student exam mode all extensions from the student assignment mode are activated.
Additionally the notebook interface is restricted. The shutdown button is removed to prevent students from accidentally shutting down their server.
Students can not create or delete notebooks via the notebook interface.
Shortcuts to change cell types, insert or delete cells are removed.
Students can only modify cells that are not `nbgrader` cells.
Students see a toolbar within their notebook to directly submit. The notebook is automatically saved before submitting.

Activate Student Exam Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   e2xgrader activate student_exam --sys-prefix