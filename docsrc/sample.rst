.. _sample:

sample
======

Input rows can be randomly sampled using the ``--sample NUM`` argument. If NUM >= 1 then sample NUM rows, otherwise if 0 <= NUM < 1, then sample NUM fraction of rows.

Example:

.. code-block:: bash

   hatch hist --sample 100 -x signal fmri.csv

In the example above a histogram is plotted of the ``signal`` column using 100 randomly sampled rows from the input data.

Example:

.. code-block:: bash

   hatch hist --sample 0.1 -x signal fmri.csv

In the example above a histogram is plotted of the ``signal`` column using 0.1 (as close as possible to one tenth) of the total rows randomly sampled from the input data.

.. note::

   Due to the randomisation of sampling, mulitple runs of the exact same command may yield different results.

.. note::

   The maximum number of rows you can randomly sample is bounded by the total number of rows in the input file. 
   If you ask to randomly sample more than the total number of rows, no sampling will be done, and all the input rows will be used. 
