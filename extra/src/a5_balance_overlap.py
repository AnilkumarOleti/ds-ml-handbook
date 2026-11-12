import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "a5-balance-overlap"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>2,000 sellers opted into a coaching programme. 18,000 did not. Before estimating its effect, an analyst compares the two groups and reports a p-value for each covariate:</p>
{table(["Before matching", "Joined: mean (sd)", "Did not: mean (sd)", "p-value"], [
["Prior 90-day GMV, ₹ thousand", "420 (300)", "260 (240)", "&lt; 0.001"],
["Active listings", "85 (60)", "70 (55)", "&lt; 0.001"],
["Tenure, months", "30 (20)", "29 (22)", "0.036"],
["Rating", "4.6 (0.3)", "4.5 (0.4)", "&lt; 0.001"]], narrow=True)}
<p>After propensity matching, 2,000 joiners against 2,000 matched non-joiners, every p-value is above 0.2, and the analyst writes "balance achieved".</p>
<p>Which covariates were really out of balance before matching? Is "every p-value above 0.2" evidence of balance?</p></div>
{attempt(S, 1)}{reveal(f'''<p>Measure balance in standard deviations, not p-values. The <strong>standardised mean difference</strong> is the gap divided by the pooled standard deviation:</p>
<ul><li>GMV: 160 ÷ 272 = <strong>0.59</strong>, badly imbalanced. Listings: <strong>0.26</strong>. Rating: <strong>0.28</strong>. Tenure: <strong>0.05</strong>, fine, despite p = 0.036.</li></ul>
<p>Tenure is "significant" only because 20,000 sellers make tiny gaps detectable. After matching there are 4,000 sellers, so the same gap gives a larger p-value: the p-values rose partly because the sample shrank. A p-value measures how sure you are a gap exists, not whether it is big enough to bias the estimate.</p>
<p>The check that counts: every SMD below about 0.1 after matching, variance ratios between about 0.5 and 2, and the same for squares and interactions of the strongest confounders. Here the matched SMDs are 0.03, 0.03, −0.05 and 0.06, so the balance claim holds, for a reason the analyst did not give. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>Weighing two bags of flour.</strong> To check whether two bags weigh the same, you put them on a scale and read the difference in grams. You do not ask how confident you are that they differ. With a sensitive enough scale, they always differ; what matters is whether the difference would spoil the recipe.</p>
<p><strong>A fair race between age groups.</strong> To compare two training plans, you pair runners of similar age and fitness. A pair of a 25-year-old and a 60-year-old tells you nothing, however you adjust, because there is no runner like the 60-year-old in the other plan. You set those runners aside and say the comparison is for the ages you could pair.</p>
{table(["Idea", "Flour", "Race", "Causal estimate"], [
["What you check", "Weight difference", "Who can be paired", "Covariate gaps and overlap"],
["The right scale", "Grams, against the recipe", "Similar age and fitness", "Standard deviations (SMD)"],
["The wrong test", "Are they different at all?", "Can a model adjust for age?", "Is the p-value small?"],
["When it fails", "One bag is far heavier", "No comparable runner exists", "No similar untreated units"],
["What you do", "Adjust until close", "Drop unpairable runners and say so", "Trim, restate the population"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>A comparison is only as good as the similarity of the things compared, measured on a scale that matters for the result and limited to the cases where similar counterparts exist.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Flour has one dimension.</strong> Sellers have dozens. Balance on every mean can hide imbalance in spread, in combinations, or in the tail.</li>
<li><strong>Runners are visible.</strong> Balance can only be checked on measured covariates. Perfect balance says nothing about the confounders you did not record.</li>
<li><strong>Setting runners aside is free.</strong> Dropping treated units changes the question: the estimate now applies to the joiners who resemble non-joiners, who may be the less interesting ones.</li></ul>
{tests([("After matching, mean GMV is identical in both groups, but the joiners' standard deviation is twice the matched controls'. Is GMV balanced?", "<p>No. The variance ratio is 4. The joiners include many very small and very large sellers that the controls lack, and if the effect varies with size, the estimate is biased. Check variance ratios and the distribution, not only means.</p>")])}"""

s3 = f"""<div class="fx">standardised mean difference (SMD)
    SMD = (mean_treated − mean_control) / √((sd_t² + sd_c²) / 2)
    |SMD| &lt; 0.1      usual threshold after adjustment
variance ratio      sd_t² / sd_c², want roughly 0.5 to 2
love plot           SMD for every covariate, before and after

overlap (common support, positivity)
    every treated unit has comparable untreated units
    check: propensity distributions by group
    trim: drop units with e(x) &lt; a or &gt; 1 − a, e.g. a = 0.1

coarsened exact matching (CEM)
    1. coarsen each covariate into bins
    2. form strata from every combination of bins
    3. drop strata without both treated and untreated units
    4. weight so each stratum's controls match its treated count</div>
<ul>
<li><strong>Balance is a property of the sample</strong>, not of a population, so hypothesis tests are the wrong tool. SMDs do not depend on sample size.</li>
<li><strong>Balance on the right things.</strong> Pre-treatment confounders, chosen with a causal diagram (see <a href="#a5-confounding-dags">confounders, mediators and colliders</a>). Never balance on mediators or on variables measured after treatment.</li>
<li><strong>Overlap comes first.</strong> Where the propensity is near 0 or 1, there is nobody to compare with, and any estimate there is extrapolation from a model.</li>
<li><strong>CEM</strong> fixes the acceptable imbalance before matching, through the bin widths, instead of checking it afterwards. Within a stratum, treated and control units are equal on the coarsened values by construction. {ref(2)}</li>
<li><strong>Trimming changes the estimand.</strong> After dropping units without overlap, the estimate is for the population that remains. Say so in the readout. {ref(3)}</li></ul>
{tests([("Why should balance not be checked with t-tests after matching?", "<p>Matching shrinks the sample, so p-values rise even if gaps do not. And balance is about the size of the gap in this sample, which is what biases the estimate, not about whether a gap exists in some population.</p>", True),
("An analyst balances the treated and control groups on GMV in the 30 days after the programme started. What is wrong?", "<p>That GMV is an outcome, possibly changed by the programme. Balancing on it removes part of the effect. Balance only on variables measured before treatment.</p>")])}"""

s4 = f"""<h4>Worked: the SMD and the variance ratio</h4>
<p>Prior GMV before matching: joiners 420 (sd 300), non-joiners 260 (sd 240).</p>
<ul><li>Pooled sd: √((300² + 240²) / 2) = √73,800 = 272. SMD = 160 ÷ 272 = <strong>0.59</strong>.</li>
<li>Variance ratio: 300² ÷ 240² = <strong>1.56</strong>, within 0.5 to 2, but the means are far apart.</li>
<li>After matching, controls have mean 410 and sd 290: SMD = 10 ÷ 295 = <strong>0.03</strong>, variance ratio <strong>1.07</strong>.</li></ul>
<p>Tenure before matching: 30 against 29 months, SMD <strong>0.05</strong>. Its t-statistic with 2,000 and 18,000 sellers is 1 ÷ √(400/2,000 + 484/18,000) = <strong>2.1</strong>, "significant", for a gap of one month. Rating before matching has a variance ratio of 0.3² ÷ 0.4² = <strong>0.56</strong>, near the edge: non-joiners are more spread out, so some have ratings no joiner has.</p>
<h4>Half-worked: coarsened exact matching</h4>
<p>Coarsen prior GMV into low, mid and high, and category into fashion and electronics. Next-90-day GMV in ₹ thousand:</p>
{table(["Stratum", "Joined", "Did not", "Joined: mean", "Did not: mean"], [
["Low, fashion", "300", "6,000", "105", "100"], ["Low, electronics", "200", "4,000", "112", "104"],
["Mid, fashion", "500", "3,500", "160", "148"], ["Mid, electronics", "400", "2,500", "175", "160"],
["High, fashion", "450", "1,500", "300", "280"], ["High, electronics", "150", "0", "330", "—"]], narrow=True)}
<p>The raw comparison: joiners average 194.2, non-joiners 134.5, a gap of <strong>59.7</strong>. The high-electronics stratum has no non-joiners, so CEM drops it. Weight the remaining stratum differences (5, 8, 12, 15, 20) by the number of joiners in each. Find the effect on the treated, and say how many joiners it covers.</p>
{reveal("<p>(300 × 5 + 200 × 8 + 500 × 12 + 400 × 15 + 450 × 20) ÷ 1,850 = 24,100 ÷ 1,850 = <strong>₹13.0 thousand</strong> per seller, a fifth of the raw gap. It covers <strong>1,850 of 2,000 joiners</strong>; the 150 large electronics sellers have no comparison, and the readout must say the estimate excludes them. Most of the raw gap was that joiners were bigger sellers to begin with.</p>")}
<h4>Bare: what trimming does</h4>
<p>The propensity model gives 20% of joiners a score above 0.9. The analyst trims everyone outside 0.1 to 0.9 and reports the effect as "the programme's effect". What is it now the effect for, and what would you write instead?</p>
{reveal("<p>For sellers whose choice to join was uncertain given their covariates, which excludes the most obvious joiners, likely the most engaged sellers. Write: \"the effect for the 80% of joiners who had comparable non-joiners; for the most engaged fifth there is no comparison group, and the data cannot say.\" If the effect for that fifth matters, the answer is a design change, such as an encouragement experiment, not a different model.</p>")}
<h4>Predict, then play</h4>
<p>Propensity scores on the log-odds scale are spread with sd 1 in each group. Predict the share of joiners lost to trimming at 0.1 and 0.9 when the groups' centres are 2 units apart, and 3 units apart.</p>
{reveal("<p>About <strong>12%</strong> at 2 units and about <strong>24%</strong> at 3. Overlap falls off quickly as the groups separate, and the joiners lost are the most distinctive ones.</p>")}
<div class="lab" data-lab="overlap"></div>
<pre class="code">import numpy as np

def smd(x_t, x_c):
    return (x_t.mean() - x_c.mean()) / np.sqrt((x_t.var(ddof=1) + x_c.var(ddof=1)) / 2)

# love plot data: one row per covariate, before and after
before = {{c: smd(df.loc[t, c], df.loc[~t, c]) for c in covs}}
after  = {{c: smd(df.loc[t, c], matched.loc[:, c]) for c in covs}}
# also check squares and key interactions, e.g. gmv**2, gmv * electronics</pre>
{tests([("Why is CEM's matched estimate equal on the coarsened covariates by construction, but not exactly balanced on the raw covariates?", "<p>Within a bin the raw values still differ: a low-GMV joiner may sit near the top of the bin and its controls near the bottom. Finer bins reduce that residual imbalance but drop more strata.</p>", True),
("After CEM, a stratum has 450 joiners and 1,500 controls. Why do those controls get a weight above 1 in the ATT?", "<p>The controls are reweighted so that, across strata, they are distributed like the joiners. This stratum has more joiners relative to controls than average, so each control stands for more joiners. With these numbers the weight is about 2.8.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["All confounders are measured", "Motivation, which drives both joining and sales, is unrecorded", "Balance looks perfect and the estimate is still biased; run sensitivity analysis"],
["Balance on means is enough", "Spreads or combinations differ", "Variance ratios, SMDs of squares and interactions, distribution plots"],
["Overlap is adequate", "Some treated units have no comparable controls", "Propensity histograms by group; extreme weights"],
["Bins are fine enough", "CEM bins lump very different sellers together", "Residual imbalance within strata; try finer bins"],
["The trimmed population is the one you care about", "The excluded units are the most important", "Describe who was dropped; compare their covariates"],
["Balance was checked on what was used", "The model balanced on a different set from the one reported", "Report balance for every covariate in the causal diagram"]])}
{tests([("Every SMD is below 0.05 after matching. A stakeholder concludes the estimate is causal. What do you say?", "<p>Balance is shown only for measured covariates. It removes measured confounding, not unmeasured. Report how large an unmeasured confounder would need to be to change the conclusion; see <a href='#a5-sensitivity-falsification'>sensitivity and falsification</a>.</p>")])}"""

s6 = f"""{table(["Tool", "Answers", "Pick it when", "Watch out"], [
["SMD and love plot", "Are measured covariates balanced?", "After any matching or weighting", "Says nothing about unmeasured ones"],
["Variance ratio and distribution plots", "Do spreads and shapes match?", "Skewed covariates such as GMV", "Many plots to read"],
["Propensity histograms", "Is there overlap?", "Before choosing a method", "Depend on the propensity model"],
["Trimming", "Removes units without comparison", "Weights are extreme", "Changes the estimand"],
["Coarsened exact matching", "Balance fixed in advance", "A few strong confounders with natural bins", "Many covariates empty the strata"],
["Propensity matching or weighting", "Balance on many covariates", "Many covariates", "Balance must be checked afterwards; see <a href='#a5-matching-propensity'>matching</a>"]])}
{tests([("You have three strong confounders, all with natural bands, and twenty weak ones. What combination would you use?", "<p>CEM on the three strong confounders, then regression or a propensity model within the matched sample for the weak ones, and a love plot for all twenty-three.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>A loyalty programme.</strong> Members spent 60% more before joining.</p>
<p><strong>A premium seller tool.</strong> Adopters had twice the listings beforehand.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A credit line for sellers.</strong> Only sellers with a score above 700 were eligible.</p>
<p><strong>A feature available only on the newest app.</strong> Older phones cannot run it.</p></div></div>
{reveal('''<p><strong>Pair 1 is imbalance.</strong> The groups overlap but differ in level. Matching or weighting can fix it, and the SMD shows how far it got.</p>
<p><strong>Pair 2 is a failure of overlap.</strong> Nobody below 700 got credit; nobody on an old phone used the feature. No weighting can compare where there is nobody to compare with. The first case suits <a href="#a5-instrumental-variables">regression discontinuity</a> at the 700 cutoff; the second can only be estimated for users with new phones.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>"Table 1" with p-values. The table comparing groups lists a significance test per covariate and calls the groups balanced when none is significant. In a small study nothing is significant and the groups can still differ badly; in a large one everything is significant and the gaps can be trivial. The guidance in medical statistics has long been to report standardised differences instead. {ref(1)}</p>
{tests([("A matched study of 300 users shows no significant difference on any covariate. Is that reassuring?", "<p>Not by itself. With 150 per group, a gap of 0.2 standard deviations, enough to bias the result, is not significant. Look at the SMDs.</p>")])}"""

s8 = f"""<ul>
<li><strong>Plot overlap before choosing a method.</strong> If it is poor, decide the population first and say so.</li>
<li><strong>Report a love plot</strong> for every covariate in the causal diagram, before and after, and a variance ratio for skewed ones.</li>
<li><strong>Check squares and interactions</strong> of the two or three strongest confounders.</li>
<li><strong>Iterate the propensity model on balance, not on its AUC.</strong> A propensity model that predicts treatment very well usually means poor overlap.</li>
<li><strong>Bin by meaning in CEM</strong>: GMV bands sellers recognise, category, region. Report how many treated units were dropped.</li>
<li><strong>Write the estimand into the readout</strong>: the effect for which units.</li></ul>
{tests([("Your propensity model has an AUC of 0.95. Is that good news?", "<p>Not for estimating effects. It means treatment is nearly predictable from covariates, so many units have scores near 0 or 1 and little overlap. Expect extreme weights and heavy trimming.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is 0.1 the right threshold?</strong> It is a convention, not a theorem. A small SMD on a very strong confounder can bias more than a larger one on a weak confounder. Some analysts weight the threshold by each covariate's link to the outcome.</li>
<li><strong>Match or regress?</strong> Matching makes the comparison transparent and design-based; regression uses every unit but extrapolates silently. Matching followed by regression on the matched sample is a common middle path.</li>
<li><strong>How much trimming is too much?</strong> Each dropped unit reduces bias but narrows the population. There is no rule, only a duty to report it.</li>
<li><strong>Is balance enough without a design?</strong> Some argue observational estimates should be judged by whether the selection mechanism is understood, not by tables of balance. A perfect love plot on the wrong covariates is worthless.</li></ul>
{tests([("Make the case for regression adjustment over matching.", "<p>It uses all the data, gives smaller standard errors, handles many covariates, and, with flexible terms, can model effects that vary. Its weakness, silent extrapolation, can be checked with overlap plots without discarding units.</p>")])}"""

rungs = [
 {"ask": "How do you check whether matching worked?", "follow": ["Why not t-tests?", "What threshold do you use?"],
  "weak": "<p>\"Check that the treated and control means are not significantly different.\"</p>",
  "strong": "<p>Standardised mean differences for every pre-treatment confounder before and after, aiming below about 0.1; variance ratios near 1 for continuous covariates; the same for squares and key interactions; and a look at overlap. Not t-tests: they depend on sample size, and matching shrinks it.</p>"},
 {"ask": "Joiners' prior GMV averages 420 with sd 300; non-joiners' 260 with sd 240. Tenure is 30 against 29 months with p = 0.036. Which is the bigger balance problem?", "follow": ["After matching all p-values exceed 0.2. Balanced?", "What would you report?"],
  "model": "<p>GMV: SMD = 160 ÷ 272 = 0.59, severe. Tenure: SMD 0.05, negligible; it is significant only because 20,000 sellers detect tiny gaps. Report SMDs, and after matching check that each is below 0.1, not that p-values are large, since the matched sample is smaller.</p>",
  "weak": "<p>Says tenure is a problem because it is significant.</p>",
  "strong": "<p><b>Must have.</b> Computes the SMDs and explains why the p-value misleads in both directions.</p><p><b>Strong signal.</b> Adds variance ratios and checks on squares of GMV.</p>"},
 {"ask": "A fifth of treated users have propensity scores above 0.95. What does that mean, and what do you do?", "follow": ["Who are those users likely to be?", "What does your estimate now describe?"],
  "weak": "<p>\"Clip the weights at 0.95 and continue.\"</p>",
  "strong": "<p>Poor overlap: those users have almost no comparable untreated users, so any estimate for them extrapolates from the model. Trim or restrict to the region of overlap, and restate the estimand as the effect for users with comparable controls. Describe who was dropped. If their effect matters, it needs a different design, such as an encouragement experiment.</p>", "roles": ["lead", "ic"]},
 {"ask": "Design the balance and overlap checks an analytics team must show before any observational causal estimate goes to leadership.", "follow": ["Who decides the covariate list?", "What happens when a check fails?"],
  "weak": "<p>\"A table of means.\"</p>",
  "strong": "<p>A causal diagram that fixes the covariates in advance; propensity histograms by group; a love plot of SMDs before and after with a 0.1 line; variance ratios for skewed covariates; the number and description of trimmed units with the resulting estimand; and a sensitivity analysis for unmeasured confounding. A failed check sends the analysis back, or the readout states the limitation in its first lines.</p>", "roles": ["lead", "ic"]},
 {"ask": "An analyst shows perfect balance after matching and a 12% effect of a seller programme. The programme's owner wants it in the board deck. What do you ask?", "follow": ["The analyst says balance proves causality. Respond.", "What would make you comfortable?"],
  "weak": "<p>Approves because the balance table is clean.</p>",
  "strong": "<p>Which covariates were balanced and why those; whether any were measured after joining; how many joiners were dropped and who they were; what the estimate is for; and how strong an unmeasured confounder such as seller motivation would need to be to erase 12%. Balance removes only measured confounding. I would be comfortable with a sensitivity analysis showing a robust result, or a design such as staggered rollout behind it.</p>", "roles": ["lead"]},
]

page(S, "A5", "Covariate balance, overlap and coarsened exact matching",
     "Matching and weighting only work if the groups end up alike on the covariates that matter, and if every treated unit has someone comparable to be matched with. This page covers measuring balance in standard deviations, checking overlap, and coarsened exact matching, which fixes the balance you accept before you match.",
     "covariate balance standardised mean difference smd variance ratio love plot overlap common support positivity trimming coarsened exact matching cem strata table 1 propensity estimand",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Before trusting a matched or weighted comparison, check that the groups are alike in standard deviations rather than p-values, that every treated unit has comparable controls, and state which units the estimate covers once those without overlap are trimmed or left unmatched.",
     ["Balance is measured with standardised differences, not tests", "Check spreads, squares and interactions too", "Overlap first: no comparison, no estimate", "CEM fixes the acceptable imbalance before matching", "Trimming changes whom the estimate is about"],
     [("a5-confounding-dags", "Confounders, mediators and colliders"), ("a5-matching-propensity", "Matching and propensity scores"), ("a2-p-values", "p-values and hypothesis tests")],
     [("a5-double-ml", "Double/debiased machine learning"), ("a5-sensitivity-falsification", "Sensitivity to hidden confounding and falsification tests"), ("a5-uplift-hte", "Uplift and heterogeneous effects")],
     sources=[("Austin, \"Balance diagnostics for comparing the distribution of baseline covariates between treatment groups in propensity-score matched samples\", Statistics in Medicine, 2009", "https://doi.org/10.1002/sim.3697"),
              ("Iacus, King and Porro, \"Causal Inference without Balance Checking: Coarsened Exact Matching\", Political Analysis, 2012", "https://doi.org/10.1093/pan/mpr013"),
              ("Crump, Hotz, Imbens and Mitnik, \"Dealing with limited overlap in estimation of average treatment effects\", Biometrika, 2009", "https://doi.org/10.1093/biomet/asn055")],
     sec_roles={11: ["lead", "ic", "mle"]})
