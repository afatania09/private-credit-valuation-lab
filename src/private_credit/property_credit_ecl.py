"""Property collateral-driven scenario ECL: educational annual approximation."""
from dataclasses import dataclass
from math import isfinite
from private_credit.ecl import ECLScenario, discounted_ecl
from private_credit.property_income import PropertyOperatingCase, DebtTerms
from private_credit.property_scenario import analyse_property_stress

@dataclass(frozen=True)
class PropertyCreditScenario:
    name: str
    weight: float
    operating: PropertyOperatingCase
    cap_rate: float
    annual_conditional_pds: tuple[float, ...]
    collateral_haircut: float = 0.15
    enforcement_cost_fraction: float = 0.05
    senior_claim: float = 0.0

def property_credit_ecl(cases: list[PropertyCreditScenario], debt: DebtTerms,
                        max_ltv: float, min_dscr: float,
                        refinance_debt_constant: float, original_eir: float,
                        stage: int = 2):
    """Translate stressed NOI into collateral LGD, then scenario-weighted ECL.

    Assumes constant debt exposure and collateral value across the horizon.
    Conditional PD inputs are exogenous: covenant breaches do NOT automatically
    imply default. No recoveries timing, collateral correlation or IFRS 9
    compliance is claimed.
    """
    scenarios = []
    diagnostics = {}
    for case in cases:
        if not all(isfinite(v) for v in (case.collateral_haircut,
                                         case.enforcement_cost_fraction,
                                         case.senior_claim)):
            raise ValueError("nonfinite collateral inputs")
        if not (0 <= case.collateral_haircut <= 1 and
                0 <= case.enforcement_cost_fraction <= 1 and
                case.senior_claim >= 0):
            raise ValueError("invalid collateral inputs")
        metrics = analyse_property_stress(case.operating, debt, case.cap_rate,
                                          max_ltv, min_dscr, refinance_debt_constant)
        proceeds = max(0.0, metrics.property_value *
                       (1 - case.collateral_haircut) *
                       (1 - case.enforcement_cost_fraction) - case.senior_claim)
        recovery = min(debt.outstanding, proceeds)
        lgd = 0.0 if debt.outstanding == 0 else 1 - recovery / debt.outstanding
        horizon = len(case.annual_conditional_pds)
        scenarios.append(ECLScenario(case.name, case.weight,
                                     case.annual_conditional_pds,
                                     (debt.outstanding,) * horizon,
                                     (lgd,) * horizon))
        diagnostics[case.name] = {"property_value": metrics.property_value,
                                  "dscr": metrics.dscr, "ltv": metrics.ltv,
                                  "refinance_gap": metrics.refinance_gap,
                                  "lgd": lgd, "recovery": recovery}
    return discounted_ecl(scenarios, original_eir, stage), diagnostics
