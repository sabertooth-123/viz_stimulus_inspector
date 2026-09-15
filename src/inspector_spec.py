"""Spec-based inspector: decide whether a stimulus pair shows only the
intended manipulation, or an unintended confound.
"""

from spec_diff import diff_specs

EXPECTED_DIFF = {"gridlines"}


def inspect_pair(spec_a, spec_b):
    """Return a verdict dict for one stimulus pair.

    Compares observed differing fields against EXPECTED_DIFF (the only
    field the researcher intended to manipulate). Any extra differing
    field is reported as unexpected.
    """
    observed = diff_specs(spec_a, spec_b)
    unexpected = observed - EXPECTED_DIFF
    missing_expected = EXPECTED_DIFF - observed

    verdict = "CONFOUND_DETECTED" if unexpected else "VALID"

    return {
        "expected_diff": EXPECTED_DIFF,
        "observed_diff": observed,
        "unexpected_fields": unexpected,
        "missing_expected_fields": missing_expected,
        "verdict": verdict,
    }