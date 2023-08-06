import random
from abc import ABC, abstractmethod

from cartesio.core.helper import catalog_decorator


@catalog_decorator
class Catalog:

    _nodes = dict()

    @classmethod
    def include(cls, node):
        cls._nodes[node.name] = node

    @classmethod
    def get(cls, node_name):
        return cls._nodes[node_name]

    @classmethod
    @abstractmethod
    def fill(cls):
        pass


class Bundle(ABC):
    def __init__(self, catalog):
        self.__nodes = {}
        self.catalog = catalog
        self.fill()

    @abstractmethod
    def fill(self):
        pass

    def add_node(self, node_name):
        self.__nodes[len(self.__nodes)] = self.catalog.get(node_name)

    def add_bundle(self, bundle):
        for f in bundle.nodes:
            self.add_node(f.name)

    def get_random_parameters_for_function(self, function_index):
        return self.__nodes[function_index].get_random_parameters()

    def get_random_parameter_for_function(self, function_index, parameter_index):
        return self.__nodes[function_index].get_random_parameters()

    def name_of(self, i):
        return self.__nodes[i].name

    def arity_of(self, i):
        return self.__nodes[i].arity

    def parameters_of(self, i):
        return self.__nodes[i].p

    def execute(self, name, connections, parameters):
        return self.__nodes[name](connections, parameters)

    def show(self):
        for i, node in self.__nodes.items():
            print(f"[{i}] - {node.name}")

    @property
    def random_index(self):
        return random.choice(self.keys)

    @property
    def last_index(self):
        return len(self.__nodes) - 1

    @property
    def nodes(self):
        return list(self.__nodes.values())

    @property
    def keys(self):
        return list(self.__nodes.keys())

    @property
    def max_arity(self):
        return max([self.arity_of(i) for i in self.keys])

    @property
    def max_parameters(self):
        return max([self.parameters_of(i) for i in self.keys])

    @property
    def size(self):
        return len(self.__nodes)

    @property
    def ordered_list(self):
        return [self.__nodes[i].name for i in range(self.size)]


class EmptyBundle(Bundle):
    def fill(self):
        pass
