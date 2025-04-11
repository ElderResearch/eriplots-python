"""Tests for matplotlib extensions."""

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from eriplots.mpl import AxesArray1D, AxesArray2D, subplots


def test_single_subplot():
    """Test that a single subplot returns a Figure and Axes."""
    fig, ax = subplots(1, 1)
    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)


def test_multiple_subplots():
    """Test that multiple subplots return a Figure and ndarray."""
    fig, axes = subplots(2, 2)
    assert isinstance(fig, Figure)
    assert isinstance(axes, AxesArray2D)
    assert axes.shape == (2, 2)


def test_flatten_subplots():
    """Test that flatten=True returns a 1D array for multi-subplots."""
    fig, axes = subplots(2, 3, flatten=True)
    assert isinstance(axes, AxesArray1D)
    assert axes.ndim == 1
    assert axes.size == 6


def test_shift_true():
    """Test that shift=True shifts only y-axis by twice the tick length."""
    fig, ax = subplots(1, 1, shift=True)
    # The actual value is based on rcParams, so we just check the spine is shifted
    assert ax.spines["left"].get_position()[0] == "outward"
    assert ax.spines["left"].get_position()[1] > 0
    assert ax.spines["bottom"].get_position()[0] == "outward"
    assert ax.spines["bottom"].get_position()[1] == 0


def test_shift_float():
    """Test that shift as a float shifts both axes by that amount."""
    shift_amount = 10.5
    fig, ax = subplots(1, 1, shift=shift_amount)
    assert ax.spines["left"].get_position()[0] == "outward"
    assert ax.spines["left"].get_position()[1] == shift_amount
    assert ax.spines["bottom"].get_position()[0] == "outward"
    assert ax.spines["bottom"].get_position()[1] == shift_amount


def test_shift_tuple():
    """Test that shift as a tuple shifts axes by respective amounts."""
    shift_y, shift_x = 15.0, 7.5
    fig, ax = subplots(1, 1, shift=(shift_y, shift_x))
    assert ax.spines["left"].get_position()[0] == "outward"
    assert ax.spines["left"].get_position()[1] == shift_y
    assert ax.spines["bottom"].get_position()[0] == "outward"
    assert ax.spines["bottom"].get_position()[1] == shift_x


def test_aspect_propagation():
    """Test that aspect is properly set on all axes."""
    aspect = 1.5
    fig, axes = subplots(2, 2, aspect=aspect)
    for ax in axes.flat:
        assert ax.get_box_aspect() == aspect


def test_shift_propagation():
    """Test that shift is applied to all axes in a multi-plot figure."""
    shift_amount = 5.0
    fig, axes = subplots(2, 2, shift=shift_amount)
    for ax in axes.flat:
        assert ax.spines["left"].get_position()[0] == "outward"
        assert ax.spines["left"].get_position()[1] == shift_amount
        assert ax.spines["bottom"].get_position()[0] == "outward"
        assert ax.spines["bottom"].get_position()[1] == shift_amount


def test_row_subplots():
    """Test for row of subplots (single row, multiple columns)."""
    fig, axes = subplots(1, 3)
    assert isinstance(fig, Figure)
    assert isinstance(axes, AxesArray1D)
    assert axes.shape == (3,)


def test_column_subplots():
    """Test for column of subplots (multiple rows, single column)."""
    fig, axes = subplots(3, 1)
    assert isinstance(fig, Figure)
    assert isinstance(axes, AxesArray1D)
    assert axes.shape == (3,)


def test_2d_subplots():
    """Test a 2D plot layout."""
    fig, axes = subplots(2, 2)
    assert isinstance(fig, Figure)
    assert isinstance(axes, AxesArray2D)
    assert axes.shape == (2, 2)


def test_axes_array_1d_indexing():
    """Test indexing behavior of AxesArray1D."""
    fig, axes = subplots(1, 3)
    assert isinstance(axes, AxesArray1D)

    # Test single index returns Axes
    assert isinstance(axes[0], Axes)
    assert isinstance(axes[-1], Axes)

    # Test slice returns AxesArray1D
    sliced = axes[:1]
    assert isinstance(sliced, AxesArray1D)
    assert sliced.np.shape == (1,)

    # Test tuple indexing returns Axes
    assert isinstance(axes[(0,)], Axes)
    assert isinstance(axes[(-1,)], Axes)


def test_axes_array_2d_indexing():
    """Test indexing behavior of AxesArray2D."""
    fig, axes = subplots(2, 2)
    assert isinstance(axes, AxesArray2D)

    # Test double integer returns Axes
    assert isinstance(axes[0, 0], Axes)
    assert isinstance(axes[0, -1], Axes)
    assert isinstance(axes[-1, 0], Axes)
    assert isinstance(axes[-1, -1], Axes)

    # Single integer returns 1D array
    assert isinstance(axes[0], AxesArray1D)
    assert isinstance(axes[-1], AxesArray1D)
    assert isinstance(axes[0, :], AxesArray1D)
    assert isinstance(axes[:, 0], AxesArray1D)
    assert isinstance(axes[(0,)], AxesArray1D)

    # But these should be 2D arrays
    assert isinstance(axes[:, :], AxesArray2D)
    assert isinstance(axes[:, :1], AxesArray2D)
    assert isinstance(axes[:1, :1], AxesArray2D)
