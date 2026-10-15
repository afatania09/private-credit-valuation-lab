"""Discrete default/recovery cash-flow model for secured bullet loans.

Conditional default probabilities are physical or user-specified; the output is
NOT automatically IFRS 13 fair value or IFRS 9 expected credit loss.
"""
from math import isfinite

def expected_secured_bullet_pv(principal: float, coupon_rate: float,
                               conditional_pds: list[float],
                               recovery_amount: float, recovery_lag_years: float,
                               discount_rate: float) -> dict[str, float]:
    for name, value in [("principal", principal), ("coupon_rate", coupon_rate),
                        ("recovery_amount", recovery_amount),
                        ("recovery_lag_years", recovery_lag_years),
                        ("discount_rate", discount_rate)]:
        if not isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and nonnegative")
    if recovery_amount > principal:
        raise ValueError("recovery_amount cannot exceed principal")
    if not conditional_pds or any(not isfinite(p) or p < 0 or p > 1 for p in conditional_pds):
        raise ValueError("conditional_pds must be a nonempty list of probabilities")
    survival = 1.0
    pv_coupon = pv_principal = pv_recovery = 0.0
    for year, pd in enumerate(conditional_pds, 1):
        default_mass = survival * pd
        survival *= (1 - pd)
        pv_coupon += survival * principal * coupon_rate / (1 + discount_rate) ** year
        pv_recovery += default_mass * recovery_amount / (1 + discount_rate) ** (year + recovery_lag_years)
    pv_principal = survival * principal / (1 + discount_rate) ** len(conditional_pds)
    return {"present_value": pv_coupon + pv_principal + pv_recovery,
            "coupon_pv": pv_coupon, "principal_pv": pv_principal,
            "recovery_pv": pv_recovery, "maturity_survival_probability": survival}
