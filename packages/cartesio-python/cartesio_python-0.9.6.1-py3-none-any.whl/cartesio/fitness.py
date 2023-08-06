from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from cartesio.core.evolution import Fitness
from cartesio.metric import (
    MetricCellpose,
    MetricCount,
    MetricIOU,
    MetricMSE,
    MetricPrecision,
    MetricCrossEntropy,
)

# from glmnet import ElasticNet, LogitNet


class FitnessAP05(Fitness):
    def __init__(self):
        self.AP05 = MetricCellpose()

    def _evaluate_one(self, y_true, y_pred):
        y_true_labels = [y[0] for y in y_true]  # get labels
        y_pred_labels = [y["labels"] for y in y_pred]  # get labels
        ap, _, _, _ = self._fitness(y_true_labels, y_pred_labels)
        return 1.0 - np.mean(np.array(ap))

    def _fitness(self, y_true, y_pred):
        return self.AP05.average_precision(y_true, y_pred, threshold=[0.5])


class FitnessAP07(Fitness):
    def __init__(self):
        self.AP07 = MetricCellpose()

    def _evaluate_one(self, y_true, y_pred):
        y_true_labels = [y[0] for y in y_true]  # get labels
        y_pred_labels = [y["labels"] for y in y_pred]  # get labels
        ap, _, _, _ = self._fitness(y_true_labels, y_pred_labels)
        return 1.0 - np.mean(np.array(ap))

    def _fitness(self, y_true, y_pred):
        return self.AP07.average_precision(y_true, y_pred, threshold=[0.7])


class FitnessCount(Fitness, ABC):
    def __init__(self):
        self.count_metric = MetricCount()

    def _fitness(self, y_true, y_pred):
        return self.count_metric.compute(y_true, y_pred)

    def _evaluate_one(self, y_true, y_pred):
        fitnesses = []
        for i in range(len(y_true)):
            fitnesses.append(self._fitness(y_true[i].copy(), y_pred[i].copy()))
        return np.mean(np.array(fitnesses))


class FitnessCountPrecision(FitnessCount):
    def __init__(self):
        super().__init__()
        self.precision_metric = MetricPrecision()

    def _fitness(self, y_true, y_pred):
        mask_true, count_true = y_true
        count = super()._fitness(count_true, y_pred["count"])
        precision = 1 - self.precision_metric.compute(mask_true, y_pred["mask"])
        return count + precision


class FitnessCountIOU(FitnessCount):
    def __init__(self):
        super().__init__()
        self.iou_metric = MetricIOU()

    def _fitness(self, y_true, y_pred):
        mask_true, count_true = y_true
        count = super()._fitness(count_true, y_pred["count"])
        iou = 1 - self.iou_metric.compute(mask_true, y_pred["mask"])
        return count + iou


class FitnessIOU(Fitness):
    def __init__(self):
        self.iou_metric = MetricIOU()

    def _fitness(self, y_true, y_pred):
        return 1.0 - self.iou_metric.compute(y_true, y_pred)


class FitnessWatershed(FitnessCount):
    def __init__(self):
        super().__init__()
        self.iou_metric = MetricIOU()
        self.precision_metric = MetricPrecision()

    def _fitness(self, y_true, y_pred):
        mask_true, count_true = y_true
        count = super()._fitness(count_true, y_pred["count"])
        iou = 1 - self.iou_metric.compute(mask_true, y_pred["mask"])
        precision = 1 - self.precision_metric.compute(mask_true, y_pred["markers"])
        return count + iou + precision


class FitnessMSE(Fitness):
    def __init__(self):
        self.mse_metric = MetricMSE()

    def _fitness(self, y_true, y_pred):
        return self.mse_metric.compute(y_true, y_pred)


class FitnessEllipse(FitnessCountIOU):
    def __init__(self, min_axis, max_axis):
        super(FitnessEllipse, self).__init__(EndpointEllipse(min_axis, max_axis))


class FitnessElasticNet(Fitness):
    def __init__(self):
        super(FitnessElasticNet, self).__init__()
        self.model = LogitNet(n_splits=0)

    def mask_to_features(self, mask, seeds):
        mask_pred, seeds, n_seeds, labels = self.watershed(mask.copy(), seeds.copy())
        count = 0
        for l in labels:
            count += np.count_nonzero(l)
        return count

    def _fitness(self, y_true, y_pred):
        mask_pred, seeds = y_pred
        if not mask_pred.any() or mask_pred.all() or np.count_nonzero(mask_pred) == 0:
            feature = 0
        else:
            feature = self.mask_to_features(mask_pred, seeds)
        return feature

    def evaluate_one_individual(self, y_true, y_pred):
        features = []
        for one_y_true, one_y_pred in zip(y_true, y_pred):
            features.append(self._fitness(one_y_true.copy(), one_y_pred))
        x = pd.Series(features)
        y = pd.Series(np.array(y_true).flatten())

        score = x.corr(y)

        if score == 0:
            return 0
        if score > 0.0:
            return 1 - score

        return 2 - score

        """
        try:
            self.model.fit(x, y)
            new_pred = self.model.predict(x)
            print(new_pred)
            score = y_true - new_pred
        except ValueError:
            score = 10.
        except IndexError:
            score = 10.
        
        """


class FitnessCrossEntropy(Fitness):
    def __init__(self):
        self.cross_entropy_metric = MetricCrossEntropy()

    def _fitness(self, y_true, y_pred):
        return self.cross_entropy_metric.compute(y_true, y_pred)

    def _evaluate_one(self, y_true, y_pred):
        fitness = []
        for i in range(len(y_true)):
            fitness.append(self._fitness(y_true[i][0].copy(), y_pred[i]["softmax"].copy()))
        return np.mean(np.array(fitness))
