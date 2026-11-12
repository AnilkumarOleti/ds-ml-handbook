import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c3-metric-sensitivity"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>Your experiments use <strong>GMV per user</strong> as the primary metric, with 500,000 users per arm for a week. Of the last 200 tests, only <strong>4%</strong> moved it significantly. A team proposes switching to <strong>share of users who add to cart</strong>, which moved in 22% of tests: "it is four times more sensitive".</p>
{table(["Metric", "Coefficient of variation per user", "Share of past tests significant"], [
["GMV per user", "8.0", "4%"], ["Buyers per user (4% buy)", "4.9", "7%"],
["Users who add to cart (25%)", "1.7", "22%"], ["Sessions per user", "1.5", "15%"]], narrow=True)}
<p>In the 30 past tests where both add-to-cart and GMV moved significantly, they moved in the same direction <strong>21</strong> times. What is the smallest change each metric can detect? Should the team switch?</p></div>
{attempt(S, 1)}{reveal(f'''<p>Minimum detectable effect, relative, at 80% power: 2.8 × CV × √(2 ÷ 500,000).</p>
<ul><li>GMV per user: <strong>4.5%</strong>. Few features move GMV by that much in a week, which is why only 4% of tests show anything.</li>
<li>Add-to-cart: <strong>1.0%</strong>, 4.6 times finer. Buyers: 2.7%. Sessions: 0.8%.</li></ul>
<p>So add-to-cart is far more <em>sensitive</em>. But a primary metric must also be <em>directional</em>: when it moves, the outcome you care about should move the same way. 21 of 30 is 70% agreement, so nearly a third of the time an add-to-cart win was a GMV loss, for example a feature that fills carts that are never bought.</p>
<p>Better answer: make GMV more sensitive (capping and CUPED take its detectable effect from 4.5% to about 2.2%), keep it as the decision metric, and use add-to-cart as a diagnostic or early signal, not the ship criterion. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>A bathroom scale and a fitness watch.</strong> To see whether a new diet works in two weeks, the scale is too noisy: daily weight swings by a kilo from water alone. Resting heart rate on a watch moves more reliably. But a lower heart rate is not weight loss; it might be better sleep.</p>
<p><strong>A shop judging a window display.</strong> Monthly profit barely registers one display. Footfall at the door responds within days. Footfall can rise while profit falls, if the display attracts browsers who do not buy.</p>
{table(["Idea", "Fitness", "Shop window", "Experiment metric"], [
["What you care about", "Weight", "Profit", "GMV, retention"],
["Too noisy to see small changes", "Daily weight", "Monthly profit", "GMV per user in one week"],
["Sensitive alternative", "Resting heart rate", "Footfall", "Add-to-cart, clicks, sessions"],
["The risk", "Heart rate improves, weight does not", "More browsers, fewer buyers", "Surrogate moves; outcome does not, or reverses"],
["The better fix", "Weigh at the same time daily, average a week", "Track conversion of footfall", "Reduce noise in the real metric; check directionality"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>A metric that responds quickly is only useful if its movements reliably point the same way as the outcome you actually want.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Heart rate and weight are both measured on you.</strong> In experiments, sensitivity depends on the population too: the same metric is sensitive for frequent users and hopeless for rare ones.</li>
<li><strong>Averaging a week of weights reduces noise.</strong> Experiments have more tools than time: capping, CUPED, better definitions, triggering on affected users.</li>
<li><strong>The shop owner sees both numbers daily.</strong> Directionality must be learned from many past experiments, which takes a corpus.</li></ul>
{tests([("Why is sensitivity a property of both the metric and the test, not the metric alone?", "<p>It depends on the metric's variance, the sample size, the test length, and how much typical features move it. The same metric can be sensitive for a checkout test and insensitive for a home-page test.</p>", True)])}"""

s3 = f"""<div class="fx">sensitivity = P(the metric detects a change | the feature changed something)
            ≈ P(the feature moves the metric)     movement probability
            × P(the test detects that movement)   statistical power

statistical power is set by
   relative MDE ≈ 2.8 × CV × √(2 / n)       80% power, 5% two-sided
   CV = standard deviation / mean, per randomisation unit

ways to raise it
   cap or winsorise heavy tails              lowers CV
   CUPED with pre-period values              × √(1 − ρ²)
   trigger on users who could see the change raises the effect
   binary or count versions of a metric      lower CV, different meaning

directionality: when the metric moves, does the north star move the same way?
   check on a corpus of past tests</div>
<ul>
<li><strong>Two halves of sensitivity.</strong> A metric can have low variance and still never move, such as \"has an account\". Power without movement is useless; movement without power is invisible. {ref(1)}</li>
<li><strong>A corpus of past tests</strong> is the evidence: how often each metric was significant, and when two metrics both moved, how often they agreed.</li>
<li><strong>Capping</strong> GMV at a high percentile removes the few huge buyers who dominate its variance. <strong>CUPED</strong> removes the predictable part using each user's pre-period value; see <a href="#a4-cuped">CUPED and variance reduction</a>.</li>
<li><strong>Triggering</strong> analyses only users who reached the changed page, which raises the effect size among those analysed without changing the noise per user.</li>
<li><strong>A more sensitive proxy</strong> is safe only if it is directional for the kind of change being tested. Validated surrogates are discussed in <a href="#a4-long-term-effects">novelty effects and long-term holdouts</a>.</li></ul>
{tests([("Why does halving a metric's CV have the same effect on its MDE as quadrupling the sample?", "<p>The MDE is proportional to CV ÷ √n. Halving CV halves the MDE; so does multiplying n by four.</p>", True),
("A metric has an MDE of 0.5% but has never been significant in 200 tests. Is it sensitive?", "<p>Statistically powerful, but features do not move it: its movement probability is near zero. It is not sensitive in the sense that matters.</p>")])}"""

s4 = f"""<h4>Worked: the MDEs</h4>
<p>500,000 users per arm, so √(2 ÷ 500,000) = 0.002, and 2.8 × 0.002 = 0.0056.</p>
<ul><li>GMV per user, CV 8: 0.0056 × 8 = <strong>4.5%</strong>.</li>
<li>Buyers, 4% buying: CV = √(0.96 ÷ 0.04) = 4.9, so <strong>2.7%</strong>.</li>
<li>Add-to-cart users, 25%: CV = √(0.75 ÷ 0.25) = 1.73, so <strong>1.0%</strong>.</li>
<li>To detect 1% on raw GMV per user would need (2.8 × 8 ÷ 0.01)² × 2 = about <strong>10 million users per arm</strong>.</li></ul>
<h4>Half-worked: making GMV sensitive</h4>
<p>Capping GMV per user at the 99.9th percentile cuts its CV from 8 to 5. CUPED with a pre-period correlation of 0.6 multiplies the remaining CV by √(1 − 0.36) = 0.8. Find the new MDE, and the power for a true 2% lift before and after.</p>
{reveal("<p>CV after both: 5 × 0.8 = 4, MDE = 0.0056 × 4 = <strong>2.2%</strong>, half of the original. Power for a 2% lift: <strong>24%</strong> on raw GMV, <strong>71%</strong> after capping and CUPED. The metric that matters becomes usable without switching to a proxy. The cap changes the metric slightly; report the uncapped number alongside.</p>")}
<h4>Bare: is add-to-cart directional?</h4>
<p>In 30 past tests where both metrics were significant, add-to-cart and GMV agreed 21 times and disagreed 9 times. Of the 9, 7 were tests of features that made adding to cart easier, such as a one-tap add button. What do you conclude about using add-to-cart as a decision metric?</p>
{reveal("<p>Its directionality depends on the kind of feature. For features that change the add step itself, it is a poor proxy, because adding becomes cheaper and less meaningful. For features upstream, such as ranking or search, it may be well aligned. Use it as a primary metric only for test types where its agreement with GMV has been high, and keep GMV as the guardrail or decision metric.</p>")}
<h4>Predict, then play</h4>
<p>Predict the power for a true 1% lift on add-to-cart, and on raw GMV, at 500,000 users per arm.</p>
{reveal("<p>About <strong>82%</strong> for add-to-cart and about <strong>9%</strong> for raw GMV. A 1% change is routine for add-to-cart to catch and nearly invisible in raw GMV. That gap is the whole temptation, and the reason directionality must be checked.</p>")}
<div class="lab" data-lab="sensitivity"></div>
<pre class="code">import numpy as np
from scipy.stats import norm

def mde(cv, n_per_arm, alpha=0.05, power=0.8):
    return (norm.ppf(1 - alpha / 2) + norm.ppf(power)) * cv * np.sqrt(2 / n_per_arm)

# CV per user from last month's data, capped and CUPED-adjusted
cv_raw = user_gmv.std() / user_gmv.mean()
capped = user_gmv.clip(upper=user_gmv.quantile(0.999))
rho = np.corrcoef(capped, pre_gmv)[0, 1]
cv_cuped = capped.std() * np.sqrt(1 - rho**2) / capped.mean()</pre>
{tests([("Why is a binary 'bought anything' metric more sensitive than GMV per user, and what does it give up?", "<p>It ignores how much each buyer spent, which removes the heavy tail, so its CV is lower. It gives up any effect on basket size: a feature that makes buyers spend more without changing who buys is invisible to it.</p>", True),
("A test triggers on users who opened the cart, 10% of all users. Why does that raise sensitivity?", "<p>Untriggered users cannot be affected, so including them dilutes the effect tenfold while adding noise. Analysing triggered users shows the effect at full size; the overall effect is then the triggered effect times the trigger rate.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["Lower variance means a better metric", "The metric does not move with features or the outcome", "Movement rate in the corpus near zero"],
["The proxy agrees with the north star", "Features game the proxy", "Disagreement in tests where both moved"],
["Agreement is uniform", "It depends on the feature type", "Split the corpus by area or type of change"],
["Capping does not change conclusions", "Effects concentrated among big spenders", "Report capped and uncapped; compare"],
["The corpus is unbiased", "Only tests that were reported, or that passed, are in it", "Include every test, including abandoned ones"],
["Past tests predict future ones", "Product strategy changes the kind of tests run", "Refresh the analysis yearly"]])}
{tests([("Your corpus only includes tests teams chose to write up. How does that bias the movement rates?", "<p>Upwards: tests with significant results are more likely to be written up, so every metric looks more sensitive than it is. Pull results directly from the platform for every test.</p>")])}"""

s6 = f"""{table(["Approach", "Answers", "Pick it when", "Watch out"], [
["MDE per metric", "Smallest detectable change", "Choosing metrics and test length", "Ignores whether features move it"],
["Movement rate in past tests", "How often features move it", "You have a corpus", "Selection bias in the corpus"],
["Directionality check", "Does it agree with the north star?", "Before promoting a proxy", "Needs tests where both moved"],
["Variance reduction", "Same metric, more power", "The right metric is too noisy", "Capping changes meaning slightly"],
["Triggering", "Bigger effect among those exposed", "Changes reach few users", "Trigger must be the same in both arms"],
["Surrogate index", "Long-term outcome from short-term metrics", "History links them", "Validation needed"]])}
{tests([("You can either switch to a proxy or make the real metric more sensitive. Which do you try first?", "<p>Make the real metric more sensitive: capping, CUPED, triggering. Only if that is not enough, adopt a proxy, and only for the kinds of test where its directionality has been shown.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Clicks as the metric for a ranking change.</strong></p>
<p><strong>Time on page for a content redesign.</strong></p></div>
<div><p class="label">Pair 2</p>
<p><strong>Revenue per user for a pricing test.</strong></p>
<p><strong>Retention for an onboarding change.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 are sensitive proxies that can mislead.</strong> Clickbait raises clicks and lowers purchases; confusing pages raise time on page. Both need directionality checks against the outcome.</p>
<p><strong>Pair 2 are the right outcomes but noisy or slow.</strong> Capping and CUPED help revenue; for retention, a validated early indicator or a longer test is needed.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Choosing the metric that moved. After a test, the team scans twenty metrics, finds that add-to-cart was significant, and promotes it to "the metric this feature was really about". That combines low directionality with <a href="#a2-multiple-testing">multiple testing</a>. Metrics are chosen for sensitivity and directionality before the test, from the corpus, not after.</p>
{tests([("A team says GMV is 'too insensitive to ever use' and drops it from all tests. What is the risk?", "<p>Features that raise engagement metrics while lowering GMV will ship unnoticed. Keep GMV as a guardrail with a non-inferiority margin, even if it cannot be the primary metric; see <a href='#a4-noninferiority'>non-inferiority tests</a>.</p>")])}"""

s8 = f"""<ul>
<li><strong>Publish an MDE table</strong> for every standard metric at typical traffic and test length, raw and variance-reduced.</li>
<li><strong>Build a test corpus</strong> from the platform: every test, every metric, effect and interval.</li>
<li><strong>Measure movement and agreement</strong> per metric and per area of the product, and refresh yearly.</li>
<li><strong>Apply capping and CUPED by default</strong> to heavy-tailed revenue metrics, reporting the raw value alongside.</li>
<li><strong>Trigger analyses</strong> on users who could be affected.</li>
<li><strong>Promote a proxy only with evidence</strong>, scoped to the test types where it agreed.</li></ul>
{tests([("What would you put in a one-page metric guide for product teams?", "<p>For each metric: what it measures, its MDE at typical traffic for one and two weeks, how often it moves, how often it agrees with GMV, the test types it suits, and whether it may be a primary metric or only a diagnostic.</p>")])}"""

s9 = f"""<ul>
<li><strong>Proxy or patience?</strong> Some teams prefer fast proxy metrics and many small tests; others prefer fewer, longer, outcome-based tests. The trade is speed against the risk of optimising the wrong thing.</li>
<li><strong>How much agreement is enough?</strong> 70% agreement means 30% of decisions on the proxy are wrong in direction. Whether that is tolerable depends on how costly a wrong ship is.</li>
<li><strong>Composite metrics.</strong> Combining several signals into one index can raise sensitivity and directionality, but makes the metric harder to explain and easier to game.</li>
<li><strong>Should variance reduction be default?</strong> It changes what dashboards show and confuses people who compare with raw reports. Most large platforms make it default anyway.</li></ul>
{tests([("Make the case for using a proxy metric despite 70% directional agreement.", "<p>If the alternative is tests that almost never detect anything, decisions are made on gut feel, which may agree less than 70%. A proxy with a GMV guardrail can be better than no signal, as long as large launches are confirmed on the outcome.</p>")])}"""

rungs = [
 {"ask": "What makes a metric sensitive for experiments?", "follow": ["What is the difference between power and movement?", "What is directionality?"],
  "weak": "<p>\"Low variance.\"</p>",
  "strong": "<p>Two things: statistical power, set by its variance relative to its mean and the sample size, and movement, how often features actually change it. A good decision metric also has directionality: when it moves, the outcome you care about moves the same way. All three are measured on a corpus of past tests.</p>"},
 {"ask": "GMV per user has a CV of 8 with 500,000 users per arm. Add-to-cart has a CV of 1.7 and agrees with GMV in 70% of tests. Which should be primary?", "follow": ["Compute the MDEs.", "Can you make GMV usable?"],
  "model": "<p>MDE for GMV is 2.8 × 8 × 0.002 = 4.5%; for add-to-cart, 1.0%. Add-to-cart is more sensitive but disagrees with GMV in 30% of cases, so it can ship GMV losses. Capping and CUPED bring GMV to about 2.2%. Keep GMV as the decision metric and use add-to-cart as a diagnostic, or as primary only for test types where it agreed reliably.</p>",
  "weak": "<p>Switches to add-to-cart because it is more sensitive.</p>",
  "strong": "<p><b>Must have.</b> Computes both MDEs and raises directionality.</p><p><b>Strong signal.</b> Makes GMV more sensitive rather than abandoning it, and scopes the proxy by test type.</p>"},
 {"ask": "How would you measure whether a proxy metric is directional?", "follow": ["What if few tests moved both?", "How does the corpus get biased?"],
  "weak": "<p>\"Check the correlation between the two metrics across users.\"</p>",
  "strong": "<p>Across past experiments, not users: in tests where both moved significantly, the share where they moved the same way, plus the correlation of their estimated effects across all tests. Split by type of change. With few joint movements, use all tests' effect estimates with their uncertainty. Pull every test from the platform to avoid write-up bias.</p>", "roles": ["ic"]},
 {"ask": "Design the metric strategy for an experimentation programme where most tests come back flat.", "follow": ["What do you change first?", "How do you keep GMV in the picture?"],
  "weak": "<p>\"Run tests for longer.\"</p>",
  "strong": "<p>Publish MDEs to show why tests are flat; apply capping and CUPED to revenue metrics; trigger analyses on exposed users; build a corpus to find metrics that move and agree with GMV; allow validated proxies as primary for specific test types, with GMV as a non-inferiority guardrail; confirm large launches on GMV with holdouts.</p>", "roles": ["lead", "ic"]},
 {"ask": "Product leadership wants to ship on clicks because 'GMV never moves'. What do you say?", "follow": ["They point to a competitor who uses clicks.", "What is your compromise?"],
  "weak": "<p>Refuses, or agrees without conditions.</p>",
  "strong": "<p>Agrees GMV as measured is too noisy and shows the fix that halves its MDE. Shows the corpus: clicks and GMV disagree often enough that shipping on clicks would have shipped specific losses, named. Proposes clicks as primary for ranking tests where agreement is high, GMV as a guardrail on all, and a quarterly holdout to check the programme's GMV effect.</p>", "roles": ["lead"]},
]

page(S, "C3", "Metric sensitivity",
     "A primary metric that never moves cannot guide decisions, and one that moves easily can point the wrong way. Sensitivity combines statistical power with how often features move the metric; directionality asks whether its moves agree with the outcome that matters.",
     "metric sensitivity directionality minimum detectable effect mde coefficient of variation movement probability proxy metric surrogate capping winsorising cuped triggering experiment corpus north star guardrail",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "A good experiment metric must be able to detect the changes features make, which depends on its variance and on how often features move it, and its movements must agree in direction with the outcome that matters, so reduce the noise in the real metric before reaching for a sensitive proxy, and validate any proxy on past tests.",
     ["Sensitivity = power × movement", "MDE ≈ 2.8 × CV × √(2/n)", "Capping, CUPED and triggering raise power", "Check directionality on a corpus of past tests", "Make the real metric usable before adopting a proxy"],
     [("c3-metric-design", "Designing metrics"), ("a3-sample-size-power", "Sample size and power"), ("a4-cuped", "CUPED and variance reduction")],
     [("c2-power-simulation", "Power and false positive rates by simulation"), ("a4-long-term-effects", "Novelty effects and long-term holdouts"), ("a4-noninferiority", "Equivalence and non-inferiority tests")],
     sources=[("Deng and Shi, \"Data-Driven Metric Development for Online Controlled Experiments: Seven Lessons Learned\", KDD 2016", "https://doi.org/10.1145/2939672.2939700")],
     sec_roles={11: ["lead", "ic", "mle"]})
