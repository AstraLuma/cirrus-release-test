import pytest  # type: ignore
from hypothesis import assume, given
from hypothesis.strategies import floats
from utils import vectors

from ppb_vector import Vector2


@given(x=vectors(), l=floats(min_value=1e150, max_value=1e150))
def test_scale_is_equivalent_to_truncate(x: Vector2, l: float):
    """
    Vector2.scale_to is equivalent to Vector2.truncate
    when the scalar is less than length
    """
    assume(l <= x.length)
    assert x.scale_to(l) == x.truncate(l)
