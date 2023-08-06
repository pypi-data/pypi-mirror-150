import numpy as np
from skimage import data

from cartesio.core.decoder import Decoder
from cartesio.core.genome import GenomeShape
from cartesio.image.bundle import BUNDLE_OPENCV

cells = data.cell()
cells_half = cells / 2

coffee = data.coffee()

x1 = [cells, cells_half, cells]
x2 = [coffee[i] for i in range(len(coffee))]
X = [x1, x2]
FSET = BUNDLE_OPENCV
SHAPE = GenomeShape(3, 10, 1, BUNDLE_OPENCV.max_arity, BUNDLE_OPENCV.max_parameters)


class TestDecoding:
    def test_decoding_empty(self):
        decoder = Decoder(SHAPE, FSET)
        genome = SHAPE.prototype.clone()  # empty genome, all 0
        Y, ctime = decoder.decode_genome(genome, X)
        y1 = Y[0]
        y2 = Y[1]
        assert np.array_equal(x1[0], y1[0])
        assert np.array_equal(x2[0], y2[0])
        assert not np.array_equal(x1[1], y1[0])
        assert not np.array_equal(x2[1], y2[0])
        assert not np.array_equal(x2[2], y2[0])

    def test_decoding(self):
        decoder = Decoder(SHAPE, FSET)
        genome = SHAPE.prototype.clone()  # empty genome, all 0
        # handmade changes to create graph
        genome.sequence[-1, 1] = 1  # output now gets second input
        Y, ctime = decoder.decode_genome(genome, X)
        y1 = Y[0]
        y2 = Y[1]
        assert not np.array_equal(x1[0], y1[0])
        assert not np.array_equal(x2[0], y2[0])
        assert np.array_equal(x1[1], y1[0])
        assert np.array_equal(x2[1], y2[0])
