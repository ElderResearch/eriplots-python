"""Save raster and vector figures together."""

from pathlib import Path
from subprocess import DEVNULL, PIPE, CalledProcessError, check_call
from typing import Literal, Optional, Union

from matplotlib.figure import Figure

_SaveTypes = Literal["pdf", "svg", "eps", "png", "tiff", "webp"]

_SUFFIX_TO_FORMAT: dict[str, _SaveTypes] = {
    "pdf": "pdf",
    "svg": "svg",
    "eps": "eps",
    "png": "png",
    "tif": "tiff",
    "tiff": "tiff",
    "webp": "webp",
}

_DEFAULT_FORMATS: tuple[_SaveTypes, ...] = ("pdf", "png")

_optipng: Optional[bool] = None


def _webp_supported() -> bool:
    """Determine and report whether WebP is supported."""
    try:
        from PIL import features as _pil_features
    except ImportError:
        return False

    try:
        return bool(_pil_features.check("webp"))
    except Exception:
        return False


def save_figures(
    figure: Figure,
    path: Union[str, Path],
    formats: Optional[Union[_SaveTypes, tuple[_SaveTypes, ...]]] = None,
    dpi: Union[int, Literal["figure"]] = "figure",
    optipng: Optional[bool] = None,
    **kw,
) -> None:
    global _optipng

    path = Path(path)

    formats_explicit = formats is not None

    if formats is None:
        formats = _DEFAULT_FORMATS
    elif isinstance(formats, str):
        formats = (formats,)

    if not formats_explicit:
        ext = path.suffix.lstrip(".").lower()
        if ext in _SUFFIX_TO_FORMAT:
            fmt = _SUFFIX_TO_FORMAT[ext]
            if fmt not in formats:
                formats = (*formats, fmt)

    if "webp" in formats and not _webp_supported():
        raise RuntimeError(
            "Saving as .webp requires Pillow built with WebP support. "
            "Install Pillow with WebP support (often `pip install pillow` "
            "on systems where libwebp is available)."
        )

    for fmt in formats:
        figure.savefig(fname=path.with_suffix(f".{fmt}"), dpi=dpi, **kw)

    if optipng is not False and _optipng is not False and "png" in formats:
        try:
            cmd = ["optipng", str(path.with_suffix(".png"))]
            check_call(cmd, stdout=DEVNULL, stderr=PIPE)
        except (FileNotFoundError, CalledProcessError) as err:
            _optipng = False
            if optipng is True:
                raise err
