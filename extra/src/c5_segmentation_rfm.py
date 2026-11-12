import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c5-segmentation-rfm"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>An analyst ran k-means with four clusters on 50,000 buyers' <strong>recency</strong> (days since last order), <strong>frequency</strong> (orders in 12 months) and <strong>monetary</strong> value (12-month spend, ₹), as raw numbers. The result:</p>
{table(["Cluster", "Share of buyers", "Mean recency, days", "Mean orders", "Mean spend, ₹"], [
["A", "83%", "81", "3.2", "4,438"], ["B", "15%", "46", "6.5", "22,505"], ["C", "2%", "31", "9.9", "66,404"], ["D", "0.3%", "21", "14.7", "1,88,408"]], narrow=True)}
<p>Marketing plans a VIP programme for cluster D and \"general\" messaging for cluster A. What went wrong, and how would you build segments marketing can use?</p></div>
{attempt(S, 1)}{reveal(f'''<p>K-means measures distance in raw units. Spend has a standard deviation of about ₹15,000, recency about 85 days, frequency about 3 orders, so spend dominates every distance and the clusters are simply spend bands. Cluster A lumps a buyer who ordered yesterday with one who left nine months ago.</p>
<p><strong>Fix the scales</strong>: log-transform the skewed variables and standardise all three. K-means with four clusters then finds groups of 20 to 33% with distinct profiles: recent frequent high spenders (median 17 days, 7 orders), recent occasional buyers (11 days, 3 orders), lapsing regulars (74 days, 4 orders) and one-time lapsed buyers (101 days, 1 order). These differ on all three dimensions and suggest different actions.</p>
<p>Or skip clustering: <strong>RFM scores</strong> put each buyer into quintiles on each dimension, which is transparent and stable. Either way, check that segments are stable across runs, large enough to act on, and differ in how they respond to what marketing will do. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>Sorting a wardrobe.</strong> Sort clothes by weight in grams and the winter coats end up in one pile and everything else in another, socks with shirts. Sort by season, formality and colour, each counted fairly, and the piles become useful for getting dressed.</p>
<p><strong>A doctor's triage.</strong> Patients are grouped by a few vital signs, each measured on its own scale and judged against its own normal range. Nobody adds heart rate to temperature in raw numbers.</p>
{table(["Idea", "Wardrobe", "Triage", "Buyer segments"], [
["The things grouped", "Clothes", "Patients", "Buyers"],
["The dimensions", "Season, formality, colour", "Vital signs", "Recency, frequency, spend"],
["The scale trap", "Grams dominate", "Adding raw numbers", "Rupees dominate days and orders"],
["The fix", "Judge each dimension fairly", "Compare with each sign's normal range", "Log and standardise, or score by quintile"],
["The test of a good grouping", "Can you dress from a pile?", "Does each group get different care?", "Does each segment get a different action?"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>A grouping is only as good as how fairly it weighs the dimensions and whether each group leads to a different action.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Clothes stay put.</strong> Buyers move between segments every month, so segments must be refreshed and the flows between them tracked.</li>
<li><strong>Triage categories are agreed in advance.</strong> Clusters are discovered, and a different algorithm or k gives different ones. Stability has to be checked.</li>
<li><strong>Both groupings are for the item itself.</strong> Marketing segments are for deciding treatments, and two segments that look different may respond the same way.</li></ul>
{tests([("Why log-transform spend before standardising?", "<p>Spend is very right-skewed. Standardising without a log leaves a few huge spenders far from everyone, and k-means spends clusters on them. The log compresses the tail so differences between ordinary buyers count.</p>", True)])}"""

s3 = f"""<div class="fx">RFM
   R  recency     days since last purchase        lower is better
   F  frequency   purchases in a window
   M  monetary    spend in the window
   score each 1 to 5 by quintile → codes such as 5-5-5 ("champions"),
   1-1-1 ("lost"); group codes into a handful of named segments

behavioural clustering
   choose features (RFM, categories, channels, discount use, returns)
   transform skewed ones (log), standardise all
   k-means, Gaussian mixture or hierarchical; choose k by
     elbow / silhouette AND stability AND usefulness
   profile each cluster; name it; size it

a good segment is
   distinct · stable over time and runs · large enough · reachable ·
   responds differently to the action you plan</div>
<ul>
<li><strong>RFM</strong> is the old workhorse of direct marketing: three numbers almost every business has, which predict the next purchase well. Its segments are easy to explain. {ref(1)}</li>
<li><strong>Clustering</strong> can use many behaviours at once, but depends on feature choice, scaling and k. See <a href="#b5-kmeans">k-means and clustering</a>.</li>
<li><strong>Stability</strong>: rerun with different seeds and on different months; the adjusted Rand index between runs should be high. Here four clusters reproduce exactly (ARI 1.00) while six do not (0.69).</li>
<li><strong>Segments describe; they do not tell you what works.</strong> Which buyers a coupon changes is an <a href="#a5-uplift-hte">uplift</a> question, which may cut across RFM segments.</li></ul>
{tests([("A 'champions' segment has the highest response to a coupon. Should it get the most coupons?", "<p>Not necessarily. Champions buy anyway; their response may be mostly purchases that would have happened. Target by incremental response, measured in a test, not by response rate.</p>", True),
("Why is silhouette score alone a poor way to choose k?", "<p>It measures geometric separation, which buyer data rarely has; it often prefers k = 2. A segmentation is chosen for stability and usefulness as much as for separation.</p>")])}"""

s4 = f"""<h4>Worked: RFM scores</h4>
<p>Quintile cutoffs from the 50,000 buyers: recency 13, 31, 60, 119 days; orders 2, 3, 4, 6; spend ₹1,677, ₹3,365, ₹6,104, ₹12,084. Recency scores run the other way: more recent is better.</p>
{table(["Buyer", "Recency", "Orders", "Spend", "R", "F", "M", "Segment"], [
["1", "8 days", "9", "₹21,000", "5", "5", "5", "Champion"], ["2", "45 days", "3", "₹3,000", "3", "2", "2", "Needs attention"],
["3", "200 days", "7", "₹15,000", "1", "5", "5", "At risk: was valuable"], ["4", "10 days", "1", "₹900", "5", "1", "1", "New"]], narrow=True)}
<p>Buyer 3 is the interesting one: a high spender who has gone quiet. A spend-only view ranks them among the best customers; RFM flags them for a win-back.</p>
<h4>Half-worked: choosing k</h4>
<p>On log-scaled, standardised RFM, k = 4 gives four groups of 20 to 33% that reproduce exactly across random starts. k = 6 splits two of them further, but two runs agree only partly (ARI 0.69). Marketing has budget for three distinct campaigns. Which k, and what would you check next?</p>
{reveal("<p><strong>k = 4</strong>: stable, and close to the number of campaigns; two segments with similar planned treatment can share a campaign. Next, check each segment's stability month to month (how many buyers switch), its size in reachable buyers, and, most of all, whether segments respond differently to the planned campaigns, by testing each campaign in each segment.</p>")}
<h4>Bare: segment or score?</h4>
<p>The CRM team wants one segmentation for every purpose: email frequency, discount targeting, and choosing who gets early access to features. Is that wise?</p>
{reveal("<p>Probably not. Email frequency fits engagement-based segments such as RFM. Discount targeting should use uplift, who is changed by the discount, which RFM does not measure. Early access should use whatever predicts useful feedback, such as category expertise. One segmentation for everything becomes a compromise that serves none of them well. Keep RFM as a shared vocabulary, and build purpose-specific scores.</p>")}
<h4>Predict, then play</h4>
<p>Predict what happens to the clusters if you keep raw units but add a fourth feature, \"share of orders on mobile\", which runs from 0 to 1.</p>
{reveal("<p>Nothing visible. Its spread is a fraction of one unit against spend's thousands of rupees, so k-means ignores it completely. A feature that cannot move the distance cannot shape the clusters, however important it is.</p>")}
<div class="lab" data-lab="rfm"></div>
<pre class="code">import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

Z = np.log1p(df[["recency_days", "orders_12m", "spend_12m"]])
Z = (Z - Z.mean()) / Z.std()
labels = KMeans(4, n_init=10, random_state=0).fit_predict(Z)
df.groupby(labels)[["recency_days", "orders_12m", "spend_12m"]].median()   # profile
# stability: different seeds, and last month against this month
adjusted_rand_score(KMeans(4, n_init=1, random_state=1).fit_predict(Z),
                    KMeans(4, n_init=1, random_state=2).fit_predict(Z))</pre>
{tests([("Why profile clusters with medians rather than means?", "<p>Spend and frequency are skewed; a few large buyers pull the mean far from the typical buyer in the cluster. The median describes the buyers marketing will actually reach.</p>", True),
("A third of buyers change segment every month. Is the segmentation broken?", "<p>Not necessarily: recency changes by definition. But treatments that take weeks to run need stable targets. Track flows between segments, and consider longer windows or smoothing.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["Features are on comparable scales", "Rupees dominate days", "One feature explains nearly all differences between clusters"],
["Clusters exist", "Buyers vary on a continuum", "Low silhouette; unstable across seeds"],
["The chosen k is meaningful", "Different k tell different stories", "Stability by k; agreement across months"],
["Segments respond differently", "All segments react the same to a campaign", "Test campaigns within segments"],
["The window is right", "Seasonal buyers look lapsed outside their season", "Compare windows; add seasonality features"],
["Segments are about buyers", "They reflect data gaps, such as logged-out buying", "Check coverage by segment"]])}
{tests([("A cluster of 'bargain hunters' turns out to be buyers whose orders all came during a sale week. What went wrong?", "<p>The window coincided with a sale, so behaviour in it reflected the calendar, not the buyer. Use windows that cover whole seasons, or features that compare sale and non-sale behaviour.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["RFM quintile scores", "Who is engaged and valuable, transparently", "Lifecycle and CRM programmes", "Only three dimensions"],
["k-means on scaled behaviour", "Natural groups across many behaviours", "Exploring behaviour types", "Scaling, k and stability"],
["Gaussian mixture", "Soft membership; groups of different shapes", "Overlapping segments", "More parameters; less stable"],
["Hierarchical clustering", "Nested groups", "Small samples; taxonomy building", "Slow on large data"],
["Rules from domain knowledge", "Segments everyone recognises", "Operations and reporting", "May miss real structure"],
["Uplift or propensity scores", "Who to target for an action", "Targeting decisions", "See <a href='#a5-uplift-hte'>uplift</a> and <a href='#c5-churn-propensity'>propensity</a>"]])}
{tests([("Which method for deciding who receives a win-back discount?", "<p>An uplift model trained on a test of the discount, perhaps applied within the RFM 'at risk' segment. RFM alone tells you who is lapsing, not who a discount will bring back.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>A win-back email for lapsed high spenders.</strong></p>
<p><strong>Email frequency by engagement level.</strong></p></div>
<div><p class="label">Pair 2</p>
<p><strong>Personas for the product team.</strong> \"Deal seekers\", \"collectors\", \"gift buyers\".</p>
<p><strong>Seller tiers for account management.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 uses RFM directly.</strong> Recency, frequency and spend say who is lapsing and who is engaged, which is exactly what these programmes act on.</p>
<p><strong>Pair 2 uses richer clustering</strong>, on categories, price points and behaviour, to describe kinds of users or sellers. It is useful for design and staffing, and needs qualitative research to give the clusters meaning; see <a href="#c6-qual-quant">joining qual and quant</a>.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Segments as a final answer. A segmentation deck names six personas, sizes them, and stops. No one tests whether they respond differently to anything, the segments drift within months, and the deck becomes vocabulary without decisions. A segmentation is worth its cost only if a treatment differs by segment and the difference is measured.</p>
{tests([("How would you check that a segmentation is worth keeping a year later?", "<p>Count the decisions that used it, test whether segments still respond differently to the main treatments, and measure its stability. If none of those holds, retire it.</p>")])}"""

s8 = f"""<ul>
<li><strong>Start with the decision</strong> the segments will drive, and the treatments they will receive.</li>
<li><strong>Use RFM as the baseline</strong>; cluster only if RFM misses something that matters.</li>
<li><strong>Log and standardise</strong> skewed features; check each feature's influence on the result.</li>
<li><strong>Choose k for stability and use</strong>, with silhouette as a hint.</li>
<li><strong>Profile with medians</strong>, name segments in plain words, and size them in reachable buyers.</li>
<li><strong>Test treatments by segment</strong>, and refresh segments on a schedule, tracking flows between them.</li></ul>
{tests([("Marketing wants to rename clusters with catchy persona names. Any risk?", "<p>Names carry stories the data may not support, such as \"gift buyers\" for a cluster defined by December purchases. Ground names in the profile and validate with qualitative research before they stick.</p>")])}"""

s9 = f"""<ul>
<li><strong>RFM or clustering?</strong> RFM is simple, stable and predictive; clustering is richer and fragile. Many teams keep RFM for operations and use clusters for insight.</li>
<li><strong>Are personas useful?</strong> Product teams find them humanising; analysts warn they turn averages into imaginary people. Pairing them with sizes and real examples helps.</li>
<li><strong>Segments or individual scores?</strong> With enough data, individual propensity or uplift scores outperform segments for targeting. Segments survive because people can reason about them.</li>
<li><strong>How often to refresh?</strong> Monthly keeps them current; quarterly keeps them stable enough for campaigns. The answer depends on how fast behaviour changes.</li></ul>
{tests([("Make the case for keeping segments even when individual scores target better.", "<p>Segments give teams a shared language, make strategy discussable, and let you design different experiences, not just choose who receives one. Scores optimise a single action; segments organise thinking.</p>")])}"""

rungs = [
 {"ask": "What is RFM segmentation, and why is it so widely used?", "follow": ["How do you score it?", "What does it miss?"],
  "weak": "<p>\"Grouping customers by how much they spend.\"</p>",
  "strong": "<p>Recency, frequency and monetary value, each scored by quintile, and the codes grouped into named segments such as champions, at risk, new and lost. It uses data every business has, predicts the next purchase well, and is easy to explain. It misses what people buy, how they shop, and who responds to a given action.</p>"},
 {"ask": "K-means on raw recency, frequency and spend gave clusters of 83%, 15%, 2% and 0.3%. What happened and how do you fix it?", "follow": ["Which feature drove the clusters?", "How would you choose k?"],
  "model": "<p>spend's standard deviation in rupees is thousands of times recency's in days, so the clusters are spend bands. Log-transform the skewed features and standardise; four clusters of 20 to 33% then appear with distinct recency, frequency and spend, and they reproduce across random starts. Choose k for stability and the number of distinct actions, not silhouette alone.</p>",
  "weak": "<p>Tries a different k without changing scales.</p>",
  "strong": "<p><b>Must have.</b> Identifies scale dominance and fixes it with transformation and standardisation.</p><p><b>Strong signal.</b> Checks stability and asks whether segments respond differently.</p>"},
 {"ask": "How do you know a segmentation is good?", "follow": ["What is ARI?", "What is the most important test?"],
  "weak": "<p>\"A high silhouette score.\"</p>",
  "strong": "<p>Distinct profiles; stable across seeds, samples and months (high adjusted Rand index); large and reachable segments; and, most important, segments that respond differently to the actions planned, shown in tests. If every segment reacts the same, the segmentation adds nothing to the decision.</p>", "roles": ["ic"]},
 {"ask": "Design a buyer segmentation for a marketplace CRM programme.", "follow": ["Which features?", "How is it used and refreshed?"],
  "weak": "<p>\"Cluster all available features.\"</p>",
  "strong": "<p>Start from the decisions: email frequency, win-back, loyalty offers. Use RFM as the backbone with a few behavioural features such as category breadth and discount share, log-scaled and standardised. Four to six named segments, stable across months, sized in reachable buyers. Each campaign tested within segments; uplift models for discount targeting. Monthly refresh with a flow report between segments.</p>", "roles": ["lead", "ic"]},
 {"ask": "Marketing wants to send the 'champions' segment the biggest discount because they respond best. Respond.", "follow": ["How would you show it?", "What would you propose instead?"],
  "weak": "<p>Agrees because champions have the highest response rate.</p>",
  "strong": "<p>Champions buy anyway, so much of their response is purchases that would have happened; the discount is mostly margin given away. Propose a test with a holdout in each segment to measure incremental response, then send discounts where the increment per rupee is highest, often the at-risk segment.</p>", "roles": ["lead"]},
]

page(S, "C5", "Behavioural segmentation and RFM",
     "Recency, frequency and monetary value sort buyers into groups that marketing can act on. Clustering can use more behaviours, but only after the scales are fixed, and only if the segments are stable and respond differently to what you plan to do.",
     "segmentation rfm recency frequency monetary quintile scores champions at risk k-means clustering standardise log transform stability adjusted rand index personas crm targeting",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Group buyers by recency, frequency and spend, scored by quintile or clustered after log-scaling and standardising so no single unit dominates, and keep only segments that are stable, large enough and respond differently to the actions you plan.",
     ["RFM: three numbers that predict the next purchase", "Scale before clustering, or rupees decide everything", "Choose k for stability and use", "Profile with medians; name in plain words", "Segments must respond differently to be worth it"],
     [("b5-kmeans", "k-means and clustering"), ("c1-retention-funnels", "Cohort retention and funnels"), ("c4-unit-economics", "Unit economics, LTV and CAC")],
     [("a5-uplift-hte", "Uplift and heterogeneous effects"), ("c5-churn-propensity", "Churn and propensity models"), ("c6-qual-quant", "Joining survey, PSAT and UXR findings to behavioural data")],
     sources=[("Fader, Hardie and Lee, \"RFM and CLV: Using Iso-Value Curves for Customer Base Analysis\", Journal of Marketing Research, 2005", "https://doi.org/10.1509/jmkr.2005.42.4.415")],
     sec_roles={11: ["lead", "ic", "mle"]})
