"""Evaluate the OR-hybrid inspector on the held-out set, using the
threshold and rule already fixed from dev-set analysis - not re-derived
here, since that would defeat the purpose of testing generalization.
"""

import csv
import json

DEV_THRESHOLD = 0.96696  # fixed from the original 120-pair dev set

ssim_rows = {r["pair_id"]: r for r in csv.DictReader(open("../data/heldout/ssim_scores.csv"))}
ai_rows = {r["pair_id"]: r for r in csv.DictReader(open("../data/heldout/ai_scores.csv"))}
manifest = json.load(open("../data/heldout/manifest.json"))

tp = fp = tn = fn = 0
by_category = {}

for item in manifest:
    pid, label = item["pair_id"], item["label"]
    is_confound = label != "valid"

    ssim_flag = float(ssim_rows[pid]["ssim"]) < DEV_THRESHOLD
    ai_flag = ai_rows[pid]["verdict"] == "CONFOUND_DETECTED"
    hybrid_flag = ssim_flag or ai_flag

    by_category.setdefault(label, {"total": 0, "detected": 0})
    by_category[label]["total"] += 1
    if hybrid_flag:
        by_category[label]["detected"] += 1

    if is_confound and hybrid_flag:
        tp += 1
    elif is_confound and not hybrid_flag:
        fn += 1
    elif not is_confound and hybrid_flag:
        fp += 1
    else:
        tn += 1

print(f"Held-out hybrid (OR): TP={tp} FP={fp} TN={tn} FN={fn}")
precision = tp / (tp + fp) if (tp + fp) else float("nan")
recall = tp / (tp + fn) if (tp + fn) else float("nan")
print(f"Precision={precision:.2%} Recall={recall:.2%}")

print("\nPer-category:")
for cat, counts in by_category.items():
    print(f"{cat}: {counts['detected']}/{counts['total']}")