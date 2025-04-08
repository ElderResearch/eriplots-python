"""Set up colormaps for named access and via matplotlib."""

__all__: list[str] = []


def _register_discrete_colormaps():
    """Create LinearSegmentedColormaps for each palette.

    For each palette, create two colormaps:
    - A regular colormap with the name "eri_{palette_name}"
    - A reversed colormap with the name "eri_{palette_name}_r"

    Both are registered with matplotlib for easy access and added to
    this module's __all__ for other use.

    """
    from matplotlib import colormaps
    from matplotlib.colors import ListedColormap

    from eriplots import palettes

    for palette_name in palettes.__all__:
        palette = getattr(palettes, palette_name)
        clist = list(palette)

        cmap_name = f"eri_{palette_name}"
        cmap = ListedColormap(clist, cmap_name)
        cmap_r = ListedColormap(clist[::-1], f"{cmap_name}_r")

        # Register with matplotlib
        colormaps.register(cmap, name=cmap_name, force=True)
        colormaps.register(cmap_r, name=f"{cmap_name}_r", force=True)

        # Assign into the package and push to all
        globals()[cmap_name] = cmap
        globals()[f"{cmap_name}_r"] = cmap_r
        __all__.append(cmap_name)
        __all__.append(f"{cmap_name}_r")


# Register continuous colormaps with matplotlib
def _register_continuous_colormaps():
    """Create and register continuous colormaps with matplotlib.

    Create continuous colormaps between color pairs:
    - 'eri_red_cyan': from darkred to lightblue (and reversed)
    - 'eri_red_blue': from darkred to darkblue (and reversed)

    All are registered with matplotlib for easy access and added to
    this module's __all__ for other use.

    """
    from matplotlib import colormaps
    from matplotlib.colors import LinearSegmentedColormap

    from eriplots.palettes import colors

    color_maps = {
        "eri_red_cyan": (colors.darkred, colors.lightblue),
        "eri_red_blue": (colors.darkred, colors.darkblue),
    }

    for cmap_name, color_tuple in color_maps.items():
        # Create and register regular and reversed colormaps
        cmap = LinearSegmentedColormap.from_list(cmap_name, color_tuple)
        cmap_r = LinearSegmentedColormap.from_list(f"{cmap_name}_r", color_tuple[::-1])

        colormaps.register(cmap, name=cmap_name, force=True)
        colormaps.register(cmap_r, name=f"{cmap_name}_r", force=True)

        # Assign into the package and push to all
        globals()[cmap_name] = cmap
        globals()[f"{cmap_name}_r"] = cmap_r
        __all__.append(cmap_name)
        __all__.append(f"{cmap_name}_r")


_register_discrete_colormaps()
_register_continuous_colormaps()
