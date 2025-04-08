"""Set up color palettes as Enums for easy named access."""

from enum import Enum

__all__ = ["colors"]


class StrEnum(str, Enum):
    """An enumeration over string values."""


class colors(StrEnum):
    """Full ERI-branded color palette.

    In addition to the primary and secondary brand colors, we have replaced
    (yellow) or added (pink, gray) colors from R. Robison's excellent
    collection of logo-related colors.
    """

    mediumblue = "#005E7B"
    darkred = "#D0073A"
    lightblue = "#008CA5"
    gray = "#777777"
    yellow = "#FBC15E"
    darkgreen = "#307F42"
    pink = "#FFB5B8"
    darkblue = "#063157"
    brightred = "#EA0D49"
    brown = "#603534"
    lightgreen = "#70B73F"
    orange = "#F7941D"
