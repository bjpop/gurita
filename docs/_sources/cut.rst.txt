.. _cut:

cut
===

Select and keep or drop specified columns from the data set.

Usage
-----

.. code-block:: bash

    gurita cut [-h] -c COLUMN [COLUMN ...] [-i]

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
     - :ref:`help <cut_help>`
   * - * ``-c [COLUMN ...]``
       * ``--columns [COLUMN ...]``
     - select columns
     - :ref:`select columns <cut_columns>`
   * - * ``-i``
       * ``--invert``
     - drop the selected columns insted of keeping them 
     - :ref:`drop selected columns <cut_invert>`

Simple example
--------------

Suppose we are working with the following small data set with 10 data rows that is stored in a file called ``example.csv``:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    6.3,3.4,5.6,2.4,virginica
    6.3,2.5,5.0,1.9,virginica
    4.8,3.4,1.9,0.2,setosa
    6.3,3.3,4.7,1.6,versicolor
    6.4,3.2,4.5,1.5,versicolor
    4.7,3.2,1.3,0.2,setosa
    6.4,2.8,5.6,2.1,virginica
    5.4,3.9,1.7,0.4,setosa
    5.9,3.0,4.2,1.5,versicolor
    5.2,3.5,1.5,0.2,setosa

We can select and keep just the ``sepal_length`` and ``species`` columns and discard all other columns with the following command:

.. code-block:: text

    gurita cut -c sepal_length species < example.csv

The output of the above command is shown below. Observe that only the two selected columns remain in the data set.

.. code-block:: text

    sepal_length,species
    6.3,virginica
    6.4,virginica
    5.4,setosa
    4.5,setosa
    6.1,versicolor
    5.6,versicolor
    6.5,virginica
    5.7,versicolor
    6.7,virginica
    5.8,versicolor

.. _cut_help:

Getting help
------------

The full set of command line arguments for ``cut`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita cut -h

.. _cut_columns:

Selecting columns
-----------------

.. code-block:: text

    -c NAME [NAME ...], --columns NAME [NAME ...]

The ``cut`` command requires one or more column names to be specified. By default, the named columns are kept and the unnamed columns are discarded. 

Note that this behaviour is inverted with the ``-i`` (``--invert``) option is specified, such that the named columns are dropped (see below).

.. _cut_invert:

Drop selected columns
---------------------

The columns specified by ``-c`` (``--columns``) are dropped when the ``-i`` (``--invert``) option is specified.

For example, the command below drops the columns ``sepal_length`` and ``species`` and keeps all other columns from the data set in ``example.csv``:

.. code-block:: text

    gurita cut -c sepal_length species -i < example.csv

The output of the command is shown below. Note that the columns retained are the inverse of the ones from the simple example above. 

.. code-block:: text

    sepal_width,petal_length,petal_width
    3.4,5.6,2.4
    3.1,5.5,1.8
    3.9,1.3,0.4
    2.3,1.3,0.3
    2.9,4.7,1.4
    2.7,4.2,1.3
    3.0,5.2,2.0
    2.6,3.5,1.0
    3.1,5.6,2.4
    2.6,4.0,1.2
