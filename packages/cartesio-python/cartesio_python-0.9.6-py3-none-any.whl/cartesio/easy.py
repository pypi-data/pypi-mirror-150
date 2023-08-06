from cartesio.applications.CGPIP import ModelImageProcessing
from cartesio.applications.CGPW import ModelWatershed
from cartesio.callback import CallbackSave, CallbackVerbose
from cartesio.core.genome import GenomeShape
from cartesio.dataset import DatasetReader
from cartesio.enums import CSV_DATASET
from cartesio.inference import SingleModel
from cartesio.utils.saving import JsonLoader


def read_dataset(
    dataset_path,
    filename=CSV_DATASET,
    indices=None,
    counting=False,
    preview=False,
    reader=None,
):
    dataset_reader = DatasetReader(dataset_path, counting=counting, preview=preview)
    if reader is not None:
        dataset_reader.add_reader(reader)
    return dataset_reader.read_dataset(dataset_filename=filename, indices=indices)


def load_model(filepath):
    dataset, elite, decoder = JsonLoader().read_individual(filepath)
    return SingleModel(elite, decoder)


def create_model(
    model_type,
    generations,
    _lambda,
    inputs: int = 3,
    nodes: int = 10,
    outputs: int = 1,
    connections: int = 2,
    parameters: int = 2,
    verbose=True,
    save_dir=None,
    frequency=1,
    endpoint=None,
    fitness="iou",
):
    callbacks = []
    if verbose:
        callbacks.append(CallbackVerbose(frequency=frequency))
    if save_dir:
        callbacks.append(CallbackSave(frequency=frequency))
    shape = GenomeShape(
        inputs=inputs,
        nodes=nodes,
        outputs=outputs,
        connections=connections,
        parameters=parameters,
    )
    if model_type == "IP":
        model = ModelImageProcessing(
            generations,
            _lambda,
            shape=shape,
            fitness=fitness,
            endpoint=endpoint,
            callbacks=callbacks,
        )
    elif model_type == "W":
        model = ModelWatershed(
            generations,
            _lambda,
            shape=shape,
            fitness=fitness,
            endpoint=endpoint,
            callbacks=callbacks,
        )
    return model
