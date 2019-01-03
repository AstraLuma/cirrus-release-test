from ppb_vector import Vector2
from pytest import raises # type: ignore
from math import sqrt
from utils import units, lengths, vectors
from hypothesis import assume, event, given, note, example
from hypothesis.strategies import floats


@given(x=vectors(), abs_tol=floats(min_value=0), rel_tol=floats(min_value=0))
def test_isclose_to_self(x, abs_tol, rel_tol):
    assert x.isclose(x, abs_tol=abs_tol, rel_tol=rel_tol)


EPSILON = 1e-8

@given(x=vectors(), direction=units(), abs_tol=lengths())
def test_isclose_abs_error(x, direction, abs_tol):
    """Test x.isclose(rel_tol=0) near the boundary between “close” and “not close”

    - x + (1 - ε) * abs_tol * direction should always be close
    - x + (1 + ε) * abs_tol * direction should not be close
      assuming it isn't equal to x (because of rounding, or because x is null)
    """
    error = abs_tol * direction
    note(f"error = {error}")

    positive = x + (1 - sqrt(EPSILON)) * error
    note(f"positive example: {positive} = x + {positive - x}")
    assert x.isclose(positive, abs_tol=abs_tol, rel_tol=0)

    if abs_tol > EPSILON * x.length:
        negative = x + (1 + sqrt(EPSILON)) * error
        event("Negative example generated (abs_tol > ε * |x|)")
        note(f"negative example: {negative} = x + {negative - x}")
        assert not x.isclose(negative, abs_tol=abs_tol, rel_tol=0)


@given(x=vectors(max_magnitude=1e30), direction=units(),
       rel_tol=floats(min_value=EPSILON, max_value=1-sqrt(EPSILON)))
@example(x=Vector2(0.5030575955800033, 4183.540331936798), direction=Vector2(-0.21080691603913568, -0.97752772039982), rel_tol=1.0000044626502047e-08)
@example(x=Vector2(0.336348726648339, 4183.540331936798), direction=Vector2(-0.2108069159366941, -0.9775277204219119), rel_tol=1.0000009102918328e-08)
def test_isclose_rel_error(x, direction, rel_tol):
    """Test x.isclose(abs_tol=0) near the boundary between “close” and “not close”

    - x + (1 - ε) * |x| * rel_tol * direction should always be close
    - In many cases, we should be able to generate an example that isn't close
    """
    assume(x.length > EPSILON)
    note(f"|x| = {x.length}")
    error = rel_tol * direction

    positive = x + (1 - sqrt(EPSILON)) * x.length * error
    note(f"positive example: {positive} = x + {positive - x} ="
         f"x + {(positive - x).length / x.length} * |x| * direction")

    assert x.isclose(positive, abs_tol=0, rel_tol=rel_tol)

    # In x.isclose(negative), the allowed relative error is relative to |x|
    # and |negative|, so the acceptable errors grow larger as negative does.
    #
    # The choice of negative accounts for this, with the (1 - rel_tol) term:
    # we have negative = x + Δ, and we want to pick Δ such that
    # δ = |x - negative| > rel_tol * max(|x|, |negative|)
    #
    # Since r * (|x| + δ) > rel_tol * max(|x|, |negative|), any choice where
    # δ > rel_tol * (|x| + δ) is suitable. The smallest is
    # rel_tol |x| / (1 - rel_tol), as such, we take
    # Δ = r * |x| * direction / (1 - rel_tol), and an ε safety margin.
    negative = x + (1 + sqrt(EPSILON)) / (1 - rel_tol) * x.length * error
    note(f"negative example: {negative} = x + {negative - x} = "
         f"x + {(negative - x).length / x.length} * |x| * direction")

    assert not x.isclose(negative, abs_tol=0, rel_tol=rel_tol)


def test_isclose_negative_tolerances():
    zero = Vector2(0, 0)

    with raises(ValueError):
        zero.isclose(zero, abs_tol=-1)

    with raises(ValueError):
        zero.isclose(zero, rel_tol=-1)
