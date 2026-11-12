"""Spot values for c5-activation."""
B = [("0", 3000, .10), ("1-2", 3000, .25), ("3-4", 1500, .45), ("5-9", 1500, .70), ("10+", 1000, .78)]
N = sum(b[1] for b in B); Rt = sum(b[1] * b[2] for b in B)
print("sellers %d retained %.0f (%.1f%%)" % (N, Rt, 100 * Rt / N))
lo = {"1": 1, "3": 2, "5": 3, "10": 4}
for k, i in lo.items():
    hit = B[i:]; nh = sum(b[1] for b in hit); rh = sum(b[1] * b[2] for b in hit)
    miss = B[:i]; nm = sum(b[1] for b in miss); rm = sum(b[1] * b[2] for b in miss)
    print(">=%s: hitters %d (%.0f%%), retained among hitters %.1f%%, among others %.1f%%, share of retained who hit %.1f%%, gap %.1f pts" % (k, nh, 100 * nh / N, 100 * rh / nh, 100 * rm / nm, 100 * rh / Rt, 100 * (rh / nh - rm / nm)))
# nudge experiment: share hitting 5 rises 25% -> 33%, retention 35.6% -> 36.6%
print("Wald: %.1f pts per seller moved over the threshold" % (100 * 0.010 / 0.08))
# immortal time: 1,200 of the 3,000 zero-listing sellers had stopped visiting before day 7
