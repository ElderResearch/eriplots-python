"""Matplotlib extensions."""

from __future__ import annotations

import warnings
from typing import Literal, Optional, Union, overload

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy import flatiter
from numpy.typing import NDArray

__all__ = ["subplots"]


# AxesArray objects to better hint subplots outputs ------------------

KeyLike1D = Union[int, slice, tuple[int], tuple[slice]]


class AxesArray:
    def __init__(self, array: NDArray):
        self.np = array

    # Operate with numpy
    def __array__(self) -> NDArray:
        return self.np

    # Automatically dispatch to numpy as a fallback
    def __getattr__(self, name):
        warnings.warn(f"Missing attribute '{name}' dispatching to NumPy")
        return getattr(self.np, name)

    # Basic numpy properties
    @property
    def shape(self) -> tuple[int, ...]:
        return self.np.shape

    @property
    def size(self) -> int:
        return self.np.size

    @property
    def ndim(self) -> int:
        return len(self.shape)

    # Wrangling shapes
    def flatten(self) -> AxesArray1D:
        return AxesArray1D(self.np.flatten())

    def ravel(self) -> AxesArray1D:
        return AxesArray1D(self.np.ravel())

    @property
    def flat(self) -> flatiter[NDArray]:
        return self.np.flat


class AxesArray1D(AxesArray):
    @overload
    def __getitem__(self, key: Union[int, tuple[int]]) -> Axes: ...

    @overload
    def __getitem__(self, key: Union[slice, tuple[slice]]) -> AxesArray1D: ...

    def __getitem__(
        self, key: Union[int, slice, tuple[int], tuple[slice]]
    ) -> Union[Axes, AxesArray1D]:
        selection = self.np[key]
        if isinstance(selection, Axes):
            return selection
        if isinstance(selection, np.ndarray) and selection.ndim == 1:
            return AxesArray1D(selection.view())
        raise ValueError(f"Invalid selection type or dimensionality: {type(selection)}")


class AxesArray2D(AxesArray):
    @overload
    def __getitem__(self, key: tuple[int, int]) -> Axes: ...

    @overload
    def __getitem__(
        self, key: Union[int, tuple[int], tuple[int, slice], tuple[slice, int]]
    ) -> AxesArray1D: ...

    @overload
    def __getitem__(
        self, key: Union[slice, tuple[slice], tuple[slice, slice]]
    ) -> AxesArray2D: ...

    def __getitem__(
        self,
        key: Union[
            int,
            slice,
            tuple[int],
            tuple[slice],
            tuple[int, int],
            tuple[slice, slice],
            tuple[int, slice],
            tuple[slice, int],
        ],
    ) -> Union[Axes, AxesArray1D, AxesArray2D]:
        selection = self.np[key]
        if isinstance(selection, Axes):
            return selection
        if isinstance(selection, np.ndarray):
            if selection.ndim == 1:
                return AxesArray1D(selection.view())
            if selection.ndim == 2:
                return AxesArray2D(selection.view())
        raise ValueError(f"Invalid selection type or dimensionality: {type(selection)}")


# Extended version of matplotlib.pyplot.subplots ---------------------


@overload
def subplots(  # type: ignore  # This actually works
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
    nrows: Literal[1] = 1,
    ncols: int = ...,
    figsize: Optional[tuple[float, float]] = None,
    aspect: Optional[float] = None,
    dpi: Optional[int] = None,
    flatten: bool = False,
    shift: Union[float, tuple[float, float], Literal[True]] = 0,
    **kw,
) -> tuple[Figure, AxesArray1D]: ...


@overload
def subplots(
    nrows: int = ...,
    ncols: Literal[1] = 1,
    figsize: Optional[tuple[float, float]] = None,
    aspect: Optional[float] = None,
    dpi: Optional[int] = None,
    flatten: bool = False,
    shift: Union[float, tuple[float, float], Literal[True]] = 0,
    **kw,
) -> tuple[Figure, AxesArray1D]: ...


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
) -> tuple[Figure, AxesArray2D]: ...


def subplots(
    nrows: int = 1,
    ncols: int = 1,
    figsize: Optional[tuple[float, float]] = None,
    aspect: Optional[float] = None,
    dpi: Optional[int] = None,
    flatten: bool = False,
    shift: Union[float, tuple[float, float], Literal[True]] = 0,
    **kw,
) -> tuple[Figure, Union[Axes, AxesArray1D, AxesArray2D]]:
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

    # If only one figure, return Axes
    if ncols == 1 and nrows == 1:
        retax: Axes = axes.item()
        return fig, retax

    # If a flat array, return AxesArray1D
    elif axes.ndim == 1:
        return fig, AxesArray1D(axes)

    # Otherwise, return a 2D array
    elif axes.ndim == 2:
        return fig, AxesArray2D(axes)

    else:
        raise ValueError(f"Axes array has ndim = {axes.ndim}")
