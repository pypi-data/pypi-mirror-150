from abc import ABC, abstractmethod
from typing import List

import cv2
import numpy as np
from micromind.cv.image import BINARY_DEFAULT_VALUE, imfill
from scipy.stats import kurtosis, skew
from skimage.morphology import remove_small_holes, remove_small_objects, thin

from cartesio.core.node import Node, WritableNode
from cartesio.image.kernel import (
    ROBERT_CROSS_H_KERNEL,
    ROBERT_CROSS_V_KERNEL,
    SHARPEN_KERNEL,
    correct_ksize,
    gabor_kernel,
    kernel_from_parameters,
)


class ImageProcessingNode2D(Node, ABC):
    @abstractmethod
    def __call__(self, inputs: List, p: List):
        pass


class Add(WritableNode):
    def __init__(self):
        super().__init__("add", 2, 0)

    def __call__(self, inputs, p):
        return cv2.add(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.add({input_names[0]}, {input_names[1]})"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::add({input_names[0]}, {input_names[1]}, {output_name});"


class Subtract(WritableNode):
    def __init__(self):
        super().__init__("subtract", 2, 0)

    def __call__(self, inputs, p):
        return cv2.subtract(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.subtract({input_names[0]}, {input_names[1]})"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::subtract({input_names[0]}, {input_names[1]}, {output_name});"


class BitwiseNot(WritableNode):
    def __init__(self):
        super().__init__("bitwise_not", 1, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_not(inputs[0])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.bitwise_not({input_names[0]})"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::bitwise_not({input_names[0]}, {output_name});"


class BitwiseOr(WritableNode):
    def __init__(self):
        super().__init__("bitwise_or", 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_or(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.bitwise_or({input_names[0]}, {input_names[1]})"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::bitwise_or({input_names[0]}, {input_names[1]}, {output_name});"


class BitwiseAnd(WritableNode):
    def __init__(self):
        super().__init__("bitwise_and", 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_and(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.bitwise_and({input_names[0]}, {input_names[1]})"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::bitwise_and({input_names[0]}, {input_names[1]}, {output_name});"


class BitwiseAndMask(WritableNode):
    def __init__(self):
        super().__init__("bitwise_and_mask", 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_and(inputs[0], inputs[0], mask=inputs[1])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.bitwise_and({input_names[0]}, {input_names[0]}, mask={input_names[1]})"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::bitwise_and({input_names[0]}, {input_names[0]}, {output_name}, {input_names[1]});"


class BitwiseXor(WritableNode):
    def __init__(self):
        super().__init__("bitwise_xor", 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_xor(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.bitwise_xor({input_names[0]}, {input_names[1]})"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::bitwise_xor({input_names[0]}, {input_names[1]}, {output_name});"


class SquareRoot(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("sqrt", 1, 0)

    def __call__(self, inputs, p):
        return (cv2.sqrt((inputs[0] / 255.0).astype(np.float32)) * 255).astype(np.uint8)


class Square(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("pow2", 1, 0)

    def __call__(self, inputs, p):
        return (cv2.pow((inputs[0] / 255.0).astype(np.float32), 2) * 255).astype(
            np.uint8
        )


class Exp(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("exp", 1, 0)

    def __call__(self, inputs, p):
        return (cv2.exp((inputs[0] / 255.0).astype(np.float32), 2) * 255).astype(
            np.uint8
        )


class Log(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("log", 1, 0)

    def __call__(self, inputs, p):
        return np.log1p(inputs[0]).astype(np.uint8)


class MedianBlur(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("median_blur", 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.medianBlur(connections[0], ksize)


class GaussianBlur(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("gaussian_blur", 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.GaussianBlur(connections[0], (ksize, ksize), 0)


class Laplacian(ImageProcessingNode2D):
    def __init__(self):
        super(Laplacian, self).__init__("laplacian", 1, 0)

    def __call__(self, connections, parameters):
        return cv2.Laplacian(connections[0], cv2.CV_64F).astype(np.uint8)


class Sobel(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("sobel", 1, 2)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        if parameters[1] < 128:
            return cv2.Sobel(connections[0], cv2.CV_64F, 1, 0, ksize=ksize).astype(
                np.uint8
            )
        return cv2.Sobel(connections[0], cv2.CV_64F, 0, 1, ksize=ksize).astype(np.uint8)


class RobertCross(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("robert_cross", 1, 1)

    def __call__(self, connections, parameters):
        img = (connections[0] / 255.0).astype(np.float32)
        h = cv2.filter2D(img, -1, ROBERT_CROSS_H_KERNEL)
        v = cv2.filter2D(img, -1, ROBERT_CROSS_V_KERNEL)
        return (cv2.sqrt(cv2.pow(h, 2) + cv2.pow(v, 2)) * 255).astype(np.uint8)


class Canny(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("canny", 1, 2)

    def __call__(self, connections, parameters):
        return cv2.Canny(connections[0], parameters[0], parameters[1])


class Sharpen(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("sharpen", 1, 0)

    def __call__(self, connections, parameters):
        return cv2.filter2D(connections[0], -1, SHARPEN_KERNEL)


class GaborFilter(ImageProcessingNode2D):
    def __init__(self, ksize=11):
        super().__init__("gabor", 1, 2)
        self.ksize = ksize

    def __call__(self, connections, parameters):
        gabor_k = gabor_kernel(self.ksize, parameters[0], parameters[1])
        return cv2.filter2D(connections[0], -1, gabor_k)


class AbsoluteDifference(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("abs_diff", 1, 2)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        image = connections[0].copy()
        return image - cv2.GaussianBlur(image, (ksize, ksize), 0) + parameters[1]


class AbsoluteDifference2(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("abs_diff2", 2, 0)

    def __call__(self, connections, parameters):
        return 255 - cv2.absdiff(connections[0], connections[1])


class FluoTopHat(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("fluo_tophat", 1, 2)

    def _rescale_intensity(self, img, min_val, max_val):
        output_img = np.clip(img, min_val, max_val)
        if max_val - min_val == 0:
            return (output_img * 255).astype(np.uint8)
        output_img = (output_img - min_val) / (max_val - min_val) * 255
        return output_img.astype(np.uint8)

    def __call__(self, connections, p):
        kernel = kernel_from_parameters(p)
        img = cv2.morphologyEx(connections[0], cv2.MORPH_TOPHAT, kernel, iterations=10)
        kur = np.mean(kurtosis(img, fisher=True))
        skew1 = np.mean(skew(img))
        if kur > 1 and skew1 > 1:
            p2, p98 = np.percentile(img, (15, 99.5), interpolation="linear")
        else:
            p2, p98 = np.percentile(img, (15, 100), interpolation="linear")

        return self._rescale_intensity(img, p2, p98)


class RelativeDifference(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("rel_diff", 1, 1)

    def __call__(self, connections, p):
        img = connections[0]
        max_img = np.max(img)
        min_img = np.min(img)

        ksize = correct_ksize(p[0])
        gb = cv2.GaussianBlur(img, (ksize, ksize), 0)
        gb = np.float32(gb)

        img = np.divide(img, gb + 1e-15, dtype=np.float32)
        img = cv2.normalize(img, img, max_img, min_img, cv2.NORM_MINMAX)
        return img.astype(np.uint8)


class Erode(WritableNode):
    def __init__(self):
        super().__init__("erode", 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.erode(inputs[0], kernel)

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.erode({input_names[0]}, kernel_from_parameters({p[0]}))"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::erode({input_names[0]}, {output_name}, kernel_from_parameters({p[0]}));"


class Dilate(WritableNode):
    def __init__(self):
        super().__init__("dilate", 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.dilate(inputs[0], kernel)

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.dilate({input_names[0]}, kernel_from_parameters({p[0]}))"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::dilate({input_names[0]}, {output_name}, kernel_from_parameters({p[0]}));"


class Open(WritableNode):
    def __init__(self):
        super().__init__("open", 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_OPEN, kernel)

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_OPEN, kernel_from_parameters({p[0]}))"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::morphologyEx({input_names[0]}, {output_name}, MORPH_OPEN, kernel_from_parameters({p[0]}));"


class Close(WritableNode):
    def __init__(self):
        super().__init__("close", 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_CLOSE, kernel)

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_CLOSE, kernel_from_parameters({p[0]}))"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::morphologyEx({input_names[0]}, {output_name}, MORPH_CLOSE, kernel_from_parameters({p[0]}));"


class MorphGradient(WritableNode):
    def __init__(self):
        super().__init__("morph_gradient", 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_GRADIENT, kernel)

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_GRADIENT, kernel_from_parameters({p[0]}))"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::morphologyEx({input_names[0]}, {output_name}, MORPH_GRADIENT, kernel_from_parameters({p[0]}));"


class MorphTopHat(WritableNode):
    def __init__(self):
        super().__init__("morph_tophat", 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_TOPHAT, kernel)

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_TOPHAT, kernel_from_parameters({p[0]}))"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::morphologyEx({input_names[0]}, {output_name}, MORPH_TOPHAT, kernel_from_parameters({p[0]}));"


class MorphBlackHat(WritableNode):
    def __init__(self):
        super().__init__("morph_blackhat", 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_BLACKHAT, kernel)

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_BLACKHAT, kernel_from_parameters({p[0]}))"

    def to_cpp(self, input_names, p, output_name):
        return f"cv::morphologyEx({input_names[0]}, {output_name}, MORPH_BLACKHAT, kernel_from_parameters({p[0]}));"


class FillHoles(WritableNode):
    def __init__(self):
        super().__init__("fill_holes", 1, 0)

    def __call__(self, inputs, p):
        return imfill(inputs[0])

    def to_python(self, input_names, p, output_name):
        return f"{output_name} = imfill({input_names[0]})"

    def to_cpp(self, input_names, p, output_name):
        return f"imfill({input_names[0]}, {output_name});"


class RemoveSmallObjects(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("remove_small_objects", 1, 1)

    def __call__(self, inputs, p):
        return remove_small_objects(inputs[0] > 0, p[0]).astype(np.uint8)


class RemoveSmallHoles(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("remove_small_holes", 1, 1)

    def __call__(self, inputs, p):
        return remove_small_holes(inputs[0] > 0, p[0]).astype(np.uint8)


class Thin(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("thin", 1, 0)

    def __call__(self, inputs, p):
        return thin(inputs[0]).astype(np.uint8)


class Threshold(ImageProcessingNode2D):
    def __init__(self):
        super(Threshold, self).__init__("threshold", 1, 2)

    def __call__(self, connections, parameters):
        if parameters[0] < 128:
            return cv2.threshold(
                connections[0], parameters[1], BINARY_DEFAULT_VALUE, cv2.THRESH_BINARY
            )[1]
        return cv2.threshold(
            connections[0], parameters[1], BINARY_DEFAULT_VALUE, cv2.THRESH_TOZERO
        )[1]


class ThresholdAt1(ImageProcessingNode2D):
    def __init__(self):
        super(ThresholdAt1, self).__init__("threshold_at_1", 1, 1)

    def __call__(self, connections, parameters):
        if parameters[0] < 128:
            return cv2.threshold(
                connections[0], 1, BINARY_DEFAULT_VALUE, cv2.THRESH_BINARY
            )[1]
        return cv2.threshold(
            connections[0], 1, BINARY_DEFAULT_VALUE, cv2.THRESH_TOZERO
        )[1]


class ThresholdAdaptive(ImageProcessingNode2D):
    def __init__(self):
        super().__init__("adaptive_threshold", 1, 2)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        C = parameters[1] - 128  # to allow negative values
        return cv2.adaptiveThreshold(
            connections[0],
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            ksize,
            C,
        )


class DistanceTransform(ImageProcessingNode2D):
    def __init__(self):
        super(DistanceTransform, self).__init__("distance_transform", 1, 1)

    def __call__(self, connections, parameters):
        return cv2.normalize(
            cv2.distanceTransform(connections[0].copy(), cv2.DIST_L2, 3),
            None,
            0,
            255,
            cv2.NORM_MINMAX,
            cv2.CV_8U,
        )


class DistanceTransformAndThresh(ImageProcessingNode2D):
    def __init__(self):
        super(DistanceTransformAndThresh, self).__init__(
            "distance_transform_and_thresh", 1, 2
        )

    def __call__(self, connections, parameters):
        d = cv2.normalize(
            cv2.distanceTransform(connections[0].copy(), cv2.DIST_L2, 3),
            None,
            0,
            255,
            cv2.NORM_MINMAX,
            cv2.CV_8U,
        )
        return cv2.threshold(d, parameters[0], BINARY_DEFAULT_VALUE, cv2.THRESH_BINARY)[
            1
        ]


class BinaryInRange(ImageProcessingNode2D):
    def __init__(self):
        super(BinaryInRange, self).__init__("inrange_bin", 1, 2)

    def __call__(self, connections, parameters):
        lower = int(min(parameters[0], parameters[1]))
        upper = int(max(parameters[0], parameters[1]))
        return cv2.inRange(connections[0], lower, upper)


class InRange(ImageProcessingNode2D):
    def __init__(self):
        super(InRange, self).__init__("inrange", 1, 2)

    def __call__(self, connections, parameters):
        lower = int(min(parameters[0], parameters[1]))
        upper = int(max(parameters[0], parameters[1]))
        return cv2.bitwise_and(
            connections[0],
            connections[0],
            mask=cv2.inRange(connections[0], lower, upper),
        )
