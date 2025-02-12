from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from uuid import uuid4, UUID

import networkx
from networkx import DiGraph, set_node_attributes, bfs_tree
from pygraphviz import AGraph

from simprov import Entity
from simprov.provenance import ProvenanceGraph, Activity


@dataclass
class ContextStackElement:
    what: str
    node_id: UUID
    entity_key: object = None


@dataclass
class GraphContext:
    activity: str = ""
    activity_id: UUID = None
    activity_nodes: List[UUID] = field(default_factory=list)
    entities: defaultdict = field(default_factory=lambda: defaultdict(lambda: []))
    last_nodes_stack: List[ContextStackElement] = field(default_factory=list)

    @property
    def nodes(self):
        result = list(self.activity_nodes)
        for value in self.entities.values():
            result += list(value)
        return set(result)

    @property
    def is_valid(self):
        return self.activity != ""

    def push_activity(self, tree_node):
        elem = ContextStackElement("Activity", tree_node)
        self.last_nodes_stack.append(elem)
        self.activity_nodes.append(tree_node)

    def push_entity(self, key, tree_node):
        elem = ContextStackElement("Entity", tree_node, key)
        self.last_nodes_stack.append(elem)
        self.entities[key].append(tree_node)

    def pop(self):
        elem = self.last_nodes_stack.pop()
        if elem.what == "Activity":
            self.activity_nodes.remove(elem.node_id)
        else:
            self.entities[elem.entity_key].remove(elem.node_id)


class GraphReducer:

    def __init__(self, provenance_graph: ProvenanceGraph, debug=False) -> None:
        super().__init__()
        self.flagged_entities = []
        self.provenance_graph = provenance_graph
        self.debug = debug
        self.draw_counter = 0

    def plot_graph(self, graph: DiGraph, label="", nodes_to_highlight=None):
        if nodes_to_highlight is None:
            nodes_to_highlight = []
        if not self.debug:
            return
        from networkx import draw_networkx_nodes, draw_networkx_edges, draw_networkx
        from networkx.drawing.nx_agraph import graphviz_layout
        import matplotlib.pyplot as plt

        dot_graph = AGraph(directed=True)
        dot_graph.graph_attr["rankdir"] = "RL"

        entities = [node for node in graph.nodes if graph.nodes[node]["type"] == "Entity"]
        activities = [node for node in graph.nodes if graph.nodes[node]["type"] == "Activity"]
        agents = [node for node in graph.nodes if graph.nodes[node]["type"] == "Agent"]

        for entity in entities:
            color = "orange" if entity in nodes_to_highlight else "green"
            node_label = str(entity)[:5]
            dot_graph.add_node(entity, label=node_label, style="filled", fillcolor=color)
        for activity in activities:
            color = "orange" if activity in nodes_to_highlight else "red"
            node_label = str(activity)[:5]
            dot_graph.add_node(activity, label=node_label, style="filled", fillcolor=color)
        for agent in agents:
            color = "orange" if agent in nodes_to_highlight else "pink"
            node_label = str(agent)[:5]
            dot_graph.add_node(agent, label=node_label, style="filled", fillcolor=color)

        for edge in graph.edges:
            dot_graph.add_edge(str(edge[0]), str(edge[1]))
        output_dir = Path("./img")
        if not output_dir.exists():
            output_dir.mkdir()
        file_name = f"{output_dir.resolve()}/{self.draw_counter:03d} {label}"
        dot_graph.write(file_name + ".dot")
        dot_graph.draw(file_name + ".png", prog="dot")

        self.draw_counter += 1

    @classmethod
    def reduce_provenance_graph(cls, provenance_graph: ProvenanceGraph) -> ProvenanceGraph:
        return cls(provenance_graph).reduce()

    def reduce(self, reduce_transitives=False, hide_nodes=False,split_agents=False) -> ProvenanceGraph:
        new_graph = self.reduce_graph()
        splitted_agent_table = {}

        if hide_nodes:
            old_graph = new_graph
            new_graph = old_graph.copy()
            nodes_to_hide = self.provenance_graph.hidden_nodes
            new_graph.remove_nodes_from(nodes_to_hide)
        if split_agents:
            old_graph = new_graph.copy()
            new_graph = self._split_agents(old_graph.copy(), splitted_agent_table)
        if reduce_transitives:
            old_graph = new_graph
            new_graph = networkx.transitive_reduction(old_graph)
            new_graph.add_nodes_from(old_graph.nodes(data=True))
            new_graph.add_edges_from((u, v, old_graph.edges[u, v]) for u, v in new_graph.edges)


        reduced_provenance_graph = self.build_reduced_provenance_graph(new_graph, hide_nodes,splitted_agent_table)
        reduced_provenance_graph.user_generated_dependencies = self.provenance_graph.user_generated_dependencies
        return reduced_provenance_graph

    def annotated_nx_graph(self):
        graph = self.provenance_graph.graph.copy()
        data = {
            node_id: {"original_in_degree": graph.in_degree[node_id], "original_out_degree": graph.out_degree[node_id]}
            for node_id in graph}
        set_node_attributes(graph, data)
        return graph

    def reduce_graph(self) -> DiGraph:
        # TODO: The reducer purges the agents nodes please track
        graph = self.annotated_nx_graph()
        self.plot_graph(graph, "Original Graph")
        reduced_graph = DiGraph()
        while True:
            in_degree_zero_nodes = [node for node in graph.nodes if graph.in_degree[node] == 0]
            if len(in_degree_zero_nodes) == 0:
                break
            self.plot_graph(graph, "In Degree Zero Nodes", in_degree_zero_nodes)
            for node in in_degree_zero_nodes:
                self.plot_graph(graph, "Current Graph to Work on with active node", [node])
                if node not in graph:
                    continue
                reduecable_context = self.calculate_reduceable_context(graph, node)
                self.plot_graph(graph, "Reduceable Graph", list(reduecable_context.nodes))
                reduced_subgraph = self.reduce_context_subgraph(graph, reduecable_context)
                self.plot_graph(reduced_subgraph, "Reduced Subgraph")
                self.merge_graphs(reduced_graph, reduced_subgraph)
                context_subgraph = self.subgraph_from_context(graph, reduecable_context)
                self.plot_graph(reduced_graph, "New Reduced Graph")
                node_to_remove = [node for node in context_subgraph if node not in reduced_subgraph]
                self.plot_graph(graph, "Remove nodes from graph", nodes_to_highlight=node_to_remove)
                graph.remove_nodes_from(node_to_remove)
                graph.remove_nodes_from([node for node in graph.nodes if graph.degree[node] == 0])
        return reduced_graph

    def build_reduced_provenance_graph(self, reduced_graph: DiGraph, hide_nodes=False,splitted_agent_table = {}):
        reduced_provenance_graph = ProvenanceGraph()
        for node in [node for node in reduced_graph.nodes if reduced_graph.nodes[node]["type"] == "Activity"]:
            node_data = reduced_graph.nodes[node]
            node_activity = node_data["name"]
            activity = Activity(node_activity)
            activity.id = node_data["context_id"]
            if hide_nodes and activity.id in self.provenance_graph.hidden_nodes:
                continue
            for pred in reduced_graph.predecessors(node):
                entity = self.provenance_graph.node_map[pred]
                activity.generated_entities.append(entity)
            for succ in reduced_graph.successors(node):
                succ_node = self.provenance_graph.node_map.get(succ,None)
                if succ_node is None:
                    succ_node = self.provenance_graph.node_map[splitted_agent_table[succ]]
                if isinstance(succ_node, Entity):
                    activity.used_entities.append(succ_node)
                else:
                    succ_node.id = succ
                    activity.associated_agents.append(succ_node)
            reduced_provenance_graph.add_activity(activity)
        return reduced_provenance_graph

    def calculate_reduceable_context(self, graph: DiGraph, starting_node):
        context = GraphContext()
        if graph.nodes[starting_node]["type"] == "Entity":
            context_bfs_tree = self.build_entity_bfs_tree(graph, starting_node)
        else:
            context_bfs_tree = self.build_activity_bfs_tree(graph, starting_node)
        self.plot_graph(graph, "Context BFS", context_bfs_tree.nodes)
        node_stack = list(context_bfs_tree)
        node_stack.reverse()
        dead_ends = set()
        while len(node_stack) != 0:
            tree_node = node_stack.pop()
            node_data = graph.nodes[tree_node]
            node_type = node_data["type"]
            if tree_node in dead_ends:
                continue
            if tree_node not in context.nodes:
                if node_type == "Activity":
                    context.push_activity(tree_node)
                    if not context.is_valid:
                        context.activity = node_data["name"]
                        context.activity_id = node_data["id"]
                        # TODO: There might be a problem when an activity generates more than one entity
                        continue
                else:
                    context.push_entity(node_data["primary_key"], tree_node)
                    # No activity was added to the context
            if not context.is_valid:
                continue
            # Flag entity if there is any activity != context activity
            if node_type == "Entity" or node_type == "Agent":
                for predecessor_activity in self.predecessors_actitvities(graph, tree_node):
                    if predecessor_activity["name"] != context.activity:
                        node_data["flag"] = True
                        self.flagged_entities.append(node_data["id"])

                titles = [activity["name"] for activity in self.predecessors_actitvities(graph, tree_node)]
                if any([title != context.activity for title in titles]):
                    node_data["flag"] = True
            # Can i Continue?
            if node_type == "Activity":
                # This was changed to neighbours
                pks = set([entity["primary_key"] for entity in self.graph_neighbours(graph, tree_node)])
                context_pks = set([entity for entity in context.entities])
                if pks != context_pks:
                    context.pop()
                    clean_nodes_tree = bfs_tree(context_bfs_tree, tree_node)
                    context_bfs_tree.remove_nodes_from(clean_nodes_tree)
                    for node in clean_nodes_tree:
                        if node in node_stack:
                            node_stack.remove(node)
            else:
                if node_data.get("flag", False):
                    clean_nodes_tree = bfs_tree(context_bfs_tree, tree_node)
                    context_bfs_tree.remove_nodes_from(clean_nodes_tree)
                    for node in clean_nodes_tree:
                        if node in node_stack:
                            node_stack.remove(node)
        return context

    def build_entity_bfs_tree(self, graph, starting_node):
        succ = list(graph.successors(starting_node))[0]
        activity = graph.nodes[succ]["name"]
        bfs_tree_result = bfs_tree(graph, succ)
        self.plot_graph(graph, "Original BFS Tree", nodes_to_highlight=bfs_tree_result)
        bfs_tree_result = self.clean_bfs_tree(graph, bfs_tree_result, activity, succ)
        bfs_tree_result.add_node(starting_node)
        bfs_tree_result.add_edge(starting_node, succ)
        bfs_tree_result = bfs_tree(bfs_tree_result, starting_node)
        return bfs_tree_result

    def build_activity_bfs_tree(self, graph, starting_node):
        activity = graph.nodes[starting_node]["name"]
        bfs_tree_result = bfs_tree(graph, starting_node)
        self.plot_graph(graph, "Original BFS Tree", nodes_to_highlight=bfs_tree_result)
        bfs_tree_result = self.clean_bfs_tree(graph, bfs_tree_result, activity, starting_node)
        return bfs_tree_result

    def clean_bfs_tree(self, graph, bfs_tree_result, activity, starting_node):
        nodes_to_remove = [node for node in bfs_tree_result if
                           graph.nodes[node]["type"] == "Activity" and graph.nodes[node][
                               "name"] != activity and node != starting_node]
        self.plot_graph(graph, "Nodes to Remove", nodes_to_highlight=nodes_to_remove)
        bfs_tree_result.remove_nodes_from(nodes_to_remove)
        bfs_tree_result = bfs_tree(bfs_tree_result, starting_node)
        return bfs_tree_result

    @staticmethod
    def predecessors_actitvities(graph, node):
        preds = list(graph.predecessors(node))
        return [graph.nodes[pred] for pred in preds if graph.nodes[pred]["type"] == "Activity"]

    @staticmethod
    def graph_neighbours(graph, node):
        succs = list(graph.successors(node))
        preds = list(graph.predecessors(node))
        return [graph.nodes[node] for node in succs + preds]

    def reduce_context_subgraph(self, graph, reduecable_context):
        activity_id = uuid4()
        reduced_sub_graph = DiGraph()
        sub_graph = self.subgraph_from_context(graph, reduecable_context)
        reduced_sub_graph.add_node(activity_id, name=reduecable_context.activity, type="Activity",
                                   context_id=reduecable_context.activity_id)

        one_degree_nodes = [node for node in sub_graph.nodes if sub_graph.degree[node] == 1]
        outputs = [node for node in one_degree_nodes if
                   sub_graph.out_degree[node] == 1 and (graph.nodes[node]["type"] == "Entity" or graph.nodes[node]["type"] == "Agent")]
        inputs = [node for node in sub_graph.nodes if
                  sub_graph.out_degree[node] == 0 and (graph.nodes[node]["type"] == "Entity" or graph.nodes[node]["type"] == "Agent")]
        for output in outputs:
            reduced_sub_graph.add_node(output, **graph.nodes[output])
            reduced_sub_graph.add_edge(output, activity_id)
            graph.nodes[output]["flag"] = True

        for input in inputs:
            reduced_sub_graph.add_node(input, **graph.nodes[input])
            reduced_sub_graph.add_edge(activity_id, input)
            graph.nodes[input]["flag"] = True

        return reduced_sub_graph

    @staticmethod
    def subgraph_from_context(graph, reduecable_context):
        sub_graph: DiGraph = graph.subgraph(reduecable_context.nodes).copy()
        return sub_graph

    @staticmethod
    def merge_graphs(reduced_graph, reduced_subgraph):
        data = {}
        reduced_graph.update(reduced_subgraph.edges, reduced_subgraph.nodes)
        for (node, node_data) in reduced_subgraph.nodes(data=True):
            data[node] = node_data
        set_node_attributes(reduced_graph, data)

    def _split_agents(self, old_graph:DiGraph,splitted_agent_table):
        agent_nodes = [node for node in old_graph if old_graph.nodes[node]["type"] == "Agent"]
        for agent_node in agent_nodes:
            node_data = old_graph.nodes[agent_node]
            associated_acitivity_ids = old_graph.predecessors(agent_node)
            for associated_acitivity_id in associated_acitivity_ids:
                new_agent_id = uuid4()
                old_graph.add_node(new_agent_id,**node_data)
                old_graph.add_edge(associated_acitivity_id,new_agent_id)
                splitted_agent_table[new_agent_id] = agent_node
            old_graph.remove_node(agent_node)
        return old_graph

