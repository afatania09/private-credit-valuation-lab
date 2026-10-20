"""Priority of payments for a property collateral enforcement sale.

All amounts in a consistent currency. Educational deterministic waterfall.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class DebtTranche:
    name: str
    balance: float

@dataclass(frozen=True)
class TrancheRecovery:
    name: str
    balance: float
    recovery: float
    loss: float
    recovery_rate: float

@dataclass(frozen=True)
class WaterfallResult:
    gross_sale_proceeds: float
    enforcement_costs: float
    distributable_proceeds: float
    residual_to_equity: float
    tranches: tuple[TrancheRecovery, ...]

def enforcement_waterfall(property_value: float, sale_haircut: float,
                          enforcement_cost_rate: float,
                          tranches: list[DebtTranche]) -> WaterfallResult:
    """Allocate proceeds senior-first in the order supplied.

    All tranches are assumed secured on the same asset and sequentially ranked.
    Pari passu ranking, guarantees, tax priorities and intercreditor agreements
    are not modelled.
    """
    if not all(isfinite(v) for v in (property_value, sale_haircut, enforcement_cost_rate)):
        raise ValueError("nonfinite input")
    if property_value < 0 or not 0 <= sale_haircut <= 1 or not 0 <= enforcement_cost_rate <= 1:
        raise ValueError("invalid sale assumptions")
    if not tranches:
        raise ValueError("at least one tranche required")
    names = set()
    for tranche in tranches:
        if not tranche.name or tranche.name in names:
            raise ValueError("duplicate or empty tranche name")
        names.add(tranche.name)
        if not isfinite(tranche.balance) or tranche.balance < 0:
            raise ValueError("invalid tranche balance")
    sale = property_value * (1 - sale_haircut)
    costs = sale * enforcement_cost_rate
    available = sale - costs
    allocated = []
    for tranche in tranches:
        paid = min(available, tranche.balance)
        available -= paid
        allocated.append(TrancheRecovery(
            tranche.name, tranche.balance, paid, tranche.balance - paid,
            1.0 if tranche.balance == 0 else paid / tranche.balance))
    return WaterfallResult(sale, costs, sale - costs, available, tuple(allocated))
