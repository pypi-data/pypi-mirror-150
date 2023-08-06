from abc import ABC, abstractmethod
from typing import List

from cartesio.core.node import Node


class Endpoint(Node, ABC):
    def __init__(self, name: str, arity: int):
        super().__init__(name, arity, 0)

    @abstractmethod
    def execute(self, entries: List):
        pass


class EndpointOptimizer(ABC):
    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    @abstractmethod
    def optimize(self):
        pass
