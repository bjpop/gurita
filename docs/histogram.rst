Histogram
*********

Plot distributions of selected numerical or categorical features as histograms.

.. code-block:: bash

    hatch hist <arguments> 

Histograms are based on Seaborn's `histplot <https://seaborn.pydata.org/generated/seaborn.histplot.html/>`_ library function.

.. list-table::
   :widths: 1 2 1
   :header-rows: 1

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help 
     - :ref:`hist_help`
   * - ``-x FEATURE, --xaxis FEATURE``
     - select feature for the X axis 
     - :ref:`hist_feature_selection`
   * - ``-y FEATURE, --yaxis FEATURE`` 
     - select feature for the Y axis 
     - :ref:`hist_feature_selection`
   * - ``--bins NUM``
     - number of bins 
     - :ref:`hist_bins`
   * - ``--binwidth NUM``
     - width of bins, overrides ``--bins`` 
     - :ref:`hist_binwidth`
   * - ``--cumulative``
     - plot a cumulative histogram 
     - :ref:`hist_cumulative`
   * - ``--kde``
     - overlay a kernel density estimate (kde) as a line 
     - :ref:`hist_kde`
   * - ``--logx``
     - log scale X axis 
     - :ref:`hist_log`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`hist_log`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`hist_range`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`hist_range`
   * - ``-r FEATURE, --row FEATURE``
     - feature to use for facet rows 
     - :ref:`hist_facets`
   * - ``-c FEATURE, --col FEATURE``
     - feature to use for facet columns 
     - :ref:`hist_facets`
   * - ``--colwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`hist_facets`


.. _hist_example:

Simple example
==============

Plot a histogram of the ``tip`` amount from the ``tips.csv`` input file:

.. code-block:: bash

    hatch hist -x tip -- tips.csv

The output of the above command is written to ``tips.tip.hist.png``:

.. image:: ../images/tips.tip.hist.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set

.. _hist_help:

Getting help
============

The full set of command line arguments for histograms can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch hist -h

.. _hist_feature_selection:

Selecting features to plot
==========================

.. code-block:: 

  -x FEATURE, --xaxis FEATURE
                        Feature to plot along the X axis
  -y FEATURE, --yaxis FEATURE
                        Feature to plot along the Y axis

Histograms can be plotted for both numerical features and for categorical features. Numerical data is binned
and the histogram shows the counts of data points per bin. Catergorical data is shown as a count plot with a
column for each categorical value in the specified feature.

You can select the feature that you want to plot as a histogram using the ``-x`` (``--xaxis``) or ``-y`` (``--yaxis``)
arguments.

If ``-x`` (``--xaxis``) is chosen the histogram columns will be plotted vertically.

If ``-y`` (``--yaxis``) is chosen the histogram columns will be plotted horizontally.

.. note::

    You may not use both ``-x FEATURE`` and ``-y FEATURE`` in the same command line for histogram plots.

See :ref:`the example <hist_example>` above for a vertical axis plot.
For comparison, the following command uses ``-y tip`` to plot a histogram of ``tip`` horizontally:

.. code-block:: bash

    hatch hist -y tip -- tips.csv

.. image:: ../images/tips.tip.hist.y.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set


.. _hist_bins:

Controlling the number of bins used
===================================

By default hatch will try to automatically pick an appropriate number of bins for the
selected feature.

However, this can be overridden by specifying the required number of bins to use with the ``--bins`` 
argument like so:

.. code-block:: bash

    hatch hist -x tip --bins 5 -- tips.csv

.. image:: ../images/tips.tip.hist.bins5.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set, using 10 bins

.. _hist_binwidth:

Controlling the width of bins 
=============================

By default hatch will try to automatically pick an appropriate bin width for the
selected feature.

However, this can be overridden by specifying the required bin width to use with the ``--binwidth`` 
argument like so:

.. code-block:: bash

    hatch hist -x tip --binwidth 3 -- tips.csv

.. image:: ../images/tips.tip.hist.binwidth3.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set, using bins of width 3

Note that ``--binwidth`` overrides the ``--bins`` parameter.

.. _hist_cumulative:

Cumulative histograms 
=====================

.. code-block:: 

  --cumulative          Generate cumulative histogram

Cumulative histograms can be plotted with the ``--cumulative`` argument.  

.. code-block:: bash

    hatch hist -x tip --cumulative -- tips.csv

.. image:: ../images/tips.tip.hist.cumulative.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set in cumulative style

.. _hist_kde:

Kernel density estimate
=======================

.. code-block:: 

  --kde                 Plot a kernel density estimate for the distribution and show as a line 

A `kernel density estimate <https://en.wikipedia.org/wiki/Kernel_density_estimation>`_ can be plotted with the ``--kde`` argument.   

.. code-block:: bash

    hatch hist -x tip --kde -- tips.csv

.. image:: ../images/tips.tip.hist.kde.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set with a kernel density overlaid as a line 

.. _hist_log:

Log scale of X and Y axes 
=========================

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``.

.. code-block:: bash

    hatch hist -x tip --logy -- tips.csv 

.. _hist_range:

Range limits
============

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical distributions can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.


.. code-block:: bash

    hatch hist -x tip --xlim 3 8 -- tips.csv 

.. _hist_facets:

Facets
======

.. code-block:: 

 -r FEATURE, --row FEATURE  
 -c FEATURE, --col FEATURE
 --colwrap INT

Scatter plots can be further divided into facets, generating a matrix of histograms, where a numerical value is
further categorised by up to 2 more categorical features.

See the :doc:`facet documentation <facets/>` for more information on this feature.

.. code-block:: bash

    hatch hist -x tip --col day -- tips.csv 

.. image:: ../images/tips.tip.hist.col.day.png
       :width: 1200px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set with a column for each day 
