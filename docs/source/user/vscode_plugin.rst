.. _vscode_plugin:

VSCode Plugin
=============

An exemplary provenance capturer for VSCode.

.. note::

    This plugin is just a proof of concept.
    The plugin was to be used with the corresponding rules and provenance pattern.
    The rules and patterns can be found as part of this artifact: ????

.. todo::

    Add the link above.

Features
--------
- Capturing provnenance information from Visual Studio Code
- Custom commands for creating new assumptions, requirements, simulation models, and experiments

Conventions
-----------

This capturer mainly relies on the following file conventions:

    - Research Question: ``research question.md`` (Markdown)
    - Assumption : ``assumption(.|\s)*\.md`` (Markdown)
    - Reference : ``reference(.|\s)*\.md`` (Markdown)
    - Requirement: ``requirement(.|\s)*\.md`` (Markdown)
    - Simulation Model: ``model(.|\s)*\.mlr`` (ML-Rules)
    - Experiment: ``experiment(.|\s)*\.py`` (Python)


Commands
--------

- ``New Simulation Study`` - Creates a new simulation study; Allows you to create and select a directory. Will create a ``.study`` file storing internal information.
- ``New Research Question`` - Will create a new file for specifying the research question of the study. Also allows to select references based on which the research question was derived.
- ``New Assumption`` - Will create a new file for specifying an assumption. Also allows to select references based on which the assumption was derived.
- ``New Requirement`` - Will create a new file for specifying a requirement. Also allows to select references based on which the requirement was derived.
- ``New Simulation Model`` - Will create a new file for a simulation model. Also allows to select requirements and assumptions to make their relation explicit.
- ``New Simulation Experiment`` - Will create a new file for a simulation experiment. Also allows to select a simulation model, requirements and assumptions to make their relation explicit.
- ``New Reference`` - Will create a new file for a reference.

Dependencies
------------

* `Visual Studio Code`_ the new fancy editor everyone seems to love (Version Tested: 1.86.2).

.. _Visual Studio Code: https://code.visualstudio.com/



Install and Usage
-----------------

Just install the  ``simprov-vsc-capturer-0.0.1.vsix`` file from the repository with VSCode.

Contribute
----------

- Source Code: https://github.com/MosiSimprov/simprov-vsc-capturer
- Issue Tracker: https://github.com/MosiSimprov/simprov-vsc-capturer/issues
- Documentation: ???

.. todo:: Add links above

Support
-------

If you are having issues, please let me know.
You can write me a mail: andreas.ruscheinski@uni-rostock.de

