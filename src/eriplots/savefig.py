"""Save raster and vector figures together."""

from pathlib import Path
from subprocess import DEVNULL, PIPE, CalledProcessError, check_call
from typing import Literal, Optional, Union

from matplotlib.figure import Figure

_SaveTypes = Literal["pdf", "svg", "eps", "png", "tiff", "webp"]
_optipng: Optional[bool] = None


def save_figures(
    figure: Figure,
    path: Union[str, Path],
    formats: Union[_SaveTypes, tuple[_SaveTypes, ...]] = ("pdf", "png"),
    dpi: Union[int, Literal["figure"]] = "figure",
    optipng: Optional[bool] = None,
    **kw,
) -> None:
    global _optipng

    path = Path(path)

    if isinstance(formats, str):
        formats = (formats,)

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
