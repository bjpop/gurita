.. _pair:

pair
====

Plot relationships between pairs of columns on a grid of axes.

By default comparisons are made between
all numerical columns in the data, however it is possible to specify which columns to compare, including
categorical columns as well.

A histogram showing the distribution of each column is shown on the diagonal.

Usage
-----

.. code-block:: text

    gurita pair [-h] [-c [COLUMN ...]] [--kind {scatter,kde,hist,reg}] ... other arguments ...

Arguments
---------

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help for this command
     - :ref:`help <pair_help>`
   * - * ``-c [COLUMN ...]``
       * ``--columns [COLUMN ...]``
     - select columns to compare 
     - :ref:`columns <pair_columns>`
   * - ``--hue COLUMN``
     - group data by a categorical column 
     - :ref:`hue <pair_hue>`
   * - ``--corner``
     - only plot the lower left corner of the grid 
     - :ref:`corner <pair_corner>`
   * - ``--kind {scatter,kde,hist,reg}`` 
     - choose the kind of plot (default: ``scatter``)
     - :ref:`kind <pair_kind>`

See also
--------

Pair plots are based on Seaborn's `pairplot <https://seaborn.pydata.org/generated/seaborn.pairplot.html>`_ library function.

Simple example
--------------

The following example generates a pair plot comparing all the numerical columns in the ``iris.csv`` data set.

Note that there are four numerical columns in this data set (``sepal_width``, ``sepal_length``, ``petal_length``, ``petal_width``) and one categorical column (``species``).
By default, if no column names are specified in a pair plot, all the numerical columns will be compared (and catergorical columns are ignored).
This behaviour can be overridden with the ``-c, --columns`` :ref:`argument <pair_columns>`.

.. code-block:: text 

    gurita pair < iris.csv

The output of the above command is written to ``pair.png``:

.. image:: ../images/pair.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing all the numerical columns in the iris.csv data set 

|

.. _pair_help:

Getting help
------------

The full set of command line arguments for pair plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita pair -h

.. _pair_columns:

Selecting columns to compare
----------------------------

.. code-block:: text

    -c [COLUMN ...], --columns [COLUMN ...]


By default, if no column names are specified in a pair plot, all the numerical columns will be compared (and catergorical columns are ignored).
This behaviour can be overridden with the ``-c`` (or ``--columns``) argument.

The following example generates a pair plot comparing the ``sepal_length``, ``petal_length``, and ``species`` columns. Note that ``species`` is
a categorical column, and it would not be plotted by default.

.. code-block:: text

    gurita pair -c sepal_length petal_length species < iris.csv 

.. image:: ../images/pair.columns.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing various specific columns in the iris.csv data set 

|

Unfortunately, due to the small size of the above plot, the axes labels for ``species`` on the X axis overlap one another. This can be avoided
by rotating the X axis tick labels by 90 degrees using ``--rxtl 90``:

.. code-block:: text

    gurita pair -c sepal_length petal_length species --rxtl 90 < iris.csv 

.. image:: ../images/pair.columns.rxtl.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing various specific columns in the iris.csv data set, with X axis labels rotated 90 degrees to avoid overlapping

|

.. _pair_hue:

Group data by a categorical column with hue 
-------------------------------------------

.. code-block:: text

    --hue COLUMN 

The plotted data can be grouped by a categorical column, where each group is rendered as a different colour. 

In the example below, no column names are specified, so only the numerical columns are plotted.

.. code-block:: text

    gurita pair --hue species < iris.csv 

.. image:: ../images/pair.species.png 
       :width: 600px
       :height: 500px
       :align: center
       :alt: Pair plot comparing all the numerical columns in the iris.csv data set, grouped by species 

|

.. _pair_corner:

Only plot the lower left corner of the grid
-------------------------------------------

.. code-block:: text

    --corner

By default a pair plot shows a full square grid of plots for each pairwise comparison. In this sense the top right and bottom left triangles 
of the plot are reflected mirror images. An alternative is to plot only the bottom left corner of the grid using the ``--corner`` argument. 

.. code-block:: text

    gurita pair --corner < iris.csv

.. image:: ../images/pair.corner.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing all the numerical columns in the iris.csv data set, showing only the lower left corner 

|

.. _pair_kind:

Choose the kind of plot
-----------------------

.. code-block:: text

    --kind {scatter,kde,hist,reg}

By default pair plots use a scatter plot to compare two numerical columns. This can be changed with the ``--kind`` argument, which allows you to choose
from four plot types:

1. ``scatter`` (the default)
2. ``kde`` kernel density estimate
3. ``hist`` histogram
4. ``reg`` regression

The example below shows a pair plot using ``kde`` (kernel density estimate) as the method of comparison: 

.. code-block:: text

    gurita pair --kind kde < iris.csv

.. image:: ../images/pair.kde.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing all the numerical columns in the iris.csv data set, using a kde to compare columns 

|

The example below shows a pair plot using ``hist`` (histogram) as the method of comparison:

.. code-block:: text

    gurita pair --kind hist < iris.csv

.. image:: ../images/pair.hist.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing all the numerical columns in the iris.csv data set, using a histogram to compare columns

|

The example below shows a pair plot using ``reg`` (regression) as the method of comparison:

.. code-block:: text

    gurita pair --kind reg < iris.csv

.. image:: ../images/pair.reg.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Pair plot comparing all the numerical columns in the iris.csv data set, using a regression to compare columns

|

