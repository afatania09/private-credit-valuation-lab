"""Deterministic portfolio covenant, concentration and credit stress monitoring.

All currency amounts are in the same user-supplied unit. No accounting or
regulatory capital claims are made.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class CreditExposure:
    name: str
    sector: str
    borrower_group: str
    outstanding: float
    commitment: float
    collateral_value: float
    annual_cfads: float
    annual_debt_service: float
    minimum_dscr: float
    maximum_ltv: float
    annual_pd: float
    lgd: float


@dataclass(frozen=True)
class ExposureMetrics:
    name: str
    dscr: float
    ltv: float
    undrawn: float
    covenant_flags: tuple[str, ...]
    expected_loss_proxy: float


@dataclass(frozen=True)
class PortfolioMetrics:
    total_outstanding: float
    total_commitments: float
    total_undrawn: float
    weighted_annual_pd: float
    weighted_lgd: float
    expected_loss_proxy: float
    largest_group_share: float
    sector_shares: dict[str, float]
    exposures: tuple[ExposureMetrics, ...]


@dataclass(frozen=True)
class PortfolioShock:
    name: str
    collateral_haircut: float = 0.0
    cfads_haircut: float = 0.0
    pd_multiplier: float = 1.0
    lgd_addition: float = 0.0


@dataclass(frozen=True)
class PortfolioStress:
    name: str
    expected_loss_proxy: float
    increase_over_base: float
    breached_exposures: tuple[str, ...]
    aggregate_collateral_coverage: float


def _valid(exposures: list[CreditExposure]) -> None:
    if not exposures:
        raise ValueError("at least one exposure required")
    names = set()
    for e in exposures:
        if not e.name or e.name in names or not e.sector or not e.borrower_group:
            raise ValueError("unique names, sector and borrower group required")
        names.add(e.name)
        nums = (e.outstanding, e.commitment, e.collateral_value, e.annual_cfads,
                e.annual_debt_service, e.minimum_dscr, e.maximum_ltv,
                e.annual_pd, e.lgd)
        if not all(isfinite(v) for v in nums):
            raise ValueError("nonfinite exposure input")
        if not (0 < e.outstanding <= e.commitment and e.collateral_value >= 0
                and e.annual_cfads >= 0 and e.annual_debt_service > 0
                and e.minimum_dscr > 0 and e.maximum_ltv > 0
                and 0 <= e.annual_pd <= 1 and 0 <= e.lgd <= 1):
            raise ValueError("invalid exposure terms")


def _metrics(e: CreditExposure, shock: PortfolioShock) -> ExposureMetrics:
    collateral = e.collateral_value * (1 - shock.collateral_haircut)
    cfads = e.annual_cfads * (1 - shock.cfads_haircut)
    dscr = cfads / e.annual_debt_service
    ltv = e.outstanding / collateral if collateral else float("inf")
    flags = []
    if dscr < e.minimum_dscr:
        flags.append("DSCR")
    if ltv > e.maximum_ltv:
        flags.append("LTV")
    pd = min(1.0, e.annual_pd * shock.pd_multiplier)
    lgd = min(1.0, e.lgd + shock.lgd_addition)
    return ExposureMetrics(e.name, dscr, ltv, e.commitment - e.outstanding,
                           tuple(flags), e.outstanding * pd * lgd)


def _validate_shock(s: PortfolioShock) -> None:
    if not s.name or not all(isfinite(v) for v in (
        s.collateral_haircut, s.cfads_haircut, s.pd_multiplier, s.lgd_addition
    )):
        raise ValueError("invalid shock")
    if not (0 <= s.collateral_haircut <= 1 and 0 <= s.cfads_haircut <= 1
            and s.pd_multiplier >= 0 and 0 <= s.lgd_addition <= 1):
        raise ValueError("invalid shock bounds")


def monitor_portfolio(exposures: list[CreditExposure]) -> PortfolioMetrics:
    _valid(exposures)
    base = PortfolioShock("Base")
    rows = tuple(_metrics(e, base) for e in exposures)
    total = sum(e.outstanding for e in exposures)
    groups: dict[str, float] = {}
    sectors: dict[str, float] = {}
    for e in exposures:
        groups[e.borrower_group] = groups.get(e.borrower_group, 0) + e.outstanding
        sectors[e.sector] = sectors.get(e.sector, 0) + e.outstanding
    return PortfolioMetrics(
        total, sum(e.commitment for e in exposures),
        sum(e.commitment - e.outstanding for e in exposures),
        sum(e.outstanding * e.annual_pd for e in exposures) / total,
        sum(e.outstanding * e.lgd for e in exposures) / total,
        sum(r.expected_loss_proxy for r in rows),
        max(groups.values()) / total,
        {sector: amount / total for sector, amount in sorted(sectors.items())},
        rows,
    )


def stress_portfolio(
    exposures: list[CreditExposure], shocks: list[PortfolioShock]
) -> tuple[PortfolioStress, ...]:
    _valid(exposures)
    if not shocks or len({s.name for s in shocks}) != len(shocks):
        raise ValueError("unique, nonempty shocks required")
    base = monitor_portfolio(exposures).expected_loss_proxy
    output = []
    total = sum(e.outstanding for e in exposures)
    for shock in shocks:
        _validate_shock(shock)
        rows = [_metrics(e, shock) for e in exposures]
        loss = sum(r.expected_loss_proxy for r in rows)
        output.append(PortfolioStress(
            shock.name, loss, loss - base,
            tuple(r.name for r in rows if r.covenant_flags),
            sum(e.collateral_value * (1 - shock.collateral_haircut)
                for e in exposures) / total,
        ))
    return tuple(output)
