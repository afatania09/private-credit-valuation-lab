"""Integrated, deterministic property-backed credit screening.

NOT a calibrated PD model, credit rating, IFRS 9 ECL, or IFRS 13 fair value.
A breach is a screening flag, not proof of borrower default.
"""
from dataclasses import dataclass
from math import isfinite
from .property_income import (
    PropertyOperatingCase, DebtTerms, dscr, refinance_capacity,
)
from .collateral import PropertySecurity, property_recovery

@dataclass(frozen=True)
class UnderwritingScenario:
    name: str
    property_case: PropertyOperatingCase
    debt: DebtTerms
    capitalization_rate: float
    maximum_refinance_ltv: float
    minimum_refinance_dscr: float
    refinance_debt_constant: float
    covenant_minimum_dscr: float
    collateral_haircut: float = 0.0
    senior_claims: float = 0.0
    enforcement_cost_rate: float = 0.0
    fixed_enforcement_cost: float = 0.0
    realization_years: float = 0.0
    recovery_discount_rate: float = 0.0

    def __post_init__(self):
        if not self.name:
            raise ValueError("scenario name is required")
        if not isfinite(self.covenant_minimum_dscr) or self.covenant_minimum_dscr <= 0:
            raise ValueError("covenant_minimum_dscr must be positive and finite")

def assess_scenario(s: UnderwritingScenario) -> dict:
    """Return underwriting signals, refinancing gap and hypothetical enforcement recovery.

    Collateral recovery is a *conditional default* scenario and should not be
    subtracted from a performing-loan DCF as though default were certain.
    """
    cfads = s.property_case.cash_available_for_debt_service
    capacity = refinance_capacity(
        s.property_case.noi, s.capitalization_rate, s.maximum_refinance_ltv,
        cfads, s.minimum_refinance_dscr, s.refinance_debt_constant,
    )
    coverage = dscr(s.property_case, s.debt)
    collateral = PropertySecurity(
        market_value=capacity["property_value"],
        senior_claims=s.senior_claims,
        enforcement_cost_rate=s.enforcement_cost_rate,
        fixed_enforcement_cost=s.fixed_enforcement_cost,
        haircut=s.collateral_haircut,
        realization_years=s.realization_years,
    )
    recovery = property_recovery(
        s.debt.outstanding, collateral, s.recovery_discount_rate
    )
    shortfall = max(0.0, s.debt.outstanding - capacity["refinance_capacity"])
    return {
        "scenario": s.name,
        "noi": s.property_case.noi,
        "cfads": cfads,
        "dscr": coverage,
        "covenant_breach": coverage < s.covenant_minimum_dscr,
        "property_value": capacity["property_value"],
        "ltv": recovery["ltv"],
        "refinance_capacity": capacity["refinance_capacity"],
        "refinance_shortfall": shortfall,
        "refinance_gap_flag": shortfall > 0,
        "conditional_nominal_recovery": recovery["nominal_recovery"],
        "conditional_discounted_recovery": recovery["discounted_recovery"],
        "conditional_nominal_loss": recovery["nominal_loss"],
    }

def assess_scenarios(scenarios: list[UnderwritingScenario]) -> list[dict]:
    if not scenarios:
        raise ValueError("at least one scenario required")
    if len({s.name for s in scenarios}) != len(scenarios):
        raise ValueError("scenario names must be unique")
    return [assess_scenario(s) for s in scenarios]
