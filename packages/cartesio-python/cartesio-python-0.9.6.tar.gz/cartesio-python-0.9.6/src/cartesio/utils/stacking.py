from typing import Dict, List

from cartesio.utils.json_utils import read


class JsonStacker(object):
    pass


class IndividualStacker(JsonStacker):
    """Stack many indivduals into a single Population JSON object

    Args:
        JsonStacker ([type]): [description]
    """

    def stack(self, individuals: List) -> Dict:
        population = []
        decoder = None
        dataset = None
        for individual_path in individuals:
            json_data = read(individual_path)
            individual_json = {
                "sequence": json_data["sequence"],
                "fitness": json_data["fitness"],
            }
            population.append(individual_json)

            if decoder is None and dataset is None:
                decoder = json_data["decoding"]
                dataset = json_data["dataset"]

        return {"dataset": dataset, "population": population, "decoding": decoder}


class GenerationStacker(JsonStacker):
    def __init__(self, old_version=False):
        self.old_version = old_version

    def stack(self, generations):
        generation_dict = {}
        decoder = None
        dataset = None

        if self.old_version:
            for generation_path in generations:
                json_data = read(generation_path)
                n = int(
                    generation_path.split("/")[-1].replace("G", "").replace(".json", "")
                )
                population = []
                for individual in json_data["population"]:
                    individual_json = {
                        "sequence": individual["sequence"],
                        "fitness": individual["fitness"],
                    }
                    population.append(individual_json)
                    if decoder is None and dataset is None:
                        decoder = individual["decoding"]
                        dataset = individual["dataset"]
                generation_json = {"population": population}
                generation_dict[n] = generation_json
        else:
            for generation_path in generations:
                json_data = read(generation_path)
                n = int(
                    generation_path.split("/")[-1].replace("G", "").replace(".json", "")
                )
                generation_json = {"population": json_data["population"]}
                generation_dict[n] = generation_json

                if decoder is None and dataset is None:
                    decoder = json_data["decoding"]
                    dataset = json_data["dataset"]

        return {"dataset": dataset, "generations": generation_dict, "decoding": decoder}
