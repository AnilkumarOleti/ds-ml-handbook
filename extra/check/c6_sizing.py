"""Spot values for c6-opportunity-sizing."""
G = 1000.0  # category GMV, crore a year
pm = G * 0.10
exposed = G * 0.40 * 0.60
lift_win, persist, pwin = 0.030, 0.60, 8 / 20
print("PM %.0f cr; exposed GMV %.0f cr" % (pm, exposed))
iw = exposed * lift_win * persist
print("if it works: %.2f cr (lift %.1f%% x persistence %.0f%% = %.2f%%)" % (iw, 100 * lift_win, 100 * persist, 100 * lift_win * persist))
ev = pwin * iw
print("expected value of the idea: %.2f cr; PM / if-works %.0fx" % (ev, pm / iw))
lo = G * .35 * .50 * .015 * .5; hi = G * .45 * .70 * .045 * .8
print("if-works range low %.2f high %.2f" % (lo, hi))
# all 20 tests average 1.2%: 8 winners avg 3.0 -> losers avg
print("losers avg %.2f%%" % ((1.2 * 20 - 3.0 * 8) / 12))
# bottom-up: 2,000 offers a day, 35% accepted, average order 1,800, 10% incremental
bu = 2000 * .35 * 1800 * .10 * 365 / 1e7
print("offer GMV a year %.1f cr" % (2000 * .35 * 1800 * 365 / 1e7))
print("bottom-up incremental %.2f cr a year" % bu)
# cost and value of a cheap test: engineering 2 cr full build; prototype test 0.3 cr
print("EV - cost full build: %.2f cr" % (ev - 2.0))
# with a 0.3 cr prototype test that reveals win/lose: build only if it wins
print("test first: %.2f cr" % (pwin * (iw - 2.0) - 0.3))
