"""Simple annual-reset floating rate bullet loan, using an explicit forward-rate path."""
from math import isfinite

def floating_bullet_cash_flows(principal: float, forward_rates: list[float], margin: float,
                               floor: float | None = None) -> list[float]:
    if not isfinite(principal) or principal < 0 or not isfinite(margin):
        raise ValueError("invalid principal or margin")
    if not forward_rates or any(not isfinite(r) for r in forward_rates):
        raise ValueError("nonempty finite forward rate path required")
    if floor is not None and not isfinite(floor):
        raise ValueError("floor must be finite")
    result = []
    for rate in forward_rates:
        reference = max(rate, floor) if floor is not None else rate
        coupon = reference + margin
        if coupon < 0:
            raise ValueError("negative coupon unsupported in this model")
        result.append(principal * coupon)
    result[-1] += principal
    return result
