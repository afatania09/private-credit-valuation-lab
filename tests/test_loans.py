import pytest
from private_credit.loans import bullet_cash_flows, present_value, simple_expected_loss

def test_par_loan_when_coupon_equals_yield():
    flows = bullet_cash_flows(10_000_000, 0.08, 5)
    assert present_value(flows, 0.08) == pytest.approx(10_000_000)

def test_loan_below_par_when_market_yield_rises():
    flows = bullet_cash_flows(10_000_000, 0.08, 5)
    assert present_value(flows, 0.12) < 10_000_000

def test_expected_loss_proxy():
    assert simple_expected_loss(0.02, 0.4, 1_000_000) == pytest.approx(8000)

def test_invalid_inputs():
    with pytest.raises(ValueError):
        bullet_cash_flows(-1, 0.08, 5)
    with pytest.raises(ValueError):
        present_value([100], -0.02)
    with pytest.raises(ValueError):
        simple_expected_loss(1.2, 0.4, 100)
