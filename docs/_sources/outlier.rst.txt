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

See also
--------

:doc:`Box plots <box/>` also employ the concept of Tukey's fences for determining outlier values.

:doc:`Z-scores <zscore/>` can be used to normalise data based on how many standard deviations it is from the mean. This can also be used as a method
for identifying outliers.


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

.. code-block:: text

   -c NAME [NAME ...], --columns NAME [NAME ...]

By default, if no column names are specified, outliers will be detected in all of the numerical columns in the dataset, one at a time.

For example, the following command detects outliers in each of the numerical columns in the ``iris.csv`` 
dataset separately (these are: ``sepal_length``, ``sepal_width``, ``petal_length``, ``petal_width``).

.. code-block:: text

   gurita outlier < iris.csv

Sometimes it is useful to specify a subset of columns in which to detect outliers. This can be achieved with the ``-c/--columns`` argument.

In the following example outliers are detected in only the ``sepal_length`` and ``petal_width`` columns:

.. code-block:: text

   gurita outlier -c sepal_length petal_width < iris.csv

By chaining this command with ``head`` we can inspect the first few rows of the output:

.. code-block:: text

   gurita outlier -c sepal_length petal_width + head < iris.csv

The output of the above command is as follows:

.. code-block:: text

   sepal_length,sepal_width,petal_length,petal_width,species,sepal_length_outlier,petal_width_outlier
   5.1,3.5,1.4,0.2,setosa,False,False
   4.9,3.0,1.4,0.2,setosa,False,False
   4.7,3.2,1.3,0.2,setosa,False,False
   4.6,3.1,1.5,0.2,setosa,False,False
   5.0,3.6,1.4,0.2,setosa,False,False

In the above example we can see that outliers are detected in just ``sepal_length`` and ``petal_width``. Two new boolean columns called
``sepal_length_outlier`` and ``petal_width_outlier`` are added to the dataset to flag which rows contain outliers for the corresponding input columns.

.. note::

   Non-numeric columns will be ignored by ``outlier`` even if they are specified as arguments to ``-c/--columns``.

.. _outlier_suffix:

Choose a column name suffix for new outlier columns
---------------------------------------------------

.. code-block:: text

    --suffix SUFFIX

The ``outlier`` command adds extra boolean columns to the dataset to flag which rows contain outlier values for the corresponding input columns.

The names of these extra columns are constructed by adding the suffix ``outlier`` on to the end of the input column names, separated by an underscore. 
This can be changed with the ``--suffix`` argument.

The following command specifies that ``out`` should be used as the suffix for the newly added columns:

.. code-block:: text

   gurita outlier --suffix out < iris.csv

By chaining this command with ``head`` we can inspect the first few rows of the output:

.. code-block:: text

   gurita outlier --suffix out + head < iris.csv

The output of the above command is as follows:

.. code-block:: text

   sepal_length,sepal_width,petal_length,petal_width,species,sepal_length_out,sepal_width_out,petal_length_out,petal_width_out
   5.1,3.5,1.4,0.2,setosa,False,False,False,False
   4.9,3.0,1.4,0.2,setosa,False,False,False,False
   4.7,3.2,1.3,0.2,setosa,False,False,False,False
   4.6,3.1,1.5,0.2,setosa,False,False,False,False
   5.0,3.6,1.4,0.2,setosa,False,False,False,False

.. _outlier_scale_factor:

Scale factor for determining outliers
-------------------------------------

.. code-block:: text

   --iqrscale S

As noted earlier, given quartiles Q1 and Q3 and some scaling factor S, a data point x is considered an outlier if either:

* x < (Q1 - S*IQR), or
* x > (Q3 + S*IQR)

By default the scaling factor S is equal to 1.5, however this can be changed with the ``--iqrscale`` argument.

Setting the scaling factor higher means that values must be more extreme before being considered outliers. Setting it lower has the opposite effect.

The following command specifies a scaling factor of 3:

.. code-block:: text

   gurita outlier --iqrscale 3 < iris.csv 

The more stringent scaling factor of 3 produces fewer outlier values than the default setting of 1.5.
