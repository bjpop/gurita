.. _out:

out
===

Write output data to a named file or standard output.

Usage
-----

.. code-block:: text 

   gurita out [--sep STR] [--na STR] [-h] [FILE]

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
     - :ref:`help <out_help>`
   * - ``--sep STR``
     - Specify the field separator 
     - :ref:`sep <out_sep>`
   * - ``[--na STR]`` 
     - Specify missing value marker
     - :ref:`na marker <out_na>`
   * - ``[FILE]``
     - Optional output file name 
     - :ref:`file name <out_file>`

See also
--------
     
The :doc:`in <in/>` command reads data in from named files or the standard input.

Please also consult the :doc:`input and output <input_output>` documentation for a more detailed discussion on working with files and standard input/output. 

Simple example
--------------

Read the contents of ``iris.csv`` as an input CSV file and write the output to ``iris.tsv`` in TSV format

.. code-block:: text
   
    gurita out --sep '\t' iris.tsv < iris.csv

.. _out_help:

Getting help
------------

The full set of command line arguments for ``out`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita out -h

.. _out_sep:

Specify the field separator 
---------------------------

.. code-block::

   --sep STR

See also :ref:`specifying the field separator <input_field_separator>` in the input and output documentation.

By default Gurita assumes that the field separator for input data is a comma, and thus input data defaults to CSV format.

This can be overridden by the ``--sep`` argument.

For example, setting ``--sep`` to a tab character will allow TSV data to be read instead:

.. code-block:: text

    gurita out --sep '\t' example.tsv < example.csv

.. note:: 

   It is recommended to surround the separator string in single quotes to make sure it is treated as a literal string and not interpreted to have special meaning by the shell.

Separators longer than 1 character and different from '\s+' will be interpreted as regular expressions. This feature should be used with caution because it is prone to incorrectly handle quoted data.

.. _out_na:

Specify the missing value markers 
---------------------------------

.. code-block::

   --na STR

See also the :ref:`missing values <missing_values>` documentation.

By default missing values will be written as empty fields in the output data. This can be overwritten with the ``--na STR`` where ``STR`` indicates the text to be used for missing values.

For example, suppose you want to use ``NA`` for missing values, then you can specify this as follows:

.. code-block:: text

   gurita out --na 'NA' < example.csv

.. note:: 

   It is recommended to surround the missing value string in single quotes to make sure it is treated as a literal string and not interpreted to have special meaning by the shell.

.. _out_file:

Optional output file
--------------------

As its last argument, the ``out`` command takes an optional output file name.

If no file name is specified then Gurita will write output to standard output. Otherwise it will try to write to the named file.

For example, the following command writes output to a named CSV file called ``example.csv``:

.. code-block:: text

   gurita ... + out example.csv

The following command writes outut to a TSV file called ``example.tsv``:

.. code-block:: text

   gurita ... + out --sep '\t' example.tsv

In the following command, no file name is supplied as an argument to ``out``. In this case Gurita will write output to the standard output.

.. code-block:: text

   gurita ... + out --sep '\t'

Writing output inside a command chain
-------------------------------------

Gurita allows you to use ``out`` multiple times within a :ref:`command chain<command_chain>`, for example:
   
.. code-block:: text

   gurita <command_1> + out example_1.csv + <command_2> + out example_2.csv 

When ``out`` is used within a command chain it receives data from the left hand side of the chain, writes the data to a file or standard output, and then passes the data along to the right hand side of the chain.

In the example above, ``<command_1>`` passes data to the first ``out`` command, which writes the
data to the file called ``example_1.csv``. The same data is then passed along unchanged to ``<command_2>``, the output of which is then passed to the second ``out`` command, which writes the data to
the file called ``example_2.csv``.

Gurita allows you to use ``out`` to write to standard output (stdout) more than once in the same command chain. In this circumstance each output will be appended together into the same standard output stream in order from left to right. This is on contrast to the ``in`` command which only allows to read from standard input stdin) once.
