from math import exp

def survival_probability(time, tenors, hazards):
    if time < 0 or not tenors or len(tenors) != len(hazards):
        raise ValueError('invalid inputs')
    previous = 0.0
    total = 0.0
    for end, hazard in zip(tenors, hazards):
        if end <= previous or hazard < 0:
            raise ValueError('invalid curve')
        total += max(0.0, min(time, end) - previous) * hazard
        previous = end
    if time > previous:
        total += (time - previous) * hazards[-1]
    return exp(-total)
