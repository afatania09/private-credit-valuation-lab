import pytest
from private_credit.property_income import PropertyOperatingCase, DebtTerms
from private_credit.property_credit_ecl import PropertyCreditScenario, property_credit_ecl

def test_recession_increases_loss():
    debt = DebtTerms(70, .06, 0)
    base = PropertyCreditScenario("base", .7, PropertyOperatingCase(10, .1, 2, .5),
                                  .07, (.02, .03))
    downside = PropertyCreditScenario("downside", .3, PropertyOperatingCase(10, .4, 2, .5),
                                      .10, (.10, .15))
    result, detail = property_credit_ecl([base, downside], debt, .65, 1.3, .09, .06, 2)
    assert result.expected_credit_loss > 0
    assert detail["downside"]["lgd"] > detail["base"]["lgd"]
    assert detail["downside"]["refinance_gap"] >= detail["base"]["refinance_gap"]

def test_full_collateral_coverage_zero_ecl():
    debt = DebtTerms(20, .05)
    case = PropertyCreditScenario("base", 1, PropertyOperatingCase(10, 0, 1),
                                  .05, (.2,), 0, 0)
    result, detail = property_credit_ecl([case], debt, .7, 1.2, .08, .05)
    assert result.expected_credit_loss == pytest.approx(0)
    assert detail["base"]["lgd"] == 0

def test_senior_claim_worsens_lgd():
    debt = DebtTerms(70, .06)
    op = PropertyOperatingCase(10, .1, 2)
    a = PropertyCreditScenario("a", 1, op, .1, (.1,), .1, .05, 0)
    b = PropertyCreditScenario("b", 1, op, .1, (.1,), .1, .05, 20)
    _, x = property_credit_ecl([a], debt, .7, 1.2, .08, .05)
    _, y = property_credit_ecl([b], debt, .7, 1.2, .08, .05)
    assert y["b"]["lgd"] > x["a"]["lgd"]

def test_invalid_haircut():
    debt = DebtTerms(20, .05)
    bad = PropertyCreditScenario("bad", 1, PropertyOperatingCase(10, 0, 1),
                                 .05, (.1,), 1.1)
    with pytest.raises(ValueError):
        property_credit_ecl([bad], debt, .7, 1.2, .08, .05)
