from math import exp
import pytest
from private_credit.credit_valuation import value_secured_bullet


def test_zero_default_contractual_value():
    result = value_secured_bullet(100, .05, 2, [2], [0], 40, .03)
    expected = 5*exp(-.03) + 105*exp(-.06)
    assert result.present_value == pytest.approx(expected)


def test_piecewise_recovery_probability_at_zero_discount():
    result = value_secured_bullet(100, 0, 2, [1, 2], [.1, .2], 40, 0)
    assert result.recovery_pv == pytest.approx(40*(1-exp(-.3)))
    assert result.principal_pv == pytest.approx(100*exp(-.3))


def test_recovery_lag_reduces_value():
    a = value_secured_bullet(100, .05, 2, [2], [.1], 40, .05, 0)
    b = value_secured_bullet(100, .05, 2, [2], [.1], 40, .05, 2)
    assert b.present_value < a.present_value
