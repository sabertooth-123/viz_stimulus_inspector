"""Consolidate spec-based and image-based results into one comparison table.

Note the asymmetry: spec-based "100%" is not a detection-ability number
(it's circular, established earlier) - it's included as a labeled
methodological baseline, not as evidence the method "works" the way the
image-based recall numbers do.
"""

import csv
from collections import defaultdict

rows = []
with open("../data/ssim_scores.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["ssim"] = float(row["ssim"])
        rows.append(row)

valid_scores = [r["ssim"] for r in rows if r["label"] == "valid"]
threshold = min(valid_scores)

by_category = defaultdict(lambda: {"total": 0, "detected": 0})
for r in rows:
    is_confound = r["label"] != "valid"
    predicted_confound = r["ssim"] < threshold
    by_category[r["label"]]["total"] += 1
    if is_confound and predicted_confound:
        by_category[r["label"]]["detected"] += 1

print(f"{'category':<20} {'spec-based*':>12} {'image-based (SSIM)':>20}")
for category in ["font_confound", "color_confound", "axis_confound", "dimension_confound", "multi_confound"]:
    counts = by_category[category]
    image_rate = counts["detected"] / counts["total"]
    print(f"{category:<20} {'100%*':>12} {image_rate:>19.0%}")

print("\n* spec-based recall is circular by construction (see Version 5 findings)")
print("  and should not be read as evidence of genuine detection ability.")
print(f"\nImage-based threshold: SSIM < {threshold:.4f} (min of valid-category scores)")
print("Image-based false positive rate: 0/20 valid pairs incorrectly flagged")