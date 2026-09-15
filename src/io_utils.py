"""Save a stimulus as a (spec.json, image.png) pair.

Keeping the spec next to its rendered image is what makes spec-based
comparison possible later - without this, a PNG on disk has no record
of what parameters produced it.
"""

import json
from pathlib import Path

from render import render


def save_stimulus(spec, name, base_dir="data"):
    """Render `spec` and write both the PNG and its spec JSON to disk.

    Args:
        spec: a stimulus spec dict (from stimulus_spec.make_spec).
        name: filename stem, e.g. "valid_001" - used for both the .png
            and the .json, so they can always be paired back up by name.
        base_dir: root data folder, expected to contain "specs/" and
            "stimuli/" subfolders.

    Returns:
        (spec_path, image_path) as Path objects.
    """
    base = Path(base_dir)
    spec_path = base / "specs" / f"{name}.json"
    image_path = base / "stimuli" / f"{name}.png"

    spec_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.parent.mkdir(parents=True, exist_ok=True)

    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=2)

    render(spec, image_path)

    return spec_path, image_path