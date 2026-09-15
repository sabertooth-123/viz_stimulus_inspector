"""Generate the full controlled confound dataset: 20 pairs x 6 categories.

Uses one seeded RNG shared across all categories in a fixed order, so the
entire dataset is exactly reproducible from SEED alone - important if this
ever needs to be regenerated or checked by someone else (e.g. a reviewer).
"""

import json
from pathlib import Path

import numpy as np

from confounds import (
    make_pair_valid, make_pair_font_confound, make_pair_color_confound,
    make_pair_axis_confound, make_pair_dimension_confound, make_pair_multi_confound,
)
from io_utils import save_stimulus

N_PER_CATEGORY = 20
SEED = 42

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

            name_a = f"{category}_{i:03d}_A"
            name_b = f"{category}_{i:03d}_B"

            spec_path_a, image_path_a = save_stimulus(spec_a, name_a, base_dir="../data")
            spec_path_b, image_path_b = save_stimulus(spec_b, name_b, base_dir="../data")

            manifest.append({
                "pair_id": f"{category}_{i:03d}",
                "label": category,
                "spec_a": str(spec_path_a),
                "spec_b": str(spec_path_b),
                "image_a": str(image_path_a),
                "image_b": str(image_path_b),
            })

    manifest_path = Path("../data/manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {len(manifest)} pairs -> {manifest_path}")


if __name__ == "__main__":
    main()