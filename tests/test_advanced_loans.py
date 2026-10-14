import pytest
from private_credit.amortization import amortization_schedule, level_payment, schedule_pv
from private_credit.floating import floating_bullet_cash_flows
from private_credit.credit import survival_valuation

def test_amortizing_par():
    rows = amortization_schedule(1_000_000, .06, 5)
    assert rows[-1]["balance"] == pytest.approx(0)
    assert sum(row["principal"] for row in rows) == pytest.approx(1_000_000)
    assert schedule_pv(rows, .06) == pytest.approx(1_000_000)

def test_zero_interest():
    assert level_payment(1200, 0, 3) == 400

def test_floating_bullet():
    assert floating_bullet_cash_flows(100, [.03, .04], .02) == pytest.approx([5, 106])

def test_no_default_matches_contractual_pv():
    out = survival_valuation(100, .08, [0, 0, 0], .4, .08)
    assert out["expected_cash_flow_pv"] == pytest.approx(100)
    assert out["survival_to_maturity"] == 1

def test_default_reduces_value_with_zero_recovery():
    base = survival_valuation(100, .08, [0, 0, 0], 0, .04)
    stressed = survival_valuation(100, .08, [.2, .2, .2], 0, .04)
    assert stressed["expected_cash_flow_pv"] < base["expected_cash_flow_pv"]

def test_invalid_pd():
    with pytest.raises(ValueError):
        survival_valuation(100, .08, [1.1], .4, .04)
