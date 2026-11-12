"""Spot values for c6-qual-quant."""
pop = [.2, .3, .5]; rr = [.18, .093, .032]; ps = [4.6, 4.4, 3.9]
resp = [p * r for p, r in zip(pop, rr)]; tot = sum(resp)
sh = [x / tot for x in resp]
print("overall response %.3f; respondent shares %s" % (tot, [round(x, 3) for x in sh]))
unw = sum(s * p for s, p in zip(sh, ps)); w = sum(p * q for p, q in zip(pop, ps))
print("unweighted %.2f weighted %.2f" % (unw, w))
n = 100_000 * tot
wts = [p / s for p, s in zip(pop, sh)]
ess = (sum(s * n * wt for s, wt in zip(sh, wts))) ** 2 / sum(s * n * wt**2 for s, wt in zip(sh, wts))
print("respondents %.0f, weights %s, Kish ESS %.0f (%.0f%%)" % (n, [round(x, 2) for x in wts], ess, 100 * ess / n))
# share 'satisfied' (4-5) unweighted vs weighted given segment shares satisfied
sat = [.88, .82, .65]
print("satisfied unweighted %.2f weighted %.2f" % (sum(s * q for s, q in zip(sh, sat)), sum(p * q for p, q in zip(pop, sat))))
# stated vs revealed: 40% of churned respondents say price; churned buyers who saw a price cut test: retention +1pt
