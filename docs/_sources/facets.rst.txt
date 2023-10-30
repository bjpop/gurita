Facets
======

Many of Gurita's plots support facets.

Facets consist of multiple sub-plots aligned in columns and/or 
rows with the same set of axes, each showing a subset of the data.

The subsets of data shown in the sub-plots are split according to the values of
categorical columns.

For example, the following box plot uses facets to split into two sub-plots based on the value of
the ``sex`` column using the ``--fcol`` argument:

.. code-block:: bash

    gurita box -y age -x class --fcol sex < titanic.csv

.. image:: ../images/box.class.age.sex.facet.png
       :width: 600px
       :height: 300px
       :align: center
       :alt: Box plot showing the mean of age for each class in the titanic data set grouped by class, using sex to determine the plot facets

|

In the above example the ``--fcol sex`` argument causes a colum-wise facet plot to be generated. Subsets of the data are defined based on the values in the ``sex`` column, which can be either ``male`` or ``female``. 


It is also possible to generate the facets row-wise, using ``--frow sex`` instead:

.. code-block:: bash

    gurita box -y age -x class --frow sex < titanic.csv

.. image:: ../images/box.class.age.sex.facet.row.png
       :width: 300px
       :height: 600px
       :align: center
       :alt: Box plot showing the mean of age for each class in the titanic data set grouped by class , using sex to determine the plot facets, displayed row-wise

|
