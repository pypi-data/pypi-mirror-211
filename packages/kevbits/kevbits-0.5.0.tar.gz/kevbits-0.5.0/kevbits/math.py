"""
Operations with angles.
"""

from math import pi


Degree = pi / 180
Hour = pi / 12
ArcMin = Degree / 60
ArcSec = ArcMin / 60


def closest_mod(x: float, target: float, modulo: float):
    """
    Add or subtract modulo to x (possible several times) to achieve
    minimal distance from the target.
    """
    assert modulo > 0.0
    return x + round((target - x) / modulo) * modulo


def closest_mod_pi(x: float, target: float):
    "See closest_mod() function."
    return closest_mod(x, target, pi)


def closest_mod_2pi(x: float, target: float):
    "See closest_mod() function."
    return closest_mod(x, target, 2 * pi)
