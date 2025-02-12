.. _installation_simprov:

Installation
============

This guide describes how you can install SimProv.

.. note::
    If you just want to use SimProv, we recommend using our :ref:`quickstart template <quickstart>`.


Getting the Source
------------------
You can download the current version of SimProvWeb from Github:

.. code-block:: console

    $ git clone git@github.com:MosiSimprov/SimProv.git

Python Version
--------------
We recommend using the latest version of Python. SimProv supports Python 3.10 and newer.

These packages will be installated automatically when installing SimProv:

* `PyYAML`_ implements a YAML parser.
* `Flask`_ is a micro web framework.
* `Flask-CORS`_ extends Flask to handle Cross Origin Resource Sharing (CORS).
* `Flask-SocketIO`_  implements bi-directional communications between the clients and the FLASK server.
* `Eventlet`_ is a concurrent networking library.
* `NetworkX`_ is library providing data structures and algorithms for working with graphs.

.. _PyYAML: https://pyyaml.org/
.. _Flask: https://flask.palletsprojects.com/en/2.3.x/
.. _Flask-CORS: https://flask-cors.readthedocs.io/en/latest/
.. _Flask-SocketIO: https://flask-socketio.readthedocs.io/en/latest/
.. _Eventlet: https://eventlet.net/
.. _NetworkX: https://networkx.org/

Method 1 - Manual Installation
------------------------------
To install SimProv, simply run this simple command in your terminal after entering ``simprov`` directory:

.. code-block:: console

    $ cd simprov
    $ pip install .

We recommend installing SimProv in its own `virtual environment`_ to prevent any conflicts with already installed Python libraries.

.. _`virtual environment`: https://docs.python.org/3/library/venv.html


After the installation, you should get the following output when trying to start SimProv:

.. code-block:: console

    $ simprov -h

    SIMPROV
    usage: simprov [-h] [--state-file STATE_FILE] pattern_specification rule_specification

    Starts the SimProv provenance builder.

    positional arguments:
      pattern_specification
                            The path to the pattern specification file (YAML)
      rule_specification    The path to the rule specification file (PYTHON).

    options:
      -h, --help            show this help message and exit
      --state-file STATE_FILE
                            The path to the file storing the provenance information. Will be written using pickle.




Method 2 - Build a Docker Image
-------------------------------

Alternatively, you can build a Docker image that contains SimProv via:

.. code-block:: console

    $ docker build -t simprov .

Afterwards, you can verify your Docker image by running:

.. code-block:: console

    $ docker run simprov simprov -h

    SIMPROV
    usage: simprov [-h] [--state-file STATE_FILE] pattern_specification rule_specification

    Starts the SimProv provenance builder.

    positional arguments:
      pattern_specification
                            The path to the pattern specification file (YAML)
      rule_specification    The path to the rule specification file (PYTHON).

    options:
      -h, --help            show this help message and exit
      --state-file STATE_FILE
                            The path to the file storing the provenance information. Will be written using pickle.


Method 3 - Download Pre-build Docker Image
------------------------------------------

Finally, you can also download a pre-build Docker image:

.. code-block:: console

    $ docker pull andreasruscheinski/simprov

Afterwards, you can verify your Docker image by running:

.. code-block:: console

    $ docker run andreasruscheinski/simprov simprov -h

    SIMPROV
    usage: simprov [-h] [--state-file STATE_FILE] pattern_specification rule_specification

    Starts the SimProv provenance builder.

    positional arguments:
      pattern_specification
                            The path to the pattern specification file (YAML)
      rule_specification    The path to the rule specification file (PYTHON).

    options:
      -h, --help            show this help message and exit
      --state-file STATE_FILE
                            The path to the file storing the provenance information. Will be written using pickle.

.. note::
    This installation only provides SimProv as it is.

    If you want to use SimProv with addtional dependencies, e.g., libraries used by the rules to extract information from the event, you should use our :ref:`quickstart image <quickstart>`.