"""Spot values for c3-metric-sensitivity."""
import numpy as np
from scipy.stats import norm
n = 500_000
k = norm.ppf(.975) + norm.ppf(.8)
mde = lambda cv, n=n: k * cv * np.sqrt(2 / n)
cvs = {"GMV per user": 8.0, "Buyers per user (4%)": np.sqrt(.96 / .04), "Add-to-cart users (25%)": np.sqrt(.75 / .25), "Sessions per user": 1.5}
for m, c in cvs.items(): print("%-26s CV %.2f MDE %.2f%%" % (m, c, 100 * mde(c)))
print("ratio GMV / add-to-cart %.1f" % (mde(8) / mde(np.sqrt(3))))
print("GMV capped CV 5: %.2f%%; CUPED rho .6 on capped: %.2f%%" % (100 * mde(5), 100 * mde(5 * np.sqrt(1 - .36))))
print("users needed for GMV 1%% MDE: %.1f M per arm" % ((k * 8 / .01) ** 2 * 2 / 1e6))
pw = lambda eff, cv, n=n: norm.cdf(eff / (cv * np.sqrt(2 / n)) - norm.ppf(.975))
for eff in (.01, .02):
    print("power for %d%%: GMV %.2f capped+CUPED %.2f ATC %.2f" % (100 * eff, pw(eff, 8), pw(eff, 4), pw(eff, np.sqrt(3))))
# corpus: 200 tests, sig share; sensitivity
