import json
import pickle
from pathlib import Path
from typing import Dict, List
from uuid import UUID

from simprov import Activity
from simprov.interface.restapi import RestAPI
from simprov.provenance import ProvenanceGraph
from simprov.reducer import GraphReducer
from simprov.rule_engine import RuleEngine
from simprov.specifications import SpecificationManager


class SimProv:
    """Represents an instance of SimProv.

    Every instance has its own :py:class:`.RuleEngine`, :py:class:`.SpecificationManager`, :py:class:`.ProvenanceGraph`,
    and :py:class:`.RestAPI`.

    During initialization the rules and specifications are automatically loaded.

    :param str rule_path:
        The path where the rules are located.
    :param str specifications_path:
        The path where the specifications are located.
    :param str state_file_path:
        The path to the file in which the state of SimProv should be stored.
    :ivar RuleEngine rule_engine:
        The rule engine.
    :ivar bool start_api:
        If true starts the REST API. Use only for testing/debugging purposes.
    :ivar SpecificationManager specification_manager:
        The specification manager.
    :ivar ProvenanceGraph provenance_graph:
        The provenance graph.
    :ivar RestAPI rest_api:
        The REST API.
    :ivar str state_file_path:
        The path to the state file.
    :ivar list event_log:
        A list of all processed events.
    """

    def __init__(self, rule_path: str, specifications_path: str,
                 state_file_path: str = "./study-state.pickle", start_api: bool = True):
        super().__init__()
        self.rule_engine: RuleEngine = RuleEngine()
        self.specification_manager: SpecificationManager = SpecificationManager()
        self.provenance_graph: ProvenanceGraph = ProvenanceGraph()
        self.rest_api: RestAPI = RestAPI(self)
        self.state_file_path: str = state_file_path
        self.event_log = []
        self.error_log: List[Exception] = []
        self.reduced_graph = None

        self.load_rules_and_specifications(rule_path, specifications_path)
        self.load_study_state(self.state_file_path)
        if start_api:
            self.rest_api.start()

    def load_rules_and_specifications(self, rule_path: str, specifications_path: str):
        """Loads the rules and specifications.

        :param str rule_path:
            The path where the rules are located.
        :param str specifications_path:
            The path where the specifications are located.
        """
        self.specification_manager.load_specification_file(specifications_path)
        self.rule_engine.load_rules(rule_path)

    def process_event(self, event: dict, save_study_state: bool = True):
        """ Processes an incoming event.

        The process consists of the following steps:

        1. Extracting the activity from the event using the rule engine
        2. Normalizing and validating the activity using the specification manager
        3. On success, the activity is chained with the provenance graph, the event is added to the event log and the REST-API emits an event signaling that the provenance graph has been updated.

        :param dict event:
            The event.
        :param bool save_study_state:
            True if the study state should be saved after processing the event
        :return:
            The extracted provenance activity.
        :rtype: Activity
        """
        try:
            if event["type"] == "Update Dependencies":
                self._update_dependencies(event)
            elif event["type"] == "Update Entity":
                self._update_entity_data(event)
            elif event["type"] == "Hide Node":
                self.provenance_graph.propagate_visibility_information(UUID(event["node_id"]), event["change"])
            else:
                self._process_capturer_event(event)
        except Exception as ex:
            print(f"Errorlog: {self.error_log}")
            self.error_log.append(ex)
            raise ex
        self.event_log.append(event)
        self.rest_api.socketio.emit("graph-update-event")
        if save_study_state:
            self.write_study_state()

    def _process_capturer_event(self, event: dict) -> Activity:
        extracted_activity = self.rule_engine.execute_rule(event)
        normalized_activity = self.specification_manager.normalize_activity(extracted_activity)
        self.specification_manager.validate_activity(normalized_activity)
        self.provenance_graph.chain_provenance_activity(normalized_activity)
        return normalized_activity

    def save_event_log(self, target_path: str):
        """ Saves the event log as JSON into a file.

        :param str target_path:
            The path at which the event log should be written.
        """
        json_str = json.dumps(self.event_log, indent=3)
        path = Path(target_path).resolve()
        with open(path, "w") as json_file:
            json_file.write(json_str)

    def reprocess_events_from_file(self, event_log_path: str):
        """ Loads events from a file and processes them.

        :param str event_log_path:
            The path at which the event log is stored.
        """
        events = json.load(open(event_log_path))
        self._reprocess_events(events)

    def get_study_state(self):
        """ Gets the current state of SimProv.

        :return: The state consists of provenance graph and the event log.
        :rtype: Tuple[ProvenanceGraph,List[Dict]]
        """
        return self.event_log

    def write_study_state(self, study_state_file_path: str = None):
        """ Writes the study state into a state file.

        :param str, optional study_state_file_path:
            The path of the state file. If `study_state_file_path` is ``None`` the instance ``state_file_path`` is used.
        """
        file_path = study_state_file_path
        if file_path is None:
            file_path = self.state_file_path
        with open(file_path, "wb") as pickle_file:
            pickle.dump(self.get_study_state(), pickle_file)

    def load_study_state(self, study_state_file_path: str = None):
        """ Loads the study state from a state file.

        Only loads the state file if the file exists.

        :param str, optional study_state_file_path:
            The path of the state file. If `study_state_file_path` is ``None`` the ``state_file_path`` is used.
        """
        file_path = study_state_file_path
        if file_path is None:
            file_path = self.state_file_path
        if not Path(file_path).exists():
            return
        with open(file_path, "rb") as pickle_file:
            events = pickle.load(pickle_file)
            self._reprocess_events(events)

    def delete_study_state(self, study_state_file_path: str = None):
        """ Deletes the study state file if exists.

        :param str, optional study_state_file_path:
            The path of the state file. If `study_state_file_path` is ``None`` the instance state file path is used.
        """
        file_path = study_state_file_path
        if file_path is None:
            file_path = self.state_file_path
        path = Path(file_path)
        if path.exists():
            path.unlink()

    def _update_entity_data(self, event: dict):
        node_id = UUID(event["node_id"])
        changes = event["changes"]
        if self.provenance_graph.is_entity(node_id):
            self.provenance_graph.update_entity_attributes(node_id, changes)

    def _update_dependencies(self, event):
        node_id = UUID(event["node_id"])
        changes = event["changes"]
        if self.provenance_graph.is_activity(node_id) and not self.check_dependencies_forms_cycle(changes):
            self.provenance_graph.update_activity_dependencies(node_id, changes)

    def check_dependencies_forms_cycle(self, dependencies: Dict) -> bool:
        """ Checks whether the new dependencies lead to a cycle in the provenance graph.

        :param Dict dependencies:
            A Dictionary with the new dependencies.
        :rtype bool:
        :return:
            `True` if changes leads to a cycle; `False` otherwise
        """
        return self.provenance_graph.are_dependencies_are_forming_a_cycle(dependencies)

    def _get_activity_node_data(self, base_data, node_id):
        user_generated_edges = []
        for edge in self.provenance_graph.user_generated_dependencies:
            if edge[0] == node_id:
                user_generated_edges.append(edge[1])
            elif edge[1] == node_id:
                user_generated_edges.append(edge[0])
        base_data["user_generated_edges"] = user_generated_edges
        base_data["hidden"] = True if node_id in self.provenance_graph.hidden_nodes else False

    def _get_entity_node_data(self, node_data):
        new_attributes = []
        for attribute in node_data["attributes"]:
            value = node_data["attributes"][attribute]
            attribute_data = {"name": attribute, "value": value,
                              "editable": self.specification_manager.is_editable(node_data["name"], attribute)}
            new_attributes.append(attribute_data)
        node_data["attributes"] = new_attributes

    def _get_agent_node_data(self, node_data):
        new_attributes = []
        for attribute in node_data["attributes"]:
            value = node_data["attributes"][attribute]
            attribute_data = {"name": attribute, "value": value,
                              "editable": False}
            new_attributes.append(attribute_data)
        node_data["attributes"] = new_attributes

    def _update_reduced_graph(self, reduce_transitives=False, hide_nodes=False, split_agents=False):
        graph_reducer = GraphReducer(self.provenance_graph)
        reduced_graph = graph_reducer.reduce(reduce_transitives, hide_nodes, split_agents)
        self.reduced_graph = reduced_graph

    def _reprocess_events(self, events):
        for event in events:
            self.process_event(event, False)
        self.write_study_state()
