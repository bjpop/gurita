.. _groupby:

groupby
=======

Group data using one or more columns as keys and apply one or more aggregating functions to selected columns within each group.

.. code-block:: text

    gurita groupby <arguments>

Arguments
---------

.. list-table::
   :widths: 25 20 10 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Required
     - Reference
   * - * ``-h``
       * ``--help``
     - display help for this command
     - optional 
     - :ref:`help <groupby_help>`
   * - * ``-k COLUMN [COLUMN...]``
       * ``--key COLUMN [COLUMN...]``
     - group data using these columns as the key 
     - required 
     - :ref:`group key <groupby_key>`
   * - * ``-f FUNCTION [FUNCTION ...]``
       * ``--fun FUNCTION [FUNCTION ...]``
     - aggregation function(s) to apply to selected columns in the group
     - optional 
     - :ref:`aggregating function <groupby_fun>`
   * - * ``-v COLUMN [COLUMN...]``
       * ``--val COLUMN [COLUMN...]``
     - apply aggregating functions to each of these numerical columns 
     - optional 
     - :ref:`aggregate values <groupby_val>`

Simple example
--------------

In the following example the ``titanic.csv`` dataset is grouped by the ``embark_town`` column. This creates three groups, one for each unique town. Within each group the mean ``age`` of individuals is calculated.

.. code-block:: text

     gurita groupby --key embark_town --val age --fun mean < titanic.csv 

The output is a new table with two data rows, one for each group. The columns are ``embark_town`` and a new column called ``age_mean`` representing the computed mean age of individuals in each group. The name of the new column
is based on its name from the original data and the name of the function that was applied.

.. code-block:: text

   embark_town,age_mean
   Cherbourg,30.81476923076923
   Queenstown,28.089285714285715
   Southampton,29.44539711191336

.. _groupby_help:

Getting help
------------

The full set of command line arguments for ``groupby`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita groupby -h

.. _groupby_key:

Choose columns as the key for grouping data
-------------------------------------------

.. code-block:: text

   -k COLUMN [COLUMN...] 
   --key COLUMN [COLUMN...]

One of more columns can be selected as the keys for grouping data using the ``--key`` (or ``-k``) argument. Rows will be grouped together
using equality on the values in the key columns. 

.. note::

   Groups are based on rows sharing a unique set of values from the ``--key`` columns. Thus key values are compared and grouped based on their *equality*.

   It is possible to have a mixture of categorical and numerical columns as keys, but for numerical keys it usually only makes sense
   when those are integers. Be careful when keys include numerical columns that contain floating point (real) numbers.

As an example, the ``titanic.csv`` dataset has a ``embark_town`` column with three possible values: ``Cherbourg`` and ``Queenstown`` and ``Southhampton``.
The simple example above showed how to compute the mean age of passengers that embarked the titanic at each of those towns.

We can extend this example by grouping on another column. For example, we might like to know the mean age of passengers from each town broken down by
their ticket ``class``. This can be achieved by adding ``class`` as another column for the key argument:

.. code-block:: text

     gurita groupby --key embark_town class --val age --fun mean < titanic.csv 

The output of the above command is as follows:

.. code-block:: text

    embark_town,class,age_mean
    Cherbourg,First,38.027027027027025
    Cherbourg,Second,22.766666666666666
    Cherbourg,Third,20.741951219512195
    Queenstown,First,38.5
    Queenstown,Second,43.5
    Queenstown,Third,25.9375
    Southampton,First,38.15203703703704
    Southampton,Second,30.38673076923077
    Southampton,Third,25.69655172413793

Now there are nine groups in the result - we have three unique towns, and each of those towns boarded passengers from three unique ticket classes.

This analysis reveals that the third class ticket passengers were generally younger than the other classes. 

We can extend this even further by using ``sex`` as another key column:

.. code-block:: text

    gurita groupby --key embark_town class sex --val age --fun mean < titanic.csv

The output of the above command is as follows:

.. code-block:: text

    embark_town,class,sex,age_mean
    Cherbourg,First,female,36.05263157894737
    Cherbourg,First,male,40.111111111111114
    Cherbourg,Second,female,19.142857142857142
    Cherbourg,Second,male,25.9375
    Cherbourg,Third,female,14.0625
    Cherbourg,Third,male,25.0168
    Queenstown,First,female,33.0
    Queenstown,First,male,44.0
    Queenstown,Second,female,30.0
    Queenstown,Second,male,57.0
    Queenstown,Third,female,22.85
    Queenstown,Third,male,28.142857142857142
    Southampton,First,female,32.70454545454545
    Southampton,First,male,41.8971875
    Southampton,Second,female,29.71969696969697
    Southampton,Second,male,30.875888888888888
    Southampton,Third,female,23.223684210526315
    Southampton,Third,male,26.574766355140188

.. _groupby_fun:

Choose the aggregation functions to apply
-----------------------------------------

.. code-block:: text

   -f FUNCTION [FUNCTION...] 
   --fun FUNCTION [FUNCTION...]

By default, if no aggregating function is specified, Gurita will count the number of items in each group:

.. code-block:: text

    gurita groupby --key embark_town --val age

.. _groupby_val:

Choose columns to aggregate within the groups 
---------------------------------------------

