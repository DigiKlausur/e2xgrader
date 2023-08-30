.. _configure_e2xgrader:

===================
Configure e2xgrader
===================

To make sure all e2xgrader features are working as expected in teacher mode, you need to edit your *nbgrader_config.py* file.
Information about where this file is located can be found 
in the `nbgrader docs`_.

Basic Configuration
-------------------

The basic configuration is only needed in teacher mode. It makes sure all custom preprocessors are activated and that `nbgrader` can grade `e2xgraders` custom cells.

.. code-block:: python

   # nbgrader_config.py

   from e2xgrader.config import configure_base

   c = get_config()

   # Register custom preprocessors for autograding and generating assignments
   configure_base(c)

.. _configuring-the-exchange:

Configuring the Exchange
------------------------

.. code-block:: python

   # nbgrader_config.py

   from e2xgrader.config import configure_exchange

   c = get_config()

   # Register custom exchange
   configure_exchange(c)

.. _nbgrader docs: https://nbgrader.readthedocs.io/en/stable/configuration/nbgrader_config.html