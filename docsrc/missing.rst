.. _missing_values:

Missing values
==============

Hatch supports data sets with missing values. 

Hatch uses `Pandas <https://pandas.pydata.org/>`_ to read, write and manipulate tabular data, and therefore inherits its behaviour for handling missing values from that library.

The `working with missing data <https://pandas.pydata.org/docs/user_guide/missing_data.html>`_ page in the Pandas documentation contains useful background information on this topic.

One of the most important consequences is that missing values are stored internally as ``NaN`` 
(standing for `not a number <https://en.wikipedia.org/wiki/NaN>`_, it is a special code that is used to encode undefined or unrepresentable values).

Missing values in input data
----------------------------

Here is the contents of a small example CSV file that has two missing values:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,
    4.9,3.0,1.4,0.2,virginica
    4.7,,1.3,0.2,setosa

The first data row is missing a categorical value in the ``species`` column. This is indicated by the comma occurring at the end of the line -- there is no final value in the last column on the first data row.

The third data row is missing a numerical value in the ``sepal_width`` column. This is indicated by two adjacent commas without in intervening value between them.

Default symbols for missing data in input files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default the following values are interpreted as missing values in input data: the empty string, ``#N/A``, ``#N/A N/A``, ``#NA``, ``-1.#IND`` ``-1.#QNAN``, ``-NaN``, ``-nan``, ``1.#IND``, ``1.#QNAN``, ``<NA>``, ``N/A``, ``NA``, ``NULL``, ``NaN``, ``n/a``, ``nan``, ``null``.

Using ``N/A`` and ``null`` to represent missing values, the above data equivalently be represented in the input file in the following way:

.. code-block:: text 

   sepal_length,sepal_width,petal_length,petal_width,species
   5.1,3.5,1.4,0.2,N/A
   4.9,3.0,1.4,0.2,virginica
   4.7,null,1.3,0.2,setosa

In this case ``N/A`` is used on the first data row to indicate a missing ``species`` value, and ``null`` is used on the third data row to indicate a missing ``sepal_length`` value. It is not common to mix and match different representations of missing values in the one data set, so this example is a bit unusual. However, it does show that it is possible.

Specifying symbols to use for missing data in input files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can override the default symbols used for representing missing data in input files using the ``--navalues`` argument to the ``in`` command.

For example, suppose you want to use the symbols ``-`` (a single dash), ``NA`` and the empty string as symbols for missing values, then you can specify this as follows:

.. code-block:: text 

   cat example.csv | hatch in --navalues '-' '' 'NA'

Note than when ``--navalues`` is used the default missing value symbols no longer apply, and only those symbols given as arguments to ``--navalues`` will be used to represent missing values.

Missing values in output data
-----------------------------

When writing a data set as output, by default Hatch will use empty fields to indicate missing values. However, this can be overridden with the ``--na <str>`` argument, where ``<str>>`` will be used to indicate a missing value.

For example, suppose that the previous small data set with missing values is stored in a file called ``missing.csv``. The following command will feed the contents of that file into the standard input of Hatch, which will then write the file back out to standard output with missing values indicated by 
underscores:

.. code-block:: text 

    cat missing.csv | hatch out --na '_'

The resulting data will be represented like so:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,_
    4.9,3.0,1.4,0.2,virginica
    4.7,_,1.3,0.2,setosa
