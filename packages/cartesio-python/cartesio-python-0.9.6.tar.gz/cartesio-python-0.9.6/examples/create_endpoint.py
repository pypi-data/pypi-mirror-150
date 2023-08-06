from typing import List

import cv2

from cartesio.core.endpoint import Endpoint


class EndpointBinarize(Endpoint):
    def __init__(self, threshold: int):
        super().__init__("binarize", 1)
        self.threshold = threshold

    def execute(self, entries: List):
        img = entries[0]
        img = cv2.threshold(img, self.threshold, 255, cv2.THRESH_BINARY)[1]
        return img


def main():
    threshold = 128
    endpoint = EndpointBinarize(threshold)


if __name__ == "__main__":
    main()
