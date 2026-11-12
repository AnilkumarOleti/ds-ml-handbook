"""Spot values for a5-double-ml. Simulation: 20,000 sellers, 20 covariates, nonlinear confounding, true effect 2.0."""
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor as GBR, HistGradientBoostingClassifier as GBC, RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import KFold
rng = np.random.default_rng(7)
n, p, theta = 20_000, 20, 2.0
X = rng.normal(size=(n, p))
g = 6 * np.tanh(X[:, 0]) + 3 * X[:, 1] ** 2 + 4 * (X[:, 2] > 0.5) + 2 * X[:, 0] * X[:, 3]
m = 1 / (1 + np.exp(-(1.2 * np.tanh(X[:, 0]) + 0.8 * X[:, 1] ** 2 - 0.8 + 0.8 * (X[:, 2] > 0.5))))
D = rng.binomial(1, m)
Y = theta * D + g + rng.normal(scale=5, size=n)
print("share treated %.3f" % D.mean())
print("naive difference %.2f" % (Y[D == 1].mean() - Y[D == 0].mean()))
Z = np.column_stack([np.ones(n), D, X])
print("OLS with linear controls %.2f" % np.linalg.lstsq(Z, Y, rcond=None)[0][1])
def dml(cross=True, folds=5):
    yr, dr = np.zeros(n), np.zeros(n)
    if cross:
        for tr, te in KFold(folds, shuffle=True, random_state=1).split(X):
            yr[te] = Y[te] - GBR(max_iter=300, learning_rate=.05).fit(X[tr], Y[tr]).predict(X[te])
            dr[te] = D[te] - GBC(max_iter=300, learning_rate=.05).fit(X[tr], D[tr]).predict_proba(X[te])[:, 1]
    else:
        yr = Y - RandomForestRegressor(200, min_samples_leaf=1, n_jobs=-1, random_state=0).fit(X, Y).predict(X)
        dr = D - RandomForestClassifier(200, min_samples_leaf=1, n_jobs=-1, random_state=0).fit(X, D).predict_proba(X)[:, 1]
    th = (dr * yr).sum() / (dr * dr).sum()
    psi = (yr - th * dr) * dr
    se = np.sqrt((psi ** 2).mean() / (dr * dr).mean() ** 2 / n)
    return th, se
th, se = dml(True)
print("DML cross-fitted %.2f se %.2f CI %.2f to %.2f" % (th, se, th - 1.96 * se, th + 1.96 * se))
th2, se2 = dml(False)
print("DML no cross-fitting, overfit forests %.2f se %.2f" % (th2, se2))
# plug-in single ML: fit Y on D,X with GBR, effect = mean(f(1,X) - f(0,X))
f = GBR(max_iter=300, learning_rate=.05).fit(np.column_stack([D, X]), Y)
pl = (f.predict(np.column_stack([np.ones(n), X])) - f.predict(np.column_stack([np.zeros(n), X]))).mean()
print("single-model plug-in (S-learner) %.2f" % pl)
# worked toy: 6 residual pairs
yt = np.array([3.0, -1.0, 4.0, -2.0, 1.0, -5.0]); dt = np.array([0.6, -0.4, 0.5, -0.3, 0.2, -0.6])
print("toy theta = %.3f / %.3f = %.2f" % ((yt * dt).sum(), (dt * dt).sum(), (yt * dt).sum() / (dt * dt).sum()))
yt = np.array([1.5, -0.5, 1.0, -1.0, 0.5, -1.0])
print("toy2 theta = %.2f / %.2f = %.2f" % ((yt * dt).sum(), (dt * dt).sum(), (yt * dt).sum() / (dt * dt).sum()))
# lab: Y = 2D + g*U + e, D = a*U + v; models capture shares qg, qm of U
def lab(a, gm, qg, qm, th=2):
    return th + gm * a / (a * a + 1), th + gm * a * (1 - qg) / (a * a + 1), th + gm * a * (1 - qg) * (1 - qm) / (a * a * (1 - qm) ** 2 + 1)
print("lab default a=1 g=5 q=.8,.8: naive %.2f outcome-only %.2f DML %.3f" % lab(1, 5, .8, .8))
