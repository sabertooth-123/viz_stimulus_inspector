"""Deterministic spec-based inspection: diff two stimulus specs.

This is Version 3, the spec-based inspector - and also doubles as an
automated sanity check on the confound generators themselves, since it
tells us exactly which fields actually differ between a generated pair.
"""


def diff_specs(spec_a, spec_b):
    """Return the set of top-level keys whose values differ between two specs."""
    keys = set(spec_a) | set(spec_b)
    return {key for key in keys if spec_a.get(key) != spec_b.get(key)}