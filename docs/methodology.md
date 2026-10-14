# Modelling methodology and boundaries

## Fixed amortisation
For annual coupon rate r, maturity n and principal P, the level payment is
A = P r / (1 - (1+r)^(-n)); if r=0, A=P/n.
At each payment date: interest = opening balance × r, principal paid = payment - interest.

## Floating rates
A forward path is explicitly supplied. Annual interest is principal × (reference rate + contractual margin), with an optional floor on the reference rate. No day-count convention, compounding, fixing lag, curve bootstrapping or discounting curve is implied.

## Conditional default model
Conditional PD q_t is the probability of default in year t given survival to the start of that year. S_t = product from i=1 to t of (1-q_i). Marginal default probability in year t is S_(t-1) × q_t. Surviving borrowers pay coupon at year-end; defaults receive a fraction of principal at year-end. Final principal is paid only by survivors. All expected cash flows are discounted at an independently supplied benchmark rate.

**Caution:** This is a simplified risk-neutral-style expected cash flow construction with *user-specified*, not market-calibrated, probabilities. Historical/physical PDs cannot simply be inserted and called fair value. Realistic IFRS 13 valuations need market-participant calibration, liquidity, recovery timing and additional contractual features. IFRS 9 ECL requires appropriate probability-weighted cash shortfalls, time value of money, forward-looking scenarios, staging and original effective interest rate conventions, as applicable.

## Next validation steps
Compare loan cash-flow schedules against independent spreadsheet examples; add day counts, irregular dates, prepayments, revolving facilities, forward curves, covenant effects and collateral-specific recovery timing. No production-grade model claims.
