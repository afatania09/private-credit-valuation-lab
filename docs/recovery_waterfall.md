# Multi-tranche enforcement waterfall

`enforcement_waterfall` models a collateral sale and allocates net proceeds
to creditors in their specified seniority order.

For example, a property worth 100 with a 20% sale haircut and 10% costs
on realised sale proceeds leaves 72 available. Senior debt of 60 recovers
60; mezzanine debt of 30 recovers 12 and loses 18.

Inputs are assumed to share the same currency and valuation date.
Enforcement costs are assessed on sale proceeds after the haircut.
The output includes gross sale proceeds, costs, distributable proceeds,
tranche recoveries and losses, and any residual for equity.

The waterfall is deliberately deterministic. It does not yet account for
pari passu classes, tax or insolvency priorities, legal enforcement timing,
guarantees, additional collateral, intercreditor agreements, or discounting
of delayed distributions. These matters can materially change recoveries.

Run `pytest -q tests/test_recovery_waterfall.py` locally.
