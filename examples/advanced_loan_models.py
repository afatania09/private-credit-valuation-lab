from private_credit.amortization import amortization_schedule, schedule_pv
from private_credit.floating import floating_bullet_cash_flows
from private_credit.credit import survival_valuation

rows = amortization_schedule(5_000_000, .075, 5)
print("Amortising loan PV at 9%:", round(schedule_pv(rows, .09), 2))
print("Floating loan annual cash flows:", floating_bullet_cash_flows(5_000_000, [.04, .035, .03], .035))
print("Survival-weighted loan:", survival_valuation(5_000_000, .08, [.02, .03, .04], .4, .04))
