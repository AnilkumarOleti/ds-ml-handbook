"""Spot values for c4-incrementality."""
from scipy.stats import norm
# s1: brand search, 4,000,000 eligible users, 10% held out
N, h = 4_000_000, 0.10
ne, nh = N * (1 - h), N * h
pe, ph = 0.0200, 0.0195
spend, value, attributed = 40e5, 800, 8000
inc = ne * (pe - ph)
print("exposed %d holdout %d incremental orders %.0f" % (ne, nh, inc))
print("attributed return %.2f, incremental return %.2f, share incremental %.1f%%" % (attributed * value / spend, inc * value / spend, 100 * inc / attributed))
print("monthly profit if attributed is believed: %.1f lakh; actual: %.1f lakh" % ((attributed * value - spend) / 1e5, (inc * value - spend) / 1e5))
se = (pe * (1 - pe) / ne + ph * (1 - ph) / nh) ** .5
lo, hi = (pe - ph) - 1.96 * se, (pe - ph) + 1.96 * se
print("SE %.6f; diff CI %.4f%% to %.4f%%; orders %.0f to %.0f" % (se, 100 * lo, 100 * hi, ne * lo, ne * hi))
print("incremental return range %.2f to %.2f" % (ne * lo * value / spend, ne * hi * value / spend))
# break-even lift
be = spend / value / ne
print("break-even lift %.4f pts = %.0f orders" % (100 * be, spend / value))
# holdout 2% vs 10% vs 30%
def ci_half(h, p=0.0195, N=N):
    ne, nh = N * (1 - h), N * h
    return 1.96 * (p * (1 - p) / ne + p * (1 - p) / nh) ** .5 * ne
def power(h, d=0.0005, p=0.0195, N=N):
    ne, nh = N * (1 - h), N * h
    se = (p * (1 - p) / ne + p * (1 - p) / nh) ** .5
    return norm.cdf(d / se - 1.96)
for hh in (.02, .05, .10, .20, .30, .50):
    print("holdout %2d%%: +- %.0f orders, power %.2f, cost of holdout %.0f orders" % (100 * hh, ci_half(hh), power(hh), N * hh * .0005))
# half-worked: geo test DiD
paused_b, paused_d, ctrl_b, ctrl_d = 50_000, 47_000, 60_000, 61_200
cf = paused_b * ctrl_d / ctrl_b
print("counterfactual %.0f, incremental %.0f, iROAS %.2f on 10 lakh" % (cf, cf - paused_d, (cf - paused_d) * value / 10e5))
# bare: average vs marginal
o40, o50 = 6000, 6400
print("average return at 40L %.2f; marginal from 40 to 50L %.2f; avg at 50L %.2f" % (o40 * value / 40e5, (o50 - o40) * value / 10e5, o50 * value / 50e5))
