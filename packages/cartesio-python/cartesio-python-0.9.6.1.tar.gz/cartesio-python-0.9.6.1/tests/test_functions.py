import numpy as np
from skimage import data

from cartesio.core.node import WritableNode
from cartesio.image.bundle import (
    BUNDLE_ARITHMETIC,
    BUNDLE_FILTERS,
    BUNDLE_MISC,
    BUNDLE_MORPHOLOGY,
)

IMAGE = data.cell()
INPUTS = [IMAGE, IMAGE]


class TestOpenCVFunctions:
    def __test_function_set(self, function_set):
        for f in function_set.nodes():
            p = np.random.randint(256, size=2)
            out = f(INPUTS, p).copy()

            #  shape retention
            assert out.shape == IMAGE.shape

            #  type retention
            assert out.dtype == np.uint8
            assert out.dtype == IMAGE.dtype

            #  idempotence
            assert np.array_equal(out, f(INPUTS, p))

            #  output range
            assert np.all(out >= 0)
            assert np.all(out <= 255)

            if isinstance(f, WritableNode):
                f.to_cpp(["node_0", "node_1"], [128, 42], "node_2")
                f.to_python(["node_0", "node_1"], [128, 42], "node_2")

    def test_filters_functions(self):
        self.__test_function_set(BUNDLE_FILTERS)

    def test_morphology_functions(self):
        self.__test_function_set(BUNDLE_MORPHOLOGY)

    def test_misc_functions(self):
        self.__test_function_set(BUNDLE_MISC)

    def test_arithmetic_functions(self):
        self.__test_function_set(BUNDLE_ARITHMETIC)
