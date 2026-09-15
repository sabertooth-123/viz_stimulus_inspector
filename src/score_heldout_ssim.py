import csv
import json

from inspector_image import compute_ssim

manifest = json.load(open("../data/heldout/manifest.json"))

with open("../data/heldout/ssim_scores.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["pair_id", "label", "ssim"])
    writer.writeheader()
    for item in manifest:
        score = compute_ssim(item["image_a"], item["image_b"])
        writer.writerow({"pair_id": item["pair_id"], "label": item["label"], "ssim": score})

print("Done")