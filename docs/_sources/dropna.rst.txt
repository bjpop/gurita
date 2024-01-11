.. _dropna:

dropna
======

Drop rows or columns from the data that contain missing (NA) values.

Usage
-----

.. code-block:: bash

   gurita dropna [-h] [--axis AXIS] [--how METHOD] [--thresh N] [-c COLUMN [COLUMN ...]] 

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
     - :ref:`help <dropna_help>`
   * - ``--axis {rows,columns}``
     - drop either rows or columns (default: rows)
     - :ref:`axis <dropna_axis>`
   * - ``--thresh N``
     - keep only those rows/columns with at least N non-missing values
     - :ref:`thresh <dropna_thresh>`
   * - * ``-c [COLUMN ...]``
       * ``--col [COLUMN ...]``
     - consider only specified columns when dropping rows 
     - :ref:`columns <dropna_columns>`
   * - ``--how {any,all}``
     - drop rows/columns containing *any* or *all* missing values
     - :ref:`how <dropna_how>`

.. note::

   For information about how missing data is represented see the documentation on :doc:`missing (NA) values <missing>`.

Simple example
--------------

Consider the following contents of a CSV file that has two missing values. In the following examples we will assume that this
data is stored in a filed called ``missing.csv``.

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,
    4.9,3.0,1.4,0.2,virginica
    4.7,,1.3,0.2,setosa

The first data row is missing a categorical value in the ``species`` column. 
The third data row is missing a numerical value in the ``sepal_width`` column. 

The following command drops all the rows that contain at least one column with a missing value:

.. code-block:: text

    gurita dropna < missing.csv 

The result of the above command is shown below, where only the middle row of the input data remains: 

.. literalinclude:: example_outputs/missing.dropna.txt
   :language: none

.. _dropna_help:

Getting help
------------

The full set of command line arguments for ``dropna`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita dropna -h

.. _dropna_axis:

Choose between dropping rows or columns
---------------------------------------

.. code-block:: text

    --axis {rows,columns} 

By default ``dropna`` will remove rows from the dataset, however, it can also drop columns instead.

You can choose between dropping rows or columns with the ``--axis`` argument.

The following command drops all the columns that contain at least one column with a missing value:

.. code-block:: text

    gurita dropna --axis columns < missing.csv

The result of the above command is shown below, where ``species`` and ``sepal_width`` columns have been removed because they contained
rows with missing values:

.. literalinclude:: example_outputs/missing.dropna.axis.txt
   :language: none

.. _dropna_thresh:

Set a minumum number of non-missing values 
------------------------------------------

.. code-block:: text

    --thresh N

By default ``dropna`` drops rows or columns that contain at least one missing value.

Or, in other words, it retains only rows or columns that have *no* missing values.

The ``--thresh N`` argument sets a threshold ``N``, such that only rows or columns with at least ``N`` *non-missing*
values in them will be retained. This can be useful when you want to ensure that a minimum number of data values are present. 

The following example requires at least 5 non-missing values across columns to be present for a row to be retained:

.. code-block:: text

    gurita dropna --thresh 5 < missing.csv 

And the following example requires at least 3 non-missing values across rows to be present for a column to be retained:

.. code-block:: text

    gurita dropna --thresh 3 --axis columns < missing.csv 

.. _dropna_columns:

Consider only specified columns when dropping rows
--------------------------------------------------

.. code-block::

  -c [COLUMN ...], --col [COLUMN ...]

By default, when dropping rows, ``dropna`` will look for missing values in all columns. The ``--col`` option
lets you specify a subset of columns to consider for missing values.

.. note::

   This option does not apply when ``--axis columns`` is also used

.. code-block:: text

   gurita dropna --col species < missing.csv 

The output of the above command is shown below:

.. literalinclude:: example_outputs/missing.dropna.species.txt
   :language: none

Only the first row from the input data has a missing value in the ``species`` column, so only that row is dropped in the above example, all other rows are retained. 
Note that the third row from the input data is retained even though it contains a missing value, this is because the missing value did not occur in the ``species`` column.

.. _dropna_how:

Drop rows/columns containing any or all missing values
------------------------------------------------------

.. code-block::

    --how {any,all}

By default ``dropna`` will drop rows or columns that have any (at least one) missing value. However, this behaviour can be changed with the
``--how all`` option, which only drops rows or columns where *all* the values are missing.

The following example drops rows that are missing all their values:

.. code-block:: text

   gurita dropna --how all < missing.csv 
