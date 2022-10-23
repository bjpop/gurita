.. _outlier:

outlier
=======

Detect and annotate outliers in numerical columns based on the interquartile range. This method is often called `Tukey's Fences <https://en.wikipedia.org/wiki/Outlier>`_.

Considering all the numerical values in a particular column we can calculate: 

* Q1 = the first quartile 
* Q3 = the third quartile
* IQR = the interquartile range (Q3 - Q1)

Given some scaling factor S (typically 1.5), a data point x is considered an outlier if either:

* x < (Q1 - S*IQR), or
* x > (Q3 + S*IQR)

Note that the ``outlier`` command does not remove data from the dataset. Instead, it adds an extra boolean column that indicate whether the value in
the corresponding column is an outlier according to the definition above. This allows flexibility in how outliers are subsequently handled. 

Multiple columns can be tested for outliers in the same command.

Usage
-----

.. code-block:: text

   gurita outlier [-h] [-c NAME [NAME ...]] [--suffix SUFFIX] [--iqrscale S]

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
     - :ref:`help <outlier_help>`
   * - * ``-c COLUMN [COLUMN...]``
       * ``--columns COLUMN [COLUMN...]``
     - determine outliers in specified numerical columns 
     - :ref:`outlier columns <outlier_columns>`
   * - ``--suffix SUFFIX``
     - choose a column name suffix for new outlier columns (default: outlier) 
     - :ref:`new column name suffix <outlier_suffix>`
   * - ``--iqrscale S``
     - scale factor for determining outliers (default: 1.5) 
     - :ref:`scale factor <outlier_scale_factor>`

Simple example
--------------

The following command determines outliers in the ``sepal_width`` column in the ``iris.csv`` dataset:

.. code-block:: text

   gurita outlier -c sepal_width < iris.csv

The output is quite long so we can adjust the command to look at only the first few rows using the :doc:`head <head>` command:

.. code-block:: text

   gurita outlier -c sepal_width + head < iris.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species,sepal_width_outlier
    5.1,3.5,1.4,0.2,setosa,False
    4.9,3.0,1.4,0.2,setosa,False
    4.7,3.2,1.3,0.2,setosa,False
    4.6,3.1,1.5,0.2,setosa,False
    5.0,3.6,1.4,0.2,setosa,False

Outliers are detected using the interquartile range.

A new boolean column called ``sepal_width_outlier`` is added to the dataset, indicating whether the value in the specified column is an outlier.
This will be ``True`` if it is an outlier and ``False`` otherwise.

.. _outlier_help:

Getting help
------------

The full set of command line arguments for ``outlier`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita outlier -h

.. _outlier_columns:

Determine outliers in specified numerical columns
-------------------------------------------------

.. _outlier_suffix:

Choose a column name suffix for new outlier columns
---------------------------------------------------

.. _outlier_scale_factor:

Scale factor for determining outliers
-------------------------------------

