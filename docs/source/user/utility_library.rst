.. _utility_library:


SimProv Helper Library
=======================

This is a simple library that demonstrates how provenance can be captured from a Python environment.

At its core the library consists of three files for demonstrating different cpaturing approaches:

- `__init__.py` provides two simple functions which allow to configure the host and port of the provenance builder as well as allowing to send an event
- `base.py` consists of two functions that wraps the creation of specific events
- `tellurium.py` consists of a wrapper-function that calls Tellurium for running a simulation and sending the respecitive provenance events

Moreover, all of these implementations are based on each other to demonstrate how these concepts can be intertwined.


.. note::

    This library is just a proof of concept.
    The library was to be used with the corresponding rules and provenance pattern.
    The rules and patterns can be found as part of the `examples` of the SimProb-Quickstart template: https://github.com/MosiSimProv/simprov-quickstart
    The complete quickstart guide can be found under https://simprov.readthedocs.io/en/latest/user/quickstart.html.


Install and Usage
-----------------

Step 1 - Clone this repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    $ git clone https://github.com/MosiSimProv/simprovhelper.git

Step 2 - Install the library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We recommend to install the library in a virtual environment.
Moreover, you have to ensure the you install the library in the environment from which you want to execute your simulation experiments.

.. code-block:: console

    $ cd simprovhelper && pip install .



Support
-------

If you are having issues, please let me know.
You can write me a mail: andreas.ruscheinski@uni-rostock.de

