.. _custom_exchange:

=====================
Personalized Exchange
=====================

`e2xgrader` comes with an optional custom exchange. The exchange takes care of distributing assignments and feedback to students and collecting submissions.
Our exchange is based on the original nbgrader exchange and extends it with the following features:

- Custom :ref:`submit <custom_submit_exchange>` behavior based on e2xgrader mode, with advanced features like hashing and HTML conversion for exams in student_exam mode.
- Personalized inbound and feedback directory for each student, to prevent students from reading each other's submissions and feedback. (Activated by default)
- Personalized outbound directory for each student, to provide personalized versions of an assignment. (Deactivated by default)

Activating the Exchange
-----------------------

To activate the exchange head over to the section about :ref:`configuring e2xgrader <configure_e2xgrader>`.

Personalized Inbound
--------------------

The inbound directory is the directory where students submit their assignments.
The custom exchange can be configured to use a personalized inbound directory. This is activated by default.
When this is active, students submit to :code:`<exchange_directory>/<course_id>/personalized-inbound/<student_id>/`.
Students will only have access to their own submissions.

In the original nbgrader exchange, the inbound directory is the same for all students (:code:`<exchange_directory>/<course_id>/inbound/`).
This can be a security issue, as students can read each other's submissions if they know the timestamp or random string of the submission.

To configure the personalized inbound, add the following to your `nbgrader_config.py`:

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

The outbound directory is the directory where students fetch their assignments from.
If the personalized outbound is activated, students will fetch from a personalized directory.
This is useful if you want to create personalized versions of an assignment for each student.

Students will fetch from 
:code:`<exchange_directory>/<course_id>/outbound/<assignment_id>/<student_id>/`.

To create personalized versions of an assignment, you will need to create a directory for each student under the release version of an assignment.

Instead of having your notebooks under
:code:`release/<assignment_id>/MyNotebook.ipynb` you will need to create a
directory for each student as
:code:`release/<assignment_id>/<student_id>/MyNotebook.ipynb`. These notebooks can be personalized for each student.

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

The feedback directory is the directory where students fetch their feedback from. This is activated by default.
Similar to the personalized outbound, there is an option for personalized feedback. 
This makes sure students can only read their feedback directory. 
To configure the personalized feedback, add the following to your `nbgrader_config.py`:

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
