import pytest
from private_credit.recovery_waterfall import DebtTranche, enforcement_waterfall

def test_senior_paid_before_mezzanine():
    result = enforcement_waterfall(100, .2, .1,
                                   [DebtTranche("senior", 60), DebtTranche("mezz", 30)])
    assert result.distributable_proceeds == pytest.approx(72)
    assert result.tranches[0].recovery == pytest.approx(60)
    assert result.tranches[1].recovery == pytest.approx(12)
    assert result.tranches[1].loss == pytest.approx(18)

def test_surplus_to_equity():
    result = enforcement_waterfall(200, 0, 0, [DebtTranche("senior", 60)])
    assert result.residual_to_equity == pytest.approx(140)

def test_total_loss():
    result = enforcement_waterfall(0, 0, 0, [DebtTranche("senior", 50)])
    assert result.tranches[0].loss == pytest.approx(50)

def test_reject_invalid_haircut():
    with pytest.raises(ValueError):
        enforcement_waterfall(100, 1.1, 0, [DebtTranche("senior", 50)])

def test_reject_duplicate_names():
    with pytest.raises(ValueError):
        enforcement_waterfall(100, 0, 0, [DebtTranche("x", 50), DebtTranche("x", 20)])
