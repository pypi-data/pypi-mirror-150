from abc import ABC, abstractmethod
from typing import List


class Node(ABC):
    def __init__(self, name: str, arity: int, p: int):
        self.name = name
        self.arity = arity
        self.p = p


class WritableNode(Node, ABC):
    @abstractmethod
    def to_python(self, input_nodes: List, p: List, node_name: str):
        pass

    @abstractmethod
    def to_cpp(self, input_nodes: List, p: List, node_name: str):
        pass
