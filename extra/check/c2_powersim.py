"""Spot values for c2-power-simulation."""
import numpy as np
from scipy import stats
rng = np.random.default_rng(5)
n_user, sims = 10_000, 2000
def arm(lift=0.0):
    rate = rng.gamma(0.7, 6.0, n_user)
    sess = 1 + rng.poisson(rate)
    p = rng.beta(0.3, 2.7, n_user)
    basket = rng.lognormal(0, 0.8, n_user)
    uid = np.repeat(np.arange(n_user), sess)
    buy = rng.random(uid.size) < p[uid]
    rev = np.where(buy, rng.lognormal(6.5, 1.0, uid.size) * basket[uid], 0.0) * (1 + lift)
    return uid, rev, sess
def one(lift=0.0):
    u0, r0, s0 = arm(); u1, r1, s1 = arm(lift)
    # naive: session-level t-test on revenue per session
    p_naive = stats.ttest_ind(r1, r0, equal_var=False).pvalue
    # user level: revenue per user t-test
    R0 = np.bincount(u0, r0, n_user); R1 = np.bincount(u1, r1, n_user)
    p_user = stats.ttest_ind(R1, R0, equal_var=False).pvalue
    # delta method for revenue per session ratio
    def dm(R, S):
        mr, ms = R.mean(), S.mean(); v = (R.var(ddof=1) / ms**2 - 2 * mr / ms**3 * np.cov(R, S)[0, 1] + mr**2 / ms**4 * S.var(ddof=1)) / len(R)
        return mr / ms, v
    a, va = dm(R0, s0); b, vb = dm(R1, s1)
    p_dm = 2 * stats.norm.sf(abs(b - a) / np.sqrt(va + vb))
    # capped user revenue at pooled 99th pct
    cap = np.percentile(np.concatenate([R0, R1]), 99)
    p_cap = stats.ttest_ind(np.minimum(R1, cap), np.minimum(R0, cap), equal_var=False).pvalue
    return p_naive, p_user, p_dm, p_cap
aa = np.array([one(0) for _ in range(sims)])
print("A/A false positive rates (sims %d): naive session-level %.3f, user-level %.3f, delta method %.3f, capped %.3f" % ((sims,) + tuple((aa < .05).mean(0))))
se = np.sqrt(.05 * .95 / sims); print("MC se of a 5%% rate: %.4f" % se)
ab = np.array([one(0.05) for _ in range(sims)])
print("power for +5%% revenue: naive %.3f user %.3f delta %.3f capped %.3f" % tuple((ab < .05).mean(0)))
# baseline numbers
u, r, s = arm(); R = np.bincount(u, r, n_user)
print("sessions/user %.2f, rev/user mean %.0f sd %.0f CV %.2f, share buyers %.3f" % (s.mean(), R.mean(), R.std(), R.std() / R.mean(), (R > 0).mean()))
# formula power for +5% on rev/user
cv = R.std() / R.mean(); se_rel = cv * np.sqrt(2 / n_user); z = 0.05 / se_rel
print("formula power for 5%%: %.3f" % (stats.norm.cdf(z - 1.96)))
for L in (0.10, 0.15):
    ab = np.array([one(L) for _ in range(1000)])
    print("power for +%d%%: naive %.3f user %.3f delta %.3f capped %.3f" % ((100 * L,) + tuple((ab < .05).mean(0))))
    print("   formula power user-level %.3f" % stats.norm.cdf(L / (cv * np.sqrt(2 / n_user)) - 1.96))
# capped metric bias: true lift on capped mean
u0, r0, s0 = arm(); u1, r1, s1 = arm(0.15)
R0 = np.bincount(u0, r0, n_user); R1 = np.bincount(u1, r1, n_user); cap = np.percentile(np.concatenate([R0, R1]), 99)
print("capped lift %.3f vs raw lift %.3f (one draw)" % (np.minimum(R1, cap).mean() / np.minimum(R0, cap).mean() - 1, R1.mean() / R0.mean() - 1))
