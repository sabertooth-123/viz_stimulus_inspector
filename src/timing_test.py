import json
import time

from inspector_image import compute_ssim
from inspector_pixeldiff import pixel_diff

manifest = json.load(open("../data/manifest.json"))

start = time.perf_counter()
for item in manifest:
    compute_ssim(item["image_a"], item["image_b"])
ssim_elapsed = time.perf_counter() - start

start = time.perf_counter()
for item in manifest:
    pixel_diff(item["image_a"], item["image_b"])
pixeldiff_elapsed = time.perf_counter() - start

print(f"SSIM: {ssim_elapsed:.3f}s total, {ssim_elapsed/len(manifest)*1000:.2f}ms/pair")
print(f"Pixel-diff: {pixeldiff_elapsed:.3f}s total, {pixeldiff_elapsed/len(manifest)*1000:.2f}ms/pair")