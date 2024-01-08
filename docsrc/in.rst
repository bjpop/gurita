.. _in:

in
==

Read input data from a named file or standard input.

Usage
-----

.. code-block:: text 

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
     - Optional input file name 
     - :ref:`file name <in_file>`

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

.. literalinclude:: example_outputs/iris_head.txt

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

.. code-block:: text

    --comment CHAR

By default Gurita does not allow comments inside input files, however this behaviour can be changed with the ``--comment`` option. It takes a single character argument that specifies the start of a comment. Comments are assumed to begin with this character and run until the end of the line.

Comment text (including the starting character) is discarded by Gurita (and thus ignored).

This allows the input data file to contain notes that may be useful for other purposes, but are not treated as data values.

For example, consider a CSV file with the following contents:

.. code-block:: text

    # this is a comment line
    name,age
    # this is another comment line
    Fred,42
    Wilma,36

The first and third rows contain comments.

The following command tells Gurita to read ``example.csv`` and discard the comment lines that start with a hash character: 

.. code-block:: text

    gurita in --comment '#' example.csv

.. warning:: 

   If the input data contains comments but you don't specify ``in --comment ...`` then it will be incorrectly parsed.

.. _in_file:

Optional input file
-------------------

As its last argument, the ``in`` command takes an optional input file name.

If no file is listed then Gurita will read input from standard input. Otherwise it will try to read
from the named file.

For example, the following command reads input from a named CSV file called ``example.csv``:

.. code-block:: text

   gurita in example.csv

The following command reads input from a TSV file called ``example.tsv``:

.. code-block:: text

   gurita in --sep '\t' example.tsv

In the following command, no file name is supplied as an argument to ``in``. In this case Gurita will read input from the standard input, where the contents of ``example.tsv`` using input redirection: 

.. code-block:: text

   gurita in --sep '\t' < example.tsv

The same thing as the above command can also be achieved using a pipe:

.. code-block:: text

   cat example.tsv | gurita in --sep '\t'

More generally this allows Gurita to be used within a more complex shell pipeline:

.. code-block:: text

   <shell commands> | gurita in --sep '\t' ... | <shell commands>

.. _in_chain:

Reading input inside a command chain
------------------------------------

Gurita allows you to use ``in`` multiple times within a :ref:`command chain<command_chain>`, for example:

.. code-block:: text

   gurita in iris.csv + <commands_1> + in tips.csv + <commands_2>

If an invocation of ``in`` is not at the start of a chain then it discards any input coming from the left side of the chain and replaces it with the contents of the new file.

In the example above, the contents of ``iris.csv`` are passed into ``<commands_1>``, where it could be plotted or transformed. The next invocation of ``in`` reads the contents of ``tips.csv`` and passes this data on to ``<commands_2>``. Note carefully that any data coming out of ``<commands_1>`` is discarded.   

One important limitation is that it is only possible to read input from standard input at most once in a command chain. Furthermore, standard input can only be read at the start of command chain (in the leftmost position). 
