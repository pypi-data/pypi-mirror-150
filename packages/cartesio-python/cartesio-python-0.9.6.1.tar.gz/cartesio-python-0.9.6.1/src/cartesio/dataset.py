import ast
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import cv2
import numpy as np
import pandas as pd
from micromind.cv.conversion import bgr2hsv, gray2rgb
from micromind.cv.image import (
    fill_ellipses_as_labels,
    fill_polygons_as_labels,
    imnew,
    overlay,
    split_channels,
)
from micromind.imagej import read_ellipses_from_csv, read_polygons_from_roi
from micromind.io.drive import Directory
from micromind.io.image import imread_color, imread_grayscale, imread_tiff

from cartesio.enums import CSV_DATASET, DIR_PREVIEW, JSON_META
from cartesio.utils.json_utils import read, write


class TrainingDataset:
    def __init__(self, training, testing, name, label_name, inputs, indices=None):
        self.training = training
        self.testing = testing
        self.name = name
        self.label_name = label_name
        self.inputs = inputs
        self.indices = indices

    @property
    def train_x(self):
        return self.training.x

    @property
    def train_y(self):
        return self.training.y

    @property
    def test_x(self):
        return self.testing.x

    @property
    def test_y(self):
        return self.testing.y


class DatasetMeta:
    @staticmethod
    def write(
        filepath,
        name,
        input_type,
        input_format,
        label_type,
        label_format,
        label_name,
        scale=1.0,
        mode="dataframe",
    ):
        json_data = {
            "name": name,
            "scale": scale,
            "label_name": label_name,
            "mode": mode,
            "input": {"type": input_type, "format": input_format},
            "label": {"type": label_type, "format": label_format},
        }
        write(filepath + "/" + JSON_META, json_data)

    @staticmethod
    def read(filepath):
        return read(filepath / JSON_META)


@dataclass
class DataReader:
    datatype: str
    dataformat: str
    scale: float = 1.0
    directory: Directory = field(init=False, default=None)

    def read(self, filename, shape=None):
        filepath = str(self.directory / filename)
        return self._read(filepath, shape)

    def set_directory(self, directory):
        self.directory = directory

    @abstractmethod
    def _read(self, filepath, shape=None):
        pass


@dataclass
class DataItem:
    datalist: List
    shape: Tuple
    count: int
    visual: np.ndarray = None

    @property
    def size(self):
        return len(self.datalist)


class ImageMaskReader(DataReader):
    def __init__(self):
        super().__init__("image", "mask")

    def _read(self, filepath, shape=None):
        image = imread_grayscale(filepath)
        _, labels = cv2.connectedComponents(image)
        return DataItem([labels], image.shape[:2], len(np.unique(labels)) - 1, image)


class ImageHSVReader(DataReader):
    def __init__(self):
        super().__init__("image", "hsv")

    def _read(self, filepath, shape=None):
        image_bgr = imread_color(filepath)
        image_hsv = bgr2hsv(image_bgr)
        return DataItem(split_channels(image_hsv), image_bgr.shape[:2], None, image_bgr)


class ImageLabels(DataReader):
    def __init__(self):
        super().__init__("image", "labels")

    def _read(self, filepath, shape=None):
        image = cv2.imread(filepath, cv2.IMREAD_ANYDEPTH)
        return DataItem([image], image.shape[:2], image.max(), visual=image)


class ImageRGBReader(DataReader):
    def __init__(self):
        super().__init__("image", "rgb")

    def _read(self, filepath, shape=None):
        image = imread_color(filepath)
        return DataItem(split_channels(image), image.shape[:2], None, visual=image)


class CsvEllipseReader(DataReader):
    def __init__(self):
        super().__init__("csv", "ellipse")

    def _read(self, filepath, shape=None):
        dataframe = pd.read_csv(filepath)
        ellipses = read_ellipses_from_csv(
            dataframe, scale=self.scale, ellipse_scale=1.0
        )
        label_mask = imnew(shape)
        fill_ellipses_as_labels(label_mask, ellipses)
        return DataItem([label_mask], shape, len(ellipses))


class ImageGrayscaleReader(DataReader):
    def __init__(self):
        super().__init__("image", "grayscale")

    def _read(self, filepath, shape=None):
        image = imread_grayscale(filepath)
        return DataItem([image], image.shape, None, visual=image)


class RoiPolygonReader(DataReader):
    def __init__(self):
        super().__init__("roi", "polygon")

    def _read(self, filepath, shape=None):
        polygons = read_polygons_from_roi(filepath)
        label_mask = imnew(shape)
        fill_polygons_as_labels(label_mask, polygons)
        return DataItem([label_mask], shape, len(polygons))


class OneHotVectorReader(DataReader):
    def __init__(self):
        super().__init__("one-hot", "vector")

    def _read(self, filepath, shape=None):
        label = np.array(ast.literal_eval(filepath.split("/")[-1]))
        return DataItem([label], shape, None)


class ImageChannelsReader(DataReader):
    def __init__(self):
        super().__init__("image", "channels")

    def _read(self, filepath, shape=None):
        image = imread_tiff(filepath)
        if image.dtype == np.uint16:
            raise ValueError(f"Image must be 8bits! ({filepath})")
        shape = image.shape[-2:]
        if len(image.shape) == 2:
            channels = [image]
            preview = gray2rgb(channels[0])
        if len(image.shape) == 3:
            channels = [channel for channel in image]
            preview = cv2.merge((imnew(channels[0].shape), channels[0], channels[1]))
        if len(image.shape) == 4:
            channels = [image[:, i] for i in range(len(image[0]))]
            preview = cv2.merge(
                (
                    channels[0].mean(axis=0),
                    channels[2].mean(axis=0),
                    channels[2].mean(axis=0),
                )
            )
        return DataItem(channels, shape, None, visual=preview)


@dataclass
class DatasetReader(Directory):
    counting: bool = False
    preview: bool = False
    preview_dir: Directory = field(init=False)
    readers: Dict = field(init=False)

    def __post_init__(self, path):
        super().__post_init__(path)
        self.readers = {}
        self.add_reader(ImageRGBReader())
        self.add_reader(ImageHSVReader())
        self.add_reader(ImageMaskReader())
        self.add_reader(ImageGrayscaleReader())
        self.add_reader(ImageChannelsReader())
        self.add_reader(ImageLabels())
        self.add_reader(RoiPolygonReader())
        self.add_reader(CsvEllipseReader())
        self.add_reader(OneHotVectorReader())
        if self.preview:
            self.preview_dir = self.next(DIR_PREVIEW)

    def add_reader(self, reader):
        reader_key = (reader.datatype, reader.dataformat)
        reader.set_directory(self)
        self.readers[reader_key] = reader

    def get_reader(self, datatype, dataformat):
        reader_key = (datatype, dataformat)
        if reader_key not in self.readers:
            raise AttributeError(
                f"{reader_key} is not handled yet, please consider to add your own Reader."
            )
        return self.readers[reader_key]

    def _read_meta(self):
        meta = DatasetMeta.read(self._path)
        self.name = meta["name"]
        self.scale = meta["scale"]
        self.mode = meta["mode"]
        self.label_name = meta["label_name"]
        self.input_reader = self.get_reader(
            meta["input"]["type"], meta["input"]["format"]
        )
        self.input_reader.scale = self.scale
        self.label_reader = self.get_reader(
            meta["label"]["type"], meta["label"]["format"]
        )
        self.label_reader.scale = self.scale

    def read_dataset(self, dataset_filename=CSV_DATASET, indices=None):
        self._read_meta()
        if self.mode == "dataframe":
            return self._read_from_dataframe(dataset_filename, indices)
        if self.mode == "auto":
            return self._read_auto()
        raise AttributeError(f"{self.mode} is not handled yet")

    def _read_from_dataframe(self, dataset_filename, indices):
        dataframe = self.read(dataset_filename)
        dataframe_training = dataframe[dataframe["set"] == "training"]
        training = self._read_dataset(dataframe_training, indices)
        dataframe_testing = dataframe[dataframe["set"] == "testing"]
        testing = self._read_dataset(dataframe_testing)
        input_sizes = []
        [input_sizes.append(len(xi)) for xi in training.x]
        [input_sizes.append(len(xi)) for xi in testing.x]
        input_sizes = np.array(input_sizes)
        inputs = int(input_sizes[0])
        if not np.all((input_sizes == inputs)):
            raise ValueError(
                f"Inconsistent size of inputs for this dataset: sizes: {input_sizes}"
            )

        if self.preview:
            for i in range(len(training.x)):
                visual = training.visuals[i]
                label = training.y[i][0]
                preview = overlay(visual, label, color=[255])
                self.preview_dir.write(f"training_{i}.png", preview)
            for i in range(len(testing.x)):
                visual = testing.visuals[i]
                label = testing.y[i][0]
                preview = overlay(visual, label, color=[255])
                self.preview_dir.write(f"testing_{i}.png", preview)
        return TrainingDataset(
            training, testing, self.name, self.label_name, inputs, indices
        )

    def _read_auto(self, dataset):
        pass

    def _read_dataset(self, dataframe, indices=None):
        dataset = Dataset(dataframe)
        dataframe.reset_index(inplace=True)
        if indices:
            dataframe = dataframe.loc[indices]
        for row in dataframe.itertuples():
            x = self.input_reader.read(row.input, shape=None)
            y = self.label_reader.read(row.label, shape=x.shape)
            if self.counting:
                y = [y.datalist[0], y.count]
            else:
                y = y.datalist
            dataset.n_inputs = x.size
            dataset.add_item(x.datalist, y)
            visual_from_table = False
            if "visual" in dataframe.columns:
                if str(row.visual) != "nan":
                    dataset.add_visual(self.read(row.visual))
                    visual_from_table = True
            if not visual_from_table:
                dataset.add_visual(x.visual)
        return dataset


class Dataset:
    def __init__(self, dataframe):
        self.x = []
        self.y = []
        self.visuals = []
        self.dataframe = dataframe

    def add_item(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def add_visual(self, visual):
        self.visuals.append(visual)
