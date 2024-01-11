.. _describe: 

describe
========

Print summary statistics of the columns in a dataset to standard output (stdout).

The summary includes the following information:

* count: the number of non-empty data values observed for the column

For categorical columns:

* unique: the number of unique values observed for the column 
* top: the most frequently observed value
* freq: the frequency (count) of the most frequently observed value

For numerical columns:

* mean: the mean (average)
* std: the standard deviation
* min: the minimum observed value
* 25%: the 25th percentile
* 50%: the 50th percentile
* 75%: the 75th percentile
* max: the maximum observed value

Usage
-----

.. code-block:: bash

   gurita describe [-h] [-c [COLUMN ...]]  

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
     - :ref:`help <describe_help>`
   * - * ``-c [COLUMN ...]``
       * ``--col [COLUMN ...]``
     - select columns to describe (default is all columns) 
     - :ref:`columns <describe_columns>`

See also
--------

The :doc:`pretty <pretty/>` command prints a fragment of the dataset in an aligned tabular format to standard output. 


Simple example
--------------

Describe all the columns in the ``titanic.csv`` file:

.. code-block:: text 

   gurita describe < titanic.csv

The output for the above command is as follows:

.. literalinclude:: example_outputs/titanic.describe.txt
   :language: none

.. _describe_help:

Getting help
------------
   
The full set of command line arguments for ``describe`` can be obtained with the ``-h`` or ``--help``
arguments:
     
.. code-block:: text
   
    gurita describe -h

.. _describe_columns: 

Select specific columns to describe
-----------------------------------

.. code-block::

  -c [COLUMN ...], --col [COLUMN ...]

By default ``describe`` prints information about all columns in a dataset.

Alternatively, a subset of the columns can be selected using the ``-c/--col`` argument.

As an example, The following commmand only shows summary information for the ``age`` and ``class`` columns in the file ``titanic.csv``:

.. code-block:: bash

    gurita describe --col age class < titanic.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/titanic.describe.age.txt
   :language: none

Usage in a command chain
------------------------

When used in a command chain the ``describe`` command passes on its input data to the rest of the chain unchanged. 
 
For example, the following command shows ``describe`` followed by a ``box`` plot:

.. code-block:: text

   gurita describe + box -x sex -y age < titanic.csv

This command will first run ``describe`` to display a summary of the data on the output, and then it will run ``box`` to generate a plot on the same input data. 

Because ``describe`` just passes the data along from left to right the ``box`` command receives the same data as its input that was read from the file.

It is also worth noting that ``describe`` can be used after other transformations have been applied to the data. For example, the data can be filtered first, and then the result of filtering can be fed into ``describe``:

.. code-block:: text

   gurita filter 'age >= 30' + describe < titanic.csv

The output of the above command is as follows:

.. literalinclude:: example_outputs/titanic.filter.30.describe.txt
   :language: none

Notice that the minimal value of ``age`` is now 30.
