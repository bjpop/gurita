.. _melt:

melt
====

Reshape data from `wide format <https://en.wikipedia.org/wiki/Wide_and_narrow_data#Wide>`_ to `narrow format <https://en.wikipedia.org/wiki/Wide_and_narrow_data#Narrow>`_.

Sometimes wide format is called *stacked* and narrow format is called *un-stacked* or *long*.

For example here is a small table in *wide format* representing working hours for two employees on each weekday, where employees are also associated with a level:

.. code-block:: text

   person,level,mon,tue,wed,thu,fri
   Alice,A1,8,8,4,1,4
   Bob,B3,0,0,4,6,0

And here is the same data in *narrow format*, such that the ``person`` column is retained as an identifier for each data point:

.. code-block:: text

   person,variable,value
   Alice,level,A1
   Bob,level,B3
   Alice,mon,8
   Bob,mon,0
   Alice,tue,8
   Bob,tue,0
   Alice,wed,4
   Bob,wed,4
   Alice,thu,1
   Bob,thu,6
   Alice,fri,4
   Bob,fri,0

Columns from the wide format become stacked in the narrow format. Note how the column headings
``level``, ``mon``, ``tue``, ``wed``, ``thur`` and ``fri`` have become categorical values in
the ``variable`` column with their associated values in the ``value`` column.

Usage
-----

.. code-block:: text

   gurita melt [-h] [-i COLUMN [COLUMN ...]] [-v COLUMN [COLUMN ...]] [--varname NAME] [--valname NAME] 

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
     - :ref:`help <melt_help>`
   * - * ``-i COLUMN [COLUMN...]``
       * ``--ids COLUMN [COLUMN...]``
     - use these columns as identifiers 
     - :ref:`identifier columns <melt_identifier_columns>`
   * - * ``-v COLUMN [COLUMN...]``
       * ``--vals COLUMN [COLUMN...]``
     - use these columns as values 
     - :ref:`value columns <melt_value_columns>`
   * - ``--varname NAME``
     - use this name for the variable column (default: variable)
     - :ref:`variable column name <melt_variable_name>`
   * - ``--valname NAME``
     - use this name for the value column (default: value)
     - :ref:`value column name <melt_value_name>`

See also
--------

The inverse of ``melt`` is provided by the :doc:`pivot <pivot/>` command. 

Simple example
--------------

Suppose the following data is stored in a file called ``example.csv``:

.. code-block:: text

   person,level,sun,mon,tue,wed,thu,fri,sat
   Alice,A1,0,8,8,4,1,4,3
   Bob,B3,4,0,0,4,6,0,3
   Wei,B1,0,0,8,8,8,4,3
   Imani,A2,0,8,8,8,4,5,0
   Diego,C2,3,7,7,2,1,1,4

This is an example of data in "wide format".

The ``melt`` command can convert the data into "long format".

In the simplest form, each column heading is treated as a variable, and each corresponding datum is treated as a value.

.. code-block:: text

    gurita melt < example.csv

The output of the above command has 45 data rows. We can use ``head`` to look at the first 15 rows:  

.. code-block:: text

    gurita melt + head 15 < example.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/example.melt.head.15.txt
   :language: none

In this example the melted data consists entirely of variable-value pairs. However, this is not normally the most useful view of the data. 
More often we want to melt only some of the columns into variable-value pairs, and preserve other columns unchanged to act as a kind of unique identifier for each row (otherwise
known as a key).

For example, the following command retains the ``person`` column as an identifier for the rows, and melts the remaining columns into variable-value pairs:

.. code-block:: text

    gurita melt -i person < example.csv

The output of this command is quite long, so for the sake of illustration, we will update the command to consider only the first 15 rows:

.. code-block:: text

    gurita melt -i person + head 15 < example.csv

.. literalinclude:: example_outputs/example.melt.index.person.head.15.txt
   :language: none

Now the ``person`` column is retained and acts as a kind of identifier for the rows.

.. _melt_help:

Getting help
------------

The full set of command line arguments for ``melt`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita melt -h

.. _melt_identifier_columns:

Specifying columns to act as identifiers
----------------------------------------

.. code-block:: text

    -i COLUMN [COLUMN ...]
    --ids COLUMN [COLUMN ...]

By default ``melt`` will transform a data set into a collection of variable-value pairs. However, most of the time we want the transformed data to retain some columns to 
act as identifiers for the rows.

The ``-i/--ids`` argument allows you to specify one or more *identifier* columns.

For example, all columns are melted *except* ``person``, which is retained unchanged, and acts as an identifier for the output rows: 

.. code-block:: text

    gurita melt -i person < example.csv

The output of this command is quite long, so for the sake of illustration, we will update the command to consider only the first 15 rows:

.. code-block:: text

    gurita melt -i person + head 15 < example.csv

.. literalinclude:: example_outputs/example.melt.index.person.head.15.txt
   :language: none

It is possible to specify more than one column as an identifier. For example, in the following command, the columns ``person`` and ``level`` are both used as identifiers:

.. code-block:: text

    gurita melt -i person level < example.csv

Again, the output of this command is long, so we can update the command to look at the first 15 rows:

.. code-block:: text

    gurita melt -i person level + head 15 < example.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/example.melt.index.person.level.head.15.txt
   :language: none

Now, only the columns representing the days of the week are melted into variable-value pairs, whereas the ``person`` and ``level`` columns are retained in the output.

.. _melt_value_columns:

Specifying columns to melt
--------------------------

.. code-block:: text

    -v COLUMN [COLUMN ...]
    --vals COLUMN [COLUMN ...]

By default ``melt`` will convert all columns into variable-value pairs, except those specified as :ref:`identifiers <melt_identifier_columns>`.

The ``-v/--vals`` argument allows you to specify a subset of columns to be melted. In this circumstance any column not mentioned in this subset or as an identifier will be
excluded from the output.

For example, the following command melts just the columns ``level``, ``sat``, and ``sun``, and uses ``person`` as an identifer. All other columns are dropped.

.. code-block:: text

   gurita melt -i person -v level sat sun < example.csv

.. literalinclude:: example_outputs/example.melt.person.level.sat.sun.txt
   :language: none

.. _melt_variable_name:

Choose a name for the variable column
-------------------------------------

.. code-block:: text

   --varname NAME

By default the output column for melted variables is called ``variable``. However this behaviour can be changed by the ``--varname`` argument.

For example, the following command melts all columns in the the data and sets the output variable column to ``key``:

.. code-block:: text

   gurita melt --varname key < example.csv

The output of the above command is long, so for the sake of illustration we can update the command to output just the first 10 rows: 

.. code-block:: text

   gurita melt --varname key + head 10 < example.csv 

The output of the above command is as follows:

.. literalinclude:: example_outputs/example.melt.varname.key.head.10.txt
   :language: none

Note that the leftmost column is now called ``key`` instead of ``variable``.

.. _melt_value_name:

Choose a name for the value column
----------------------------------

.. code-block:: text

   --valname NAME

By default the output column for melted values is called ``value``. However this behaviour can be changed by the ``--valname`` argument.

For example, the following command melts all columns in the the data and sets the output value column to ``data``:

.. code-block:: text

   gurita melt --valname data < example.csv

The output of the above command is long, so for the sake of illustration we can update the command to output just the first 10 rows: 

.. code-block:: text

   gurita melt --valname data + head 10 < example.csv 

The output of the above command is as follows:

.. literalinclude:: example_outputs/example.melt.valname.data.head.10.txt
   :language: none

Note that the rightmost column is now called ``data`` instead of ``value``.

Of course it is possible to change both the variable and value column names at the same time, as the following example demonstrates:

.. code-block:: text

   gurita melt --varname key --valname data + head 10 < example.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/example.melt.varname.key.valname.data.head.10.txt
   :language: none
