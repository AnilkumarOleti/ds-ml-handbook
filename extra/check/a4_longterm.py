"""Spot values for a4-long-term-effects."""
import numpy as np
from scipy.stats import norm
# s1: novelty decay. effect(t) = L + (E0 - L) * exp(-(t-1)/tau), days 1..14
L, E0, tau = 0.015, 0.08, 4.0
d = np.arange(1, 15)
eff = L + (E0 - L) * np.exp(-(d - 1) / tau)
print("daily effects %:", np.round(100 * eff, 2))
print("week1 avg %.2f%%, week2 avg %.2f%%, 14-day avg %.2f%%, long run %.2f%%" % (100 * eff[:7].mean(), 100 * eff[7:].mean(), 100 * eff.mean(), 100 * L))
print("overstatement of 14-day avg vs long run: %.1fx" % (eff.mean() / L))
# new users see no novelty: flat 1.5%
# value: 20M clicks/week baseline revenue? keep relative
# s4 worked: fit decay from week averages? Use ratio method: day 1 vs day 8 vs day 14
print("day1 %.2f day8 %.2f day14 %.2f" % tuple(100 * eff[[0, 7, 13]]))
# half-worked: holdout sizing. 8,000,000 users, orders per user per quarter mean 0.9 sd 2.4
N, mu, sd = 8_000_000, 0.9, 2.4
for h in (0.01, 0.02, 0.05):
    nh, ne = N * h, N * (1 - h)
    se = sd * (1 / nh + 1 / ne) ** .5
    mde = (norm.ppf(.975) + norm.ppf(.8)) * se
    print("holdout %d%%: n=%d, MDE %.4f orders = %.2f%% relative; cost if launches worth 5%%: %.0f orders/quarter" % (100 * h, nh, mde, 100 * mde / mu, nh * mu * 0.05))
# bare: sum of 12 test lifts
lifts = np.array([2.1, 1.4, 0.9, 1.8, 0.6, 1.2, 0.8, 1.5, 1.1, 0.7, 1.0, 0.9])
print("sum of lifts %.1f%%, compounded %.1f%%" % (lifts.sum(), 100 * (np.prod(1 + lifts / 100) - 1)))
# lab default check: E0 8, L 1.5, half-life = tau*ln2
print("half-life %.2f days" % (tau * np.log(2)))
# predict-then-play: days until the running average is within 1.5x and 1.25x the lasting lift
for k in (1.5, 1.25):
    T = next(T for T in range(1, 400) if (L + (E0 - L) * np.exp(-(np.arange(1, T + 1) - 1) / tau)).mean() <= k * L)
    print("average within %.2fx of lasting after %d days (%.1f weeks)" % (k, T, T / 7))
print("1%% holdout SE %.5f" % (2.4 * (1 / 80000 + 1 / 7920000) ** .5))
