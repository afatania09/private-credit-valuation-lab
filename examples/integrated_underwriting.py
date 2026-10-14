"""Synthetic £70m secured loan: base and stressed underwriting assessment."""
from private_credit.property_income import PropertyOperatingCase, DebtTerms
from private_credit.underwriting import UnderwritingScenario, assess_scenarios

debt = DebtTerms(70_000_000, .06, 1_000_000)
scenarios = [
    UnderwritingScenario(
        name=name,
        property_case=PropertyOperatingCase(10_000_000, vacancy, 2_000_000, 500_000),
        debt=debt,
        capitalization_rate=cap_rate,
        maximum_refinance_ltv=.65,
        minimum_refinance_dscr=1.3,
        refinance_debt_constant=.09,
        covenant_minimum_dscr=1.2,
        collateral_haircut=.2,
        senior_claims=10_000_000,
        enforcement_cost_rate=.05,
        realization_years=2,
        recovery_discount_rate=.08,
    )
    for name, vacancy, cap_rate in [("Base", .10, .07), ("Stress", .30, .09)]
]
for result in assess_scenarios(scenarios):
    print("\n", result.pop("scenario"))
    for key, value in result.items():
        print(f"{key}: {value:,.3f}" if isinstance(value, float) else f"{key}: {value}")
