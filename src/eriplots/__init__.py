"""Plotting utilities in support of best practices.

* colormaps: matplotlib and general-use colormaps and utilities
* extensions: matplotlib extensions, like subplots()
* palettes: color palettes
* styles: matplotlib style dictionary generaing function

"""

from importlib import metadata as _metadata

from eriplots import colormaps, styles
from eriplots.mpl import alpha, subplots
from eriplots.palettes import colors
from eriplots.savefig import save_figures
from eriplots.styles import eri_style

__all__ = [
    "subplots",
    "colors",
    "eri_style",
    "save_figures",
    "colormaps",
    "styles",
    "alpha",
]

# https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
__version__ = _metadata.version("eriplots")
