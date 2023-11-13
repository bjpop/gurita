.. _unique:

unique
======

Get the unique values from a column.

Usage
-----

.. code-block:: text

   gurita unique [-h] -c COLUMN 

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
     - :ref:`help <unique_help>`
   * - * ``-c COLUMN``
       * ``--col COLUMN``
     - get unique values in this column 
     - :ref:`column <unique_column>`

Simple example
--------------

Get the unique values in the ``species`` column in the ``iris.csv`` file:

.. code-block:: text

   gurita unique -c species < iris.csv

The output of the above command is:

.. code-block:: text

   species_unique
   setosa
   versicolor
   virginica

The output is a new table with one column called ``species_unique``. The rows in the new column list all the unique values from the ``species`` column in the input data. 

Here we see that there are three unique values: ``setosa``, ``versicolor``, and ``virginica``.

Because the output is a new table it can be passed to new commands in a chain. 

The following example passes the output of ``unique`` is the ``sort`` command, which sorts the unique values in descending order (because the ``--order d`` argument is used):

.. code-block:: text

   gurita unique -c species + sort -c species_unique --order d < iris.csv 

The output of the above command is as follows:

.. code-block:: text

   species_unique
   virginica
   versicolor
   setosa

The above output shows the same unique values as the original example, the only difference is that the values are shown in a different order. 

.. _unique_help:
    
Getting help
------------

The full set of command line arguments for ``unique`` can be obtained with the ``-h`` or ``--help``
arguments:
   
.. code-block:: text
   
    gurita unqiue -h
   
.. _unique_column:
     
Selecting the column
--------------------

.. code-block:: text

   -c COLUMN, --col COLUMN

The ``unique`` command requires the name of a single column to be specified using the ``-c/--col`` argument.

The output of ``unique`` is a new data table with a single column. The name of the output column is based on the name of the column specified by the ``-c/--col`` argument.

If the input column is named ``example`` the output column will be called ``example_unique``.

For example, the following command generates the unique values in the ``class`` column in the ``titanic.csv`` file:

.. code-block:: text

   gurita unique -c class < titanic.csv

The output of the above command is as follows:

.. code-block:: text

   class_unique
   Third
   First
   Second


