import pytest
from private_credit.collateral import PropertySecurity, property_recovery, collateral_stress

def test_full_recovery_and_ltv():
    r = property_recovery(60, PropertySecurity(100))
    assert r["nominal_recovery"] == 60
    assert r["ltv"] == pytest.approx(.6)
    assert r["nominal_loss"] == 0

def test_enforcement_waterfall():
    s = PropertySecurity(market_value=100, senior_claims=20,
                         enforcement_cost_rate=.05, fixed_enforcement_cost=2,
                         haircut=.20, realization_years=2)
    r = property_recovery(80, s, .10)
    # sale=80, costs=6, senior=20, available=54
    assert r["distributable_proceeds"] == pytest.approx(54)
    assert r["nominal_recovery"] == pytest.approx(54)
    assert r["discounted_recovery"] == pytest.approx(54 / 1.1**2)
    assert r["nominal_loss"] == pytest.approx(26)

def test_stress_reduces_recovery():
    s = PropertySecurity(100, senior_claims=10)
    assert collateral_stress(90, s, .3)["nominal_recovery"] < property_recovery(90, s)["nominal_recovery"]

def test_zero_property_value():
    r = property_recovery(50, PropertySecurity(0))
    assert r["nominal_recovery"] == 0
    assert r["ltv"] == float("inf")

def test_invalid_haircut():
    with pytest.raises(ValueError):
        PropertySecurity(100, haircut=1.2)
