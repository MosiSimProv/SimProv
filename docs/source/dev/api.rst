.. _api:

REST-API
========

Capturer API
------------
.. http:post:: capturer/process-event

    Allows to send an event to SimProv for processing.

    See :ref:`capturer`


Web API
--------
.. http:get:: /provenance-data

    Returns the provenance graph for the webinterface in the Cytoscape JSON format.

   :query showReducedGraph: `true` if the reduced graph shall be displayed in the web interface; `false` otherwise
   :query reduceTransitive: `true` if the transitive closure of the graph shall be computered; `false` otherwise
   :query hideNodes: `true` if nodes that are markd as hidden shall be removed from the graph; `false` otherwise
   :query splitAgents: `true` if agents shall be split in the graph; `false` otherwise

.. http:get:: /node-data

    Returns the node data in JSON.

   :query id: The id of the node
   :query reducedGraph: `true` if the node information shall be collected from the reduced graph

.. http:post:: /update-entity

    Updates the node data of an entity.

    :<json id: The id of the node
    :<json changes: Object with keys are the names of the attributes and the value are the new values

.. http:post:: /update-activity

    Updates the dependencies of an activity.

    :<json id: The id of the node
    :<json changes: Object with keys are the source ids and values are the target ids

.. http:post:: /check-dependency-froms-cycle

    Checks whether the new dependencies form a circle

    :<json node: The id of the node
    :<json changes: Object with keys are the source ids and values are the target ids
    :>json result: `True` if depedencies form a cycle, `False` otherwise

.. http:get:: /event-log

    Returns all collected events in JSON.

.. http:get:: /error-log
    Returns all collected errors in JSON.

.. http:get:: /graph-style

    Returns all the graph style for rendering the provenance graph in JSON.

.. http:get:: /graph-events

    Allows to download a file with all events.

.. http:get:: /graph-json

    Allows to download a file with all provenance information formatted in PROV-JSON.

   :query showReducedGraph: `true` if the reduced graph shall be exported, `false` otherwise
   :query reduceTransitive: `true` if the transitive closure of the graph shall be computered; `false` otherwise
   :query hideNodes: `true` if nodes that are markd as hidden shall be removed from the graph; `false` otherwise
   :query splitAgents: `true` if agents shall be split in the graph; `false` otherwise

.. http:get:: /graph-dot

    Allows to download a DOT file containing the provenance graph.

   :query showReducedGraph: `true` if the reduced graph shall be exported, `false` otherwise
   :query reduceTransitive: `true` if the transitive closure of the graph shall be computered; `false` otherwise
   :query hideNodes: `true` if nodes that are markd as hidden shall be removed from the graph; `false` otherwise
   :query splitAgents: `true` if agents shall be split in the graph; `false` otherwise
