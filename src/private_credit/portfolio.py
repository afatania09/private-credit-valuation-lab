"""Deterministic synthetic loan portfolio analytics; educational, not IFRS fair value."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Loan:
    loan_id: str
    principal: float
    coupon: float
    maturity_years: int
    market_yield: float
    pd: float
    lgd: float

    def __post_init__(self):
        if not self.loan_id:
            raise ValueError("loan_id is required")
        for name in ("principal", "coupon", "market_yield", "pd", "lgd"):
            value = getattr(self, name)
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        if self.pd > 1 or self.lgd > 1:
            raise ValueError("pd and lgd must be <= 1")
        if isinstance(self.maturity_years, bool) or not isinstance(self.maturity_years, int) or self.maturity_years < 1:
            raise ValueError("maturity_years must be a positive integer")

def value_loan(loan: Loan, yield_shock: float = 0.0) -> float:
    """PV of contractual annual cash flows, ignoring explicit defaults/recoveries."""
    y = loan.market_yield + yield_shock
    if not isfinite(y) or y <= -1:
        raise ValueError("shocked yield must be finite and greater than -100%")
    return sum((loan.principal * loan.coupon + (loan.principal if t == loan.maturity_years else 0)) / (1 + y) ** t for t in range(1, loan.maturity_years + 1))

def portfolio_summary(loans: list[Loan], yield_shock: float = 0.0, pd_multiplier: float = 1.0) -> dict[str, float]:
    """Parallel yield shock and single-period undiscounted expected-loss proxy."""
    if not loans:
        raise ValueError("portfolio must contain loans")
    if not isfinite(pd_multiplier) or pd_multiplier < 0:
        raise ValueError("pd_multiplier must be finite and non-negative")
    if len({x.loan_id for x in loans}) != len(loans):
        raise ValueError("loan IDs must be unique")
    return {
        "principal": sum(x.principal for x in loans),
        "contractual_dcf": sum(value_loan(x, yield_shock) for x in loans),
        "expected_loss_proxy": sum(min(1.0, x.pd * pd_multiplier) * x.lgd * x.principal for x in loans),
        "loan_count": len(loans),
    }
