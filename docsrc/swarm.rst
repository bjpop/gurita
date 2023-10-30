.. _swarm:

swarm
=====

Swarm plots show the distribution of values in a numerical column optionally grouped by categorical columns.

Usage
-----

.. code-block:: text 

    gurita swarm [-h] [-x COLUMN] [-y COLUMN] ... other arguments ... 

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
     - :ref:`help <swarm_help>`
   * - * ``-x COLUMN``
       * ``--xaxis COLUMN``
     - select column for the X axis
     - :ref:`X axis <swarm_column_selection>`
   * - * ``-y COLUMN``
       * ``--yaxis COLUMN``
     - select column for the Y axis
     - :ref:`Y axis <swarm_column_selection>`
   * - ``--orient {v,h}``
     - Orientation of plot. Allowed values: v = vertical, h = horizontal. Default: v.
     - :ref:`orient <swarm_orient>`
   * - ``--order VALUE [VALUE ...]``
     - controlling the order of the plotted swarms 
     - :ref:`order <swarm_order>`
   * - ``--hue COLUMN``
     - group columns by hue
     - :ref:`hue <swarm_hue>`
   * - ``--dodge``
     - separate hue levels along the categorical axis
     - :ref:`dodge <swarm_dodge>`
   * - ``--hueorder VALUE [VALUE ...]``
     - order of hue columns
     - :ref:`hue order <swarm_hueorder>`
   * - ``--logx``
     - log scale X axis 
     - :ref:`log X <swarm_log>`
   * - ``--logy``
     - log scale Y axis 
     - :ref:`log Y <swarm_log>`
   * - ``--xlim BOUND BOUND``
     - range limit X axis 
     - :ref:`limit X axis <swarm_range>`
   * - ``--ylim BOUND BOUND``
     - range limit Y axis 
     - :ref:`limit Y axis <swarm_range>`
   * - ``--frow COLUMN``
     - column to use for facet rows 
     - :ref:`facet rows <swarm_facets>`
   * - ``--fcol COLUMN``
     - column to use for facet columns 
     - :ref:`facet columns <swarm_facets>`
   * - ``--fcolwrap INT``
     - wrap the facet column at this width, to span multiple rows
     - :ref:`facet wrap <swarm_facets>`

See also
--------

Similar functionality to swarm plots are provided by:

 * :doc:`Box plots <box/>`
 * :doc:`Violin plots <violin/>`
 * :doc:`Strip plots <strip/>` 
 * :doc:`Boxen plots <boxen/>` 

Swarm plots are based on Seaborn's `catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_ library function, using the ``kind="swarm"`` option.

.. warning::
   Swarm plots can be slow to render on input data sets with large numbers of rows. 
   In cases where the swarm plot is too slow to render, consider using an alternative
   distribution plot, such as :doc:`strip<strip/>`, :doc:`box<box/>`, :doc:`boxen<boxen/>`, or :doc:`violin<violin/>`.
   Alternatively you can reduce the number of rows using a :doc:`random sample<sample/>` of the data.

Simple example
--------------

Swarm plot of the ``age`` numerical column from the ``titanic.csv`` input file:

.. code-block:: bash

    gurita swarm -y age < titanic.csv 

The output of the above command is written to ``swarm.age.png``:

.. image:: ../images/swarm.age.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for the titanic data set

|

The plotted numerical column can be divided into groups based on a categorical column.
In the following example the distribution of ``age`` is shown for each value in the ``class`` column:

.. code-block:: bash

    gurita swarm -y age -x class < titanic.csv 

The output of the above command is written to ``swarm.class.age.png``:

.. image:: ../images/swarm.class.age.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set

|

.. _swarm_help:

Getting help
------------

The full set of command line arguments for swarm plots can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: bash

    gurita swarm -h

.. _swarm_column_selection:

Selecting columns to plot
--------------------------

.. code-block:: 

  -x COLUMN, --xaxis COLUMN
  -y COLUMN, --yaxis COLUMN

Swarm plots can be plotted for numerical columns and optionally grouped by categorical columns.

If no categorical column is specified, a single column swarm plot will be generated showing
the distribution of the numerical column.

.. note:: 

    .. _swarm_orient:

    By default the orientation of the swarm plot is vertical. In this scenario
    the numerical column is specified by ``-y``, and the (optional) categorical column is specified
    by ``-x``.
    
    However, the orientation of the swarm plot can be made horizontal using the ``--orient h`` argument.
    In this case the sense of the X and Y axes are swapped from the default, and thus
    the numerical column is specified by ``-x``, and the (optional) categorical column is specified
    by ``-y``.

In the following example the distribution of ``age`` is shown for each value in the ``class`` column,
where the boxes are plotted horizontally:

.. code-block:: bash

    gurita swarm -x age -y class --orient h < titanic.csv

.. image:: ../images/swarm.age.class.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, shown horizontally

|

.. _swarm_order:

Controlling the order of the swarms
-----------------------------------

.. code-block:: 

    --order VALUE [VALUE ...]

By default the order of the categorical columns displayed in the swarm plot is determined from their occurrence in the input data.
This can be overridden with the ``--order`` argument, which allows you to specify the exact ordering of columns based on their values. 

In the following example the swarm columns of the ``class`` column are displayed in the order of ``First``, ``Second``, ``Third``:

.. code-block:: bash

    gurita swarm -y age -x class --order First Second Third < titanic.csv

.. image:: ../images/swarm.class.age.order.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, shown in a specified order

|

.. _swarm_hue:

Grouping columns with hue 
--------------------------

.. code-block:: 

  --hue COLUMN

The data can be further grouped by an additional categorical column with the ``--hue`` argument.

In the following example the distribution of ``age`` is shown for each value in the ``class`` column, and further sub-divided by the ``sex`` column:

.. code-block:: bash

    gurita swarm -y age -x class --hue sex < titanic.csv

.. image:: ../images/swarm.class.age.sex.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, grouped by class and sex 

|

.. _swarm_dodge:

As the previous example demonstrates, when ``--hue`` is used, by default all hue levels are shown mixed together in the same swarm.
However, you might want to show each hue level in its own swarm. This can be achieved with the ``--dodge`` command.

The ``--dodge`` argument will separate hue levels along the categorical axis, rather than mix them together:

.. code-block:: bash

    gurita swarm -y age -x class --hue sex --dodge < titanic.csv

.. image:: ../images/swarm.class.age.sex.dodge.png 
       :width: 700px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, grouped by class and sex, with the sex data separated into swarms 

|

.. _swarm_hueorder:

By default the order of the columns within each hue group is determined from their occurrence in the input data. 
This can be overridden with the ``--hueorder`` argument, which allows you to specify the exact ordering of columns within each hue group, based on their values. 

In the following example the ``sex`` values are displayed in the order of ``female``, ``male``: 

.. code-block:: bash

    gurita swarm -y age -x class --hue sex --hueorder female male < titanic.csv

.. image:: ../images/swarm.class.age.sex.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, grouped by class and sex, and the order of sex values specified 

|

It is also possible to use both ``--order`` and ``--hueorder`` in the same command. For example, the following command controls
the order of both the ``class`` and ``sex`` categorical columns:

.. code-block:: bash

    gurita swarm -y age -x class --order First Second Third --hue sex --hueorder female male < titanic.csv

.. image:: ../images/swarm.class.age.sex.order.hueorder.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, grouped by class and sex, and the order of class and sex values specified 

|

.. _swarm_log:

Log scale
---------

.. code-block:: 

  --logx
  --logy

The distribution of numerical values can be displayed in log (base 10) scale with ``--logx`` and ``--logy``. 

It only makes sense to log-scale the numerical axis (and not the categorical axis). Therefore, ``--logx`` should be used when numerical columns are selected with ``-x``, and
conversely, ``--logy`` should be used when numerical columns are selected with ``-y``.

For example, you can display a log scale swarm plot for the ``age`` column grouped by ``class`` (when the distribution of ``age`` is displayed on the Y axis) like so. Note carefully that the numerical data is displayed on the Y-axis (``-y``), therefore the ``--logy`` argument should be used to log-scale the numerical distribution:

.. code-block:: bash

    gurita swarm -y age -x class --logy < titanic.csv 

.. image:: ../images/swarm.class.age.logy.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, with the Y axis in log scale 

|

.. _swarm_range:

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

.. code-block:: bash

    gurita swarm -y age -x class --ylim 10 30 < titanic.csv

.. image:: ../images/swarm.class.age.ylim.png 
       :width: 600px
       :height: 600px
       :align: center
       :alt: Swarm plot showing the distribution of age for each class in the titanic data set, with the Y axis limited to values in the range 10 to 30 inclusive 

|

.. _swarm_facets:

Facets
------

.. code-block:: 

 --frow COLUMN
 --fcol COLUMN
 --fcolwrap INT

Swarm plots can be further divided into facets, generating a matrix of swarm plots, where a numerical value is
further categorised by up to 2 more categorical columns.

See the :doc:`facet documentation <facets/>` for more information on this feature.

The follow command creates a faceted swarm plot where the ``sex`` column is used to determine the facet columns:

.. code-block:: bash

    gurita swarm -y age -x class --fcol sex < titanic.csv

.. image:: ../images/swarm.class.age.sex.facets.png 
       :width: 600px
       :height: 300px
       :align: center
       :alt: Swarm plot showing the mean of age for each class in the titanic data set grouped by class, using sex to determine the plot facets

|

