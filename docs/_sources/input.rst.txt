.. _input_files:

Reading input data 
==================

Hatch can read data from a named input file or standard input (stdin).

Input from a named file 
-----------------------

The ``in`` command allows you to specify an input file by name: 

.. code-block:: text 

    hatch in titanic.csv ... 

We use ``...`` to indicate that the remainder of the example Hatch command is omitted for the sake of simplifying the discussion.

You should imagine that ``...`` would be replaced by more text to complete the command.
For example, if you wanted to generate a count plot of the ``class`` feature in the ``titanic.csv`` file, the ``...`` in the above example could be expanded like so:

.. code-block:: text 

    hatch in titanic.csv + count -x class 

In the above example data is read from the input file and then passed along the :ref:`command chain <command_chain>` from left to right into the ``count`` command to make a plot.

When reading input from a named file (and not from standard input) Hatch will look at the file extension and assume CSV format if the extension is ``.csv`` and TSV format if the extension is ``.tsv``. This behaviour can be overridden with the
``--sep <str>`` option as noted below.

Specifying the field separator 
------------------------------

The ``in`` command lets you specify the field separator explicitly. This will override any default behaviour that Hatch would otherwise have when choosing what separator to use. 

Using a comma as the field separator:

.. code-block:: text 

    hatch in --sep ',' ...

Note: comma is the default separator used by Hatch, so you don't need to specify it explicitly. Therefore the above example is redundant, and only shown for the sake of illustration.

Using a tab character as the field separator:

.. code-block:: text 

    hatch in --sep '\t' ... 

Be sure to enclose the ``\t`` in quote characters to ensure that it is treated as a single string.

Elaborating the above example to a full command, assuming ``example_filename`` is the name of a file containing data in TSV format:

.. code-block:: text 

    hatch in --sep '\t' example_filename + count -x class 

Using a vertical bar character as the field separator:

.. code-block:: text 

    hatch in --sep '|' ... 

.. note::

    ``--sep <str>`` forces Hatch to use the specified field separator regardless of the filename extension or contents of the file. 

Input from standard input (stdin) 
---------------------------------

If you don't specify a file name when using the ``in`` command Hatch will assume that the input should be read from standard input (stdin):

.. code-block:: text

    hatch in ... 

For example:

.. code-block:: text

    hatch in + count -x class < titanic.csv

In the above example the notation ``< titanic.csv`` causes the contents of the file ``titantic.csv`` to be fed into the standard input of Hatch.
This is called *input redirection*. 

Instead of using input redirection, it is also possible to *pipe* the output from another command to the standard input of Hatch:

.. code-block:: text 

    cat titanic.csv | hatch in + count -x class

In the above example the command ``cat titanic.csv`` outputs the contents of the file ``titanic.csv`` to standard output which is then fed through a pipe using the ``|`` (vertical bar) operator
into the standard input of Hatch.

Reading from standard input is particularly useful when you want to use Hatch as part of a command pipeline: 

.. code-block:: text

    example_command | hatch in + count -x class

Here ``example_command`` is supposed to represent an arbitrary command, possibly itself a series of commands piped together, whose ouput is sent as input into Hatch.

For performance reasons Hatch does not try to detect the format of the input file when reading from standard input. 

Therefore, when reading from standard input, unless otherwise specified, Hatch assumes that the file is in CSV format.

As before, this can be overridden by ``in --sep <str>``, as illustrated in the example below: 

.. code-block:: text

    cat titanic.tsv | hatch in --sep '\t' + count -x class


.. note::

   **Standard input can only be read once in a Hatch command**

   A Hatch command can only read from standard input at most once in a command. An attempt to read from standard input more than once will result in an error: 

   .. code-block:: text

       hatch in + count -x class + in < titanic.csv
       hatch ERROR: stdin may only be used at most once, and only as the first command; exiting


.. note::

   **Standard input can only be read at the start of a command**

   Hatch will only permit standard input to be read at the start of a command chain. Therefore it is an error to request to read
   from standard input in any position other then the first command in the chain:

   .. code-block:: text

      hatch count -x class + in < titanic.csv
      hatch ERROR: stdin may only be used at most once, and only as the first command; exiting

   Note that this restriction is only a concern when using the ``in`` command to read from standard input, and does
   not apply when reading from standard input implicitly (as noted below).


Implicit CSV input from standard input (stdin)
----------------------------------------------

For convenience, if you don't use the ``in`` command explicitly Hatch will assume you wanted to read from standard input in CSV format.

Therefore:

.. code-block:: text

    hatch in + <rest of command>

can be simplified to:

.. code-block:: text

    hatch <rest of command>

In other words, if a Hatch command starts with ``in +`` you can simply omit that part, and Hatch will implicitly read from standard input using CSV format. This saves you a bit of typing and makes the command line tidier.

As a concrete example, the following command:

.. code-block:: text

    cat titanic.csv | hatch in + count -x class

can be simplified to:

.. code-block:: text

    cat titanic.csv | hatch count -x class

or, of course, you could achieve the same result with input redirection, again dropping the ``in +`` from the original command:

.. code-block:: text

    hatch count -x class < titanic.csv

Note carefully that when implicitly reading from standard input Hatch will always assume the input file is in CSV format. If you want to read a different format from standard input you must explicitly specify
the type using: ``in --sep <str>``


Ignoring comments in the input data
-----------------------------------

Hatch optionally supports comments in input data files where the comment starts with a special character, such as a hash, and continues until the end of the line.

This feature is enabled for the ``in`` command with the ``--comment <char>`` option, where ``<char>`` is a single character that marks the start of a comment.

For example, the following CSV data contains two comments, each starting with a hash character.

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species
    # This is a comment
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,virginica# This is also a comment
    4.7,3.2,1.3,0.2,setosa

Such an input file can be read like so:

.. code-block:: text

    cat iris.csv | hatch in --comment '#' ... 

Be sure to enclose the comment marker in quotes to ensure that is is not interpreted as having a special meaning to the shell.
For instance, the hash character ``#`` indicates a comment in most Unix command line shells. Enclosing it in quotes prevents it from being interpreted this way. 

Reading input from more than one file in a command chain
--------------------------------------------------------

You may read input from more than one file in a command chain, but only when each of those files is read from a named file (and not standard input). 

For example you can do something like this:

.. code-block:: text

    hatch in titanic.csv + ... + in iris.csv + ... 

In the above example, first ``titanic.csv`` is read as input, then some unspecified commands are run, and later ``iris.csv`` is read as input, and some more unspecified commands are run.

Whenever a new input is read from a named file the contents of that file become the current data set, and any previous data set in the command chain is discarded.

The following command is a more concrete example:

.. code-block:: text

   hatch in titanic.csv + hist -x fare + in iris.csv + count -x species

There are four parts to the above command chain:

1. input is read from the ``titanic.csv`` file, this becomes the current data set
2. a histogram is plotted of the ``fare`` column from the current (titanic) data set, generating an output file called ``hist.fare.png`` 
3. input is read from the ``iris.csv`` file, this becomes the new current data set, replacing the titanic data set, which is now discarded 
4. a count plot is created using the ``species`` column for the X axis from the current (iris) data set, generating an output file called ``count.species.png``
