"""Spot values for c5-text-analytics."""
po = 170 / 200; pa, pb = 65 / 200, 65 / 200
pe = pa * pb + (1 - pa) * (1 - pb)
print("kappa po %.3f pe %.4f kappa %.3f" % (po, pe, (po - pe) / (1 - pe)))
se, sp, obs = .90, .97, .18
pi = (obs - (1 - sp)) / (se - (1 - sp))
print("Rogan-Gladen true share %.4f" % pi)
prec = se * pi / obs
print("implied precision %.3f" % prec)
for true in (.02, .05, .17):
    o = se * true + (1 - sp) * (1 - true)
    print("true %.2f -> observed %.4f, precision %.2f" % (true, o, se * true / o))
# monthly trend artefact: prompt change raises sensitivity .90 -> .95 and lowers sp .97 -> .95
o1 = .90 * .17 + .03 * .83; o2 = .95 * .17 + .05 * .83
print("same true 17%%: observed %.3f before, %.3f after a prompt change (+%.0f%%)" % (o1, o2, 100 * (o2 / o1 - 1)))
# sample size for precision estimate: 300 labelled, 54 tagged positive -> CI of precision
import math
n_pos = 54; p = .85; print("precision CI half-width with %d positives: %.3f" % (n_pos, 1.96 * math.sqrt(p * (1 - p) / n_pos)))
