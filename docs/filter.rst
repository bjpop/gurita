Filtering rows
**************

Input rows can be filtered using the ``--filter EXPR`` option, where ``EXPR`` is a logical (boolean) expression that determines which rows are retained. 

Example:

.. code-block:: bash

   hatch hist --filter 'embark_town == "Cherbourg"' -x age titanic.csv

In the example above, a histogram will be generated for the ``age`` column in ``titanic.csv``, but only for rows where ``embark_town`` is equal to the string ``"Cherbourg"``. 

Columns can be referred to by their name, such as ``embark_town``. Literal categorical values are written as strings inside quotation marks, such as ``"Cherbourg"``.

Filter expression syntax
========================

Hatch row filtering uses the same syntax as the `Pandas data frame query method <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html>`_, and generally resembles
Python notation.

You can refer to column headings (feature names) in the input data by name, join multiple sub-expressions together using logical operators ``and`` ``or`` and ``not``, and group sub-expressions with parentheses. 

Filtering on numerical features 
-------------------------------

Numerical features can be compared for equality and also ordering. Numerical literals are written using Python syntax.

.. code-block:: bash

    hatch hist --filter 'fare <= 100' -x age titanic.csv

In the example above, a histogram will be generated for the ``age`` column in ``titanic.csv``, but only for rows where ``fare`` is less than or equal to ``100``. 

Filtering on categorical features 
---------------------------------

Categorical literals (but not booleans) are written as quoted strings.

.. code-block:: bash

    hatch hist --filter 'who != "child"' -x age titanic.csv

In the example above, a histogram will be generated for the ``age`` column in ``titanic.csv``, but only for rows where ``who`` is not equal to ``"child"`` (in other words only for adults). 

Filtering on boolean features 
-----------------------------

Boolean literals are written with a capital first letter, as they are done in Python. Note that boolean literals are not quoted.

.. code-block:: bash

    hatch hist --filter 'adult_male == True' -x age titanic.csv

In the example above, a histogram will be generated for the ``age`` column in ``titanic.csv``, but only for rows where ``adult_male`` is ``True``.

Note that it is redundant to compare boolean features to literal truth values. The same result in the above example can be achieved as follows:

.. code-block:: bash

    hatch hist --filter 'adult_male' -x age titanic.csv

Boolean features can be negated with ``not``:

.. code-block:: bash
 
    hatch hist --filter 'not adult_male' -x age --show titanic.csv

In the example above, a histogram will be generated for the ``age`` column in ``titanic.csv``, but only for rows where ``adult_male`` is ``False``.


Compound filter expressions
---------------------------


Comparing features
------------------
