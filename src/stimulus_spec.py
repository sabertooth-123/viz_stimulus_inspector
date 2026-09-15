"""Declarative specification schema for controlled bar-chart stimuli.

Every stimulus is generated FROM one of these dicts, never from hardcoded
plotting calls. This is what lets us create a confound by changing exactly
one field, and what gives Version 2 (spec-based comparison) a ground truth
to diff against.
"""

DEFAULT_SPEC = {
    "gridlines": False,  # the independent variable in the motivating experiment
    "data": {
        "categories": ["A", "B", "C", "D", "E"],
        "values": [42, 67, 31, 84, 55],
    },
    "chart_width": 800,   # pixels
    "chart_height": 600,  # pixels
    "bar_width": 0.6,     # fraction of the unit slot per category (matplotlib convention)
    "tick_spacing": 20,
    "background_color": "#FFFFFF",
    "axis_min": 0,
    "axis_max": 100,
    "font_family": "DejaVu Sans",
    "font_size": 12,
    "bar_color": "#4C72B0",
}


def make_spec(**overrides):
    """Return a fresh copy of DEFAULT_SPEC with the given fields overridden.

    Always copy rather than mutate DEFAULT_SPEC directly - dicts are
    mutable, so handing out DEFAULT_SPEC itself would let one caller's
    edits leak into every other stimulus generated afterward.
    """
    spec = {
        key: (value.copy() if isinstance(value, dict) else value)
        for key, value in DEFAULT_SPEC.items()
    }
    spec.update(overrides)
    return spec