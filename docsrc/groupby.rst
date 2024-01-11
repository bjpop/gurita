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

.. literalinclude:: example_outputs/titanic.groupby.embark_town.txt
   :language: none

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

.. literalinclude:: example_outputs/titanic.groupby.embark_town.class.txt
   :language: none

Now there are nine groups in the result - we have three unique towns, and each of those towns boarded passengers from three unique ticket classes.

We can extend this even further by using ``sex`` as another key column:

.. code-block:: text

    gurita groupby --key embark_town class sex < titanic.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/titanic.groupby.embark_town.class.sex.txt
   :language: none

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

.. literalinclude:: example_outputs/titanic.groupby.embark_town.age.mean.txt
   :language: none

As demonstrated in this example, when aggregating data within groups,
new column names are created using the name of the ``--val`` column concatenated with the ``--fun`` name, and separated by an underscore.

Extending this further, we could also compute the maximum and minimum age of passengers per town by adding extra functions to the ``--fun`` argument:

.. code-block:: text

    gurita groupby --key embark_town --val age --fun mean max min < titanic.csv

The output of the above command is as follows, with extra columns ``age_max`` and ``age_min``:

.. literalinclude:: example_outputs/titanic.groupby.embark_town.age.mean.max.min.txt
   :language: none

And yes, there are some unusual fractional ages in the dataset - the minimum age of Cherbourg passengers really is 0.42.

It is also possible to specify multiple columns for aggregation:

.. code-block:: text

    gurita groupby --key embark_town --val age fare --fun mean max min < titanic.csv

In this scenario each ``--val`` column is aggregated by each ``--fun`` function. In the above example 2 columns are aggregated by
3 functions, yielding 6 additional output columns for each group:

.. literalinclude:: example_outputs/titanic.groupby.embark_town.age.fare.mean.max.min.txt
   :language: none

It is also possible to group on multiple columns and aggregate on multiple other columns at the same time, for example:

.. code-block:: text

   gurita groupby --key embark_town class --val age fare --fun mean max min < titanic.csv

The above command yields the following output:

.. literalinclude:: example_outputs/titanic.groupby.embark_town.class.age.fare.mean.max.min.txt
   :language: none

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
