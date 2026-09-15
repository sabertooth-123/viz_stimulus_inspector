"""Compare SSIM-alone, Gemini-alone, OR-hybrid, and AND-hybrid on the
SAME held-out set - the actual apples-to-apples comparison, including F1."""

import csv
import json

DEV_THRESHOLD = 0.96696  # mean - 2*stdev, fixed from dev set

ssim_rows = {r["pair_id"]: r for r in csv.DictReader(open("../data/heldout/ssim_scores.csv"))}
ai_rows = {r["pair_id"]: r for r in csv.DictReader(open("../data/heldout/ai_scores.csv"))}
manifest = json.load(open("../data/heldout/manifest.json"))


def score(flag_fn, name):
    tp = fp = tn = fn = 0
    by_cat = {}
    for item in manifest:
        pid, label = item["pair_id"], item["label"]
        is_confound = label != "valid"
        flag = flag_fn(pid)
        by_cat.setdefault(label, {"total": 0, "detected": 0})
        by_cat[label]["total"] += 1
        if flag:
            by_cat[label]["detected"] += 1
        if is_confound and flag: tp += 1
        elif is_confound and not flag: fn += 1
        elif not is_confound and flag: fp += 1
        else: tn += 1
    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    recall = tp / (tp + fn) if (tp + fn) else float("nan")
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else float("nan")
    print(f"\n{name}: TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"  Precision={precision:.2%} Recall={recall:.2%} F1={f1:.2%}")
    for cat, c in by_cat.items():
        print(f"  {cat}: {c['detected']}/{c['total']}")


ssim_flag = lambda pid: float(ssim_rows[pid]["ssim"]) < DEV_THRESHOLD
ai_flag = lambda pid: ai_rows[pid]["verdict"] == "CONFOUND_DETECTED"
or_flag = lambda pid: ssim_flag(pid) or ai_flag(pid)
and_flag = lambda pid: ssim_flag(pid) and ai_flag(pid)

score(ssim_flag, "SSIM alone")
score(ai_flag, "Gemini alone")
score(or_flag, "OR-hybrid")
score(and_flag, "AND-hybrid")