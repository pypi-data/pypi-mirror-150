from cartesio.core.decoder import Decoder
from cartesio.core.genome import GenomeFactory, GenomeShape
from cartesio.core.model import ModelCGP
from cartesio.endpoint import EndpointCounting
from cartesio.fitness import FitnessCountIOU, FitnessCountPrecision
from cartesio.image.bundle import BUNDLE_OPENCV
from cartesio.mutation import GoldmanWrapper, MutationAllRandom, MutationClassic
from cartesio.strategy import OnePlusLambda


# Cartesian Genetic Programming for Counting
class ModelCounter(ModelCGP):
    def __init__(
        self,
        generations,
        _lambda,
        mutation_rate=0.15,
        output_mutation_rate=0.2,
        fitness="iou",
        bundle=BUNDLE_OPENCV,
        shape=GenomeShape(),
        area_range=None,
        threshold=1,
        goldman=True,
        callbacks=[],
    ):
        genome_factory = GenomeFactory(shape.prototype)
        endpoint = EndpointCounting(area_range=area_range, threshold=threshold)
        decoder = Decoder(shape, bundle, endpoint)
        n_functions = decoder.function_set.size
        init_method = MutationAllRandom(shape, n_functions)
        mutation_method = MutationClassic(
            shape, n_functions, mutation_rate, output_mutation_rate
        )
        if goldman:
            mutation_method = GoldmanWrapper(mutation_method, decoder)
        if fitness == "iou":
            fitness = FitnessCountIOU()
        elif fitness == "precision":
            fitness = FitnessCountPrecision()
        strategy = OnePlusLambda(
            _lambda, genome_factory, init_method, mutation_method, fitness
        )
        super().__init__(generations, strategy, decoder, callbacks=callbacks)
