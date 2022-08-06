.. _describe: 

describe
========

Input data can be summarised with the ``describe`` command

.. code-block:: bash

    gurita describe <arguments>

This produces a summary table of columns in the input data. 

.. code-block:: bash

   gurita describe < titanic.csv

The output for the file ``titanic.csv`` is as follows:

.. code-block:: text

              survived      pclass   sex         age       sibsp       parch  \
    count   891.000000  891.000000   891  714.000000  891.000000  891.000000   
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
    
                  fare embarked  class  who adult_male deck  embark_town alive  \
    count   891.000000      889    891  891        891  203          889   891   
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

    rows: 891, cols: 15

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

The number of rows and columns in the input data is shown at the end. In this case there are 891 rows and 15 columns in
the ``titanic.csv`` file.


.. _info_trans: 

Summary information for transformed input data 
----------------------------------------------

As an example, The following commmand only shows summary information for the ``age`` and ``class`` columns in the file ``titanic.csv``:

.. code-block:: bash

    gurita describe --columns age class < titanic.csv

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
    
    rows: 891, cols: 2

Similarly it is possible to get summary information for data after ``--filter``, ``--eval``, and ``--sample`` have been applied to the data.
In all cases the summary shows that state of the data after the transformations have been applied.
