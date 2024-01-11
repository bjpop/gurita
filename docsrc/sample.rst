.. _sample:

sample
======

Randomly sample rows, either a fixed number or a fraction of the rows in the dataset.

Usage
-----

.. code-block:: text

   gurita sample [-h] NUM

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
     - :ref:`help <sample_help>`
   * - ``NUM``
     - number or fraction of rows to sample 
     - :ref:`sample number or fraction <sample_num>`


Simple example
--------------

The example below randomly samples 10 rows from the ``iris.csv`` dataset:

.. code-block:: text

   gurita sample 10 < iris.csv

The output of the above command is as follows: 

.. literalinclude:: example_outputs/iris.sample.10.txt
   :language: none

The example below randomly samples 0.05 (20%) of the rows from the ``iris.csv`` dataset:

.. code-block:: text

   gurita sample 0.05 < iris.csv

The output of the above command is as follows: 

.. literalinclude:: example_outputs/iris.sample.05.txt
   :language: none

.. note::

   Due to the randomisation of sampling, mulitple runs of the same command may pick different rows. 

.. _sample_help:

Getting help
------------

The full set of command line arguments for ``sample`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita sample -h

.. _sample_num:

Number or fraction of rows to sample
------------------------------------

The ``sample`` command takes one non-negative numerical argument ``NUM``. Either a fixed number of rows or a fraction of rows will be sampled:

* ``NUM >= 1``: the argument specifies a fixed number of rows to sample 
* ``0 <= NUM < 1``: the argument specifies a fraction of the number of rows from the input data to be sampled 

.. note::

   The maximum number of rows you can randomly sample is bounded by the total number of rows in the input file. 
   If you ask to randomly sample more than the total number of rows, no sampling will be done, and all the input rows will be used. 
