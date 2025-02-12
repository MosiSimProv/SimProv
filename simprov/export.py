from io import StringIO

from prov.model import ProvDocument
from prov.serializers.provjson import ProvJSONSerializer
from pygraphviz import AGraph

from simprov import Entity
from simprov.provenance import ProvenanceGraph


def _to_dot_graph(provenance_graph: ProvenanceGraph) -> AGraph:
    def _node_attributes(entity: Entity):
        node_name = f"{provenance_entity.name}"
        attributes = {'node_label': node_name, "style": "rounded"}
        if "background-color" in provenance_entity.meta_information:
            attributes["style"] = "filled,rounded"
            attributes["fillcolor"] = f"{provenance_entity.meta_information['background-color']}"
        if "border-width" in provenance_entity.meta_information:
            attributes["penwidth"] = provenance_entity.meta_information["border-width"]
        if "border-color" in provenance_entity.meta_information:
            attributes["color"] = f"{provenance_entity.meta_information['border-color']}"
        return attributes

    dot_graph = AGraph(directed=True, name="G")
    dot_graph.graph_attr["rankdir"] = "RL"
    # Acitvities
    dot_graph.node_attr["shape"] = "box"
    for provenance_activity in provenance_graph.activities:
        node_names = f"{provenance_activity.name}"
        dot_graph.add_node(str(provenance_activity.id), label=node_names)
    # Entities
    dot_graph.node_attr["shape"] = "box"
    for provenance_activity in provenance_graph.activities:
        for provenance_entity in provenance_activity.used_entities:
            dot_graph.add_node(str(provenance_entity.id), **_node_attributes(provenance_entity))
            dot_graph.add_edge(str(provenance_activity.id), str(provenance_entity.id))
        for provenance_entity in provenance_activity.generated_entities:
            dot_graph.add_node(str(provenance_entity.id), **_node_attributes(provenance_entity))
            dot_graph.add_edge(str(provenance_entity.id), str(provenance_activity.id))
    return dot_graph


def to_dot(provenance_graph: ProvenanceGraph) -> str:
    """
    Returns the provenance graph in the DOT format.

    :param ProvenanceGraph provenance_graph:
    :return: The provenance graph in DOT format
    :rtype: str
    """
    return _to_dot_graph(provenance_graph).to_string()


def to_prov_json(provenance_graph: ProvenanceGraph) -> str:
    """
    Returns the provenance graph in the PROV-JSON format.

    :param ProvenanceGraph provenance_graph:
    :return: The provenance graph in PROV-JSON format
    :rtype: str
    """
    prov_document = ProvDocument()
    prov_document.set_default_namespace("http://example.org/")
    entity_table = {}
    for entity in provenance_graph.entities:
        entity_attributes = {}
        for (attribute, value) in entity.attributes.items():
            prov_attribute = str(attribute).replace(" ", "_")
            entity_attributes[prov_attribute] = str(value)
        entity_attributes["prov:node_label"] = entity.name
        provenance_entity = prov_document.entity(str(entity.id), entity_attributes)
        entity_table[entity.id] = provenance_entity
    for activity in provenance_graph.activities:
        prov_activity = prov_document.activity(str(activity.id), other_attributes={'prov:node_label': activity.name})
        for generated_entity in activity.generated_entities:
            prov_document.wasGeneratedBy(entity_table[generated_entity.id], prov_activity)
        for used_entity in activity.used_entities:
            prov_document.usage(prov_activity, entity_table[used_entity.id])
    prov_json_serializer = ProvJSONSerializer(prov_document)
    stream = StringIO()
    prov_json_serializer.serialize(stream)
    result = stream.getvalue()
    stream.close()
    return result
