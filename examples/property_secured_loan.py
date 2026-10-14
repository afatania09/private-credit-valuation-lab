"""Synthetic commercial-property-backed loan. Figures in GBP millions."""
from private_credit.collateral import PropertySecurity, property_recovery, collateral_stress

security = PropertySecurity(
    market_value=100,
    senior_claims=15,
    enforcement_cost_rate=.04,
    fixed_enforcement_cost=1,
    haircut=.10,
    realization_years=2,
)
for name, result in [
    ("Base", property_recovery(70, security, .08)),
    ("Property values -25%", collateral_stress(70, security, .25, .08)),
]:
    print(name)
    for key, value in result.items():
        print(f"  {key}: {value:.4f}")
