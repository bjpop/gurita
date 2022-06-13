.. _pair:

pair
====

Plot relationships between pairs of columns on a grid of axes.

By default comparisons are made between
all numerical columns in the data, however it is possible to specify which columns to compare, including
categorical columns as well.

Pair plots are based on Seaborn's `pairplot <https://seaborn.pydata.org/generated/seaborn.pairplot.html>`_ library function.

.. code-block:: bash

    hatch pair <arguments>

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help for this command
     - :ref:`help <pair_help>`
   * - * ``-c [COLUMN ...]``
       * ``--columns [COLUMN ...]``
     - select columns to compare 
     - :ref:`columns <pair_columns>`


Simple example
--------------

The following example generates a pair plot comparing all the numerical columns in the ``iris.csv`` data set.

Note that there are four numerical columns in this data set (``sepal_width``, ``sepal_length``, ``petal_length``, ``petal_width``) and one categorical column (``species``).
By default, if no column names are specified in a pair plot, all the numerical columns will be compared (and catergorical columns are ignored).
This behaviour can be overridden with the ``-c, --columns`` :ref:`argument <pair_columns>`.

.. code-block:: bash

    hatch pair < iris.csv

The output of the above command is written to ``pair.png``:

.. image:: ../images/pair.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing all the numerical columns in the iris.csv data set 

|

.. _pair_help:

Getting help
------------

The full set of command line arguments for pair plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch pair -h

.. _pair_columns:

Selecting columns to compare
----------------------------
