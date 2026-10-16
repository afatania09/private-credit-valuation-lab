"""Survival-weighted secured bullet valuation with exact recovery integration."""
from dataclasses import dataclass
from math import exp, expm1, isfinite
from private_credit.hazard_curves import survival_probability


@dataclass(frozen=True)
class CreditValuation:
    coupon_pv: float
    principal_pv: float
    recovery_pv: float
    present_value: float
    maturity_survival: float


def value_secured_bullet(principal: float, annual_coupon_rate: float,
                         maturity_years: int, tenors: list[float],
                         hazards: list[float], recovery_amount: float,
                         discount_rate: float,
                         recovery_lag_years: float = 0.0) -> CreditValuation:
    """Annual coupons if alive; fixed recovery after default plus lag.

    Externally supplied hazards; not market-calibrated fair value or IFRS 9 ECL.
    Discount rate is assumed credit-risk-free to avoid double counting.
    """
    values = (principal, annual_coupon_rate, recovery_amount,
              discount_rate, recovery_lag_years)
    if not all(isfinite(x) for x in values):
        raise ValueError("inputs must be finite")
    if principal <= 0 or annual_coupon_rate < 0 or not 0 <= recovery_amount <= principal:
        raise ValueError("invalid principal, coupon or recovery")
    if discount_rate < 0 or recovery_lag_years < 0:
        raise ValueError("invalid discount rate or lag")
    if isinstance(maturity_years, bool) or not isinstance(maturity_years, int) or maturity_years < 1:
        raise ValueError("maturity must be a positive integer")
    survival_probability(0, tenors, hazards)
    coupon_pv = sum(principal * annual_coupon_rate *
                    survival_probability(t, tenors, hazards) *
                    exp(-discount_rate * t) for t in range(1, maturity_years + 1))
    survival = survival_probability(maturity_years, tenors, hazards)
    principal_pv = principal * survival * exp(-discount_rate * maturity_years)
    boundaries = [0.0] + [t for t in tenors if t < maturity_years] + [float(maturity_years)]
    recovery_pv = 0.0
    for left, right in zip(boundaries, boundaries[1:]):
        hazard = next((h for end, h in zip(tenors, hazards) if right <= end), hazards[-1])
        combined = hazard + discount_rate
        dt = right - left
        integral = dt if combined == 0 else -expm1(-combined * dt) / combined
        recovery_pv += (recovery_amount * hazard *
                        survival_probability(left, tenors, hazards) *
                        exp(-discount_rate * (left + recovery_lag_years)) * integral)
    total = coupon_pv + principal_pv + recovery_pv
    if not isfinite(total):
        raise ValueError("nonfinite valuation")
    return CreditValuation(coupon_pv, principal_pv, recovery_pv, total, survival)
