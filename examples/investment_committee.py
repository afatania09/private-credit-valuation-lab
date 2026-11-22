"""Run: python examples/investment_committee.py"""
from private_credit.investment_decision import (
    CreditInvestment, StressCase, assess_investment, stress_investment,
)

investment = CreditInvestment(
    principal=10_000_000, coupon_rate=.105, maturity_years=5,
    purchase_price=9_600_000, discount_rate=.045,
    recovery_amount=5_500_000, recovery_lag_years=1.0,
    tenors=(1, 3, 5), hazards=(.025, .04, .06),
)
assessment = assess_investment(investment, minimum_margin_of_safety=.05)
print("SYNTHETIC INVESTMENT COMMITTEE SCREEN — NOT INVESTMENT ADVICE")
print(f"Model value: GBP {assessment.model_value:,.0f}")
print(f"Acquisition price: GBP {assessment.purchase_price:,.0f}")
print(f"NPV: GBP {assessment.expected_npv:,.0f}")
print(f"Margin of safety: {assessment.margin_of_safety_pct:.2%}")
print(f"Break-even coupon: {assessment.break_even_coupon_rate:.2%}")
print(f"Default probability to maturity: {assessment.maturity_default_probability:.2%}")
print(f"Committee screen: {assessment.decision}")
print("\nCredit stress matrix")
for row in stress_investment(investment, [
    StressCase("Base"),
    StressCase("Recession", 1.75, .85, .01, .5),
    StressCase("Severe downturn", 3, .6, .025, 1.5),
]):
    print(
        f"{row.name:20s} value=GBP {row.model_value:,.0f} "
        f"NPV=GBP {row.npv:,.0f} default={row.default_probability:.1%}"
    )
