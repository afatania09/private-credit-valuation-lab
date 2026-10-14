import pytest
from private_credit.portfolio import Loan, value_loan, portfolio_summary

def sample():
    return [Loan("A", 60_000_000, .08, 5, .08, .02, .4), Loan("B", 40_000_000, .07, 3, .10, .05, .6)]

def test_principal():
    assert portfolio_summary(sample())["principal"] == 100_000_000

def test_yield_shock():
    assert portfolio_summary(sample(), .02)["contractual_dcf"] < portfolio_summary(sample())["contractual_dcf"]

def test_default_stress():
    assert portfolio_summary(sample(), pd_multiplier=2)["expected_loss_proxy"] > portfolio_summary(sample())["expected_loss_proxy"]

def test_par_loan():
    assert value_loan(sample()[0]) == pytest.approx(60_000_000)

def test_duplicate_ids():
    with pytest.raises(ValueError):
        portfolio_summary([sample()[0], sample()[0]])
