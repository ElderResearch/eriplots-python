"""Matplotlib extensions."""

from __future__ import annotations

from typing import Literal, Optional, Union, overload

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

__all__ = ["subplots"]


# Extended version of matplotlib.pyplot.subplots ---------------------


@overload
def subplots(
    nrows: Literal[1] = 1,
    ncols: Literal[1] = 1,
    figsize: Optional[tuple[float, float]] = None,
    aspect: Optional[float] = None,
    dpi: Optional[int] = None,
    flatten: bool = False,
    shift: Union[float, tuple[float, float], Literal[True]] = 0,
    **kw,
) -> tuple[Figure, Axes]: ...


@overload
def subplots(
    nrows: int,
    ncols: int,
    figsize: Optional[tuple[float, float]] = None,
    aspect: Optional[float] = None,
    dpi: Optional[int] = None,
    flatten: bool = False,
    shift: Union[float, tuple[float, float], Literal[True]] = 0,
    **kw,
) -> tuple[Figure, NDArray]: ...


def subplots(
    nrows: int = 1,
    ncols: int = 1,
    figsize: Optional[tuple[float, float]] = None,
    aspect: Optional[float] = None,
    dpi: Optional[int] = None,
    flatten: bool = False,
    shift: Union[float, tuple[float, float], Literal[True]] = 0,
    **kw,
) -> tuple[Figure, Union[Axes, NDArray]]:
    """Create a figure and one or more subplots.

    This extends matplotlib.pyplot.subplots().

    Args:
        nrows:
            Number of rows in the subplot grid.
        ncols:
            Number of columns in the subplot grid.
        figsize:
            Width, height in inches.
        aspect:
            Aspect ratio of each subplot.
        dpi:
            Resolution of the figure.
        flatten:
            If True, return the axes array flattened to 1D. Default is
            False.
        shift:
            Shift the y and/or x axes by this number of points. Useful
            for making "capped" axes that look good. If an integer,
            shift both axes by the same amount. If a tuple, shift the y
            and x axes by these amounts, respectively. If True, shift
            only the y axis, and shift by twice the tick length.

    Returns:
        A tuple containing:

        - fig: The created matplotlib Figure object.
        - axes: Either a single Axes object (if nrows == ncols == 1)
                or a 1-D or 2-D ndarray of Axes objects, depending on
                the configuration of nrows and ncols.

    """
    # Promote the axis shift if needed
    if shift is True:
        shift = (2 * plt.rcParams.get("xtick.major.size", 0), 0)
    elif isinstance(shift, (float, int)):
        shift = (shift, shift)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi, **kw)

    # Fix up weird typing thing matplotlib does
    if not isinstance(axes, np.ndarray):
        axes = np.array([axes])

    # Operate on the individual axes
    for ax in axes.flat:
        if aspect is not None:
            ax.set_box_aspect(aspect)
        if shift != (0, 0):
            for spine, ds in zip(("left", "bottom"), shift):
                ax.spines[spine].set_position(("outward", ds))

    # If multiple axes, flatten
    if flatten and not isinstance(axes, Axes) and axes.ndim > 1:
        axes = axes.flatten()

    # Nonsense with mypy x matplotlib x numpy
    return_axes: Union[Axes, NDArray]
    return_axes = axes.item() if ncols == 1 and nrows == 1 else axes

    return fig, return_axes
