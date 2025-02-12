.. _quickstart:

Quickstart
==========

The :ref:`default installations <installation_simprov>` offer straightforward methods to install SimProv as it is.
However, if you simply want to utilize SimProv without diving into its intricacies, we highly recommend following this guide.

With our quickstart template, you can concentrate on specifying the rules and provenance patterns relevant to your needs.
This template serves as a comprehensive solution for your provenance capturing requirements.
Moreover, it seamlessly integrates with our :ref:`web interface <simprov_web>`, enhancing your experience with SimProv.

Dependencies
------------

For using our Quickstart template, you have to install:

    - `Docker`_ provides a OS-level virtualization solution.
    - `Docker Compose`_ allows to declaratively describe and deploy multiple Docker services.

    .. _Docker: https://docs.docker.com/get-docker/
    .. _Docker Compose: https://docs.docker.com/compose/install/



Usage
-----

Step 0 - Installing the Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install the mentioned dependencies mentioned above.
The links should directly bring you the installation manuals.

After the installation, you should get the similar output when running the command in your terminal:

.. code-block:: console

    $ docker info

    Client:
     Version:    24.0.7
     Context:    default
     Debug Mode: false
     Plugins:
      compose: Docker Compose (Docker Inc.)
        Version:  2.23.3
        Path:     /usr/lib/docker/cli-plugins/docker-compose


Step 1 - Downloading the Quickstart Template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The quickstart template is available under: https://github.com/MosiSimprov/simprov-quickstart

You can download the template by running the following command:

.. code-block:: console

    $ git clone git@github.com:MosiSimprov/simprov-quickstart.git


Step 2 - Specifying the Rules and Provenance Patterns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you have to specify the rules and provenance patterns.
For this, the following files have to be modified:

- ``rules.py`` for specifying the rules (see :ref:`Specifying rules <rules>`)
- ``patterns.yaml`` for specifying the patterns (see :ref:`Specifying provenance patterns <specifying_entities_and_activities>`)
- ``requirements.txt`` for specifying additional Python dependencies for the rules , e.g., `CommonMark <https://commonmark.org/>`_ for extracting information from Markdown

Step 3 - Starting SimProv
^^^^^^^^^^^^^^^^^^^^^^^^^

After changing these files you can start SimProv via:

.. code-block:: console

    $ docker-compose up

.. note::

    Make sure you delete all Docker containers and images created by Docker Compose when adding a new dependency to the requirements.txt.


(OPTIONAL) - Enabling the web interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to run SimProv with the web interface enabled you should modify the ``docker-compose.yaml`` file to:

.. code-block:: yaml

    services:
      casestudy:
        build: .
        volumes:
          - ".:/case-study"
        command: simprov --state-file /case-study/study-state.pickle /case-study/patterns.yaml /case-study/rules.py
        ports:
            - "5000:5000"
      web:
        image: andreasruscheinski/simprovweb
        ports:
            - "1234:1234"
        command: "npm run start"

When now starting docker compose, you can find the webinterface under: http://localhost:1234/

.. note::

    If you want to ensure that the latest SimProv version is used, you have to rebuild the images and recreate the respective Docker container:
    `docker-compose down && docker-compose build --no-cache && docker-compose up -d --force-recreate`