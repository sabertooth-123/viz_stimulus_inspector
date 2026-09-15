"""Generate randomized (spec_a, spec_b, label) pairs with known ground truth.

Each pair's underlying data is randomized so 20 pairs in one category are
20 genuinely different examples, not the same example repeated - otherwise
we'd effectively have a sample size of 1 per category, and any detector
could "succeed" by memorizing one hardcoded confound value instead of
actually generalizing.
"""

import numpy as np

from stimulus_spec import make_spec

CATEGORY_LABELS = ["A", "B", "C", "D", "E"]


def random_base_data(rng):
    """Sample 5 random bar values in a fixed, reasonable range."""
    values = rng.integers(low=20, high=95, size=5).tolist()
    return {"categories": CATEGORY_LABELS, "values": values}


def make_pair_valid(rng):
    """A and B differ ONLY in gridlines - the clean baseline, no confound."""
    data = random_base_data(rng)
    spec_a = make_spec(gridlines=False, data=data)
    spec_b = make_spec(gridlines=True, data=data)
    return spec_a, spec_b, "valid"


def make_pair_font_confound(rng):
    """B also has a shifted font_size - an unintended confound."""
    data = random_base_data(rng)
    delta = int(rng.choice([2, 3, 4]))  # points - randomized, not fixed
    spec_a = make_spec(gridlines=False, data=data)
    spec_b = make_spec(
        gridlines=True, data=data, font_size=spec_a["font_size"] + delta
    )
    return spec_a, spec_b, "font_confound"

def make_pair_color_confound(rng):
    """B also has a shifted bar_color - an unintended confound."""
    data = random_base_data(rng)
    palette = ["#DD8452", "#55A868", "#C44E52", "#8172B2"]
    new_color = str(rng.choice(palette))
    spec_a = make_spec(gridlines=False, data=data)
    spec_b = make_spec(gridlines=True, data=data, bar_color=new_color)
    return spec_a, spec_b, "color_confound"


def make_pair_axis_confound(rng):
    """B also has a shifted axis_min - an unintended confound."""
    data = random_base_data(rng)
    new_min = int(rng.choice([5, 10, 15]))
    spec_a = make_spec(gridlines=False, data=data)
    spec_b = make_spec(gridlines=True, data=data, axis_min=new_min)
    return spec_a, spec_b, "axis_confound"


def make_pair_dimension_confound(rng):
    """B also has a shifted chart_width - an unintended confound."""
    data = random_base_data(rng)
    delta = int(rng.choice([50, 100, 150]))
    spec_a = make_spec(gridlines=False, data=data)
    spec_b = make_spec(
        gridlines=True, data=data, chart_width=spec_a["chart_width"] + delta
    )
    return spec_a, spec_b, "dimension_confound"


def make_pair_multi_confound(rng):
    """B has 2-3 randomly chosen confounds combined, not a fixed pair
    every time - tests general multi-attribute detection rather than
    one hardcoded combination.
    """
    data = random_base_data(rng)
    spec_a = make_spec(gridlines=False, data=data)

    def font_component():
        delta = int(rng.choice([2, 3, 4]))
        return "font_size", spec_a["font_size"] + delta

    def color_component():
        palette = ["#DD8452", "#55A868", "#C44E52", "#8172B2"]
        return "bar_color", str(rng.choice(palette))

    def axis_component():
        return "axis_min", int(rng.choice([5, 10, 15]))

    def dimension_component():
        delta = int(rng.choice([50, 100, 150]))
        return "chart_width", spec_a["chart_width"] + delta

    components = [font_component, color_component, axis_component, dimension_component]
    n_confounds = int(rng.choice([2, 3]))
    chosen_idx = rng.choice(len(components), size=n_confounds, replace=False)

    overrides = {}
    for i in chosen_idx:
        field, value = components[i]()
        overrides[field] = value

    spec_b = make_spec(gridlines=True, data=data, **overrides)
    return spec_a, spec_b, "multi_confound"