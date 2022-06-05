.. _heatmap:

heatmap
=======

Heatmap showing the relationship between two categorical features and a numerical feature.

.. code-block:: bash

    hatch heatmap <arguments>

Heatmap plots are based on Seaborn's `heatmap <https://seaborn.pydata.org/generated/seaborn.heatmap.html/>`__ library function.

.. list-table::
   :widths: 1 2 1
   :header-rows: 1

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help
     - :ref:`heatmap_help`
   * - ``-x FEATURE, --xaxis FEATURE``
     - select categorial feature for the X axis
     - :ref:`heatmap_feature_selection`
   * - ``-y FEATURE, --yaxis FEATURE``
     - select categorical feature for the Y axis
     - :ref:`heatmap_feature_selection`
   * - ``-v FEATURE, --val FEATURE``
     - select intensity value for heatmap 
     - :ref:`heatmap_feature_selection`
   * - ``--cmap COLOR_MAP_NAME``
     - color map for the heat map 
     - :ref:`heatmap_cmap`
   * - ``--log``
     - Use a log scale on the intensity value
     - :ref:`heatmap_log`


Simple example
--------------

Heatmap showing the number of ``passengers`` by ``month`` and ``year``
in the ``flights.csv`` data set:

.. code-block:: bash

    hatch heatmap -y year -x month -v passengers -- flights.csv  

The output of the above command is written to ``flights.month.year.passengers.heatmap.png``:

.. image:: ../images/flights.month.year.passengers.heatmap.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Heatmap showing the number of passengers by month and year in the flights.csv data set 

|

.. _heatmap_help:

Getting help
------------

The full set of command line arguments for heatmap plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch heatmap -h

.. _heatmap_feature_selection:

Selecting features to plot
--------------------------

.. code-block:: 

  -x FEATURE, --xaxis FEATURE 
  -y FEATURE, --yaxis FEATURE


.. _heatmap_cmap:

Colour palette
--------------

.. _heatmap_log:

Log scale
---------

.. code-block:: 

  --log

.. _heatmap_range:

