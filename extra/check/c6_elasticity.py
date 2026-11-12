"""Spot values for c6-price-elasticity."""
import numpy as np
Q0, F0, F1, c = 100_000, 40, 50, 80
for e in (-0.4, -0.8, -1.2):
    Q1 = Q0 * (F1 / F0) ** e
    fee0, fee1 = F0 * Q0, F1 * Q1
    com_loss = (Q0 - Q1) * c
    print("e %.1f: orders %.0f (%.2f%%), fee rev %.1f -> %.1f lakh, commission lost %.1f lakh, net %+.1f lakh/day" % (e, Q1, 100 * (Q1 / Q0 - 1), fee0 / 1e5, fee1 / 1e5, com_loss / 1e5, (fee1 - fee0 - com_loss) / 1e5))
print("log check: ln(Q1/Q0)/ln(1.25) = %.3f" % (np.log((1.25) ** -0.4) / np.log(1.25)))
# break-even elasticity for net zero: (F1 Q1 - F0 Q0) = c (Q0 - Q1) -> (F1 + c) Q1 = (F0 + c) Q0 -> (1.25)^e = 120/130
print("break-even elasticity %.3f" % (np.log((F0 + c) / (F1 + c)) / np.log(F1 / F0)))
# simulated observational bias: cities with higher demand have higher fees
rng = np.random.default_rng(2)
n = 300
demand = rng.normal(size=n)
lnF = np.log(40) + 0.05 * demand + 0.08 * rng.normal(size=n)
lnQ = np.log(1e5) + 0.2 * demand - 0.4 * (lnF - np.log(40)) + 0.1 * rng.normal(size=n)
b = np.polyfit(lnF, lnQ, 1)[0]
print("observational slope %.2f (true -0.4)" % b)
Z = np.column_stack([np.ones(n), lnF, demand]); print("controlling for demand index: %.2f" % np.linalg.lstsq(Z, lnQ, rcond=None)[0][1])
# switchback: half-worked numbers: high fee periods 46,200 orders per city-week vs low 50,000? use 50 vs 40 fee -> ratio
print("switchback: orders at 50 vs 40 ratio for e=-0.4: %.4f" % (1.25 ** -0.4))
# optimal fee with commission 80 for e=-1.5: F* = -e c/(1+e)
for F in (30, 35, 45, 50, 60):
    print("fee %d, e -0.4: net %+.1f lakh/day" % (F, ((F + c) * Q0 * (F / F0) ** -0.4 - (F0 + c) * Q0) / 1e5))
