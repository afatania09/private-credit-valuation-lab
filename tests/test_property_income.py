import math
import pytest
from private_credit.property_income import (
    PropertyOperatingCase, DebtTerms, dscr, interest_coverage,
    income_capitalization, refinance_capacity,
)

def test_operating_case_and_dscr():
    p = PropertyOperatingCase(10_000_000, .10, 2_000_000, 500_000)
    d = DebtTerms(70_000_000, .06, 1_000_000)
    assert p.noi == pytest.approx(7_000_000)
    assert p.cash_available_for_debt_service == pytest.approx(6_500_000)
    assert d.annual_debt_service == pytest.approx(5_200_000)
    assert dscr(p, d) == pytest.approx(1.25)
    assert interest_coverage(p, d) == pytest.approx(7 / 4.2)

def test_capitalization_and_refinance_binding_dscr():
    r = refinance_capacity(noi=7_000_000, cap_rate=.07, max_ltv=.65,
                           cfads=6_500_000, min_dscr=1.3, annual_debt_constant=.09)
    assert r["property_value"] == pytest.approx(100_000_000)
    assert r["ltv_limit"] == pytest.approx(65_000_000)
    assert r["dscr_limit"] == pytest.approx(6_500_000 / (.117))
    assert r["refinance_capacity"] == pytest.approx(r["dscr_limit"])

def test_vacancy_stress_reduces_dscr():
    debt = DebtTerms(70_000_000, .06, 1_000_000)
    base = PropertyOperatingCase(10_000_000, .1, 2_000_000, 500_000)
    stress = PropertyOperatingCase(10_000_000, .3, 2_000_000, 500_000)
    assert dscr(stress, debt) < dscr(base, debt)

def test_zero_service_is_not_misreported_as_finite():
    p = PropertyOperatingCase(100, 0, 0)
    assert math.isinf(dscr(p, DebtTerms(0, 0)))

def test_validation():
    with pytest.raises(ValueError):
        PropertyOperatingCase(100, 1.1, 0)
    with pytest.raises(ValueError):
        income_capitalization(100, 0)
    with pytest.raises(ValueError):
        DebtTerms(100, .05, 101)
