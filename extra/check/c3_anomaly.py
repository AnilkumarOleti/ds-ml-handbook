"""Spot values for c3-anomaly-detection."""
import numpy as np
from scipy.stats import norm, t
S, D = 200, 30
q3 = 2 * norm.sf(3)
print("P(|z|>3) %.4f -> false alerts/day %.2f, /month %.1f" % (q3, S * q3, S * q3 * D))
# heavier tails: t with 4 df scaled to unit variance
sc = np.sqrt(4 / 2)
q3t = 2 * t.sf(3 * sc, 4)
print("t4 residuals: P(|z|>3) %.4f -> /month %.1f" % (q3t, S * q3t * D))
# detection of a 2.5 sigma drop
d = 2.5
p1 = norm.cdf(-3 + d)
print("single-day 3-sigma detection of 2.5 sigma drop %.3f; within 3 days %.3f" % (p1, 1 - (1 - p1) ** 3))
# persistence: two consecutive days beyond 2 sigma on the same side
qf = 2 * norm.sf(2) ** 2
print("2-of-2 at 2 sigma false per series-day %.5f -> /month %.1f" % (qf, S * qf * D))
p2 = norm.cdf(-2 + d)
print("2-consec detection: per-day %.3f, within 3 days %.3f" % (p2, 2 * p2**2 - p2**3))
# precision: 2 real incidents a month across all series
inc = 2
for name, det, fa in (("3-sigma daily", 1 - (1 - p1) ** 3, S * q3 * D), ("2-consecutive at 2 sigma", 2 * p2**2 - p2**3, S * qf * D)):
    tp = inc * det; print("%s: true alerts %.2f false %.1f precision %.0f%%" % (name, tp, fa, 100 * tp / (tp + fa)))
# raw vs forecast residuals: daily orders with weekly cycle, raw CV 15%, residual CV 4%
print("10%% drop in raw-sd units: %.2f; in residual units %.2f" % (0.10 / 0.15, 0.10 / 0.04))
# robust: MAD vs sd with one outlier day in 28
x = np.r_[np.zeros(27) + norm.ppf(np.linspace(.03, .97, 27)), 8.0]
print("sd %.2f, 1.4826*MAD %.2f" % (x.std(ddof=1), 1.4826 * np.median(abs(x - np.median(x)))))
# Bonferroni-style threshold for 1 false alert/month across 200 series: per-test alpha
alpha = 1 / (S * D)
print("threshold for 1 false/month: z = %.2f" % norm.isf(alpha / 2))
from scipy.optimize import brentq
k = brentq(lambda k: 2 * t.sf(k * sc, 4) - q3, 2, 10)
print("t4: threshold for 0.27%% is %.2f sigma" % k)
print("2 sigma everywhere: %.0f false/month" % (S * D * 2 * norm.sf(2)))
# t4 cdf closed form check
F = lambda x: 0.5 + x * (x * x + 6) / (2 * (x * x + 4) ** 1.5)
print("closed form check", F(1.3), t.cdf(1.3, 4))
