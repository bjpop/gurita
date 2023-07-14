.. _in:

in
==

Read input data from a named file or standard input.

Usage
-----

.. code-block:: bash

   gurita in [-h] [--sep STR] [--navalues STR [STR ...]] [--comment CHAR] [FILE] 

Arguments
---------

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - * ``-h``
       * ``--help``
     - display help for this command
     - :ref:`help <in_help>`
   * - ``--sep STR``
     - Specify the field separator 
     - :ref:`sep <in_sep>`
   * - ``--navalues STR [STR ...]``
     - Specify missing value markers
     - :ref:`navalues <in_navalues>`
   * - ``--comment CHAR``
     - If provided, CHAR marks the start of comment lines
     - :ref:`comment <in_comment>`
   * - ``[FILE]``
     - Optional list of file names 
     - :ref:`files <in_files>`

See also
--------
     
The :doc:`out <out/>` command writes data out to named files or the standard output.

Please also consult the :doc:`input and output <input_output>` documentation for a more detailed discussion on working with files and standard input/output. 

Simple example
--------------

Read contents of ``iris.csv`` as an input file: 

.. code-block:: text
   
    gurita in iris.csv

This is admittedly a contrived example because you would normally want to do something else with the data, apart from reading it in.

A more realistic example is to chain the output into another command, such as `head` to see the first few lines:

.. code-block:: text

    gurita in iris.csv + head

The output of the above command is as follows:

.. code-block:: text

   sepal_length,sepal_width,petal_length,petal_width,species
   5.1,3.5,1.4,0.2,setosa
   4.9,3.0,1.4,0.2,setosa
   4.7,3.2,1.3,0.2,setosa
   4.6,3.1,1.5,0.2,setosa
   5.0,3.6,1.4,0.2,setosa

Note that for simple cases of reading data from a single CSV file, the same effect can be achieved by the following command:

.. code-block:: text

    gurita head < iris.csv

This is because Gurita will default to :ref:`reading CSV data from standard input <input_implicit_csv_stdin>` if no explicit ``in`` command is given at the start of a command chain.

.. _in_help:

Getting help
------------

The full set of command line arguments for ``in`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita in -h

.. _in_sep:

Specify the field separator 
---------------------------

.. code-block::

   --sep STR

See also :ref:`specifying the field separator <input_field_separator>` in the input and output documentation.

By default Gurita assumes that the field separator for input data is a comma, and thus input data defaults to CSV format.

This can be overridden by the ``--sep`` argument.

For example, setting ``--sep`` to a tab character will allow TSV data to be read instead:

.. code-block:: text

    gurita in --sep '\t' example.tsv 

.. note:: 

   It is recommended to surround the separator string in single quotes to make sure it is treated as a literal string and not interpreted to have special meaning by the shell.

Separators longer than 1 character and different from '\s+' will be interpreted as regular expressions. This feature should be used with caution because it is prone to incorrectly handle quoted data.

.. _in_navalues:

Specify the missing value markers 
---------------------------------

.. code-block::

   --navalues STR [STR ...] 

See also the :ref:`missing values <missing_values>` documentation.

By default the following values are interpreted as missing values in input data: the empty string, ``#N/A``, ``#N/A N/A``, ``#NA``, ``-1.#IND`` ``-1.#QNAN``, ``-NaN``, ``-nan``, ``1.#IND``, ``1.#QNAN``, ``<NA>``, ``N/A``, ``NA``, ``NULL``, ``NaN``, ``n/a``, ``nan``, ``null``.

You can override the default symbols used for representing missing data in input files using the ``--navalues`` argument.

For example, suppose you want to use the symbols ``-`` (a single dash), ``NA`` and the empty string as symbols for missing values, then you can specify this as follows:

.. code-block:: text

   cat example.csv | gurita in --navalues '-' '' 'NA'

Note than when ``--navalues`` is used the default missing value symbols no longer apply, and only those symbols given as arguments to ``--navalues`` will be used to represent missing values.

.. _in_comment:

Allow comments in the input data
--------------------------------

.. code-block::

    --comment CHAR


