.. _sort:

sort
====

Sort rows in the dataset based on the values in specified columns.

Usage
-----

.. code-block:: text

   gurita sort [-h] -c COLUMN [COLUMN ...] [--napos {first,last}]
               [--order {a,d} [{a,d} ...]]
               [--alg {quicksort,mergesort,heapsort,stable}]

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
     - :ref:`help <sort_help>`
   * - * ``-c COLUMN [COLUMN...]``
       * ``--col COLUMN [COLUMN...]``
     - sort data by these columns 
     - :ref:`sort columns <sort_columns>`
   * - * ``-o ORDER [ORDER ...]``
       * ``--order ORDER [ORDER ...]``
     - ascending or descending sort order (default: ascending)
     - :ref:`sort order <sort_order>`
   * - ``--alg {quicksort,mergesort,heapsort,stable}``
     - algorithm to use for sort (default: quicksort) 
     - :ref:`sort algorithm <sort_algorithm>`
   * - ``--napos {first,last}``
     - ordering for missing (NA) values (default: first)
     - :ref:`NA order <sort_napos>`

The ``-c`` (``--col``) argument is required, and all other arguments are optional. 

Simple example
--------------

Suppose we are working with the following small data set with 10 data rows that is stored in a file called ``example.csv``:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    6.3,3.4,5.6,2.4,virginica
    6.3,2.5,5.0,1.9,virginica
    4.8,3.4,1.9,0.2,setosa
    6.3,3.3,4.7,1.6,versicolor
    6.4,3.2,4.5,1.5,versicolor
    4.7,3.2,1.3,0.2,setosa
    6.4,2.8,5.6,2.1,virginica
    5.4,3.9,1.7,0.4,setosa
    5.9,3.0,4.2,1.5,versicolor
    5.2,3.5,1.5,0.2,setosa

The command below sorts the rows of the data based on the values in the ``sepal_width`` row in ascending order:

.. code-block:: text

    gurita sort -c sepal_width < example.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    6.3,2.5,5.0,1.9,virginica
    6.4,2.8,5.6,2.1,virginica
    5.9,3.0,4.2,1.5,versicolor
    6.4,3.2,4.5,1.5,versicolor
    4.7,3.2,1.3,0.2,setosa
    6.3,3.3,4.7,1.6,versicolor
    6.3,3.4,5.6,2.4,virginica
    4.8,3.4,1.9,0.2,setosa
    5.2,3.5,1.5,0.2,setosa
    5.4,3.9,1.7,0.4,setosa

After sorting all rows are in ascending order according to their value in the ``sepal_width`` column.  
Categorical columns are sorted in alpha-numeric order, as is common in most applications.

For example, sorting on the categorical ``species`` column can be done like so:

.. code-block:: text

    gurita sort -c species < example.csv

producing the following output:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    4.8,3.4,1.9,0.2,setosa
    4.7,3.2,1.3,0.2,setosa
    5.4,3.9,1.7,0.4,setosa
    5.2,3.5,1.5,0.2,setosa
    6.3,3.3,4.7,1.6,versicolor
    6.4,3.2,4.5,1.5,versicolor
    5.9,3.0,4.2,1.5,versicolor
    6.3,3.4,5.6,2.4,virginica
    6.3,2.5,5.0,1.9,virginica
    6.4,2.8,5.6,2.1,virginica


.. _sort_help:

Getting help
------------

The full set of command line arguments for ``sort`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita sort -h

.. _sort_columns:

Selecting columns to use for sorting 
------------------------------------

.. code-block:: text

   -c COLUMN [COLUMN ...], --col COLUMN [COLUMN ...]

The ``sort`` command requires one or more columns to be specified.

Multi-column sorting behaves like most spreadsheet applications, where precedence goes from left to right in the order of the specified columns. 

The following example sorts first on ``sepal_width`` and then on ``species``:

.. code-block:: text

    gurita sort -c sepal_width species < example.csv

The relative order of rows that are tied on equal values of ``sepal_width`` will be determined by the corresponding values in the ``species`` column.

The result of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    6.3,2.5,5.0,1.9,virginica
    6.4,2.8,5.6,2.1,virginica
    5.9,3.0,4.2,1.5,versicolor
    4.7,3.2,1.3,0.2,setosa
    6.4,3.2,4.5,1.5,versicolor
    6.3,3.3,4.7,1.6,versicolor
    4.8,3.4,1.9,0.2,setosa
    6.3,3.4,5.6,2.4,virginica
    5.2,3.5,1.5,0.2,setosa
    5.4,3.9,1.7,0.4,setosa

Observe that the two rows with a ``sepal_length`` of ``3.2`` are sorted based on ``species`` such that ``setosa`` comes before ``versicolor``. Likewise, the two rows with a ``sepal_length`` of ``3.4`` are sorted based on ``species`` such that ``setosa`` comes before ``virginica``.

.. _sort_order:

Sorting in ascending or descending order
----------------------------------------

.. code-block:: text

   -o {a,d} [{a,d} ...], --order {a,d} [{a,d} ...]

By default rows are sorted in ascending order according to the values in the specified columns. However, this can be changed to descending order using the ``-o`` (or ``--order``) argument.  The direction of the ordering is given by the characters ``a`` (ascending) and ``d`` (descending).

The following command sorts the rows in descending order based on the values in the ``sepal_width`` column:

.. code-block:: text

    gurita sort -c sepal_width --order d < example.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    5.4,3.9,1.7,0.4,setosa
    5.2,3.5,1.5,0.2,setosa
    6.3,3.4,5.6,2.4,virginica
    4.8,3.4,1.9,0.2,setosa
    6.3,3.3,4.7,1.6,versicolor
    6.4,3.2,4.5,1.5,versicolor
    4.7,3.2,1.3,0.2,setosa
    5.9,3.0,4.2,1.5,versicolor
    6.4,2.8,5.6,2.1,virginica
    6.3,2.5,5.0,1.9,virginica

When sorting on multiple columns the ordering can be specified on a per-column basis.

The following command sorts rows in descending order based on the values in the ``sepal_width`` column and, when there are equal ties, it sorts in ascending order on values in the ``species`` column: 

.. code-block:: text

    gurita sort -c sepal_width species --order d a < example.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    5.4,3.9,1.7,0.4,setosa
    5.2,3.5,1.5,0.2,setosa
    4.8,3.4,1.9,0.2,setosa
    6.3,3.4,5.6,2.4,virginica
    6.3,3.3,4.7,1.6,versicolor
    4.7,3.2,1.3,0.2,setosa
    6.4,3.2,4.5,1.5,versicolor
    5.9,3.0,4.2,1.5,versicolor
    6.4,2.8,5.6,2.1,virginica
    6.3,2.5,5.0,1.9,virginica

.. note::

   The columns specified with ``-c`` (or ``--col``) and the ordering specified by ``-o`` (or ``--order``) match up pairwise.

   For example, in the scheme below, the order for column ``C1`` is given by ``O1``, and ``C2`` is ordered by ``O2``,  and so forth:

   .. code-block:: text

       gurita sort -c C1 C2 C3 -o O1 O2 O3

   Because of this notation and the fact that ordering defaults to ascending, it is only necessary to specify all orderings to the left of
   column ``CN``, where ``CN`` is the rightmost column with non-default ordering. Or in other words, it is redunant to specify
   ascending orderings on the rightmost columns. 

   For example the following command:

   .. code-block:: text

       gurita sort -c C1 C2 C3 -o a d a

   can be simplified to:

   .. code-block:: text

       gurita sort -c C1 C2 C3 -o a d

   because the rightmost column defaults to ascending, so there is no need to specify that explicitly.

.. _sort_algorithm:

Sorting algorithm
-----------------

.. code-block:: text

   --alg {quicksort,mergesort,heapsort,stable} 

By default data is sorted using the quicksort algorithm, however it is possible to choose from alternatives:

* quicksort (default)
* mergesort
* heapsort
* stable

For most use cases quicksort is likely to be the best choice, though do note that it can have poor runtime performance on data that is already mostly sorted. Also note that quicksort is not stable, as noted below.

.. note::

   Quicksort is *not* a stable sorting algorithm. This means that when there are ties for equal values, the output rows may not retain the same relative order as the input data.

   However, the sorting algorithm can be changed using the ``--alg`` option, and the 
   **mergesort** and **stable** algorithms are stable.

.. _sort_napos:

Ordering of missing (NA) values
-------------------------------

.. code-block:: text

   --napos {first,last}

Suppose that the example input data is modifed such that the first and last rows have missing values for ``sepal_length``:

.. code-block:: text

   sepal_length,sepal_width,petal_length,petal_width,species
   ,3.4,5.6,2.4,virginica
   6.3,2.5,5.0,1.9,virginica
   4.8,3.4,1.9,0.2,setosa
   6.3,3.3,4.7,1.6,versicolor
   6.4,3.2,4.5,1.5,versicolor
   4.7,3.2,1.3,0.2,setosa
   6.4,2.8,5.6,2.1,virginica
   5.4,3.9,1.7,0.4,setosa
   5.9,3.0,4.2,1.5,versicolor
   ,3.5,1.5,0.2,setosa

To sort the data on the ``speal_length`` column, we will need to decide what to do with the two rows with missing values.

By default Gurita will place rows with missing values at the end of the sorted data, like so:

.. code-block:: text

   gurita sort -c sepal_length < example.csv 

The output of the above command is as follows:

.. code-block:: text

   sepal_length,sepal_width,petal_length,petal_width,species
   4.7,3.2,1.3,0.2,setosa
   4.8,3.4,1.9,0.2,setosa
   5.4,3.9,1.7,0.4,setosa
   5.9,3.0,4.2,1.5,versicolor
   6.3,2.5,5.0,1.9,virginica
   6.3,3.3,4.7,1.6,versicolor
   6.4,3.2,4.5,1.5,versicolor
   6.4,2.8,5.6,2.1,virginica
   ,3.4,5.6,2.4,virginica
   ,3.5,1.5,0.2,setosa

Observe that the two rows with missing ``sepal_length`` values appear last in the sorted data.

The ``--napos`` argument tells Gurita how to handle rows with missing values in the sorted columns. 
Setting it to ``first`` will cause rows with missing values in the sorted columns to appear first in the sorted output.

.. code-block:: text

   gurita sort -c sepal_length --napos first < example.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    ,3.4,5.6,2.4,virginica
    ,3.5,1.5,0.2,setosa
    4.7,3.2,1.3,0.2,setosa
    4.8,3.4,1.9,0.2,setosa
    5.4,3.9,1.7,0.4,setosa
    5.9,3.0,4.2,1.5,versicolor
    6.3,2.5,5.0,1.9,virginica
    6.3,3.3,4.7,1.6,versicolor
    6.4,3.2,4.5,1.5,versicolor
    6.4,2.8,5.6,2.1,virginica

Observe that the two rows with missing ``sepal_length`` values appear first in the sorted data.

It is also possible to remove rows or columns that contain missing values based on certain criteria using 
the :doc:`dropna <dropna>` command.
