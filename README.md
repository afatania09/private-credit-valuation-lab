# Private Credit Valuation Lab

A public, educational Python toolkit for private credit valuation and credit-risk analysis.

> **Development status: early-stage prototype.** Models have not undergone independent professional validation. Do not use for investment, accounting or regulatory decisions.

## Implemented
- Fixed-rate annual-pay bullet-loan cash-flow schedules and discounted cash-flow values
- Fully amortising annual-payment loan schedules and present values
- Floating-rate bullet-loan cash flows using an explicit forward-rate path
- Conditional default/survival and simplified recovery-weighted cash-flow valuation
- Synthetic £100m portfolio aggregation, yield and PD sensitivity scenarios
- Property-secured loan recovery waterfall: LTV, haircuts, costs, senior claims and discounted recoveries
- Simple PD × LGD × EAD expected-loss illustration
- Automated unit tests, worked examples and [methodology notes](docs/methodology.md)

- Property income and refinancing: NOI, CFADS proxy, DSCR, interest coverage, direct capitalisation and LTV/DSCR borrowing constraints
- Collateral recovery: security priority, sale haircuts, enforcement costs and recovery timing

- Integrated secured-credit underwriting: NOI, DSCR covenant flag, refinance gap and conditional enforcement recovery

## Run locally
```bash
python -m pip install -e ".[dev]"
pytest -q
python examples/basic_loan.py
python examples/portfolio_stress.py
python examples/advanced_loan_models.py
python examples/property_secured_loan.py
python examples/property_income_stress.py
python examples/integrated_underwriting.py
python examples/property_secured_loan.py
```

## Model boundaries
The DCF model discounts *contractual* cash flows at an externally supplied rate. It is not automatically an IFRS 13 fair value model: market-participant credit, liquidity, calibration and other relevant factors must be considered. The PD × LGD × EAD calculation is a single-horizon undiscounted teaching proxy, **not** a complete IFRS 9 expected-credit-loss implementation. Avoid double counting credit risk in both expected cash flows and the discount rate.

## Planned research stages
1. Irregular-date cash flows, day-count conventions and SONIA forward/discount curves
2. Yield/spread sensitivity, duration and convexity
3. Hazard-curve calibration and collateral recovery waterfalls
4. IFRS 9 staging and discounted expected cash shortfalls
5. Real estate cash-flow modelling, refinance risk and multi-tranche security waterfalls
6. Portfolio reporting and independent benchmark validation

## Specialist case study
[Property-secured credit methodology](docs/property_secured_credit.md) connects commercial property values to collateral recovery and enforcement stress scenarios. This is a simplified educational recovery model, not a property appraisal or IFRS valuation opinion.

## Property-backed credit case studies
- [Collateral and enforcement methodology](docs/property_secured_credit.md)
- [Income, covenant and refinancing methodology](docs/property_income_methodology.md)

## Integrated underwriting case study
[Methodology and interpretation](docs/integrated_underwriting.md). The manual-only [GitHub Actions test workflow](.github/workflows/manual-tests.yml) is intentionally not triggered on every push to minimise CI consumption.

## Project principles
Transparent formulas, synthetic data, reproducible tests, documented assumptions, conservative CI spending, and clear distinctions between prototypes and independently validated models.

## Reference standards
- [IFRS 9 Financial Instruments](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/)
- [IFRS 13 Fair Value Measurement](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-13-fair-value-measurement/)

MIT licence.