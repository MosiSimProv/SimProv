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

    # Activities
    Executing Experiment:
        usage:
            - Simulation Model
            - Experiment
        generation:
            - Simulation Data+
        association:
            - Tellurium