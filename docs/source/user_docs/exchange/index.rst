.. _custom_exchange:

===============
Custom Exchange
===============

`e2xgrader` comes with an optional custom exchange. The exchange provides personalized directories for each student.

Activating the Exchange
-----------------------

To activate the exchange head over to the section about :ref:`configuring e2xgrader <configure_e2xgrader>`.

Personalized Inbound
--------------------

The custom exchange can be configured to use a personalized inbound. 
If this is activated, each student will have a personalized inbound directory.

Assume you have the course *MyCourse* and the assignment
*MyAssignment*. In the original nbgrader exchange the student
will submit to :code:`<exchange_directory>/MyCourse/inbound/`.
This will be the same for each student and causes a potential security 
issue. If a student knows the name of the submission of another student,
they can read their submission.

If the personalized inbound is used, the student will submit to
:code:`<exchange_directory>/MyCourse/personalized-inbound/<student_id>/`.
This directory is only readable by the student.

.. code-block:: python

   # nbgrader_config.py

   from e2xgrader.config import configure_base, configure_exchange

   c = get_config()

   # Register custom preprocessors for autograding and generating assignments
   configure_base(c)

   # Register custom exchange
   configure_exchange(c)

   # Activate the personalized inbound
   c.Exchange.personalized_inbound = True

Personalized Outbound
---------------------

If activated, the custom exchange uses a personalized outbound
directory for each student.

This allows for creating custom versions of an assignment per student.
Students will fetch from 
:code:`<exchange_directory>/MyCourse/outbound/MyAssignment/<student_id>/`.

For this to work you will need a release version for each student.
In your formgrader you will need to create a folder for each student 
under the release version of an assignment.

Instead of having your notebooks under
:code:`release/MyAssignment/MyNotebook.ipynb` you will need to create a
directory for each student as
:code:`release/MyAssignment/<student_id>/MyNotebook.ipynb`. These notebooks
can then be personalized.

.. code-block:: python

   # nbgrader_config.py

   from e2xgrader.config import configure_base, configure_exchange

   c = get_config()

   # Register custom preprocessors for autograding and generating assignments
   configure_base(c)

   # Register custom exchange
   configure_exchange(c)

   # Activate the personalized outbound
   c.Exchange.personalized_outbound = True

Personalized Feedback
---------------------

Similar to the personalized outbound, there is an option for personalized feedback. 
This makes sure students can only read their feedback directory. 

.. code-block:: python

   # nbgrader_config.py

   from e2xgrader.config import configure_base, configure_exchange

   c = get_config()

   # Register custom preprocessors for autograding and generating assignments
   configure_base(c)

   # Register custom exchange
   configure_exchange(c)

   # Activate the personalized feedback
   c.Exchange.personalized_feedback = True