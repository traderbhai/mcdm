from decimal import Decimal

import pytest

from mcdm_app.mcdm.fuzzy_topsis import TriangularFuzzyNumber


def test_absolute_zero_scale():
    with pytest.raises(ValueError):
        TriangularFuzzyNumber(Decimal("-1"), Decimal("2"), Decimal("3"))
    with pytest.raises(ValueError):
        TriangularFuzzyNumber(Decimal("1"), Decimal("-2"), Decimal("3"))
    with pytest.raises(ValueError):
        TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("-3"))


def test_elements_assumptions_scale():
    with pytest.raises(ValueError):
        TriangularFuzzyNumber(Decimal("2"), Decimal("4"), Decimal("3"))
    with pytest.raises(ValueError):
        TriangularFuzzyNumber(Decimal("5"), Decimal("3"), Decimal("4"))


def test_combine():
    assert TriangularFuzzyNumber.combine(
        [
            TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3")),
            TriangularFuzzyNumber(Decimal("0"), Decimal("4"), Decimal("5")),
            TriangularFuzzyNumber(Decimal("0"), Decimal("6"), Decimal("7")),
        ],
        how=None,
    ) == TriangularFuzzyNumber(Decimal("0"), Decimal("4"), Decimal("7"))

    assert TriangularFuzzyNumber.combine(
        [
            TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3")),
            TriangularFuzzyNumber(Decimal("0"), Decimal("4"), Decimal("5")),
            TriangularFuzzyNumber(Decimal("0"), Decimal("6"), Decimal("7")),
        ],
        how="max",
    ) == TriangularFuzzyNumber(Decimal("1"), Decimal("6"), Decimal("7"))

    assert TriangularFuzzyNumber.combine(
        [
            TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3")),
            TriangularFuzzyNumber(Decimal("0"), Decimal("4"), Decimal("5")),
            TriangularFuzzyNumber(Decimal("0"), Decimal("6"), Decimal("7")),
        ],
        how="min",
    ) == TriangularFuzzyNumber(Decimal("0"), Decimal("2"), Decimal("3"))


def test_scalar_multiply():
    assert TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3")) * Decimal("2") == TriangularFuzzyNumber(
        Decimal("2"), Decimal("4"), Decimal("6")
    )


def test_fuzzy_multiply():
    assert TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3")) * TriangularFuzzyNumber(
        Decimal("2"), Decimal("3"), Decimal("4")
    ) == TriangularFuzzyNumber(Decimal("2"), Decimal("6"), Decimal("12"))


def test_scalar_divide():
    assert TriangularFuzzyNumber(Decimal("2"), Decimal("4"), Decimal("6")) / Decimal("2") == TriangularFuzzyNumber(
        Decimal("1"), Decimal("2"), Decimal("3")
    )


def test_fuzzy_divide():
    assert TriangularFuzzyNumber(Decimal("2"), Decimal("6"), Decimal("12")) / TriangularFuzzyNumber(
        Decimal("2"), Decimal("3"), Decimal("4")
    ) == TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3"))


def test_power_positive():
    assert TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3")) ** Decimal("2") == TriangularFuzzyNumber(
        Decimal("1"), Decimal("4"), Decimal("9")
    )


def test_power_negative():
    assert TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("3")) ** Decimal("-2") == TriangularFuzzyNumber(
        Decimal("1") / Decimal("9"), Decimal("1") / Decimal(Decimal("4")), Decimal("1") / Decimal("1")
    )


def test_less_than():
    assert TriangularFuzzyNumber(Decimal("1"), Decimal("4"), Decimal("5")) < TriangularFuzzyNumber(
        Decimal("2"), Decimal("2"), Decimal("2")
    )
    assert not TriangularFuzzyNumber(Decimal("1"), Decimal("4"), Decimal("5")) < TriangularFuzzyNumber(
        Decimal("0"), Decimal("2"), Decimal("2")
    )


def test_greater_than():
    assert TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10")) > TriangularFuzzyNumber(
        Decimal("5"), Decimal("6"), Decimal("7")
    )
    assert not TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10")) > TriangularFuzzyNumber(
        Decimal("5"), Decimal("6"), Decimal("15")
    )


def test_min():
    assert min(
        TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10")),
        TriangularFuzzyNumber(Decimal("5"), Decimal("6"), Decimal("7")),
    ) == TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10"))
    assert min(
        TriangularFuzzyNumber(Decimal("5"), Decimal("6"), Decimal("7")),
        TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10")),
    ) == TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10"))


def test_max():
    assert max(
        TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10")),
        TriangularFuzzyNumber(Decimal("5"), Decimal("6"), Decimal("7")),
    ) == TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10"))
    assert max(
        TriangularFuzzyNumber(Decimal("5"), Decimal("6"), Decimal("7")),
        TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10")),
    ) == TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("10"))


def test_euclidean_distance():
    assert TriangularFuzzyNumber.euclidean_distance(
        TriangularFuzzyNumber(
            Decimal("2"),
            Decimal("2"),
            Decimal("2"),
        ),
        TriangularFuzzyNumber(
            Decimal("0"),
            Decimal("0"),
            Decimal("0"),
        ),
    ) == Decimal("2")
