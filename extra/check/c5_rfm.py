"""Spot values for c5-segmentation-rfm."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
rng = np.random.default_rng(3)
n = 50_000
eng = rng.normal(size=n)                                    # latent engagement
freq = rng.poisson(np.exp(0.8 + 0.7 * eng)) + 1             # orders in 12 months
rec = np.minimum(365, rng.exponential(np.exp(4.2 - 0.6 * eng)))  # days since last order
mon = freq * rng.lognormal(7.3 + 0.2 * eng, 0.8)            # 12-month spend
X = np.column_stack([rec, freq, mon])
print("medians: recency %.0f d, freq %.0f, spend %.0f" % tuple(np.median(X, 0)))
print("sd: recency %.0f, freq %.1f, spend %.0f" % tuple(X.std(0)))
km = KMeans(4, n_init=5, random_state=0).fit(X)
for c in range(4):
    m = km.labels_ == c; print("unscaled cluster %d: share %.2f recency %.0f freq %.1f spend %.0f" % (c, m.mean(), *X[m].mean(0)))
Z = np.column_stack([np.log1p(rec), np.log1p(freq), np.log1p(mon)]); Z = (Z - Z.mean(0)) / Z.std(0)
km2 = KMeans(4, n_init=5, random_state=0).fit(Z)
for c in range(4):
    m = km2.labels_ == c; print("scaled cluster %d: share %.2f recency %.0f freq %.1f spend %.0f" % (c, m.mean(), *np.median(X[m], 0)))
# stability across two halves / seeds
a = KMeans(4, n_init=1, random_state=1).fit(Z).labels_; b = KMeans(4, n_init=1, random_state=2).fit(Z).labels_
print("ARI scaled seeds %.2f" % adjusted_rand_score(a, b))
a = KMeans(6, n_init=1, random_state=1).fit(Z).labels_; b = KMeans(6, n_init=1, random_state=2).fit(Z).labels_
print("ARI k=6 seeds %.2f" % adjusted_rand_score(a, b))
# quintile cutoffs
for nm, col, rev in (("recency", rec, True), ("frequency", freq, False), ("spend", mon, False)):
    print(nm, "quintile cutoffs", np.round(np.percentile(col, [20, 40, 60, 80]), 0))
