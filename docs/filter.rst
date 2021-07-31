Filtering rows
**************

Input rows can be filtered using the ``--filter EXPR`` option, where ``EXPR`` is a logical (boolean) expression that determines which rows are retained. 

Example:

.. code-block:: bash

   hatch hist --filter 'embark_town == "Cherbourg"' -x age -- titanic.csv


In this example, a histogram will be generated for the ``age`` column, but only for rows where ``embark_town`` is equal to the string ``"Cherbourg"``. 

Columns can be referred to by their name, such as ``embark_town``. Literal categorical values are written as strings inside quotation marks, such as ``"Cherbourg"``.

Filter expression syntax
------------------------

Hatch row filtering uses the same syntax as the `Pandas data frame query method <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html>`_, and generally resembles
Python notation.

You can refer to column headings (feature names) in the input data by name, join multiple sub-expressions together using logical operators ``and`` ``or`` and ``not``, and group sub-expressions with parentheses. 
