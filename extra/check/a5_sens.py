"""Spot values for a5-sensitivity-falsification."""
import numpy as np
from scipy.stats import norm, binom
from scipy.optimize import brentq
E = lambda rr: rr + np.sqrt(rr * (rr - 1))
for rr in (1.30, 1.18, 1.43, 2.0, 1.1, 3.0):
    print("RR %.2f -> E-value %.2f" % (rr, E(rr)))
# bias factor for confounder with RR_UD (with treatment) and RR_UY
B = lambda a, b: a * b / (a + b - 1)
print("confounder 1.8 & 2.5: bias factor %.2f -> adjusted RR %.2f, adjusted lower %.2f" % (B(1.8, 2.5), 1.30 / B(1.8, 2.5), 1.18 / B(1.8, 2.5)))
print("confounder 1.5 & 1.5: bias factor %.3f -> adjusted RR %.3f" % (B(1.5, 1.5), 1.30 / B(1.5, 1.5)))
# Rosenbaum sign test: 1000 discordant pairs, 600 favour treatment
n, k = 1000, 600
def p_upper(G):
    pp = G / (1 + G)
    return binom.sf(k - 1, n, pp)
for G in (1.0, 1.2, 1.3, 1.4, 1.5):
    print("Gamma %.1f worst-case p %.4f" % (G, p_upper(G)))
Gstar = brentq(lambda G: p_upper(G) - 0.05, 1.0, 2.0)
print("Gamma* where p=0.05: %.3f" % Gstar)
# normal approx solution
pp = lambda G: G / (1 + G)
print("at Gamma 1.38 expected %.1f sd %.2f" % (n * pp(1.38), np.sqrt(n * pp(1.38) * (1 - pp(1.38)))))
# placebo: pre-period purchases 9% higher
