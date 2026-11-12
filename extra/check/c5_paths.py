"""Spot values for c5-path-analysis. States: H home, S search, L listing, C cart, K checkout; absorbing P purchase, X exit."""
import numpy as np
T = ["H", "S", "L", "C", "K"]
def build(lc=.20, ck=.60, kp=.70, search=True):
    Q = np.zeros((5, 5)); R = np.zeros((5, 2))
    Q[0, 1], Q[0, 2], R[0, 1] = .50, .20, .30
    Q[1, 1], Q[1, 2], R[1, 1] = .20, .55, .25
    Q[2, 1], Q[2, 2], Q[2, 3], R[2, 1] = .25, .10, lc, .65 - lc
    Q[3, 2], Q[3, 4], R[3, 1] = .15, ck, .85 - ck
    R[4, 0], R[4, 1] = kp, 1 - kp
    if not search:   # removal effect: search leads to exit
        R[:, 1] += Q[:, 1]; Q[:, 1] = 0
    return Q, R
def conv(**kw):
    Q, R = build(**kw); N = np.linalg.inv(np.eye(5) - Q); B = N @ R
    return B[0, 0], N[0].sum(), B
c0, steps, B = conv()
print("conversion from home %.4f, expected pages before leaving %.2f" % (c0, steps))
print("absorption P(purchase) from each state:", dict(zip(T, np.round(B[:, 0], 4))))
print("L->C .20->.25: %.4f (+%.1f%%)" % (conv(lc=.25)[0], 100 * (conv(lc=.25)[0] / c0 - 1)))
print("C->K .60->.70: %.4f (+%.1f%%)" % (conv(ck=.70)[0], 100 * (conv(ck=.70)[0] / c0 - 1)))
print("K->P .70->.80: %.4f (+%.1f%%)" % (conv(kp=.80)[0], 100 * (conv(kp=.80)[0] / c0 - 1)))
print("removal of search: %.4f (removal effect %.0f%%)" % (conv(search=False)[0], 100 * (1 - conv(search=False)[0] / c0)))
# naive funnel: share of sessions reaching each step (ever visit) via simulation
rng = np.random.default_rng(0); Q, R = build(); M = np.hstack([Q, R])
reach = np.zeros(7); n = 200_000; loops = 0
for _ in range(n):
    s, seen = 0, {0}
    while s < 5:
        s = rng.choice(7, p=M[s]); seen.add(s)
    for x in seen: reach[x] += 1
print("share of sessions ever reaching:", dict(zip(T + ["P", "X"], np.round(reach / n, 3))))
