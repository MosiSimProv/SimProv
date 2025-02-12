.. _capturer:

Building a Provenance Capturer
------------------------------

A provenance capturer has two primary tasks: detecting and collecting information about the modeler's activity within a software system and sending this information as an event to the provenance builder.

For Integrated Development Environments (IDEs) and libraries, plugin interfaces like those for PyCharm, :ref:`Visual Studio Code <vscode_plugin>`, or Notepad++ can be utilized.
These interfaces define functions triggered upon user interactions, allowing for the implementation of custom functions within them to gather information about user activity.

Software libraries require monitoring function calls to detect user activity.
Wrapper functions can be implemented to call original functions and gather relevant information about the activity.
Alternatively, you can also write a :ref:`utility library <utility_library>` that allows the modeler to send events directly to the provenance builder.
For simulation systems like COPASI or NetLogo, a combination of capturing approaches may be necessary, considering their IDEs and simulation libraries.

Once information is collected, it is encoded as an event using JSON format.
Each event must include a ``type`` key briefly describing the event's nature.
The event is then sent via a POST request to the :ref:`REST API <api>` of the provenance builder.

Below is an example of an event capturing the execution of a simulation experiment:

.. code-block:: json

    {
        "type": "Experiment Executed",
        "executed_experiment": "~/study/experiment.py",
        "experiment_specification": "...",
        "with_model": "~/study/my-model.mlr",
        "generated_data": "~/study/exp1-results.csv",
        "tellurium_version": "2.2.10",
        "model_specification": "..."
    }

A complete overview of the event processing process can be found :ref:`here <extracting>`.