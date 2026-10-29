import math
from numbers import Real


def validate_coord(name: str, value, low: float, high: float) -> float:
    # bool is a subclass of int in Python, so True would otherwise pass as 1
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f'{name} must be a number, got {type(value).__name__}')
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    if not low <= value <= high:
        raise ValueError(f'{name} must be between {low} and {high}, got {value}')
    return value