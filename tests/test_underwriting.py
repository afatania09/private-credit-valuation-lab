import pytest
from private_credit.property_income import PropertyOperatingCase, DebtTerms
from private_credit.underwriting import UnderwritingScenario, assess_scenario, assess_scenarios

def scenario(name="base", vacancy=.10, cap_rate=.07):
    return UnderwritingScenario(
        name=name,
        property_case=PropertyOperatingCase(10_000_000, vacancy, 2_000_000, 500_000),
        debt=DebtTerms(70_000_000, .06, 1_000_000),
        capitalization_rate=cap_rate,
        maximum_refinance_ltv=.65,
        minimum_refinance_dscr=1.3,
        refinance_debt_constant=.09,
        covenant_minimum_dscr=1.2,
        collateral_haircut=.2,
        senior_claims=10_000_000,
        enforcement_cost_rate=.05,
        realization_years=2,
        recovery_discount_rate=.08,
    )

def test_base_case_refinance_gap_but_no_dscr_breach():
    r = assess_scenario(scenario())
    assert r["dscr"] == pytest.approx(1.25)
    assert r["covenant_breach"] is False
    assert r["refinance_gap_flag"] is True
    assert r["refinance_shortfall"] == pytest.approx(70_000_000 - 6_500_000 / (.09 * 1.3))

def test_stress_weakens_metrics():
    base, stress = assess_scenarios([scenario(), scenario("stress", .30, .09)])
    assert stress["dscr"] < base["dscr"]
    assert stress["property_value"] < base["property_value"]
    assert stress["conditional_nominal_recovery"] <= base["conditional_nominal_recovery"]
    assert stress["covenant_breach"] is True

def test_duplicate_scenarios_rejected():
    with pytest.raises(ValueError):
        assess_scenarios([scenario(), scenario()])

def test_no_automatic_default_inference():
    result = assess_scenario(scenario())
    assert "default_probability" not in result
    assert "fair_value" not in result
