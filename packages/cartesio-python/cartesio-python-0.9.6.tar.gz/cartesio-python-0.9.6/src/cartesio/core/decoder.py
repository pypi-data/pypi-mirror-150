import time
from typing import List

import numpy as np

from cartesio.core.genome import Genome, GenomeReader


class Decoder(GenomeReader):
    def __init__(self, shape, function_bundle, endpoint=None):
        super().__init__(shape)
        self.function_set = function_bundle
        self.endpoint = endpoint

    def to_json(self):
        decoding = {
            "metadata": {
                "rows": 1,  # single row CGP
                "columns": self.shape.nodes,
                "n_in": self.shape.inputs,
                "n_out": self.shape.outputs,
                "n_para": self.shape.parameters,
                "n_conn": self.shape.connections,
            },
            "functions": self.function_set.ordered_list,
            "_endpoint": None if not self.endpoint else self.endpoint.name,
        }
        return decoding

    def __genome_to_one_graph(self, genome, root):
        next_indices = root.copy()
        output_tree = root.copy()
        while next_indices:
            next_index = next_indices.pop()
            if next_index < self.shape.inputs:
                continue
            function_index = self.read_function(genome, next_index - self.shape.inputs)
            active_connections = self.function_set.arity_of(function_index)
            next_connections = set(
                self.read_active_connections(
                    genome, next_index - self.shape.inputs, active_connections
                )
            )
            next_indices = next_indices.union(next_connections)
            output_tree = output_tree.union(next_connections)
        return output_tree

    def read_active_nodes(self, G):
        graphs = []
        outputs = self.read_outputs(G)

        for output in outputs:
            root = {output[self.shape.con_idx]}
            one_graph = self.__genome_to_one_graph(G, root)
            graphs.append(sorted(list(one_graph)))

        return graphs

    def __decode_one(self, G: Genome, graphs: List, x: List):
        # fill output_map with inputs
        output_map = {i: x[i].copy() for i in range(self.shape.inputs)}
        # now, execute the functions
        for graph in graphs:
            for node in graph:
                # inputs are already in the map
                if node < self.shape.inputs:
                    continue
                node_index = node - self.shape.inputs
                # fill the map with active nodes
                function_index = self.read_function(G, node_index)
                arity = self.function_set.arity_of(function_index)
                connections = self.read_active_connections(G, node_index, arity)
                inputs = [output_map[c] for c in connections]
                p = self.read_parameters(G, node_index)
                value = self.function_set.execute(function_index, inputs, p)

                output_map[node] = value

        return [
            output_map[output_gene[self.shape.con_idx]]
            for output_gene in self.read_outputs(G)
        ]

    def functions_list(self, G):
        functions = {}
        graphs = self.read_active_nodes(G)
        for graph in graphs:
            for node in graph:
                # inputs are already in the map
                if node < self.shape.inputs:
                    continue
                node_index = node - self.shape.inputs
                # fill the map with active nodes
                function_index = self.read_function(G, node_index)
                function_name = self.function_set.name_of(function_index)
                if function_name not in functions.keys():
                    functions[function_name] = 0
                functions[function_name] += 1
        return functions

    def decode_population(self, population, x):
        y_pred = []
        for i in range(len(population.individuals)):
            y, t = self.decode_genome(population.individuals[i], x)
            population.set_time(i, t)
            y_pred.append(y)
        return y_pred

    def decode_genome(self, genome, x):
        """Decode the Genome given a list of inputs

        Args:
            genome (Genome): [description]
            x (List): [description]

        Returns:
            [type]: [description]
        """
        all_y_pred = []
        all_times = []
        graphs = self.read_active_nodes(genome)

        # for each image
        for xi in x:
            start_time = time.time()
            y_pred = self.__decode_one(genome, graphs, xi)
            if self.endpoint is not None:
                y_pred = self.endpoint.execute(y_pred)
            all_times.append(time.time() - start_time)
            all_y_pred.append(y_pred)
        whole_time = np.mean(np.array(all_times))
        return all_y_pred, whole_time


class GenomeToCode(Decoder):
    def to_code(self, node_name, genome):
        pass
