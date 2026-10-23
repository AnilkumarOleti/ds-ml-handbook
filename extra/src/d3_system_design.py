import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "d3-system-design"
R = ["ic", "mle"]

BANDS = table(["Score band", "Mean P(counterfeit)", "Listings a day", "Counterfeits a day"], [
    ["Very high", "0.95", "20,000", "19,000"], ["High", "0.60", "30,000", "18,000"], ["Medium", "0.20", "60,000", "12,000"],
    ["Low", "0.05", "2,00,000", "10,000"], ["Very low", "0.002", "96,90,000", "19,380"]], narrow=True)

s1 = f"""<div class="problem"><p>The interviewer says: <em>"Design a system that stops counterfeit listings on a marketplace."</em> Ten million listings are created a day. You have 45 minutes.</p>
<p>Before you draw a single box, write down the five questions whose answers change the design. For each, say what would change.</p></div>
{attempt(S, 1)}{reveal('''<ol>
<li><strong>What decision does the system make, and when?</strong> Block at publish, hide pending review, or flag after publication. Blocking at publish means a latency budget of a few hundred milliseconds. Flagging afterwards allows a batch job and heavier models.</li>
<li><strong>What does each mistake cost?</strong> A missed counterfeit (refunds, lost buyer trust, brand complaints) against a wrongly blocked genuine seller (lost sales, a support ticket, a seller who leaves). The ratio sets every threshold.</li>
<li><strong>How many human reviews are available a day?</strong> Review capacity, not model accuracy, usually decides how many listings get a careful look.</li>
<li><strong>Where do labels come from?</strong> Reviewer decisions, buyer reports, brand-owner takedowns, returns marked "not as described". Each arrives at a different delay and covers a different slice, and reviewers only label what the model sent them.</li>
<li><strong>How will we know it works?</strong> An offline metric at the operating point, an online experiment, and a guardrail on genuine sellers.</li></ol>
<p>Candidates who start with "I would use a CNN on the images" have answered question six before asking the first five. The interviewer is grading the order.</p>''')}"""

s2 = f"""<p><strong>Airport security.</strong> Every passenger walks through a cheap metal detector. A few are sent to a slower, more thorough search. Very few are refused boarding. The lanes are sized to the number of officers, and the threshold for a second look is set so the queue keeps moving.</p>
<p><strong>A hospital emergency department.</strong> A triage nurse spends a minute on each arrival and assigns a band. Doctors' time goes where it changes outcomes most. That is not always the sickest patients: someone certain to need surgery goes straight to the surgical team without a long assessment.</p>
{table(["Idea", "Airport", "Emergency department", "Counterfeit system"], [
["Cheap check on everyone", "Metal detector", "Triage nurse", "Rules and a light model at publish"],
["Expensive check on a few", "Hand search", "Doctor's assessment", "Image model, human reviewer"],
["Capacity limit", "Officers on shift", "Doctors on shift", "Reviews a day, GPU budget"],
["Automatic action", "Refuse boarding", "Straight to surgery", "Block without review"],
["Labels", "Rarely learned", "Outcomes known later", "Reviewer decisions, buyer reports, returns"]])}
<p>What does the emergency department teach that the airport does not? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Scarce expert time is best spent where the decision is uncertain and the stakes are high, not on the cases the cheap check is already sure about.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Passengers do not adapt.</strong> Counterfeiters do. Block one pattern and the next week's listings avoid it, so a fraud model decays faster than most.</li>
<li><strong>Triage is labelled by outcomes.</strong> A listing that was allowed and never reported is not known to be genuine: the labels come mostly from what was reviewed.</li>
<li><strong>Both have fixed queues.</strong> Listing volume spikes in sale seasons, and the threshold that fit the capacity in March overflows it in October.</li></ul>
{tests([("Why should reviewer time not go first to the listings the model is surest about?", "<p>Those can be blocked automatically at little cost, because the model is almost always right about them. A review there changes few decisions. Reviews change most decisions in the uncertain middle.</p>", True)])}"""

s3 = f"""<div class="fx">1 clarify    decision, timing, cost of each error,
             capacity, scale, latency
2 metrics    offline: precision and recall at the operating point
             online: counterfeits reaching buyers
             business: loss a day · guardrail: genuine blocked
3 data       label sources, their delays, and what never
             gets a label
4 features   text, images, price against the category,
             seller history, network signals
5 model      baseline first (rules, logistic regression),
             then boosting, then image and text in a cascade
6 serving    at publish within the latency budget, or after;
             cheap model on all, expensive on the uncertain
7 iterate    shadow mode, experiment, monitoring, retraining

for each listing:
  allow    cost  p × C_miss
  block    cost  (1 − p) × C_block
  review   cost  C_review, while capacity lasts</div>
<ul>
<li><strong>Operating point.</strong> The threshold where the system actually acts. A model's AUC is a summary over all thresholds; the business lives at one or two of them, set by costs and capacity, as in <a href="#b4-precision-recall">precision, recall and the threshold</a>.</li>
<li><strong>Cascade.</strong> A cheap stage scores everything and passes only the uncertain or risky share to an expensive stage. Total cost and latency are dominated by the first stage.</li>
<li><strong>Capacity-constrained triage.</strong> With unlimited reviewers, review whenever it is cheaper than the best automatic action. With limited reviewers, spend them where they save the most money per review.</li>
<li><strong>Shadow mode.</strong> Run the new model alongside the old one and log what it would have done, before it acts. It catches broken features and threshold surprises without risk.</li>
<li><strong>Feedback loop.</strong> The model decides which listings get reviewed, and reviews become labels. Without a small random sample of unflagged listings, the training data stops covering what the model lets through: see <a href="#d3-feedback-loops">feedback loops and selective labels</a>.</li></ul>
{tests([("A missed counterfeit costs ₹2,000, a wrong block ₹300 and a review ₹40. Above what probability should a listing be blocked rather than allowed, if there were no reviewers?", "<p>Block when (1 − p) × 300 &lt; p × 2,000, so p &gt; 300 / 2,300 = <strong>13%</strong>. The threshold is far below 50% because a miss costs nearly seven times a wrong block.</p>")])}"""

s4 = f"""<h4>Worked: triage with 80,000 reviews a day</h4>
<p>The model sorts the day's listings into five bands. Reviewers are assumed to decide correctly. Costs: miss ₹2,000, wrong block ₹300, review ₹40.</p>
{BANDS}
<p><strong>Without capacity limits.</strong> Review beats allowing when p &gt; 40 / 2,000 = 2%, and blocking beats reviewing when p &gt; 1 − 40 / 300 = 87%. So: block the very high band, review high, medium and low, allow very low. That needs 2,90,000 reviews.</p>
<p><strong>With 80,000.</strong> Rank the bands by what a review saves over the best automatic action:</p>
<ul><li>Medium: the best automatic action is to block, at (1 − 0.2) × 300 = ₹240. A review saves ₹200.</li>
<li>High: block, ₹120. A review saves ₹80.</li>
<li>Low: allow, 0.05 × 2,000 = ₹100. A review saves ₹60.</li>
<li>Very high: block, ₹15. A review would cost more than it saves.</li></ul>
<p>So review all 60,000 medium listings and 20,000 of the high band, block the rest of the high band and all of the very high band, and allow the low and very low bands. Cost: <strong>₹634.6 lakh a day</strong>, against ₹1,567.6 lakh for allowing everything. Genuine listings blocked: <strong>5,000</strong>.</p>
<p>The intuitive plan, reviewing from the top band down, spends 50,000 reviews on listings the model was already sure about. It costs <strong>₹691.6 lakh</strong> and blocks <strong>24,000</strong> genuine listings. Reviewers belong in the uncertain middle.</p>
<h4>Half-worked: where the remaining loss lives</h4>
<p>Of the ₹634.6 lakh, how much comes from the low and very low bands, which are allowed? What does that say about where to invest next?</p>
{reveal("<p>Low: 2,00,000 × 0.05 × 2,000 = ₹200 lakh. Very low: 96,90,000 × 0.002 × 2,000 = ₹387.6 lakh. Together <strong>₹587.6 lakh, 93% of the loss</strong>. More reviewers barely help: 1,50,000 reviews a day cut the cost only to ₹590.6 lakh. The money is in the 29,380 counterfeits the model scores as safe. The next investment is a better model for the bottom bands: image similarity to known brand products, price far below the category, new sellers listing many luxury items.</p>")}
<h4>Bare: sizing the image model</h4>
<p>Each listing has five images. An image model on one GPU handles 400 images a second. Traffic peaks at three times the daily average. How many GPUs to score every image at publish? And if a light model first passes only 20% of listings to the image model?</p>
{reveal("<p>50,000,000 images a day is 579 a second on average and <strong>1,736 at peak</strong>: 4.3 GPUs, so 5, plus one spare for failures, <strong>6</strong>. With the cascade, peak load is 347 images a second: 1 GPU plus a spare, <strong>2</strong>. The cascade cuts serving cost by two thirds, and the light model must be checked for counterfeits it waves through, because the image model never sees them.</p>")}
<h4>Predict, then play</h4>
<p>Cut review capacity from 80,000 to 50,000 a day. Predict what happens to the daily cost and to the number of genuine listings blocked.</p>
{reveal("<p>Cost rises only from ₹634.6 to <strong>₹670.6 lakh</strong>, but genuine listings blocked rise from 5,000 to <strong>21,000</strong>: the medium listings no longer reviewed are blocked, because blocking a 20% band is cheaper than letting it through. The money metric barely moves while the guardrail quadruples, which is why the design needs both.</p>")}
<div class="lab" data-lab="triage"></div>
<pre class="code">bands = [(.95, 20_000), (.60, 30_000), (.20, 60_000), (.05, 200_000), (.002, 9_690_000)]
MISS, BLOCK, REVIEW, CAP = 2000, 300, 40, 80_000

auto = lambda p: min(p * MISS, (1 - p) * BLOCK)            # best action without a reviewer
order = sorted(bands, key=lambda b: REVIEW - auto(b[0]))   # biggest saving per review first
cost, left = 0, CAP
for p, n in order:
    r = min(n, left) if auto(p) > REVIEW else 0
    left -= r
    cost += r * REVIEW + (n - r) * auto(p)
cost / 1e5                                                 # 634.6 lakh a day</pre>
{tests([("Why does the very high band get no reviews even when capacity is plentiful?", "<p>Blocking it costs (1 − 0.95) × 300 = ₹15 a listing, less than the ₹40 review. The model is right often enough that a review cannot pay for itself.</p>", True),
("The worked plan assumes reviewers are always right. Reviewers miss 10% of counterfeits. What changes?", "<p>A review now costs ₹40 plus 10% of the counterfeits slipping through, so it saves less in every band. Bands near the edges lose their reviews first, and measuring reviewer accuracy with audits becomes part of the design.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["Labels describe all listings", "Only flagged listings get reviewed, so the model never learns about the counterfeits it lets through", "Review a small random sample of allowed listings every day"],
["Counterfeiters stand still", "They change wording, crop logos, switch accounts", "Recall on the random sample falls month by month"],
["Costs are known and fixed", "A brand-owner complaint or a news story makes a miss far more expensive", "Write the costs down with an owner and revisit them"],
["Capacity is fixed", "Sale-season volume doubles listings while reviewers stay the same", "Set thresholds from capacity daily, not once"],
["Offline metrics predict online results", "Training data came from the old model's flags, a different population", "Shadow mode, then an experiment with buyer-side outcomes"],
["The cheap stage misses little", "Counterfeits that look ordinary to the light model never reach the image model", "Measure the cascade's end-to-end recall, not each stage's"]])}
{tests([("Recall on reviewed listings is steady at 85%, but buyer reports of counterfeits are rising. Explain.", "<p>Recall is measured only on what the model sent for review. Counterfeits it scores low are never reviewed, so their rise is invisible to the metric. A random audit of allowed listings would show it.</p>")])}"""

s6 = f"""{table(["Design choice", "Pick it when", "Cost"], [
["Rules only", "Day one, known patterns, need for explanations", "Brittle; easy to evade"],
["Gradient boosting on tabular features", "Seller history, price, category signals", "Weak on images and free text"],
["Image and text models", "Visual copies of branded goods", "GPU cost; needs a cascade"],
["Synchronous scoring at publish", "Bad listings must never be seen", "Latency budget limits model size"],
["Asynchronous scoring after publish", "A short exposure is acceptable", "Some buyers see the listing first"],
["Human review", "Uncertain, high-stakes cases", "Capacity and reviewer accuracy"],
["Graph features", "Rings of related accounts", "Engineering effort; leakage between training and test"]])}
{tests([("A counterfeit appearing for five minutes before removal is acceptable to the business. Which serving row, and what does it buy?", "<p>Asynchronous scoring. It frees the latency budget, so the image model and seller-network features can run on every listing, and allows batching on GPUs.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Counterfeit listings.</strong> Review queue limited to 80,000 a day.</p>
<p><strong>Payment fraud.</strong> Manual checks limited by an operations team.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Search ranking.</strong> Retrieve a thousand candidates, rank the top hundred carefully.</p>
<p><strong>Content moderation for an LLM feature.</strong> A cheap classifier, then a larger model on borderline outputs.</p></div></div>
{reveal('''<p><strong>Pair 1 is capacity-constrained triage.</strong> Costs set the thresholds; capacity decides where human attention goes; reviewed cases become biased labels.</p>
<p><strong>Pair 2 is a cascade.</strong> A cheap stage on everything and an expensive one on a small share. In search the cheap stage is <a href="#b9-retrieval-ranking">retrieval</a>; in moderation it is a small classifier. In both, the end-to-end recall is capped by the first stage.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Presenting the model as the system. A design that ends at "train a classifier with 0.97 AUC" has said nothing about thresholds, capacity, latency, labels or monitoring, which is where these systems succeed or fail. A widely cited paper from Google argues that the model code is a small fraction of a real ML system, and that most of the risk lives in the data dependencies and glue around it. {ref(1)}</p>
{tests([("An interviewer asks for your model's AUC. What do you say after the number?", "<p>The precision and recall at the operating point, how that point was chosen from costs and capacity, and how the number was measured given that labels come from reviews.</p>")])}"""

s8 = f"""<ul>
<li><strong>Spend the first five minutes on the decision, the costs and the capacity.</strong> Write them on the board.</li>
<li><strong>Start with a baseline</strong> you could ship in a week, then say what would justify each step up. Google's guidance puts a simple heuristic or model in production before machine learning gets clever. {ref(2)}</li>
<li><strong>Set thresholds from costs and capacity</strong>, and recompute them when either changes.</li>
<li><strong>Audit a random sample</strong> of what the system allows. It is the only unbiased recall.</li>
<li><strong>Launch in shadow mode, then experiment</strong> with buyer-side outcomes as the primary metric and blocked genuine sellers as the guardrail.</li>
<li><strong>Plan the decay.</strong> Retraining cadence, drift alerts and a playbook for a new fraud pattern: see <a href="#d3-monitoring-drift">monitoring and drift</a>.</li></ul>
{tests([("Name the one number you would put on the team's weekly dashboard to show the system is working, and why not precision.", "<p>Counterfeits reaching buyers per million orders, estimated from audits and buyer reports. Precision can rise while more counterfeits get through, if the model simply flags less.</p>")])}"""

s9 = f"""<ul>
<li><strong>Block automatically or always review?</strong> One view: an automated block is a judgment about a seller's livelihood and should have a human in the loop. The other: at millions a day, insisting on review means most listings get no check at all. Appeals and audit trails are the usual compromise.</li>
<li><strong>Explainable or accurate?</strong> Rules and simple models are easy to explain to sellers and regulators. Deep models catch more. Many teams use the deep model to rank and show reviewers the evidence, not the score.</li>
<li><strong>Build or buy?</strong> Vendors bring cross-company fraud signals; in-house teams know the marketplace's own patterns. The answer often changes with scale.</li>
<li><strong>How much to tell sellers?</strong> Specific reasons help honest sellers fix listings and teach counterfeiters how to evade.</li></ul>
{tests([("Give the strongest case for always having a human confirm a block.", "<p>A wrong block can cost a small seller their income and is hard to reverse in their customers' eyes. Human confirmation catches model failures that look confident, and supports a fair appeal. The cost is capacity, so it fits when blocks are rare.</p>")])}"""

rungs = [
 {"ask": "Walk me through how you structure any ML system design answer.", "follow": ["Where do most candidates lose time?", "What do you write down before choosing a model?"],
  "weak": "<p>Starts with the model architecture.</p>",
  "strong": "<p>Clarify the decision, timing, error costs, capacity, scale and latency. Then metrics at the operating point and a guardrail; data and label sources with their biases; features; a baseline model and what justifies the next one; serving and a cascade; then shadow mode, experiment, monitoring and retraining. Says which of these the interviewer seems to care about and spends the time there.</p>"},
 {"ask": "Why would you review medium-risk listings before high-risk ones when reviewers are scarce?", "follow": ["When would you review the high band first?", "What happens to the medium band when there are no reviewers?"],
  "model": "<p>a review is worth what it saves over the best automatic action. High-risk listings can be blocked cheaply because the model is usually right; medium-risk ones are expensive whichever way you act automatically. With a miss at ₹2,000, a wrong block at ₹300 and a review at ₹40, a medium review saves ₹200 and a high one ₹80.</p>",
  "weak": "<p>\"Highest risk first\" without reasoning about the automatic alternative.</p>",
  "strong": "<p><b>Must have.</b> Compares each band's review cost with its best automatic action.</p><p><b>Strong signal.</b> Notes the effect on genuine sellers blocked, and that the answer flips if blocks become much more expensive.</p>"},
 {"ask": "Your counterfeit model's recall on reviewed listings is steady, but complaints from buyers are rising. What is happening?", "follow": ["How would you measure true recall?", "How big must the audit sample be?"],
  "weak": "<p>\"Retrain the model.\"</p>",
  "strong": "<p>Selective labels: recall is measured only where the model sent listings, so new counterfeits it scores low never appear. Start a daily random audit of allowed listings to estimate true recall and find the new pattern, then add those labels to training. Size the audit from the rare rate: finding a 0.2% pattern needs thousands of reviews.</p>"},
 {"ask": "Design the serving path for scoring 10 million listings a day at publish within 200 milliseconds.", "follow": ["Images are the best signal but the model takes 80 ms. Where does it go?", "What happens when the image service is down?"],
  "weak": "<p>One large model behind an API.</p>",
  "strong": "<p>A cascade: rules and a boosted model on precomputed seller features synchronously, well inside the budget; the image model only on the uncertain share, either synchronously within the remaining budget or asynchronously with the listing held as pending. Sizing from peak load, not average. A fallback that fails safe by holding risky listings rather than allowing everything. Feature freshness from a feature store with point-in-time training data.</p>", "roles": ["mle"]},
 {"ask": "Operations wants to cut review capacity from 80,000 to 50,000 a day because the model is now very accurate. What do you tell them?", "follow": ["They point to the cost metric, which barely moves.", "What would make you agree?"],
  "weak": "<p>Agrees because the cost metric is flat, or refuses without numbers.</p>",
  "strong": "<p>Runs the triage at the lower capacity: in the worked case cost rises 6% but genuine listings blocked quadruple, from 5,000 to 21,000 a day, which shows up later as seller churn and support load. Presents both numbers, proposes the cut with a guardrail on wrongful blocks and an appeal-rate threshold, or invests the savings in the bottom bands where 93% of the loss lives.</p>", "roles": ["ic", "mle", "lead"]},
]

page(S, "D3", "ML system design, end to end",
     "How to answer \"design a system that…\" in an interview: the questions to ask before choosing a model, how costs and review capacity set the thresholds, how a cascade keeps serving cheap, and why the labels you get are biased by the system itself.",
     "ml system design interview counterfeit fraud trust and safety triage review capacity cascade latency throughput gpu sizing threshold cost matrix shadow mode feedback loop selective labels audit serving",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "An ML system is designed from the decision outward: the costs of each error and the review capacity set the thresholds, a cascade keeps serving cheap, scarce reviewers go to the uncertain middle, and a random audit is the only honest measure of what the system lets through.",
     ["Start with the decision, error costs, capacity and latency", "Thresholds come from costs; capacity decides where humans look", "Review the uncertain middle, not the cases the model is sure of", "A cascade: cheap stage on everything, expensive stage on a few", "Reviewed cases are biased labels, so audit a random sample"],
     [("b4-precision-recall", "Precision, recall and the threshold"), ("d3-serving-deployment", "Serving, rollout and rollback"), ("d2-feature-pipelines", "Feature pipelines and point-in-time correctness")],
     [("d3-feedback-loops", "Feedback loops and selective labels"), ("d3-monitoring-drift", "Monitoring, drift and retraining"), ("e3-fairness", "Fairness and responsible models")],
     sources=[("Sculley et al., \"Hidden Technical Debt in Machine Learning Systems\", NeurIPS 2015", "https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/"),
              ("Zinkevich, \"Rules of Machine Learning: Best Practices for ML Engineering\", Google", "https://developers.google.com/machine-learning/guides/rules-of-ml")],
     sec_roles={11: ["lead", "ic", "mle"], 9: ["lead", "ic", "mle"]})
