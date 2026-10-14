"""Transparent educational loan calculations. Annual periods and decimal rates."""
from math import isfinite

def _nonnegative(value: float, label: str) -> float:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{label} must be finite and non-negative")
    return value

def bullet_cash_flows(principal: float, coupon_rate: float, years: int) -> list[float]:
    """Annual coupon payments and principal repaid at maturity."""
    _nonnegative(principal, "principal")
    _nonnegative(coupon_rate, "coupon_rate")
    if isinstance(years, bool) or not isinstance(years, int) or years < 1:
        raise ValueError("years must be a positive integer")
    flows = [principal * coupon_rate for _ in range(years)]
    flows[-1] += principal
    return flows

def present_value(cash_flows: list[float], annual_yield: float) -> float:
    """End-of-year discounting; yield is an annual decimal rate."""
    _nonnegative(annual_yield, "annual_yield")
    if not cash_flows or any(not isfinite(cf) for cf in cash_flows):
        raise ValueError("cash_flows must be a non-empty list of finite values")
    return sum(cf / (1 + annual_yield) ** t for t, cf in enumerate(cash_flows, 1))

def simple_expected_loss(pd: float, lgd: float, ead: float) -> float:
    """Single-horizon undiscounted EL proxy; NOT an IFRS 9 ECL model."""
    for value, label in [(pd, "pd"), (lgd, "lgd")]:
        _nonnegative(value, label)
        if value > 1:
            raise ValueError(f"{label} must not exceed 1")
    _nonnegative(ead, "ead")
    return pd * lgd * ead
