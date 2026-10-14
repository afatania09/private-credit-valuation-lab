"""Synthetic commercial property cash-flow and loan covenant analysis.

Annual convention, GBP nominal amounts. This is a screening tool, not a
property valuation, lender covenant opinion or IFRS fair-value model.
"""
from dataclasses import dataclass
from math import isfinite

def _nonnegative(value: float, label: str) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{label} must be finite and nonnegative")

@dataclass(frozen=True)
class PropertyOperatingCase:
    gross_potential_rent: float
    vacancy_rate: float
    operating_costs: float
    recurring_capex: float = 0.0

    def __post_init__(self):
        for label in ("gross_potential_rent", "vacancy_rate", "operating_costs", "recurring_capex"):
            _nonnegative(getattr(self, label), label)
        if self.vacancy_rate > 1:
            raise ValueError("vacancy_rate must be <= 1")

    @property
    def effective_gross_income(self) -> float:
        return self.gross_potential_rent * (1 - self.vacancy_rate)

    @property
    def noi(self) -> float:
        """NOI excludes financing and recurring capex."""
        return self.effective_gross_income - self.operating_costs

    @property
    def cash_available_for_debt_service(self) -> float:
        """Simplified CFADS proxy = NOI less recurring capex."""
        return self.noi - self.recurring_capex

@dataclass(frozen=True)
class DebtTerms:
    outstanding: float
    annual_interest_rate: float
    scheduled_annual_principal: float = 0.0

    def __post_init__(self):
        for label in ("outstanding", "annual_interest_rate", "scheduled_annual_principal"):
            _nonnegative(getattr(self, label), label)
        if self.scheduled_annual_principal > self.outstanding:
            raise ValueError("scheduled principal cannot exceed outstanding")

    @property
    def annual_debt_service(self) -> float:
        return self.outstanding * self.annual_interest_rate + self.scheduled_annual_principal

def dscr(case: PropertyOperatingCase, debt: DebtTerms) -> float:
    """CFADS / annual scheduled debt service; infinity if zero service and positive CFADS."""
    service = debt.annual_debt_service
    if service == 0:
        return float("inf") if case.cash_available_for_debt_service > 0 else float("nan")
    return case.cash_available_for_debt_service / service

def interest_coverage(case: PropertyOperatingCase, debt: DebtTerms) -> float:
    """NOI / annual interest; undefined where annual interest is zero."""
    interest = debt.outstanding * debt.annual_interest_rate
    return case.noi / interest if interest else float("nan")

def income_capitalization(noi: float, cap_rate: float) -> float:
    """Simplified direct capitalization using stabilised annual NOI."""
    if not isfinite(noi) or not isfinite(cap_rate) or cap_rate <= 0:
        raise ValueError("NOI must be finite and cap_rate positive")
    return noi / cap_rate

def refinance_capacity(noi: float, cap_rate: float, max_ltv: float,
                       cfads: float, min_dscr: float, annual_debt_constant: float) -> dict[str, float]:
    """Minimum of collateral LTV and DSCR debt capacity, before transaction costs."""
    for v, label in [(max_ltv, "max_ltv"), (min_dscr, "min_dscr"),
                     (annual_debt_constant, "annual_debt_constant")]:
        if not isfinite(v) or v <= 0:
            raise ValueError(f"{label} must be positive and finite")
    if max_ltv > 1:
        raise ValueError("max_ltv must not exceed 1")
    if not isfinite(cfads):
        raise ValueError("cfads must be finite")
    property_value = income_capitalization(noi, cap_rate)
    ltv_limit = max(0.0, property_value * max_ltv)
    dscr_limit = max(0.0, cfads / (min_dscr * annual_debt_constant))
    return {"property_value": property_value, "ltv_limit": ltv_limit,
            "dscr_limit": dscr_limit, "refinance_capacity": min(ltv_limit, dscr_limit)}
