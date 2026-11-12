import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c2-power-simulation"
R = ["ic", "mle"]

s1 = f"""<div class="problem"><p>A test randomises <strong>users</strong>, 10,000 per arm, and the metric is revenue per <strong>session</strong>. Users average 5.3 sessions, a quarter of them buy anything, and revenue per user is very skewed: mean ₹755, standard deviation ₹3,300.</p>
<p>The dashboard runs a t-test on all sessions. Before trusting it, you simulate 2,000 A/A tests, with no real difference, from data built to look like yours.</p>
<p>The dashboard's test calls <strong>17.5%</strong> of them significant at the 5% level. A user-level test calls 5.6%. And for a real <strong>+15%</strong> lift, the standard power formula promises 68% power, while simulation of the user-level test gives <strong>56%</strong>.</p>
<p>What is going on in each case, and what would you change?</p></div>
{attempt(S, 1)}{reveal(f'''<p><strong>The 17.5%</strong>: sessions from the same user are correlated, since heavy buyers buy in many sessions, but the session-level t-test treats them as independent. Its standard error is too small, so it finds "effects" three and a half times as often as it should. The fix is to analyse at the randomisation unit: revenue per user, or revenue per session with the delta method, both near 5% in simulation. See <a href="#a3-randomisation-unit">randomisation unit and ratio metrics</a>.</p>
<p><strong>The power gap</strong>: the formula assumes the average is close to normal. With revenue this skewed, 10,000 users are not enough for that to hold well, and a few huge spenders dominate the variance. Simulation measures the test you will actually run. Capping revenue at the 99th percentile raises simulated power to 67%, at the cost of measuring a slightly different metric.</p>
<p>Neither problem shows up in a formula. Both show up the moment you simulate. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>A fire drill.</strong> You do not learn whether an evacuation plan works by reading it. You stage a fire that does not exist and see how many people get out in time. Then you stage one in a different place.</p>
<p><strong>A flight simulator.</strong> Pilots practise engine failures in a machine that knows the right answer. The simulator does not tell you how often engines fail; it tells you how the pilot performs when one does.</p>
{table(["Idea", "Fire drill", "Flight simulator", "Simulated tests"], [
["What is staged", "A fire that is not there", "A failure that did not happen", "An effect you set yourself"],
["What is known", "Where the fire is", "What failed", "The true effect, including zero"],
["What is measured", "How many got out", "Whether the pilot recovered", "How often the test is significant"],
["With nothing happening", "False alarms", "Unnecessary aborts", "False positive rate (A/A)"],
["With something happening", "Evacuation rate", "Successful recoveries", "Power"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Both test a procedure by running it many times in a world where the right answer is known, so its error rates can be counted rather than assumed.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>A drill uses the real building.</strong> A simulation uses a model of your data, which can be wrong. Resampling real data, or real A/A splits, keeps it honest.</li>
<li><strong>A simulator pilot knows it is a test.</strong> A statistical test cannot tell, which is the point: its behaviour on fake data is its behaviour on real data, if the fake data is realistic.</li>
<li><strong>Drills are expensive.</strong> Simulated tests are cheap, so run thousands; the result has its own error, about √(p(1 − p)/N).</li></ul>
{tests([("Why run A/A simulations on resampled real users rather than on data drawn from a normal distribution?", "<p>The problems you are looking for, such as skew, within-user correlation and outliers, are properties of the real data. A normal model would hide them and report that everything is fine.</p>", True)])}"""

s3 = f"""<div class="fx">A/A simulation (false positive rate)
   repeat many times:
      split real users at random into two arms, or simulate from
      a model fitted to real data, with no effect
      run exactly the analysis you will use
   false positive rate = share of p-values &lt; 0.05   (should be 5%)
   and the p-values should look uniform

power by simulation
   same, but add a known effect to one arm
   power = share significant
   vary n, effect, metric definition, analysis

Monte Carlo error of a rate p from N simulations ≈ √(p(1 − p) / N)
   N = 2,000, p = 0.05  →  ± 0.5 points</div>
<ul>
<li><strong>Simulate the analysis you will run</strong>, end to end: the same filters, metric definitions, capping, CUPED and test. A formula covers only the idealised version.</li>
<li><strong>Use for non-standard designs</strong>: cluster randomisation, switchbacks, ratio metrics, quantile metrics, sequential looks, several metrics with corrections. Closed forms are often missing or wrong.</li>
<li><strong>How to add an effect</strong> matters: multiply revenue by 1.05 for everyone, or add it to buyers only, or change conversion. Each gives different power. Choose the one that matches what the feature would do.</li>
<li><strong>Uniform p-values</strong> under A/A are the full check: a histogram that piles up near zero means too many false positives, one that piles up near one means a test that is too conservative.</li>
<li><strong>Real A/A tests</strong> on the platform catch problems simulation cannot, such as bucketing bugs. Run both. {ref(2)}</li></ul>
{tests([("Your A/A simulation gives a false positive rate of 5.7% from 2,000 runs. Is the test miscalibrated?", "<p>Probably not. The simulation error is about ±0.5 points, so 5.7% is within about 1.5 standard errors of 5%. Run more simulations if the difference would matter.</p>", True),
("Why can simulated power differ from the formula's for a skewed metric?", "<p>The formula assumes the difference in means is normal with a known variance. With heavy tails, the sample variance is unstable and the test statistic is skewed at this sample size, so the real test can reject more or less often than the formula expects. Here it rejected less often; in other data it can be the other way, which is why you simulate.</p>")])}"""

s4 = f"""<h4>Worked: reading the A/A results</h4>
{table(["Analysis", "False positive rate, 2,000 A/A runs"], [
["t-test on revenue per session, sessions as units", "17.5%"], ["t-test on revenue per user", "5.6%"],
["Revenue per session, delta method on user totals", "5.7%"], ["t-test on revenue per user capped at the 99th percentile", "4.8%"]], narrow=True)}
<p>The simulation error at 5% is ±0.5 points, so the last three are all consistent with 5%. The first is three and a half times too high. Sessions per user average 5.3 and within-user correlation is substantial, so the session-level standard error is badly understated. Every "significant" session-level result on this dashboard is suspect.</p>
<h4>Half-worked: power by simulation</h4>
<p>With 10,000 users per arm, revenue multiplied by the lift for everyone, 1,000 simulations each:</p>
{table(["True lift", "Formula, user level", "Simulated, user level", "Simulated, capped at P99"], [
["+5%", "13%", "12%", "14%"], ["+10%", "37%", "29%", "38%"], ["+15%", "68%", "56%", "67%"]], narrow=True)}
<p>The team wants 80% power for a +10% lift. Roughly how many users per arm does the capped metric need, and what would you check before adopting the cap?</p>
{reveal("<p>Power of 38% at 10,000 means the effect is about 1.65 standard errors (1.96 − 0.31). Reaching 2.8 standard errors needs (2.8 ÷ 1.65)² ≈ <strong>2.9 times</strong> the users, about <strong>29,000 per arm</strong>, and a simulation at that size to confirm it. Before adopting the cap: that the A/A false positive rate is still 5% (it is, 4.8%), that the cap is computed from pooled data or pre-period data, not separately per arm, and that the business accepts that the capped metric understates gains concentrated among the biggest spenders.</p>")}
<h4>Bare: a design with no formula</h4>
<p>A delivery-fee test will switch fees on and off by city and hour (a switchback), across 12 cities for 4 weeks, with demand that has strong daily cycles and carries over between hours. How do you know what effect it can detect?</p>
{reveal("<p>Simulate it. Take last year's hourly orders for the 12 cities, apply the planned switching schedule, add a known effect in the treated hours, with and without carry-over into the following hour, and run the planned analysis thousands of times. Measure power and, with no effect added, the false positive rate. Try schedule variations, such as two-hour blocks or buffers between switches, and pick the one with valid error rates and the most power. See <a href='#a4-interference'>interference and marketplace experiments</a>.</p>")}
<h4>Predict, then play</h4>
<p>Predict what happens to the gap between the session-level and user-level false positive rates as the number of sessions per user grows.</p>
{reveal("<p>It widens. The variance inflation from clustering grows roughly like 1 + (sessions per user − 1) × the within-user correlation, so more sessions per user means a larger understatement. With one session each, the two tests agree.</p>")}
<div class="lab" data-lab="powersim"></div>
<pre class="code">import numpy as np
from scipy import stats
rng = np.random.default_rng(0)

def simulate(users, lift, n_sims=2000, cap=None):
    hits = 0
    for _ in range(n_sims):
        a = rng.choice(users, size=10_000)                 # resample real users
        b = rng.choice(users, size=10_000) * (1 + lift)
        if cap is not None:
            c = np.percentile(np.concatenate([a, b]), cap)
            a, b = np.minimum(a, c), np.minimum(b, c)
        hits += stats.ttest_ind(a, b, equal_var=False).pvalue &lt; 0.05
    return hits / n_sims       # lift = 0 gives the false positive rate</pre>
{tests([("Why compute the cap from both arms pooled, not separately for each arm?", "<p>A cap computed per arm depends on that arm's own data, including the effect, which can bias the comparison. Pooled data or a pre-period cap treats both arms the same.</p>", True),
("A/A simulation of a new metric gives p-values that pile up near 1. What does it mean?", "<p>The test is too conservative: its standard error is too large. It will rarely give false positives but also has less power than it should. Look for a variance formula that overcounts, such as a correction applied twice.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The simulated data resembles the real data", "A model of the data misses skew, seasonality or correlation", "Resample real users or periods instead"],
["The effect is added realistically", "The feature changes buyers only, or only conversion", "Simulate several effect shapes"],
["The simulated analysis is the real one", "The dashboard filters, caps or triggers differently", "Run the production code on simulated data"],
["Enough simulations", "Error rates estimated from 100 runs", "Report the Monte Carlo error"],
["Users are independent", "Network or marketplace effects link arms", "Simulate clusters; see interference"],
["The past predicts the test period", "A sale or a new market changes the variance", "Simulate on several historical windows"]])}
{tests([("Resampling real users gives a false positive rate of 5% for a metric. Six months later, a festival test shows strange results. Why might the earlier check not have covered it?", "<p>The resampled period had no festival. Variance and skew during a festival can be very different. Simulate on festival periods too, or on the most volatile weeks you have.</p>")])}"""

s6 = f"""{table(["Tool", "Answers", "Pick it when", "Watch out"], [
["Power formula", "Approximate n for a simple test", "Means or proportions, large samples, light tails", "Unreliable with heavy tails; optimistic with clustering"],
["Power by simulation", "Power of the exact analysis", "Skewed metrics, clusters, switchbacks, CUPED, corrections", "Needs a realistic data model"],
["A/A simulation", "False positive rate", "Any new metric or analysis", "Simulation error; run enough"],
["Real A/A tests", "Platform-level problems", "Before trusting a platform; periodically", "Costs traffic"],
["Bootstrap", "Uncertainty of one estimate", "A single dataset", "See <a href='#c2-bootstrap-simulation'>bootstrap</a>"],
["Permutation test", "An exact p-value under random assignment", "Small or odd samples", "Assumes exchangeability"]])}
{tests([("A colleague says simulation is overkill for a conversion-rate test with a million users. Agree?", "<p>Yes, for the power calculation: binary metrics at that scale are close to normal and the formula is fine. An A/A check is still worth doing once for the metric pipeline.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Revenue per session, randomised by user.</strong></p>
<p><strong>Orders per city-hour, randomised by city.</strong></p></div>
<div><p class="label">Pair 2</p>
<p><strong>GMV per buyer, with a handful of business buyers.</strong></p>
<p><strong>The 90th percentile of delivery time.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 has clustering.</strong> The analysis unit is smaller than the randomisation unit, so naive tests understate variance. A/A simulation exposes it; the fix is to analyse at the randomisation unit or use the delta method or cluster-robust errors.</p>
<p><strong>Pair 2 has awkward distributions.</strong> Extreme values or a quantile metric make normal-theory power unreliable. Simulation gives the true power, and shows whether capping or a different metric helps.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Running an A/A test once and declaring the platform sound because it was not significant. One A/A test has a 95% chance of passing even with a broken method. The check is the rate over many splits, real or simulated, and the shape of the p-value histogram. Large platforms run continuous A/A tests for this reason. {ref(2)}</p>
{tests([("A single A/A test came back with p = 0.4. The platform owner says it is validated. What do you say?", "<p>One test cannot measure a rate. A test with a 17% false positive rate passes a single A/A test 83% of the time. Run hundreds of A/A splits on historical data and look at the rate and the histogram.</p>")])}"""

s8 = f"""<ul>
<li><strong>A/A-simulate every new metric</strong> before it goes on a dashboard: 1,000 or more resampled splits, a rate and a histogram.</li>
<li><strong>Use real data</strong>: resample users or historical periods rather than inventing distributions.</li>
<li><strong>Simulate the production analysis code</strong>, not a reimplementation.</li>
<li><strong>Report Monte Carlo error</strong> with every simulated rate.</li>
<li><strong>Size non-standard designs by simulation</strong>, and keep the simulation in the repository so the next test can reuse it.</li>
<li><strong>Re-run the checks</strong> when the metric definition, traffic mix or platform changes.</li></ul>
{tests([("You can run 500 or 5,000 simulations. When does the extra cost pay?", "<p>When the answer is close to a threshold: a false positive rate of 6% with ±1 point of simulation error cannot be distinguished from 5%. For a rate of 17%, 500 is plenty.</p>")])}"""

s9 = f"""<ul>
<li><strong>Cap, transform or leave the tail alone?</strong> Capping raises power but changes the metric; log transforms change what a \"lift\" means; leaving it alone is honest but slow. Teams disagree, and the answer depends on whether big spenders' behaviour is the point.</li>
<li><strong>Simulate from a model or resample?</strong> Resampling keeps real quirks but cannot extrapolate to new conditions; models can, but carry their assumptions.</li>
<li><strong>How realistic must the effect be?</strong> A uniform multiplicative lift is convenient and often wrong. Effects concentrated in a few users make power much lower.</li>
<li><strong>Does a passing A/A simulation prove a test is valid?</strong> It proves it for the simulated conditions. Real platforms have bucketing, logging and timing issues that only real A/A tests catch.</li></ul>
{tests([("Make the case against capping revenue in experiments.", "<p>Big spenders can be where the effect is, and a cap hides changes in their behaviour. It also makes the reported lift a lift in a capped metric, which finance cannot use directly. Better variance reduction, such as CUPED, may give the power without changing the metric.</p>")])}"""

rungs = [
 {"ask": "What is an A/A test, and why would you simulate many of them?", "follow": ["What should the p-values look like?", "How many simulations?"],
  "weak": "<p>\"An A/A test checks that two identical groups look the same.\"</p>",
  "strong": "<p>An A/A test compares two arms with no difference, so any significant result is a false positive. Simulating many, by resampling real users, measures the method's actual false positive rate, which should be 5% with uniform p-values. A single A/A test cannot measure a rate. A thousand or more simulations give about ±0.7 points of precision.</p>"},
 {"ask": "A session-level t-test on revenue per session, with users randomised, gives 17.5% false positives in A/A simulation. Explain and fix it.", "follow": ["Why do user-level and delta-method tests pass?", "Which would you put on the dashboard?"],
  "model": "<p>sessions from the same user are correlated, so treating them as independent understates the standard error. Analyse at the randomisation unit: revenue per user, or revenue per session with the delta method on user totals, both near 5%. For a per-session metric, the delta method keeps the metric the business asked for with a correct error.</p>",
  "weak": "<p>Suggests a smaller significance level to compensate.</p>",
  "strong": "<p><b>Must have.</b> Names clustering and the mismatch of randomisation and analysis units.</p><p><b>Strong signal.</b> Chooses the delta method to keep the metric and notes the gap grows with sessions per user.</p>"},
 {"ask": "The formula says 68% power for +15%, simulation says 56%. Which do you believe, and what do you do?", "follow": ["Why do they differ?", "Does capping help, and what does it cost?"],
  "weak": "<p>\"The formula, because it is exact.\"</p>",
  "strong": "<p>The simulation, if it resamples real users and runs the real analysis: the formula assumes normality that heavy-tailed revenue does not reach at this size. Options: more users, CUPED, or a cap at the 99th percentile, which raises simulated power to about 67% while keeping false positives at 5%. The cap measures a slightly different metric, so agree that with the business first.</p>", "roles": ["ic", "mle"]},
 {"ask": "Design how an experimentation platform validates a new metric before teams can use it.", "follow": ["What counts as a pass?", "How often is it re-run?"],
  "weak": "<p>\"Check the metric matches the dashboard.\"</p>",
  "strong": "<p>Resample a few months of real users into thousands of A/A splits and run the production analysis: the false positive rate must be within simulation error of 5% and the p-values uniform. Simulate power for a few realistic effect shapes and publish the minimum detectable effect at typical traffic. Run real A/A tests on the platform periodically. Re-validate when the definition or traffic mix changes.</p>", "roles": ["ic", "mle"]},
 {"ask": "Your audit shows a headline dashboard metric has had a 17% false positive rate for a year. Teams have shipped on it. What do you do?", "follow": ["Do you re-open past decisions?", "How do you tell the teams?"],
  "weak": "<p>Quietly fixes the metric.</p>",
  "strong": "<p>Fix the metric first, then re-run the past year's tests with the correct analysis and list which conclusions change. Share the finding plainly with the teams and leadership, with that list, framed as a platform fault, not theirs. Revisit only the launches whose decisions flip and that still matter. Add A/A simulation to the metric review so it cannot recur.</p>", "roles": ["lead", "ic"]},
]

page(S, "C2", "Power and false positive rates by simulation",
     "Power formulas and standard tests assume tidy data. Skewed revenue, clustered sessions and unusual designs break those assumptions without any warning. Simulating many A/A and A/B tests on data like yours counts how often your actual analysis is wrong.",
     "power analysis simulation a/a test false positive rate type i error p-value histogram uniform resampling clustered sessions delta method capping winsorising heavy tails switchback monte carlo error",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Instead of trusting formulas built for tidy data, run your actual analysis thousands of times on resampled real data, with no effect to count false positives and with a known effect to measure power, because skew, clustering and unusual designs break the formulas silently.",
     ["Simulate the analysis you will actually run", "A/A: false positive rate and uniform p-values", "Add a known effect for power; choose its shape", "Clustering and skew are what formulas miss", "Report the simulation's own error"],
     [("a3-sample-size-power", "Sample size and power"), ("a3-randomisation-unit", "Randomisation unit and ratio metrics"), ("c2-bootstrap-simulation", "Bootstrap and simulation")],
     [("a4-cuped", "CUPED and variance reduction"), ("a4-interference", "Interference and marketplace experiments"), ("c3-metric-sensitivity", "Metric sensitivity")],
     sources=[("Kohavi, Tang and Xu, Trustworthy Online Controlled Experiments, Cambridge University Press, 2020, chapters 18 and 19", "https://experimentguide.com/"),
              ("Kohavi, Deng, Frasca, Walker, Xu and Pohlmann, \"Online Controlled Experiments at Large Scale\", KDD 2013", "https://doi.org/10.1145/2487575.2488217")],
     sec_roles={11: ["lead", "ic", "mle"]})
