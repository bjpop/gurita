.. _head:

head
====

Select a number of rows from the start (top) of the input data set, return the result as a new table.

Usage
-----

.. code-block:: text

   gurita head [-h] [NUM]

Arguments
---------

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help for this command
     - :ref:`help <head_help>`
   * - ``NUM``
     - the number of rows to select 
     - :ref:`number of rows <head_num>`

See also
--------

Compare to the :doc:`tail <tail/>` command that returns rows from the end (bottom) of the data instead of the start.

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

Select the first 5 rows from ``example.csv``:

.. code-block:: text 

    gurita head 5 < example.csv 

The output of the above command is:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,setosa
    4.7,3.2,1.3,0.2,setosa
    4.6,3.1,1.5,0.2,setosa
    5.0,3.6,1.4,0.2,setosa

Note that there are 5 data rows in the above result *plus* one header row.

The ``head`` command returns a data set as its output, so it can be combined with other commands in a chain using the ``+`` operator.

For example the following command uses ``head`` to select the first 5 rows from the input data *and then* uses ``tail`` to select the last 3 rows from the first 5. The net result is that rows 3,4,5 (counting from 1) of the original data are returned.

.. code-block:: text

    gurita head 5 + tail 3 < example.csv

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    4.7,3.2,1.3,0.2,setosa
    4.6,3.1,1.5,0.2,setosa
    5.0,3.6,1.4,0.2,setosa

.. _head_help:

Getting help
------------

The full set of command line arguments for ``head`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita head -h

.. _head_num:

Specifying the number of rows to select
---------------------------------------

The head command takes exactly one argument, an integer ``NUM``. 

 * If ``NUM > 0``, rows will be selected from the *start* (top) of the data. If ``NUM`` is greater than or equal to the number of rows in the data then the entire input data will be returned as the result.
 * If ``NUM = 0``, the result will be an empty data set.
 * If ``NUM < 0``, select all rows *except* the last ``NUM`` rows of the data. If ``NUM`` is greater than or equal to the number of rows in the data then the result will be an empty data set.

Select the first 1 rows from ``example.csv``:

.. code-block:: text 

    gurita head 1 < example.csv 

The output of the above command is:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa

Select all but the last 3 lines from ``example.csv``. Note that this yields the first 7 rows of the data because there are 10 rows in total and the last 3 are removed.

.. code-block:: text 

    gurita head -3 < example.csv 

The output of the above command is:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,setosa
    4.7,3.2,1.3,0.2,setosa
    4.6,3.1,1.5,0.2,setosa
    5.0,3.6,1.4,0.2,setosa
    5.4,3.9,1.7,0.4,setosa
    4.6,3.4,1.4,0.3,setosa
