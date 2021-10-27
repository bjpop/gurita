Filtering rows
**************

Input rows can be filtered using the ``--filter EXPR`` option, where ``EXPR`` is a logical (boolean) expression that determines which rows are retained. 

Example:

.. code-block:: bash

   hatch hist --filter 'embark_town == "Cherbourg"' -x age titanic.csv

In the example above, the string ``'embark_town == "Cherbourg"'`` specifies the filtering expression. Note that the whole expression is inside quotes; this is necessary to ensure that the whole expression is passed as a single entity
to Hatch. In this case a histogram will be generated for the ``age`` column in ``titanic.csv``, but only for rows where ``embark_town`` is equal to the string ``"Cherbourg"``. 

Columns can be referred to by their name, such as ``embark_town``. Literal categorical values are written as strings inside quotation marks, such as ``"Cherbourg"``.

Filter expression syntax
========================

Hatch row filtering uses the same syntax as the `Pandas data frame query method <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html>`_, and generally resembles
Python notation.

You can refer to column headings (feature names) in the input data by name, join multiple sub-expressions together using logical operators ``and`` ``or`` and ``not``, and group sub-expressions with parentheses. 

Quoting feature names with spaces
---------------------------------

Features (column names) that contain spaces must be surrounded in back-tick quotes:

.. code-block:: bash

    hatch hist --filter '`top score` > 1000' -x time game.csv 

In the above example, the feature (column name) ``top score`` must be surrounded in back-tick quotes because it contains a whitespace character.

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
 
    hatch hist --filter 'not adult_male' -x age titanic.csv

In the example above, a histogram will be generated for the ``age`` column in ``titanic.csv``, but only for rows where ``adult_male`` is ``False``.

Comparing features
------------------

Filter expressions can compare values from different columns, assuming they have a compatible type (for example, numerical features may only be compared to other numerical features, and so forth).

.. code-block:: bash

   hatch hist --filter 'sepal_length > petal_length' -x sepal_width iris.csv

In the example above, a histogram will be generated for the ``sepal_width`` column in ``iris.csv``, but only for rows where the numerical feature ``sepal_length`` is greater than the numerical feature ``petal_length``.

Compound filter expressions
---------------------------

Multiple filtering crtieria can be combined into one filter expression by combining sub-expressions with boolean operators ``and`` and ``or``.

.. code-block:: bash

    hatch hist --filter 'smoker == "No" and total_bill > 10' -x tip tips.csv

In the example above, a histogram will be generated for the ``tip`` column in ``tips.csv``, but only for rows where the categorical feature ``smoker`` is ``"No"`` and the numerical feature ``total_bill`` is greater than 10.

If needed, parentheses can be used to group sub-expressions:

.. code-block:: bash

   hatch hist --filter 'smoker == "No" and (total_bill > 10 or day == "Sun")' -x tip tips.csv

In the above example, the sub-expression inside the parentheses is evaluated first, before the outer sub-expression.
