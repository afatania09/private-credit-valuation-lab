"""Illustrative discrete annual conditional-default survival and recovery valuation.

Assumptions: interest only if surviving to payment date; default during a year
pays recovery at year-end; no accrued coupon on default; fixed recovery fraction
of principal; independent discounting at a credit-risk-free benchmark rate.
Not a calibrated IFRS 13 fair value model or IFRS 9 ECL model.
"""
from math import isfinite

def survival_valuation(principal: float, coupon: float, conditional_pds: list[float],
                       recovery_rate: float, discount_rate: float) -> dict[str, float]:
    if not conditional_pds:
        raise ValueError("at least one year is required")
    for value, label in [(principal, "principal"), (coupon, "coupon"),
                         (recovery_rate, "recovery_rate"), (discount_rate, "discount_rate")]:
        if not isfinite(value) or value < 0:
            raise ValueError(f"{label} must be finite and nonnegative")
    if recovery_rate > 1:
        raise ValueError("recovery_rate must be <= 1")
    if any(not isfinite(p) or p < 0 or p > 1 for p in conditional_pds):
        raise ValueError("conditional_pds must be probabilities in [0,1]")
    survival = 1.0
    pv = 0.0
    expected_default_loss = 0.0
    for year, pd in enumerate(conditional_pds, 1):
        default_probability = survival * pd
        survival *= (1 - pd)
        expected_payment = (survival * principal * coupon
                            + default_probability * principal * recovery_rate)
        if year == len(conditional_pds):
            expected_payment += survival * principal
        pv += expected_payment / (1 + discount_rate) ** year
        expected_default_loss += default_probability * principal * (1 - recovery_rate)
    return {"expected_cash_flow_pv": pv, "survival_to_maturity": survival,
            "undiscounted_principal_loss_proxy": expected_default_loss}
