"""Independent closed-form and finite-difference sensitivity checks."""
from math import exp

import pytest

from private_credit.sensitivities import cashflow_sensitivities


def test_single_zero_coupon_matches_analytic_duration_and_convexity():
    result = cashflow_sensitivities([(3.0, 100.0)], [0.04], spread=0.01)
    assert result.present_value == pytest.approx(100 * exp(-0.15))
    assert result.modified_duration == pytest.approx(3.0)
    assert result.macaulay_duration == pytest.approx(3.0)
    assert result.convexity == pytest.approx(9.0)
    assert result.dv01 == pytest.approx(result.present_value * (1 - exp(-0.0003)))


def test_multiple_cashflows_bump_matches_price_change():
    flows = [(1, 5), (2, 5), (3, 105)]
    rates = [0.02, 0.03, 0.04]
    r = cashflow_sensitivities(flows, rates)
    bumped = cashflow_sensitivities(flows, [x + 0.0001 for x in rates])
    assert r.dv01 == pytest.approx(r.present_value - bumped.present_value)
    assert r.spread01 == pytest.approx(r.dv01)
    assert r.down_100bp > r.present_value > r.up_100bp
    assert r.convexity > 0


def test_zero_time_cashflow_has_zero_sensitivity():
    r = cashflow_sensitivities([(0, 100)], [0.03])
    assert r.present_value == pytest.approx(100)
    assert r.modified_duration == pytest.approx(0)
    assert r.dv01 == pytest.approx(0)


@pytest.mark.parametrize("flows,rates", [
    ([], []),
    ([(1, 100)], []),
    ([(-1, 100)], [0.03]),
    ([(1, float("nan"))], [0.03]),
    ([(1, -100)], [0.03]),
])
def test_invalid_inputs(flows, rates):
    with pytest.raises(ValueError):
        cashflow_sensitivities(flows, rates)


def test_invalid_bump():
    with pytest.raises(ValueError):
        cashflow_sensitivities([(1, 100)], [0.03], bump=0)
