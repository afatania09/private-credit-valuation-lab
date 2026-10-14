# Integrated secured-credit underwriting — methodology

This module links the previously separate **property income**, **refinancing capacity** and **collateral recovery** calculations. It is a *screening analysis*, not an estimate of borrower default probability, IFRS 9 ECL or IFRS 13 fair value.

## Decision sequence
1. Forecast gross rent, vacancy, operating expenses and recurring capital expenditure.
2. Derive NOI and a simplified cash flow available for debt service (CFADS).
3. Compare CFADS with scheduled annual debt service (DSCR) and a user-supplied covenant threshold.
4. Capitalize stabilised NOI using an assumed cap rate to obtain an indicative property value.
5. Calculate new-debt borrowing limits under **both** maximum LTV and minimum DSCR; take the binding limit.
6. Calculate the gap between outstanding debt and refinancing capacity.
7. **Separately**, simulate a hypothetical default/enforcement outcome: sale haircut, costs, senior claims, exposure cap and recovery delay.

## Interpretation
A covenant breach, negative refinancing gap, and actual default are different events. A refinancing shortfall does not automatically mean the loan will default; sponsor equity, extension, sale, refinancing on different terms or restructuring may resolve it. Recovery estimates are conditional on enforcement and must not be added to or subtracted from contractual loan valuations without a coherent probability-weighted model.

## Data needed before professional use
Rent roll, lease events, property sector/location evidence, cap-rate support, borrower financial statements, debt terms, security perfection, intercreditor waterfall, covenants, enforceability, property-specific exit costs, actual interest-rate forward curves and stress calibration. Independently review assumptions and independently benchmark results.

## Reproducibility
Run `python examples/integrated_underwriting.py`. Tests: `pytest -q`. All figures are synthetic.
