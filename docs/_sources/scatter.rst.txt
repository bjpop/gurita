Scatter
*******

Scatter plots show the relationship between two features as a scatter of data points.

.. code-block:: bash

    hatch scatter <arguments>

When one of the two features being compared is a categorical value the scatter plot is similar to
:doc:`strip plot <strip/>`.

Scatter plots are based on Seaborn's `relplot <https://seaborn.pydata.org/generated/seaborn.relplot.html>`_ library function, using the ``kind="scatter"`` option.

.. list-table::
   :widths: 1 2 1
   :header-rows: 1

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help
     - :ref:`scatter_help`
   * - ``-x FEATURE, --xaxis FEATURE``
     - select feature for the X axis
     - :ref:`scatter_feature_selection`
   * - ``-y FEATURE, --yaxis FEATURE``
     - select feature for the Y axis
     - :ref:`scatter_feature_selection`
   * - ``--hue FEATURE``
     - group features by hue
     - :ref:`scatter_hue`
   * - ``--hueorder FEATURE [FEATURE ...]``
     - order of hue features
     - :ref:`Hue order <scatter_hueorder>`
   * - ``--dotstyle FEATURE``
     - name of categorical feature to use for plotted dot marker style
     - :ref:`Dot style <scatter_dotstyle>`
   * - ``--dotsize FEATURE``
     - scale the size of plotted dots based on a feature 
     - :ref:`scatter_dotsize`
   * - ``--dotalpha ALPHA``
     - alpha value for plotted points, default: 0.5  
     - :ref:`scatter_dotalpha_linewidth`
   * - ``--dotlinewidth WIDTH``
     - line width value for plotted points, default: 0
     - :ref:`scatter_dotalpha_linewidth`
   * - ``--logx``
     - log scale X axis 
     - :ref:`scatter_log`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`scatter_log`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`scatter_range`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`scatter_range`
   * - ``-r FEATURE, --row FEATURE``
     - feature to use for facet rows 
     - :ref:`scatter_facets`
   * - ``-c FEATURE, --col FEATURE``
     - feature to use for facet columns 
     - :ref:`scatter_facets`
   * - ``--colwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`scatter_facets`

.. _scatter_example:

Simple example
==============

Scatter plot of the ``tip`` numerical feature compared to the ``total_bill`` numerical feature from the ``tips.csv`` input file:

.. code-block:: bash

    hatch scatter -x total_bill -y tip -- tips.csv 

The output of the above command is written to ``tips.tip.total_bill.scatter.png``:

.. image:: ../images/tips.tip.total_bill.scatter.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing tip to total_bill in the tips.csv file 

.. _scatter_help:

Getting help
============

The full set of command line arguments for scatter plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch scatter -h

.. _scatter_feature_selection:

Selecting features to plot
==========================

.. code-block:: 

  -x FEATURE, --xaxis FEATURE
  -y FEATURE, --yaxis FEATURE

Scatter plots can be plotted for two numerical features as illustrated in the :ref:`example above <scatter_example>`, one on each of the axes.

Scatter plots can also be used to compare a numerical feature against a categorical feature. In the example below, the numerical ``tip`` feature is compared with the categorical ``day`` feature in the ``tips.csv`` dataset:

.. code-block::

    hatch scatter -x day -y tip -- tips.csv

.. image:: ../images/tips.tip.day.scatter.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing tip to day in the tips.csv file 

It should be noted that :doc:`strip plots <strip/>` achieve a similar result as above, and may be preferable over scatter plots when comparing numerical and categorical data. 

Swapping ``-x`` and ``-y`` in the above command would result in a horizontal plot instead of a vertical plot.

.. _scatter_hue:

Colouring data points with hue 
==============================

.. code-block:: 

  --hue FEATURE

The data points can be coloured by an additional numerical or categorical feature with the ``--hue`` argument.

In the following example the data points in a scatter plot comparing ``tip`` and ``total_bill`` are
coloured by their corresponding categorical ``day`` value: 

.. code-block:: bash

    hatch scatter -x total_bill -y tip --hue day -- tips.csv 

.. image:: ../images/tips.tip.total_bill.day.scatter.png
       :width: 700px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing tip and total_bill coloured by day 

When the ``--hue`` paramter specifies a numerical feature the colour scale is graduated.
For example, in the following scatter plot the numerical ``size`` feature is used for the ``--hue``
argument:

.. code-block:: bash

    hatch scatter -x total_bill -y tip --hue size -- tips.csv 

.. image:: ../images/tips.tip.total_bill.size.scatter.png
       :width: 700px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing tip and total_bill coloured by size 

.. _scatter_hueorder:

For categorical hue groups, the order displayed in the legend is determined from their occurrence in the input data. This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of 
the hue groups in the legend.

.. _scatter_dotstyle:

Dot style based on categorical feature
======================================

.. code-block:: 

    --dotstyle FEATURE 

By default dots in scatter plots are drawn as circles.

The ``--dotstyle`` argument lets you change the shape of dots based on a categorical feature.

.. code-block:: bash

    hatch scatter -x total_bill -y tip --hue day --dotstyle sex -- tips.csv

.. image:: ../images/tips.tip.total_bill.scatter.dotstyle.png
       :width: 700px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing tip and total_bill with dot size where the dot style is based on the sex categorical feature 

In the above example the hue of dots is determined by the ``day`` feature and the dot marker style is determined by the ``sex`` feature. In this case ``male`` dots use a cross marker and ``female`` dots use a circle marker.

It is acceptable for both the ``--hue`` and ``--dotstyle`` arguments to be based on the same (categorical) feature in the data set. In such cases both the colour and marker shape will vary with 
the underlying feature.

.. _scatter_dotsize:

Scaling dot size base on feature
================================

.. code-block:: 

    --dotsize FEATURE 

The size of plotted dots in the scatter plot can be scaled according the a numerical feature with the ``--dotsize`` argument.

In the following example, the dot size is scaled according to the value of the ``size`` feature
in ``tips.csv``:

.. code-block:: bash

    hatch scatter -x total_bill -y tip --dotsize size -- tips.csv

.. image:: ../images/tips.tip.total_bill.scatter.dotsize.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing tip and total_bill with dot size scaled by size 

.. _scatter_dotalpha_linewidth:

Dot alpha transparency and border linewidth
===========================================

.. code-block:: 

    --dotalpha ALPHA 
    --dotlinewidth WIDTH

By default the alpha transparency value of scatter plot dots is set to 0.5, and the dot border linewidth is set to 0. These can be overridden with the ``--dotalpha`` and ``--dotlinewidth`` arguments
respectively.

In the following example, the dot alpha is set to 1 and the boder line width is set to 1.

.. code-block:: bash

    hatch scatter -x total_bill -y tip --dotalpha 1 --dotlinewidth 1 -- tips.csv

.. image:: ../images/tips.tip.total_bill.scatter.dotalpha.dotlinewidth.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing tip and total_bill with dot alpha set to 1 and dot line width set to 1

.. _scatter_log:

Log scale of X and Y axes 
=========================

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

.. code-block:: bash

    hatch scatter -x total_bill -y tip --logy -- tips.csv 

.. _scatter_range:

Range limits
============

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical distributions can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.


.. code-block:: bash

    hatch scatter -x total_bill -y tip --xlim 20 40  -- tips.csv 

.. _scatter_facets:

Facets
======

.. code-block:: 

 -r FEATURE, --row FEATURE  
 -c FEATURE, --col FEATURE
 --colwrap INT

Scatter plots can be further divided into facets, generating a matrix of scatter plots, where a numerical value is
further categorised by up to 2 more categorical features.

See the :doc:`facet documentation <facets/>` for more information on this feature.
