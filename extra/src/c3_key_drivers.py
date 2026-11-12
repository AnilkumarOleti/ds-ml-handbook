import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c3-key-drivers"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>3,000 buyers rated their last order: overall satisfaction (CSAT), plus five attributes. Leadership wants to know which attribute to invest in. Three analyses come back:</p>
{table(["Attribute", "Correlation with CSAT", "Regression coefficient (standardised)", "Share of explained variance (Shapley)"], [
["Item as described", "0.67", "0.44", "37%"], ["Delivery speed", "0.64", "0.39", "22%"], ["Packaging", "0.60", "0.00", "19%"],
["Price", "0.44", "0.20", "12%"], ["Customer service", "0.44", "0.13", "10%"]], narrow=True)}
<p>Packaging ratings correlate <strong>0.95</strong> with delivery ratings. The packaging team says their 19% share justifies a ₹5 crore packaging upgrade. Do you agree? Which attribute would you put money behind?</p></div>
{attempt(S, 1)}{reveal(f'''<p><strong>Correlations</strong> count shared credit many times over: every attribute rides on the same overall impression, so all look important.</p>
<p><strong>Shapley shares</strong> divide the model's explained variance fairly among correlated predictors, which is what they are designed to do. When two predictors are nearly the same, they split the credit, so packaging gets 19% for being a near-copy of delivery.</p>
<p><strong>The regression</strong>, holding the others fixed, gives packaging nothing (bootstrap interval −0.06 to +0.07) and delivery 0.39. Buyers rate packaging well when the courier was good. In this simulated data, packaging truly has no effect.</p>
<p>So no to the packaging case on this evidence. "Item as described" and delivery speed lead on every measure. Even then, these are associations in survey data: before spending, test whether improving delivery speed raises satisfaction and repeat purchase, for example in a region where it can be changed. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>Splitting a restaurant bill.</strong> Five friends share starters, and two of them ordered the same dish. A fair split asks what each person added to the bill, averaged over every order in which they could have joined. That is the Shapley value. It is fair about money. It does not say who enjoyed the meal.</p>
<p><strong>A football team's goals.</strong> The striker scores, but the midfielder made every pass. Crediting goals to whoever touched the ball last is like a correlation; crediting by what the team scores with and without each player is closer to a fair split. Neither tells you whether buying a better midfielder will score more goals next season.</p>
{table(["Idea", "Bill", "Football", "Key drivers"], [
["The total to divide", "The bill", "Goals scored", "Variance explained (R²)"],
["Naive credit", "Everyone who touched a dish", "Last touch", "Correlation"],
["Fair credit", "Average contribution over all orders", "With and without each player", "Shapley value, relative weights"],
["What fair credit is not", "Who liked the food", "Who to sign next", "What will move the outcome"],
["The two who ordered the same dish", "Split it", "Two similar strikers", "Correlated predictors share credit"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Both divide a total fairly among overlapping contributors, which is a different question from what would change if one contributor were improved.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Diners know what they ordered.</strong> A driver model knows only what was measured; an attribute nobody asked about gets no share however much it matters.</li>
<li><strong>The bill is fixed.</strong> R² depends on which attributes are in the model, so adding one reshuffles every share.</li>
<li><strong>Players act.</strong> Survey ratings are perceptions, filled in after the overall judgement and coloured by it, the halo effect.</li></ul>
{tests([("Why do all five attributes correlate between 0.44 and 0.67 with CSAT?", "<p>A happy buyer rates everything higher, so every attribute shares the overall impression. Correlation cannot separate that halo from each attribute's own contribution.</p>", True)])}"""

s3 = f"""<div class="fx">key driver analysis: which inputs most explain an outcome

correlation              each input alone; double counts shared signal
regression coefficient   each input holding the others fixed;
                         unstable when inputs are correlated
relative importance      divide R² among inputs
   Shapley (LMG)         average gain in R² from adding an input,
                         over every order of adding inputs
   relative weights      a fast approximation
tree model + SHAP        nonlinear drivers, interactions; shares
                         prediction credit the same way

none of these is a causal effect.
before acting: is the driver a cause, a symptom, or a proxy?</div>
<ul>
<li><strong>Shapley value regression</strong> answers "how much of the explained variation belongs to each input", averaged over all orders, so it does not depend on the order of entry and always adds to R². {ref(2)}</li>
<li><strong>Coefficients answer a different question</strong>: the change in the outcome per unit of the input, others fixed. With highly correlated inputs, they swing wildly between samples; check them with a bootstrap.</li>
<li><strong>SHAP on gradient-boosted trees</strong> extends the same fair-split idea to nonlinear models and to individual predictions; see <a href="#b3-feature-importance">feature importance and explaining models</a>.</li>
<li><strong>Key driver analysis is descriptive.</strong> A driver can be a cause, a symptom of the outcome, or a proxy for something unmeasured. The analysis ranks hypotheses for testing.</li>
<li><strong>Stated and derived importance differ.</strong> Asking buyers what matters gives one ranking; deriving it from ratings gives another. Both carry biases.</li></ul>
{tests([("Why do Shapley shares always add up to the model's R²?", "<p>By construction: each input's share is its average marginal gain in R², and averaging over all orders of entry distributes the full R² exactly among the inputs.</p>", True),
("A regression coefficient for 'customer service' is negative although its correlation with CSAT is positive. What could cause that?", "<p>Correlated inputs: holding delivery and description fixed, buyers who contacted service may have had a problem, so higher service ratings appear among troubled orders. Or plain instability from collinearity. It is not evidence that good service lowers satisfaction.</p>")])}"""

s4 = f"""<h4>Worked: Shapley with two inputs</h4>
<p>Delivery alone explains R² = 0.30 of CSAT. Description alone explains 0.20. Together they explain 0.38.</p>
<ul><li>Order delivery first: delivery adds 0.30, description adds 0.08.</li>
<li>Order description first: description adds 0.20, delivery adds 0.18.</li>
<li>Average: delivery <strong>(0.30 + 0.18) ÷ 2 = 0.24</strong>; description <strong>(0.20 + 0.08) ÷ 2 = 0.14</strong>. They add to 0.38.</li></ul>
<p>The overlap, 0.30 + 0.20 − 0.38 = 0.12, is split equally between them. That is the fairness principle, and also its limit: if one of the two is a mere proxy for the other, it still gets half the overlap.</p>
<h4>Half-worked: the five attributes</h4>
<p>With all five attributes, R² = 0.69. The bootstrap interval for the packaging coefficient is −0.06 to +0.07; for delivery, 0.32 to 0.46. Packaging's correlation with delivery is 0.95. Write the two sentences that go to the packaging team.</p>
{reveal("<p>\"Packaging ratings move almost exactly with delivery ratings, so the analysis cannot separate them, and once delivery is accounted for, packaging adds nothing we can detect. Before investing ₹5 crore, we would want a test: improve packaging in one region with delivery unchanged and see whether satisfaction or returns move.\"</p>")}
<h4>Bare: from driver to action</h4>
<p>A key driver analysis of seller churn names \"number of buyer messages answered late\" as the top driver. The ops team proposes auto-replies to cut late answers. What do you check first?</p>
{reveal("<p>Whether late replies cause churn or signal it: sellers already disengaging answer late and also leave. Look at timing (do late replies precede churn by weeks, or appear only near the end?), compare sellers whose late replies were caused by something outside their control, such as a holiday or app outage, and then test auto-replies against a holdout. A symptom in the top spot is the classic way driver analysis misleads.</p>")}
<h4>Predict, then play</h4>
<p>Two attributes each correlate 0.5 with CSAT. Predict what happens to their regression coefficients and their Shapley shares as the correlation between them rises from 0 to 0.95.</p>
{reveal("<p>The shares stay equal and their total shrinks, from 0.25 each towards about 0.13 each, because the two carry more and more of the same information. The coefficients fall from 0.5 towards 0.26 each, and in real data their standard errors explode, so they swing apart from sample to sample. With unequal correlations, one coefficient can even turn negative while its share stays positive.</p>")}
<div class="lab" data-lab="shapley2"></div>
<pre class="code">import itertools, math
import numpy as np
from sklearn.linear_model import LinearRegression

def r2(cols):
    return LinearRegression().fit(X[:, cols], y).score(X[:, cols], y) if cols else 0.0

p = X.shape[1]
shapley = np.zeros(p)
for j in range(p):
    rest = [k for k in range(p) if k != j]
    for s in range(p):
        for S in itertools.combinations(rest, s):
            w = math.factorial(s) * math.factorial(p - s - 1) / math.factorial(p)
            shapley[j] += w * (r2(list(S) + [j]) - r2(list(S)))
# exact for a handful of inputs; for many, use relative weights or SHAP</pre>
{tests([("How many regressions does exact Shapley need for 5 inputs, and for 20?", "<p>One per subset: 2⁵ = 32 for 5 inputs, about a million for 20. Beyond 10 to 15 inputs, use relative weights or sampling approximations.</p>", True),
("Shares sum to an R² of 0.25. Should you report the shares as percentages of 100?", "<p>Say both: the shares of explained variance, and that three-quarters of CSAT's variation is unexplained by these attributes. Percentages of the explained part alone can make a weak model look decisive.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The drivers cause the outcome", "Symptoms or proxies rank high", "Timing; natural experiments; a test"],
["Ratings measure attributes", "Halo: everyone rates everything by overall mood", "All attributes correlate highly with each other"],
["The attribute list is complete", "A missing driver's effect is spread over its proxies", "Low R²; qualitative research finds other themes"],
["Linear and additive", "Effects saturate, or matter only when bad", "Tree models with SHAP; plot rating against outcome"],
["Stable across segments", "New and repeat buyers care about different things", "Run by segment; compare shares"],
["Coefficients are meaningful", "Inputs correlate at 0.9 or more", "Bootstrap intervals; variance inflation factors"]])}
{tests([("Satisfaction drops sharply when delivery is late but barely rises when it is early. What does a linear driver model miss?", "<p>An asymmetric, threshold effect: delivery is a must-have, not a delighter. A linear coefficient averages the two sides. Model the drop below the promise separately, or use a tree model.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Correlation", "Which inputs move with the outcome", "A first look", "Double counts shared signal"],
["Multiple regression", "Effect of each, holding others fixed", "Inputs not too correlated", "Unstable under collinearity"],
["Shapley / LMG relative importance", "Fair share of explained variance", "Correlated survey attributes", "Credits proxies; not causal"],
["Gradient boosting + SHAP", "Nonlinear drivers and interactions", "Behavioural data with many inputs", "Same caveats; see <a href='#b3-feature-importance'>feature importance</a>"],
["Mix and rate decomposition", "Which segment's change moved a total", "Explaining a metric move", "See <a href='#c3-metric-diagnosis'>diagnosing a metric change</a>"],
["Experiment or causal method", "What happens if we change it", "Before investing", "Cost; not every driver can be moved"]])}
{tests([("A driver analysis on behavioural data finds 'used wish list' is the top driver of retention. Which row next?", "<p>A causal one. Wish list use is probably a sign of engaged users. Test a nudge to use the wish list against a holdout, or find a natural experiment, before treating it as a lever.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Drivers of NPS from a seller survey.</strong> Eight attribute ratings.</p>
<p><strong>Drivers of CSAT after support contacts.</strong> Speed, resolution, tone.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Drivers of churn from behaviour.</strong> Logins, listings, messages.</p>
<p><strong>Drivers of conversion from session features.</strong> Searches, filters, page views.</p></div></div>
{reveal('''<p><strong>Pair 1 is survey key driver analysis.</strong> Ratings share a halo and correlate heavily, so relative importance is the right descriptive tool, and qualitative research fills gaps in the attribute list.</p>
<p><strong>Pair 2 is behavioural.</strong> Features are often symptoms of the outcome: people about to churn log in less; people about to buy view more pages. SHAP on a prediction model ranks predictors, not levers, and the step to action needs an experiment.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>"The top five drivers of churn" built from a model's feature importance and handed to product teams as a to-do list. The list ranks what helps the model predict. Some entries are symptoms of leaving, some proxies for tenure or market, and a few may be levers. Treating all five as levers spends a quarter on the wrong things.</p>
{tests([("A slide titled 'What drives seller GMV' lists 'number of listings' first. What do you ask the presenter?", "<p>Whether more listings cause more GMV or whether successful sellers list more, and whether any evidence separates the two, such as a test of a listing tool. Also what share of GMV variation the model explains.</p>")])}"""

s8 = f"""<ul>
<li><strong>Report three views side by side</strong>: correlation, coefficient with a bootstrap interval, and Shapley share. Disagreement among them is information.</li>
<li><strong>Check the correlation matrix first.</strong> Merge or drop near-duplicate inputs before modelling.</li>
<li><strong>Run by segment</strong> when the decision is segment-specific.</li>
<li><strong>Label every driver</strong> as a possible lever, symptom or proxy, with the reasoning.</li>
<li><strong>Link to outcomes, not only ratings.</strong> Drivers of stated satisfaction may differ from drivers of repeat purchase; join the survey to behaviour (see <a href='#c6-qual-quant'>joining qual and quant</a>).</li>
<li><strong>End with a test plan</strong> for the top lever, not a ranking.</li></ul>
{tests([("Why join survey ratings to repeat-purchase data before running driver analysis?", "<p>Stated satisfaction is a means, not an end. An attribute can drive satisfaction scores without changing behaviour, or the reverse. Modelling the behaviour directly shows what matters for the business.</p>")])}"""

s9 = f"""<ul>
<li><strong>Shapley shares or coefficients?</strong> Shapley is stable and adds up, but credits proxies. Coefficients isolate effects but are unstable. Survey researchers favour relative importance; econometricians favour coefficients with careful design.</li>
<li><strong>Stated or derived importance?</strong> Asking \"what matters most to you\" captures what buyers think; derived importance captures what moves their ratings. Each misses something; many teams show both.</li>
<li><strong>Is driver analysis worth doing at all?</strong> Critics say it produces confident rankings of correlations. Defenders say it is a cheap way to prioritise what to test, as long as it is labelled as such.</li>
<li><strong>Should halo be removed?</strong> Some analysts regress out the overall rating first; others argue halo is part of how buyers experience the product.</li></ul>
{tests([("Make the case for showing leadership stated importance rather than derived importance.", "<p>It is in buyers' own words, easy to explain, and does not depend on modelling choices. Its weakness, that people misjudge what drives them, matters less when the next step is a test anyway.</p>")])}"""

rungs = [
 {"ask": "What is key driver analysis, and what does it not tell you?", "follow": ["Name three methods.", "Why is it not causal?"],
  "weak": "<p>\"It finds what causes the metric to change.\"</p>",
  "strong": "<p>It ranks which inputs best explain an outcome: correlations, regression coefficients, Shapley relative importance, or SHAP on a tree model. It does not say what will happen if you change an input, because drivers can be symptoms or proxies and survey ratings share a halo. It ranks hypotheses for testing.</p>"},
 {"ask": "Packaging correlates 0.60 with CSAT and gets a 19% Shapley share, but its regression coefficient is 0.00 and it correlates 0.95 with delivery. Should you invest in packaging?", "follow": ["Why does Shapley give it 19%?", "What would convince you?"],
  "model": "<p>not on this evidence. Shapley splits the shared variance between near-duplicates, so packaging gets credit for riding along with delivery; holding delivery fixed, packaging adds nothing detectable. Delivery and item description lead on every measure. A regional test that improves packaging with delivery unchanged would settle it.</p>",
  "weak": "<p>Approves because 19% is a large share.</p>",
  "strong": "<p><b>Must have.</b> Explains how Shapley splits credit among correlated inputs and uses the coefficient and its interval.</p><p><b>Strong signal.</b> Proposes a test that separates packaging from delivery.</p>"},
 {"ask": "Your churn model says 'late replies to buyers' is the top driver. Is it a lever?", "follow": ["How would you tell a symptom from a cause?", "What test would you run?"],
  "weak": "<p>\"Yes, so we should reduce late replies.\"</p>",
  "strong": "<p>Possibly a symptom: disengaging sellers reply late and then leave. Check timing, use variation outside sellers' control such as outages, and run an auto-reply or reminder test against a holdout, measuring churn rather than reply time. Only a test result makes it a lever.</p>", "roles": ["lead", "ic"]},
 {"ask": "Design a driver analysis programme for buyer satisfaction that leadership can act on.", "follow": ["How do survey and behaviour data combine?", "What is the output?"],
  "weak": "<p>\"A quarterly CSAT regression.\"</p>",
  "strong": "<p>A survey with a tight attribute list and an open question; ratings joined to orders and repeat purchase; Shapley shares and bootstrapped coefficients for both satisfaction and repeat purchase, by key segment; each top driver labelled lever, symptom or proxy; and for the top one or two levers, an experiment or natural experiment. The output is a test plan with expected value, refreshed each half.</p>", "roles": ["lead", "ic"]},
 {"ask": "A VP presents 'the five drivers of GMV' from a feature importance chart and asks teams to own one each. What do you do?", "follow": ["The VP says the model has 92% accuracy. Respond.", "What would you offer instead?"],
  "weak": "<p>Accepts the list because the model is accurate.</p>",
  "strong": "<p>Raises, privately first, that the chart ranks predictors, not levers; accuracy says nothing about causation. Offers to sort the five into likely levers, symptoms and proxies, and to propose a quick test for the two that look like levers, so teams spend the quarter on things that can move GMV.</p>", "roles": ["lead"]},
]

page(S, "C3", "Key driver analysis",
     "Which factors most explain satisfaction, churn or GMV? Correlations double count, regression coefficients swing when factors overlap, and relative importance shares the credit fairly but gives proxies their cut. None of them says what will move the metric, so driver analysis ends in a test plan.",
     "key driver analysis relative importance shapley value regression lmg relative weights shap halo effect collinearity derived importance stated importance csat nps drivers symptom proxy lever correlation causation",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Key driver analysis ranks which factors explain an outcome, with Shapley shares dividing explained variance fairly among overlapping factors, but a driver can be a symptom or a proxy, so the ranking is a list of hypotheses to test, not of levers to pull.",
     ["Correlation double counts the halo", "Coefficients isolate but swing under collinearity", "Shapley splits R² fairly, proxies included", "Label each driver: lever, symptom or proxy", "Finish with a test of the top lever"],
     [("b2-linear-regression", "Linear regression and its assumptions"), ("b3-feature-importance", "Feature importance and explaining models"), ("a5-confounding-dags", "Confounders, mediators and colliders")],
     [("c3-metric-diagnosis", "Diagnosing a metric change"), ("c6-qual-quant", "Joining survey, PSAT and UXR findings to behavioural data"), ("c5-churn-propensity", "Churn and propensity models")],
     sources=[("Johnson and LeBreton, \"History and Use of Relative Importance Indices in Organizational Research\", Organizational Research Methods, 2004", "https://doi.org/10.1177/1094428104266510"),
              ("Grömping, \"Estimators of Relative Importance in Linear Regression Based on Variance Decomposition\", The American Statistician, 2007", "https://doi.org/10.1198/000313007X188252")],
     sec_roles={11: ["lead", "ic", "mle"]})
