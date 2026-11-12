"""Spot values for a5-balance-overlap."""
import numpy as np
from scipy.stats import norm
def smd(mt, st, mc, sc): return (mt - mc) / ((st**2 + sc**2) / 2) ** .5
rows = {"Prior 90-day GMV, ₹ thousand": (420, 300, 260, 240, 410, 290),
        "Active listings": (85, 60, 70, 55, 83, 58),
        "Tenure, months": (30, 20, 29, 22, 31, 21),
        "Rating": (4.6, 0.3, 4.5, 0.4, 4.58, 0.33)}
for k, (mt, st, mc, sc, mm, sm) in rows.items():
    print("%-30s before SMD %.3f VR %.2f | after SMD %.3f VR %.2f" % (k, smd(mt, st, mc, sc), st**2 / sc**2, smd(mt, st, mm, sm), st**2 / sm**2))
# t-test on tenure with 2,000 vs 18,000
se = (20**2 / 2000 + 22**2 / 18000) ** .5
t = 1 / se
print("tenure t %.2f p %.3f" % (t, 2 * norm.sf(t)))
# after matching, 2000 vs 2000, GMV diff 10
se2 = (300**2 / 2000 + 290**2 / 2000) ** .5
print("matched GMV t %.2f p %.2f" % (10 / se2, 2 * norm.sf(10 / se2)))
# CEM strata
S = [("Low GMV, fashion", 300, 6000, 105, 100), ("Low GMV, electronics", 200, 4000, 112, 104),
     ("Mid GMV, fashion", 500, 3500, 160, 148), ("Mid GMV, electronics", 400, 2500, 175, 160),
     ("High GMV, fashion", 450, 1500, 300, 280), ("High GMV, electronics", 150, 0, 330, None)]
nt = sum(s[1] for s in S); nc = sum(s[2] for s in S)
yt = sum(s[1] * s[3] for s in S) / nt; yc = sum(s[2] * s[4] for s in S if s[2]) / nc
print("naive: treated %.1f control %.1f diff %.1f" % (yt, yc, yt - yc))
kept = [s for s in S if s[2] > 0]
ntk = sum(s[1] for s in kept)
att = sum(s[1] * (s[3] - s[4]) for s in kept) / ntk
print("CEM ATT %.2f on %d of %d treated (dropped %.1f%%)" % (att, ntk, nt, 100 * (nt - ntk) / nt))
for s in kept: print("  %s: diff %d weight %.3f" % (s[0], s[3] - s[4], s[1] / ntk))
# control weights in CEM: w = (nt_s/nc_s) * (NC_kept/NT_kept)
NCk = sum(s[2] for s in kept)
for s in kept: print("  %s control weight %.3f" % (s[0], (s[1] / s[2]) * (NCk / ntk)))
# overlap: logit propensity N(+d/2,1) treated, N(-d/2,1) control
def kept_share(d, a):
    lo, hi = np.log(a / (1 - a)), np.log((1 - a) / a)
    return norm.cdf(hi - d / 2) - norm.cdf(lo - d / 2), norm.cdf(hi + d / 2) - norm.cdf(lo + d / 2)
for d in (1, 2, 3):
    print("sep %.0f trim .1: treated kept %.3f control kept %.3f" % ((d,) + kept_share(d, .1)))
print("max ATT control weight at p=.9: %.1f; at .99: %.0f" % (.9 / .1, .99 / .01))
