.. _line:

line
====

Line plots show the relationship between two numerical features, 
optionally grouped by categorical features.

If multiple Y values are provided for each X value then the plot will show an estimate of the central tendency of X and confidence interval for the estimate.

.. code-block:: bash

    hatch line <arguments>

Line plots are based on Seaborn's `relplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_ library function, using the ``kind="line"`` option.

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help
     - :ref:`help <line_help>`
   * - * ``-x COLUMN``
       * ``--xaxis COLUMN``
     - select feature for the X axis
     - :ref:`X axis <line_feature_selection>`
   * - * ``-y COLUMN``
       * ``--yaxis COLUMN``
     - select feature for the Y axis
     - :ref:`Y axis <line_feature_selection>`
   * - ``--hue COLUMN``
     - group features by hue
     - :ref:`hue <line_hue>`
   * - ``--hueorder VALUE [VALUE ...]``
     - order of hue features
     - :ref:`hue order <line_hueorder>`
   * - ``--logx``
     - log scale X axis 
     - :ref:`log X axis <line_log>`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`log Y axis <line_log>`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`limit X axis <line_range>`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`limit Y axis <line_range>`
   * - * ``--row COLUMN``
       * ``-r COLUMN``
     - feature to use for facet rows 
     - :ref:`facet rows <line_facets>`
   * - * ``--col COLUMN``
       * ``-c COLUMN``
     - feature to use for facet columns 
     - :ref:`facet columns <line_facets>`
   * - ``--colwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`facet wrap <line_facets>`

Simple example
--------------

A line plot showing the relationship between ``timepoint`` on the X axis and ``signal`` on the Y axis for the ``fmri.csv`` dataset:

.. code-block:: bash

    hatch line -x timepoint -y signal < fmri.csv  

The output of the above command is written to ``line.timepoint.signal.png``.

.. image:: ../images/line.timepoint.signal.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: line plot showing the relationship between timepoint on the X axis and signal on the Y axis for the fmri.csv dataset

|

.. _line_help:

Getting help
------------

The full set of command line arguments for line plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch line -h

.. _line_feature_selection:

Selecting features to plot
--------------------------

.. code-block:: 

  -x COLUMN, --xaxis COLUMN
  -y COLUMN, --yaxis COLUMN

Line plots show an indepdent numerical feature on the X axis and a depdendent numerical feature on the Y axis.

.. _line_hue:

Grouping features with hue 
--------------------------

.. code-block:: 

  --hue COLUMN

The data can be grouped by a categorical feature with the ``--hue`` argument.

In the following example ``signal`` is plotted against ``timepoint`` for the two different classes of the ``event`` feature in the ``fmri.csv`` dataset:

.. code-block:: bash

    hatch line -x timepoint -y signal --hue event < fmri.csv

.. image:: ../images/line.timepoint.signal.event.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Line plot where signal is plotted against timepoint for the two different classes of the event feature  in the fmri.csv dataset.

|

.. _line_hueorder:

By default the order of the columns within each hue group is determined from their occurrence in the input data. 
This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of columns within each hue group, based on their values. 

In the following example the classes of ``event`` are displayed in the order ``cue``, ``stim``:

.. code-block:: bash

        hatch line -x timepoint -y signal --hue event --hueorder cue stim < fmri.csv

.. image:: ../images/line.timepoint.signal.event.hue.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Line plot where signal is plotted against timepoint for the two different classes of the event feature in the fmri.csv dataset, using a specified hue order

|

.. _line_log:

Log scale
---------

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

It only makes sense to log-scale the numerical axis (and not the categorical axis). Therefore, ``--logx`` should be used when numerical features are selected with ``-x``, and
conversely, ``--logy`` should be used when numerical features are selected with ``-y``.

For example, the X axis can be plotted in log scale like so:

.. code-block:: bash

   hatch line -x timepoint -y signal --logx < fmri.csv

.. image:: ../images/line.timepoint.signal.logx.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Line plot where signal is plotted against timepoint with the X axis in log scale 

|

.. _line_range:

Axis range limits
-----------------

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical distributions can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.

It only makes sense to range-limit the numerical axis (and not the categorical axis). Therefore, ``--xlim`` should be used when numerical features are selected with ``-x``, and
conversely, ``--ylim`` should be used when numerical features are selected with ``-y``.

For example, you can display range-limited range for the ``timepoint`` feature like so:

.. code-block:: bash

    hatch line -x timepoint -y signal --xlim 5 15.5 < fmri.csv 

.. image:: ../images/line.timepoint.signal.xlim.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Line plot where signal is plotted against timepoint with the X axis range limited to [5, 15.5] 

|

.. _line_facets:

Facets
------

.. code-block:: 

 --row COLUMN, -r COLUMN 
 --col COLUMN, -c COLUMN 
 --colwrap INT

Line plots can be further divided into facets, generating a matrix of line plots, where a numerical value is
further categorised by up to 2 more categorical features.

See the :doc:`facet documentation <facets/>` for more information on this feature.

The following command creates a faceted line plot where the ``event`` feature is used to determine the facet columns:

.. code-block:: bash

    hatch line -x timepoint -y signal --col event < fmri.csv 

.. image:: ../images/line.timepoint.signal.event.facet.png 
       :width: 600px
       :height: 300px 
       :align: center
       :alt: Line plot where signal is plotted against timepoint split into facets based on the event feature 

|
