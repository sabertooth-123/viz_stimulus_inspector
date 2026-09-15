"""Raw pixel-difference baseline, kept in RGB (unlike SSIM's grayscale)
to isolate whether grayscale conversion specifically explains SSIM's
color-confound blind spot, or whether any coarse pixel method would miss it.
"""

import numpy as np
from PIL import Image


def load_rgb(path):
    return np.array(Image.open(path).convert("RGB"))


def pad_to_common_size_rgb(img_a, img_b, fill_value=255):
    max_h = max(img_a.shape[0], img_b.shape[0])
    max_w = max(img_a.shape[1], img_b.shape[1])
    padded_a = np.full((max_h, max_w, 3), fill_value, dtype=img_a.dtype)
    padded_a[: img_a.shape[0], : img_a.shape[1]] = img_a
    padded_b = np.full((max_h, max_w, 3), fill_value, dtype=img_b.dtype)
    padded_b[: img_b.shape[0], : img_b.shape[1]] = img_b
    return padded_a, padded_b


def pixel_diff(image_path_a, image_path_b):
    """Mean absolute pixel difference across RGB channels, normalized to [0,1]."""
    img_a = load_rgb(image_path_a)
    img_b = load_rgb(image_path_b)
    if img_a.shape != img_b.shape:
        img_a, img_b = pad_to_common_size_rgb(img_a, img_b)
    diff = np.abs(img_a.astype(np.int16) - img_b.astype(np.int16))
    return diff.mean() / 255.0