import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c2-monte-carlo"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>You are sizing a buyer protection programme. It costs <strong>₹15 crore</strong> a year. Its value is eligible buyers × share who adopt × lift in their annual spend × annual spend. The team's ranges:</p>
{table(["Input", "Low", "Most likely", "High"], [
["Eligible buyers", "4 million", "5 million", "6 million"], ["Adoption", "5%", "10%", "20%"],
["Lift in spend among adopters", "3%", "6%", "12%"], ["Annual spend", "₹6,000", "₹7,000", "₹8,000"]], narrow=True)}
<p>The deck multiplies the most likely values: <strong>₹21 crore</strong>. A sceptic multiplies the lows (₹3.6 crore) and the highs (₹115 crore) and says the range is useless.</p>
<p>What is the chance the programme pays for itself? Is ₹21 crore the most likely outcome?</p></div>
{attempt(S, 1)}{reveal('''<p>Simulate: draw each input from its range, say a triangular distribution with those three points, multiply, and repeat a million times.</p>
<ul><li>Median <strong>₹26.7 crore</strong>; 80% of outcomes fall between <strong>₹15.6 and ₹44.2 crore</strong>; the mean is ₹28.6 crore.</li>
<li>Chance of exceeding ₹15 crore: about <strong>92%</strong>.</li></ul>
<p>The deck's ₹21 crore is not the most likely outcome, nor the median. Adoption and lift are skewed upwards (most likely 10%, but up to 20%), so their averages are above their most likely values, and the product of most likely values sits below the middle of the distribution. The sceptic's range needs every input at its extreme at once, which almost never happens: in a million draws the largest was ₹103 crore, and only about 3 in 10,000 exceeded ₹80 crore.</p>
<p>The decision-relevant statement: about a 9-in-10 chance of covering the cost, assuming the inputs are independent and the ranges are honest. The weakest link is the lift range, which an experiment could narrow.</p>''')}"""

s2 = f"""<p><strong>Packing for a trip.</strong> You could pack for the worst weather on every day at once, snow and heatwave together, and carry three suitcases. Or you could think about the likely range of each day and pack for the combination that is plausible. Real days are rarely all extreme in the same way.</p>
<p><strong>A commute with three legs.</strong> A walk, a train and a bus, each 10 to 30 minutes. Adding the worst cases says 90 minutes. Adding the typical ones says 50. Asking "how often will I be later than an hour?" needs the spread of the total, which you get by imagining many mornings.</p>
{table(["Idea", "Packing", "Commute", "Sizing"], [
["The inputs", "Each day's weather", "Each leg's time", "Adoption, lift, spend"],
["Worst-case thinking", "Snow and heat every day", "All three legs at their worst", "Multiply all the lows"],
["Point thinking", "Pack for average weather", "Add the typical times", "Multiply the most likely values"],
["Simulation", "Imagine many possible weeks", "Imagine many mornings", "Draw inputs, multiply, repeat"],
["The useful answer", "What fits most weeks", "Chance of being later than an hour", "Chance of clearing break-even"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>When an outcome combines several uncertain parts, the useful answer is the distribution of the combination, which neither the all-worst nor the all-typical case describes.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Weather on different days is nearly independent.</strong> Business inputs often move together: a programme that more people adopt may help each of them less. Ignoring that changes the spread.</li>
<li><strong>Commute times are measured every day.</strong> Sizing inputs are often guesses. A simulation of guesses is only as good as the guesses, though it makes them explicit.</li>
<li><strong>Both have a natural unit of repetition.</strong> A sizing happens once; the probability is a statement about your uncertainty, not a frequency.</li></ul>
{tests([("Why does multiplying the most likely values not give the most likely product?", "<p>The most likely value of a product depends on the whole shape of each distribution. With skewed inputs, the product's centre sits away from the product of modes, here above it.</p>", True)])}"""

s3 = f"""<div class="fx">Monte Carlo simulation
   1. write the outcome as a function of uncertain inputs
         value = buyers × adoption × lift × spend
   2. give each input a distribution
         triangular(low, likely, high), lognormal, beta, uniform …
   3. say how inputs move together (correlation, shared drivers)
   4. draw all inputs, compute the outcome; repeat N times
   5. report percentiles (P10, P50, P90), P(outcome &gt; threshold),
      and which input drives the spread

error of a simulated probability ≈ √(p(1 − p) / N)
   N = 10,000, p = 0.9  →  ± 0.003</div>
<ul>
<li><strong>Inputs are beliefs, made explicit.</strong> A range of 3% to 12% for lift says what the team thinks, and the simulation shows what that belief implies.</li>
<li><strong>Triangular or PERT distributions</strong> suit expert ranges with a most likely value. Use data where you have it: past experiment lifts, adoption of similar features.</li>
<li><strong>Correlation matters.</strong> Positively related inputs widen the spread; negatively related ones narrow it. Model a shared driver directly when you can.</li>
<li><strong>Tornado analysis</strong> shows which input's uncertainty matters most: vary one at a time across its range and see how much the outcome moves. That input is where to spend research.</li>
<li><strong>Scenario planning</strong> is the same method applied to forecasts: simulate demand, capacity and prices together to see how often a plan breaks.</li></ul>
{tests([("Why report P(value > cost) rather than the expected value alone?", "<p>Two programmes with the same expected value can carry very different risk of losing money. The probability speaks to the decision directly, and leadership can weigh it against their appetite for risk.</p>", True),
("How many simulation draws are enough?", "<p>Enough that the numbers you report stop moving. For a probability near 0.9, 10,000 draws give about ±0.3 points; tail percentiles such as P99 need more.</p>")])}"""

s4 = f"""<h4>Worked: five draws by hand</h4>
{table(["Draw", "Buyers", "Adoption", "Lift", "Spend", "Value, ₹ crore"], [
["1", "5.2 M", "8%", "5%", "₹7,200", "15.0"], ["2", "4.6 M", "14%", "9%", "₹6,500", "37.7"],
["3", "5.5 M", "7%", "4%", "₹7,600", "11.7"], ["4", "4.9 M", "12%", "7%", "₹6,900", "28.4"],
["5", "5.1 M", "18%", "10%", "₹7,100", "65.2"]], narrow=True)}
<p>Two of five draws are at or below ₹15 crore, and one is far above. With five draws you see the shape; with a million you get stable percentiles. Notice draw 5: high adoption and high lift together give a large value. If the two were negatively related, such draws would be rarer.</p>
<h4>Half-worked: correlated inputs</h4>
<p>Suppose broader adoption brings less committed buyers, so adoption and lift are negatively correlated (−0.6). Simulated: P10 ₹18.7 crore, median ₹26.5, P90 ₹37.3. With a positive correlation of +0.6: P10 ₹13.5, median ₹26.9, P90 ₹50.6. Find the chance of clearing ₹15 crore in each case and explain why the median barely moves.</p>
{reveal("<p>About <strong>98%</strong> with negative correlation and <strong>86%</strong> with positive, against 92% if independent. The median is about the same because correlation mostly changes how often the two inputs are extreme together, which moves the tails, not the centre. For a go or no-go decision near the threshold, the correlation assumption can matter more than the ranges.</p>")}
<h4>Bare: which input to research</h4>
<p>Holding the others at their medians, moving adoption from 5% to 20% moves the value from ₹12 to ₹48 crore. Moving lift from 3% to 12% does the same, ₹12 to ₹48 crore. Moving buyers across their range moves it from ₹22 to ₹32 crore, and spend from ₹23 to ₹31 crore. The research team can run one study. Which, and what kind?</p>
{reveal("<p>Adoption and lift dominate, equally in this tornado, each about four times the swing of buyers or spend. Lift is the better target, because an experiment on a pilot group measures it causally, and the pilot also gives an adoption rate. Buyers and spend are known well enough. The point is to narrow the inputs that drive the decision, not the easiest ones.</p>")}
<h4>Predict, then play</h4>
<p>Predict whether widening the top of the lift range from 12% to 20%, with everything else unchanged, raises the chance of clearing ₹15 crore by much.</p>
{reveal("<p>Only a little. It stretches the upper tail, which was already above break-even, and it raises the median somewhat. The chance of clearing the cost depends on the lower parts of the ranges. To lower the risk, evidence that rules out the low end is worth more than optimism about the high end.</p>")}
<div class="lab" data-lab="montecarlo"></div>
<pre class="code">import numpy as np
rng = np.random.default_rng(0)
N = 1_000_000
tri = lambda lo, mode, hi: rng.triangular(lo, mode, hi, N)
value = tri(4e6, 5e6, 6e6) * tri(.05, .10, .20) * tri(.03, .06, .12) * tri(6000, 7000, 8000) / 1e7
np.percentile(value, [10, 50, 90])     # about 15.6, 26.7, 44.2 crore
(value > 15).mean()                     # about 0.92</pre>
{tests([("A colleague uses uniform distributions instead of triangular for the same ranges. What happens to the spread, and why?", "<p>It widens, because a uniform puts as much weight near the extremes as near the most likely value. The median moves towards the midpoint of each range.</p>", True),
("Your P90 changes by ₹0.8 crore every time you rerun with 1,000 draws. What do you do?", "<p>Use more draws, such as 100,000, until it is stable to the precision you report, and fix the random seed so a rerun reproduces the numbers.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The ranges are honest", "Owners give optimistic ranges for their own projects", "Compare past ranges with outcomes; ask for a range from a sceptic"],
["Inputs are independent", "Adoption and lift, or price and volume, move together", "Ask what would make two inputs both high; model the shared driver"],
["The formula is right", "A missing term such as cannibalisation of existing spend", "Walk the formula with finance; check units"],
["The distributions' shapes", "Fat tails not captured by a triangle", "Check against data where it exists"],
["Enough draws", "Unstable tail percentiles", "Rerun with different seeds"],
["The probability is a frequency", "It is a statement of belief", "Say so in the readout"]])}
{tests([("The simulation says 92% chance of clearing break-even. A year later the programme misses. Was the simulation wrong?", "<p>Not necessarily: 8% events happen. Check whether the miss came from an input outside its range, which says the ranges were too narrow, or from a combination inside them. Track sizings against outcomes over many programmes to calibrate the team's ranges.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Point estimate", "One number", "Quick order of magnitude", "Hides risk; often off-centre"],
["Low / likely / high scenarios", "Three stories", "Communicating to a wide audience", "Scenarios are not probabilities"],
["Monte Carlo", "The distribution of the outcome", "Several uncertain inputs combine", "Garbage in, garbage out"],
["Tornado chart", "Which input matters most", "Deciding what to research", "One at a time ignores interactions"],
["Bootstrap", "Uncertainty from data you have", "Inputs come from a sample", "See <a href='#c2-bootstrap-simulation'>bootstrap and simulation</a>"],
["Bayesian model", "Uncertainty combining data and priors", "Some inputs have data, some only beliefs", "More work; same honesty needed"]])}
{tests([("For a board slide, would you show the Monte Carlo distribution or low, likely and high scenarios?", "<p>Scenarios with the probability attached: \"base case ₹27 crore; a 1-in-10 chance it is below ₹16 crore; a 1-in-10 chance above ₹44 crore\". The distribution is the analysis; percentiles are how it is told.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Sizing a new category launch.</strong> Sellers, listings, conversion and price are each uncertain.</p>
<p><strong>A warehouse capacity plan.</strong> Demand, pick rate and staffing are each uncertain.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A revenue forecast for next quarter.</strong> Finance wants a number and a range.</p>
<p><strong>An experiment's projected annual value.</strong> The lift has a confidence interval.</p></div></div>
{reveal('''<p><strong>Pair 1 is sizing and capacity.</strong> Several uncertain inputs multiply or combine; the question is how often the outcome crosses a line: break-even, or capacity.</p>
<p><strong>Pair 2 propagates measured uncertainty.</strong> Draw the lift from its interval, combine it with uncertain reach and persistence, and report the projection as a range rather than the point lift times traffic.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Precise-looking outputs from invented inputs. A simulation with ten thousand draws produces a crisp P90 of ₹44.2 crore, and the precision of the number is taken for the precision of the knowledge. The decimal reflects the arithmetic, not the inputs, which were three guesses each. Round, state the inputs on the same slide, and show what happens when the key range is wrong.</p>
{tests([("A sizing deck shows 'P50 ₹26.71 crore'. What would you change?", "<p>Round to ₹27 crore or even ₹25 to ₹30 crore, list the input ranges and their sources beside it, and show the effect of the most uncertain input. The second decimal implies knowledge nobody has.</p>")])}"""

s8 = f"""<ul>
<li><strong>Write the formula with finance or the business owner</strong> before any distribution.</li>
<li><strong>Ground ranges in data</strong>: past launches' adoption, past experiments' lifts, shrunk towards typical values.</li>
<li><strong>Ask two people for ranges</strong>, the owner and a sceptic, and run both.</li>
<li><strong>Model correlation explicitly</strong> or through shared drivers. Test the result's sensitivity to it.</li>
<li><strong>Report P10, P50, P90 and P(clears the bar)</strong>, rounded, with the tornado.</li>
<li><strong>Keep a log of sizings and outcomes.</strong> After a year, check whether 80% of outcomes fell in the P10 to P90 ranges.</li></ul>
{tests([("After a year, only 40% of outcomes fell inside the stated P10 to P90 ranges. What does that tell you?", "<p>The ranges are overconfident: they should contain 80%. Widen future ranges, or anchor them on past outcomes. Typical overconfidence is a well-known pattern in expert estimates.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is simulation false precision?</strong> Sceptics say three guesses per input do not deserve a probability distribution. Defenders say the guesses are being multiplied anyway, and simulation is the honest way to do it.</li>
<li><strong>Triangular or something smoother?</strong> Triangles are easy to elicit and explain; PERT or lognormal shapes are smoother and often more realistic in the tails. The choice matters less than the ranges.</li>
<li><strong>Should leadership see distributions?</strong> Some find percentiles clarifying; others anchor on the median and ignore the rest. Framing as \"chance of clearing the bar\" usually works best.</li>
<li><strong>Who sets the ranges?</strong> Owners know the most and are the most optimistic. Separating who sizes from who benefits improves calibration but costs knowledge.</li></ul>
{tests([("Make the case for a simple low-likely-high table over a simulation.", "<p>It is transparent, needs no tooling, and invites debate about each input. For a decision far from break-even, the simulation adds little. Simulation earns its keep near the threshold, or when many inputs combine.</p>")])}"""

rungs = [
 {"ask": "What is Monte Carlo simulation, and when would you use it for sizing?", "follow": ["Why not multiply the most likely values?", "What do you report?"],
  "weak": "<p>\"Running a model many times with random numbers.\"</p>",
  "strong": "<p>Write the outcome as a function of uncertain inputs, give each a distribution, draw them many times and compute the outcome each time, so you get the distribution of the result. Use it when several uncertain inputs combine and the decision depends on a threshold. Report percentiles and the probability of clearing the threshold, plus which input drives the spread.</p>"},
 {"ask": "Buyers 4 to 6 million, adoption 5 to 20%, lift 3 to 12%, spend ₹6,000 to ₹8,000, cost ₹15 crore. The deck says ₹21 crore. What is the chance it pays back?", "follow": ["Why is the median above ₹21 crore?", "What if adoption and lift are negatively correlated?"],
  "model": "<p>simulating triangular inputs gives a median near ₹27 crore, an 80% range of about ₹16 to ₹44 crore, and roughly a 92% chance of exceeding ₹15 crore. The median is above the deck's number because adoption and lift are skewed upwards. With negative correlation the spread narrows and the chance rises to about 98%; with positive, it falls to about 86%.</p>",
  "weak": "<p>Gives the ₹21 crore point estimate, or multiplies the extremes.</p>",
  "strong": "<p><b>Must have.</b> Simulates, reports a probability against the cost, and explains the skew.</p><p><b>Strong signal.</b> Raises correlation and says which input to research.</p>"},
 {"ask": "How would you choose the distributions for the inputs?", "follow": ["What if there is no data at all?", "How do you avoid optimism?"],
  "weak": "<p>\"Use normal distributions for everything.\"</p>",
  "strong": "<p>From data where it exists: past launch adoption, past experiment lifts shrunk towards typical values, and spend from the warehouse. Where it does not, elicit low, likely and high from more than one person, including a sceptic, and use triangular or PERT shapes that respect the bounds. Check calibration over time against outcomes.</p>", "roles": ["ic"]},
 {"ask": "Design a sizing process the product org uses for every major investment.", "follow": ["Who owns the inputs?", "How do you know if it is working?"],
  "weak": "<p>\"A spreadsheet template.\"</p>",
  "strong": "<p>A shared template: formula agreed with finance; input ranges with sources, from data where possible; a sceptic's ranges alongside the owner's; simulation with P10, P50, P90 and the probability of clearing the cost; a tornado to point research at the biggest unknown. Every sizing logged, and a yearly review of how often outcomes fell inside the ranges.</p>", "roles": ["lead", "ic"]},
 {"ask": "The CEO wants one number for a new programme's value, not a distribution. What do you give?", "follow": ["She asks which number you would bet on.", "How do you keep the risk visible?"],
  "weak": "<p>Gives the mean, or refuses to give one number.</p>",
  "strong": "<p>Gives the median, rounded, in one sentence with the risk attached: \"about ₹27 crore; roughly a 1-in-10 chance it does not cover its ₹15 crore cost.\" Names the one input that would change the answer most and the pilot that would measure it. One number plus one risk statement is usually what a CEO can act on.</p>", "roles": ["lead"]},
]

page(S, "C2", "Monte Carlo simulation for sizing and scenarios",
     "A sizing multiplies several uncertain guesses, and neither the product of the likely values nor the product of the extremes says what will probably happen. Simulation draws the inputs many times and gives the distribution of the outcome, so you can state the chance of clearing the bar.",
     "monte carlo simulation sizing scenario planning triangular distribution pert p10 p50 p90 percentiles probability of break-even tornado chart correlation uncertainty propagation forecasting uncertainty",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "When an outcome combines several uncertain inputs, draw each from an honest range many times and look at the distribution of the result, reporting percentiles and the chance of clearing the bar, because the product of likely values is not the likely product and the product of extremes almost never happens.",
     ["Write the formula, then give each input a range", "Simulate, do not multiply modes or extremes", "Report P10, P50, P90 and P(clears the bar)", "Correlation moves the tails", "A tornado shows which input to research"],
     [("a1-expectation-variance", "Expectation, variance and sums"), ("c2-bootstrap-simulation", "Bootstrap and simulation"), ("c3-problem-framing", "Framing a decision and the value of information")],
     [("c6-opportunity-sizing", "Opportunity sizing with ranges and past experiment lifts"), ("c2-power-simulation", "Power and false positive rates by simulation"), ("c4-unit-economics", "Unit economics, LTV and CAC")],
     sources=[("Savage, The Flaw of Averages: Why We Underestimate Risk in the Face of Uncertainty, Wiley, 2009", "https://www.flawofaverages.com/"),
              ("Hubbard, How to Measure Anything, 3rd edition, Wiley, 2014", "https://www.howtomeasureanything.com/")],
     sec_roles={11: ["lead", "ic", "mle"]})
