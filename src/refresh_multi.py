"""Remove stale multi_confound rows so collect_ai_scores.py only
re-fetches those 20 (now-changed) pairs, not all 120."""

import csv

with open("../data/ai_scores.csv") as f:
    rows = [r for r in csv.DictReader(f) if r["label"] != "multi_confound"]

with open("../data/ai_scores.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["pair_id", "label", "verdict", "unexpected_differences"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Kept {len(rows)} rows, removed stale multi_confound entries")