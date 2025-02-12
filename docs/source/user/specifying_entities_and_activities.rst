.. _specifying_entities_and_activities:

Specifying Provenance Patterns
==============================
Provenance patterns are declarative specifications of the provenance entities, agents and activities of interest, and their expected relations.
In SimProV, the provenance patterns are specified using `YAML <https://yaml.org/>`_.

Specifying Entities and Agents
------------------------------

Each entity- and agent-specifications begins with a name followed by sub-mapping called ``attributes``, listing the attributes of the provenance entity/agent.
Attributes are specified as a sequence of attributes names.
Attributes marked with ``$`` denote primary key attributes, while ``!`` signifies mandatory attributes.
Optional attributes are assumed by default.
Additionally, a meta sub-mapping controls rendering attributes in the web interface.

.. code-block:: yaml

    # Entities
	Simulation Model:
		attributes:
			- File Path$
			- Name!
			- Specification

	Experiment:
		attributes:
			- File Path$
			- Name!
			- Specification

	Simulation Data:
		attributes:
			- File Path$
			- Name!
			- Content

	# Agents
	Tellurium:
		attributes:
			- Version$

Specifying Activities
---------------------

Activity specifications begin with the activity name followed by three sub-mappings: ``usage``, ``generation,`` and ``association``, describing dependencies between the activity, entities, and agents.
Modifiers at the end of entity/agent names indicate occurrence frequency in dependencies:

- ``?``: Optional (Zero or One)
- ``*``: Arbitrary often (Zero or More)
- ``+``: At least once (One or More)

Entities/agents without a modifier have to occur exactly once.

.. code-block:: yaml

    # Activities
	Executing Experiment:
		usage:
			- Simulation Model
			- Simulation Experiment
		generation:
			- Simulation Data+
		association:
			- Tellurium

