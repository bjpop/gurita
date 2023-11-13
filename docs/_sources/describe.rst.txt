.. _describe: 

describe
========

Print a high level summary of the columns in a dataset to standard output (stdout).

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

Simple example
--------------

Describe all the columns in the ``titanic.csv`` file:

.. code-block:: text 

   gurita describe < titanic.csv

The output for the above command is as follows:

.. code-block:: text

             survived      pclass   sex         age       sibsp       parch   
   count   891.000000  891.000000   891  714.000000  891.000000  891.000000  \
   unique         NaN         NaN     2         NaN         NaN         NaN   
   top            NaN         NaN  male         NaN         NaN         NaN   
   freq           NaN         NaN   577         NaN         NaN         NaN   
   mean      0.383838    2.308642   NaN   29.699118    0.523008    0.381594   
   std       0.486592    0.836071   NaN   14.526497    1.102743    0.806057   
   min       0.000000    1.000000   NaN    0.420000    0.000000    0.000000   
   25%       0.000000    2.000000   NaN   20.125000    0.000000    0.000000   
   50%       0.000000    3.000000   NaN   28.000000    0.000000    0.000000   
   75%       1.000000    3.000000   NaN   38.000000    1.000000    0.000000   
   max       1.000000    3.000000   NaN   80.000000    8.000000    6.000000   
   
                 fare embarked  class  who adult_male deck  embark_town alive   
   count   891.000000      889    891  891        891  203          889   891  \
   unique         NaN        3      3    3          2    7            3     2   
   top            NaN        S  Third  man       True    C  Southampton    no   
   freq           NaN      644    491  537        537   59          644   549   
   mean     32.204208      NaN    NaN  NaN        NaN  NaN          NaN   NaN   
   std      49.693429      NaN    NaN  NaN        NaN  NaN          NaN   NaN   
   min       0.000000      NaN    NaN  NaN        NaN  NaN          NaN   NaN   
   25%       7.910400      NaN    NaN  NaN        NaN  NaN          NaN   NaN   
   50%      14.454200      NaN    NaN  NaN        NaN  NaN          NaN   NaN   
   75%      31.000000      NaN    NaN  NaN        NaN  NaN          NaN   NaN   
   max     512.329200      NaN    NaN  NaN        NaN  NaN          NaN   NaN   
   
          alone  
   count    891  
   unique     2  
   top     True  
   freq     537  
   mean     NaN  
   std      NaN  
   min      NaN  
   25%      NaN  
   50%      NaN  
   75%      NaN  
   max      NaN 

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

.. code-block:: text

                  age  class
   count   714.000000    891
   unique         NaN      3
   top            NaN  Third
   freq           NaN    491
   mean     29.699118    NaN
   std      14.526497    NaN
   min       0.420000    NaN
   25%      20.125000    NaN
   50%      28.000000    NaN
   75%      38.000000    NaN
   max      80.000000    NaN

Usage in a command chain
------------------------

When used in a command chain the ``describe`` command passes on its input data to the rest of the chain unchanged. 
 
For example, the following command shows ``describe`` followed by a ``box`` plot:

.. code-block:: text

   gurita describe + box -x sex -y age < titanic.csv

This command will first run ``describe`` to display a summary of the data on the output, and then it will run ``box`` to generate a plot on the same input data. 

Because ``describe`` just passes the data along from left to right the ``box`` command receives the same data as its input that was read from the file.
