import random

import numpy as np

from cartesio.core.genome import Genome, GenomeShape
from cartesio.core.mutation import Mutation


class GoldmanWrapper:
    def __init__(self, mutation, decoder):
        self.mutation = mutation
        self.decoder = decoder

    def mutate(self, genome):
        changed = False
        active_nodes = self.decoder.read_active_nodes(genome)
        while not changed:
            genome = self.mutation.mutate(genome)
            new_active_nodes = self.decoder.read_active_nodes(genome)
            changed = active_nodes != new_active_nodes
        return genome


class MutationClassic(Mutation):
    def __init__(self, shape, n_functions, mutation_rate, output_mutation_rate):
        super().__init__(shape, n_functions)
        self.mutation_rate = mutation_rate
        self.output_mutation_rate = output_mutation_rate
        self.init()

    def init(self):
        self.n_mutations = int(
            np.floor(self.shape.nodes * self.shape.w * self.mutation_rate)
        )
        self.all_indices = np.indices((self.shape.nodes, self.shape.w))
        self.all_indices = np.vstack(
            (self.all_indices[0].ravel(), self.all_indices[1].ravel())
        ).T
        self.sampling_range = range(len(self.all_indices))

    def mutate(self, G):
        sampling_indices = np.random.choice(
            self.sampling_range, self.n_mutations, replace=False
        )
        sampling_indices = self.all_indices[sampling_indices]

        for idx, mutation_parameter_index in sampling_indices:
            if mutation_parameter_index == 0:
                self.mutate_function(G, idx)
            elif mutation_parameter_index <= self.shape.connections:
                connection_idx = mutation_parameter_index - 1
                self.mutate_connections(G, idx, only_one=connection_idx)
            else:
                parameter_idx = mutation_parameter_index - self.shape.connections - 1
                self.mutate_parameters(G, idx, only_one=parameter_idx)
        for output in range(self.shape.outputs):
            if random.random() < self.output_mutation_rate:
                self.mutate_output(G, output)
        return G


class MutationAllRandom(Mutation):
    """
    Can be used to initialize genome (G) randomly
    """

    def __init__(self, metadata: GenomeShape, n_functions: int):
        super().__init__(metadata, n_functions)

    def mutate(self, G: Genome):
        # mutate genes
        for i in range(self.shape.nodes):
            self.mutate_function(G, i)
            self.mutate_connections(G, i)
            self.mutate_parameters(G, i)
        # mutate outputs
        for i in range(self.shape.outputs):
            self.mutate_output(G, i)
        return G


class CopyGenome:
    def __init__(self, genome: Genome):
        self.genome = genome

    def mutate(self, G: Genome):
        return self.genome.clone()
