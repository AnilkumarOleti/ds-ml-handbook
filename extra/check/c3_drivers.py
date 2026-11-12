"""Spot values for c3-key-drivers."""
import numpy as np, itertools
rng = np.random.default_rng(42)
n = 3000
halo = rng.normal(size=n)
deliv = 0.6 * halo + 0.8 * rng.normal(size=n)
desc = 0.6 * halo + 0.8 * rng.normal(size=n)
price = 0.4 * halo + 0.92 * rng.normal(size=n)
pack = 0.95 * deliv + 0.31 * rng.normal(size=n)          # packaging rated with delivery (same courier)
supp = 0.5 * halo + 0.87 * rng.normal(size=n)
y = 0.45 * deliv + 0.55 * desc + 0.25 * price + 0.0 * pack + 0.15 * supp + 0.3 * halo + 0.8 * rng.normal(size=n)
X = np.column_stack([deliv, desc, price, pack, supp]); names = ["Delivery speed", "Item as described", "Price", "Packaging", "Customer service"]
Xs = (X - X.mean(0)) / X.std(0); ys = (y - y.mean()) / y.std()
r = [np.corrcoef(X[:, j], y)[0, 1] for j in range(5)]
beta = np.linalg.lstsq(np.column_stack([np.ones(n), Xs]), ys, rcond=None)[0][1:]
def r2(cols):
    if not cols: return 0.0
    Z = np.column_stack([np.ones(n), Xs[:, cols]]); b = np.linalg.lstsq(Z, ys, rcond=None)[0]
    return 1 - ((ys - Z @ b) ** 2).sum() / (ys ** 2).sum()
from math import factorial
p = 5; shap = np.zeros(p)
for j in range(p):
    others = [k for k in range(p) if k != j]
    for s in range(p):
        for S in itertools.combinations(others, s):
            w = factorial(s) * factorial(p - s - 1) / factorial(p)
            shap[j] += w * (r2(list(S) + [j]) - r2(list(S)))
tot = r2(list(range(5)))
print("total R2 %.3f" % tot)
for j in range(5): print("%-18s r %.2f beta %.2f shapley %.3f share %.0f%%" % (names[j], r[j], beta[j], shap[j], 100 * shap[j] / tot))
print("corr deliv-pack %.2f" % np.corrcoef(deliv, pack)[0, 1])
# bootstrap stability of betas for packaging vs delivery
bs = []
for _ in range(300):
    i = rng.integers(0, n, n); Z = np.column_stack([np.ones(n), Xs[i]]); bs.append(np.linalg.lstsq(Z, ys[i], rcond=None)[0][[1, 4]])
bs = np.array(bs); print("bootstrap 95%% beta deliv %.2f..%.2f pack %.2f..%.2f" % (*np.percentile(bs[:, 0], [2.5, 97.5]), *np.percentile(bs[:, 1], [2.5, 97.5])))
# two-predictor worked example
ra, rb, rab = np.sqrt(.30), np.sqrt(.20), None
r2a, r2b, r2ab = .30, .20, .38
print("worked: A %.2f B %.2f" % ((r2a + r2ab - r2b) / 2, (r2b + r2ab - r2a) / 2))
