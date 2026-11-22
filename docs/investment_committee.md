# Investment committee decision screen (synthetic)

`private_credit.investment_decision` links the existing piecewise-constant hazard survival model and continuous default-time recovery integration to an acquisition-price assessment and controlled downside scenarios.

**The decision is a mechanical model gate, not investment advice.** `PASS` means simplified model value exceeds price by at least the specified margin; it does not validate PD inputs, collateral appraisal, legal priority, liquidity, covenants or suitability.

## Mechanics

- **Model value:** survival-weighted coupons + principal paid upon survival + continuous default-time recovery; all discounted using an externally supplied continuously compounded risk-free proxy.
- **NPV / margin:** value less acquisition price; margin percentage divides by model value.
- **Break-even coupon:** `max(0, (purchase_price - zero_coupon_value) / expected_survival_coupon_annuity)`. If a zero-coupon instrument is already above acquisition price, zero is the smallest admissible coupon. This is not a yield/IRR calculation.
- **Default probability:** `1 - survival_probability(maturity)`.
- **Annual expected-loss proxy:** maturity default probability × unrecovered principal ÷ years; **not** IFRS 9 ECL, annual PD or fair value.
- **Stress:** multiplicative hazard shocks, haircut of fixed recovery, additional continuously compounded discount-rate shifts and longer recovery lags. These are deterministic, not statistically calibrated.

## Running

```bash
python -m pip install -e ".[dev]"
python examples/investment_committee.py
pytest -q
```

## Limitations and development priorities

A production-calibre model needs forward-SONIA curve data, irregular coupon dates/day counts, prepayments, commitment fees, drawdowns, risk-neutral calibration, market credit/liquidity premiums, collateral valuations, documentation-specific cash-flow waterfalls, correlated borrower exposures and independent benchmark/model validation. Distinguish IFRS 9 ECL, IFRS 13 fair value and investment price discipline rather than treating them as interchangeable.
