from abc import ABC

from cartesio.core.bundle import Bundle
from cartesio.image.catalog import Catalog2D


class BundleImage2D(Bundle, ABC):
    def __init__(self):
        super().__init__(Catalog2D)


class BundleFilters(BundleImage2D):
    def fill(self):
        self.add_node("median_blur")
        self.add_node("gaussian_blur")
        self.add_node("laplacian")
        self.add_node("sobel")
        self.add_node("robert_cross")
        self.add_node("canny")
        self.add_node("sharpen")
        self.add_node("abs_diff")
        self.add_node("abs_diff2")
        self.add_node("rel_diff")
        self.add_node("fluo_tophat")
        self.add_node("gabor")


class BundleMorphology(BundleImage2D):
    def fill(self):
        self.add_node("erode")
        self.add_node("dilate")
        self.add_node("open")
        self.add_node("close")
        self.add_node("morph_gradient")
        self.add_node("morph_tophat")
        self.add_node("morph_blackhat")
        self.add_node("fill_holes")
        self.add_node("remove_small_objects")
        self.add_node("remove_small_holes")
        # self.add_function('thin')


class BundleMisc(BundleImage2D):
    def fill(self):
        self.add_node("distance_transform")
        self.add_node("distance_transform_and_thresh")
        self.add_node("threshold")
        self.add_node("threshold_at_1")
        self.add_node("inrange_bin")
        self.add_node("inrange")


class BundleArithmetic(BundleImage2D):
    def fill(self):
        self.add_node("bitwise_and")
        self.add_node("bitwise_and_mask")
        self.add_node("bitwise_not")
        self.add_node("bitwise_or")
        self.add_node("bitwise_xor")
        self.add_node("add")
        self.add_node("subtract")
        self.add_node("sqrt")
        self.add_node("pow2")
        self.add_node("exp")
        self.add_node("log")


class BundleOpenCV(BundleImage2D):
    def fill(self):
        self.add_bundle(BUNDLE_FILTERS)
        self.add_bundle(BUNDLE_MORPHOLOGY)
        self.add_bundle(BUNDLE_ARITHMETIC)
        self.add_bundle(BUNDLE_MISC)


BUNDLE_FILTERS = BundleFilters()
BUNDLE_MORPHOLOGY = BundleMorphology()
BUNDLE_ARITHMETIC = BundleArithmetic()
BUNDLE_MISC = BundleMisc()
BUNDLE_OPENCV = BundleOpenCV()
