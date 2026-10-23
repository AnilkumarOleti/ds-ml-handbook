"""Spot values for e2-building-team: hiring funnel and model choice."""
def funnel(hires, rates, hours):
    need = hires
    out = []
    for (name, r), hr in zip(reversed(rates), reversed(hours)):
        need = need / r; out.append((name, need, hr))
    out.reverse()
    tot = sum(n * hr for _, n, hr in out)
    return out, tot
rates = [("Application screen", 0.30), ("Phone screen", 0.50), ("Take-home and review", 0.45), ("Onsite loop", 0.35), ("Offer accepted", 0.70)]
hours = [0.1, 1.0, 1.5, 5.0, 0.0]   # interviewer hours per candidate entering the stage
out, tot = funnel(4, rates, hours)
for name, n, hr in out: print("%-22s enter %6.1f  hours %.0f" % (name, n, n * hr))
print("total interviewer hours %.0f" % tot)
p = 1
for _, r in rates: p *= r
print("applications per hire %.0f" % (1 / p))
# cheaper: raise phone-screen pass precision -> take-home pass 0.6
rates2 = [("Application screen", 0.30), ("Phone screen", 0.40), ("Take-home and review", 0.60), ("Onsite loop", 0.35), ("Offer accepted", 0.70)]
out2, tot2 = funnel(4, rates2, hours)
print("stricter phone screen: total hours %.0f; applications %.0f" % (tot2, out2[0][1]))
# offer acceptance 0.5
rates3 = rates[:-1] + [("Offer accepted", 0.5)]
out3, tot3 = funnel(4, rates3, hours)
print("acceptance 50%%: hours %.0f, applications %.0f" % (tot3, out3[0][1]))
# capacity: 6 squads, 8 people. Hub-and-spoke: 6 embedded, 2 hub.
squads, heads = 6, 8
print("embedded share %.0f%%" % (100 * 6 / 8))
# ramp: new analyst productive 50% month 1-2, 80% month 3, 100% after
print("first-quarter output of 4 new hires = %.1f analyst-months of 12" % (4 * (0.5 + 0.5 + 0.8)))
# predict-then-play: onsite pass rate 35% -> 50%
rates4 = rates[:3] + [("Onsite loop", 0.50), rates[4]]
out4, tot4 = funnel(4, rates4, hours)
print("onsite 50%%: applications %.0f, hours %.0f" % (out4[0][1], tot4))
