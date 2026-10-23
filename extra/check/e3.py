"""Spot values for e3-fairness."""
from scipy.stats import norm
def grp(base, tpr, fpr, N=10_000):
    pos = base * N; neg = N - pos; tp = tpr * pos; fp = fpr * neg
    return tp, fp, tp / (tp + fp), (tp + fp) / N
for name, b in (("new", .04), ("established", .01)):
    tp, fp, prec, flag = grp(b, .8, .05)
    print("%-11s per 10,000: TP %.0f FP %.0f precision %.1f%% flagged %.2f%%" % (name, tp, fp, 100 * prec, 100 * flag))
# FPR for established to reach 40% precision at recall 0.8
f = 0.8 * 0.01 * (1 / 0.4 - 1) / 0.99
print("FPR for established to reach 40%% precision: %.2f%%" % (100 * f))
# with binormal scores, separation d: thresholds
d = 2.5
t_for_tpr = lambda tpr: d - norm.ppf(tpr) * 1  # TPR = 1 - Phi(t - d)
t = d + norm.ppf(1 - 0.8)
print("d=%.1f threshold for 80%% recall t=%.3f -> FPR %.2f%%" % (d, t, 100 * (1 - norm.cdf(t))))
# four-fifths rule
a, b = 0.60, 0.42
print("selection ratio %.2f" % (b / a))
# same threshold, binormal d=2.5 at t=1.658: per group precision
fpr = 1 - norm.cdf(t)
for name, base in (("new", .04), ("established", .01)):
    tp, fp, prec, flag = grp(base, .8, fpr)
    print("binormal %s precision %.1f%%" % (name, 100 * prec))
# raise established threshold to equalise precision at 40%
from scipy.optimize import brentq
def prec_at(tt, base, d=2.5):
    tpr = 1 - norm.cdf(tt - d); fpr = 1 - norm.cdf(tt)
    return tpr * base / (tpr * base + fpr * (1 - base)), tpr, fpr
p_new = prec_at(t, .04)[0]
tt = brentq(lambda x: prec_at(x, .01)[0] - p_new, t, 6)
pr, tpr, fpr2 = prec_at(tt, .01)
print("equal precision %.1f%%: established threshold %.2f, recall %.1f%%, FPR %.2f%%" % (100 * p_new, tt, 100 * tpr, 100 * fpr2))
