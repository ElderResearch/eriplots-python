"""Tests for the colormaps module."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from eriplots import colormaps, palettes


def test_discrete_colormaps_registered():
    """Test that all discrete colormaps are registered with matplotlib."""
    # For each palette in palettes.__all__, there should be eri_{name} and eri_{name}_r
    for palette_name in palettes.__all__:
        cmap_name = f"eri_{palette_name}"
        cmap_r_name = f"{cmap_name}_r"

        # Check registration with matplotlib
        assert cmap_name in plt.colormaps()
        assert cmap_r_name in plt.colormaps()

        # Check that they're accessible as Python objects
        assert hasattr(colormaps, cmap_name)
        assert hasattr(colormaps, cmap_r_name)


def test_continuous_colormaps_registered():
    """Test that all continuous colormaps are registered with matplotlib."""
    continuous_cmaps = [
        "eri_red_cyan",
        "eri_red_cyan_r",
        "eri_red_blue",
        "eri_red_blue_r",
    ]

    for cmap_name in continuous_cmaps:
        # Check registration with matplotlib
        assert cmap_name in plt.colormaps()

        # Check that they're accessible as Python objects
        assert hasattr(colormaps, cmap_name)


def get_all_cmap_names():
    """Get all expected colormap names for parameterized tests."""
    cmap_names = []

    # Discrete colormaps from palettes
    for palette_name in palettes.__all__:
        cmap_names.append(f"eri_{palette_name}")
        cmap_names.append(f"eri_{palette_name}_r")

    # Continuous colormaps
    cmap_names.extend(
        [
            "eri_red_cyan",
            "eri_red_cyan_r",
            "eri_red_blue",
            "eri_red_blue_r",
        ]
    )

    return cmap_names


@pytest.mark.parametrize("cmap_name", get_all_cmap_names())
def test_colormaps_usable_in_plots(cmap_name):
    """Test that all colormaps can be used with matplotlib plots."""
    # Create a simple plot using the colormap
    fig, ax = plt.subplots()

    # Generate data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Plot with the colormap
    scatter = ax.scatter(x, y, c=x, cmap=cmap_name)

    # Add a colorbar
    fig.colorbar(scatter, ax=ax)

    # Ensure this doesn't raise an exception
    plt.close(fig)


@pytest.mark.parametrize("cmap_name", get_all_cmap_names())
def test_colormaps_as_python_objects(cmap_name):
    """Test that colormaps can be used as Python objects."""
    # Get the colormap as a Python object
    cmap = getattr(colormaps, cmap_name)

    # Test applying the colormap directly to values
    values = np.linspace(0, 1, 10)

    # This should return RGB or RGBA values
    colors = cmap(values)

    # Verify shape and type
    assert colors.shape == (10, 4)  # RGBA values
    assert colors.dtype == np.float64

    # Verify range
    assert np.all(colors >= 0)
    assert np.all(colors <= 1)
