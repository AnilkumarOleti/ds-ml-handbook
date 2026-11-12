import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c5-activation"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>Of 10,000 new sellers, 35.5% are still selling at day 90. By listings created in their first 14 days:</p>
{table(["Listings in first 14 days", "Sellers", "Active at day 90"], [
["0", "3,000", "10%"], ["1 to 2", "3,000", "25%"], ["3 to 4", "1,500", "45%"], ["5 to 9", "1,500", "70%"], ["10 or more", "1,000", "78%"]], narrow=True)}
<p>The PM declares the aha moment: <strong>\"5 listings in 14 days\"</strong>. Sellers who reach it retain at 73%, the rest at 23%. The plan: push every new seller to five listings, and forecast retention rising towards 73%.</p>
<p>A month later, a nudge test raised the share of sellers reaching five listings from 25% to <strong>33%</strong>, and day-90 retention from 35.6% to <strong>36.6%</strong>. What went wrong with the forecast?</p></div>
{attempt(S, 1)}{reveal('''<p>The 50-point gap between sellers above and below five listings is mostly about <em>who</em> reaches five: committed sellers with stock list a lot and stay for reasons of their own. It also has a built-in bias: a seller who stopped visiting on day 3 could never reach five listings, so early leavers are counted as \"did not activate\" by construction, an <strong>immortal time</strong> bias.</p>
<p>The nudge test gives the causal answer. It moved 8% of sellers over the threshold and raised retention by 1 point, so each seller pushed over the line gained about 1 ÷ 8 = <strong>12.5 points</strong> of retention: real and worth having, but a quarter of the observed gap. This is the <a href="#a5-instrumental-variables">instrumental variable</a> logic: the random nudge is the instrument.</p>
<p>An aha metric is a useful <em>leading indicator</em> and a hypothesis about a lever. Its size as a lever is only known from a test.</p>''')}"""

s2 = f"""<p><strong>Gym regulars and their lockers.</strong> Members who rent a locker in their first month are far more likely to still come a year later. Giving every new member a free locker will not turn them into regulars: renting a locker is what committed people do. It may still help a little, by making the gym part of the routine.</p>
<p><strong>Students who visit office hours.</strong> They get better grades. Requiring office hours helps some students, and many sit through them without it changing anything.</p>
{table(["Idea", "Gym", "Office hours", "Activation"], [
["The early behaviour", "Renting a locker", "Visiting office hours", "Five listings in 14 days"],
["The outcome", "Still coming in a year", "Final grade", "Selling at day 90"],
["Why they move together", "Committed members do both", "Engaged students do both", "Committed sellers do both"],
["What forcing it does", "A small nudge to routine", "Helps some students", "Some real effect, much smaller than the gap"],
["How to know the size", "Give lockers to a random half", "Invite a random half", "Nudge a random half"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>An early behaviour that separates people who stay from people who leave is partly a sign of commitment and partly a cause of it, and only a randomised push shows how much is cause.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Lockers cost little.</strong> Pushing sellers to list can backfire: hurried, low-quality listings may sell badly and discourage them.</li>
<li><strong>A gym year is long.</strong> Activation windows are days, and their length is a choice that changes the answer.</li>
<li><strong>Both have one behaviour.</strong> Real activation often combines actions, such as listing, receiving a first message and making a first sale, and the order matters.</li></ul>
{tests([("Why is 'reached five listings within 14 days' biased against sellers who left early?", "<p>A seller who left on day 3 could not reach five listings, so leaving early makes 'not activated' more likely by construction. Comparing retention by activation then partly compares leavers with stayers. Measure activation only among sellers still active at the end of the window.</p>", True)])}"""

s3 = f"""<div class="fx">activation metric: an early, specific behaviour that predicts
                   long-term retention or value, and that the product can influence

finding candidates
   for each early action and threshold k, within a fixed window:
      share who reach it          (coverage)
      retention if reached vs not (separation)
      share of retained who reached it   (recall)
   look for the knee: high separation, still broad coverage

avoiding the biases
   landmark: include only users still active at the window's end
   adjust for intent signals: source, first-day behaviour, segment
   pick the window and threshold on one cohort, check on another

validating as a lever
   randomise a nudge towards the behaviour
   effect per user moved = Δ retention ÷ Δ share reaching it</div>
<ul>
<li><strong>A good activation metric</strong> is early (so teams can act within days), specific (so it suggests what to build), predictive (it separates retainers from leavers) and movable.</li>
<li><strong>Threshold choice</strong> trades precision for coverage: higher thresholds pick out more loyal users but cover fewer of them. The knee of that curve is usually where the metric is useful.</li>
<li><strong>Landmark analysis</strong> removes immortal time bias by starting the comparison at the end of the window, among users still present. {ref(1)}</li>
<li><strong>Prediction is not causation.</strong> The activation metric is chosen because it predicts; its effect as a lever comes from an experiment, and is usually much smaller than the observed gap.</li></ul>
{tests([("Why check the chosen threshold on a different cohort?", "<p>Picking the threshold with the biggest gap on one cohort fits its noise. A threshold that holds up on a later cohort is more likely to reflect a real pattern.</p>", True),
("A nudge raised the share reaching five listings by 8 points and retention by 1 point. Why is 12.5 points the effect for sellers moved, not for all sellers?", "<p>Only the sellers the nudge pushed over the threshold changed their behaviour. The 1-point change in overall retention came from those 8%, so the effect among them is 1 ÷ 0.08. It says nothing directly about sellers who would reach five anyway or never would.</p>")])}"""

s4 = f"""<h4>Worked: choosing the threshold</h4>
{table(["Threshold", "Sellers reaching it", "Retained if reached", "Retained if not", "Gap", "Share of retained sellers who reached it"], [
["1+ listings", "70%", "46.5%", "10.0%", "36.5 pts", "92%"], ["3+", "40%", "62.6%", "17.5%", "45.1 pts", "70%"],
["5+", "25%", "73.2%", "23.0%", "50.2 pts", "52%"], ["10+", "10%", "78.0%", "30.8%", "47.2 pts", "22%"]], narrow=True)}
<p>Five gives the largest gap, but reaching it covers only half of the sellers who stay. Three covers 70% of them with a gap almost as large, and 40% of new sellers already get there, so it is a target most sellers can be helped towards. A reasonable choice is three, checked on another month's cohort.</p>
<h4>Half-worked: the immortal-time check</h4>
<p>Of the 3,000 sellers with zero listings, 1,200 had stopped visiting before day 7. Restrict the comparison to sellers still active on day 14 (a landmark). Explain which way this moves the gap, and why it still does not make the gap causal.</p>
{reveal("<p>Sellers who left before day 14 sit almost entirely in the low-listing groups, and they all fail to retain. Removing them raises retention in the low groups and shrinks the gap. What remains still mixes the effect of listing with the commitment of sellers who list a lot. Only the nudge test separates them, and it found 12.5 points per seller moved.</p>")}
<h4>Bare: buyers</h4>
<p>For new buyers, candidates are: saved a search, followed a seller, made a second purchase within 30 days, installed the app. How would you choose among them?</p>
{reveal("<p>For each, within the first 30 days and among buyers still active at day 30: coverage, retention gap, and recall of retained buyers. Prefer actions the product can encourage directly, such as saved searches and follows, over outcomes such as a second purchase, which is closer to the result than to a lever. Check on a second cohort, then test nudges for the top two and compare effects per buyer moved.</p>")}
<h4>Predict, then play</h4>
<p>Predict what happens to the share of retained sellers who reached the threshold as you raise it from 1 to 10 listings, and to the gap.</p>
{reveal("<p>The share of retained sellers covered falls steadily, from 92% to 22%. The gap rises, then levels off and dips: at very high thresholds, the comparison group includes many good sellers who simply list less. The useful threshold is before the curve flattens.</p>")}
<div class="lab" data-lab="aha"></div>
<pre class="code">import pandas as pd

d = sellers[sellers.last_seen_day &gt;= 14]                       # landmark: still active at day 14
for k in [1, 3, 5, 10]:
    hit = d.listings_14d &gt;= k
    print(k, hit.mean(), d.active_d90[hit].mean(), d.active_d90[~hit].mean(),
          (hit &amp; d.active_d90).sum() / d.active_d90.sum())
# then: randomise a nudge; effect per seller moved = Δ retention / Δ share reaching k</pre>
{tests([("Why prefer an activation action the product controls, like 'saved a search', over 'made a second purchase'?", "<p>A second purchase is nearly the outcome itself: it predicts retention because it is part of it. A saved search is something the product can prompt, so if it works, the team has a lever.</p>", True),
("The activation rate rose 10 points after an onboarding redesign, and retention did not move. What does that suggest?", "<p>The redesign moved the behaviour without moving what made it predictive: users went through the motion without the commitment, or the behaviour was a sign of commitment rather than a cause. Reconsider the metric, and judge onboarding on retention.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The behaviour causes retention", "It signals commitment", "A nudge test moves the behaviour much more than retention"],
["Everyone had the full window", "Early leavers could not reach the threshold", "Landmark analysis shrinks the gap"],
["The threshold is real", "It was chosen to maximise the gap on one cohort", "It fails on the next cohort"],
["Forcing the behaviour keeps its value", "Rushed listings are poor, people game the metric", "Quality of the behaviour drops after the push"],
["One metric fits all", "Business sellers and casual sellers activate differently", "Different curves by segment"],
["The window is right", "Value takes longer to show for some users", "Compare windows; check the time to the behaviour"]])}
{tests([("After setting 'five listings' as a team goal, the share reaching it rose fast and listings got shorter and had fewer photos. What happened?", "<p>Goodhart's law: the measure became the target and lost its meaning. Pair the activation metric with a quality guardrail and judge the team on retention.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Retention by early-behaviour bucket", "Which behaviours separate stayers", "Finding candidates", "Selection; immortal time"],
["Coverage-separation-recall table", "Which threshold", "Choosing the metric", "Overfitting one cohort"],
["Landmark analysis", "A fair comparison after the window", "Always, for window-based metrics", "Drops early leavers from the question"],
["Survival models with time-varying covariates", "Effect of reaching the behaviour when it happens", "Behaviour can happen at any time", "See <a href='#b8-survival-analysis'>survival analysis</a>"],
["Randomised nudge", "Causal value of the behaviour", "Before building a strategy on it", "Effect is for users the nudge moved"],
["Propensity or DML adjustment", "Gap net of measured intent", "No test possible yet", "Unmeasured commitment remains"]])}
{tests([("You have one quarter. Which two rows do you spend it on?", "<p>The coverage-separation table with a landmark, to choose a candidate, and a randomised nudge, to measure its value. Together they give a metric and a number to plan with.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>New sellers: first sale within 21 days.</strong></p>
<p><strong>New buyers: second purchase within 30 days.</strong></p></div>
<div><p class="label">Pair 2</p>
<p><strong>New sellers: used the pricing suggestion.</strong></p>
<p><strong>New buyers: saved a search.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 are outcomes dressed as activation.</strong> They predict retention because they are early versions of it. Useful as early-warning metrics, but they do not say what to build.</p>
<p><strong>Pair 2 are product actions.</strong> They point at features the team can promote. Whether promoting them works is the test's job, but they are the kind of metric that guides building.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>\"Users who do X in their first week are three times more likely to stay, so we will make everyone do X.\" The famous versions of this story, such as friend counts in a first week, were useful because teams then tested ways to help users get there, not because the correlation guaranteed the result. Forecasting retention from the gap, as if the whole gap were causal, sets targets that cannot be met.</p>
{tests([("A board deck projects that moving activation from 25% to 50% will lift retention from 36% to 48%. How was that computed, and what would you put instead?", "<p>By applying the observed gap of about 50 points to the extra 25% of users. Use the effect per user moved from a nudge test, 12.5 points, which gives about 3 points, and say so.</p>")])}"""

s8 = f"""<ul>
<li><strong>Define the window and the landmark</strong> before looking at thresholds.</li>
<li><strong>Tabulate coverage, separation and recall</strong> for several candidates and thresholds; choose the knee.</li>
<li><strong>Validate on a second cohort.</strong></li>
<li><strong>Test a nudge</strong> early and use the effect per user moved for forecasts.</li>
<li><strong>Pair the metric with a quality guardrail</strong> so teams cannot hit it with empty actions.</li>
<li><strong>Revisit yearly</strong>: as the product changes, what predicts retention changes too.</li></ul>
{tests([("How would you explain to a PM why their aha metric's forecast was four times too optimistic?", "<p>Most of the difference between activated and non-activated users was who they were, not what the behaviour did. The test measured what changing the behaviour actually does, about a quarter of the gap. The metric is still useful as a guide; the forecast must use the tested number.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is the aha moment a real thing?</strong> Some argue it is a myth of growth folklore, a correlation that teams retrofit. Others find it a useful organising goal even if the causal share is modest.</li>
<li><strong>One activation metric or several?</strong> A single metric aligns teams; several capture different user types. Segmenting activation by user type is a common compromise.</li>
<li><strong>Predictive power or controllability?</strong> The most predictive behaviours are often outcomes; the most controllable are often weak predictors. The right metric balances them.</li>
<li><strong>How hard to push?</strong> Aggressive onboarding can raise activation and annoy users into leaving. Tests should measure retention and satisfaction, not activation alone.</li></ul>
{tests([("Make the case for keeping an activation metric whose causal effect is only a quarter of its observed gap.", "<p>A quarter of 50 points is still 12.5 points per user moved, which is valuable. It gives teams a near-term target that they can measure in days, which beats waiting 90 days for retention. The mistake is only in forecasting with the full gap.</p>")])}"""

rungs = [
 {"ask": "How would you find an activation or aha metric?", "follow": ["How do you choose the threshold?", "What bias does a fixed window create?"],
  "weak": "<p>\"Find the action most correlated with retention.\"</p>",
  "strong": "<p>For candidate early actions and thresholds within a fixed window, among users still active at the window's end: coverage, retention gap, and share of retained users who reached it. Choose the knee, prefer actions the product can influence, and check on a second cohort. Then test a nudge to learn its causal value, because the gap is mostly selection.</p>"},
 {"ask": "Sellers with 5+ listings in 14 days retain at 73% vs 23%. A nudge raised the 5+ share by 8 points and retention by 1 point. Reconcile.", "follow": ["What is the effect per seller moved?", "What should the forecast use?"],
  "model": "<p>the 50-point gap is mostly selection, committed sellers list more, plus immortal time bias, since early leavers cannot reach five. The nudge is a randomised instrument: 1 ÷ 0.08 = 12.5 points of retention per seller pushed over the threshold. Forecasts should use 12.5, not 50, and the metric stays as a leading indicator.</p>",
  "weak": "<p>Says the nudge did not work, or that the gap is causal and the test underpowered.</p>",
  "strong": "<p><b>Must have.</b> Computes the Wald ratio and names selection.</p><p><b>Strong signal.</b> Names immortal time bias and the landmark fix.</p>"},
 {"ask": "What is immortal time bias, and how do you avoid it in activation analysis?", "follow": ["Give an example.", "Is a survival model an alternative?"],
  "weak": "<p>\"When people die during the study.\"</p>",
  "strong": "<p>Classifying users by something they must survive long enough to do, so leaving early forces them into the 'did not' group. Avoid it with a landmark, comparing only users present at the window's end, or with a survival model where reaching the behaviour is a time-varying covariate.</p>", "roles": ["ic"]},
 {"ask": "Design how a new product line finds and validates its activation metric.", "follow": ["How long does it take?", "How do teams use it after?"],
  "weak": "<p>\"Run a correlation analysis at launch.\"</p>",
  "strong": "<p>Instrument early actions from day one; after two or three cohorts, build the coverage-separation-recall table with landmarks; shortlist two controllable candidates; validate on a new cohort; test nudges for both; adopt the one with the larger effect per user moved; pair it with a quality guardrail; forecast with the tested effect; review yearly.</p>", "roles": ["lead", "ic"]},
 {"ask": "Leadership set an OKR to double activation and expects retention to follow. You know the causal effect is a quarter of the gap. What do you do?", "follow": ["How do you avoid sounding negative?", "What OKR would you propose?"],
  "weak": "<p>Says nothing until the retention numbers disappoint.</p>",
  "strong": "<p>Raises it now, with the nudge result: doubling activation should add about 3 points of retention, not 12, which is still worth doing. Proposes keeping activation as the team's leading metric with a quality guardrail, and setting the retention expectation from the tested effect, so nobody is surprised next quarter.</p>", "roles": ["lead"]},
]

page(S, "C5", "Activation and aha-moment analysis",
     "Users who do certain things early tend to stay. Finding those behaviours gives teams a target they can move within days. But the gap between users who do them and users who do not is mostly about who they are, so the value of pushing the behaviour has to be measured with a test.",
     "activation aha moment leading indicator onboarding retention threshold coverage separation landmark analysis immortal time bias nudge experiment wald ratio goodhart new users new sellers",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "An activation metric is an early, controllable behaviour that predicts retention, chosen by coverage and separation among users still present at the end of the window, and its value as a lever comes from a randomised nudge, which usually shows a fraction of the observed gap.",
     ["Early, specific, predictive, movable", "Choose the threshold at the knee of coverage and separation", "Landmark to avoid immortal time bias", "The observed gap is mostly selection", "Forecast with the effect per user moved from a test"],
     [("c1-retention-funnels", "Cohort retention and funnels"), ("b8-survival-analysis", "Survival analysis and censoring"), ("a5-instrumental-variables", "Instrumental variables and regression discontinuity")],
     [("c5-churn-propensity", "Churn and propensity models"), ("c3-metric-design", "Designing metrics"), ("c5-path-analysis", "Path and sequence analysis")],
     sources=[("Dafni, \"Landmark analysis at the 25-year landmark point\", Circulation: Cardiovascular Quality and Outcomes, 2011", "https://doi.org/10.1161/CIRCOUTCOMES.110.957951")],
     sec_roles={11: ["lead", "ic", "mle"]})
