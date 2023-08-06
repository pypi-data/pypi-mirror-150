from abc import ABC, abstractmethod

import numpy as np


class Metric(ABC):
    @abstractmethod
    def compute(self, y_true, y_pred):
        pass


class Fitness(ABC):
    def evaluate(self, y_true, y_pred):
        return [
            self._evaluate_one(y_true, individual_pred) for individual_pred in y_pred
        ]

    def _evaluate_one(self, y_true, y_pred):
        fitness = []
        for i in range(len(y_true)):
            fitness.append(self._fitness(y_true[i][0].copy(), y_pred[i]["mask"].copy()))
        return np.mean(np.array(fitness))

    @abstractmethod
    def _fitness(self, y_true, y_pred):
        pass


class EvolutionStrategy(ABC):
    @abstractmethod
    def selection(self):
        pass

    @abstractmethod
    def reproduction(self):
        pass
