import pytest
from private_credit.default_cashflows import expected_secured_bullet_pv

def test_zero_default_par_loan():
    r = expected_secured_bullet_pv(100, .05, [0, 0, 0], 40, 1, .05)
    assert r["present_value"] == pytest.approx(100)

def test_certain_default_first_year():
    r = expected_secured_bullet_pv(100, .05, [1, 0], 40, 1, 0)
    assert r["present_value"] == pytest.approx(40)
    assert r["maturity_survival_probability"] == 0

def test_later_recovery_reduces_pv():
    a = expected_secured_bullet_pv(100, .05, [.2, .2], 40, 0, .1)
    b = expected_secured_bullet_pv(100, .05, [.2, .2], 40, 2, .1)
    assert b["present_value"] < a["present_value"]

def test_reject_excess_recovery():
    with pytest.raises(ValueError):
        expected_secured_bullet_pv(100, .05, [.1], 101, 0, .05)
