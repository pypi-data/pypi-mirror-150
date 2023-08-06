from abc import ABC, abstractmethod

import numpy as np

from cartesio.enums import JSON_ELITE
from cartesio.utils.saving import JsonLoader


class InferenceModel(ABC):
    @abstractmethod
    def predict(self, x):
        pass


class CodeModel(InferenceModel, ABC):
    def __init__(self, catalog, endpoint=None):
        self.catalog = catalog
        self.endpoint = endpoint

    @abstractmethod
    def _decode(self, xi):
        pass

    def _endpoint(self, x):
        if self.endpoint is None:
            return x
        return self.endpoint.execute(x)

    def predict(self, x):
        return [self._endpoint(self._decode(xi)) for xi in x]


class SingleModel(InferenceModel):
    def __init__(self, genome, decoder):
        self.genome = genome
        self.decoder = decoder

    def predict(self, x):
        return self.decoder.decode_genome(self.genome, x)


class EnsembleModel(InferenceModel):
    def __init__(self, models):
        self.models = models

    def predict(self, x):
        return [model.predict(x) for model in self.models]


class ModelPool:
    def __init__(self, directory):
        self.models = []
        self.directory = directory
        self.read()

    def read(self):
        json_loader = JsonLoader()
        for elite in self.directory.ls(f"*/{JSON_ELITE}"):
            _, elite, decoder = json_loader.read_individual(elite)
            self.models.append(SingleModel(elite, decoder))

    def sample_ensemble_model(self, n):
        indices = np.random.randint(0, len(self.models), n)
        models = [self.models[i] for i in indices]
        return EnsembleModel(models)
