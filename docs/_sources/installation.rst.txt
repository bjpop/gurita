Installation 
*****************************

Gurita requires Python 3.6 or greater and relies heavily on the following libraries: `NumPy <https://numpy.org/>`_, `SciPy <https://www.scipy.org/>`_, `Pandas <https://pandas.pydata.org/>`_, `Seaborn <https://seaborn.pydata.org/>`_ (and hence `Matplotlib <https://matplotlib.org/>`_), `Scikit-learn <https://scikit-learn.org/>`_.

You can install gurita :ref:`directly from source <install_src>` code.

.. _install_src:

Installing directly from source code
====================================

Clone this repository:

.. code-block:: bash

    git clone https://github.com/bjpop/gurita

Move into the repository directory:

.. code-block:: bash

    cd gurita

Python 3 is required for this software.

Gurita can be installed using ``pip`` in a variety of ways:

1. Inside a virtual environment:

.. code-block:: bash

    python3 -m venv gurita_dev
    source gurita_dev/bin/activate
    pip install -U /path/to/gurita

2. Into the global package database for all users:

.. code-block:: bash

    pip install -U /path/to/gurita

3. Into the user package database (for the current user only):

.. code-block:: bash

    pip install -U --user /path/to/gurita
