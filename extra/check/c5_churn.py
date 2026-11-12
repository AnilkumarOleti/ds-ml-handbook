"""Spot values for c5-churn-propensity."""
import numpy as np
churn = np.array([62, 45, 35, 30, 27, 22, 10, 8, 6, 5]) / 100
upl = np.array([4, 6, 8, 8, 7, 5, 2, 1, 1, 0]) / 100
print("base rate %.3f" % churn.mean())
cum = np.cumsum(churn) / churn.sum()
print("capture top1 %.3f top3 %.3f lift top1 %.2f" % (cum[0], cum[2], churn[0] / churn.mean()))
V, C, n = 2500, 150, 10_000   # value of a saved buyer, cost per offer, buyers per decile
prof = n * (upl * V - C)
for d in range(10): print("decile %d churn %.2f uplift %.2f profit per decile %+.0f" % (d + 1, churn[d], upl[d], prof[d]))
print("target top-3 by risk: %+.0f; target by uplift (positive-profit deciles): %+.0f (deciles %s)" % (prof[:3].sum(), prof[prof > 0].sum(), list(np.where(prof > 0)[0] + 1)))
print("break-even uplift %.3f" % (C / V))
# decile 1 per 1000: saved 40, value 100k vs cost 150k
print("decile1 per 1000: saved %d value %d cost %d" % (1000 * upl[0], 1000 * upl[0] * V, 1000 * C))
print("decile3 per 1000: saved %d value %d cost %d" % (1000 * upl[2], 1000 * upl[2] * V, 1000 * C))
