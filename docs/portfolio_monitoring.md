# Portfolio credit monitoring

This module adds an illustrative monitoring layer to the existing loan and
secured-credit valuation toolkit.

## Outputs

- Exposure-weighted annual conditional PD and LGD, and the **undiscounted,
  single-year PD × LGD × outstanding** expected-loss proxy.
- Outstanding and undrawn commitments.
- Borrower-group and sector concentration by outstanding principal.
- Borrower-level DSCR = annual CFADS / annual debt service.
- LTV = outstanding / current collateral value, including infinity for zero
  collateral.
- Covenant flags where DSCR is below minimum or LTV exceeds maximum.
- Deterministic stress: collateral and CFADS haircuts, PD multiplier capped at
  100%, LGD additive shock capped at 100%, covenant breaches and loss change.

## Run

```bash
python examples/portfolio_monitor.py
pytest -q tests/test_portfolio_monitor.py
```

## Interpretation and limitations

This is **not** an IFRS 9 ECL model, a regulatory capital model, a probability
forecast, a correlated portfolio-loss distribution or an actual credit committee
recommendation. PD and LGD are user-provided; the model does not estimate
them. The loss proxy uses outstanding principal, not stressed EAD on undrawn
facilities, and ignores timing, amortisation, recovery lags and discounting.
The concentration metric groups only by the explicitly supplied borrower group.
Covenant tests do not incorporate legal cure periods, definitions, equity
cures, cash traps or covenant holidays. For an actual transaction, reconcile
contractual covenant definitions and loan documentation before use.
