import json
import csv

from inspector_image import compute_ssim

manifest = json.load(open("../data/manifest.json"))

rows = []
for item in manifest:
    score = compute_ssim(item["image_a"], item["image_b"])
    rows.append({"pair_id": item["pair_id"], "label": item["label"], "ssim": score})

with open("../data/ssim_scores.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["pair_id", "label", "ssim"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} scores to ../data/ssim_scores.csv")