# eriplots: Simple Plotting Utilities

[![CI](https://github.com/ElderResearch/eriplots-python/actions/workflows/ci.yml/badge.svg)](https://github.com/ElderResearch/eriplots-python/actions/workflows/ci.yml)

The *[eriplots][]* library for Python makes it a little easier to
create clean, client-ready figures, inspired by *[Trees, maps,
and theorems][tmth]* among others.

[eriplots]: https://github.com/ElderResearch/eriplots-python
[tmth]: https://www.principiae.be/X0100.php

## Installation

The best way to install or use the library is directly from GitHub:

```bash
# pip
pip install git+https://github.com/ElderResearch/eriplots-python.git

# uv
uv add git+https://github.com/ElderResearch/eriplots-python.git
```

## Features

The library's utilities are organized along four directions:

1. Simple plot styles, with "profiles" for papers and slides
2. A streamlined `subplots()` workflow
3. Multi-format figure saving with automatic PNG compression
4. ERI-branded color palettes and colormaps

### Plot Styling

The _eriplots_ library provides a simple, customizable
*[matplotlib][]* style via `eri_style()` that supports two
"profiles" for common scenarios:

1. **document**: 10 pt base type, 4.5 in × 2.5 in figure at 300 DPI
2. **presentation**: 20 pt base type, 7 in × 4 in figure at 300 DPI

Both profiles apply a clean style with consistent spacing,
reduced visual noise, and harmonically-scaled text elements.

```python
import matplotlib.pyplot as plt
import eriplots as ep

# Document and Presentation profiles
plt.style.use(ep.eri_style(profile="document"))
plt.style.use(ep.eri_style(profile="presentation"))

# Further customizations
plt.style.use(ep.eri_style(base_size=12, base_family="serif"))

# Use in a context
with plt.style.context(ep.eri_style()):
    ...
```

[matplotlib]: https://matplotlib.org/

### Simplified Workflow

The library also simplifies the `fig, ax = plt.subplots()`
workflow, making it easier to set options directly in the
function call.

```python
import eriplots as ep

# All subplots have a given aspect, provided as a flat array
fig, axes = ep.subplots(nrows=3, ncols=5, aspect=0.618, flatten=True)
```

### Multi-Format Figures

The _eriplots_ library provides a `save_figures()` function that
automatically store raster (PNG) and vector (PDF) copies of the
figure by default. When available, `[optipng][]` is applied to
any created PNGs.

```python
import eriplots as ep

# By default: "plot.png", "plot.pdf"
ep.save_figures(fig, "plot")

# Specify the formats: "plot.png"
ep.save_figures(fig, "plot", formats="png")

# Disable PNG optimization
ep.save_figures(fig, "plot", optipng=False)
```

[optipng]: https://optipng.sourceforge.net/

### Colors and Colormaps

Finally, the _eriplots_ library provides an enumeration over
colors related to ERI's branding with accompanying discrete and
continuous color maps.

```python
import eriplots as ep

# Individual colors
print(ep.colors.mediumblue)  # "#005E7B"
print(ep.colors.darkred)     # "#D0073A"

# Colormaps
import matplotlib.pyplot as plt
plt.imshow(data, cmap="eri_colors")  # Discrete colormap
plt.imshow(data, cmap="eri_red_cyan")  # Continuous colormap
```
## Contributing

We welcome contributions, both by raising issues and submitting
pull requests!

## License

The _eriplots_ library is licensed under the MIT license
([LICENSE.md](./LICENSE.md) or
<https://opensource.org/license/MIT>).
