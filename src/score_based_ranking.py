"""Score-based combination: rank held-out pairs by combined risk, and
check how many real confounds are surfaced by reviewing only the top-K -
motivated by triage/researcher-effort reduction, not by beating OR's
already-ceiling precision/recall.
"""

import csv
import json
import statistics

ssim_rows = {r["pair_id"]: r for r in csv.DictReader(open("../data/heldout/ssim_scores.csv"))}
ai_rows = {r["pair_id"]: r for r in csv.DictReader(open("../data/heldout/ai_scores.csv"))}
manifest = json.load(open("../data/heldout/manifest.json"))

dev_valid_scores = [float(r["ssim"]) for r in csv.DictReader(open("../data/ssim_scores.csv")) if r["label"] == "valid"]
dev_mean = statistics.mean(dev_valid_scores)
dev_stdev = statistics.stdev(dev_valid_scores)


def combined_score(pid):
    ssim_z = (dev_mean - float(ssim_rows[pid]["ssim"])) / dev_stdev  # higher = more anomalous
    ai_bonus = 10.0 if ai_rows[pid]["verdict"] == "CONFOUND_DETECTED" else 0.0
    return ssim_z + ai_bonus


ranked = sorted(manifest, key=lambda item: combined_score(item["pair_id"]), reverse=True)
n_confounds = sum(1 for item in manifest if item["label"] != "valid")
print(f"Total real confounds: {n_confounds}/{len(manifest)}\n")

found = 0
for rank, item in enumerate(ranked, start=1):
    if item["label"] != "valid":
        found += 1
    if rank % 5 == 0:
        print(f"Top {rank}: {found}/{n_confounds} confounds surfaced ({found/n_confounds:.0%})")