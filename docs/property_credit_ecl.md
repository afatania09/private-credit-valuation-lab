# Integrated property-backed credit ECL (research prototype)

`private_credit.property_credit_ecl.property_credit_ecl` combines existing
property underwriting and scenario-weighted ECL modules.

For each economic scenario:

1. Calculate NOI, CFADS, capitalised property value, DSCR and refinancing gap.
2. Deduct a specified collateral sale haircut, enforcement cost fraction and
   senior-ranking claim from collateral proceeds.
3. Cap recoveries at outstanding loan principal; set LGD = 1 - recovery/EAD.
4. Apply *externally supplied* conditional default probabilities to constant
   annual exposure and LGD, using the existing discounted ECL engine.
5. Aggregate scenario results using scenario probability weights.

This connects property fundamentals and loan losses but **does not estimate
PD from DSCR**. An observed DSCR breach or refinancing gap is a risk indicator,
not proof of default. Recovery values are constant through the horizon;
recoveries have no lag and defaulted loan interest is excluded. The output is
not IFRS 9-compliant and must not be presented as IFRS 13 fair value.

Run `pytest -q tests/test_property_credit_ecl.py` locally. GitHub Actions
remains manual-only to conserve CI usage.
