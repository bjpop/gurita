.. _violin:

violin
======

Violin plots show the distribution of values in a numerical column optionally grouped by categorical columns.

Usage
-----

.. code-block:: text

    gurita violin [-h] [-x COLUMN] [-y COLUMN] ... other arguments ... 

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
     - display help
     - :ref:`help <violin_help>`
   * - * ``-x COLUMN``
       * ``--xaxis COLUMN``
     - select column for the X axis
     - :ref:`X axis <violin_column_selection>`
   * - * ``-y COLUMN``
       * ``--yaxis COLUMN``
     - select column for the Y axis
     - :ref:`Y axis <violin_column_selection>`
   * - ``--orient {v,h}``
     - Orientation of plot. Allowed values: v = vertical, h = horizontal. Default: v.
     - :ref:`orient <violin_orient>`
   * - ``--order VALUE [VALUE ...]``
     - controlling the order of the plotted violins 
     - :ref:`order <violin_order>`
   * - ``--hue COLUMN``
     - group columns by hue
     - :ref:`hue <violin_hue>`
   * - ``--hueorder VALUE [VALUE ...]``
     - order of hue columns
     - :ref:`hue order <violin_hueorder>`
   * - ``--logx``
     - log scale X axis 
     - :ref:`log X axis <violin_log>`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`log Y axis <violin_log>`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`limit X axis <violin_range>`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`limit Y axis <violin_range>`
   * - ``--frow COLUMN``
     - column to use for facet rows 
     - :ref:`facet rows <violin_facets>`
   * - ``--fcol COLUMN``
     - column to use for facet columns 
     - :ref:`facet columns <violin_facets>`
   * - ``--fcolwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`facet wrap <violin_facets>`

See also
--------

Similar functionality to violin plots are provided by:

 * :doc:`Box plots <box/>`
 * :doc:`Swarm plots <swarm/>`
 * :doc:`Strip plots <strip/>` 
 * :doc:`Boxen plots <boxen/>` 

Violin plots are based on Seaborn's `catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_ library function, using the ``kind="violin"`` option.

Simple example
--------------

Violin plot of the ``age`` numerical column from the ``titanic.csv`` input file:

.. code-block:: text

    gurita violin -y age < titanic.csv 

The output of the above command is written to ``violin.age.png``:

.. image:: ../images/violin.age.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Violin plot showing the distribution of age for the titanic data set

|

The plotted numerical column can be divided into groups based on a categorical column.
In the following example the distribution of ``age`` is shown for each value in the ``class`` column:

.. code-block:: text

    gurita violin -y age -x class < titanic.csv 

The output of the above command is written to ``violin.class.age.png``:

.. image:: ../images/violin.class.age.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Violin plot showing the distribution of age for each class in the titanic data set

|

.. _violin_help:

Getting help
------------

The full set of command line arguments for violin plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita violin -h

.. _violin_column_selection:

Selecting columns to plot
--------------------------

.. code-block:: 

  -x COLUMN, --xaxis COLUMN
  -y COLUMN, --yaxis COLUMN

Violin plots can be plotted for numerical columns and optionally grouped by categorical columns.

If no categorical column is specified, a single column violin plot will be generated showing
the distribution of the numerical column.

.. note:: 

    .. _violin_orient:

    By default the orientation of the violin plot is vertical. In this scenario
    the numerical column is specified by ``-y``, and the (optional) categorical column is specified
    by ``-x``.
    
    However, the orientation of the violin plot can be made horizontal using the ``--orient h`` argument.
    In this case the sense of the X and Y axes are swapped from the default, and thus
    the numerical column is specified by ``-x``, and the (optional) categorical column is specified
    by ``-y``.

In the following example the distribution of ``age`` is shown for each value in the ``class`` column,
where the boxes are plotted horizontally:

.. code-block:: text

    gurita violin -x age -y class --orient h < titanic.csv

.. image:: ../images/violin.age.class.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Violin plot showing the distribution of age for each class in the titanic data set, shown horizontally

|

.. _violin_order:

Controlling the order of the violins 
------------------------------------

.. code-block:: 

    --order VALUE [VALUE ...]

By default the order of the categorical columns displayed in the violin plot is determined from their occurrence in the input data.
This can be overridden with the ``--order`` argument, which allows you to specify the exact ordering of columns based on their values. 

In the following example the violin columns of the ``class`` column are displayed in the order of ``First``, ``Second``, ``Third``:

.. code-block:: text

    gurita violin -y age -x class --order First Second Third < titanic.csv

.. image:: ../images/violin.class.age.order.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Violin plot showing the distribution of age for each class in the titanic data set, shown in a specified order

|

.. _violin_hue:

Grouping columns with hue 
--------------------------

.. code-block:: 

  --hue COLUMN

The data can be further grouped by an additional categorical column with the ``--hue`` argument.

In the following example the distribution of ``age`` is shown for each value in the ``class`` column, and further sub-divided by the ``sex`` column:

.. code-block:: text

    gurita violin -y age -x class --hue sex < titanic.csv

.. image:: ../images/violin.class.age.sex.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Violin plot showing the distribution of age for each class in the titanic data set, grouped by class and sex 

|

.. _violin_hueorder:

By default the order of the columns within each hue group is determined from their occurrence in the input data. 
This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of columns within each hue group, based on their values. 

In the following example the ``sex`` values are displayed in the order of ``female``, ``male``: 

.. code-block:: text

    gurita violin -y age -x class --hue sex --hueorder female male < titanic.csv

.. image:: ../images/violin.class.age.sex.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Violin plot showing the distribution of age for each class in the titanic data set, grouped by class and sex, with the order of sex specified

|

It is also possible to use both ``--order`` and ``--hueorder`` in the same command. For example, the following command controls
the order of both the ``class`` and ``sex`` categorical columns:

.. code-block:: text

    gurita violin -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv

.. image:: ../images/violin.class.age.sex.order.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Violin plot showing the distribution of age for each class in the titanic data set, grouped by class and sex, with the order of class and sex specified

|

.. _violin_log:

Log scale
---------

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

It only makes sense to log-scale the numerical axis (and not the categorical axis). Therefore, ``--logx`` should be used when numerical columns are selected with ``-x``, and
conversely, ``--logy`` should be used when numerical columns are selected with ``-y``.

For example, you can display a log scale violin plot for the ``age`` column grouped by ``class`` (when the distribution of ``age`` is displayed on the Y axis) like so. Note carefully that the numerical data is displayed on the Y-axis (``-y``), therefore the ``--logy`` argument should be used to log-scale the numerical distribution:

.. code-block:: text

    gurita violin -y age -x class --logy < titanic.csv 

.. _violin_range:

Axis range limits
-----------------

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical distributions can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.

It only makes sense to range-limit the numerical axis (and not the categorical axis). Therefore, ``--xlim`` should be used when numerical columns are selected with ``-x``, and
conversely, ``--ylim`` should be used when numerical columns are selected with ``-y``.

For example, you can display range-limited range for the ``age`` column grouped by ``class`` (when the distribution of ``age`` is displayed on the Y axis) like so.
Note carefully that the numerical 
data is displayed on the Y-axis (``-y``), therefore the ``--ylim`` argument should be used to range-limit the distribution: 

.. code-block:: text

    gurita violin -y age -x class --ylim 10 30 < titanic.csv

.. _violin_facets:

Facets
------

.. code-block:: 

 --frow COLUMN
 --fcol COLUMN
 --fcolwrap INT

Violin plots can be further divided into facets, generating a matrix of violin plots, where a numerical value is
further categorised by up to 2 more categorical columns.

See the :doc:`facet documentation <facets/>` for more information on this feature.

The following command creates a faceted violin plot where the ``sex`` column is used to determine the facet columns:

.. code-block:: bash

    gurita violin -y age -x class --fcol sex < titanic.csv

.. image:: ../images/violin.class.age.sex.facet.png 
       :width: 600px
       :height: 300px
       :align: center
       :alt: Violin plot showing the mean of age for each class in the titanic data set grouped by class, using sex to determine the plot facets

|
