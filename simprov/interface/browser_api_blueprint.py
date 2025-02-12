import json
from copy import deepcopy
from copy import deepcopy
from tempfile import mkstemp
from uuid import UUID

from flask import Blueprint, jsonify, request, send_file

from simprov import Activity
from simprov.exceptions import InvalidActivityException
from simprov.export import to_prov_json, _to_dot_graph, to_dot
from simprov.interface.wrapper import BlueprintWrapper


class BrowserAPI(BlueprintWrapper):

    def _get_provenance_graph_cytoscape_data(self, show_reduced_graph: bool = False, reduce_transitives: bool = False,
                                             hide_nodes: bool = False, split_agents: bool = False):

        graph = self._get_provenance_graph(show_reduced_graph, reduce_transitives, hide_nodes, split_agents)
        graph.hidden_nodes = self.simprov.provenance_graph.hidden_nodes
        return graph.cytoscape_data()

    def _get_provenance_graph(self, show_reduced_graph: bool = False, reduce_transitives: bool = False,
                              hide_nodes: bool = False, split_agents: bool = False):
        graph = self.simprov.provenance_graph
        if show_reduced_graph:
            self.simprov._update_reduced_graph(reduce_transitives, hide_nodes, split_agents)
            graph = self.simprov.reduced_graph
        return graph

    def _get_node_data(self, node_id: UUID, query_reduced_graph: bool = False) -> dict:
        """Gets the node data for the webinterface.

        node_id : UUID
            The node_id of the node.
        query_reduced_graph: bool
            If `True` the node data is queried from the reduced provenance graph.

        :py:meth:`.ProvenanceGraph.node_data`
        """
        graph = self.simprov.provenance_graph
        if query_reduced_graph:
            # self.simprov._update_reduced_graph()
            graph = self.simprov.reduced_graph
        node_data = graph.node_data(node_id)
        if graph.is_entity(node_id):
            self.simprov._get_entity_node_data(node_data)
        elif graph.is_agent(node_id):
            self.simprov._get_agent_node_data(node_data)
        else:
            self.simprov._get_activity_node_data(node_data, node_id)
        if node_data["name"] == "Simulation Model":
            for attribute in node_data["attributes"]:
                if attribute["name"] == "Content":
                    print(attribute["value"])
        return node_data

    def _build_copy_activity_with_changes(self, request_json):
        activity_node: Activity = self.simprov.provenance_graph.node_map[UUID(request_json["node"])]
        copy_node: Activity = deepcopy(activity_node)
        for edge in request_json["changes"]:
            source_id = UUID(edge["source"])
            target_id = UUID(edge["target"])
            if source_id == copy_node.id:
                copy_node.used_entities.append(self.simprov.provenance_graph.node_map[target_id])
            elif target_id == copy_node.id:
                copy_node.generated_entities.append(self.simprov.provenance_graph.node_map[source_id])
        return copy_node

    def _check_activity_validity_after_dependency_addition(self, request_json):
        activity_copy = self._build_copy_activity_with_changes(request_json)
        try:
            self.simprov.specification_manager.validate_activity(activity_copy)
        except InvalidActivityException as ex:
            return False
        return True

    def _hide_node(self, request_json):
        node_id = UUID(request_json["id"])
        hidden = request_json["changes"]
        event = {"type": "Hide Node", "node_id": str(node_id), "change": hidden}
        self.simprov.process_event(event)

    def _build_graph_style(self):
        entries = []
        for entity in self.simprov.specification_manager.entity_specifications.values():
            selector_str = f'node[name=\"{entity.name}\"]'
            style_parts = []
            if entity.style_info == {}:
                continue
            for (key, value) in entity.style_info.items():
                style_parts.append(f"{key}: {value}")
            style_str = "{" + ";".join(style_parts) + "}"
            entries.append(f"{selector_str}{style_str}")
        return entries

    def _build_blueprint(self):
        blueprint = Blueprint("browser_api", __name__)

        @blueprint.get("/provenance-data")
        def get_provenance_data():
            """ Gets the provenance graph data for the webinterface.

            The data is returned in the JSON format for Cytoscape.

            The following GET parameters are supported:
                - `showReducedGraph`: `True` if the reduced graph shall be displayed in the web interface; `False` otherwise
                - `reduceTransitive`: `True` if the transitive closure of the graph shall be computered; `False` otherwise
                - `hideNodes`: `True` if nodes that are markd as hidden shall be removed from the graph; `False` otherwise
                - `splitAgents`: True` if agents shall be split; `False` otherwise
            """
            show_reduced_graph = request.args.get("showReducedGraph", default=False, type=lambda v: v.lower() == 'true')
            reduce_transitives = request.args.get("reduceTransitives", default=False,
                                                  type=lambda v: v.lower() == 'true')
            hide_nodes = request.args.get("hideNodes", default=False,
                                          type=lambda v: v.lower() == 'true')
            split_agents = request.args.get("splitAgents", default=False, type=lambda v: v.lower() == 'true')
            data = self._get_provenance_graph_cytoscape_data(show_reduced_graph, reduce_transitives, hide_nodes,
                                                             split_agents)
            return jsonify(data)

        @blueprint.get("/node-data")
        def get_node_data():
            args = request.args.to_dict()
            uuid = UUID(args["id"])
            query_reduced_graph = request.args.get("reducedGraph", default=False, type=lambda v: v.lower() == 'true')
            node_data = self._get_node_data(uuid, query_reduced_graph)
            return jsonify(node_data)

        @blueprint.post("/update-entity")
        def update_entity():
            request_json = request.json
            event = {"type": "Update Entity", "node_id": str(request_json["id"]), "changes": request_json["changes"]}
            self.simprov.process_event(event)
            return ('', 204)

        @blueprint.post("/update-activity")
        def update_dependencies():
            request_json = request.json
            event = {"type": "Update Dependencies", "node_id": str(request_json["id"]),
                     "changes": request_json["changes"]}
            self.simprov.process_event(event)
            return ('', 204)

        @blueprint.post("/check-dependency-froms-cycle")
        def check_dependencies():
            request_json = request.json

            result = self.simprov.check_dependencies_forms_cycle(request_json)
            return {"result": result}

        @blueprint.post("/dependency-valid-activity")
        def check_valid_activity():
            request_json = request.json
            result = self._check_activity_validity_after_dependency_addition(request_json)
            return {"result": result}

        @blueprint.get("/event-log")
        def get_event_log():
            return jsonify(self.simprov.event_log)

        @blueprint.get("/error-log")
        def get_error_log():
            error_json = []
            for ex in self.simprov.error_log:
                ex_json = {'type': type(ex).__name__, 'message': ex.args[0]}
                error_json.append(ex_json)
            return jsonify(error_json)

        @blueprint.post("/hide-node")
        def hide_node():
            request_json = request.json
            self._hide_node(request_json)
            return ('', 204)

        @blueprint.get("/graph-style")
        def get_graph_style():
            result = self._build_graph_style()
            return jsonify(result)

        @blueprint.get("/graph-events")
        def get_graph_events():
            event_log_json = json.dumps(self.simprov.event_log)
            (handle, path) = mkstemp(text=True)
            with open(path, "w") as of:
                of.write(event_log_json)
            res = send_file(path, download_name="events.json", mimetype="application/json",
                            as_attachment=True)
            return res

        @blueprint.get("/graph-json")
        def get_graph_json():
            show_reduced_graph = request.args.get("showReducedGraph", default=False, type=lambda v: v.lower() == 'true')
            reduce_transitives = request.args.get("reduceTransitives", default=False,
                                                  type=lambda v: v.lower() == 'true')
            hide_nodes = request.args.get("hideNodes", default=False, type=lambda v: v.lower == 'true')
            split_agents = request.args.get("splitAgents", default=False, type=lambda v: v.lower() == 'true')

            graph = self._get_provenance_graph(show_reduced_graph, reduce_transitives, hide_nodes,split_agents)
            graph = self._get_provenance_graph(show_reduced_graph, reduce_transitives, hide_nodes)
            json_str = to_prov_json(graph)
            (handle, path) = mkstemp(text=True)
            with open(path, "w") as of:
                of.write(json_str)
            res = send_file(path, download_name="provenance_graph.json", mimetype="application/json",
                            as_attachment=True)
            return res

        @blueprint.get("/graph-dot")
        def get_graph_dot():
            show_reduced_graph = request.args.get("showReducedGraph", default=False, type=lambda v: v.lower() == 'true')
            reduce_transitives = request.args.get("reduceTransitives", default=False,
                                                  type=lambda v: v.lower() == 'true')
            hide_nodes = request.args.get("hideNodes", default=False, type=lambda v: v.lower() == 'true')
            split_agents = request.args.get("splitAgents", default=False, type=lambda v: v.lower() == 'true')

            graph = self._get_provenance_graph(show_reduced_graph, reduce_transitives, hide_nodes,split_agents)
            dot_graph_str = to_dot(graph)
            (handle, path) = mkstemp(text=True)
            with open(path, "w") as of:
                of.write(dot_graph_str)
            res = send_file(path, download_name="provenance_graph.dot", mimetype="application/text", as_attachment=True)
            return res

        return blueprint
