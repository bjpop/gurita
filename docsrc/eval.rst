.. _eval:

eval
====

Add new columns to the dataset by evaluating an expression. 

On each row the value in the new column is computed using a simple expression language that can refer to the values in other columns on the same row.

The expression language uses a simple syntax that resembles Python.

.. warning::

   Eval is based on the `Pandas eval method on dataframes <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.eval.html>`_.

   The documentation on that method says:

       "This allows eval to run arbitrary code, which can make you vulnerable to code injection if you pass user input to this function."

   This is a security risk!

   Do not use ``eval`` if you do not trust the expression supplied as an argument. For example, do not use ``eval`` on strings that
   are input from untrusted sources, such as input to web pages.

.. code-block:: text 

    gurita eval <arguments>

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - * ``-h``
       * ``--help``
     - display help for this command
     - :ref:`help <eval_help>`
   * - ``expression``
     - the expression to evaluate 
     - :ref:`expression <eval_expression>`

Simple example
--------------

The ``iris.csv`` dataset contains information about the lengths and widths of iris sepals and petals for a variety of species.

We can look at the first few data rows using the ``head`` command:

.. code-block:: text

    gurita head < iris.csv

The output is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,setosa
    4.7,3.2,1.3,0.2,setosa
    4.6,3.1,1.5,0.2,setosa
    5.0,3.6,1.4,0.2,setosa

Suppose that we want to add a new column to the dataset called ``sepal_area`` that is computed on each row from ``sepal_length * sepal_height * 0.5`` (where ``*`` means multiplication).

This can be achieved with the ``eval`` command like so:

.. code-block:: text

   gurita eval 'sepal_area = sepal_length * sepal_width * 0.5' < iris.csv

Note that the whole expression is inside quotation marks.

In this example we us an expression to compute the value of the new column:

.. code-block:: text

   sepal_area = sepal_length * sepal_width * 0.5

The syntax of the expression closely resembles that of the Python programming language.

Note in paricular that a new column is made simply by assigning to it on the left-hand-side of the expression. On the right-hand-side we can refer to the values of other existing
columns by using their names, such as ``sepal_length``. We can also refer to numerical constants such as ``0.5``.

We can see the effect of the above example ``eval`` statment by viewing the first few rows of the output like so:

.. code-block:: text

   gurita eval 'sepal_area = sepal_length * sepal_width * 0.5' + head < iris.csv

The output of the above command is shown below:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species,sepal_area
    5.1,3.5,1.4,0.2,setosa,8.924999999999999
    4.9,3.0,1.4,0.2,setosa,7.3500000000000005
    4.7,3.2,1.3,0.2,setosa,7.5200000000000005
    4.6,3.1,1.5,0.2,setosa,7.13
    5.0,3.6,1.4,0.2,setosa,9.0

As you can see a new column called ``sepal_area`` has been added to the data, such that the value on each row is computed from the supplied expression.

Complex example
---------------

Suppose we have a dataset in a file called ``points.csv`` with numerical columns ``x1``, ``y1``, ``x2``, ``y2``, representing pairs of points in the cartesian plane: ``(x1, y1)`` and ``(x2, y2)``.

A new column called ``dist`` representing the cartesian distance between the pairs of points can be created with ``eval`` like so:

.. code-block:: text

     gurita eval 'dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)' < points.csv 

Some notable features of this example expression include the use of a mathematical function ``sqrt``, parentheses for grouping sub-expressions, and the use of various mathematical operators ``+``, ``-`` and ``**`` (exponentiation).

A more detailed description of the expression syntax is provided below.

.. _eval_help:

Getting help
------------

The full set of command line arguments for ``eval`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita eval -h

.. _eval_expression:

Expressions 
-----------

.. code-block:: text

   eval EXPR [EXPR ..]

The ``eval`` command accepts one or more expression arguments. Each of these specifies how to create a new column in the data. 

Each expression creates a new column in the dataset. Therefore each expression must specify the name of the new column in the form of an assignment statment:

.. code-block:: text

   new_column_name = expression_right_hand_side 

If more than one expression is provided multiple columns will be added, one for each expression. Expressions can even refer to new columns that were added on their left.

In the example below the first expression adds a new column called ``new1`` (assuming the existence of a column ``old`` in the input data). The second expression adds another column called ``new2`` that is computed from the row-wise addition of ``old`` and ``new1``.

.. code-block:: text

    gurita eval 'new1 = old + 5' 'new2 = old + new1' < example.csv

Expression syntax
^^^^^^^^^^^^^^^^^

The ``eval`` command is implemented using the `Pandas eval method on dataframes <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.eval.html>`_. 

And therefore the syntax of ``eval`` in Gurita is the same as the syntax of the Pandas ``eval`` method.

In essence the ``eval`` expression syntax is a simplified form of Python. 
The details of which are described in the `Pandas documenation <https://pandas.pydata.org/docs/user_guide/enhancingperf.html#expression-evaluation-via-eval>`_. We give a summary below.

.. warning::

   If the new column name already exists in the dataset it will be overwritten in the output.

Referring to column names
^^^^^^^^^^^^^^^^^^^^^^^^^

On each row the value in the new column is computed using a simple expression language that can refer to the values in other columns on the same row.

Column names can be written as if they are ordinary variables inside the expression.

In the example from earlier ``sepal_length`` and ``sepal_width`` are the names of existing columns in the data, and ``sepal_area`` is the name
given to the new column added to the data:

.. code-block:: text

   gurita eval 'sepal_area = sepal_length * sepal_width * 0.5' < iris.csv


Column names that cannot be written like ordinary Python variables must be written inside back-quotes. For instance, column names can have spaces in them, but Python variable names cannot.

For example, a column named ``average height`` (note the space in the name) would have to be wrtten as ```average height```.

Allowed expressions
^^^^^^^^^^^^^^^^^^^

* Parentheses (round brackets for grouping sub-expressions)
* Constants:
      * strings
      * floating point numbers
      * integers
      * booleans (True, False)
* Arithmetic operations:
      * multiplication: ``*`` 
      * addition: ``+`` 
      * subtraction: ``-`` 
      * division: ``/`` 
      * exponentiation: ``**`` (raising to a power)
* Comparison operations:
      * equality: ``==`` 
      * less-than: ``<`` 
      * less-than-equals: ``<=`` 
      * greater-than: ``>`` 
      * greater-than-equals: ``>=`` 
* Logical operations:
      * conjunction: ``and``
      * disjuntion: ``or``
      * negation: ``not``
* Mathematical functions (written as ``fun(arg)``):
      * ``sin``
      * ``cos``
      * ``exp``
      * ``log`` (natural log)
      * ``expm1``
      * ``log1p``
      * ``sqrt``
      * ``sinh``
      * ``cosh``
      * ``tanh``
      * ``arcsin``
      * ``arccos``
      * ``arctan``
      * ``arccosh``
      * ``arcsinh``
      * ``arctanh``
      * ``abs``
      * ``arctan2``
      * ``log10``
