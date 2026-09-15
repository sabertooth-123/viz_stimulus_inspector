"""Pilot run: 2 pairs per category (12 total) before spending the full quota."""

import json
import time

from inspector_ai import inspect_pair_ai

manifest = json.load(open("../data/manifest.json"))

by_category = {}
for item in manifest:
    by_category.setdefault(item["label"], []).append(item)

pilot_items = []
for category, items in by_category.items():
    pilot_items.extend(items[:2])

for item in pilot_items:
    result = inspect_pair_ai(item["image_a"], item["image_b"])
    print(f"{item['pair_id']} (true={item['label']}): verdict={result['verdict']}, unexpected={result.get('unexpected_differences')}")
    time.sleep(20)  