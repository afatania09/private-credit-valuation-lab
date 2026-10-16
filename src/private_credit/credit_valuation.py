from math import exp

def survival_discounted_principal(principal: float, hazard: float, discount_rate: float, years: float) -> float:
    if principal < 0 or hazard < 0 or discount_rate < 0 or years < 0:
        raise ValueError('Inputs must be nonnegative')
    return principal * exp(-(hazard + discount_rate) * years)
