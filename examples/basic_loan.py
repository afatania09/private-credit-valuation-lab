from private_credit import bullet_cash_flows, present_value, simple_expected_loss

flows = bullet_cash_flows(10_000_000, 0.08, 5)
print("Contractual DCF at 12%:", round(present_value(flows, 0.12), 2))
print("Illustrative EL proxy:", round(simple_expected_loss(0.02, 0.4, 10_000_000), 2))
