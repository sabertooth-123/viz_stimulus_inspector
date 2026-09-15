"""Render a stimulus spec dict into a bar-chart PNG."""

import numpy as np
import matplotlib.pyplot as plt

RENDER_DPI = 100  # fixed pipeline constant - never varies between stimuli


def render(spec, output_path):
    """Render one stimulus spec to a PNG at output_path.

    Uses plt.rc_context to scope font settings to just this call, instead
    of mutating plt.rcParams globally - if we generate 120 stimuli in a
    loop, a global rcParams change would leak from one stimulus into the
    next whenever a later spec doesn't explicitly override it. That would
    be a bug in the generator itself introducing an unintended font
    confound - exactly the failure mode this whole project is about.
    """
    with plt.rc_context({"font.family": spec["font_family"], "font.size": spec["font_size"]}):
        fig, ax = plt.subplots(
            figsize=(spec["chart_width"] / RENDER_DPI, spec["chart_height"] / RENDER_DPI),
            dpi=RENDER_DPI,
        )

        ax.bar(
            spec["data"]["categories"],
            spec["data"]["values"],
            width=spec["bar_width"],
            color=spec["bar_color"],
        )

        ax.set_ylim(spec["axis_min"], spec["axis_max"])

        ticks = np.arange(
            spec["axis_min"],
            spec["axis_max"] + spec["tick_spacing"],
            spec["tick_spacing"],
        )
        ax.set_yticks(ticks)

        ax.grid(spec["gridlines"], axis="y")

        fig.patch.set_facecolor(spec["background_color"])
        ax.set_facecolor(spec["background_color"])

        fig.savefig(output_path, dpi=RENDER_DPI)
        plt.close(fig)