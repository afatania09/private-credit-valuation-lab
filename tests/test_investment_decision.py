from math import exp
import pytest

from private_credit.investment_decision import (
    CreditInvestment, StressCase, assess_investment, stress_investment,
)


def loan(**updates):
    args = dict(
        principal=100, coupon_rate=.06, maturity_years=3,
        purchase_price=95, discount_rate=.03, recovery_amount=45,
        recovery_lag_years=.5, tenors=(1.0, 3.0), hazards=(.02, .04),
    )
    args.update(updates)
    return CreditInvestment(**args)


def test_no_default_benchmark_and_break_even_coupon():
    asset = loan(hazards=(0, 0), recovery_amount=0, recovery_lag_years=0)
    result = assess_investment(asset)
    expected = sum(6 * exp(-.03 * t) for t in range(1, 4)) + 100 * exp(-.09)
    annuity = sum(100 * exp(-.03 * t) for t in range(1, 4))
    assert result.model_value == pytest.approx(expected)
    assert result.break_even_coupon_rate == pytest.approx(
        (95 - 100 * exp(-.09)) / annuity
    )
    assert result.maturity_default_probability == 0
    assert result.expected_npv == pytest.approx(result.model_value - 95)


def test_stress_repricing_and_decision_gate():
    asset = loan()
    base = assess_investment(asset)
    cases = stress_investment(asset, [
        StressCase("base"),
        StressCase("credit deterioration", 3, .6, .01, 1),
    ])
    assert cases[0].model_value == pytest.approx(base.model_value)
    assert cases[1].model_value < cases[0].model_value
    assert cases[1].default_probability > cases[0].default_probability
    assert assess_investment(asset, minimum_margin_of_safety=.999).decision == "REJECT"


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        assess_investment(loan(purchase_price=0))
    with pytest.raises(ValueError):
        assess_investment(loan(), minimum_margin_of_safety=1)
    with pytest.raises(ValueError):
        stress_investment(loan(), [StressCase("a", hazard_multiplier=-1)])
    with pytest.raises(ValueError):
        stress_investment(loan(), [StressCase("same"), StressCase("same")])
    with pytest.raises(ValueError):
        stress_investment(loan(), [
            StressCase("negative discount", discount_rate_shift=-.1),
        ])
