from typing import List

import cv2
import numpy as np
from micromind.cv.image import BINARY_DEFAULT_VALUE, contours, fill_contours, imnew, imfill
from micromind.cv.morphology.watershed import WatershedSkimage

from cartesio.core.endpoint import Endpoint


class EndpointEllipse(Endpoint):
    def __init__(self, min_axis, max_axis):
        super().__init__("fit_ellipse", 1)
        self.min_axis = min_axis
        self.max_axis = max_axis

    def execute(self, entries):
        mask = entries[0]
        n = 0
        new_mask = imnew(mask.shape)
        new_seeds = imnew(mask.shape)
        labels = []

        cnts = contours(entries[0], exclude_holes=True)
        for cnt in cnts:
            if len(cnt) >= 5:
                (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)
                if (
                    self.min_axis <= MA <= self.max_axis
                    and self.min_axis <= ma <= self.max_axis
                ):
                    cv2.ellipse(
                        new_mask,
                        ((x, y), (MA, ma), angle),
                        BINARY_DEFAULT_VALUE,
                        thickness=-1,
                    )
                    cv2.ellipse(
                        new_seeds,
                        ((x, y), (3, 3), angle),
                        BINARY_DEFAULT_VALUE,
                        thickness=-1,
                    )
                    labels.append(((x, y), (MA, ma), angle))
                    n += 1

        return new_mask, new_seeds, n, labels


class EndpointThreshold(Endpoint):
    def __init__(self, threshold=1):
        super().__init__("threshold", 1)
        self.threshold = threshold

    def execute(self, entries):
        mask = entries[0].copy()
        mask[mask < self.threshold] = 0
        return {"mask": mask}


class EndpointClassification(Endpoint):
    def __init__(self, labels, threshold, reduce_method="count"):
        super().__init__(f"softmax-{reduce_method}", len(labels))
        self.labels = labels
        self.threshold = threshold
        self.reduce_method = reduce_method

    def __reduce_mean(self, x):
        return np.mean(x, where=x > 0)

    def __reduce_count(self, x):
        return np.log(np.count_nonzero(x) + 0.0001)

    def __reduce_sum(self, x):
        return np.log(np.sum(x / 255., where=x > 0) + 0.0001)

    def __softmax(self, x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def reduce_one_entry(self, x):
        x[x < self.threshold] = 0
        if self.reduce_method == "count":
            return x, self.__reduce_count(x)
        elif self.reduce_method == "mean":
            return x, self.__reduce_mean(x)
        elif self.reduce_method == "sum":
            return x, self.__reduce_sum(x)

    def execute(self, entries: List):
        output = {}
        reduced_array = np.zeros(len(entries))
        for i in range(len(entries)):
            y, reduced_array[i] = self.reduce_one_entry(entries[i])
            output[self.labels[i]] = y
        output["softmax"] = self.__softmax(reduced_array)
        return output


class EndpointCounting(Endpoint):
    def __init__(self, area_range=None, threshold=1):
        super().__init__("C", 1)
        self.area_range = area_range
        self.threshold = threshold

    def execute(self, entries):
        mask = entries[0].copy()
        mask[mask < self.threshold] = 0
        cnts = contours(mask, exclude_holes=True)
        if not self.area_range:
            return {"mask": mask, "count": len(cnts)}

        bin_mask = np.zeros_like(mask)
        new_output = mask.copy()
        new_cnts = [
            c
            for c in cnts
            if self.area_range[0] <= cv2.contourArea(c) <= self.area_range[1]
        ]
        bin_mask = fill_contours(bin_mask, new_cnts, color=BINARY_DEFAULT_VALUE)
        bin_mask = imfill(bin_mask)
        new_output[bin_mask == 0] = 0
        new_output[(new_output == 0) & bin_mask > 0] = BINARY_DEFAULT_VALUE

        return {"mask": new_output, "count": len(new_cnts)}


class EndpointMaskToLabels(Endpoint):
    def __init__(self):
        super().__init__("L", 1)

    def execute(self, entries):
        mask_pred = entries[0]
        ret, labels = cv2.connectedComponents(mask_pred)
        return mask_pred, None, len(np.unique(labels)) - 1, labels


class EndpointRescale(Endpoint):
    def __init__(self, scale_factor):
        super().__init__("R", 1)
        self.scale_factor = 1.0 / scale_factor

    def execute(self, entries):
        mask_pred = cv2.resize(
            entries[0],
            None,
            fx=self.scale_factor,
            fy=self.scale_factor,
            interpolation=cv2.INTER_CUBIC,
        )
        return mask_pred, mask_pred, mask_pred, mask_pred


class EndpointWatershed(Endpoint):
    def __init__(self, use_dt=False, markers_distance=21, markers_area=None):
        super().__init__("W", 2)
        self.wt = WatershedSkimage(use_dt=use_dt, markers_distance=markers_distance, markers_area=markers_area)

    def execute(self, entries):
        mask = entries[0]
        markers = entries[1]
        mask, markers, labels = self.wt.apply(mask, markers=markers, mask=mask > 0)
        return {
            "mask": mask,
            "markers": markers,
            "count": len(np.unique(labels)) - 1,
            "labels": labels,
        }
