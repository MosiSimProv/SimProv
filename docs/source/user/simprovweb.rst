.. _simprov_web:

SimProvWeb
==========

Features
--------
- User-friendly web interface for exploring the captured provenance graph, enabling researchers to visualize and analyze the history of their simulation studies.
- Exporting the captures provenance information
- View the provenance graph in an aggregated form
- Inspecting all events and errors
- Automatically refreshing the provnenace graph when new provenance information was captured


Dependencies
------------

* `NodeJS`_ is a micro web framework (Tested Version: v21.5.0).
* `NPM`_ is a package manager for JavaScript (Tested Version: 10.3.0).

.. _NPM: https://www.npmjs.com/
.. _NodeJS: https://nodejs.org/en


Install and Usage
-----------------

The web interface assumes that the SimProv provenance capturer is running under port 5000.

Manual Install
^^^^^^^^^^^^^^

After installing the dependencies, you should be able to run the web interface via:

.. code-block:: console

    $ npm run dev

    > simprov-web@1.0.0 dev
    > parcel ./src/index.html --open --no-cache

    Server running at http://localhost:1234

Afterwards, you can access the webinterface under `localhost:1234`.

Docker
^^^^^^

We also provide the web interface as a Docker image:

.. code-block:: console

    $ docker run andreasruscheinski/simprovweb npm run start

    > simprov-web@1.0.0 start
    > parcel --no-cache

    Server running at http://localhost:1234

Afterwards, you can access the webinterface under `localhost:1234`.


Contribute
----------

- Source Code: https://github.com/MosiSimprov/SimProvWeb
- Issue Tracker: https://github.com/MosiSimprov/SimProvWeb/issues


Support
-------

If you are having issues, please let me know.
You can write me a mail: andreas.ruscheinski@uni-rostock.de

