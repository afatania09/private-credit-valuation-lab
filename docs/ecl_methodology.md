# Stage 4: Discounted expected credit loss prototype

This module calculates a **simplified** annual, scenario-weighted credit-loss
proxy, not a complete IFRS 9 expected credit loss implementation.

For each scenario and year, marginal default probability equals survival
to the beginning of the year times the conditional PD during that year.
The discounted shortfall is:

`marginal_PD[t] * EAD[t] * LGD[t] / (1 + original_EIR)**t`

Results are weighted by scenario probability, which must sum to one.

- **Stage 1:** includes defaults occurring in the first 12 months only,
  with loss severity intended to represent the cash shortfall resulting
  from those defaults; it is **not** just 12 months of missed payments.
- **Stage 2:** includes defaults over the full supplied remaining life.
- **Stage 3:** uses the same lifetime shortfall proxy but **does not**
  implement credit-impaired asset measurement, net-basis interest revenue,
  purchased-or-originated-credit-impaired treatment, or cure mechanics.

Important exclusions: independent SICR/staging assessment; forward-looking
scenario construction and calibration; recoveries occurring after default;
time-varying contractual shortfalls beyond the PD/EAD/LGD approximation;
EIR modification and floating-rate EIR conventions; collateral dependency,
prepayment, write-offs, discounting to the precise cash shortfall date,
and reconciliation to accounting ledgers.

This module must **not** be represented as an IFRS 9-compliant ECL engine.
It is distinct from IFRS 13 market-participant fair value: physical PD
assumptions and original EIR should not be conflated with market-implied
hazard rates or fair-value discount curves.

Example:

```python
from private_credit.ecl import ECLScenario, discounted_ecl
base = ECLScenario("base", 0.7, (0.02, 0.03), (1e6, 1e6), (0.4, 0.4))
downside = ECLScenario("downside", 0.3, (0.05, 0.08), (1e6, 1e6), (0.6, 0.6))
print(discounted_ecl([base, downside], 0.06, stage=2))
```

Run `pytest -q tests/test_ecl.py`. GitHub Actions remains manual-only.
