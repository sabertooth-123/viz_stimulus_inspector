"""Image-based inspection: compare rendered stimuli via SSIM.

This is deliberately the simplest possible baseline - one global SSIM
score per pair, no masking or region isolation. We expect this to
struggle on subtle confounds when gridlines are also toggled, since
gridlines dominate the score. That's a hypothesis to test, not something
to engineer around yet.
"""

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def load_grayscale(path):
    """Load a PNG as a grayscale numpy array."""
    return np.array(Image.open(path).convert("L"))


def compute_ssim(image_path_a, image_path_b):
    """Return the SSIM score (0-1, higher = more similar) between two images."""
    img_a = load_grayscale(image_path_a)
    img_b = load_grayscale(image_path_b)
    score, _ = ssim(img_a, img_b, full=True)
    return score
def pad_to_common_size(img_a, img_b, fill_value=255):
    """Pad both arrays to the same shape (top-left anchored), no rescaling.

    Rescaling would distort content and could artificially hide a real
    dimension confound; padding preserves true pixel content and scale.
    """
    max_h = max(img_a.shape[0], img_b.shape[0])
    max_w = max(img_a.shape[1], img_b.shape[1])

    padded_a = np.full((max_h, max_w), fill_value, dtype=img_a.dtype)
    padded_a[: img_a.shape[0], : img_a.shape[1]] = img_a

    padded_b = np.full((max_h, max_w), fill_value, dtype=img_b.dtype)
    padded_b[: img_b.shape[0], : img_b.shape[1]] = img_b

    return padded_a, padded_b


def compute_ssim(image_path_a, image_path_b):
    """Return the SSIM score (0-1, higher = more similar) between two images."""
    img_a = load_grayscale(image_path_a)
    img_b = load_grayscale(image_path_b)

    if img_a.shape != img_b.shape:
        img_a, img_b = pad_to_common_size(img_a, img_b)

    score, _ = ssim(img_a, img_b, full=True)
    return score