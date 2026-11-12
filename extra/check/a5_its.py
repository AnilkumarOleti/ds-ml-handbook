"""Spot values for a5-its-causalimpact."""
import numpy as np
from scipy.stats import norm
# pre-period weeks 1..26: orders (thousand) = 200 + 1.0 * week, residual sd 3
a, b, s, n = 200.0, 1.0, 3.0, 26
pre = np.arange(1, 27); post = np.arange(27, 35)
cf = a + b * post
print("counterfactual weeks 27-34:", cf, "avg %.1f" % cf.mean())
obs_avg = 238.0
before8 = (a + b * np.arange(19, 27)).mean()
print("naive before/after: before avg %.1f, after %.1f, diff %.1f (%.1f%%)" % (before8, obs_avg, obs_avg - before8, 100 * (obs_avg - before8) / before8))
print("ITS effect %.1f (%.1f%%)" % (obs_avg - cf.mean(), 100 * (obs_avg - cf.mean()) / cf.mean()))
cf2 = cf.mean() * 1.02
print("with control +2%%: counterfactual %.1f effect %.1f (%.1f%%)" % (cf2, obs_avg - cf2, 100 * (obs_avg - cf2) / cf2))
# prediction se for the average of 8 post weeks (OLS on 26 points)
tbar = pre.mean(); Sxx = ((pre - tbar) ** 2).sum()
var_line = s**2 * (1 / n + (post.mean() - tbar) ** 2 / Sxx)
var_noise = s**2 / len(post)
se = (var_line + var_noise) ** .5
print("se of average effect %.2f (line %.2f noise %.2f); 95%% half-width %.2f" % (se, var_line**.5, var_noise**.5, 1.96 * se))
print("ITS interval %.1f to %.1f" % (obs_avg - cf.mean() - 1.96 * se, obs_avg - cf.mean() + 1.96 * se))
# with control, model se larger, say 1.6 (stated); interval
print("control-adjusted interval %.1f to %.1f" % (obs_avg - cf2 - 1.96 * 1.6, obs_avg - cf2 + 1.96 * 1.6))
# single-week forecast band at week 34 and 52
for t in (27, 34, 52):
    print("week %d single-week 95%% band +- %.2f" % (t, 1.96 * s * (1 + 1 / n + (t - tbar) ** 2 / Sxx) ** .5))
# lab default: pre 26, sd 3, horizon 8 -> half width as above. pre 8:
for npre in (8, 13, 26, 52):
    p = np.arange(1, npre + 1); tb = p.mean(); Sx = ((p - tb) ** 2).sum(); q = np.arange(npre + 1, npre + 9)
    v = s**2 * (1 / npre + (q.mean() - tb) ** 2 / Sx) + s**2 / 8
    print("pre %d weeks: half-width %.2f" % (npre, 1.96 * v**.5))
