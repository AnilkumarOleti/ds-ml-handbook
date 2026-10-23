"""Spot values for e1-exec-communication."""
base, new, visitors, value = 0.020, 0.023, 3_000_000, 900   # monthly visitors, contribution per order (Rs)
print("absolute +%.1f pts, relative +%.0f%%, per 1,000 visitors +%.0f orders" % (100 * (new - base), 100 * (new / base - 1), 1000 * (new - base)))
orders = visitors * (new - base)
print("extra orders/month %.0f, contribution/month Rs %.1f lakh, per year Rs %.1f crore" % (orders, orders * value / 1e5, 12 * orders * value / 1e7))
# interval: lift CI +0.1 to +0.5 pts
for d in (0.001, 0.005):
    print("  at %.1f pts: Rs %.1f crore/yr" % (100 * d, 12 * visitors * d * value / 1e7))
# truncated axis: bars 2.0 and 2.3 with axis from 1.9
for start in (0, 1.0, 1.9):
    vis = (2.3 - start) / (2.0 - start)
    print("axis from %.1f: bar ratio %.2f, lie factor %.2f" % (start, vis, (vis - 1) / (2.3 / 2.0 - 1)))
# frequency format: 70% chance forecast beats target
print("70%: 7 of 10 quarters like this one")
