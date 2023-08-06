import cartesio.utils.json_utils as json


def load(filename):
    json_data = json.read(filename)
    genome = json.to_genome(json_data["sequence"])
    decoder = json.to_decoder(json_data["decoding"])
    return genome, decoder


class JsonLoader(object):
    def read_individual(self, filepath):
        json_data = json.read(filepath)
        dataset = json_data["dataset"]
        decoder = json.to_decoder(json_data["decoding"])
        try:
            individual = json.to_genome(json_data["individual"])
        except KeyError:
            try:
                individual = json.to_genome(json_data)
            except KeyError:
                individual = json.to_genome(json_data["population"][0])
        return dataset, individual, decoder


class JsonSaver(object):
    def __init__(self, dataset, decoder):
        self.dataset_json = json.from_dataset(dataset)
        self.decoder_json = decoder.to_json()

    def save_population(self, filepath, population):
        json_data = {
            "dataset": self.dataset_json,
            "population": json.from_population(population),
            "decoding": self.decoder_json,
        }
        json.write(filepath, json_data)

    def save_individual(self, filepath, individual):
        json_data = {
            "dataset": self.dataset_json,
            "individual": json.from_individual(individual),
            "decoding": self.decoder_json,
        }
        json.write(filepath, json_data)
