.. _aesthetics:

Plot aesthetics 
===============

Gurita tries to use sensible default values for parameters that control the appearance of output plots. However, these can be overridden by optional command line arguments.

Each plot command accepts a ``-h/--help`` argument that will cause Gurita to display more information about how to control the visual appearance of the output. 



Arguments
---------

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - ``--width``
     - width of the plot in cm 
     - :ref:`width <aesthetics_width>`
   * - ``--height``
     - height of the plot in cm 
     - :ref:`height <aesthetics_height>`
   * - ``--title``
     - plot title 
     - :ref:`title <aesthetics_title>`
   * - ``--xlabel``
     - X axis label 
     - :ref:`X axis label<aesthetics_xlabel>`
   * - ``--ylabel``
     - Y axis label 
     - :ref:`Y axis label<aesthetics_ylabel>`
   * - ``--plotstyle {darkgrid,whitegrid,dark,white,ticks}``
     - Change the aesthetic style of the plot 
     - :ref:`plot style<aesthetics_plotstyle>`
   * - ``--context {paper,notebook,talk,poster}``
     - Change the aesthetic context of the plot 
     - :ref:`plot context<aesthetics_context>`
   * - ``--nolegend``
     - Do not display a plot legend 
     - :ref:`no legend<aesthetics_nolegend>`
   * - * ``--nxtl``
       * ``--noxticklabels``
     - Turn off Y axis tick labels 
     - :ref:`no X axis tick labels<aesthetics_noxticklabels>`
   * - * ``--nytl``
       * ``--noyticklabels``
     - Turn off X axis tick labels 
     - :ref:`no Y axis tick labels<aesthetics_noyticklabels>`
   * - * ``--rxtl``
       * ``--rotxticklabels``
     - Rotate tick labels on the X axis by angle 
     - :ref:`rotate X tick labels <aesthetics_rotxticklabels>`
   * - * ``--rytl``
       * ``--rotyticklabels``
     - Rotate tick labels on the Y axis by angle 
     - :ref:`rotate Y tick labels <aesthetics_rotyticklabels>`

.. _aesthetics_width: 

Width
-----

Set the width of the plot in cm. By default plots are 20cm wide.

.. code-block:: text 

    --width SIZE

Example:

.. code-block:: text

    gurita box --width 40 ...

.. _height: 

.. _aesthetics_height: 

Height
------

Set the height of the plot in cm. By default plots are 20cm high.

.. code-block:: bash

    --height SIZE

Example:

.. code-block:: text

    gurita box --height 10 ...

.. _aesthetics_title: 

Title
-----

Set the title text of the plot. By default plots do not have a title text.

.. code-block:: text 

    --title TEXT 

Example:

.. code-block:: text

    gurita box --title "An example plot title" ... 

.. _aesthetics_xlabel: 

X axis label
------------

Set the label of the X axis. The default X axis label depends on the type of plot. In many cases
it is derived from the input data. 

.. code-block:: bash

    --xlabel STR 

Example:

.. code-block:: text

    gurita box --xlabel "An example X axis label" ... 

.. _aesthetics_ylabel: 

Y axis label
------------

Set the label of the Y axis. The default Y axis label depends on the type of plot. In many cases
it is derived from the input data. 

.. code-block:: bash

    --ylabel STR 

Example:

.. code-block:: text

    gurita box --ylabel "An example Y axis label" ... 
    
.. _aesthetics_plotstyle: 

Style
-----

Set the visual style of the plot. By default the ``darkgrid`` style is used.

.. code-block:: text 

    --plotstyle {darkgrid,whitegrid,dark,white,ticks}

Example:

.. code-block:: text

    gurita box --plotstyle whitegrid ... 

.. _aesthetics_context:

Context
-------

Set the visual context for the plot. By default the ``notebook`` context is used. 

Contexts are
a convenient way to adjust various visualisation parameters to suit different 
common scenarios where plots are displayed. For example, the ``poster`` context will use larger
text sizes for labels for easier reading at a distance.

.. code-block:: text 

    --context {paper,notebook,talk,poster} 

Example:

.. code-block:: text

    gurita box --context poster ... 

.. _aesthetics_nolegend: 

No legend
---------

Many plots display a legend either on top of the plot or next to the plot. This argument
turns the legend off so it won't be displayed.

.. code-block:: text 

    --nolegend

Example:

.. code-block:: text

    gurita box --nolegend ... 

.. _aesthetics_noxticklabels: 

Turn off X axis tick labels 
---------------------------

By default the X axis will show data labels next to axis tick marks 
(note that not all plots have tick marks). This arugment turns off tick labels so that they won't be displayed.

.. code-block:: text 

    --nxtl, --noxticklabels

Example:

.. code-block:: text

    gurita box --noxticklabels ... 

.. _aesthetics_noyticklabels: 

Turn off Y axis tick labels 
---------------------------

By default the Y axis will show data labels next to axis tick marks 
(note that not all plots have tick marks). This arugment turns off tick labels so that they won't be displayed.

.. code-block:: text 

    --nytl, --noyticklabels

Example:

.. code-block:: text

    gurita box --noyticklabels ... 

.. _aesthetics_rotxticklabels:

Rotate tick labels on the X axis
--------------------------------

Adjust the angle in degrees that tick labels are displayed on the X axis (note that not all plots have tick labales). This can be useful when the default tick labels overlap each other.

.. code-block:: text 

    --rxtl, --rotxticklabels

Example:

.. code-block:: text

    gurita box --rotxticklabels 90 ... 

.. _aesthetics_rotyticklabels:

Rotate tick labels on the Y axis
--------------------------------

Adjust the angle in degrees that tick labels are displayed on the X axis (note that not all plots have tick labales). This can be useful when the default tick labels overlap each other.

.. code-block:: text 

    --rytl, --rotyticklabels

Example:

.. code-block:: text

    gurita box --rotyticklabels 90 ... 
