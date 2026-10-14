"""Simplified property-secured credit recovery waterfall.

All figures are monetary amounts at a common valuation date unless explicitly
discounted. A gross collateral value is NOT itself a loan recovery.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class PropertySecurity:
    market_value: float
    senior_claims: float = 0.0
    enforcement_cost_rate: float = 0.0
    fixed_enforcement_cost: float = 0.0
    haircut: float = 0.0
    realization_years: float = 0.0

    def __post_init__(self):
        for name in ("market_value", "senior_claims", "enforcement_cost_rate",
                     "fixed_enforcement_cost", "haircut", "realization_years"):
            v = getattr(self, name)
            if not isfinite(v) or v < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.enforcement_cost_rate > 1 or self.haircut > 1:
            raise ValueError("rates must be <= 1")

def property_recovery(exposure: float, security: PropertySecurity,
                      discount_rate: float = 0.0) -> dict[str, float]:
    """Recovery net of haircut, costs, senior claims, capped at exposure.

    No additional recoveries, guarantees, legal priorities or tax effects modelled.
    """
    if not isfinite(exposure) or exposure < 0:
        raise ValueError("exposure must be finite and nonnegative")
    if not isfinite(discount_rate) or discount_rate <= -1:
        raise ValueError("discount_rate must be finite and > -100%")
    gross_sale = security.market_value * (1 - security.haircut)
    costs = gross_sale * security.enforcement_cost_rate + security.fixed_enforcement_cost
    distributable = max(0.0, gross_sale - costs - security.senior_claims)
    nominal_recovery = min(exposure, distributable)
    discounted_recovery = nominal_recovery / (1 + discount_rate) ** security.realization_years
    return {
        "gross_sale_proceeds": gross_sale,
        "enforcement_costs": costs,
        "distributable_proceeds": distributable,
        "nominal_recovery": nominal_recovery,
        "discounted_recovery": discounted_recovery,
        "nominal_loss": exposure - nominal_recovery,
        "recovery_fraction": nominal_recovery / exposure if exposure else 0.0,
        "ltv": exposure / security.market_value if security.market_value else float("inf") if exposure else 0.0,
    }

def collateral_stress(exposure: float, security: PropertySecurity,
                      additional_haircut: float, discount_rate: float = 0.0) -> dict[str, float]:
    """Apply an additional proportional decline to the already haircut sale value."""
    if not isfinite(additional_haircut) or not 0 <= additional_haircut <= 1:
        raise ValueError("additional_haircut must be in [0,1]")
    stressed = PropertySecurity(
        market_value=security.market_value,
        senior_claims=security.senior_claims,
        enforcement_cost_rate=security.enforcement_cost_rate,
        fixed_enforcement_cost=security.fixed_enforcement_cost,
        haircut=1 - (1 - security.haircut) * (1 - additional_haircut),
        realization_years=security.realization_years,
    )
    return property_recovery(exposure, stressed, discount_rate)
