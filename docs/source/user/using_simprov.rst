.. _using_simprov:

Using SimProv
-------------
Before you can use SimProv, you have to follow these steps:

    1. :ref:`Integration <capturer>`: Integrate SimProv with your preferred software systems or libraries by implementing provenance capturers. These capturers detect and collect information about the user's activities within the systems.
    2. :ref:`Pattern Specification <specifying_entities_and_activities>`: Secify patterns that describe the expected relationships between entities, activities, and agents in the simulation study. These patterns guide the construction of the provenance graph.
    3. :ref:`Rule Specification <rules>`: Define rules using Python functions to process the incoming events. These rules extract provenance information from the events and construct provenance activities.


