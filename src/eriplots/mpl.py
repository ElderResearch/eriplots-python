"""Matplotlib extensions."""

from __future__ import annotations

import warnings
from collections.abc import Iterator
from typing import Literal, overload

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy import flatiter
from numpy.typing import NDArray

__all__ = ["subplots", "alpha"]

# AxesArray objects to better hint subplots outputs ------------------


class AxesArray:
    """Semi-transparent wrapper for arrays of Axes objects.

    This class provides typed access to arrays of Axes objects while
    maintaining numpy-like behavior. It automatically forwards
    operations to the underlying NumPy array while ensuring proper type
    hints for indexing operations.

    Attributes:
        np: The underlying NumPy array of Axes objects.

    Note:
        This is a base class that should not be used directly. Use
        AxesArray1D or AxesArray2D instead, which provide type hints for
        their respective dimensionalities.

    """

    def __init__(self, array: NDArray):
        self.np = array

    def __array__(self) -> NDArray:
        """Mark this class as available for use with NumPy."""
        return self.np

    def __getattr__(self, name: str):
        """Automatically dispatch to NumPy as a fallback."""
        if not name.startswith("_"):
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
    """One-dimensional array of Axes with typed indexing.

    This class provides type hints for indexing operations on 1D arrays
    of Axes objects. Single indices return Axes objects, while slices
    return new AxesArray1D instances.

    Examples:
        >>> fig, axes = subplots(1, 3)
        >>> isinstance(axes[0], Axes)  # Single index returns Axes
        True
        >>> isinstance(axes[1:], AxesArray1D)  # Slice returns AxesArray1D
        True
    """

    def __iter__(self) -> Iterator[Axes]:
        for ax in self.np:
            yield ax

    @overload
    def __getitem__(self, key: int | tuple[int]) -> Axes: ...

    @overload
    def __getitem__(self, key: slice | tuple[slice]) -> AxesArray1D: ...

    def __getitem__(
        self,
        key: int | slice | tuple[int] | tuple[slice],
    ) -> Axes | AxesArray1D:
        """Index into the array of Axes objects.

        Args:
            key: Integer, slice, or 1D tuple of the same.

        Returns:
            Either a single Axes object or a new AxesArray1D instance,
            depending on the indexing operation.

        """
        selection = self.np[key]
        if isinstance(selection, Axes):
            return selection
        if isinstance(selection, np.ndarray) and selection.ndim == 1:
            return AxesArray1D(selection.view())
        raise ValueError(f"Invalid selection type or dimensionality: {type(selection)}")


class AxesArray2D(AxesArray):
    """Two-dimensional array of Axes with typed indexing.

    This class provides type hints for indexing operations on 2D arrays
    of Axes. The return type depends on the indexing operation:

    - Single indices return AxesArray1D instances
    - Double indices return Axes objects
    - Slices return AxesArray2D instances

    Examples:
        >>> fig, axes = subplots(2, 2)
        >>> isinstance(axes[0], AxesArray1D)  # Single index returns AxesArray1D
        True
        >>> isinstance(axes[0, 0], Axes)  # Double index returns Axes
        True
        >>> isinstance(axes[:, :1], AxesArray2D)  # Slice returns AxesArray2D
        True
    """

    def __iter__(self) -> Iterator[AxesArray1D]:
        for arr in self.np:
            yield AxesArray1D(arr.view())

    @overload
    def __getitem__(self, key: tuple[int, int]) -> Axes: ...

    @overload
    def __getitem__(
        self,
        key: int | tuple[int] | tuple[int, slice] | tuple[slice, int],
    ) -> AxesArray1D: ...

    @overload
    def __getitem__(
        self,
        key: slice | tuple[slice] | tuple[slice, slice],
    ) -> AxesArray2D: ...

    def __getitem__(
        self,
        key: (
            int
            | slice
            | tuple[int]
            | tuple[slice]
            | tuple[int, int]
            | tuple[slice, slice]
            | tuple[int, slice]
            | tuple[slice, int]
        ),
    ) -> Axes | AxesArray1D | AxesArray2D:
        """Index into the array of Axes objects.

        Args:
            key: An integer, slice, or tuple of integers/slices.

        Returns:
            Either a single Axes object, an AxesArray1D instance, or an
            AxesArray2D instance, depending on the indexing operation.

        """
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
def subplots(  # type: ignore[overload-overlap]
    nrows: Literal[1] = 1,
    ncols: Literal[1] = 1,
    figsize: tuple[float, float] | None = None,
    aspect: float | None = None,
    dpi: int | None = None,
    flatten: bool = False,
    shift: float | tuple[float, float] | Literal[True] = 0,
    **kw,
) -> tuple[Figure, Axes]: ...


@overload
def subplots(
    nrows: Literal[1] = 1,
    ncols: int = ...,
    figsize: tuple[float, float] | None = None,
    aspect: float | None = None,
    dpi: int | None = None,
    flatten: bool = False,
    shift: float | tuple[float, float] | Literal[True] = 0,
    **kw,
) -> tuple[Figure, AxesArray1D]: ...


@overload
def subplots(
    nrows: int = ...,
    ncols: Literal[1] = 1,
    figsize: tuple[float, float] | None = None,
    aspect: float | None = None,
    dpi: int | None = None,
    flatten: bool = False,
    shift: float | tuple[float, float] | Literal[True] = 0,
    **kw,
) -> tuple[Figure, AxesArray1D]: ...


@overload
def subplots(
    nrows: int,
    ncols: int,
    figsize: tuple[float, float] | None = None,
    aspect: float | None = None,
    dpi: int | None = None,
    flatten: bool = False,
    shift: float | tuple[float, float] | Literal[True] = 0,
    **kw,
) -> tuple[Figure, AxesArray2D]: ...


def subplots(
    nrows: int = 1,
    ncols: int = 1,
    figsize: tuple[float, float] | None = None,
    aspect: float | None = None,
    dpi: int | None = None,
    flatten: bool = False,
    shift: float | tuple[float, float] | Literal[True] = 0,
    **kw,
) -> tuple[Figure, Axes | AxesArray1D | AxesArray2D]:
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


# Layer alpha values -------------------------------------------------


def alpha(n: int, max_opacity: float = 0.85) -> float:
    """Calculate alpha levels for stacked plot components.

    This function calculates alpha (opacity) values for plot components
    so that when n layers are stacked they have overall alpha =
    max_opacity.

    Args:
        n: Target number of stacked layers.
        max_opacity: The maximum opacity value at n (default: 0.85).

    Returns:
        A float between 0 and max_opacity.

    Examples:
        >>> alpha(1)  # Single component
        0.85
        >>> alpha(2)  # Two components, each with alpha ~ 0.613
        0.6127016653792583
        >>> alpha(3)  # Three components, each with alpha ~ 0.469
        0.4686707154086944
        >>> alpha(2, max_opacity=0.8)  # Custom max opacity
        0.5527864045000421

    """
    if n <= 0:
        raise ValueError("n must be positive")

    if max_opacity <= 0 or max_opacity > 1:
        raise ValueError("max_opacity must be between 0 and 1")

    return 1 - (1 - max_opacity) ** (1 / n)
