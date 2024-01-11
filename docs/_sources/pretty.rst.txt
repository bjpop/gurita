.. _pretty:

pretty
======

Pretty print a fragment of the dataset in an aligned tabular format to standard output. 

When the table is large only the first and last few rows and columns of data are shown.

The size of the dataset in number of rows and columns is also displayed at the end.

This is useful for getting a quick overview of the dataset.

Usage
-----

.. code-block:: bash

   gurita pretty [-h] [-c [COLUMN ...]] [--maxrows NUM] [--maxcols NUM]

Arguments
---------

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
     - :ref:`help <pretty_help>`
   * - * ``-c [COLUMN ...]``
       * ``--col [COLUMN ...]``
     - select columns for display 
     - :ref:`columns <describe_columns>`
   * - ``--maxrows NUM``
     - display at most this many rows of data (default 10)
     - :ref:`maximum rows <pretty_maxrows>`
   * - ``--maxcols NUM``
     - display at most this many columns of data (default 10)
     - :ref:`maximum columns <pretty_maxcols>`

See also
--------

The :doc:`describe <describe/>` command prints summary statistics of the columns in a dataset to standard output (stdout).

Simple example
--------------

Make a pretty display of the data in the ``titanic.csv`` file:

.. code-block:: text

   gurita pretty < titanic.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/titanic.pretty.txt
   :language: none

.. _pretty_help:

Getting help
------------

The full set of command line arguments for ``pretty`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita pretty -h

.. _pretty_columns:

Select specific columns to display 
----------------------------------

.. code-block::

  -c [COLUMN ...], --col [COLUMN ...]

By default ``pretty`` shows information about all columns in a dataset up to the limit imposed by
the ``--maxcols`` parameter, which defaults to 10.

Alternatively, a subset of the columns can be selected using the ``-c/--col`` argument.

As an example, The following commmand only shows summary information for the ``age`` and ``class`` columns in the file ``titanic.csv``:

.. code-block:: bash

    gurita pretty --col age class < titanic.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/titanic.pretty.age.class.txt
   :language: none

Note that only the ``age`` and ``class`` columns are shown. However, the size of the dataset reported at the bottom of the display reflects the entire dataset, not just the columns that are shown.

.. _pretty_maxrows:
.. _pretty_maxcols:

Limiting the maximum number of rows and columns to display
----------------------------------------------------------

.. code-block:: text

   --maxrows NUM
   --maxcols NUM

By default the ``pretty`` command will display a maximum of 10 rows and columns. If the dataset is larger than this size then the first 5 and last 5 rows and columns will be shown, and the intervening columns will be elided and shown with ellipses.

These defaults can be overridden by ``--maxrows`` and ``--maxcols`` respectively.

For example, the following command sets the maximum number of rows to 20 and maximum number of columns to 6:

.. code-block:: text

    gurita pretty --maxrows 20 --maxcols 6 < titanic.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/titanic.pretty.maxrows.20.maxcols.6.txt
   :language: none

Usage in a command chain
------------------------

When used in a command chain the ``pretty`` command passes on its input data to the rest of the chain unchanged.

For example, the following command shows ``pretty`` followed by a ``box`` plot:

.. code-block:: text

   gurita pretty + box -x sex -y age < titanic.csv

This command will first run ``pretty`` to display the data on the output, and then it will run ``box`` to generate a plot on the same input data.

Because ``pretty`` just passes the data along from left to right the ``box`` command receives the same data as its input that was read from the file.

It is also worth noting that ``pretty`` can be used after other transformations have been applied to the data. For example, the data can be filtered first, and then the result of filtering can be fed
into ``pretty``:

.. code-block:: text

   gurita filter 'age >= 30' + pretty < titanic.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/titanic.filter.30.pretty.txt
   :language: none
