.. _filter:

filter
======

Filter rows using a logical expression that refers to the values in the columns. 

Rows that evaluate to ``True`` in the expression are retained and all other rows are discarded. 

Usage
-----

.. code-block:: text

   gurita filter [-h] EXPR  

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
     - :ref:`help <filter_help>`
   * - ``expression``
     - the expression to evaluate
     - :ref:`expression <filter_expression>`

The expression argument is required. If it contains spaces then it ought to be surrounded in quotes on the command line.

Simple example
--------------

The following example reads data from ``titanic.csv`` and retains only rows where ``embark_town`` is equal to ``Cherbourg``, all other rows are discarded: 

.. code-block:: text

   gurita filter 'embark_town == "Cherbourg"' <  titanic.csv 

The string ``'embark_town == "Cherbourg"'`` specifies the filtering expression. 

Note that the whole expression is inside quotes; this is necessary to ensure that the 
whole expression is passed as a single entity to Gurita.

Columns can be referred to by their name, such as ``embark_town``. Literal categorical values are written as strings inside quotation marks, such as ``"Cherbourg"``.

.. _filter_help:

Getting help
------------

The full set of command line arguments for ``filter`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita filter -h

.. _filter_expression:

Expressions
-----------

Row filtering uses the same syntax as the `Pandas data frame query method <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html>`_, and generally resembles
Python notation.

You can refer to column headings (column names) in the input data by name, join multiple sub-expressions together using logical operators ``and`` ``or`` and ``not``, and group sub-expressions with parentheses. 

Quoting column names with spaces
---------------------------------

Features (column names) that contain spaces must be surrounded in back-tick quotes:

.. code-block:: text

    gurita hist --filter '`top score` > 1000' -x time game.csv 

In the above example, the column (column name) ``top score`` must be surrounded in back-tick quotes because it contains a whitespace character.

Filtering on numerical columns 
-------------------------------

Numerical columns can be compared for equality (``==``), inequality (``!=``) and ordering (less than ``<``, greater than ``>``, less than or equals ``<=``, greater than or equals ``>=``). Numerical literals are written using Python syntax.

In the example below rows where the ``fare`` column is less than or equal to ``100`` are retained and all others are discarded:

.. code-block:: text 

    gurita filter 'fare <= 100' < titanic.csv

Filtering on categorical columns 
---------------------------------

Categorical literals (i.e. strings but not booleans) are written as quoted strings.

In the example below all rows where ``who`` is not equal to ``child`` 
are retained. Or, in other words,
all rows relating to children are discareded and only adults are retained.

.. code-block:: text

    gurita filter 'who != "child"' < titanic.csv

Note that the categorical value ``"child"`` is written inside quotes.

Filtering on boolean columns 
-----------------------------

Boolean literals are written with a capital first letter, as they are done in Python. Note that boolean literals are not quoted.

.. code-block:: text

    gurita filter 'adult_male == True' < titanic.csv

In the example above, only rows where ``adult_male`` is ``True`` are retained.

.. note::

    It is redundant to compare boolean columns to literal truth values. 
    
    Therefore the following two commands have the same behaviour: 

    .. code-block:: text
    
        gurita filter 'adult_male == True' < titanic.csv
    
    .. code-block:: text
    
        gurita filter 'adult_male' < titanic.csv

Boolean columns can be negated with ``not``:

.. code-block:: text
 
    gurita filter 'not adult_male' < titanic.csv

In the example above only rows where ``adult_male`` is ``False`` will be retained.

Comparing columns
------------------

Filter expressions can compare values from different columns, assuming they have a compatible type (for example, numerical columns may only be compared to other numerical columns, and so forth).

.. code-block:: text

   gurita filter 'sepal_length > petal_length' < iris.csv

In the example above only rows in ``iris.csv`` where ``sepal_length`` is greater than ``petal_length`` will be retained.

Compound filter expressions
---------------------------

Multiple filtering crtieria can be combined into one filter expression by combining sub-expressions with boolean operators ``and`` and ``or``.

.. code-block:: text

    gurita filter 'smoker == "No" and total_bill > 10' < tips.csv

In the example above only rows in ``tips.csv`` where the column ``smoker`` is ``"No"`` and the numerical column ``total_bill`` is greater than 10 will be retained.

If needed, parentheses can be used to group sub-expressions:

.. code-block:: text

   gurita filter 'smoker == "No" and (total_bill > 10 or day == "Sun")' < tips.csv

In the above example, the sub-expression inside the parentheses is evaluated first, before the outer sub-expression.
