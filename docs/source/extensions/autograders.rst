.. _custom_autograders:

=========================
Adding Custom Autograders
=========================

`e2xgrader` allows you to register custom autograders.

Writing Your Own Autograder
---------------------------

To write your own autograder, you need to inherit from `e2xgrader.graders.base.BaseGrader`.
This class exposes two methods:

* :code:`def cell_changed(self, cell: NotebookNode) -> bool:` 
* :code:`def determine_grade(self, cell: NotebookNode, log: logger = None) -> Tuple[Optional[float], float]:`

In most cases you can ignore the `cell_changed` method.
You always need to implement the `determine_grade` method. This method takes a cell and returns a tuple of `(points, max_points)`. 
Here `points` is the amount of points the autograder assigns to this cell and `max_points` is the maximum number of points the cell is worth.

Custom MultipleChoice Grader
----------------------------

Here is an example of a custom multiple choice grader that only assigns points if all answers are correctly selected:

.. code-block:: python

   from e2xgrader.graders import BaseGrader
   from e2xgrader.utils.extra_cells import get_choices, get_instructor_choices

   class CustomMultipleChoiceGrader(BaseGrader):

       def determine_grade(self, cell, log=None):
           # Determine the maximum number of points
           max_points = float(cell.metadata["nbgrader"]["points"])
           
           # Determine the correct solution
           reference_solution = get_instructor_choices(cell)

           # Determine what the student chose
           student_solution = get_choices(cell)

           # Return 0 points if the student did not select all correct answers
           for choice in reference_solution:
               if choice not in student_solution:
                   return 0, max_points
            
           # Return 0 points if the student did select an incorrect answer
           for choice in student_solution:
               if choice not in reference_solution:
                   return 0, max_points

           # The student did select only correct answers
           return max_points, max_points

Registering Your Autograder
---------------------------

To register your own autograder you need to add it via the `nbgrader_config.py` file.

Here is an example of how to do it for the example grader above:

.. code-block:: python

    # nbgrader_config.py
    from e2xgrader.config import configure_base

    c = get_config()
    configure_base(c)

    # Import your grader, here we assume it is in a package called mygrader
    # It can also be implemented directly in the config

    from mygrader import CustomMultipleChoiceGrader

    c.SaveAutoGrades.graders.update({
       "multiplechoice": CustomMultipleChoiceGrader
    })

Advanced Options
----------------

To find out which autograder to use, `e2xgrader` first determines the cell type and then looks in the dictionary :code:`SaveAutoGrades.graders` if there is an entry for the cell type.
If so it will call the grader for that entry. If not it will fall back to the standard `nbgrader` autograder.

The cell type is determined as follows:

If the cell has a metadata entry :code:`cell.metadata.extended_cell.type`, this value will be used (currently the options here are: `multiplechoice`, `singlechoice`, `diagram`, `attachments`). 
You can also add your own value here.
Otherwise the standard cell type :code:`cell.cell_type` will be used (`code`, `markdown`).