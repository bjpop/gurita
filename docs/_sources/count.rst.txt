.. _count:

Count 
*****

Count plots show the frequency of values within categorical features using bars.

.. code-block:: bash

    hatch count <arguments> 

Count plots are based on Seaborn's `catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_ library function, using the ``kind="count"`` option.

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help 
     - :ref:`help <count_help>`
   * - * ``-x FEATURE``
       * ``--xaxis FEATURE``
     - select feature for the X axis 
     - :ref:`X axis <count_feature_selection>`
   * - * ``-y FEATURE``
       * ``--yaxis FEATURE`` 
     - select feature for the Y axis 
     - :ref:`Y axis <count_feature_selection>`
   * - ``--order VALUE [VALUE ...]`` 
     - order of the plotted columns  
     - :ref:`order <count_order>`
   * - ``--hue FEATURE`` 
     - group features by hue 
     - :ref:`hue <count_hue>`
   * - ``--hueorder VALUE [VALUE ...]`` 
     - order of hue features
     - :ref:`hue order <count_hueorder>`
   * - ``--logx``
     - log scale X axis 
     - :ref:`log X axis <count_log>`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`log Y axis <count_log>`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`limit X axis <count_range>`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`limit Y axis <count_range>`
   * - * ``--row FEATURE``
       * ``-r FEATURE``
     - feature to use for facet rows
     - :ref:`facet rows <count_facets>`
   * - * ``--col FEATURE``
       * ``-c FEATURE``
     - feature to use for facet columns
     - :ref:`facet columns <count_facets>`
   * - ``--colwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`facet wrap <count_facets>`

.. _count_example:

Simple example
==============

Plot a count of the ``embark_town`` categorical feature from the ``titanic.csv`` input file:

.. code-block:: bash

    hatch count -x embark_town < titanic.csv

The output of the above command is written to ``count.embark_town.png``:

.. image:: ../images/count.embark_town.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file 

.. _count_help:

Getting help
============

The full set of command line arguments for count plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch count -h

.. _count_feature_selection:

Selecting features to plot
==========================

.. code-block:: 

  -x FEATURE, --xaxis FEATURE
  -y FEATURE, --yaxis FEATURE

Count plots can be plotted for categorical features.

.. note::

    If a numerical feature is selected for a count plot it will be treated as categorical, which may
    not give expected behaviour.

    You may not use both ``-x FEATURE`` and ``-y FEATURE`` in the same command line for count plots.

You can select the feature that you want to plot as a count using the ``-x`` (``--xaxis``) or ``-y`` (``--yaxis``)
arguments.

If ``-x`` (``--xaxis``) is chosen the count columns will be plotted vertically.

If ``-y`` (``--yaxis``) is chosen the count columns will be plotted horizontally.

See :ref:`the example <count_example>` above for a vertical axis plot.
For comparison, the following command uses ``-y embark_town`` to plot a histogram of ``embark_town`` horizontally:

.. code-block:: bash

    hatch count -y embark_town < titanic.csv

.. image:: ../images/count.embark_town.y.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file, plotted horizontally



.. _count_order:

Controlling the order of the plotted columns
============================================

.. code-block:: 

    --order VALUE [VALUE ...]

By default the order of the categorical features displayed in the count plot is determined from their occurrence in the input data.
This can be overridden with the ``--order`` argument, which allows you to specify the exact ordering of columns based on their values. 

In the following example the counts of the ``embark_town`` feature are displayed in the order of ``Cherbourg``, ``Queenstown``, ``Southampton``:

.. code-block:: bash

    hatch count -x embark_town --order Cherbourg Queenstown Southampton < titanic.csv

.. image:: ../images/count.embark_town.order.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file, with specific order 

.. _count_hue:

Grouping features with hue 
==========================

.. code-block:: 

  --hue FEATURE

The feature being counted can be grouped based on another categorical feature using the ``--hue`` argument.

In the following example the counts of the ``embark_town`` feature are grouped by the ``class`` feature from the titanic data set:

.. code-block:: bash

    hatch count -x embark_town --hue class < titanic.csv  

.. image:: ../images/count.embark_town.class.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file, grouped by the class feature 

.. _count_hueorder:

By default the order of the columns within each hue group is determined from their occurrence in the input data. 
This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of columns within each hue group, based on their values. 

In the following example the ``class`` values are displayed in the order of ``First``, ``Second``, ``Third``: 

.. code-block:: bash

    hatch count -x embark_town --hue class --hueorder First Second Third < titanic.csv  

.. image:: ../images/count.embark_town.class.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file, grouped by the class feature, displayed in a specified order

It is possible to use both ``--order`` and ``--hueorder`` in the same command. For example, the following command controls the order of both 
the ``embark_town`` and ``class`` categorical features:

.. code-block:: bash

    hatch count -x embark_town --hue class --order Cherbourg Queenstown Southampton \
                --hueorder First Second Third < titanic.csv

.. image:: ../images/count.embark_town.class.order.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot of embark_town showing grouping on town and on class, where the order of values is specified 

.. _count_log:

Log scale of counts
===================

.. code-block:: 

  --logx
  --logy

Count values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

It only makes sense to log-scale the count axis (and not the categorical axis). Therefore, ``--logx`` should be used when categorical features are selected with ``-y``, and
conversely, ``--logy`` should be used when categorical features are selected with ``-x``.

For example, you can display a log scale of counts for the ``embark_town`` feature (when the feature is displayed on the X-axis) like so. Note carefully that the categorical
data is displayed on the X-axis (``-x``), therefore the ``--logy`` argument should be used to log-scale the counts:

.. code-block:: bash

    hatch count -x embark_town --logy < titanic.csv  

.. image:: ../images/count.embark_town.logy.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot of embark_town showing grouping on town and on class, where the order of values is specified


.. _count_range:

Range limits
============

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed count values can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of values to be displayed.

It only makes sense to range-limit the count axis (and not the categorical axis). Therefore, ``--xlim`` should be used when categorical features are selected with ``-y``, and
conversely, ``--ylim`` should be used when categorical features are selected with ``-x``.

For example, you can display range-limited count for the ``embark_town`` feature (when the feature is displayed on the X-axis) like so. Note carefully that the categorical
data is displayed on the X-axis (``-x``), therefore the ``--ylim`` argument should be used to range-limit the counts: 

.. code-block:: bash

    hatch count -x embark_town --ylim 100 300 < titanic.csv

.. _count_facets:

Facets
======

.. code-block:: 

 -r FEATURE, --row FEATURE
 -c FEATURE, --col FEATURE
 --colwrap INT


Count plots can be further divided into facets, generating a matrix of count plots. 

See the :doc:`facet documentation <facets/>` for more information on this feature.

The follow command creates a faceted bar plot where the ``sex`` feature is used to determine the facet columns:

.. code-block:: bash

    hatch count -x embark_town --col sex < titanic.csv 

.. image:: ../images/count.embark_town.sex.png 
       :width: 600px
       :height: 300px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file, using sex to determine facet columns
