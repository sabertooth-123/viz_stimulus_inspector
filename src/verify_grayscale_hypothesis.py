"""Check whether color_confound detection correlates with grayscale
luminance difference - the proposed mechanism for why grayscale SSIM
misses some hue-only changes. Checks ALL 20 pairs, not just the misses,
to avoid cherry-picking evidence for our own hypothesis.
"""

import csv
import json

rows = []
with open("../data/ssim_scores.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["ssim"] = float(row["ssim"])
        rows.append(row)

valid_scores = [r["ssim"] for r in rows if r["label"] == "valid"]
threshold = min(valid_scores)

manifest = {item["pair_id"]: item for item in json.load(open("../data/manifest.json"))}


def hex_to_grayscale_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    # same luminance-weighted formula PIL's "L" conversion uses
    return 0.299 * r + 0.587 * g + 0.114 * b


color_rows = [r for r in rows if r["label"] == "color_confound"]

print(f"{'pair_id':<22} {'lum_diff':>9} {'ssim':>8} {'status':>10}")
for r in sorted(color_rows, key=lambda x: x["pair_id"]):
    item = manifest[r["pair_id"]]
    spec_a = json.load(open(item["spec_a"]))
    spec_b = json.load(open(item["spec_b"]))
    lum_a = hex_to_grayscale_luminance(spec_a["bar_color"])
    lum_b = hex_to_grayscale_luminance(spec_b["bar_color"])
    lum_diff = abs(lum_a - lum_b)
    status = "MISSED" if r["ssim"] >= threshold else "detected"
    print(f"{r['pair_id']:<22} {lum_diff:>9.1f} {r['ssim']:>8.4f} {status:>10}")