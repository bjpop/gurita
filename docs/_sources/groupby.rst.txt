.. _groupby:

groupby
=======

Group data using one or more columns as keys and apply one or more aggregating functions to selected columns within each group.

Usage
-----

.. code-block:: text

    gurita groupby [-h] [-f FUNCTION [FUNCTION ...]] [-v COLUMN [COLUMN ...]]
                   -k COLUMN [COLUMN ...] 

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
     - :ref:`help <groupby_help>`
   * - * ``-k COLUMN [COLUMN...]``
       * ``--key COLUMN [COLUMN...]``
     - group data using these columns as the key 
     - :ref:`group key <groupby_key>`
   * - * ``-v COLUMN [COLUMN...]``
       * ``--val COLUMN [COLUMN...]``
     - apply aggregating functions to each of these numerical columns 
     - :ref:`aggregate values <groupby_val>`
   * - * ``-f FUNCTION [FUNCTION ...]``
       * ``--fun FUNCTION [FUNCTION ...]``
     - aggregation function(s) to apply to selected columns in the group
     - :ref:`aggregating function <groupby_fun>`

The ``--key`` (or ``-k``) argument is required. All others are optional.
Both ``--val`` (or ``-v``) and ``--fun`` (or ``-f``) must be used together, if they are used at all.

Simple example
--------------

In the following example the ``titanic.csv`` dataset is grouped using the ``embark_town`` column as the key.

.. code-block:: text

     gurita groupby --key embark_town < titanic.csv 

All rows in the dataset that have the same value in the ``embark_town`` column are grouped together. 

There are 3 unique towns in that column, so the output has 3 corresponding data rows:

.. code-block:: text

    embark_town,size
    Cherbourg,168
    Queenstown,77
    Southampton,644

By default the size of the groups is computed and included in the output as an extra column.

It is also possible to specify an :ref:`aggregating function <groupby_fun>` to apply to the groups.

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

One or more columns can be selected as the keys for grouping data using the ``--key`` (or ``-k``) argument. Rows will be grouped together
using equality on the values in the key columns. 

.. note::

   Groups are based on rows sharing a unique set of values from the ``--key`` columns. Thus key values are compared and grouped based on their *equality*.

   It is possible to have a mixture of categorical, numerical and boolean columns as keys. 

As an example, the ``titanic.csv`` dataset has a ``embark_town`` column with three possible values: ``Cherbourg`` and ``Queenstown`` and ``Southhampton``.

The simple example above showed how to compute the size of each of those groups. We can extend this example by grouping on another column. 
For example, we might like to know how the number of people in each ticket class for each of the
towns:

.. code-block:: text

     gurita groupby --key embark_town class < titanic.csv 

The output of the above command is as follows:

.. code-block:: text

   embark_town,class,size
   Cherbourg,First,85
   Cherbourg,Second,17
   Cherbourg,Third,66
   Queenstown,First,2
   Queenstown,Second,3
   Queenstown,Third,72
   Southampton,First,127
   Southampton,Second,164
   Southampton,Third,353

Now there are nine groups in the result - we have three unique towns, and each of those towns boarded passengers from three unique ticket classes.

We can extend this even further by using ``sex`` as another key column:

.. code-block:: text

    gurita groupby --key embark_town class sex < titanic.csv

The output of the above command is as follows:

.. code-block:: text

   embark_town,class,sex,size
   Cherbourg,First,female,43
   Cherbourg,First,male,42
   Cherbourg,Second,female,7
   Cherbourg,Second,male,10
   Cherbourg,Third,female,23
   Cherbourg,Third,male,43
   Queenstown,First,female,1
   Queenstown,First,male,1
   Queenstown,Second,female,2
   Queenstown,Second,male,1
   Queenstown,Third,female,33
   Queenstown,Third,male,39
   Southampton,First,female,48
   Southampton,First,male,79
   Southampton,Second,female,67
   Southampton,Second,male,97
   Southampton,Third,female,88
   Southampton,Third,male,265

Missing values in the key columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the ``--key`` columns contain missing (NA) values then the corresponding group will be dropped.

.. _groupby_val:
.. _groupby_fun:

Aggregate data within groups
----------------------------

.. code-block:: text

   -f FUNCTION [FUNCTION...] 
   --fun FUNCTION [FUNCTION...]

   -v COLUMN [COLUMN...]
   --val COLUMN [COLUMN...]

By default Gurita computes the size (number of rows) of each group. However it is also possible to aggregate over particular
columns within each group using one or more functions.

This is achieved by selecting columns using ``--val`` (or ``-v``) and specifying aggregating functions using ``--fun`` (or ``-f``).

.. note::

   If you want to aggregate data within groups you must supply both of the ``--val`` and ``--fun`` options in the command. 
   It is not possible to supply only one of these without the other.

For example, we could group rows in ``titanic.csv`` by the ``embark_town`` column and compute the mean age of passengers for each group like so:

.. code-block:: text

    gurita groupby --key embark_town --val age --fun mean < titanic.csv

The output of the above command is as follows, with the new aggregated column called ``age_mean``:

.. code-block:: text

    embark_town,age_mean
    Cherbourg,30.81476923076923
    Queenstown,28.089285714285715
    Southampton,29.44539711191336

As demonstrated in this example, when aggregating data within groups,
new column names are created using the name of the ``--val`` column concatenated with the ``--fun`` name, and separated by an underscore.

Extending this further, we could also compute the maximum and minimum age of passengers per town by adding extra functions to the ``--fun`` argument:

.. code-block:: text

    gurita groupby --key embark_town --val age --fun mean max min < titanic.csv

The output of the above command is as follows, with extra columns ``age_max`` and ``age_min``:

.. code-block:: text

    embark_town,age_mean,age_max,age_min
    Cherbourg,30.81476923076923,71.0,0.42
    Queenstown,28.089285714285715,70.5,2.0
    Southampton,29.44539711191336,80.0,0.67

And yes, there are some unusual fractional ages in the dataset - the minimum age of Cherbourg passengers really is 0.42.

It is also possible to specify multiple columns for aggregation:

.. code-block:: text

    gurita groupby --key embark_town --val age fare --fun mean max min < titanic.csv

In this scenario each ``--val`` column is aggregated by each ``--fun`` function. In the above example 2 columns are aggregated by
3 functions, yielding 6 additional output columns for each group:

.. code-block:: text

   embark_town,age_mean,age_max,age_min,fare_mean,fare_max,fare_min
   Cherbourg,30.81476923076923,71.0,0.42,59.95414404761905,512.3292,4.0125
   Queenstown,28.089285714285715,70.5,2.0,13.27602987012987,90.0,6.75
   Southampton,29.44539711191336,80.0,0.67,27.079811801242233,263.0,0.0

It is also possible to group on multiple columns and aggregate on multiple other columns at the same time, for example:

.. code-block:: text

   gurita groupby --key embark_town class --val age fare --fun mean max min < titanic.csv

The above command yields the following output:

.. code-block:: text

    embark_town,class,age_mean,age_max,age_min,fare_mean,fare_max,fare_min
    Cherbourg,First,38.027027027027025,71.0,16.0,104.71852941176472,512.3292,26.55
    Cherbourg,Second,22.766666666666666,36.0,1.0,25.358335294117648,41.5792,12.0
    Cherbourg,Third,20.741951219512195,45.5,0.42,11.214083333333333,22.3583,4.0125
    Queenstown,First,38.5,44.0,33.0,90.0,90.0,90.0
    Queenstown,Second,43.5,57.0,30.0,12.35,12.35,12.35
    Queenstown,Third,25.9375,70.5,2.0,11.183393055555555,29.125,6.75
    Southampton,First,38.15203703703704,80.0,0.92,70.3648622047244,263.0,0.0
    Southampton,Second,30.38673076923077,70.0,0.67,20.327439024390245,73.5,0.0
    Southampton,Third,25.69655172413793,74.0,1.0,14.64408300283286,69.55,0.0

Allowed aggregation functions 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following aggregating functions can be used with ``--fun``:

* sample (randomly choose one of the possible values)
* size (size of the group)
* sum
* mean
* mad (mean absolute deviation)
* median
* min
* max
* prod
* std (standard deviation)
* var (variance)
* sem (standard error of the mean)
* skew
* quantile (50% quantile)
