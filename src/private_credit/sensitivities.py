"""Deterministic discounted-cash-flow spread and rate sensitivity.

Educational parallel-shift analytics for *contractual* cash flows, not a
market-calibrated fair-value or credit-spread model.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite


@dataclass(frozen=True)
class SensitivityResult:
    present_value: float
    macaulay_duration: float
    modified_duration: float
    convexity: float
    dv01: float
    spread01: float
    up_100bp: float
    down_100bp: float


def cashflow_sensitivities(
    cashflows: list[tuple[float, float]],
    base_zero_rates: list[float],
    *,
    spread: float = 0.0,
    bump: float = 0.0001,
) -> SensitivityResult:
    """Price cash flows with continuously compounded spot rates plus a flat spread.

    Each (time_years, amount) has a corresponding continuously compounded zero
    rate. DV01 and spread01 are PV losses for a +1bp parallel rate/spread move.
    Modified duration and convexity are analytic derivatives w.r.t. a parallel
    continuously compounded shift; negative cash flows are supported, but
    duration is undefined for nonpositive PV.
    """
    if not cashflows or len(cashflows) != len(base_zero_rates):
        raise ValueError("cashflows and base_zero_rates must be nonempty and equal length")
    if not isfinite(spread) or not isfinite(bump) or bump <= 0:
        raise ValueError("spread must be finite and bump positive and finite")
    weighted = []
    for (time, amount), rate in zip(cashflows, base_zero_rates):
        if not all(isfinite(x) for x in (time, amount, rate)) or time < 0:
            raise ValueError("finite cash flows/rates and nonnegative times required")
        weighted.append((time, amount * exp(-(rate + spread) * time)))
    pv = sum(v for _, v in weighted)
    if pv <= 0 or not isfinite(pv):
        raise ValueError("positive finite present value required for duration")
    first = sum(t * v for t, v in weighted)
    second = sum(t * t * v for t, v in weighted)

    def price(shift: float) -> float:
        return sum(v * exp(-shift * t) for t, v in weighted)

    # A +1bp shift in the base curve and in the flat spread are algebraically
    # identical in this simple model. Report both for interpretability, not
    # as independent risk factors to be summed.
    pv_up_bp = price(0.0001)
    return SensitivityResult(
        present_value=pv,
        macaulay_duration=first / pv,
        modified_duration=first / pv,
        convexity=second / pv,
        dv01=pv - pv_up_bp,
        spread01=pv - pv_up_bp,
        up_100bp=price(0.01),
        down_100bp=price(-0.01),
    )
