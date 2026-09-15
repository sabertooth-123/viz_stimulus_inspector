"""Run the spec-based inspector across the full dataset and report results."""

import json
from collections import Counter

from inspector_spec import inspect_pair

manifest = json.load(open("../data/manifest.json"))

results = []
for item in manifest:
    spec_a = json.load(open(item["spec_a"]))
    spec_b = json.load(open(item["spec_b"]))
    verdict = inspect_pair(spec_a, spec_b)

    ground_truth_confound = item["label"] != "valid"
    predicted_confound = verdict["verdict"] == "CONFOUND_DETECTED"

    results.append({
        "pair_id": item["pair_id"],
        "label": item["label"],
        "predicted": verdict["verdict"],
        "correct": ground_truth_confound == predicted_confound,
    })

correct = sum(r["correct"] for r in results)
print(f"Overall: {correct}/{len(results)} = {correct/len(results):.1%}")

by_category, correct_by_category = Counter(), Counter()
for r in results:
    by_category[r["label"]] += 1
    correct_by_category[r["label"]] += r["correct"]

for cat in by_category:
    print(f"{cat}: {correct_by_category[cat]}/{by_category[cat]}")