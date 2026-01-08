"""Tests for styles module."""

import matplotlib.pyplot as plt

import eriplots as ep
from eriplots.styles import GGPLOT2_MM, MM_TO_PT


def test_eri_style_with_style_use():
    """Test that eri_style works with plt.style.use."""
    plt.style.use("default")
    default_fontsize = plt.rcParams["font.size"]

    plt.style.use(ep.eri_style(base_size=default_fontsize + 2))
    assert plt.rcParams["font.size"] == default_fontsize + 2

    plt.style.use("default")


def test_eri_style_with_style_context():
    """Test that eri_style works with plt.style.context."""
    default_fontsize = plt.rcParams["font.size"]

    with plt.style.context(ep.eri_style(base_size=default_fontsize + 2)):
        assert plt.rcParams["font.size"] == default_fontsize + 2

    # After context - should revert to default
    assert plt.rcParams["font.size"] == default_fontsize


def test_profile_document():
    """Test document profile settings."""
    style = ep.eri_style(profile="document")

    # Check specific document profile attributes
    assert style["font.size"] == 10
    assert style["figure.figsize"] == (4.5, 2.5)
    assert style["savefig.dpi"] == 300


def test_profile_presentation():
    """Test presentation profile settings."""
    style = ep.eri_style(profile="presentation")

    # Check specific presentation profile attributes
    assert style["font.size"] == 18
    assert style["figure.figsize"] == (7, 4)
    assert style["savefig.dpi"] == 300


def test_default_profile():
    """Test default profile settings."""
    style = ep.eri_style()

    # Default profile uses base_size 11 but keeps original figsize
    assert style["font.size"] == 11
    assert "figure.figsize" not in style
    assert "savefig.dpi" not in style


def test_profile_base_size_interaction():
    """Test the interaction between profile and base_size."""
    # Profile should set the base_size by default
    doc_style = ep.eri_style(profile="document")
    assert doc_style["font.size"] == 10

    # But explicit base_size should override profile default
    custom_style = ep.eri_style(profile="document", base_size=15)
    assert custom_style["font.size"] == 15

    # Figure size should still be from the document profile
    assert custom_style["figure.figsize"] == (4.5, 2.5)


def test_base_line_size_default():
    """Test that default base_line_size is correctly derived from base_size."""
    base_size = 12
    style = ep.eri_style(base_size=base_size)

    # Default calculation: base_size / (10 / 0.3) * GGPLOT2_MM * MM_TO_PT
    expected_width = base_size / (10 / 0.3) * GGPLOT2_MM * MM_TO_PT

    assert style["axes.linewidth"] == expected_width
    assert style["xtick.major.width"] == expected_width
    assert style["ytick.major.width"] == expected_width


def test_custom_base_line_size():
    """Test that custom base_line_size overrides the default calculation."""
    custom_width = 1.5
    style = ep.eri_style(base_line_size=custom_width)

    assert style["axes.linewidth"] == custom_width
    assert style["xtick.major.width"] == custom_width
    assert style["ytick.major.width"] == custom_width


def test_default_color_cycle():
    """Test that the default color cycle uses the ERI colors palette."""
    from eriplots.palettes import colors

    style = ep.eri_style()

    # Convert the color cycle to a list for comparison
    color_cycle = style["axes.prop_cycle"].by_key()["color"]

    # Get all color values from the colors enum programmatically
    expected_colors = [color.value for color in colors]

    assert color_cycle == expected_colors
