"""Property stress underwriting diagnostics; synthetic screening only."""
from dataclasses import dataclass
from math import isfinite
from private_credit.property_income import PropertyOperatingCase, DebtTerms, dscr, refinance_capacity

@dataclass(frozen=True)
class PropertyScenarioResult:
    noi: float
    cfads: float
    dscr: float
    property_value: float
    ltv: float
    refinance_capacity: float
    refinance_gap: float
    dscr_breach: bool
    ltv_breach: bool

def analyse_property_stress(operating: PropertyOperatingCase, debt: DebtTerms,
                            cap_rate: float, max_ltv: float, min_dscr: float,
                            refinance_debt_constant: float) -> PropertyScenarioResult:
    if not all(isfinite(x) for x in (cap_rate, max_ltv, min_dscr, refinance_debt_constant)):
        raise ValueError("constraints must be finite")
    capacity = refinance_capacity(operating.noi, cap_rate, max_ltv,
                                  operating.cash_available_for_debt_service,
                                  min_dscr, refinance_debt_constant)
    value = capacity["property_value"]
    leverage = debt.outstanding / value if value > 0 else float("inf")
    coverage = dscr(operating, debt)
    available = capacity["refinance_capacity"]
    return PropertyScenarioResult(operating.noi, operating.cash_available_for_debt_service,
                                  coverage, value, leverage, available,
                                  max(0.0, debt.outstanding - available),
                                  coverage < min_dscr, leverage > max_ltv)
