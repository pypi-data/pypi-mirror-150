import cv2
import numpy as np
from micromind.cv.image import contours, overlay
from micromind.figure.figure import Figure


def plot_mask(original, mask, color=[0, 255, 255]):
    fig = Figure(title="Mask Prediction", size=(12, 4))
    fig.create_panels(nrows=1, ncols=3)

    original_panel = fig.get_panel(0)
    original_panel.set_title("Original")
    original_panel.axis("off")
    original_panel.imshow(original)

    mask_panel = fig.get_panel(1)
    mask_panel.set_title("Mask")
    mask_panel.axis("off")
    mask_panel.imshow(mask, cmap="viridis")

    overlayed = overlay(original.copy(), mask, color=color)
    overlay_panel = fig.get_panel(2)
    overlay_panel.set_title("Overlayed")
    overlay_panel.axis("off")
    overlay_panel.imshow(overlayed)


def plot_markers(original, markers, color=[255, 0, 0], use_centroid=True):
    fig = Figure(title="Markers Prediction", size=(12, 4))
    fig.create_panels(nrows=1, ncols=3)

    original_panel = fig.get_panel(0)
    original_panel.set_title("Original")
    original_panel.axis("off")
    original_panel.imshow(original)

    mask_panel = fig.get_panel(1)
    mask_panel.set_title("Markers")
    mask_panel.axis("off")
    mask_panel.imshow(markers, cmap="viridis")

    overlayed = original.copy()
    if use_centroid:
        cnts = contours(markers)
        for cnt in cnts:
            cnt_x = cnt[:, 0, 0]
            cnt_y = cnt[:, 0, 1]
            centroid_x = cnt_x.mean()
            centroid_y = cnt_y.mean()
            cv2.circle(overlayed, (int(centroid_x), int(centroid_y)), 10, color, -1)
    else:
        overlayed = overlay(overlayed, markers, color=color)
    overlay_panel = fig.get_panel(2)
    overlay_panel.set_title("Overlayed")
    overlay_panel.axis("off")
    overlay_panel.imshow(overlayed)


def plot_watershed(original, mask, markers, labels):
    fig = Figure(title="Labels", size=(12, 4))
    fig.create_panels(nrows=1, ncols=4)

    original_panel = fig.get_panel(0)
    original_panel.set_title("Original")
    original_panel.axis("off")
    original_panel.imshow(original)

    mask_panel = fig.get_panel(1)
    mask_panel.set_title("Mask")
    mask_panel.axis("off")
    mask_panel.imshow(mask, cmap="viridis")

    mask_panel = fig.get_panel(2)
    mask_panel.set_title("Markers")
    mask_panel.axis("off")
    mask_panel.imshow(markers, cmap="viridis")

    overlayed = original.copy()
    list_labels = np.unique(labels)
    colors = np.random.randint(256, size=(len(list_labels), 3), dtype=np.uint8)
    # colors.sort()
    for i, label in enumerate(list_labels):
        if label == 0:
            continue
        color = colors[i].tolist()
        overlayed = overlay(
            overlayed, (labels == label).astype(np.uint8), color=color, alpha=0.8
        )
    overlay_panel = fig.get_panel(3)
    overlay_panel.set_title("Overlayed")
    overlay_panel.axis("off")
    overlay_panel.imshow(overlayed)
