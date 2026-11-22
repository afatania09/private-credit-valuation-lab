"""Synthetic portfolio covenant and stress dashboard."""
from private_credit.portfolio_monitor import (
    CreditExposure, PortfolioShock, monitor_portfolio, stress_portfolio,
)

portfolio = [
    CreditExposure("Office Loan", "Real Estate", "Sponsor A", 60e6, 70e6,
                   100e6, 9e6, 6e6, 1.25, .70, .025, .40),
    CreditExposure("Energy Loan", "Infrastructure", "Sponsor B", 25e6, 30e6,
                   45e6, 5e6, 3e6, 1.20, .75, .015, .30),
    CreditExposure("Logistics Loan", "Real Estate", "Sponsor A", 15e6, 20e6,
                   22e6, 2e6, 1.5e6, 1.20, .75, .035, .45),
]
report = monitor_portfolio(portfolio)
print("SYNTHETIC PORTFOLIO MONITOR — EDUCATIONAL ONLY")
print(f"Outstanding: GBP {report.total_outstanding:,.0f}")
print(f"Undrawn commitments: GBP {report.total_undrawn:,.0f}")
print(f"Largest borrower-group share: {report.largest_group_share:.1%}")
print(f"One-year PD x LGD x EAD proxy: GBP {report.expected_loss_proxy:,.0f}")
for item in report.exposures:
    print(f"{item.name}: DSCR={item.dscr:.2f}x LTV={item.ltv:.1%} "
          f"flags={','.join(item.covenant_flags) or 'none'}")
for result in stress_portfolio(portfolio, [
    PortfolioShock("Base"),
    PortfolioShock("Recession", .2, .25, 2, .1),
    PortfolioShock("Severe", .4, .4, 3, .2),
]):
    print(f"{result.name}: loss proxy GBP {result.expected_loss_proxy:,.0f}, "
          f"breaches={','.join(result.breached_exposures) or 'none'}")
