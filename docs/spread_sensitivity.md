# Parallel rate and spread sensitivity (educational)

The module `private_credit.sensitivities` adds independently testable,
continuously compounded zero-curve DCF analytics for contractual cash flows.

For cash flow `CF_i` at year `t_i`, with continuously compounded zero
rate `z_i` and flat spread `s`:

`PV = sum(CF_i * exp(-(z_i + s) * t_i))`

Analytic modified duration under a parallel shift is
`sum(t_i * PV_i) / PV`; convexity is `sum(t_i^2 * PV_i) / PV`.
DV01 and spread01 are the **loss of PV** for a positive 1bp shift
(`PV(0) - PV(+0.0001)`). The 100bp scenarios report the bumped PVs.

## Important limitations

- Times are year fractions **supplied by the caller**; no date/day-count
  calculations are implied.
- Rates use continuous compounding; this is not the standard street
  convention for all loan instruments.
- The module uses fixed contractual cash flows, not default-weighted,
  option-adjusted, callable, floating-rate-reset, or stochastic cash flows.
- A parallel base-curve shift and a flat-spread shift have identical
  numerical effects in this model: **DV01 and spread01 must not be added**
  as if they were independent sensitivities.
- The reported duration is the continuous-compounding modified duration;
  the `macaulay_duration` field is numerically equal under this convention.
- No market spread calibration, liquidity adjustment, IFRS 13 fair-value
  conclusion, or IFRS 9 ECL is inferred.
- Negative cash flows are allowed if total PV remains positive; unusual
  cash-flow signs can make duration/convexity nonstandard.

## Example

```python
from private_credit.sensitivities import cashflow_sensitivities

result = cashflow_sensitivities(
    [(1, 5), (2, 5), (3, 105)],
    [0.03, 0.032, 0.035],
    spread=0.02,
)
print(result)
```

Run `pytest -q tests/test_sensitivities.py` locally. GitHub Actions are
manual-only to avoid unrequested compute costs.
