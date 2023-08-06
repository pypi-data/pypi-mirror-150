from io import BytesIO

import networkx as nx
import pygraphviz as pgv
from networkx.drawing.nx_agraph import from_agraph
from PIL import Image

from cartesio.core.decoder import Decoder


class GenomeViewer(Decoder):
    def __init__(self, metadata, function_set):
        super().__init__(metadata, function_set)

    def get_graph(self, genome, only_active=False, jupyter=False):
        G = pgv.AGraph(name="genome", directed="true")
        G.graph_attr["rankdir"] = "LR"
        G.graph_attr["ranksep"] = 0.75
        G.graph_attr["splines"] = "true"
        G.graph_attr["compound"] = "true"

        G.node_attr["fontsize"] = "12"
        G.node_attr["style"] = "filled"
        G.node_attr["shape"] = "ellipse"
        G.node_attr["fillcolor"] = "white"
        G.node_attr["fixedsize"] = "true"
        G.node_attr["width"] = 1.0
        G.node_attr["height"] = 0.5

        with G.subgraph(
            range(self.shape.inputs), name="cluster_inputs", penwidth=0, rank="source"
        ) as cluster_inputs:
            for node in range(self.shape.inputs):
                cluster_inputs.add_node(node, label=f"node_{node}", fillcolor="#B6D7A8")

        with G.subgraph(
            range(self.shape.inputs, self.shape.out_idx),
            name="cluster_genes",
            penwidth=0,
        ) as cluster_genes:
            for node in range(self.shape.inputs, self.shape.out_idx):
                function_index = self.read_function(genome, node - self.shape.inputs)
                function_name = self.function_set.name_of(function_index)
                cluster_genes.add_node(node, label=f"[{node}]\n{function_name}")
                active_connections = self.function_set.arity_of(function_index)
                connections = self.read_active_connections(
                    genome, node - self.shape.inputs, active_connections
                )
                parameters = self.read_parameters(genome, node - self.shape.inputs)

                for c in connections:
                    G.add_edge(c, node)

        with G.subgraph(
            range(self.shape.out_idx, self.shape.out_idx + self.shape.outputs),
            name="cluster_outputs",
            penwidth=0,
            rank="sink",
        ) as cluster_outputs:
            for node in range(
                self.shape.out_idx, self.shape.out_idx + self.shape.outputs
            ):
                c = self.read_outputs(genome)[node - self.shape.out_idx][
                    self.shape.con_idx
                ]
                cluster_outputs.add_node(
                    node, label=f"node_{node}", fillcolor="#F9CB9C"
                )
                G.add_edge(c, node)

        # converting pygraphviz graph to networkx graph
        X = from_agraph(G)
        max_rank = 0
        nodeshapeax_rank = 0
        for node_in in range(self.shape.inputs):
            # dictionary {node: length}
            lengths = nx.shortest_path_length(X, str(node_in))
            result = max(lengths.items(), key=lambda p: p[1])
            if result[1] > max_rank:
                max_rank = result[1]
                nodeshapeax_rank = result[0]

        for node_out in range(
            self.shape.out_idx, self.shape.out_idx + self.shape.outputs
        ):
            G.add_edge(nodeshapeax_rank, node_out, style="invis")

        G.layout(prog="dot")
        if jupyter:
            # create image without saving to disk
            return Image.open(BytesIO(G.draw(format="png")))
        return G


"""
    def save_graph_only_active(self, genome, filename, output_index=0):
        active_nodes = self.read_active_nodes(genome)[output_index]
        G = pgv.AGraph(directed=True)
        G.graph_attr["rankdir"] = "TB"
        G.graph_attr["splines"] = "ortho"
        map_nodes = {}
        for node in active_nodes:
            if node < self.shape.inputs:
                G.add_node(str(node) + ' - input', color='green')
                continue
            if node < self.shape.out_idx:
                function_index = self.read_function(genome, node-self.shape.inputs)
                active_connections = self.function_set.get_arity(function_index)
                connections = self.read_active_connections(genome, node-self.shape.inputs, active_connections)
                parameters = self.read_parameters(genome, node-self.shape.inputs)
                node_name = str(node) + ' - ' + self.function_set.get_function_name(function_index) + '(p=' + str(parameters) + ')'
                map_nodes[node] = node_name
                for c in connections:
                    if c < self.shape.inputs:
                        G.add_edge(str(c) + ' - input', map_nodes[node])
                    else:
                        G.add_edge(map_nodes[c], map_nodes[node])

        out_name = f'node_{self.shape.out_idx+output_index}'
        G.add_node(out_name, style='filled', fillcolor='#F9CB9C', shape='circle')
        G.add_edge(map_nodes[active_nodes[-1]], out_name)
        G.layout(prog='dot')
        G.draw(filename)
"""
