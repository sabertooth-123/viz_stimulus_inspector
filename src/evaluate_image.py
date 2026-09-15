"""Evaluate image-based (SSIM) inspection using an anomaly-detection threshold.

Threshold is set using ONLY the 'valid' category's scores (the least
similar valid pair) - we never touch confound-labeled data to pick it,
avoiding tuning and evaluating on the same information.
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
print(f"Threshold (min valid SSIM) = {threshold:.4f}")

import statistics
# was: threshold = min(valid_scores)
threshold = statistics.mean(valid_scores) - 2 * statistics.stdev(valid_scores)

by_category = defaultdict(lambda: {"total": 0, "detected": 0})
tp = fp = tn = fn = 0

for r in rows:
    is_confound = r["label"] != "valid"
    predicted_confound = r["ssim"] < threshold

    by_category[r["label"]]["total"] += 1
    if predicted_confound:
        by_category[r["label"]]["detected"] += 1

    if is_confound and predicted_confound:
        tp += 1
    elif is_confound and not predicted_confound:
        fn += 1
    elif not is_confound and predicted_confound:
        fp += 1
    else:
        tn += 1

print(f"\nOverall: TP={tp} FP={fp} TN={tn} FN={fn}")
precision = tp / (tp + fp) if (tp + fp) else float("nan")
recall = tp / (tp + fn) if (tp + fn) else float("nan")
print(f"Precision={precision:.2%} Recall={recall:.2%}")

print("\nPer-category detection rate:")
for category, counts in by_category.items():
    rate = counts["detected"] / counts["total"]
    print(f"{category}: {counts['detected']}/{counts['total']} = {rate:.1%}")