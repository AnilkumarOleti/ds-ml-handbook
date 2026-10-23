"""Spot values for d3-system-design: the counterfeit-listing triage."""
import math
bands = [  # (name, mean P(counterfeit), listings per day)
    ("Very high", 0.95, 20_000), ("High", 0.60, 30_000), ("Medium", 0.20, 60_000),
    ("Low", 0.05, 200_000), ("Very low", 0.002, 9_690_000)]
total = sum(n for _, _, n in bands); bad = sum(p * n for _, p, n in bands)
print("listings %d, counterfeit %.0f (%.2f%%)" % (total, bad, 100 * bad / total))
MISS, BLOCK, REVIEW = 2000, 300, 40
for name, p, n in bands:
    print("%-9s allow %6.1f block %6.1f review %5.1f" % (name, p * MISS, (1 - p) * BLOCK, REVIEW))
print("review beats allow when p > %.3f; block beats review when p > %.3f; block beats allow when p > %.3f" %
      (REVIEW / MISS, 1 - REVIEW / BLOCK, BLOCK / (MISS + BLOCK)))
def plan(cap, MISS=MISS, BLOCK=BLOCK, REVIEW=REVIEW):
    """Greedy: review where it saves most over the best non-review action, up to capacity."""
    rows, left = [], cap
    best_nr = lambda p: min(p * MISS, (1 - p) * BLOCK)
    order = sorted(bands, key=lambda b: -(best_nr(b[1]) - REVIEW))
    alloc = {}
    for name, p, n in order:
        gain = best_nr(p) - REVIEW
        r = min(n, left) if gain > 0 else 0
        alloc[name] = r; left -= r
    cost = caught = blocked_genuine = 0
    for name, p, n in bands:
        r = alloc[name]; rest = n - r
        cost += r * REVIEW; caught += r * p
        if p * MISS <= (1 - p) * BLOCK:
            cost += rest * p * MISS; act = "allow"
        else:
            cost += rest * (1 - p) * BLOCK; caught += rest * p; blocked_genuine += rest * (1 - p); act = "block"
        rows.append((name, r, rest, act))
    return rows, cost, caught, blocked_genuine
for cap in (80_000, 50_000, 150_000):
    rows, cost, caught, bg = plan(cap)
    print("cap", cap, rows)
    print("  cost/day %.1f lakh, counterfeits stopped %.0f of %.0f (%.1f%%), genuine blocked %.0f" % (cost / 1e5, caught, bad, 100 * caught / bad, bg))
# allow-everything and block-band-1-only baselines
allow_all = bad * MISS
print("allow everything: %.1f lakh/day" % (allow_all / 1e5))
# bare: GPUs
imgs = 10_000_000 * 5; avg = imgs / 86400; peak = 3 * avg
print("images/s avg %.0f peak %.0f -> GPUs at 400/s: %.2f" % (avg, peak, peak / 400))
casc = peak * 0.2
print("cascade 20%%: %.0f/s -> %.2f GPUs" % (casc, casc / 400))
print("listings/s avg %.0f peak %.0f" % (10e6 / 86400, 3 * 10e6 / 86400))
