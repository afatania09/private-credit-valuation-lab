"""Educational discounted scenario-weighted expected credit loss model."""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class ECLScenario:
    name: str
    weight: float
    annual_conditional_pds: tuple[float, ...]
    exposure_at_default: tuple[float, ...]
    loss_given_default: tuple[float, ...]


@dataclass(frozen=True)
class ECLResult:
    stage: int
    expected_credit_loss: float
    scenario_losses: dict[str, float]
    year_contributions: tuple[float, ...]


def discounted_ecl(scenarios: list[ECLScenario],
                   original_effective_interest_rate: float,
                   stage: int) -> ECLResult:
    """Discrete annual PD x EAD x LGD shortfalls discounted at original EIR.

    Stage 1 counts defaults in the first year; stages 2 and 3 use the full
    supplied horizon. Stage 3 here is a label only: credit-impaired interest
    accounting and SICR assessment are out of scope. This is not an IFRS 9
    compliant implementation.
    """
    if isinstance(stage, bool) or stage not in (1, 2, 3):
        raise ValueError("stage must be 1, 2 or 3")
    if not isfinite(original_effective_interest_rate) or original_effective_interest_rate <= -1:
        raise ValueError("invalid original EIR")
    if not scenarios:
        raise ValueError("at least one scenario required")
    horizon = len(scenarios[0].annual_conditional_pds)
    if not horizon:
        raise ValueError("empty PD term structure")
    names = set()
    weights = []
    for scenario in scenarios:
        if not scenario.name or scenario.name in names:
            raise ValueError("scenario names must be unique")
        names.add(scenario.name)
        if not isfinite(scenario.weight) or not 0 <= scenario.weight <= 1:
            raise ValueError("invalid scenario weight")
        weights.append(scenario.weight)
        if any(len(v) != horizon for v in (scenario.annual_conditional_pds,
                                            scenario.exposure_at_default,
                                            scenario.loss_given_default)):
            raise ValueError("inconsistent scenario horizons")
        if any(not isfinite(x) or not 0 <= x <= 1 for x in scenario.annual_conditional_pds):
            raise ValueError("invalid conditional PD")
        if any(not isfinite(x) or x < 0 for x in scenario.exposure_at_default):
            raise ValueError("invalid EAD")
        if any(not isfinite(x) or not 0 <= x <= 1 for x in scenario.loss_given_default):
            raise ValueError("invalid LGD")
    if abs(sum(weights) - 1) > 1e-10:
        raise ValueError("scenario weights must sum to one")
    contributions = [0.0] * horizon
    scenario_losses = {}
    for scenario in scenarios:
        survival = 1.0
        loss = 0.0
        for i, (pd, ead, lgd) in enumerate(zip(scenario.annual_conditional_pds,
                                                scenario.exposure_at_default,
                                                scenario.loss_given_default)):
            default_mass = survival * pd
            survival *= 1 - pd
            if stage == 1 and i > 0:
                continue
            shortfall = default_mass * ead * lgd / (1 + original_effective_interest_rate) ** (i + 1)
            contributions[i] += scenario.weight * shortfall
            loss += shortfall
        scenario_losses[scenario.name] = loss
    total = sum(contributions)
    if not isfinite(total):
        raise ValueError("nonfinite ECL")
    return ECLResult(stage, total, scenario_losses, tuple(contributions))
