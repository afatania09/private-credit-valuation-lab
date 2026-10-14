"""Property cash flow, covenant and refinancing stress; synthetic GBP amounts."""
from private_credit.property_income import (
    PropertyOperatingCase, DebtTerms, dscr, refinance_capacity
)

debt = DebtTerms(70_000_000, .06, 1_000_000)
for label, vacancy, cap_rate in [
    ("Base", .10, .07),
    ("Stress: vacancy 30%, cap rate 9%", .30, .09),
]:
    property_case = PropertyOperatingCase(10_000_000, vacancy, 2_000_000, 500_000)
    capacity = refinance_capacity(
        property_case.noi, cap_rate, .65,
        property_case.cash_available_for_debt_service, 1.3, .09
    )
    print(label)
    print("NOI:", round(property_case.noi))
    print("DSCR:", round(dscr(property_case, debt), 3))
    print("Implied property value:", round(capacity["property_value"]))
    print("Refinance capacity:", round(capacity["refinance_capacity"]))
    print("Refinancing shortfall:", round(max(0, debt.outstanding - capacity["refinance_capacity"])))
