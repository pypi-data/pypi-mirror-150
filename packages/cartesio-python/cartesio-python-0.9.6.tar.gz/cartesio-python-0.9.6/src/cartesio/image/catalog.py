from cartesio.core.bundle import Catalog
from cartesio.core.helper import catalog_decorator
from cartesio.image.nodes import *


@catalog_decorator
class Catalog2D(Catalog):
    @classmethod
    def fill(cls):
        cls.include(Erode())
        cls.include(Dilate())
        cls.include(Open())
        cls.include(Close())
        cls.include(MorphGradient())
        cls.include(MorphTopHat())
        cls.include(MorphBlackHat())
        cls.include(FillHoles())
        cls.include(RemoveSmallHoles())
        cls.include(RemoveSmallObjects())
        cls.include(Thin())
        cls.include(MedianBlur())
        cls.include(GaussianBlur())
        cls.include(Laplacian())
        cls.include(Sobel())
        cls.include(RobertCross())
        cls.include(Canny())
        cls.include(Sharpen())
        cls.include(AbsoluteDifference())
        cls.include(AbsoluteDifference2())
        cls.include(RelativeDifference())
        cls.include(FluoTopHat())
        cls.include(GaborFilter())
        cls.include(DistanceTransform())
        cls.include(DistanceTransformAndThresh())
        cls.include(Threshold())
        cls.include(ThresholdAt1())
        cls.include(BinaryInRange())
        cls.include(InRange())
        cls.include(BitwiseAnd())
        cls.include(BitwiseAndMask())
        cls.include(BitwiseNot())
        cls.include(BitwiseOr())
        cls.include(BitwiseXor())
        cls.include(Add())
        cls.include(Subtract())
        cls.include(SquareRoot())
        cls.include(Square())
        cls.include(Exp())
        cls.include(Log())
