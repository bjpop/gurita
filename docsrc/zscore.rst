.. _zscore:

zscore
======

Compute the `z-score <https://en.wikipedia.org/wiki/Z-score>`_ (sometimes called standard score) for values in numerical columns.

The z-score is the number of standard deviations a value is above or below the mean of a set of values. Values above the mean have a positive z-score and values below the mean
have a negative z-score. The z-score of a value equal to the mean is zero.

Given a set of values, if M is the mean of the set and S is the standard deviation of the set then the z-score of some value x is defined to be:

z-score = (x - M) / S

The z-score is commonly used for `normalization <https://en.wikipedia.org/wiki/Normalization_(statistics)>`_ and is particularly useful when the data comes from a normal distrbution.

The ``zscore`` command adds a new column to the dataset storing the computed z-scores for the values in the corresponding input column. 
Z-scores for multiple input columns can be computed (separately) by the same command.

Usage
-----

.. code-block:: text

   gurita zscore [-h] [-c NAME [NAME ...]] [--suffix SUFFIX]  

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
     - :ref:`help <zscore_help>`
   * - * ``-c COLUMN [COLUMN...]``
       * ``--columns COLUMN [COLUMN...]``
     - determine z-scores in specified numerical columns
     - :ref:`z-score columns <zscore_columns>`
   * - ``--suffix SUFFIX``
     - choose a column name suffix for new z-score columns (default: zscore)
     - :ref:`new column name suffix <zscore_suffix>`

See also
--------

:doc:`Outliers <outlier/>` can be detected using the ``outlier`` command. 

Simple example
--------------

The following command computes z-scores for the ``sepal_width`` column in the ``iris.csv`` dataset:

.. code-block:: text

   gurita zscore -c sepal_width < iris.csv

   The output is quite long so we can adjust the command to look at only the first few rows using the :doc:`head <head>` command:

.. code-block:: text

   gurita zscore -c sepal_width + head < iris.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species,sepal_width_zscore
    5.1,3.5,1.4,0.2,setosa,1.0320572244889565
    4.9,3.0,1.4,0.2,setosa,-0.12495760117130933
    4.7,3.2,1.3,0.2,setosa,0.3378483290927974
    4.6,3.1,1.5,0.2,setosa,0.10644536396074403
    5.0,3.6,1.4,0.2,setosa,1.2634601896210098

A new numerical column called ``sepal_width_zscore`` is added to the dataset, this holds the computed z-scores for the corresponding values in the ``sepal_width`` column.

.. _zscore_help:

Getting help
------------

The full set of command line arguments for ``zscore`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita zscore -h

.. _zscore_columns:

Compute z-scores in specified numerical columns
-----------------------------------------------

.. code-block:: text

   -c NAME [NAME ...], --columns NAME [NAME ...]


By default, if no column names are specified, z-scores will be computed in all of the numerical columns in the dataset, one at a time.

For example, the following command computes z-scores in each of the numerical columns in the ``iris.csv``
dataset separately (these are: ``sepal_length``, ``sepal_width``, ``petal_length``, ``petal_width``).

.. code-block:: text

   gurita zscore < iris.csv

Sometimes it is useful to specify a subset of columns in which to compute z-scores. This can be achieved with the ``-c/--columns`` argument.

In the following example z-scores are computed in only the ``sepal_length`` and ``petal_width`` columns:

.. code-block:: text

   gurita zscore -c sepal_length petal_width < iris.csv

By chaining this command with ``head`` we can inspect the first few rows of the output:

.. code-block:: text

   gurita zscore -c sepal_length petal_width + head < iris.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species,sepal_length_zscore,petal_width_zscore
    5.1,3.5,1.4,0.2,setosa,-0.9006811702978088,-1.3129767272601454
    4.9,3.0,1.4,0.2,setosa,-1.1430169111851105,-1.3129767272601454
    4.7,3.2,1.3,0.2,setosa,-1.3853526520724133,-1.3129767272601454
    4.6,3.1,1.5,0.2,setosa,-1.5065205225160652,-1.3129767272601454
    5.0,3.6,1.4,0.2,setosa,-1.0218490407414595,-1.3129767272601454

In the above example we can see that z-scores are computed in just ``sepal_length`` and ``petal_width``. Two new numerical columns called
``sepal_length_zscore`` and ``petal_width_zscore`` are added to the dataset.

Note that in the sample of data shown in the output above all rows have the same ``petal_width`` value and hence the corresponding values in ``petal_width_zscore``
are also all identical.

.. note::

   Non-numeric columns will be ignored by ``zscore`` even if they are specified as arguments to ``-c/--columns``.

.. _zscore_suffix:

Choose a column name suffix for new z-score columns
---------------------------------------------------

.. code-block:: text

    --suffix SUFFIX

The ``zscore`` command adds extra numerical columns to the dataset to store the z-score values for the corresponding input columns.

The names of these extra columns are constructed by adding the suffix ``zscore`` on to the end of the input column names, separated by an underscore.
This can be changed with the ``--suffix`` argument.

The following command specifies that ``z`` should be used as the suffix for the newly added columns:

.. code-block:: text

   gurita zscore --suffix z < iris.csv

By chaining this command with ``head`` we can inspect the first few rows of the output:

.. code-block:: text

   gurita zscore --suffix z + head < iris.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species,sepal_length_z,sepal_width_z,petal_length_z,petal_width_z
    5.1,3.5,1.4,0.2,setosa,-0.9006811702978088,1.0320572244889565,-1.3412724047598314,-1.3129767272601454
    4.9,3.0,1.4,0.2,setosa,-1.1430169111851105,-0.12495760117130933,-1.3412724047598314,-1.3129767272601454
    4.7,3.2,1.3,0.2,setosa,-1.3853526520724133,0.3378483290927974,-1.3981381087490836,-1.3129767272601454
    4.6,3.1,1.5,0.2,setosa,-1.5065205225160652,0.10644536396074403,-1.284406700770579,-1.3129767272601454
    5.0,3.6,1.4,0.2,setosa,-1.0218490407414595,1.2634601896210098,-1.3412724047598314,-1.3129767272601454
