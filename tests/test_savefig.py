"""Tests for savefig module."""

import subprocess
from pathlib import Path

import pytest

import eriplots.savefig
from eriplots.savefig import save_figures


@pytest.fixture(autouse=True)
def reset_optipng():
    """Reset the _optipng module variable before each test."""
    original_optipng = eriplots.savefig._optipng
    eriplots.savefig._optipng = None
    yield
    eriplots.savefig._optipng = original_optipng


@pytest.fixture
def mock_figure(mocker):
    """Create a mock figure object."""
    fig = mocker.Mock()
    fig.savefig = mocker.Mock()
    return fig


def test_path_without_extension(mock_figure):
    """Test save_figures with path that has no extension."""
    path = Path("test_fig")
    save_figures(mock_figure, path, formats=("pdf", "png"))

    assert mock_figure.savefig.call_count == 2
    mock_figure.savefig.assert_any_call(fname=path.with_suffix(".pdf"), dpi="figure")
    mock_figure.savefig.assert_any_call(fname=path.with_suffix(".png"), dpi="figure")


def test_path_with_extension(mock_figure):
    """Test save_figures with path that has extension."""
    path = Path("test_fig.jpg")  # Extension doesn't match formats
    save_figures(mock_figure, path, formats=("pdf", "png"))

    assert mock_figure.savefig.call_count == 2
    mock_figure.savefig.assert_any_call(fname=Path("test_fig.pdf"), dpi="figure")
    mock_figure.savefig.assert_any_call(fname=Path("test_fig.png"), dpi="figure")


def test_path_with_matching_extension(mock_figure):
    """Test save_figures with path that has extension matching a format."""
    path = Path("test_fig.pdf")
    save_figures(mock_figure, path, formats=("pdf", "png"))

    assert mock_figure.savefig.call_count == 2
    mock_figure.savefig.assert_any_call(fname=path, dpi="figure")
    mock_figure.savefig.assert_any_call(fname=Path("test_fig.png"), dpi="figure")


def test_single_string_format(mock_figure):
    """Test save_figures with a single string format."""
    path = Path("test_fig")
    save_figures(mock_figure, path, formats="pdf")

    mock_figure.savefig.assert_called_once_with(
        fname=path.with_suffix(".pdf"),
        dpi="figure",
    )


def test_tuple_single_format(mock_figure):
    """Test save_figures with a tuple containing one format."""
    path = Path("test_fig")
    save_figures(mock_figure, path, formats=("pdf",))

    mock_figure.savefig.assert_called_once_with(
        fname=path.with_suffix(".pdf"), dpi="figure"
    )


def test_tuple_multiple_formats(mock_figure):
    """Test save_figures with multiple formats."""
    path = Path("test_fig")
    save_figures(mock_figure, path, formats=("pdf", "png", "svg"))

    assert mock_figure.savefig.call_count == 3
    mock_figure.savefig.assert_any_call(fname=path.with_suffix(".pdf"), dpi="figure")
    mock_figure.savefig.assert_any_call(fname=path.with_suffix(".png"), dpi="figure")
    mock_figure.savefig.assert_any_call(fname=path.with_suffix(".svg"), dpi="figure")


def test_custom_dpi(mock_figure):
    """Test save_figures with custom DPI."""
    path = Path("test_fig")
    save_figures(mock_figure, path, formats="pdf", dpi=300)

    mock_figure.savefig.assert_called_once_with(fname=path.with_suffix(".pdf"), dpi=300)


def test_webp_supported(mock_figure, mocker):
    """Test saving webp when Pillow supports the format."""
    mocker.patch("eriplots.savefig._webp_supported", return_value=True)

    path = Path("test_fig")
    save_figures(mock_figure, path, formats="webp")

    mock_figure.savefig.assert_called_once_with(
        fname=path.with_suffix(".webp"),
        dpi="figure",
    )


def test_webp_not_supported(mock_figure, mocker):
    """Test that requesting webp fails with a helpful error."""
    mocker.patch("eriplots.savefig._webp_supported", return_value=False)

    path = Path("test_fig")
    with pytest.raises(RuntimeError, match="WebP"):
        save_figures(mock_figure, path, formats=("pdf", "webp"))

    mock_figure.savefig.assert_not_called()


def test_optipng_false(mock_figure, mocker):
    """Test that optipng is skipped when optipng=False."""
    mock_check_call = mocker.patch("eriplots.savefig.check_call")
    path = Path("test_fig")
    save_figures(mock_figure, path, formats=("pdf", "png"), optipng=False)

    mock_check_call.assert_not_called()


def test_optipng_true_success(mock_figure, mocker):
    """Test that optipng is called when optipng=True and succeeds."""
    mock_check_call = mocker.patch("eriplots.savefig.check_call")
    path = Path("test_fig")
    save_figures(mock_figure, path, formats=("pdf", "png"), optipng=True)

    mock_check_call.assert_called_once_with(
        ["optipng", str(path.with_suffix(".png"))],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


def test_optipng_true_not_found(mock_figure, mocker):
    """Test that optipng=True raises error when executable not found."""
    mock_check_call = mocker.patch("eriplots.savefig.check_call")
    mock_check_call.side_effect = FileNotFoundError("optipng not found")

    path = Path("test_fig")
    with pytest.raises(FileNotFoundError):
        save_figures(mock_figure, path, formats=("pdf", "png"), optipng=True)


def test_optipng_none_success(mock_figure, mocker):
    """Test that optipng is attempted when optipng=None and succeeds."""
    mock_check_call = mocker.patch("eriplots.savefig.check_call")
    path = Path("test_fig")
    save_figures(mock_figure, path, formats=("pdf", "png"), optipng=None)

    mock_check_call.assert_called_once()


def test_optipng_none_failure(mock_figure, mocker):
    """Test that optipng silently fails when optipng=None and not available."""
    mock_check_call = mocker.patch("eriplots.savefig.check_call")
    mock_check_call.side_effect = FileNotFoundError("optipng not found")

    path = Path("test_fig")
    # Should not raise an exception
    save_figures(mock_figure, path, formats=("pdf", "png"), optipng=None)

    # Check that _optipng is now False
    assert eriplots.savefig._optipng is False


def test_optipng_skipped_when_png_not_in_formats(mock_figure, mocker):
    """Test that optipng is not called when PNG is not in formats."""
    mock_check_call = mocker.patch("eriplots.savefig.check_call")
    path = Path("test_fig")
    save_figures(mock_figure, path, formats=("pdf", "svg"), optipng=True)

    mock_check_call.assert_not_called()
