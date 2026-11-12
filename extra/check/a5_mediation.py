"""Spot values for a5-mediation."""
import numpy as np
a, b_obs, total = 1.5, 4.0, 12.0
print("product of coefficients: indirect %.1f direct %.1f share %.0f%%" % (a * b_obs, total - a * b_obs, 100 * a * b_obs / total))
b_true = 2.5
print("with b from the photo experiment: indirect %.2f direct %.2f share %.0f%%" % (a * b_true, total - a * b_true, 100 * a * b_true / total))
# interaction: Y = c' T + b M + d T M; E[M|T=0] = 4
m0, b, d = 4.0, 3.0, 2.0
c = total - d * m0 - (b + d) * a
print("c' %.1f NDE %.1f NIE %.1f PNIE %.1f TDE %.1f" % (c, c + d * m0, (b + d) * a, b * a, total - b * a))
# confounding of the mediator: M = 4 + a T + k U + e_m (sd 1.5); Y = c T + b M + 4k U + e
sm = 1.5
k = np.sqrt(1.5 * sm**2 / 2.5)
print("k for b_hat=4 with b=2.5: %.3f" % k)
bh = lambda b, k: b + 4 * k * k / (k * k + sm**2)
for kk in (0, 0.5, 0.8, k, 1.5):
    print("k %.2f b_hat %.2f indirect est %.2f (true %.2f)" % (kk, bh(2.5, kk), a * bh(2.5, kk), a * 2.5))
# simulation check
rng = np.random.default_rng(3); n = 400_000
T = rng.binomial(1, .5, n); U = rng.normal(size=n)
M = 4 + a * T + k * U + rng.normal(scale=sm, size=n)
direct_true = total - a * 2.5
Y = direct_true * T + 2.5 * M + 4 * k * U + rng.normal(scale=10, size=n)
Y = Y - 2.5 * 4  # level irrelevant
Z = np.column_stack([np.ones(n), T, M])
co = np.linalg.lstsq(Z, Y, rcond=None)[0]
print("sim: total %.2f, b_hat %.2f, direct_hat %.2f" % (Y[T == 1].mean() - Y[T == 0].mean(), co[2], co[1]))
