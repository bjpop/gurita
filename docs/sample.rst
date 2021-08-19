Random sampling
***************

Input rows can be randomly sampled using the ``--sample NUM`` argument. If NUM >= 1 then sample NUM rows, otherwise if 0 <= NUM < 1, then sample NUM fraction of rows.

Example:

.. code-block:: bash

   hatch hist --sample 100 -x signal fmri.csv

In the example above a histogram is plotted of the ``signal`` feature using 100 randomly sampled rows from the input data.

Example:

.. code-block:: bash

   hatch hist --sample 0.1 -x signal fmri.csv

In the example above a histogram is plotted of the ``signal`` feature using 0.1 of the total rows randomly sampled from the input data.
