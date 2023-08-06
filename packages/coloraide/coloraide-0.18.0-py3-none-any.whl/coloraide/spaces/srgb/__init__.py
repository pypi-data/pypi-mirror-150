"""SRGB color class."""
from ...spaces import Space
from ...cat import WHITES
from ...gamut.bounds import GamutBound, FLG_OPT_PERCENT
from ... import algebra as alg
from ...types import Vector
import math


def lin_srgb(rgb: Vector) -> Vector:
    """
    Convert an array of sRGB values in the range 0.0 - 1.0 to linear light (un-corrected) form.

    https://en.wikipedia.org/wiki/SRGB
    """

    result = []
    for i in rgb:
        # Mirror linear nature of algorithm on the negative axis
        abs_i = abs(i)
        if abs_i > 0.04045:
            result.append(math.copysign(((abs_i + 0.055) / 1.055) ** 2.4, i))
        else:
            result.append(i / 12.92)
    return result


def gam_srgb(rgb: Vector) -> Vector:
    """
    Convert an array of linear-light sRGB values in the range 0.0-1.0 to gamma corrected form.

    https://en.wikipedia.org/wiki/SRGB
    """

    result = []
    for i in rgb:
        # Mirror linear nature of algorithm on the negative axis
        abs_i = abs(i)
        if abs_i > 0.0031308:
            result.append(math.copysign(1.055 * (alg.nth_root(abs_i, 2.4)) - 0.055, i))
        else:
            result.append(12.92 * i)
    return result


class SRGB(Space):
    """SRGB class."""

    BASE = "srgb-linear"
    NAME = "srgb"
    CHANNEL_NAMES = ("r", "g", "b")
    CHANNEL_ALIASES = {
        "red": 'r',
        "green": 'g',
        "blue": 'b'
    }
    WHITE = WHITES['2deg']['D65']

    EXTENDED_RANGE = True
    BOUNDS = (
        GamutBound(0.0, 1.0, FLG_OPT_PERCENT),
        GamutBound(0.0, 1.0, FLG_OPT_PERCENT),
        GamutBound(0.0, 1.0, FLG_OPT_PERCENT)
    )

    @property
    def r(self) -> float:
        """Adjust red."""

        return self._coords[0]

    @r.setter
    def r(self, value: float) -> None:
        """Adjust red."""

        self._coords[0] = value

    @property
    def g(self) -> float:
        """Adjust green."""

        return self._coords[1]

    @g.setter
    def g(self, value: float) -> None:
        """Adjust green."""

        self._coords[1] = value

    @property
    def b(self) -> float:
        """Adjust blue."""

        return self._coords[2]

    @b.setter
    def b(self, value: float) -> None:
        """Adjust blue."""

        self._coords[2] = value

    @classmethod
    def from_base(cls, coords: Vector) -> Vector:
        """From sRGB Linear to sRGB."""

        return gam_srgb(coords)

    @classmethod
    def to_base(cls, coords: Vector) -> Vector:
        """To sRGB Linear from sRGB."""

        return lin_srgb(coords)
