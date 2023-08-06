from cartesio.core.decoder import Decoder
from cartesio.core.genome import GenomeFactory, GenomeShape
from cartesio.core.model import ModelCGP
from cartesio.endpoint import EndpointWatershed
from cartesio.fitness import FitnessAP05, FitnessWatershed
from cartesio.image.bundle import BUNDLE_OPENCV
from cartesio.mutation import GoldmanWrapper, MutationAllRandom, MutationClassic
from cartesio.strategy import OnePlusLambda


# Cartesian Genetic Programming Watershed based
class ModelWatershed(ModelCGP):
    def __init__(
        self,
        generations,
        _lambda,
        mutation_rate=0.15,
        output_mutation_rate=0.2,
        fitness="iou",
        bundle=BUNDLE_OPENCV,
        shape=GenomeShape(),
        endpoint=EndpointWatershed(),
        goldman=True,
        callbacks=[],
    ):
        genome_factory = GenomeFactory(shape.prototype)
        decoder = Decoder(shape, bundle, endpoint)
        n_functions = decoder.function_set.size
        init_method = MutationAllRandom(shape, n_functions)
        mutation_method = MutationClassic(
            shape, n_functions, mutation_rate, output_mutation_rate
        )
        if goldman:
            mutation_method = GoldmanWrapper(mutation_method, decoder)
        if fitness == "watershed":
            fitness = FitnessWatershed()
        elif fitness == "ap50":
            fitness = FitnessAP05()
        strategy = OnePlusLambda(
            _lambda, genome_factory, init_method, mutation_method, fitness
        )
        super().__init__(generations, strategy, decoder, callbacks=callbacks)
