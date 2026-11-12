import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "a5-its-causalimpact"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>Free returns launched everywhere at once in week 27, so there is no control group. Weekly orders, in thousands, had grown by almost exactly <strong>1,000 a week</strong> for six months, from 201 in week 1 to <strong>226</strong> in week 26, with week-to-week noise of about 3.</p>
<p>Weeks 27 to 34 averaged <strong>238</strong>. The launch deck compares that with the eight weeks before, which averaged 222.5, and claims <strong>+7%</strong>.</p>
<p>One more fact: a neighbouring country, which did not get free returns, ran <strong>2% above its own trend</strong> in weeks 27 to 34. A festival fell in week 31 in both.</p>
<p>What was the effect of free returns?</p></div>
{attempt(S, 1)}{reveal('''<p><strong>Before and after</strong> credits the launch with six months of growth that was happening anyway. It is not an estimate of anything.</p>
<p><strong>Interrupted time series.</strong> Extend the pre-launch trend: weeks 27 to 34 would have averaged 230.5. The gap is <strong>+7.5 thousand a week, +3.3%</strong>, with an interval of about 4.0 to 11.0 from the trend's own uncertainty.</p>
<p><strong>With the neighbour as a control series.</strong> The festival lifted orders everywhere by about 2%, so the counterfactual is 230.5 × 1.02 = 235.1, and the effect is <strong>+2.9 thousand, +1.2%</strong>. The interval, roughly −0.2 to +6.0, now includes zero.</p>
<p>The honest readout: the trend-only method says +3%, but most of that coincides with a festival that lifted a comparable market by 2%. The best estimate is about +1%, and it is not clearly different from zero. If the decision needs more, measure the next region's launch with a staggered rollout.</p>''')}"""

s2 = f"""<p><strong>A weight-loss diet started on 1 January.</strong> You lost 3 kg in a month. But you had been losing half a kilo a month all autumn, and everyone in your office loses a kilo in January after the holidays. The diet's share is what is left after both.</p>
<p><strong>A new bus route.</strong> A shop's sales rose 10% the month the route opened. The shop was already growing 2% a month, and the shop next door, not on the route, rose 5% that month.</p>
{table(["Idea", "Diet", "Bus route", "Launch with no control"], [
["The naive comparison", "Weight before and after", "Sales before and after", "Weeks before against weeks after"],
["The trend you must remove", "Half a kilo a month", "2% a month", "The pre-launch trend and seasonality"],
["The shock that coincided", "January for everyone", "Whatever lifted the shop next door", "A festival, a sale, a competitor's move"],
["The control series", "Your colleagues", "The shop next door", "An unaffected market or category"],
["The effect", "What is left after both", "10% minus trend minus 5%", "Observed minus a forecast built from both"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>A change measured against the past alone absorbs both the existing trend and anything else that happened at the same moment, so the counterfactual must extend the trend and borrow the shock from something unaffected.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Colleagues are people like you.</strong> A control series must move with the target before the launch, which is checked in data, not assumed from resemblance.</li>
<li><strong>The diet has one start date.</strong> Launches are often announced early (anticipation) or rolled out over weeks (gradual onset), which blurs the break.</li>
<li><strong>Both are short.</strong> The further a forecast runs past the launch, the wider its uncertainty and the more other changes creep in.</li></ul>
{tests([("Your control series is a category the launch could also affect, such as accessories bought with returned clothes. What goes wrong?", "<p>The control is contaminated. If the launch raised accessory sales, the counterfactual is too high and the effect is understated. A control series must be one the intervention cannot touch.</p>")])}"""

s3 = f"""<div class="fx">interrupted time series (segmented regression)
   y_t = a + b·t + c·post_t + d·(t − t0)·post_t + e_t
   c = jump at launch, d = change in slope after it
   add seasonality terms; allow for autocorrelated errors

CausalImpact (Bayesian structural time series)
   fit y_t on its own trend and season and on control series x_t
   using the pre-period only; forecast the post-period
   effect_t = observed_t − forecast_t, with a posterior interval
   cumulative effect = Σ effect_t

synthetic difference-in-differences
   weights on control units, so their pre-trend matches the treated
   + weights on pre-periods, so they resemble the post-period
   + a unit fixed effect: levels may differ, trends must match</div>
<ul>
<li><strong>An interrupted time series</strong> uses the treated series' own past as the control. It is credible when the pre-period is long and stable and nothing else changed at the launch. {ref(3)}</li>
<li><strong>CausalImpact</strong> adds control series, such as other markets, categories or search interest, that are related to the outcome but not affected by the launch. It learns the relationship before the launch and uses it after. {ref(1)}</li>
<li><strong>Synthetic DiD</strong> sits between <a href="#a5-diff-in-diff">difference-in-differences</a> and synthetic control. It weights control units like synthetic control, but lets the treated unit sit at a different level, as DiD does, and weights pre-periods towards the most relevant ones. {ref(2)}</li>
<li><strong>Uncertainty grows with the forecast horizon.</strong> The trend's slope is estimated, so its error is multiplied by the distance from the middle of the pre-period.</li></ul>
{tests([("Why does the ITS interval widen the longer after the launch you measure?", "<p>The counterfactual is the pre-period trend extended forward. Any error in the estimated slope grows with distance, and the chance that something else changes grows too.</p>", True),
("When would you prefer synthetic DiD to plain synthetic control?", "<p>When the treated unit is larger or smaller than any combination of controls can match in level, but its trend can be matched. Synthetic control needs the level matched too; synthetic DiD absorbs the level difference.</p>")])}"""

s4 = f"""<h4>Worked: the interrupted time series</h4>
<p>From section 1: pre-period orders = 200 + 1.0 × week, residual sd 3, 26 weeks.</p>
<ul><li>Counterfactual for weeks 27 to 34: 227, 228, … 234, average <strong>230.5</strong>.</li>
<li>Effect: 238 − 230.5 = <strong>7.5 thousand a week</strong>, 3.3%.</li>
<li>Uncertainty has two parts. The fitted line's error at the post-period's midpoint: 3 × √(1/26 + (30.5 − 13.5)²/1,462.5) = <strong>1.46</strong>. The noise in eight observed weeks: 3 ÷ √8 = <strong>1.06</strong>. Together √(1.46² + 1.06²) = 1.80, so the 95% interval is <strong>4.0 to 11.0</strong>.</li></ul>
<p>The line's error is the larger part, and it grows with the horizon. A single week's 95% band is ±6.3 at week 27 and ±8.4 at week 52.</p>
<p>This assumes independent weekly errors. Weekly sales are usually autocorrelated, which makes the true interval wider. Use errors that allow for it, or a model such as CausalImpact that includes it.</p>
<h4>Half-worked: adding a control series</h4>
<p>The neighbouring market tracked your market closely before week 27 (correlation 0.94 in weekly changes) and ran 2% above its own trend in weeks 27 to 34. A model that uses it gives a counterfactual of 230.5 × 1.02 = 235.1, with a standard error of about 1.6 for the average effect. Find the effect and its interval, and decide what to write.</p>
{reveal("<p>238 − 235.1 = <strong>+2.9 thousand</strong>, +1.2%, interval about <strong>−0.2 to +6.0</strong>. The point estimate is positive but zero cannot be ruled out. Write that the trend-only estimate of +3.3% is mostly explained by the festival, that the adjusted effect is about +1%, and that it is not yet distinguishable from zero. If the policy's cost needs more than +1% to break even, that is the decision-relevant line, not zero.</p>")}
<h4>Bare: when did it start?</h4>
<p>Free returns were announced on social media in week 25, two weeks before launch, and orders in weeks 25 and 26 ran 4 thousand above trend. What does this do to the estimate, and how do you handle it?</p>
{reveal("<p>Anticipation: the pre-period is contaminated, so the trend is fitted partly on treated weeks, and those weeks are counted as baseline. Fit the trend on weeks 1 to 24 only, treat the announcement as the start of the intervention, and report the effect from week 25. If people delayed purchases until free returns began, there may also be a dip before the launch and a bump after it, which inflates an effect read from the first few weeks.</p>")}
<h4>Predict, then play</h4>
<p>The 95% half-width for the eight-week average effect is 3.5 thousand with 26 pre-period weeks. Predict it with 8 weeks of pre-period, and with 52.</p>
{reveal("<p>About <strong>7.8</strong> with 8 weeks and <strong>2.8</strong> with 52. A short pre-period makes the slope uncertain, and that uncertainty is projected forward. A longer one helps, until the risk grows that the old trend no longer applies.</p>")}
<div class="lab" data-lab="its"></div>
<pre class="code">from causalimpact import CausalImpact   # one of several Python ports

# df: index = week, columns: y (your market), x1, x2 (control series)
ci = CausalImpact(df, pre_period=[1, 26], post_period=[27, 34])
print(ci.summary())        # average and cumulative effect, interval, posterior probability
ci.plot()                  # observed vs counterfactual, pointwise and cumulative effect</pre>
{tests([("Why can the eight-week average be estimated more precisely than any single week's effect?", "<p>The observation noise averages out over eight weeks. The trend's error does not; it is shared by all eight weeks, so it sets a floor on precision however many weeks you average.</p>", True),
("A control series moved with yours before the launch but is driven by the same marketing calendar. Is that a problem?", "<p>It is the point. A shared calendar is what lets it absorb the festival. The problem is only if the launch itself could move it.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The pre-period trend would have continued", "A competitor, a price change or a market shift arrives at the same time", "Check news and other launches; use control series"],
["Nothing else changed at the launch", "A sale, festival or app release coincides", "Annotate the chart; a control series moves too"],
["Control series are unaffected", "The launch spills into the control market or category", "Ask how the launch could reach it; test several controls"],
["The relationship with controls is stable", "The pre-period link breaks after the launch for other reasons", "Placebo launches in the pre-period"],
["The start date is known", "Announcement, anticipation, gradual rollout", "Plot the residuals around the launch; move the start"],
["Errors are independent", "Weekly sales are autocorrelated", "Residual autocorrelation; intervals too narrow in placebo tests"]])}
{tests([("You run the same model with a fake launch date in week 15. It finds a 'significant' effect of +4%. What does that tell you?", "<p>The model is finding effects that do not exist: its intervals are too narrow, or the pre-period has structural breaks. Fix the model, for example by allowing for autocorrelation or adding seasonality, until placebo dates give null results.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Before and after", "Nothing causal", "Never, alone", "Absorbs trend and coincident shocks"],
["Interrupted time series", "Effect against the unit's own trend", "Long, stable pre-period; no control units", "Coincident shocks; extrapolation"],
["CausalImpact", "Effect against trend plus control series", "Good unaffected control series exist", "Contaminated controls; model choices"],
["Difference-in-differences", "Effect against a comparison group's change", "A similar untreated group exists", "Parallel trends"],
["Synthetic control", "Effect against a weighted mix of units", "One treated unit, many controls, long pre-period", "Level must be matched"],
["Synthetic DiD", "DiD with unit and time weights", "Panel data; level differences", "Needs several control units and periods"]])}
{tests([("A feature launched in one city, with fifty other cities untouched and two years of weekly data. Which row?", "<p>Synthetic control or synthetic DiD, with placebo tests that apply the method to each untreated city in turn. An ITS on the one city would ignore fifty natural controls.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>A nationwide app redesign.</strong> Everyone got it on the same day.</p>
<p><strong>A new law on marketplace fees.</strong> It applied to every seller at once.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A TV campaign in one state.</strong> Other states saw none.</p>
<p><strong>A warehouse opening near one city.</strong> Delivery times fell there only.</p></div></div>
{reveal('''<p><strong>Pair 1 has no untreated units.</strong> Interrupted time series with control series from outside the affected population, such as other countries, unaffected categories or search trends, is the main option.</p>
<p><strong>Pair 2 has one treated unit among many.</strong> Synthetic control or synthetic DiD, using the untreated states or cities, gives a much stronger counterfactual than the unit's own trend.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>The before-and-after chart in a launch announcement. A line rises, a vertical bar marks the launch, and the gap between the averages either side is presented as the effect. It credits the launch with the existing trend, the season and anything that happened that week. The fix is cheap: extend the trend, add a control series, and run the same analysis on a fake launch date.</p>
{tests([("A leader shows a chart: weekly sellers onboarded rose 12% in the month after a new onboarding flow. What two questions do you ask?", "<p>What was the trend before, and what else changed that month? Then: what does the same chart show for a comparable market without the new flow?</p>")])}"""

s8 = f"""<ul>
<li><strong>Use at least a year of pre-period</strong> for weekly data when you can, so seasonality is in the model.</li>
<li><strong>Pick control series before looking at the post-period</strong>, and say why the launch cannot affect them.</li>
<li><strong>Run placebo launch dates</strong> in the pre-period. A model that finds effects on fake dates has intervals you cannot trust.</li>
<li><strong>Report cumulative and average effects with intervals</strong>, and the horizon you measured over. Keep the horizon short.</li>
<li><strong>Plan a staggered rollout</strong> when a launch can be phased. Even two waves turn a fragile time-series estimate into a <a href="#a5-diff-in-diff">difference-in-differences</a>.</li>
<li><strong>Mark known events</strong> such as sales, festivals and outages on every chart.</li></ul>
{tests([("A PM asks for the effect of a launch 26 weeks after it happened. What do you warn about?", "<p>Six months of extrapolation: the trend's error has grown, and many other changes have happened. Report the effect over the first few weeks with confidence, and anything later as increasingly a guess.</p>")])}"""

s9 = f"""<ul>
<li><strong>How many control series?</strong> More series fit the pre-period better but risk fitting noise and picking up contaminated ones. CausalImpact uses a prior that favours few; some analysts prefer a handful chosen by reasoning.</li>
<li><strong>Bayesian or frequentist?</strong> CausalImpact reports a posterior probability of an effect, which is easy to misread as the probability that the launch worked. It depends on the model and priors like any other estimate.</li>
<li><strong>Is ITS causal at all?</strong> Critics say a single series can never rule out coincident shocks. Defenders reply that with a long stable history, a sharp break exactly at the launch, and placebo checks, it is often the best evidence available.</li>
<li><strong>Synthetic DiD or synthetic control?</strong> Synthetic DiD is more robust in many simulations, but it adds weights that are harder to explain. For a leadership audience, a transparent synthetic control with placebo plots may persuade more.</li></ul>
{tests([("Make the case for a simple ITS over CausalImpact for a leadership readout.", "<p>It can be drawn and checked by eye: a straight line extended, a gap, a placebo date. Its assumptions are visible. CausalImpact's extra machinery helps with seasonality and controls, but adds choices a sceptical audience cannot see.</p>")])}"""

rungs = [
 {"ask": "A feature launched to everyone at once. How do you estimate its effect?", "follow": ["Why not compare the weeks before and after?", "What would make you distrust the result?"],
  "weak": "<p>\"Compare the average before with the average after.\"</p>",
  "strong": "<p>Model the pre-launch trend and seasonality and forecast what would have happened, an interrupted time series, adding control series that the launch cannot affect, as CausalImpact does. The effect is observed minus forecast, with an interval that widens with the horizon. Distrust it if placebo launch dates also show effects, or if something else changed at the same time.</p>"},
 {"ask": "Orders grew 1 thousand a week for six months to 226. After a launch in week 27 they averaged 238 for eight weeks. A comparable market without the launch ran 2% above its trend. Estimate the effect.", "follow": ["The deck says +7%. Where does that come from?", "Is the adjusted effect significant?"],
  "model": "<p>the trend gives a counterfactual of 230.5, an effect of 7.5 thousand or 3.3%. The comparable market says 2% of that was a shared shock, so the counterfactual is 235.1 and the effect is about 2.9 thousand, 1.2%, with an interval around −0.2 to 6.0. The deck's 7% compares with the previous eight weeks and counts the trend as effect.</p>",
  "weak": "<p>Accepts 7%, or uses the trend but ignores the control market.</p>",
  "strong": "<p><b>Must have.</b> Removes the trend, then the shared shock, and gives an interval.</p><p><b>Strong signal.</b> Notes that the estimate is not distinguishable from zero and compares it with the break-even effect.</p>"},
 {"ask": "Your ITS finds +5% at a fake launch date six months before the real one. What now?", "follow": ["What are the likely causes?", "When would you give up on the method?"],
  "weak": "<p>\"Fake dates do not matter; the real one is what counts.\"</p>",
  "strong": "<p>The model is mis-specified: probably missing seasonality, a structural break, or autocorrelated errors making intervals too narrow. Add seasonality, allow for autocorrelation, try control series, and rerun placebos until they are null. If no specification passes, the series is too unstable for ITS, and the answer is a design: a staggered rollout or a holdout.</p>", "roles": ["lead", "ic"]},
 {"ask": "Design the measurement for a nationwide policy change you cannot randomise or stagger.", "follow": ["Which control series would you choose, and why?", "How long a post-period would you report?"],
  "weak": "<p>\"Look at the dashboard after launch.\"</p>",
  "strong": "<p>Before launch: fix the metric, the horizon, and two or three control series the policy cannot touch, such as another country, an unaffected category, and search interest; collect at least a year of history. After launch: CausalImpact or ITS with seasonality, the average and cumulative effect over a short horizon, placebo dates, a check for anticipation, and a decision threshold set in advance.</p>", "roles": ["lead", "ic"]},
 {"ask": "Leadership wants a single number for a launch's impact for the annual report. Your best estimate is +1.2%, interval −0.2% to +6%. The launch owner wants to use the trend-only +3.3%. What do you do?", "follow": ["The owner argues the festival adjustment is speculative. Respond.", "What goes in the report?"],
  "weak": "<p>Gives the owner's number, or refuses to give any number.</p>",
  "strong": "<p>Explains that the comparable market rose 2% in the same weeks, so the trend-only number counts the festival as effect. Offers the adjusted estimate with its range, in plain words: about 1%, and possibly zero. If a single number must go in, it is the adjusted one with \"estimated\" beside it. Proposes a staggered rollout for the next market to settle it.</p>", "roles": ["lead"]},
]

page(S, "A5", "Interrupted time series, CausalImpact and synthetic DiD",
     "When a launch hits everyone at once, the only control is the past, and the past has a trend. This page covers forecasting the counterfactual from the pre-launch series, borrowing shared shocks from control series that the launch could not touch, and synthetic DiD for panels.",
     "interrupted time series its segmented regression causalimpact bayesian structural time series bsts counterfactual forecast control series synthetic difference in differences sdid placebo launch date anticipation pre-period trend",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "With no control group, estimate a launch's effect as the gap between what happened and a forecast built from the pre-launch trend and from control series the launch could not affect, check it with placebo dates, and keep the horizon short because the forecast's uncertainty grows with it.",
     ["Before-and-after counts the trend as effect", "Extend the trend and season; add unaffected control series", "Uncertainty grows with the horizon", "Placebo launch dates test the model", "Synthetic DiD weights units and periods and allows level differences"],
     [("a5-diff-in-diff", "Difference-in-differences and synthetic control"), ("b8-arima-seasonality", "Stationarity, ARIMA and seasonality"), ("b8-forecasting-backtests", "Forecasting, baselines and backtests")],
     [("a5-sensitivity-falsification", "Sensitivity to hidden confounding and falsification tests"), ("c3-launch-strategy", "Launch decisions and strategy answers"), ("c3-anomaly-detection", "Anomaly detection and alerting thresholds")],
     sources=[("Brodersen, Gallusser, Koehler, Remy and Scott, \"Inferring causal impact using Bayesian structural time-series models\", Annals of Applied Statistics, 2015", "https://doi.org/10.1214/14-AOAS788"),
              ("Arkhangelsky, Athey, Hirshberg, Imbens and Wager, \"Synthetic Difference-in-Differences\", American Economic Review, 2021", "https://doi.org/10.1257/aer.20190159"),
              ("Bernal, Cummins and Gasparrini, \"Interrupted time series regression for the evaluation of public health interventions: a tutorial\", International Journal of Epidemiology, 2017", "https://doi.org/10.1093/ije/dyw098")],
     sec_roles={11: ["lead", "ic", "mle"]})
