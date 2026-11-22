import pytest
from private_credit.portfolio_monitor import (
    CreditExposure, PortfolioShock, monitor_portfolio, stress_portfolio,
)


def sample():
    return [
        CreditExposure("A", "Property", "Group 1", 60, 75, 100, 9, 6, 1.2, .7, .02, .4),
        CreditExposure("B", "Infrastructure", "Group 1", 20, 25, 40, 3, 2, 1.2, .7, .03, .3),
        CreditExposure("C", "Property", "Group 2", 20, 20, 40, 1, 2, 1.2, .7, .05, .6),
    ]


def test_concentrations_and_weighted_loss():
    m = monitor_portfolio(sample())
    assert m.total_outstanding == 100
    assert m.total_undrawn == 20
    assert m.largest_group_share == pytest.approx(.8)
    assert m.sector_shares["Property"] == pytest.approx(.8)
    assert m.expected_loss_proxy == pytest.approx(60*.02*.4 + 20*.03*.3 + 20*.05*.6)
    assert m.exposures[2].covenant_flags == ("DSCR",)


def test_stress_triggers_covenants_and_higher_loss():
    cases = stress_portfolio(sample(), [
        PortfolioShock("Base"),
        PortfolioShock("Recession", .4, .4, 2, .2),
    ])
    assert cases[0].increase_over_base == pytest.approx(0)
    assert cases[1].expected_loss_proxy > cases[0].expected_loss_proxy
    assert set(cases[1].breached_exposures) == {"A", "B", "C"}
    assert cases[1].aggregate_collateral_coverage == pytest.approx(1.08)


def test_invalid_exposures_and_shocks():
    with pytest.raises(ValueError):
        monitor_portfolio([])
    with pytest.raises(ValueError):
        monitor_portfolio(sample() + [sample()[0]])
    with pytest.raises(ValueError):
        monitor_portfolio([CreditExposure(
            "Bad", "Property", "G", 100, 50, 100, 1, 1, 1.2, .7, .02, .5)])
    with pytest.raises(ValueError):
        stress_portfolio(sample(), [PortfolioShock("bad", collateral_haircut=1.1)])
