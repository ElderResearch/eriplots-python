# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `alpha(n, max_opacity=0.85)` computes layer opacities such that
  n layers stack with a cumulative `max_opacity`.

### Changed

- (DEV) Added isort rules to Ruff

## [0.1.2] – 2025-04-10

### Added

- `AxesArray`, `AxesArray1D`, and `AxesArray2D`: thin wrappers
  around NumPy arrays of `Axes` to support type hinting and
  autocompletion for users following usual patterns.

### Changed

- `subplots()` now returns one of the `AxesArray` subclasses (or
  just `Axes`) depending on the requested rows and columns. These
  arrays support autocompletion much better than the usual NumPy
  ones but should perform just the same.

## [0.1.1] – 2025-04-09

### Added

- R. Robison is correctly added as an author for his color
  palette definitions. Apologies for the oversight!
- CI pipeline to run Ruff, pytest, and mypy. Also tests direct
  package installation.

## [0.1.0] – 2025-04-08

First *eriplots* release!

### Added

- Matplotlib style function
- Augmented `subplots()`
- Save figures in multiple formats
- Color palettes and colormaps

[Unreleased]: https://github.com/ElderResearch/eriplots-python/compare/0.1.2...develop
[0.1.0]: https://github.com/ElderResearch/eriplots-python/releases/tag/0.1.0
[0.1.1]: https://github.com/ElderResearch/eriplots-python/releases/tag/0.1.1
[0.1.2]: https://github.com/ElderResearch/eriplots-python/releases/tag/0.1.2
