"""Spot values for the A3 design lab: smallest detectable effects for a fixed run length (two-sided 5%, 80% power)."""
from scipy.stats import norm
z = norm.ppf(0.975) + norm.ppf(0.80)
def mde(p, n):  # absolute, per-arm n, equal arms, unpooled approximation
    return z * (2 * p * (1 - p) / n) ** 0.5
n = 2000 * 14
print("users per arm", n)
m = mde(0.10, n); print("conversion 10%%: %.2f pts = %.1f%% relative" % (100 * m, 100 * m / 0.10))
g = mde(0.03, n); print("refunds 3%%: %.2f pts = %.1f%% relative" % (100 * g, 100 * g / 0.03))
for w in (1, 2, 4, 6):
    print(w, "weeks:", "%.2f pts" % (100 * mde(0.10, 2000 * 7 * w)), "refund %.1f%% rel" % (100 * mde(0.03, 2000 * 7 * w) / 0.03))
