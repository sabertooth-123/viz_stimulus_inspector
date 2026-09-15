import json
from collections import defaultdict

from inspector_pixeldiff import pixel_diff

manifest = json.load(open("../data/manifest.json"))

scores_by_category = defaultdict(list)
for item in manifest:
    score = pixel_diff(item["image_a"], item["image_b"])
    scores_by_category[item["label"]].append(score)

for category, scores in scores_by_category.items():
    print(f"{category}: min={min(scores):.5f} max={max(scores):.5f} mean={sum(scores)/len(scores):.5f}")