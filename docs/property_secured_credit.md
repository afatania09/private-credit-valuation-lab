# Property-secured credit: collateral and enforcement

This model links commercial property valuation to credit recovery. It is deliberately **not** a complete property debt fair value or legal enforcement model.

## Core concepts
- **LTV** = outstanding exposure / property market value. A high LTV indicates a thinner collateral cushion, but is not a standalone probability of default.
- **Security priority**: senior-ranking debt and enforcement costs reduce funds available to the modelled lender.
- **Market value versus proceeds**: a hypothetical market value is not guaranteed realisable cash. Timing, vacant possession, tenancy, liquidity, sale costs and enforcement route can matter.
- **Recovery waterfall**: gross collateral sale proceeds less disposal/enforcement costs and prior-ranking claims; the remaining amount is capped at the lender's exposure.
- **Time to recovery**: the model discounts nominal proceeds over a user-defined realization period.
- **Stress**: a proportional haircut tests the sensitivity of recovery to property market declines.

## Worked example (GBP millions)
A lender has exposure 80 against property market value 100. Assumptions: 20% sale haircut, 5% variable costs, 2 fixed costs, and 20 prior-ranking claims. Gross sale = 80; costs = 6; available = 54; lender nominal recovery = 54; nominal loss = 26. If recovery takes two years and the selected discount rate is 10%, present value of recovery = 54 / 1.1^2 = approximately 44.63.

## Professional limitations
Legal enforceability, security perfection, intercreditor agreements, collateral ownership, insolvency priorities, rent roll, tenancy, covenants, property valuation basis and date, loan amortisation, borrower enterprise value, guarantees, recovery uncertainty, and tax are outside this initial model. A real assignment requires evidence and expert judgement. **IFRS 13 fair value and IFRS 9 ECL are separate measurement objectives** and must not be inferred directly from these calculations.

## Suggested future extensions
Income-producing property DCF, net operating income, DSCR, refinance risk, property cap rates, lease expiries, sector/location sensitivities, multiple properties and multiple lender tranches, stochastic recovery timing and legal costs.
