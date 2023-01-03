.. _melt:

melt
====

Reshape data from `wide format <https://en.wikipedia.org/wiki/Wide_and_narrow_data#Wide>`_ to `narrow format <https://en.wikipedia.org/wiki/Wide_and_narrow_data#Narrow>`_.

Sometimes wide format is called *stacked* and narrow format is called *un-stacked* or *long*.

For example here is a small table in *wide format* representing working hours for two employees on each weekday:

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
