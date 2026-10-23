"""Spot values for b0-likelihood-entropy."""
import numpy as np
from scipy.optimize import brentq
ln = np.log
# s1: accuracy vs log loss
y = np.array([1, 0, 0, 0]); A = np.array([.6, .4, .4, .4]); B = np.array([.95, .05, .05, .7])
ll = lambda p: -np.mean(y * ln(p) + (1 - y) * ln(1 - p))
acc = lambda p: np.mean((p > .5) == y)
print("A acc %.2f loss %.3f | B acc %.2f loss %.3f" % (acc(A), ll(A), acc(B), ll(B)))
print("B loss from the one mistake: %.3f of %.3f total" % (-ln(.3), -ln(.3) - 3 * ln(.95)))
# s4 worked: 12 of 200
k, n = 12, 200
L = lambda p: k * ln(p) + (n - k) * ln(1 - p)
print("MLE", k / n, " LR 6%% vs 5%%: %.2f" % np.exp(L(.06) - L(.05)), " vs 3%%: %.3f" % np.exp(L(.06) - L(.03)))
def interval(k, n):
    m = k / n; f = lambda p: k * ln(p) + (n - k) * ln(1 - p) - (k * ln(m) + (n - k) * ln(1 - m)) + 1.92
    return brentq(f, 1e-9, m), brentq(f, m, 1 - 1e-9)
print("likelihood interval 12/200: %.4f %.4f" % interval(12, 200))
print("likelihood interval 120/2000: %.4f %.4f" % interval(120, 2000))
print("wald 12/200: %.4f %.4f" % (0.06 - 1.96 * (0.06 * 0.94 / 200) ** .5, 0.06 + 1.96 * (0.06 * 0.94 / 200) ** .5))
# MAP with Beta(2,38)
a, b = 2, 38
print("MAP %.4f  posterior mean %.4f" % ((k + a - 1) / (n + a + b - 2), (k + a) / (n + a + b)))
print("MAP with 1 of 10: MLE %.3f MAP %.4f" % (0.1, (1 + a - 1) / (10 + a + b - 2)))
# bare: entropy and base-rate log loss
H2 = lambda p: -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
He = lambda p: -(p * ln(p) + (1 - p) * ln(1 - p))
for p in (.5, .1, .02):
    print("p=%.2f entropy %.3f bits, base-rate log loss %.4f nats" % (p, H2(p), He(p)))
# a model with log loss 0.09 at 2% base rate: improvement
print("0.09 vs base %.4f -> %.1f%% better" % (He(.02), 100 * (1 - .09 / He(.02))))
# KL
kl = lambda p, q: p * ln(p / q) + (1 - p) * ln((1 - p) / (1 - q))
print("KL(.02||.05) %.4f  KL(.05||.02) %.4f" % (kl(.02, .05), kl(.05, .02)))
# cross-entropy decomposition check: H(p,q) = H(p) + KL
p, q = .02, .05
print("H(p,q) %.4f = H(p) %.4f + KL %.4f" % (-(p * ln(q) + (1 - p) * ln(1 - q)), He(p), kl(p, q)))
# clipped confident error
print("loss of p=0.999 on a negative: %.2f ; clipped at 0.99: %.2f" % (-ln(.001), -ln(.01)))
# perplexity
print("perplexity of loss 2.3 nats: %.1f" % np.exp(2.3))
