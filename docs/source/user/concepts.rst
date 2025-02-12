User Guide
==========
SimProv relies on a strict separation of concerns between two key components: `provenance capturers` and a `provenance builder`.

The `provenance capturers` are responsible for detecting and collecting information about the modeler's activities :ref:`from different software systems <capturer>`.
They function as clients, gathering data related to the development of the simulation model, execution of simulation experiments, and analysis of results.
These capturers ensure that relevant information is captured in real-time as the simulation study progresses.

The `provenance builder`, i.e., the software you are currently learning about in this documentation, operates as a server and processes the information collected by the capturers.
It :ref:`extracts provenance information <extracting>` from the collected data and constructs a provenance graph.
This graph represents the relationships between entities, activities, and agents involved in the simulation study, providing a clear overview of the study's history.


.. toctree::
    :maxdepth: 3
    :caption: Table of Contents

    using_simprov

    building_capturer

    specifying_entities_and_activities
    specifying_rules
    extracting_provenance



