.. _hist:

hist (histogram)
================

Plot distributions of selected numerical or categorical columns as histograms.

.. code-block:: text

    hatch hist <arguments> 

Histograms are based on Seaborn's `displot <https://seaborn.pydata.org/generated/seaborn.displot.html>`_ library function, using the ``kind="hist"`` option.

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help 
     - :ref:`help <hist_help>`
   * - * ``-x COLUMN``
       * ``--xaxis COLUMN``
     - select column for the X axis 
     - :ref:`X axis <hist_column_selection>`
   * - * ``-y COLUMN``
       * ``--yaxis COLUMN`` 
     - select column for the Y axis 
     - :ref:`Y axis <hist_column_selection>`
   * - ``--bins NUM``
     - number of bins 
     - :ref:`bins <hist_bins>`
   * - ``--binwidth NUM``
     - width of bins, overrides ``--bins`` 
     - :ref:`bin width <hist_binwidth>`
   * - ``--cumulative``
     - plot a cumulative histogram 
     - :ref:`cumulative <hist_cumulative>`
   * - ``--hue COLUMN``
     - group columns by hue
     - :ref:`hue <hist_hue>`
   * - ``--stat {count, frequency, probability, proportion, percent, density}``
     - Statistic to use for each bin (default: count) 
     - :ref:`stat <hist_stat>`
   * - ``--indnorm``
     - normalise each histogram in the plot independently
     - :ref:`independent normalisation <hist_indnorm>`
   * - ``--kde``
     - overlay a kernel density estimate (kde) as a line 
     - :ref:`kernel density estimation <hist_kde>`
   * - ``--nofill``
     - use unfilled histogram bars instead of solid coloured bars 
     - :ref:`no fill <hist_nofill>`
   * - ``--element {bars,step,poly}``
     - style of histogram bars (default is bars)
     - :ref:`element <hist_element>`
   * - ``--logx``
     - log scale X axis 
     - :ref:`log X axis <hist_log>`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`log Y axis <hist_log>`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`limit X axis <hist_range>`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`limit Y axis <hist_range>`
   * - * ``-r COLUMN``
       * ``--row COLUMN``
     - column to use for facet rows 
     - :ref:`facet rows <hist_facets>`
   * - * ``-c COLUMN``
       * ``--col COLUMN``
     - column to use for facet columns 
     - :ref:`facet columns <hist_facets>`
   * - ``--colwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`facet wrap <hist_facets>`


.. _hist_example:

Simple examples
---------------

Plot a histogram of the ``tip`` amount from the ``tips.csv`` input file:

.. code-block:: text

    hatch hist -x tip < tips.csv

The output of the above command is written to ``hist.tip.png``:

.. image:: ../images/hist.tip.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set

|

Plot a count of the different categorical values in the ``day`` column:

.. code-block:: text

    hatch hist -x day < tips.csv

The output of the above command is written to ``hist.day.png``:

.. image:: ../images/hist.day.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the count of the different categorical values in the day column 

|

.. _hist_help:

Getting help
------------

The full set of command line arguments for histograms can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    hatch hist -h

.. _hist_column_selection:

Selecting columns to plot
--------------------------

.. code-block:: 

  -x COLUMN, --xaxis COLUMN
                        Feature to plot along the X axis
  -y COLUMN, --yaxis COLUMN
                        Feature to plot along the Y axis

Histograms can be plotted for both numerical columns and for categorical columns. Numerical data is binned
and the histogram shows the counts of data points per bin. Catergorical data is shown as a count plot with a
column for each categorical value in the specified column.

You can select the column that you want to plot as a histogram using the ``-x`` (``--xaxis``) or ``-y`` (``--yaxis``)
arguments.

If ``-x`` (``--xaxis``) is chosen the histogram columns will be plotted vertically.

If ``-y`` (``--yaxis``) is chosen the histogram columns will be plotted horizontally.

If both ``-x`` and ``-y`` are both specified then a heatmap will be plotted.

See :ref:`the example <hist_example>` above for a vertical axis plot.
For comparison, the following command uses ``-y tip`` to plot a histogram of ``tip`` horizontally:

.. code-block:: text

    hatch hist -y tip < tips.csv

.. image:: ../images/hist.tip.y.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set

|

.. _hist_bivariate:

Histogram of two columns (bivariate heatmaps)
----------------------------------------------

Bivariate histograms (two columns) can be plotted by specifying both ``-x`` and ``-y``.

In the following example the distribution of ``tip`` is compared to the distribution of ``total_bill``. The result is shown as a heatmap:

.. code-block:: text

    hatch hist -x tip -y total_bill < tips.csv 

.. image:: ../images/hist.tip.total_bill.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bivariate histogram plot showing the distribution of tip against total_bill 

|

Bivariate histograms also work with categorical variables and combinations of numerical and categorical variables.

.. _hist_bins:

Number of bins 
--------------

For numerical columns, by default hatch will try to automatically pick an appropriate number of bins for the
selected column.

However, this can be overridden by specifying the required number of bins to use with the ``--bins`` 
argument like so:

.. code-block:: text

    hatch hist -x tip --bins 5 < tips.csv

.. image:: ../images/hist.tip.bins5.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set, using 5 bins 

|

.. _hist_binwidth:

Width of bins 
-------------

For numerical columns, by default hatch will try to automatically pick an appropriate bin width for the
selected column.

However, this can be overridden by specifying the required bin width to use with the ``--binwidth`` 
argument like so:

.. code-block:: text

    hatch hist -x tip --binwidth 3 < tips.csv

.. image:: ../images/hist.tip.binwidth3.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set, using bins of width 3

|

Note that ``--binwidth`` overrides the ``--bins`` parameter.

.. _hist_cumulative:

Cumulative histograms 
---------------------

Cumulative histograms can be plotted with the ``--cumulative`` argument.  

.. code-block:: text

    hatch hist -x tip --cumulative < tips.csv

.. image:: ../images/hist.tip.cumulative.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set in cumulative style

|

.. _hist_hue:

Show distributions of categorical subsets using hue
---------------------------------------------------

.. code-block:: 

  --hue COLUMN

The distribution of categorical subsets of the data can be shown with the ``--hue`` argument.

In the following example the distribution of distribution of the ``tip`` column
is divided into two subsets based on the categorical ``smoker`` column. Each
subset is plotted as its own histogram, layered on top of each other:

.. code-block:: text

    hatch hist -x tip --hue smoker < tips.csv  

.. image:: ../images/hist.tip.smoker.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram showing the distribution of tip based divided into subsets based on the smoker column 

|

The default behaviour is to layer overlapping histograms on top of each other, as demonstrated in the above plot.

.. _hist_multiple:

The ``--multiple`` parameter lets you choose alternative ways to show overlapping histograms. The example below shows the
two histograms stacked on top of each other:

.. code-block:: text

    hatch hist -x tip --hue smoker --multiple stack < tips.csv  

.. image:: ../images/hist.tip.smoker.stacked.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram showing the distribution of tip based divided into subsets based on the smoker column, with overlapping histograms stacked

|

The ``--multiple`` paramter supports the following values: ``layer`` (default), ``stack``, ``dodge``, and ``fill``.

The following example shows the effect of ``--multiple dodge``, where categorical fields are shown next to each other:

.. code-block:: text

    hatch hist -x tip --hue smoker --multiple dodge < tips.csv  

.. image:: ../images/hist.tip.smoker.dodge.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram showing the distribution of tip based divided into subsets based on the smoker column, with overlapping histograms side-by-side 

|

The following example shows the effect of ``--multiple fill``, where counts are normalised to a proportion, and bars are filled so that all categories sum to 1:

.. code-block:: text

    hatch hist -x tip --hue smoker --multiple fill < tips.csv  

.. image:: ../images/hist.tip.smoker.fill.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram showing the distribution of tip based divided into subsets based on the smoker column, with overlapping histograms filled to proportions 

|

.. _hist_stat:

Histogram statistic
-------------------

By default histograms show a count of the number of values in each bin. However this can be changed with the ``--stat {count,frequency,probability,proportion,percent,density}``
argument

.. code-block:: text

    hatch hist -x tip --stat proportion < tips.csv

.. image:: ../images/hist.tip.proportion.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set showing the proportion statistic for each bin 

|

.. _hist_indnorm:

Independent normalised statistics
---------------------------------

The ``--stat`` argument allows the use of the following normalising statistics:

* probability
* proportion (same as probability)
* percent
* density

In plots with mutliple histograms for categorical subsets using ``--hue``, by default these statistics are normalised across the entire dataset.
This behaviour can be changed by ``--indnorm`` such that the normalisation happens *within* each categorical subset.

Compare the following plots that show a histograms of the ``tip`` column for each value of ``smoker`` using a ``proportion`` as the statistic.

In the example below the default normalisation occurs, across the entire dataset:

.. code-block:: text

    hatch hist -x tip --hue smoker --stat proportion --multiple dodge < tips.csv 

.. image:: ../images/hist.tip.proportion.smoker.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set showing the proportion statistic for each bin and global normalisation

|

And now the same command as above, but with the ``--indnorm`` argument supplied, so that each value of ``smoker`` is normalised independently:

.. code-block:: text

    hatch hist -x tip --hue smoker --stat proportion --multiple dodge --indnorm < tips.csv 

.. image:: ../images/hist.tip.proportion.smoker.indnorm.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set showing the proportion statistic for each bin and indepdendent normalisation

|

.. _hist_kde:

Kernel density estimate
-----------------------

A `kernel density estimate <https://en.wikipedia.org/wiki/Kernel_density_estimation>`_ can be plotted with the ``--kde`` argument.   

.. code-block:: text

    hatch hist -x tip --kde < tips.csv

.. image:: ../images/hist.tip.kde.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set with a kernel density overlaid as a line 

|

.. _hist_nofill:

Unfilled histogram bars 
-----------------------

By default histogram bars are shown with solid filled bars. This can be changed with ``--nofill`` which uses unfilled bars instead:

.. code-block:: text

    hatch hist -x tip --nofill < tips.csv

.. image:: ../images/hist.tip.nofill.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set with unfilled bars

|

.. _hist_element:

Visual style of univariate histograms
-------------------------------------

By default univariate histograms are visualised as bars. This can be changed with ``--element {bars,step,poly}`` which allows alternative renderings. 

The example below shows the ``step`` visual style.

.. code-block:: text

    hatch hist -x tip --element step < tips.csv

.. image:: ../images/hist.tip.step.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set using a step visualisation style 

|

The example below shows the ``poly`` (polygon) visual style, with vertices in the center of each bin.

.. code-block:: text

    hatch hist -x tip --element poly < tips.csv

.. image:: ../images/hist.tip.poly.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set using a polygon visualisation style 

|

.. _hist_log:

Log scale
---------

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``.

.. code-block:: text

    hatch hist -x tip --logy < tips.csv 

.. image:: ../images/hist.tip.logy.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set with log scale on the Y axis 

|

.. _hist_range:

Axis range limits
-----------------

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical distributions can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.

.. code-block:: text

    hatch hist -x tip --xlim 3 8 < tips.csv 

.. _hist_facets:

Facets
------

.. code-block:: 

 -r COLUMN, --row COLUMN  
 -c COLUMN, --col COLUMN
 --colwrap INT

Scatter plots can be further divided into facets, generating a matrix of histograms, where a numerical value is
further categorised by up to 2 more categorical columns.

See the :doc:`facet documentation <facets/>` for more information on this feature.

.. code-block:: text

    hatch hist -x tip --col day < tips.csv 

.. image:: ../images/hist.tip.day.png 
       :width: 600px
       :height: 300px
       :align: center
       :alt: Histogram plot showing the distribution of tip amounts for the tips data set with a column for each day 

|
