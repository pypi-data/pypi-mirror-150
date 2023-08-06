from cartesio.core.decoder import Decoder
from cartesio.core.genome import GenomeFactory, GenomeShape
from cartesio.core.model import ModelCGP
from cartesio.endpoint import EndpointClassification
from cartesio.fitness import FitnessCrossEntropy
from cartesio.image.bundle import BUNDLE_OPENCV
from cartesio.mutation import GoldmanWrapper, MutationAllRandom, MutationClassic
from cartesio.strategy import OnePlusLambda


# Cartesian Genetic Programming for Classification
class ModelClassifier(ModelCGP):
    def __init__(
        self,
        generations,
        _lambda,
        labels,
        mutation_rate=0.15,
        output_mutation_rate=0.2,
        fitness="cross_entropy",
        bundle=BUNDLE_OPENCV,
        shape=GenomeShape(),
        goldman=True,
        callbacks=[],
        threshold=128,
        reduce_method="count"
    ):
        genome_factory = GenomeFactory(shape.prototype)
        endpoint = EndpointClassification(labels, threshold, reduce_method=reduce_method)
        decoder = Decoder(shape, bundle, endpoint)
        n_functions = decoder.function_set.size
        init_method = MutationAllRandom(shape, n_functions)
        mutation_method = MutationClassic(
            shape, n_functions, mutation_rate, output_mutation_rate
        )
        if goldman:
            mutation_method = GoldmanWrapper(mutation_method, decoder)
        if fitness == "cross_entropy":
            fitness = FitnessCrossEntropy()
        strategy = OnePlusLambda(
            _lambda, genome_factory, init_method, mutation_method, fitness
        )
        super().__init__(generations, strategy, decoder, callbacks=callbacks)
