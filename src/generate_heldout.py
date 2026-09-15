"""Generate a held-out set with a different seed - never used to design
the hybrid inspector. This is the real test of whether the hybrid rule
generalizes, not just fits the original 120-pair sample.
"""

import json
from pathlib import Path

import numpy as np

from confounds import (
    make_pair_valid, make_pair_font_confound, make_pair_color_confound,
    make_pair_axis_confound, make_pair_dimension_confound, make_pair_multi_confound,
)
from io_utils import save_stimulus

N_PER_CATEGORY = 5
SEED = 123  # different from the dev set's seed=42

GENERATORS = {
    "valid": make_pair_valid,
    "font_confound": make_pair_font_confound,
    "color_confound": make_pair_color_confound,
    "axis_confound": make_pair_axis_confound,
    "dimension_confound": make_pair_dimension_confound,
    "multi_confound": make_pair_multi_confound,
}


def main():
    rng = np.random.default_rng(seed=SEED)
    manifest = []

    for category, generator in GENERATORS.items():
        for i in range(N_PER_CATEGORY):
            spec_a, spec_b, label = generator(rng)
            assert label == category

            spec_path_a, image_path_a = save_stimulus(
                spec_a, f"heldout_{category}_{i:03d}_A", base_dir="../data/heldout"
            )
            spec_path_b, image_path_b = save_stimulus(
                spec_b, f"heldout_{category}_{i:03d}_B", base_dir="../data/heldout"
            )

            manifest.append({
                "pair_id": f"heldout_{category}_{i:03d}",
                "label": category,
                "spec_a": str(spec_path_a),
                "spec_b": str(spec_path_b),
                "image_a": str(image_path_a),
                "image_b": str(image_path_b),
            })

    with open("../data/heldout/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {len(manifest)} held-out pairs")


if __name__ == "__main__":
    main()