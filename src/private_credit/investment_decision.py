"""Investment committee analytics for a survival-weighted private-credit bullet loan.

Educational underwriting aid, not market-calibrated fair value or IFRS 9 ECL.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from math import isfinite

from .credit_valuation import value_secured_bullet


@dataclass(frozen=True)
class CreditInvestment:
    principal: float
    coupon_rate: float
    maturity_years: int
    purchase_price: float
    discount_rate: float
    recovery_amount: float
    recovery_lag_years: float
    tenors: tuple[float, ...]
    hazards: tuple[float, ...]


@dataclass(frozen=True)
class InvestmentDecision:
    purchase_price: float
    model_value: float
    margin_of_safety: float
    margin_of_safety_pct: float
    expected_npv: float
    price_per_100_par: float
    break_even_coupon_rate: float
    maturity_default_probability: float
    expected_annual_credit_loss_proxy: float
    decision: str


@dataclass(frozen=True)
class StressCase:
    name: str
    hazard_multiplier: float = 1.0
    recovery_multiplier: float = 1.0
    discount_rate_shift: float = 0.0
    recovery_lag_addition: float = 0.0


@dataclass(frozen=True)
class StressResult:
    name: str
    model_value: float
    npv: float
    downside_from_base: float
    default_probability: float


def _value(investment: CreditInvestment, case: StressCase | None = None):
    if not isfinite(investment.purchase_price) or investment.purchase_price <= 0:
        raise ValueError("purchase_price must be positive and finite")
    if len(investment.tenors) != len(investment.hazards) or not investment.tenors:
        raise ValueError("a nonempty, aligned hazard curve is required")
    case = case or StressCase("Base")
    inputs = (case.hazard_multiplier, case.recovery_multiplier,
              case.discount_rate_shift, case.recovery_lag_addition)
    if not all(isfinite(x) for x in inputs):
        raise ValueError("stress inputs must be finite")
    if case.hazard_multiplier < 0 or not 0 <= case.recovery_multiplier <= 1:
        raise ValueError("invalid hazard/recovery multiplier")
    if case.recovery_lag_addition < 0:
        raise ValueError("additional enforcement lag must be nonnegative")
    return value_secured_bullet(
        principal=investment.principal,
        annual_coupon_rate=investment.coupon_rate,
        maturity_years=investment.maturity_years,
        tenors=list(investment.tenors),
        hazards=[h * case.hazard_multiplier for h in investment.hazards],
        recovery_amount=investment.recovery_amount * case.recovery_multiplier,
        discount_rate=investment.discount_rate + case.discount_rate_shift,
        recovery_lag_years=investment.recovery_lag_years + case.recovery_lag_addition,
    )


def assess_investment(
    investment: CreditInvestment, *, minimum_margin_of_safety: float = 0.0,
) -> InvestmentDecision:
    """Compare survival-adjusted discounted receipts against purchase price.

    Break-even coupon floors at zero because negative coupons are excluded.
    Annual loss proxy is NOT IFRS 9 ECL.
    """
    if not isfinite(minimum_margin_of_safety) or not 0 <= minimum_margin_of_safety < 1:
        raise ValueError("minimum_margin_of_safety must lie in [0, 1)")
    result = _value(investment)
    zero_value = _value(replace(investment, coupon_rate=0.0)).present_value
    unit_value = _value(replace(investment, coupon_rate=1.0)).present_value
    coupon_annuity = unit_value - zero_value
    break_even = max(0.0, (investment.purchase_price - zero_value) / coupon_annuity)
    model_value = result.present_value
    safety = model_value - investment.purchase_price
    safety_pct = safety / model_value if model_value > 0 else float("-inf")
    probability = 1 - result.maturity_survival
    annual_loss_proxy = (
        probability * (investment.principal - investment.recovery_amount)
        / investment.maturity_years
    )
    decision = "PASS" if safety_pct >= minimum_margin_of_safety else "REJECT"
    return InvestmentDecision(
        investment.purchase_price, model_value, safety, safety_pct, safety,
        100 * investment.purchase_price / investment.principal, break_even,
        probability, annual_loss_proxy, decision,
    )


def stress_investment(
    investment: CreditInvestment, cases: list[StressCase],
) -> list[StressResult]:
    """Reprice the same asset under deterministic credit/rate scenarios."""
    base = _value(investment)
    if (not cases or len({case.name for case in cases}) != len(cases)
            or any(not case.name for case in cases)):
        raise ValueError("at least one uniquely named scenario is required")
    output = []
    for case in cases:
        value = _value(investment, case)
        output.append(StressResult(
            name=case.name,
            model_value=value.present_value,
            npv=value.present_value - investment.purchase_price,
            downside_from_base=base.present_value - value.present_value,
            default_probability=1 - value.maturity_survival,
        ))
    return output
