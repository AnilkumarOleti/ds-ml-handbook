import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c5-churn-propensity"
R = ["lead", "ic", "mle"]

s1 = f"""<div class="problem"><p>A churn model scores 100,000 active buyers; 25% will not buy in the next 90 days. Its AUC is 0.82. The retention team sends a win-back offer, costing <strong>₹150</strong> per buyer targeted, to the <strong>top three risk deciles</strong>. A saved buyer is worth <strong>₹2,500</strong>.</p>
<p>The offer was tested with a random holdout in every decile. Churn by decile, and how many points the offer cut it:</p>
{table(["Risk decile", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], [
["Churn without offer", "62%", "45%", "35%", "30%", "27%", "22%", "10%", "8%", "6%", "5%"],
["Cut by the offer", "4", "6", "8", "8", "7", "5", "2", "1", "1", "0"]], narrow=True)}
<p>Is the current targeting profitable? Who should get the offer?</p></div>
{attempt(S, 1)}{reveal(f'''<p>Each targeted buyer costs ₹150 and is saved with probability equal to the cut, worth ₹2,500, so the offer pays where the cut exceeds 150 ÷ 2,500 = <strong>6 points</strong>.</p>
<ul><li>Top three deciles: −₹5 lakh, ₹0, +₹5 lakh: <strong>break-even overall</strong>. The riskiest decile loses money: many of those buyers leave whatever you send.</li>
<li>Deciles 3, 4 and 5 are where the offer works best: <strong>+₹12.5 lakh</strong> together.</li></ul>
<p>The model ranks who will leave, which is not who the offer will keep. Use the churn score to <em>understand</em> and <em>prioritise</em>, and target the offer by measured uplift, or by an <a href="#a5-uplift-hte">uplift model</a> trained on this test. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>A hospital's triage list.</strong> Ranking patients by how sick they are is not the same as ranking them by how much a treatment will help. The sickest may be beyond help; the healthiest do not need it. Treatment goes where it changes the outcome.</p>
<p><strong>A teacher's at-risk list.</strong> A model can predict which pupils will fail. Extra tutoring helps the pupils who are struggling but reachable, not the ones who have stopped attending or the ones who will pass anyway.</p>
{table(["Idea", "Triage", "Tutoring", "Churn"], [
["The risk score", "How sick", "Chance of failing", "Chance of leaving"],
["What it is good for", "Who needs attention", "Who to watch", "Who is leaving, why, and how many"],
["What it is not", "Who the drug helps", "Who tutoring helps", "Who an offer keeps"],
["The lost causes", "Beyond help", "Stopped attending", "Leaving whatever you do"],
["The sure things", "Recovering anyway", "Passing anyway", "Staying anyway"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>A good prediction of who will have a bad outcome is a different thing from a prediction of who an intervention will change, and resources should follow the second.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Triage is about one patient at a time.</strong> Retention budgets are about portfolios: the decision is how many to target and in what order.</li>
<li><strong>Sickness is observed.</strong> Churn in non-contractual businesses is defined by a choice of window: \"no purchase in 90 days\" is a definition, not an event.</li>
<li><strong>Treatments have known side effects.</strong> Retention offers can train buyers to wait for discounts, a cost no single test sees.</li></ul>
{tests([("Why might the highest-risk decile respond least to an offer?", "<p>Many of those buyers have already decided to leave, for reasons such as moving, a bad experience or a competitor, that a coupon does not change. Risk and responsiveness are different properties.</p>", True)])}"""

s3 = f"""<div class="fx">set-up for a non-contractual business
   observation date t
   features: behaviour before t        (e.g. last 180 days)
   label:    churned = no purchase in (t, t + 90 days]
   population: buyers active before t
   validate on a LATER observation date, not a random split

models   logistic regression (baseline, interpretable)
         gradient boosting (usually more accurate)
evaluate AUC; lift and capture by decile; calibration;
         stability across months

using the score
   risk ranking        who is likely to leave; sizing; reporting
   value-weighted risk expected loss = P(churn) × value
   targeting an action needs uplift: P(stay | offer) − P(stay | none)</div>
<ul>
<li><strong>Churn has to be defined</strong> in businesses without subscriptions. The window should match the purchase cycle: 90 days may be churn for groceries and normal for furniture. {ref(2)}</li>
<li><strong>Leakage is the classic failure</strong>: features computed after the observation date, such as \"days since last visit\" measured at label time. A random split hides it; a time split exposes it. See <a href="#b1-validation-leakage">validation and leakage</a>.</li>
<li><strong>Lift and capture</strong> speak to the business: the top decile has 2.5 times the base churn rate and holds a quarter of churners.</li>
<li><strong>Propensity models</strong> for purchase, upgrade or response use the same machinery with a different label. The same warning applies: propensity to act is not responsiveness to a nudge.</li>
<li><strong>Calibration matters</strong> when scores feed expected-value calculations; see <a href="#b4-calibration">calibration</a>.</li></ul>
{tests([("A churn model has an AUC of 0.91 on a random split and 0.82 on next month's data. What is the likeliest reason?", "<p>Leakage or drift: features that use information from the label period, or patterns that changed. A random split lets the model see the same time period in training and testing. Trust the time-split number.</p>", True),
("Why multiply churn probability by customer value before ranking for a retention programme?", "<p>Losing a high-value buyer costs more. Ranking by expected loss puts attention where the money is, though targeting an offer still needs uplift.</p>")])}"""

s4 = f"""<h4>Worked: lift and capture</h4>
<p>Churn rates by decile sum to 250 over ten deciles: a base rate of 25%.</p>
<ul><li>Top decile: 62%, a lift of 62 ÷ 25 = <strong>2.5</strong>; it holds 62 ÷ 250 = <strong>25%</strong> of all churners.</li>
<li>Top three deciles: (62 + 45 + 35) ÷ 250 = <strong>57%</strong> of churners in 30% of buyers.</li></ul>
<p>Those are the numbers for planning and staffing: who to watch, how many saves are possible, and which reasons dominate in the riskiest groups.</p>
<h4>Half-worked: the economics per decile</h4>
<p>With 10,000 buyers per decile, profit = 10,000 × (cut × ₹2,500 − ₹150). Decile 1: 10,000 × (0.04 × 2,500 − 150) = −₹5 lakh. Finish deciles 2 to 10 and find the most profitable set.</p>
{reveal("<p>Decile 2: ₹0. Deciles 3 and 4: +₹5 lakh each. Decile 5: +₹2.5 lakh. Decile 6: −₹2.5 lakh. Deciles 7 to 10: −₹10 to −₹15 lakh each. Best set: <strong>deciles 3 to 5, +₹12.5 lakh</strong>, against ₹0 for the current top three. The break-even cut is 6 points; only middle-risk buyers clear it. Notice that ranking by risk would never find this set without the test.</p>")}
<h4>Bare: a suspicious feature</h4>
<p>The model's most important feature is \"number of support tickets in the last 7 days\", computed from a table refreshed weekly. The model is scored on the 1st of each month. What do you check?</p>
{reveal("<p>Whether, in training, the 7-day window ended at the observation date or at the refresh date, which may fall inside the label window. If it peeked into the label period, it is leakage. Also whether tickets are a cause or a symptom: buyers who have already decided to leave complain first. As a predictor that is fine; as a reason to cut ticket volume, it is not.</p>")}
<h4>Predict, then play</h4>
<p>Predict what happens to the best targeting set if the offer's cost falls from ₹150 to ₹75.</p>
{reveal("<p>Break-even falls to 3 points, so deciles 1 to 6 all pay: the set widens to the top six, and decile 1 joins because a 4-point cut now covers its cost. The ranking of who to target is set by uplift; the cut-off is set by cost and value.</p>")}
<div class="lab" data-lab="churn"></div>
<pre class="code">import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

train = build(obs_date="2026-03-01")   # features before the date, label in the next 90 days
test  = build(obs_date="2026-06-01")   # a later date: time-based validation
m = HistGradientBoostingClassifier().fit(train[X], train.churned)
p = m.predict_proba(test[X])[:, 1]
roc_auc_score(test.churned, p)
test.assign(decile=pd.qcut(-p, 10, labels=False) + 1).groupby("decile").churned.mean()   # lift table</pre>
{tests([("Why build training and test sets from different observation dates rather than a random split of one date?", "<p>The model will be used on future dates. Behaviour and data pipelines drift, and some leakage only shows across time. A later date mimics deployment.</p>", True),
("The retention team wants to judge the model by how many targeted buyers stayed. What is wrong with that?", "<p>Many would have stayed anyway, and the model chose them because of who they were. Judge the programme by the difference between targeted buyers and a random holdout of similar buyers.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The churn definition fits the buying cycle", "Seasonal or infrequent buyers flagged as churned", "Many 'churned' buyers return after the window"],
["Features exist before the observation date", "Pipelines backfill or refresh late", "AUC drops on a time split; feature timestamps"],
["High risk means worth targeting", "Lost causes and sure things", "Uplift by decile from a test"],
["The future looks like the past", "A policy or market change", "Monthly calibration and AUC tracking"],
["Scores are probabilities", "Boosted scores are poorly calibrated", "Reliability plot; recalibrate"],
["Offers have no long-term cost", "Buyers learn to wait for coupons", "Long holdouts; repeat-offer response"]])}
{tests([("30% of buyers labelled 'churned' buy again within the following 90 days. What does that suggest?", "<p>The window is too short for this business, or seasonal buyers are being labelled as churned. Lengthen the window, or define churn relative to each buyer's own purchase cycle.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Churn rate by cohort", "How many leave, when", "Tracking and reporting", "See <a href='#c1-retention-funnels'>cohort retention</a>"],
["Logistic regression", "Risk with interpretable drivers", "Baseline; explanation", "Linear in features"],
["Gradient boosting", "Risk, more accurately", "Production scoring", "Calibration; explanation via SHAP"],
["Survival models", "When will they leave?", "Time matters; censoring", "See <a href='#b8-survival-analysis'>survival analysis</a>"],
["BG/NBD and Pareto/NBD", "Is the buyer still alive, and future purchases", "Non-contractual, transaction data only", "Strong assumptions; few features"],
["Uplift model", "Who an action changes", "Targeting offers", "Needs a randomised test; see <a href='#a5-uplift-hte'>uplift</a>"]])}
{tests([("Finance wants next year's expected purchases per buyer for CLV. Which row?", "<p>A BG/NBD-type model, or a survival model with spend, which estimate both whether a buyer is still active and how much they will buy. A churn classifier answers a narrower question.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Account managers for sellers at risk.</strong> Limited staff.</p>
<p><strong>A quarterly churn forecast for finance.</strong></p></div>
<div><p class="label">Pair 2</p>
<p><strong>A win-back coupon.</strong></p>
<p><strong>A free trial of a premium subscription.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 uses risk directly.</strong> Staff attention and forecasts need to know who is likely to leave and how many; value-weighted risk ranks the accounts.</p>
<p><strong>Pair 2 targets an offer.</strong> Who the offer changes is what matters, so a randomised test and an uplift ranking beat a risk ranking. Propensity to subscribe is not responsiveness to a trial.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>\"Our churn model saved 4,000 customers.\" The count is of targeted customers who stayed. Without a holdout, the number includes everyone who would have stayed anyway, and the riskiest-first targeting may even be losing money. Every retention programme needs a standing random holdout.</p>
{tests([("How would you report a retention programme's impact credibly?", "<p>Keep a random holdout among eligible buyers; report the difference in retention between targeted and held-out buyers, times the number targeted, minus the cost. Break it down by risk decile to show where it pays.</p>")])}"""

s8 = f"""<ul>
<li><strong>Define churn from the buying cycle</strong>, and check how many \"churned\" buyers come back.</li>
<li><strong>Build features strictly before the observation date</strong>; validate on later dates.</li>
<li><strong>Report lift, capture and calibration</strong>, not just AUC.</li>
<li><strong>Use risk for attention and forecasts</strong>; use uplift for offers.</li>
<li><strong>Keep a random holdout</strong> in every retention programme, in every decile.</li>
<li><strong>Price the offer</strong>: break-even uplift = cost ÷ value of a saved buyer.</li>
<li><strong>Monitor monthly</strong>: AUC, calibration, and the uplift by decile.</li></ul>
{tests([("Why keep a holdout in every decile rather than one overall?", "<p>Uplift varies by decile, which is where the targeting decision is made. An overall holdout gives the average effect and hides that the top decile loses money while the middle pays.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is churn prediction worth it if offers need uplift?</strong> Risk scores still guide staffing, forecasting and understanding. Some teams skip them for targeting and go straight to uplift models.</li>
<li><strong>Interpretable or accurate?</strong> Logistic models explain; boosted models predict better. Many teams deploy the boosted model and use the simpler one to explain.</li>
<li><strong>Act on the riskiest?</strong> Customer-success teams often feel they must try with the riskiest accounts. The economics may say otherwise; the answer is a test.</li>
<li><strong>Discount dependence.</strong> Repeated offers may teach buyers to churn to get coupons. Long-term holdouts are the only way to see it.</li></ul>
{tests([("Make the case for sending offers to the riskiest decile even though the test says it loses money.", "<p>If those buyers are high-value strategic accounts, or losing them has costs beyond their spend, such as sellers who anchor a category, the value of a save may be much larger than ₹2,500. Then recompute break-even with that value.</p>")])}"""

rungs = [
 {"ask": "How would you build a churn model for a marketplace without subscriptions?", "follow": ["How do you define churn?", "How do you validate it?"],
  "weak": "<p>\"Label users who stopped using the app and train a classifier.\"</p>",
  "strong": "<p>Pick an observation date; features from behaviour before it; label = no purchase in a window after it, sized to the buying cycle and checked against how many 'churned' buyers return. Logistic baseline and gradient boosting; validate on a later date to catch leakage and drift; report AUC, lift and capture by decile, and calibration.</p>"},
 {"ask": "The top three risk deciles get an offer costing ₹150; a save is worth ₹2,500; the test shows cuts of 4, 6 and 8 points there and 8 and 7 in deciles 4 and 5. Who should get it?", "follow": ["What is the break-even cut?", "Why does decile 1 lose money?"],
  "model": "<p>break-even is 150 ÷ 2,500 = 6 points. The current targeting nets zero: decile 1 loses ₹5 lakh, decile 2 breaks even, decile 3 gains ₹5 lakh. Deciles 3 to 5 gain ₹12.5 lakh together. Decile 1 has many buyers who leave regardless. Target by uplift, not risk.</p>",
  "weak": "<p>Keeps the top three because they have the most churners.</p>",
  "strong": "<p><b>Must have.</b> Computes break-even and profit by decile.</p><p><b>Strong signal.</b> Separates risk from responsiveness and proposes an uplift model with a standing holdout.</p>"},
 {"ask": "Your churn model's AUC drops from 0.91 to 0.82 when you validate on a later month. What happened?", "follow": ["How would you find the leaking feature?", "Is 0.82 bad?"],
  "weak": "<p>\"Overfitting; add regularisation.\"</p>",
  "strong": "<p>Likely leakage, features using information from the label window, or drift. Check feature timestamps against the observation date, look for features whose importance collapses on the time split, and rebuild them strictly from earlier data. 0.82 on a time split is the honest number, and may be fine; lift and the economics decide.</p>", "roles": ["ic", "mle"]},
 {"ask": "Design a retention programme that uses churn and uplift models.", "follow": ["Where does each model fit?", "How do you measure the programme?"],
  "weak": "<p>\"Target the riskiest customers.\"</p>",
  "strong": "<p>Risk model for forecasting, staffing and understanding reasons; value-weighted risk for account management. For offers: a randomised test across deciles, an uplift model trained on it, targeting where expected uplift × value exceeds cost. A standing random holdout to measure the programme every month; long-term holdouts for discount dependence; monthly checks of calibration and uplift.</p>", "roles": ["lead", "ic"]},
 {"ask": "The retention team reports '4,000 customers saved' by the churn model. What do you ask?", "follow": ["There was no holdout. What now?", "How do you raise it without killing the programme?"],
  "weak": "<p>Accepts the number.</p>",
  "strong": "<p>Saved compared with what? Without a holdout, 4,000 counts targeted customers who stayed, including those who would have stayed anyway. Propose a random holdout from next month, framed as how to prove the programme's value and find where it pays most, which the team wants too.</p>", "roles": ["lead"]},
]

page(S, "C5", "Churn and propensity models",
     "A churn model predicts who will leave, and it is useful for forecasting, staffing and understanding why. But the buyers most likely to leave are not the ones an offer will keep, so targeting needs uplift measured in a test, and every programme needs a holdout.",
     "churn model propensity model non-contractual churn definition observation window label window leakage time-based validation lift capture decile auc calibration retention offer uplift break-even holdout bg/nbd expected loss",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "A churn or propensity model ranks who is likely to leave or act, built from behaviour before an observation date and validated on a later one, but who an offer will keep is a different question, so target offers by measured uplift against cost and keep a holdout in every programme.",
     ["Define churn from the buying cycle", "Features before the date; validate on a later date", "Lift and capture speak to the business", "Risk is not responsiveness", "Break-even uplift = cost ÷ value of a save"],
     [("b2-logistic-regression", "Logistic regression, odds and log loss"), ("b3-gradient-boosting", "Gradient boosting"), ("b1-validation-leakage", "Validation, cross-validation and leakage")],
     [("a5-uplift-hte", "Uplift and heterogeneous effects"), ("c4-unit-economics", "Unit economics, LTV and CAC"), ("b4-calibration", "Calibration")],
     sources=[("Ascarza, \"Retention Futility: Targeting High-Risk Customers Might Be Ineffective\", Journal of Marketing Research, 2018", "https://doi.org/10.1509/jmr.16.0163"),
              ("Fader and Hardie, \"Probability Models for Customer-Base Analysis\", Journal of Interactive Marketing, 2009", "https://doi.org/10.1016/j.intmar.2008.11.003")],
     sec_roles={11: ["lead", "ic", "mle"]})
