.. _tail:

tail
====

Select a number of data rows from the end (bottom) of the input data set, return the result as a new table.

Compare to the :doc:`head <head/>` command that returns rows from the start (top) of the data instead of the end.

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help for this command
     - :ref:`help <tail_help>`
   * - ``NUM``
     - the number of rows to select 
     - :ref:`number of rows <tail_num>`


Simple example
--------------

In the following document we assume the existence of an input file called ``example.csv`` that contains the following data (10 data rows and 1 heading row):

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,setosa
    4.7,3.2,1.3,0.2,setosa
    4.6,3.1,1.5,0.2,setosa
    5.0,3.6,1.4,0.2,setosa
    5.4,3.9,1.7,0.4,setosa
    4.6,3.4,1.4,0.3,setosa
    5.0,3.4,1.5,0.2,setosa
    4.4,2.9,1.4,0.2,setosa
    4.9,3.1,1.5,0.1,setosa

Select the last 5 rows from ``example.csv`` :

.. code-block:: text 

    gurita tail 5 < example.csv 

The output of the above command is:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.4,3.9,1.7,0.4,setosa
    4.6,3.4,1.4,0.3,setosa
    5.0,3.4,1.5,0.2,setosa
    4.4,2.9,1.4,0.2,setosa
    4.9,3.1,1.5,0.1,setosa

Note that there are 5 data rows in the above result *plus* one header row.

The ``tail`` command returns a data set as its output, so it can be combined with other commands in a chain using the ``+`` operator.

For example the following command uses ``tail`` to select the last 5 rows from the input data *and then* uses ``head`` to select the first 3 rows from the last 5. The net result is that rows 6,7,8 (counting from 1) of the original data are returned.

.. code-block:: text

    gurita tail 5 + head 3 < example.csv

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.4,3.9,1.7,0.4,setosa
    4.6,3.4,1.4,0.3,setosa
    5.0,3.4,1.5,0.2,setosa


.. _tail_help:

Getting help
------------

The full set of command line arguments for ``tail`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita tail -h

.. _tail_num:

Specifying the number of rows to select
---------------------------------------

The tail command takes exactly one argument, an integer ``NUM``. 

 * If ``NUM > 0``, rows will be selected from the *end* (bottom) of the data. If ``NUM`` is greater than or equal to the number of rows in the data then the entire input data will be returned as the result.
 * If ``NUM = 0``, the result will be an empty data set.
 * If ``NUM < 0``, select all rows *except* the first ``NUM`` rows of the data. If ``NUM`` is greater than or equal to the number of rows in the data then the result will be an empty data set.

Select the first 1 rows from ``example.csv``:

.. code-block:: text 

    gurita tail 1 < example.csv 

The output of the above command is:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    4.9,3.1,1.5,0.1,setosa

Select all but the first 3 lines from ``example.csv``. Note that this yields the last 7 data rows of the data because there are 10 data rows in total and the first 3 are removed.

.. code-block:: text 

    gurita tail -3 < example.csv 

The output of the above command is:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    4.6,3.1,1.5,0.2,setosa
    5.0,3.6,1.4,0.2,setosa
    5.4,3.9,1.7,0.4,setosa
    4.6,3.4,1.4,0.3,setosa
    5.0,3.4,1.5,0.2,setosa
    4.4,2.9,1.4,0.2,setosa
    4.9,3.1,1.5,0.1,setosa
