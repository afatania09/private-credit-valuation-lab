"""Annual fixed-rate fully amortising loan schedules (simplified conventions)."""
from math import isfinite

def level_payment(principal: float, annual_rate: float, years: int) -> float:
    if not isfinite(principal) or principal < 0 or not isfinite(annual_rate) or annual_rate < 0:
        raise ValueError("principal and annual_rate must be finite and nonnegative")
    if isinstance(years, bool) or not isinstance(years, int) or years < 1:
        raise ValueError("years must be a positive integer")
    if annual_rate == 0:
        return principal / years
    return principal * annual_rate / (1 - (1 + annual_rate) ** (-years))

def amortization_schedule(principal: float, annual_rate: float, years: int) -> list[dict[str, float]]:
    payment = level_payment(principal, annual_rate, years)
    outstanding = principal
    rows = []
    for year in range(1, years + 1):
        interest = outstanding * annual_rate
        principal_paid = payment - interest if year < years else outstanding
        principal_paid = min(outstanding, max(0.0, principal_paid))
        cash_flow = interest + principal_paid
        outstanding = max(0.0, outstanding - principal_paid)
        rows.append({"year": year, "interest": interest, "principal": principal_paid,
                     "payment": cash_flow, "balance": outstanding})
    return rows

def schedule_pv(schedule: list[dict[str, float]], yield_rate: float) -> float:
    if not isfinite(yield_rate) or yield_rate <= -1:
        raise ValueError("yield_rate must be finite and > -1")
    return sum(row["payment"] / (1 + yield_rate) ** row["year"] for row in schedule)
