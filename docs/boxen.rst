Boxen
*****

Boxen plots show the distribution of values in a numerical feature optionally grouped by categorical features.

.. code-block:: bash

    hatch boxen <arguments>

Boxen plots are based on Seaborn's `catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html/>`_ library function, using the ``kind="boxen"`` option.

.. list-table::
   :widths: 1 2 1
   :header-rows: 1

   * - Argument
     - Description
     - Reference
   * - ``-h``
     - display help
     - :ref:`boxen_help`
   * - ``-x FEATURE [FEATURE ...], --xaxis FEATURE [FEATURE ...]``
     - select feature for the X axis
     - :ref:`boxen_feature_selection`
   * - ``-y FEATURE [FEATURE ...], --yaxis FEATURE [FEATURE ...]``
     - select feature for the Y axis
     - :ref:`boxen_feature_selection`
   * - ``--orient {v,h}``
     - Orientation of plot. Allowed values: v = vertical, h = horizontal. Default: v.
     - :ref:`Box orientation <boxen_orient>`
   * - ``--hue FEATURE [FEATURE ...]``
     - group features by hue
     - :ref:`boxen_hue`
   * - ``--hueorder FEATURE [FEATURE ...]``
     - order of hue features
     - :ref:`Hue order <boxen_hueorder>`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`boxen_log`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`boxen_range`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`boxen_range`
   * - ``--row FEATURE [FEATURE ...], -r FEATURE [FEATURE ...]``
     - feature to use for facet rows 
     - :ref:`boxen_facets`
   * - ``--col FEATURE [FEATURE ...], -c FEATURE [FEATURE ...]``
     - feature to use for facet columns 
     - :ref:`boxen_facets`
   * - ``--colwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`boxen_facets`

Similar functionality to boxen plots are provided by:

 * :doc:`Box plots <box/>`
 * :doc:`Violin plots <violin/>`
 * :doc:`Swarm plots <swarm/>` 
 * :doc:`Strip plots <strip/>` 

Simple example
==============

Boxen plot of the ``age`` numerical feature from the ``titanic.csv`` input file:

.. code-block:: bash

    hatch boxen -y age -- titanic.csv 

The output of the above command is written to ``titanic.age.boxen.png``:

.. image:: ../images/titanic.age.boxen.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Boxen plot showing the distribution of age for the titanic data set

The plotted numerical feature can be divided into groups based on a categorical feature.
In the following example the distribution of ``age`` is shown for each value in the ``class`` feature:

.. code-block:: bash

    hatch boxen -y age -x class -- titanic.csv 

The output of the above command is written to ``titanic.age.class.boxen.png``:

.. image:: ../images/titanic.age.class.boxen.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Boxen plot showing the distribution of age for each class in the titanic data set

.. _boxen_help:

Getting help
============

The full set of command line arguments for boxen plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    hatch boxen -h

.. _boxen_feature_selection:

Selecting features to plot
==========================

.. code-block:: 

  -x FEATURE [FEATURE ...], --xaxis FEATURE [FEATURE ...]
  -y FEATURE [FEATURE ...], --yaxis FEATURE [FEATURE ...]

Boxen plots can be plotted for numerical features and optionally grouped by categorical features.

If no categorical feature is specified, a single column boxen plot will be generated showing
the distribution of the numerical feature.

.. note:: 

    .. _boxen_orient:

    By default the orientation of the boxen plot is vertical. In this scenario
    the numerical feature is specified by ``-y``, and the (optional) categorical feature is specified
    by ``-x``.
    
    However, the orientation of the boxen plot can be made horizontal using the ``--orient h`` argument.
    In this case the sense of the X and Y axes are swapped from the default, and thus
    the numerical feature is specified by ``-x``, and the (optional) categorical feature is specified
    by ``-y``.

In the following example the distribution of ``age`` is shown for each value in the ``class`` feature,
where the boxes are plotted horizontally:

.. code-block:: bash

    hatch boxen -x age -y class --orient h -- titanic.csv

.. image:: ../images/titanic.class.age.boxen.horizontal.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Boxen plot showing the distribution of age for each class in the titanic data set, shown horizontally

You may specifiy multiple numerical features and multiple categorical features in the same command.
Hatch will generate a separate plot for each combination of numerical and categorical feature
specified. For example, the following command specifies two numerical values and three categorical
values from the ``tips.csv`` data set to generate a total of six plots (2 times 3):

.. code-block:: bash

    hatch boxen -x sex smoker day -y tip total_bill -- tips.csv

The following output files are created by the above command.

.. code-block:: bash

    tips.tip.sex.boxen.png
    tips.total_bill.sex.boxen.png
    tips.tip.smoker.boxen.png
    tips.total_bill.smoker.boxen.png
    tips.tip.day.boxen.png
    tips.total_bill.day.boxen.png

.. _boxen_order:

Controlling the order of the plotted boxen columns
==================================================

.. code-block:: 

    --order FEATURE [FEATURE ...]

By default the order of the categorical features displayed in the boxen plot is determined from their occurrence in the input data.
This can be overridden with the ``--order`` argument, which allows you to specify the exact ordering of columns based on their values. 

In the following example the boxen columns of the ``class`` feature are displayed in the order of ``First``, ``Second``, ``Third``:

.. code-block:: bash

    hatch boxen -y age -x class --order First Second Third -- titanic.csv

.. image:: ../images/titanic.age.class.boxen.order.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Boxen plot showing the distribution of age for each class in the titanic data set, shown in a specified order

.. _boxen_hue:

Grouping features with hue 
==========================

.. code-block:: 

  --hue FEATURE [FEATURE ...]

The data can be further grouped by an additional categorical feature with the ``--hue`` argument.

In the following example the distribution of ``age`` is shown for each value in the ``class`` feature, and further sub-divided by the ``sex`` feature:

.. code-block:: bash

    hatch boxen -y age -x class --hue sex -- titanic.csv

.. image:: ../images/titanic.age.class.sex.boxen.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Boxen plot showing the distribution of age for each class in the titanic data set, grouped by class and sex 

You can specify more than one feature to group by; hatch will generate a separate boxen plot for every ``hue`` feature specified.

.. _boxen_hueorder:

By default the order of the columns within each hue group is determined from their occurrence in the input data. 
This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of columns within each hue group, based on their values. 

In the following example the ``sex`` values are displayed in the order of ``female``, ``male``: 

.. code-block:: bash

    hatch boxen -y age -x class --hue sex --hueorder female male -- titanic.csv

.. image:: ../images/titanic.age.class.sex.boxen.hueorder.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file, grouped by the class feature, displayed in a specified order

It is also possible to use both ``--order`` and ``--hueorder`` in the same command. For example, the following command controls
the order of both the ``class`` and ``sex`` categorical features:

.. code-block:: bash

    hatch boxen -y age -x class --order First Second Third --hue sex --hueorder female male -- titanic.csv

.. image:: ../images/titanic.age.class.sex.boxen.order.hueorder.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Count plot showing the frequency of the categorical values in the embark_town feature from the titanic.csv file, grouped by the class feature, displayed in a specified order

.. _boxen_log:

Log scale of numerical distribution 
===================================

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

It only makes sense to log-scale the numerical axis (and not the categorical axis). Therefore, ``--logx`` should be used when numerical features are selected with ``-x``, and
conversely, ``--logy`` should be used when numerical features are selected with ``-y``.

For example, you can display a log scale boxen plot for the ``age`` feature grouped by ``class`` (when the distribution of ``age`` is displayed on the Y axis) like so. Note carefully that the numerical data is displayed on the Y-axis (``-y``), therefore the ``--logy`` argument should be used to log-scale the numerical distribution:

.. code-block:: bash

    hatch boxen -y age -x class --logy -- titanic.csv 

.. _boxen_range:

Range limits
============

.. code-block:: 

  --xlim LOW HIGH 
  --ylim LOW HIGH

The range of displayed numerical distributions can be restricted with ``--xlim`` and ``--ylim``. Each of these flags takes two numerical values as arguments that represent the lower and upper bounds of the range to be displayed.

It only makes sense to range-limit the numerical axis (and not the categorical axis). Therefore, ``--xlim`` should be used when numerical features are selected with ``-x``, and
conversely, ``--ylim`` should be used when numerical features are selected with ``-y``.

For example, you can display range-limited range for the ``age`` feature grouped by ``class`` (when the distribution of ``age`` is displayed on the Y axis) like so.
Note carefully that the numerical 
data is displayed on the Y-axis (``-y``), therefore the ``--ylim`` argument should be used to range-limit the distribution: 

.. code-block:: bash

    hatch boxen -y age -x class --ylim 10 30 -- titanic.csv

.. _boxen_facets:

Facets
======

.. code-block:: 

 --row FEATURE [FEATURE ...], -r FEATURE [FEATURE ...]
 --col FEATURE [FEATURE ...], -c FEATURE [FEATURE ...]
 --colwrap INT

Boxen plots can be further divided into facets, generating a matrix of boxen plots, where a numerical value is
further categorised by up to 2 more categorical features.

See the :doc:`facet documentation <facets/>` for more information on this feature.
