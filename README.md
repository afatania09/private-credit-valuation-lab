# Private Credit Valuation Lab

A public, educational Python toolkit for private credit valuation and credit-risk analysis.

> **Development status: early-stage prototype.** Models have not undergone independent professional validation. Do not use for investment, accounting or regulatory decisions.

## Implemented
- Fixed-rate annual-pay bullet-loan cash-flow schedules
- Discounted cash-flow present values at specified yields
- Simple PD × LGD × EAD expected-loss illustration
- Automated unit tests and worked example

## Run locally
```bash
python -m pip install -e ".[dev]"
pytest -q
python examples/basic_loan.py
```

## Model boundaries
The DCF model discounts *contractual* cash flows at an externally supplied rate. It is not automatically an IFRS 13 fair value model: market-participant credit, liquidity, calibration and other relevant factors must be considered. The PD × LGD × EAD calculation is a single-horizon undiscounted teaching proxy, **not** a complete IFRS 9 expected-credit-loss implementation. Avoid double counting credit risk in both expected cash flows and the discount rate.

## Planned research stages
1. Amortising, floating-rate and irregular-date loans
2. Yield/spread sensitivity, duration and convexity
3. Default timing, hazard curves, recovery waterfalls
4. IFRS 9 staging and discounted expected cash shortfalls
5. Distressed loans, collateral and real estate-backed credit
6. Portfolio stress testing, reporting and independent benchmark validation

## Project principles
Transparent formulas, synthetic data, reproducible tests, documented assumptions, conservative CI spending, and clear distinctions between prototypes and independently validated models.

## Reference standards
- [IFRS 9 Financial Instruments](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/)
- [IFRS 13 Fair Value Measurement](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-13-fair-value-measurement/)

MIT licence.