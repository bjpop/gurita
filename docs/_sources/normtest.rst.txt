.. _normtest:

normtest
========

Test whether numerical columns differ from a normal distribution.

Specifically this command tests a null hypothesis that data comes from a normal distribution
and computes a p-value for that test. 

If the p-value is less than or equal to some threshold for significance (e.g. p <= 0.05) then the null-hypothesis can be rejected, concluding that the data is not likely to come from a normal 
distribution. 

Otherwise, if the p-value is greater than the threshold of significance (e.g. p > 0.05) then we 
cannot reject the null-hypothesis and we may conclude that the data likely comes from a normal
distribution.

Usage
-----

.. code-block:: text

    gurita normtest [-h] [-c [COLUMN ...]] [-m {dagostino,shapiro}] [-a ALPHA] [-p] [-s] 

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
     - :ref:`help <normtest_help>`
   * - * ``-c COLUMN [COLUMN...]``
       * ``--col COLUMN [COLUMN...]``
     - test these numerical columns 
     - :ref:`test specific columns <normtest_columns>`
   * - * ``-a ALPHA``
       * ``--alpha ALPHA`` 
     - threshold of significance
     - :ref:`threshold <normtest_threshold>`
   * - * ``-p``
       * ``--pvalue`` 
     - report p-value in output
     - :ref:`p-value <normtest_pvalue>`
   * - * ``-s``
       * ``--stat`` 
     - report test statistic in output
     - :ref:`statistic <normtest_statistic>`
   * - * ``-m {dagostino,shapiro}``
       * ``--method {dagostino,shapiro}`` 
     - method for testing normality 
     - :ref:`method <normtest_method>`

By default `D'Agostino's K^2 test <https://en.wikipedia.org/wiki/D%27Agostino%27s_K-squared_test>`_ is applied. However, it is also possible to use the `Shapiro-Wilk test <https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test>`_ instead. 

If no columns are specified Gurita will test all numerical columns in the dataset one at a time. 

By default the p-value and test statistic are not included in the output, but this can be
overridden with the ``-p/--pvalue`` and ``-s/--stat`` arguments.

Simple example
--------------

The following example tests all the numerical columns in ``iris.csv`` independently to see if they each differ from the normal distribution.

.. code-block:: text

     gurita normtest < iris.csv 

The output of the above command is shown below:

.. literalinclude:: example_outputs/iris.normtest.txt
   :language: none 

The output contains two columns:

1. ``column``: this is the name of the numerical column of data being tested
2. ``is_normal``: a boolean value, True if the corresponding column is likely from a normal distribution and False otherwise. 

Looking at the above results we see that, under the default parameters of the test, ``sepal_length`` and ``sepal_width`` appear to be normal, but ``petal_length`` and ``petal_width`` do not appear to be normal.  Indeed, plotting the histogram for ``petal_length`` or ``petal_width`` suggests that they are multi-modal.

Note that ``iris.csv`` also contains a categoritcal column called ``species``. The normality test
only applies to numerical columns, therefore non-numerical columns are ignored.

.. _normtest_help:

Getting help
------------

The full set of command line arguments for ``normtest`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita normtest -h

.. _normtest_columns:

Choose columns to test for normality 
------------------------------------

.. code-block:: text

   -c COLUMN [COLUMN...]
   --col COLUMN [COLUMN...]

By default ``normtest`` will test all numerical columns for normality, however the ``--col/-c`` option allows you to test only specific columns.

For example the following command tests only the ``sepal_length`` column from the ``iris.csv`` dataset:

.. code-block:: text

    gurita normtest -c sepal_length < iris.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/iris.normtest.sepal_length.txt
   :language: none

Multiple specific columns can be tested as the following example demonstrates:

.. code-block:: text

    gurita normtest -c sepal_length petal_length < iris.csv 

The output of the above command is as follows:

.. literalinclude:: example_outputs/iris.normtest.sepal_length.petal_length.txt
   :language: none

Note that non-numerical columns are ignored, even if they are specified using ``--col/-c``.
For example the following command tries to test of the categorical ``species`` column is normal:

.. code-block:: text

    gurita normtest -c species < iris.csv

It is not logical to make this test, so the output of the command is just an empty dataset, with
only a header row and no data rows:

.. literalinclude:: example_outputs/iris.normtest.species.txt
   :language: none

.. _normtest_threshold:

Threshold for the p-value 
-------------------------

.. code-block:: text

   -a ALPHA
   --alpha ALPHA

The ``normtest`` command computes a p-value for the null-hypothesis that the data comes from
a normal distribution.

A threshold called ``alpha`` is applied to the p-value to decide whether or not the 
data differs from a normal distrbution.

By default alpha is set to 0.05, as is often done by convention.

If the p-value is less than or equal to alpha, the null-hypothesis is rejected and we 
conclude that the data differs from a normal distribution (i.e. the data is not normally distributed). Alternatively, if the p-value is greater than alpha then we cannot reject 
the null-hypothesis, and therefore we conclude that the data does not differ from a normal
distrbution.

In summary:

* p-value <= alpha: data *is not* normally distributed
* p-value > alpha: data *is* normally distributed

The value of the ``alpha`` threshold can be adjusted using the ``-a/--alpha`` argument:

.. code-block:: text

    gurita normtest --alpha 0.06 < iris.csv 

The above command produces the following output:

.. literalinclude:: example_outputs/iris.normtest.alpha.txt
   :language: none

Note that the ``sepal_length`` column is no longer considered normally distributed when alpha is 0.06 (previously it was considered normal when alpha was equal to the defualt of 0.05). This suggests that the our confidence of ``sepal_length`` being normally distributed is not as strong as it is for
``sepal_width``.

.. _normtest_pvalue:
.. _normtest_statistic:

Report the p-value and/or the test statistic in the output
----------------------------------------------------------

.. code-block:: text

   -p, --pvalue
   -s, --stat            

By default Gurita does not show the p-value or the test statistic in the output data.

This behaviour can be changed with ``-p/--pvalue``, which causes the p-value to be included in the output, and ``-s/--stat`` which causes the test statistic to be included in the output.

.. code-block:: text

    gurita normtest --pvalue --stat < iris.csv 

The output of the above command is shown below:

.. literalinclude:: example_outputs/iris.normtest.pvalue.stat.txt
   :language: none

.. _normtest_method:

Choose the method for testing normality
---------------------------------------

.. code-block:: text

   -m {dagostino,shapiro}, --method {dagostino,shapiro} 

By default `D'Agostino's K^2 test <https://en.wikipedia.org/wiki/D%27Agostino%27s_K-squared_test>`_ is applied.
However, it is also possible to use the `Shapiro-Wilk test <https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test>`_ instead. 

The ``-m/--method`` option allows the method to be specified, and can be either ``dagostino`` (the default) or ``shapiro``.

The following example illustrates the use of the Shapiro-Wilk test:

.. code-block:: text

    gurita normtest --method shapiro < iris.csv 

The output of the above command is shown below:

.. literalinclude:: example_outputs/iris.normtest.method.shapiro.txt
   :language: none
    
In this case we can see that under default parameters the ``sepal_length`` column is not considered normally distributed, whereas it was 
using the D'Agostino's K^2 test.
