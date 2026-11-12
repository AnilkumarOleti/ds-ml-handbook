import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c3-anomaly-detection"
R = ["lead", "ic", "mle"]

s1 = f"""<div class="problem"><p>You monitor daily orders for 40 categories in 5 regions: <strong>200 series</strong>. The current rule alerts when a day is more than <strong>3 standard deviations</strong> from the series' 28-day average. The on-call analyst gets about <strong>80 alerts a month</strong> and has started ignoring them. Last month a checkout bug cut one category's orders by <strong>10%</strong> for four days and nobody noticed.</p>
<p>Daily orders in that category swing ±15% over the week; a forecast that knows the day of week is off by about 4% on a typical day.</p>
<p>Why so many false alerts? Why was a 10% drop missed? What would you change?</p></div>
{attempt(S, 1)}{reveal('''<p><strong>Too many alerts.</strong> Even with perfectly normal noise, 200 series × 30 days × 0.27% gives about <strong>16</strong> false alerts a month. Real day-to-day changes have heavier tails: with residuals shaped like a t-distribution, the same rule gives about <strong>80</strong>. And the 28-day average ignores the weekly cycle, so every Sunday looks strange.</p>
<p><strong>The miss.</strong> Against raw daily variation of 15%, a 10% drop is only 0.7 standard deviations, invisible. Against a forecast that knows the day of week, it is 10 ÷ 4 = <strong>2.5</strong> standard deviations: visible, though below a 3σ single-day threshold most days.</p>
<p><strong>The fix.</strong> Compare each day with a forecast (day of week, holidays, trend), not a flat average. Measure the residuals' spread robustly. Use a persistence rule, such as two consecutive days beyond 2σ in the same direction: about <strong>6</strong> false alerts a month under normal noise, and a 63% chance of catching a 2.5σ drop within three days, close to the single-day rule's 67%. Then set the threshold from the false alert budget the team can actually handle, and route alerts by size and business impact.</p>''')}"""

s2 = f"""<p><strong>A car alarm.</strong> One set off by every passing lorry is soon ignored by the whole street, including on the night the car is actually stolen. A good alarm is quiet often enough that people still look up when it sounds.</p>
<p><strong>A fever thermometer.</strong> 37.8°C means something different at 6 a.m. than after a run. A doctor reads it against what is normal for that person, at that time, in that state.</p>
{table(["Idea", "Car alarm", "Thermometer", "Metric alerts"], [
["The baseline", "A quiet street", "Normal for this person at this time", "A forecast: day of week, holidays, trend"],
["The threshold", "How hard a knock sets it off", "How far above normal", "How many standard deviations of the residual"],
["False alarms", "Lorries", "Exercise, hot day", "Normal noise, heavy tails, unmodelled seasonality"],
["The cost of false alarms", "Everyone ignores it", "Needless tests", "Alert fatigue; real incidents missed"],
["Better design", "Sense movement inside the car", "Measure twice, at rest", "Persistence, robust spread, impact-based routing"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>An alarm is judged against the right baseline and by the balance between missing real problems and crying wolf, because an alarm that is ignored catches nothing.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>A car alarm watches one car.</strong> A monitoring system watches hundreds of series, so even rare false alarms add up: it is a multiple testing problem.</li>
<li><strong>A fever is always bad.</strong> A metric spike can be good news, a campaign working. Alerts need a direction and an owner who knows the calendar.</li>
<li><strong>Both alarms are physical.</strong> Metric alerts also fire on broken pipelines, where the data is wrong rather than the business. Data-quality checks should run first.</li></ul>
{tests([("Why does adding more series to the monitor increase false alerts even if each series' rule is unchanged?", "<p>Each series has its own small false alert rate, and they add up. 200 series at 0.27% a day give about half a false alert every day. It is the same arithmetic as multiple testing.</p>", True)])}"""

s3 = f"""<div class="fx">anomaly score = (observed − expected) / typical error

expected     a forecast: day of week, holidays, trend, events
             (seasonal naive, ETS, Prophet, ARIMA, regression)
typical error  robust spread of past residuals
             e.g. 1.4826 × median absolute deviation

alert rules
   single point   |score| &gt; k
   persistence    m of the last n days beyond k′ on the same side
   cumulative     CUSUM or EWMA: catches small sustained shifts

budget         false alerts per month ≈ series × days × P(|score| &gt; k)
               choose k from the budget, not from habit
precision      true alerts ÷ all alerts; falls as incidents get rarer</div>
<ul>
<li><strong>The forecast is the baseline.</strong> Most false alerts in practice come from a baseline that ignores weekly cycles, holidays and planned events. See <a href="#b8-forecasting-backtests">forecasting, baselines and backtests</a>.</li>
<li><strong>Robust spread.</strong> A standard deviation computed from a window that contains last month's outage is inflated, and hides the next one. The median absolute deviation ignores a few extreme days.</li>
<li><strong>Persistence and cumulative rules</strong> trade a day or two of delay for far fewer false alarms, and catch sustained small shifts that single-day rules miss. {ref(1)}</li>
<li><strong>It is a base-rate problem.</strong> If real incidents are rare, most alerts are false even with a good detector; see <a href="#a1-bayes-base-rates">Bayes' rule and base rates</a>.</li>
<li><strong>Size matters more than surprise.</strong> A 50% drop in a tiny category is statistically louder than a 2% drop in the largest. Rank alerts by estimated impact in orders or revenue.</li></ul>
{tests([("Why is a 3σ threshold not a fixed 0.27% false alarm rate in practice?", "<p>That number assumes normal residuals with a correctly estimated spread. Real residuals have heavier tails, and spreads estimated from short windows are noisy, so the true rate is usually several times higher.</p>", True),
("A metric drifts down 1% a day for two weeks. Which rule catches it?", "<p>A cumulative rule such as CUSUM or EWMA, or a trend check. Each day is unremarkable on its own; the sum is not.</p>")])}"""

s4 = f"""<h4>Worked: the false alert budget</h4>
<ul><li>Normal residuals, 3σ, 200 series, 30 days: 6,000 × 0.0027 = <strong>16 false alerts a month</strong>.</li>
<li>Residuals shaped like a t-distribution with 4 degrees of freedom, scaled to the same standard deviation: P(|z| &gt; 3) = 1.3%, so <strong>79 a month</strong>, matching what the analyst sees.</li>
<li>For one false alert a month under normal residuals, the per-test rate must be 1 ÷ 6,000, which needs a threshold of <strong>3.8σ</strong>. That is too blunt to catch a 2.5σ drop.</li></ul>
<p>So threshold-tuning alone cannot win. The spread of the baseline must shrink (a better forecast), and the rule must use more than one day.</p>
<h4>Half-worked: two days instead of one</h4>
<p>Rule B alerts when two consecutive days are beyond 2σ in the same direction. Under normal residuals, the false alert chance per series-day is 2 × (0.0228)² = 0.00104. A 2.5σ drop puts each day beyond −2σ with probability Φ(0.5) = 0.69. Find B's false alerts per month, its chance of catching the drop within three days, and the precision of each rule if there are two real incidents a month.</p>
{reveal("<p>B: 6,000 × 0.00104 = <strong>6.2 false alerts a month</strong>. Detection within three days: 2 × 0.69² − 0.69³ = <strong>0.63</strong>. The single-day 3σ rule: within three days 1 − (1 − 0.31)³ = 0.67, with 16 false alerts. With two incidents a month, rule A gives 1.3 true alerts among 17.5, <strong>8% precision</strong>; rule B gives 1.25 among 7.5, <strong>17%</strong>. Better, and still mostly false: base rates bite. Routing by impact and pairing alerts with data-quality checks are what make the queue workable.</p>")}
<h4>Bare: what goes in the alert</h4>
<p>The on-call analyst gets the alert \"electronics, south: −2.6σ\". What should the message contain so that the analyst can decide in two minutes whether to act?</p>
{reveal("<p>The observed and expected values and their gap in orders and rupees; how unusual it is and how long it has lasted; whether the region or the category as a whole moved too; whether pipelines and data-quality checks passed; known events that day; a link to the series chart with the forecast band; and the owner. Impact in rupees decides urgency; context decides whether it is real.</p>")}
<h4>Predict, then play</h4>
<p>Predict how many false alerts a month the 3σ single-day rule gives on 200 series if residuals have heavy tails, and how far the threshold must rise to bring it back to about 16.</p>
{reveal("<p>About <strong>80</strong>. With these heavy tails, getting back to 16 needs a threshold of about <strong>4.7σ</strong>, which makes moderate drops nearly undetectable. Heavy tails are an argument for persistence rules and robust spreads, not just higher thresholds.</p>")}
<div class="lab" data-lab="alerts"></div>
<pre class="code">import numpy as np

resid = actual - forecast                       # forecast knows weekday, holidays, events
scale = 1.4826 * np.median(np.abs(resid[-56:] - np.median(resid[-56:])))   # robust spread
z = resid / scale
same_side = np.sign(z[-1]) == np.sign(z[-2])
alert = same_side and min(abs(z[-1]), abs(z[-2])) &gt; 2       # two days beyond 2 sigma
impact = resid[-2:].sum()                       # orders lost or gained; rank alerts by this</pre>
{tests([("Why compute the spread over the last 56 days with the median absolute deviation rather than the standard deviation?", "<p>A single outage in the window inflates the standard deviation, widening the band and hiding the next incident. The MAD barely moves for a few extreme days. Eight weeks gives enough points and covers weekday patterns.</p>", True),
("Why might you set a different threshold for the ten largest categories than for the rest?", "<p>Their incidents cost more, so missing one is worse; and their series are less noisy relative to their size. A lower threshold there buys detection where it matters, while a higher one elsewhere keeps the total false alert budget.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The forecast captures normal patterns", "Holidays, sales, launches, weather", "Alerts cluster on known event days; add them to the model"],
["Residuals are normal", "Heavy tails", "More false alerts than the formula predicts"],
["The spread is stable", "Volatility differs by season or grows with volume", "Rolling robust spread; model on the log scale"],
["Series are independent", "A national issue moves all 200 at once", "Group alerts; alert on the parent series first"],
["The data is right", "A pipeline delay shows as a drop", "Run freshness and completeness checks before anomaly checks"],
["Past incidents look like future ones", "New failure modes, slow drifts", "Add cumulative rules; review missed incidents"]])}
{tests([("On the morning after a pipeline delay, 150 of 200 series alert at once. What should the system have done?", "<p>Checked data freshness and completeness first and suppressed anomaly alerts for late data; and grouped simultaneous alerts into one, pointing at the shared cause. See <a href='#d1-data-quality'>data quality, contracts and observability</a>.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Rolling mean ± k sd", "Is today far from recent days?", "Stable series without cycles", "Weekly cycles and outliers wreck it"],
["Forecast residual ± k robust sd", "Is today far from expected?", "Most business metrics", "Forecast must include events"],
["Persistence (m of n)", "Is the deviation sustained?", "Daily metrics where a day of delay is fine", "Slower"],
["CUSUM / EWMA", "Has the level shifted slightly?", "Slow drifts, small sustained changes", "Tuning; harder to explain"],
["Isolation forest, autoencoders", "Is this combination of values unusual?", "Many related metrics, unlabelled", "Opaque; need labelled incidents to tune"],
["Hierarchical alerting", "Where in the tree is the problem?", "Many series in a hierarchy", "Needs reconciliation of levels"]])}
{tests([("You monitor revenue by country, category and platform: 2,000 series. Which rows would you combine?", "<p>Forecast residuals with robust spreads per series, hierarchical alerting that checks totals first and drills down, persistence rules for small series, and impact-based ranking. Machine-learning detectors only if simpler ones miss incidents that matter.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Daily GMV by category.</strong> Weekly cycle, festival peaks.</p>
<p><strong>Hourly payment failures.</strong> Daily cycle, sudden spikes.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Seller sign-ups slowly declining for a month.</strong></p>
<p><strong>A fraud rate creeping up.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 needs seasonal baselines.</strong> Each has a strong cycle, so a flat average alerts on every peak and trough. Forecast residuals with robust thresholds, and for payment failures, a short persistence rule because minutes matter.</p>
<p><strong>Pair 2 are slow drifts.</strong> No single day is alarming. Cumulative rules (CUSUM, EWMA) or a weekly trend check against a forecast catch them; single-day thresholds never will.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Tuning thresholds by complaint. The team lowers thresholds after a missed incident and raises them after a noisy week, so the system swings between deafening and silent. The fix is to agree a false alert budget, measure detection on past incidents, and change the baseline or the rule rather than the number.</p>
{tests([("After a missed incident, a VP asks for thresholds to be lowered to 2σ everywhere. What do you show them?", "<p>The arithmetic: 200 series at 2σ give about 270 false alerts a month under ideal conditions, more in practice, and the team will stop reading them. Then show what would have caught the missed incident with a few false alerts: a better baseline and a persistence rule.</p>")])}"""

s8 = f"""<ul>
<li><strong>Start from a false alert budget</strong> the on-call team agrees to, such as five a week, and work back to thresholds.</li>
<li><strong>Use a forecast with events</strong> as the baseline; maintain the event calendar.</li>
<li><strong>Use robust spreads</strong> on a log scale for volume metrics.</li>
<li><strong>Combine rules</strong>: single-day for large shocks, persistence for moderate ones, cumulative for drifts.</li>
<li><strong>Run data-quality checks first</strong> and suppress anomaly alerts on late or incomplete data.</li>
<li><strong>Rank and route by impact</strong>, with context in the message.</li>
<li><strong>Review monthly</strong>: false alerts, missed incidents, time to detect.</li></ul>
{tests([("How would you measure whether a new alerting system is better than the old one?", "<p>Replay the past year: for each, count false alerts and how many known incidents were caught and how fast. Compare at the same false alert budget. Then watch the live precision and missed incidents for a quarter.</p>")])}"""

s9 = f"""<ul>
<li><strong>Statistical or ML detectors?</strong> Forecast-residual methods are transparent and easy to tune; ML detectors find odd combinations but are hard to explain and to trust. Most teams start simple and add ML for specific blind spots.</li>
<li><strong>Who owns an alert?</strong> Analytics, engineering or the business owner. Unowned alerts are ignored. The usual answer is to route by series to a named owner.</li>
<li><strong>Alert on everything or on what matters?</strong> Monitoring every cut catches more, at the cost of noise. Monitoring the few metrics tied to decisions keeps attention but misses local problems.</li>
<li><strong>Should good news alert?</strong> A spike can be a campaign or a bot attack. Many teams alert both ways and route positive spikes at lower priority.</li></ul>
{tests([("Make the case for monitoring fewer series.", "<p>Each series adds false alerts, and attention is finite. A hierarchy that watches totals closely and drills down on demand catches most incidents that matter with far less noise.</p>")])}"""

rungs = [
 {"ask": "How would you set up alerts for a daily business metric?", "follow": ["What is the baseline?", "How do you pick the threshold?"],
  "weak": "<p>\"Alert when it is more than three standard deviations from the mean.\"</p>",
  "strong": "<p>Compare each day with a forecast that includes day of week, holidays, trend and known events; score the residual against a robust spread; alert on large single-day deviations or sustained smaller ones. Choose thresholds from an agreed false alert budget across all monitored series, rank alerts by business impact, and run data-quality checks first.</p>"},
 {"ask": "200 series with a 3σ rule produce 80 false alerts a month, and a 10% drop was missed. Diagnose and fix.", "follow": ["Why 80 and not 16?", "How does a two-day rule compare?"],
  "model": "<p>200 × 30 × 0.27% is 16 under normal residuals; heavy tails push it to about 80. The miss: against a flat average with ±15% weekly swings, 10% is under one standard deviation; against a weekday-aware forecast with 4% error it is 2.5σ. Fix with a forecast baseline, robust spread, and a two-days-beyond-2σ rule: about 6 false alerts a month and a 63% chance of catching the drop within three days.</p>",
  "weak": "<p>Lowers the threshold to catch the drop, or raises it to cut the noise.</p>",
  "strong": "<p><b>Must have.</b> Computes the false alert budget and identifies the missing seasonality in the baseline.</p><p><b>Strong signal.</b> Uses persistence and robust spread, and talks about precision and routing.</p>"},
 {"ask": "Even with a good rule, 80% of alerts are false. Why, and is that acceptable?", "follow": ["How do you raise precision?", "What is the cost of a miss?"],
  "weak": "<p>\"The model is not good enough.\"</p>",
  "strong": "<p>Base rates: real incidents are rare compared with series-days, so even a good detector's alerts are mostly false. Raise precision with better baselines, grouping simultaneous alerts, data-quality checks first, and impact thresholds. Whether 20% precision is acceptable depends on the cost of a miss versus the time spent per false alert; agree that trade with the owners.</p>", "roles": ["ic", "mle"]},
 {"ask": "Design anomaly detection for revenue across 2,000 series in a country × category × platform hierarchy.", "follow": ["How do you avoid 2,000 alerts from one outage?", "How do you know it works?"],
  "weak": "<p>\"An ML anomaly detector on every series.\"</p>",
  "strong": "<p>Forecast baselines per series with an event calendar; robust spreads on log scale; hierarchical checks from totals down, grouping alerts that share a parent; data freshness checks gating everything; rules mixing single-day, persistence and CUSUM; a false alert budget per owner; impact ranking and context in messages. Validate by replaying a year of known incidents and tracking precision and time to detect monthly.</p>", "roles": ["ic", "mle"]},
 {"ask": "Your team is drowning in alerts and missed a costly incident. Leadership wants a fix this month. What do you do?", "follow": ["What do you switch off?", "How do you report progress?"],
  "weak": "<p>Adds more alerts.</p>",
  "strong": "<p>This week: suppress anomaly alerts on late data, group simultaneous alerts, and route by impact so the top 20 series get attention. This month: replace flat averages with weekday-aware forecasts and add a persistence rule, tuned on the past year so the missed incident would have been caught within the agreed false alert budget. Report weekly: alerts, precision, incidents caught and time to detect.</p>", "roles": ["lead"]},
]

page(S, "C3", "Anomaly detection and alerting thresholds",
     "An alert is only useful if someone still reads it. Comparing each day with a forecast rather than a flat average, using robust spreads and persistence rules, and setting thresholds from a false alert budget across all series is what lets a monitor catch real drops without crying wolf.",
     "anomaly detection alerting thresholds false alerts alert fatigue forecast baseline residual robust spread median absolute deviation mad persistence rule cusum ewma multiple testing base rate precision prophet seasonality monitoring",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Judge each day against a forecast that knows the calendar, measure surprise with a robust spread, require persistence for moderate deviations, and set thresholds from the false alert budget across every series you watch, because rare incidents mean most alerts are false and an ignored alarm catches nothing.",
     ["Baseline is a forecast, not a flat average", "False alerts = series × days × tail probability", "Heavy tails multiply false alerts", "Persistence and cumulative rules trade delay for precision", "Rank by impact; check data quality first"],
     [("b8-forecasting-backtests", "Forecasting, baselines and backtests"), ("a2-multiple-testing", "Multiple testing"), ("a1-bayes-base-rates", "Bayes' rule and base rates")],
     [("c3-metric-diagnosis", "Diagnosing a metric change"), ("d1-data-quality", "Data quality, contracts and observability"), ("d3-monitoring-drift", "Monitoring, drift and retraining")],
     sources=[("Montgomery, Introduction to Statistical Quality Control, 8th edition, Wiley, 2019, chapter 9 (CUSUM and EWMA)", "https://www.wiley.com/en-us/Introduction+to+Statistical+Quality+Control%2C+8th+Edition-p-9781119399308"),
              ("Taylor and Letham, \"Forecasting at Scale\", The American Statistician, 2018", "https://doi.org/10.1080/00031305.2017.1380080")],
     sec_roles={11: ["lead", "ic", "mle"]})
