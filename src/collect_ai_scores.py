"""Run the AI-assisted inspector across the full dataset, saving results
incrementally so a rate-limit interruption doesn't lose completed work.
Safe to re-run - it skips pairs already recorded in ai_scores.csv.
"""

import csv
import json
import os
import time

from inspector_ai import inspect_pair_ai

manifest = json.load(open("../data/manifest.json"))
results_path = "../data/ai_scores.csv"

done_ids = set()
if os.path.exists(results_path):
    with open(results_path) as f:
        for row in csv.DictReader(f):
            done_ids.add(row["pair_id"])

fieldnames = ["pair_id", "label", "verdict", "unexpected_differences"]
write_header = not os.path.exists(results_path)

with open(results_path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if write_header:
        writer.writeheader()

    for item in manifest:
        if item["pair_id"] in done_ids:
            continue

        result = inspect_pair_ai(item["image_a"], item["image_b"])
        writer.writerow({
            "pair_id": item["pair_id"],
            "label": item["label"],
            "verdict": result["verdict"],
            "unexpected_differences": json.dumps(result.get("unexpected_differences", [])),
        })
        f.flush()
        print(f"{item['pair_id']} ({item['label']}): {result['verdict']}")
        time.sleep(20)