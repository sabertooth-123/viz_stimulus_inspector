"""Evaluate AI-assisted inspection results across the full dataset."""

import csv
from collections import defaultdict

with open("../data/ai_scores.csv") as f:
    rows = list(csv.DictReader(f))

parse_errors = [r for r in rows if r["verdict"] == "PARSE_ERROR"]
scored_rows = [r for r in rows if r["verdict"] != "PARSE_ERROR"]

by_category = defaultdict(lambda: {"total": 0, "detected": 0})
tp = fp = tn = fn = 0

for r in scored_rows:
    is_confound = r["label"] != "valid"
    predicted_confound = r["verdict"] == "CONFOUND_DETECTED"

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

print(f"Parse errors (excluded from metrics): {len(parse_errors)} -> {[r['pair_id'] for r in parse_errors]}")
print(f"Overall: TP={tp} FP={fp} TN={tn} FN={fn}")
precision = tp / (tp + fp) if (tp + fp) else float("nan")
recall = tp / (tp + fn) if (tp + fn) else float("nan")
print(f"Precision={precision:.2%} Recall={recall:.2%}")

print("\nPer-category detection rate:")
for category, counts in by_category.items():
    rate = counts["detected"] / counts["total"]
    print(f"{category}: {counts['detected']}/{counts['total']} = {rate:.1%}")