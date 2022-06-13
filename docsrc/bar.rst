.. _bar:

bar
===

Bar plots summarise a numerical feature as boxes with optional error bars.

By default the numerical feature is summarised by its mean, but other summary functions can be chosen.

.. code-block:: bash

    hatch bar <arguments>

Bar plots are based on Seaborn's `catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_ library function, using the ``kind="bar"`` option.


.. list-table::
   :widths: 25 20 10 
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h`` 
     - display help for this command
     - :ref:`help <bar_help>`
   * - * ``-x COLUMN``
       * ``--xaxis COLUMN``
     - select feature for the X axis
     - :ref:`X axis <bar_feature_selection>`
   * - * ``-y COLUMN``
       * ``--yaxis COLUMN``
     - select feature for the Y axis
     - :ref:`Y axis <bar_feature_selection>`
   * - ``--orient {v,h}``
     - Orientation of plot.
       Allowed values: v = vertical, h = horizontal.
       Default: v.
     - :ref:`orient <bar_orient>`
   * - ``--estimator {mean, median, max, min, sum, std, var}``
     - Function to compute point estimate of numerical feature
     - :ref:`estimator <bar_estimator>`
   * - ``--std``
     - show standard deviation of numerical feature as error bar 
     - :ref:`standard deviation error bar <standard_deviation>`
   * - ``--ci [NUM]``
     - Show confidence interval as error bar to estimate uncertainty of point estimate 
     - :ref:`confidence interval error bar <confidence_interval>`
   * - ``--order VALUE [VALUE ...]``
     - controlling the order of the plotted bars
     - :ref:`order <bar_order>`
   * - ``--hue COLUMN``
     - group features by hue
     - :ref:`hue <bar_hue>`
   * - ``--hueorder VALUE [VALUE ...]``
     - order of hue features
     - :ref:`hue order <bar_hueorder>`
   * - ``--logx``
     - log scale X axis (only relevant with ``--orient h``)
     - :ref:`log X axis <bar_log>`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`log Y axis <bar_log>`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`limit X axis <bar_range>`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`limit Y axis <bar_range>`
   * - * ``--row COLUMN``
       * ``-r COLUMN``
     - feature to use for facet rows 
     - :ref:`facet rows <bar_facets>`
   * - * ``--col COLUMN``
       * ``-c COLUMN``
     - feature to use for facet columns 
     - :ref:`facet columns <bar_facets>`
   * - ``--colwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`facet wrap <bar_facets>`

Similar functionality to bar plots are provided by:

 * :doc:`Point plots <point/>`

Simple example
--------------

Bar plot the mean ``age`` of passengers for each value of ``class`` in the ``titanic.csv`` input file:

.. code-block:: bash

    hatch bar -y age -x class < titanic.csv 

The output of the above command is written to ``bar.class.age.png``:

.. image:: ../images/bar.class.age.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set

|

.. _bar_help:

Getting help
------------

The full set of command line arguments for bar plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch bar -h

.. _bar_feature_selection:

Selecting features to plot
--------------------------

.. code-block:: 

  -x COLUMN, --xaxis COLUMN
  -y COLUMN, --yaxis COLUMN

Bar plots can be plotted for numerical features and optionally grouped by categorical features.

If no categorical feature is specified, a single column bar plot will be generated showing
a summary (mean by default) of the numerical feature.

.. note:: 

    .. _bar_orient:

    By default the orientation of the bar plot is vertical. In this scenario
    the numerical feature is specified by ``-y``, and the (optional) categorical feature is specified
    by ``-x``.
    
    However, the orientation of the bar plot can be made horizontal using the ``--orient h`` argument.
    In this case the sense of the X and Y axes are swapped from the default, and thus
    the numerical feature is specified by ``-x``, and the (optional) categorical feature is specified
    by ``-y``.

In the following example the mean of ``age`` is shown for each value in the ``class`` feature,
where the boxes are plotted horizontally:

.. code-block:: bash

    hatch bar -x age -y class --orient h < titanic.csv

.. image:: ../images/bar.age.class.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set, shown horizontally

|

.. _bar_estimator:

Summary function
----------------

By default bar plots show the mean of the selected numerical feature. However alternative functions
can be chosen using the ``--estimator`` argument.

The allowed choices are: ``mean``, ``median``, ``max``, ``min``, ``sum``, ``std`` (standard deviation), ``var`` (variance).

For example, the maximum ``age`` is shown for each value of ``class``: 

.. code-block:: bash

    hatch bar -y age -x class --estimator max < titanic.csv 

.. image:: ../images/bar.class.age.max.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the maximum age for each class in the titanic data set

|

.. _standard_deviation:

Standard deviaiton
------------------

The standard deviation of the numerical feature can be shown as an error bar with the ``--std`` argument.

For example the mean and standard deviation of ``age`` is shown for each value in the ``class`` feature:

.. code-block:: bash

    hatch bar -y age -x class --std < titanic.csv 

.. image:: ../images/bar.class.age.std.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set

|

.. _confidence_interval:

Confidence interval
-------------------

The confidence interval of the summary estimate can be shown as an error bar with the ``--ci`` argument.

By default, if ``--ci`` is specified without a numerical argument, then the 95% confidence interval is shown, but this can be changed by supplying a specific numeric value.

For example the mean of age and its 98% confidence interval is shown for each value in the ``class`` feature:

.. code-block:: bash

    hatch bar -y age -x class --ci 98 < titanic.csv 

.. image:: ../images/bar.class.age.ci.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age and 98% confidence interval for each class in the titanic data set

|

.. _bar_order:

Controlling the order of the bars
---------------------------------

.. code-block:: 

    --order VALUE [VALUE...]

By default the order of the categorical features displayed in the bar plot is determined from their occurrence in the input data.
This can be overridden with the ``--order`` argument, which allows you to specify the exact ordering of columns based on their values. 

In the following example the bar columns of the ``class`` feature are displayed in the order of ``First``, ``Second``, ``Third``:

.. code-block:: bash

    hatch bar -y age -x class --order First Second Third < titanic.csv

.. image:: ../images/bar.class.age.order.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set, shown in a specified order

|

.. _bar_hue:

Grouping features with hue 
--------------------------

.. code-block:: 

  --hue COLUMN

The data can be further grouped by an additional categorical feature with the ``--hue`` argument.

In the following example the mean and error of ``age`` is shown for each value in the ``class`` feature, and further sub-divided by the ``sex`` feature:

.. code-block:: bash

    hatch bar -y age -x class --hue sex < titanic.csv

.. image:: ../images/bar.class.age.sex.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set, grouped by class and sex 

|

.. _bar_hueorder:

By default the order of the columns within each hue group is determined from their occurrence in the input data. 
This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of columns within each hue group, based on their values. 

In the following example the ``sex`` values are displayed in the order of ``female``, ``male``: 

.. code-block:: bash

    hatch bar -y age -x class --hue sex --hueorder female male < titanic.csv

.. image:: ../images/bar.class.age.sex.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set, grouped by class and sex, with sex order specified

|

It is also possible to use both ``--order`` and ``--hueorder`` in the same command. For example, the following command controls
the order of both the ``class`` and ``sex`` categorical features:

.. code-block:: bash

    hatch bar -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv

.. image:: ../images/bar.class.age.sex.order.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set, grouped by class and sex, with class order and sex order specified

|

.. _bar_log:

Log scale 
---------

.. code-block:: 

  --logx
  --logy

The mean of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

It only makes sense to log-scale the numerical axis (and not the categorical axis). Therefore, ``--logx`` should be used when numerical features are selected with ``-x``, and
conversely, ``--logy`` should be used when numerical features are selected with ``-y``.

For example, you can display a log scale bar plot for the ``age`` feature grouped by ``class`` (when the mean of ``age`` is displayed on the Y axis) like so. Note carefully that the numerical data is displayed on the Y-axis (``-y``), therefore the ``--logy`` argument should be used to log-scale the numerical mean:

.. code-block:: bash

    hatch bar -y age -x class --logy < titanic.csv 

.. image:: ../images/bar.class.age.logy.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set, with the Y axis plotted in log scale 

|

.. _bar_range:

Axis range limits
-----------------

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical features can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.

It only makes sense to range-limit the numerical axis (and not the categorical axis). Therefore, ``--xlim`` should be used when numerical features are selected with ``-x``, and
conversely, ``--ylim`` should be used when numerical features are selected with ``-y``.

For example, you can display range-limited range for the ``age`` feature grouped by ``class`` (when ``age`` is displayed on the Y axis) like so.
Note carefully that the numerical 
data is displayed on the Y-axis (``-y``), therefore the ``--ylim`` argument should be used to range-limit the mean: 

.. code-block:: bash

    hatch bar -y age -x class --ylim 10 30 < titanic.csv

.. _bar_facets:

Facets
------

.. code-block:: 

 --row COLUMN, -r COLUMN
 --col COLUMN, -c COLUMN
 --colwrap INT

Bar plots can be further divided into facets, generating a matrix of bar plots, where a numerical value is
further categorised by up to 2 more categorical features.

See the :doc:`facet documentation <facets/>` for more information on this feature.

The follow command creates a faceted bar plot where the ``sex`` feature is used to determine the facet columns:

.. code-block:: bash

    hatch bar -y age -x class --col sex < titanic.csv

.. image:: ../images/bar.class.age.sex.facet.png 
       :width: 600px
       :height: 300px
       :align: center
       :alt: Bar plot showing the mean of age for each class in the titanic data set grouped by class, using sex to determine the plot facets

|
