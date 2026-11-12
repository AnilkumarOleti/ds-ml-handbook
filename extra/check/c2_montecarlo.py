"""Spot values for c2-monte-carlo."""
import numpy as np
rng = np.random.default_rng(11)
N = 1_000_000
tri = lambda lo, mode, hi: rng.triangular(lo, mode, hi, N)
elig, adopt, lift, spend = tri(4e6, 5e6, 6e6), tri(.05, .10, .20), tri(.03, .06, .12), tri(6000, 7000, 8000)
point = 5e6 * .10 * .06 * 7000
lo, hi = 4e6 * .05 * .03 * 6000, 6e6 * .2 * .12 * 8000
print("point %.1f cr, all-low %.1f cr, all-high %.1f cr" % (point / 1e7, lo / 1e7, hi / 1e7))
v = elig * adopt * lift * spend / 1e7
q = np.percentile(v, [10, 50, 90])
print("MC P10 %.1f P50 %.1f P90 %.1f mean %.1f cr" % (*q, v.mean()))
print("P(> 15 cr) %.3f, P(> point 21) %.3f" % ((v > 15).mean(), (v > 21).mean()))
print("means: adopt %.4f lift %.4f -> product of means %.1f" % (adopt.mean(), lift.mean(), 5e6 * adopt.mean() * lift.mean() * 7000 / 1e7))
# correlated adoption and lift (negative: broader adoption = smaller lift), via gaussian copula rho=-0.6 and +0.6
from scipy.stats import norm
def tri_ppf(u, lo, m, hi):
    c = (m - lo) / (hi - lo)
    return np.where(u < c, lo + np.sqrt(u * (hi - lo) * (m - lo)), hi - np.sqrt((1 - u) * (hi - lo) * (hi - m)))
for rho in (-0.6, 0.6):
    z1 = rng.normal(size=N); z2 = rho * z1 + np.sqrt(1 - rho**2) * rng.normal(size=N)
    a2, l2 = tri_ppf(norm.cdf(z1), .05, .10, .20), tri_ppf(norm.cdf(z2), .03, .06, .12)
    w = elig * a2 * l2 * spend / 1e7
    print("rho %.1f: P10 %.1f P50 %.1f P90 %.1f P(>15) %.3f" % (rho, *np.percentile(w, [10, 50, 90]), (w > 15).mean()))
# worked: five draws table
draws = [(5.2e6, .08, .05, 7200), (4.6e6, .14, .09, 6500), (5.5e6, .07, .04, 7600), (4.9e6, .12, .07, 6900), (5.1e6, .18, .10, 7100)]
for d in draws: print("draw %.2f cr" % (np.prod(d) / 1e7))
# convergence: MC error of P90 with 1000 draws
reps = [np.percentile((tri(4e6, 5e6, 6e6)[:1000] * tri(.05, .1, .2)[:1000] * tri(.03, .06, .12)[:1000] * tri(6000, 7000, 8000)[:1000]) / 1e7, 90) for _ in range(30)]
print("P90 with 1,000 draws: sd across reruns %.2f" % np.std(reps))
# tornado at medians
med = lambda lo, m, hi: (lo + np.sqrt(.5 * (hi - lo) * (m - lo))) if (m - lo) / (hi - lo) >= .5 else (hi - np.sqrt(.5 * (hi - lo) * (hi - m)))
B, A, L, P = med(4e6, 5e6, 6e6), med(.05, .1, .2), med(.03, .06, .12), med(6000, 7000, 8000)
print("medians", B, round(A, 4), round(L, 4), P)
f = lambda b, a, l, p: b * a * l * p / 1e7
print("tornado: adoption %.1f-%.1f lift %.1f-%.1f buyers %.1f-%.1f spend %.1f-%.1f" % (f(B, .05, L, P), f(B, .2, L, P), f(B, A, .03, P), f(B, A, .12, P), f(4e6, A, L, P), f(6e6, A, L, P), f(B, A, L, 6000), f(B, A, L, 8000)))
print("max of 1M draws %.1f; share above 100: %.2e; above 80: %.2e" % (v.max(), (v > 100).mean(), (v > 80).mean()))
