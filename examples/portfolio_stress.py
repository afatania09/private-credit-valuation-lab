"""Synthetic £100m portfolio with independent yield and PD stresses."""
from private_credit.portfolio import Loan, portfolio_summary

loans = [
    Loan("Corporate-A", 60_000_000, .08, 5, .08, .02, .4),
    Loan("Corporate-B", 40_000_000, .07, 3, .10, .05, .6),
]
for label, yield_shock, pd_mult in [("Base", 0, 1), ("Rates +200bp", .02, 1), ("PD doubles", 0, 2)]:
    print(label, portfolio_summary(loans, yield_shock, pd_mult))
