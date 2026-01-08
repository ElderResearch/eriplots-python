"""Matplotlib style."""

from typing import Any, Final, Literal

from cycler import cycler
from matplotlib.pyplot import rcParams

from eriplots.palettes import colors

__all__ = ["eri_style", "font_rel", "font_abs"]


# Unit conversions ---------------------------------------------------

# ggplot2's linewidths are in units of (roughly) 0.75 mm. See:
# https://ggplot2.tidyverse.org/articles/ggplot2-specs.html#linewidth.
GGPLOT2_MM: Final[float] = 0.75
MM_TO_PT: Final[float] = 72 / 10 / 2.54


# Styles -------------------------------------------------------------


def font_rel(n: float) -> float:
    """Set the relative (harmonic) font size."""
    return 2 ** (n / 5)


def font_abs(n: float) -> float:
    """Set the absolute (harmonic) font size."""
    return font_rel(n) * rcParams["font.size"]


def eri_style(
    profile: Literal["presentation", "document"] | None = None,
    base_size: float | None = None,
    base_family: str = "sans-serif",
    base_line_size: float | None = None,
) -> dict[str, Any]:
    """Define a style via rcParams overrides.

    Args:
        profile:
            Either "document" or "presentation". Sets the base font size
            and overall default figure size to touchly match the
            document type.
        base_size:
            The base font size, measured in points. The various textual
            elements in a figure are sized relative to this value.
        base_family:
            The base font family for the figure. Can be a generic name
            (e.g., "serif") or a specific font family name, as it is
            passed directly to "font.family" in `rcParams`.
        base_line_size:
            The base width of the figure spines and tick marks, measured
            in points. If None (the default), linewidths are defined in
            proportion to the base font size in a similar way as in the
            eriplots R package.

    Returns:
        An rcParams-compatible dictionary.

    Examples:
        Import libraries:

        >>> import matplotlib.pyplot as plt
        >>> import eriplots as ep

        Set the overall matplotlib styling:

        >>> plt.style.use(ep.eri_style(profile="presentation"))

        Or use a context manager for a short-term change:

        >>> with plt.style.context(ep.eri_style(base_size=10)):
                fix, ax = ep.subplots()
                ax.plot()

    """
    # Set default figure size and DPI based on profile
    figsize = None
    dpi = None

    # Hold on to original base size
    original_base_size = base_size

    # Set default values based on profile
    if profile == "document":
        base_size = 10
        figsize = (4.5, 2.5)
        dpi = 300

    elif profile == "presentation":
        base_size = 18
        figsize = (7, 4)
        dpi = 300

    # Apply, in order: original, profile, default
    if base_size is None:
        base_size = 11

    if original_base_size is not None:
        base_size = original_base_size

    # Config constants
    tick_size = 4 / 10 * base_size
    text_gray = "0.25"
    lims_gray = "0.65"

    # Use the R package linewidth unless specified. According to the
    # ggplot2 docs, linewidths are measured in about 0.75 mm, so we do a
    # conversion to points here and match up whatever's in our R theme.
    R_lw = base_size / (10 / 0.3) * GGPLOT2_MM * MM_TO_PT
    line_width = base_line_size if base_line_size is not None else R_lw

    style: dict[str, Any] = {}

    # Overall figure size
    if figsize is not None:
        style["figure.figsize"] = figsize

    # Fonts start at the base size and move down from there
    style["font.family"] = base_family
    style["font.size"] = base_size
    style["text.color"] = text_gray
    style["axes.labelsize"] = base_size * font_rel(1)
    style["axes.titlesize"] = base_size * font_rel(1)
    style["figure.titlesize"] = base_size * font_rel(2)
    style["xtick.labelsize"] = base_size * font_rel(-1)
    style["ytick.labelsize"] = base_size * font_rel(-1)

    # Do not set top and right edges
    style["axes.spines.right"] = False
    style["axes.spines.top"] = False

    # Spines and ticks are light gray
    style["axes.edgecolor"] = lims_gray
    style["xtick.color"] = lims_gray
    style["ytick.color"] = lims_gray

    # Text is dark gray
    style["axes.labelcolor"] = text_gray
    style["axes.titlecolor"] = text_gray
    style["xtick.labelcolor"] = text_gray
    style["ytick.labelcolor"] = text_gray

    # Spines and ticks are the same (small) width
    style["axes.linewidth"] = line_width
    style["xtick.major.width"] = line_width
    style["ytick.major.width"] = line_width

    # Grids share color and width with the spines
    style["grid.color"] = lims_gray
    style["grid.linewidth"] = line_width

    # Tick sizes and spacing
    # tick...pad: spacing between tick and tick label
    # titlepad: spacing to an axis title (not a label)
    # labelpad: spacing to an axis label
    style["xtick.major.pad"] = tick_size / 2
    style["ytick.major.pad"] = tick_size / 2
    style["xtick.major.size"] = tick_size
    style["ytick.major.size"] = tick_size
    style["axes.titlepad"] = tick_size
    style["axes.labelpad"] = tick_size

    # Standard boxes, but set padding in case we later choose "tight"
    style["savefig.bbox"] = "standard"
    style["savefig.pad_inches"] = 10 / 72

    # By default we use layout = "constrained"
    style["figure.constrained_layout.use"] = True

    # DPI for savefig
    if dpi is not None:
        style["savefig.dpi"] = dpi

    # Marker and line stylings
    style["lines.markersize"] = 3
    style["lines.linewidth"] = 1.25

    style["axes.axisbelow"] = True
    style["axes.xmargin"] = 0.05
    style["axes.ymargin"] = 0.05

    # Color cycle
    style["axes.prop_cycle"] = cycler("color", colors)

    return style
