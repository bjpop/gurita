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

.. code-block:: text

   survived  pclass    sex  age  sibsp  ...  adult_male  deck embark_town alive alone
          0       3   male 22.0      1  ...        True   NaN Southampton    no False
          1       1 female 38.0      1  ...       False     C   Cherbourg   yes False
          1       3 female 26.0      0  ...       False   NaN Southampton   yes  True
          1       1 female 35.0      1  ...       False     C Southampton   yes False
          0       3   male 35.0      0  ...        True   NaN Southampton    no  True
        ...     ...    ...  ...    ...  ...         ...   ...         ...   ...   ...
          0       2   male 27.0      0  ...        True   NaN Southampton    no  True
          1       1 female 19.0      0  ...       False     B Southampton   yes  True
          0       3 female  NaN      1  ...       False   NaN Southampton    no False
          1       1   male 26.0      0  ...        True     C   Cherbourg   yes  True
          0       3   male 32.0      0  ...        True   NaN  Queenstown    no  True

   [891 rows x 15 columns]

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

.. code-block:: bash

     age  class
    22.0  Third
    38.0  First
    26.0  Third
    35.0  First
    35.0  Third
     ...    ...
    27.0 Second
    19.0  First
     NaN  Third
    26.0  First
    32.0  Third
    
    [891 rows x 15 columns]

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

.. code-block:: text

    survived  pclass    sex  ...  embark_town  alive  alone
           0       3   male  ...  Southampton     no  False
           1       1 female  ...    Cherbourg    yes  False
           1       3 female  ...  Southampton    yes   True
           1       1 female  ...  Southampton    yes  False
           0       3   male  ...  Southampton     no   True
           0       3   male  ...   Queenstown     no   True
           0       1   male  ...  Southampton     no   True
           0       3   male  ...  Southampton     no  False
           1       3 female  ...  Southampton    yes  False
           1       2 female  ...    Cherbourg    yes  False
         ...     ...    ...  ...          ...    ...    ...
           0       3   male  ...  Southampton     no   True
           0       3 female  ...  Southampton     no   True
           0       2   male  ...  Southampton     no   True
           0       3   male  ...  Southampton     no   True
           0       3 female  ...   Queenstown     no  False
           0       2   male  ...  Southampton     no   True
           1       1 female  ...  Southampton    yes   True
           0       3 female  ...  Southampton     no  False
           1       1   male  ...    Cherbourg    yes   True
           0       3   male  ...   Queenstown     no   True
   
   [891 rows x 15 columns]

Usage in a command chain
------------------------

When used in a command chain the ``pretty`` command passes on its input data to the rest of the chain unchanged.

For example, the following command shows ``pretty`` followed by a ``box`` plot:

.. code-block:: text

   gurita pretty + box -x sex -y age < titanic.csv

This command will first run ``pretty`` to display the data on the output, and then it will run ``box`` to generate a plot on the same input data.

Because ``pretty`` just passes the data along from left to right the ``box`` command receives the same data as its input that was read from the file.

It is also worth noting that ``pretty`` can be used after other transformations have been applied t
o the data. For example, the data can be filtered first, and then the result of filtering can be fed
into ``pretty``:

.. code-block:: text

   gurita filter 'age >= 30' + pretty < titanic.csv
