Heatmap
*******

Heatmap showing the relationship between two categorical features and a numerical feature.

.. code-block:: bash

    hatch heatmap <arguments>

Heatmap plots are based on Seaborn's `heatmap <https://seaborn.pydata.org/generated/seaborn.heatmap.html/>`_ library function.

.. list-table::
   :widths: 1 2 1
   :header-rows: 1

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help
     - :ref:`heatmap_help`
   * - ``-x FEATURE [FEATURE ...], --xaxis FEATURE [FEATURE ...]``
     - select feature for the X axis
     - :ref:`heatmap_feature_selection`
   * - ``-y FEATURE [FEATURE ...], --yaxis FEATURE [FEATURE ...]``
     - select feature for the Y axis
     - :ref:`heatmap_feature_selection`
   * - ``-v FEATURE [FEATURE ...], --val FEATURE [FEATURE ...]``
     - select intensity value for heatmap 
     - :ref:`heatmap_feature_selection`
   * - ``--cmap COLOR_MAP_NAME``
     - color map for the heat map 
     - :ref:`heatmap_cmap`

Simple example
==============

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

.. _heatmap_help:

Getting help
============

The full set of command line arguments for heatmap plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch heatmap -h

.. _heatmap_feature_selection:

Selecting features to plot
==========================

.. code-block:: 

  -x FEATURE [FEATURE ...], --xaxis FEATURE [FEATURE ...]
  -y FEATURE [FEATURE ...], --yaxis FEATURE [FEATURE ...]

Heatmap plots show an indepdent numerical feature on the X axis and a depdendent numerical feature on the Y axis.

You may specifiy multiple numerical features for both X and Y. 
Hatch will generate a separate plot for each combination of those features. 

.. _heatmap_hue:

Grouping features with hue 
==========================

.. code-block:: 

  --hue FEATURE [FEATURE ...]

The data can be grouped by a categorical feature with the ``--hue`` argument.

In the following example ``signal`` is plotted against ``timepoint`` for the two different classes of the ``event`` feature in the ``fmri.csv`` dataset:

.. code-block:: bash

    hatch heatmap -x timepoint -y signal --hue event -- fmri.csv

.. image:: ../images/fmri.signal.timepoint.event.heatmap.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Heatmap plot where signal is plotted against timepoint for the two different classes of the event feature  in the fmri.csv dataset.


You can specify more than one feature to group by; hatch will generate a separate heatmap plot for every ``hue`` feature specified.

.. _heatmap_hueorder:

By default the order of the columns within each hue group is determined from their occurrence in the input data. 
This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of columns within each hue group, based on their values. 

In the following example the classes of ``event`` are displayed in the order ``cue``, ``stim``:

.. code-block:: bash

        hatch heatmap -x timepoint -y signal --hue event --hueorder cue stim -- fmri.csv

.. image:: ../images/fmri.signal.timepoint.event.heatmap.hueorder.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Heatmap plot where signal is plotted against timepoint for the two different classes of the event feature in the fmri.csv dataset, using a specified hue order

.. _heatmap_log:

Log scale of numerical distribution 
===================================

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

It only makes sense to log-scale the numerical axis (and not the categorical axis). Therefore, ``--logx`` should be used when numerical features are selected with ``-x``, and
conversely, ``--logy`` should be used when numerical features are selected with ``-y``.

For example, you can display a log scale heatmap plot for the ``signal`` feature like so:

.. code-block:: bash

    hatch heatmap -x timepoint -y signal --logy -- fmri.csv 

.. _heatmap_range:

Range limits
============

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical distributions can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.

It only makes sense to range-limit the numerical axis (and not the categorical axis). Therefore, ``--xlim`` should be used when numerical features are selected with ``-x``, and
conversely, ``--ylim`` should be used when numerical features are selected with ``-y``.

For example, you can display range-limited range for the ``timepoint`` feature like so:

.. code-block:: bash

    hatch heatmap -x timepoint -y signal --xlim 7.5 12.5 -- fmri.csv 

.. _heatmap_facets:

Facets
======

.. code-block:: 

 --row FEATURE [FEATURE ...], -r FEATURE [FEATURE ...]
 --col FEATURE [FEATURE ...], -c FEATURE [FEATURE ...]
 --colwrap INT

Heatmap plots can be further divided into facets, generating a matrix of heatmap plots, where a numerical value is
further categorised by up to 2 more categorical features.

See the :doc:`facet documentation <facets/>` for more information on this feature.
