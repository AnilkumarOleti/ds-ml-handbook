import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "e3-fairness"
R = ["lead", "ic", "mle"]

s1 = f"""<div class="problem"><p>A counterfeit model is applied to two groups of sellers. Among <strong>new sellers</strong>, 4% list counterfeits. Among <strong>established sellers</strong>, 1% do. The model is equally good in both groups: it catches <strong>80%</strong> of counterfeit sellers and wrongly flags <strong>5%</strong> of genuine ones.</p>
<p>Per 10,000 sellers in each group, what share of flagged sellers are actually counterfeit? An advocacy group for new sellers says the model is biased against them. Another says it is biased against established sellers. Who is right?</p></div>
{attempt(S, 1)}{reveal('''<p><strong>New sellers:</strong> 400 counterfeit, 320 caught. 9,600 genuine, 480 wrongly flagged. Precision 320 / 800 = <strong>40%</strong>, and 8% of the group is flagged.</p>
<p><strong>Established sellers:</strong> 100 counterfeit, 80 caught. 9,900 genuine, 495 wrongly flagged. Precision 80 / 575 = <strong>13.9%</strong>, and 5.75% of the group is flagged.</p>
<p>Both groups can point to a real disparity. New sellers are flagged more often: 8% against 5.75%. Established sellers who are flagged are far more likely to be innocent: 86% of their flags are wrong, against 60%. The error rates, 80% caught and 5% wrongly flagged, are identical.</p>
<p>That is not a flaw of this model. When base rates differ, no imperfect model can have equal error rates and equal precision in both groups at once. Choosing which equality to keep is a decision about values, and it should be made deliberately and written down.</p>''')}"""

s2 = f"""<p><strong>The airport's secondary screening.</strong> Officers pick passengers for a second search. If one route carries more contraband, a rule tuned to catch the same share of smugglers on every route will stop more innocent travellers in absolute numbers on some routes, or search each route's travellers at different rates. Equal treatment can be defined by who gets searched, or by who gets searched in error, and the two disagree.</p>
<p><strong>Grading on a curve.</strong> Two classes take different exams. One teacher gives every class the same pass mark. Another passes the same share of each class. Each says the other is unfair, and each is applying a reasonable idea of fairness.</p>
{table(["Idea", "Airport", "Exam", "Counterfeit model"], [
["Groups", "Routes", "Classes", "New and established sellers"],
["Same rule for everyone", "One profile for all routes", "One pass mark", "One threshold"],
["Same outcome rate", "Search the same share of each route", "Pass the same share", "Flag the same share: demographic parity"],
["Same errors among the innocent", "Same share of innocent travellers searched", "Same share of able students failed", "Equal false positive rates"],
["Same reliability of a flag", "A search finds contraband equally often", "A pass means the same everywhere", "Equal precision: predictive parity"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>When groups differ in how often the thing being judged occurs, every reasonable definition of equal treatment pulls in a different direction, so fairness is a choice among them rather than a property to switch on.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Exam marks are the outcome itself.</strong> A model's score is a prediction of an outcome that is often measured with bias, such as flags from past reviews.</li>
<li><strong>Routes are given.</strong> Seller groups can be defined many ways, and a model can be fair across one split and unfair across another.</li>
<li><strong>Both are one-off decisions.</strong> A model's decisions change the data it is next trained on.</li></ul>
{tests([("Why is equal precision across groups impossible here without changing the error rates?", "<p>Precision depends on the base rate, as in Bayes' rule. With the same catch rate and false positive rate, the group with the lower base rate must have lower precision.</p>", True)])}"""

s3 = f"""<div class="fx">for each group g, with prevalence πg:
  selection rate   P(flag | g)        equal → demographic parity
  true pos. rate   P(flag | bad, g)   equal → equal opportunity
  false pos. rate  P(flag | good, g)  with TPR → equalised odds
  precision        P(bad | flag, g)   equal → predictive parity

precision = TPR·π / (TPR·π + FPR·(1 − π))
π differs and the model is imperfect →
  equalised odds and predictive parity cannot both hold

four-fifths rule   lowest selection rate ÷ highest < 0.8
                   → evidence of adverse impact</div>
<ul>
<li><strong>Demographic parity.</strong> The same share of each group receives the decision. Simple to explain; ignores differences in the outcome itself.</li>
<li><strong>Equal opportunity and equalised odds.</strong> Equal true positive rates, and also equal false positive rates. Focuses on errors made against each group. {ref(3)}</li>
<li><strong>Predictive parity.</strong> A flag, or a given score, means the same probability in every group.</li>
<li><strong>The impossibility.</strong> With different base rates, a classifier that is not perfect cannot satisfy calibration within groups and equal error rates at once. {ref(1)} {ref(2)}</li>
<li><strong>Proxies.</strong> Removing the group attribute does not remove the disparity: pin code, device, account age or language can stand in for it.</li>
<li><strong>Adverse impact.</strong> In US employment practice, a selection rate for one group below four fifths of the highest group's is generally treated as evidence of adverse impact. {ref(4)}</li></ul>
{tests([("Removing seller tenure from the model's features. Does that make it fair to new sellers?", "<p>Not necessarily. Other features such as review count, listing history and account age carry the same information. The disparity in outcomes can remain, now harder to see and to correct.</p>"),
("Approval rates are 60% for one group of applicants and 42% for another. What does the four-fifths rule say?", "<p>42 / 60 = 0.70, below 0.8, which is generally treated as evidence of adverse impact and calls for a review of the decision rule.</p>")])}"""

s4 = f"""<h4>Worked: equalising precision</h4>
<p>Suppose the policy is that a flag must mean the same thing in both groups: 40% precision, as for new sellers. Keep the catch rate at 80% among established sellers. What false positive rate do they need?</p>
<p>0.40 = 80 / (80 + FPR × 9,900), so FPR × 9,900 = 120 and <strong>FPR = 1.2%</strong>. Genuine new sellers are wrongly flagged at 5%, genuine established sellers at 1.2%. Equal precision has made a genuine new seller <strong>four times</strong> as likely to be wrongly flagged.</p>
<p>In practice the error rates are not free to set: a model trades them along its ROC curve. With scores that separate the classes by 2.5 standard deviations, a single threshold gives 80% recall and a false positive rate just under 5% in both groups, and precision of 41% and 14%. Raising the established sellers' threshold until their precision also reaches 41% cuts their recall to <strong>53%</strong>: a quarter of the counterfeits from established sellers, which the shared threshold would have caught, now go through.</p>
<h4>Half-worked: who bears the cost</h4>
<p>Each wrong flag freezes a seller's payouts for a week. Using section 1's numbers, how many genuine sellers per 10,000 in each group bear that cost under one threshold? And under the equal-precision policy?</p>
{reveal("<p>One threshold: 480 genuine new sellers and 495 genuine established sellers, nearly equal in number, 5% of each group's genuine sellers. Equal precision: still 480 new, but only 120 established. The policy moves the burden of mistakes onto the group with more counterfeits, including its honest members, which is the core complaint about such policies.</p>")}
<h4>Bare: a fairness check before launch</h4>
<p>Write the five checks you would run before launching a seller-risk model, with the number each produces.</p>
{reveal("<ol><li>Selection rate by group, and the four-fifths ratio.</li><li>True and false positive rates by group, with intervals, since small groups give noisy rates.</li><li>Calibration by group: predicted against actual rate in each score band.</li><li>The same three for groups defined by likely proxies, such as region or language.</li><li>Who bears the cost: wrongly flagged honest sellers per 10,000 in each group, and the appeal and reversal rate.</li></ol><p>Then write down which disparity the business has chosen to accept, and why.</p>")}
<h4>Predict, then play</h4>
<p>Start from one shared threshold. Lower the new sellers' base rate from 4% until it matches established sellers at 1%. Predict what happens to the precision gap.</p>
{reveal("<p>It closes completely. With equal base rates and an equally good model, one threshold gives equal error rates and equal precision together. The conflict between definitions exists only because base rates differ.</p>")}
<div class="lab" data-lab="fairness"></div>
<pre class="code">def by_group(base, tpr, fpr, n=10_000):
    tp, fp = tpr * base * n, fpr * (1 - base) * n
    return {{"precision": tp / (tp + fp), "flagged": (tp + fp) / n}}

by_group(0.04, 0.80, 0.05)   # precision 0.40, flagged 8.0%
by_group(0.01, 0.80, 0.05)   # precision 0.139, flagged 5.75%
0.8 * 0.01 * (1 / 0.4 - 1) / 0.99   # FPR for 40% precision: 0.0121</pre>
{tests([("Why does equalising precision fall hardest on honest members of the higher-risk group?", "<p>Their group's flags are already more often right, so to match the other group's reliability the other group's threshold rises, and theirs stays. Their false positive rate is now the higher one.</p>", True)])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The labels are unbiased", "Past reviews checked new sellers more often, so more of their counterfeits were found", "Compare label rates from random audits with rates from flagged reviews"],
["Groups are known", "The attribute is not collected, or is collected only for some", "Estimate it carefully, or audit on proxies, with privacy review"],
["Group sizes are large", "A small group's rates have wide intervals", "Report intervals; pool over time"],
["The decision is one-off", "Flagged sellers leave, so the next year's data has fewer of them", "Track group composition over time"],
["A fair model gives a fair outcome", "The action after the flag differs, such as faster appeals for some", "Measure outcomes after the decision, not only the flag"],
["One split is enough", "Fair by tenure, unfair by region", "Check intersections of attributes"]])}
{tests([("New sellers have a higher counterfeit rate in the training labels. Name one way that could be an artefact.", "<p>Reviewers checked new sellers more often, so more of their counterfeits were found. A random audit would show whether the true rates differ that much.</p>")])}"""

s6 = f"""{table(["Approach", "What it does", "Pick it when", "Cost"], [
["Change nothing, document", "Report rates by group and the chosen trade-off", "Disparities are small or justified", "Must be revisited"],
["Group-specific thresholds", "Equalise a chosen rate after training", "A clear policy target", "Explicit use of the attribute, which may be restricted"],
["Constrained training", "Penalise disparity during fitting", "A model is being rebuilt anyway", "Some accuracy; harder to explain"],
["Better data", "Audit labels and fix measurement bias", "Labels are suspect", "Time and review capacity"],
["Change the action", "Hold instead of block; faster appeals", "Errors are costly to individuals", "Operational cost"],
["Privacy techniques", "Limit what is learned about individuals", "Sensitive data, regulators", "Noise or reduced detail"]])}
{tests([("Which approach changes the cost of an error rather than the number of errors?", "<p>Changing the action: holding a listing for review instead of blocking a seller, or reversing a wrong flag within hours, makes each mistake cheaper for the person who suffers it.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Seller risk scores</strong> across new and established sellers.</p>
<p><strong>Credit limits for buy-now-pay-later</strong> across regions.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Search ranking</strong> that favours sellers with more reviews.</p>
<p><strong>Fraud labels</strong> that come only from reviewed cases.</p></div></div>
{reveal('''<p><strong>Pair 1 is the base-rate conflict.</strong> Groups differ in how often the outcome occurs, so the choice between equal error rates and equal precision has to be made explicitly, with the cost to honest members of each group in view.</p>
<p><strong>Pair 2 is a feedback loop.</strong> Sellers with more reviews rank higher, sell more and gain more reviews; reviewed fraud cases shape the next model. New entrants are disadvantaged by the system's history, not their quality. See <a href="#d3-feedback-loops">feedback loops and selective labels</a>.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>"The model does not use the protected attribute, so it is fair." Removing the attribute neither prevents disparities, because proxies carry the information, nor lets you measure them, because the attribute is needed to check. Fairness is assessed on outcomes by group, which needs the group.</p>
{tests([("How would you give new sellers a fair chance in search ranking without hiding quality signals?", "<p>Reserve a small share of exposure for new listings and learn their quality from it, an exploration budget as in <a href='#a4-bandits'>bandits</a>, and shrink sparse ratings towards a prior rather than ranking them as zero.</p>")])}"""

s8 = f"""<ul>
<li><strong>Choose the fairness definition before training</strong>, with the people accountable for the decision, and write it down.</li>
<li><strong>Report error rates and precision by group</strong> with intervals, in every model review.</li>
<li><strong>Audit labels with random samples</strong>, because biased labels make every metric misleading.</li>
<li><strong>Count the people who bear the errors</strong>, not only the rates.</li>
<li><strong>Make errors cheaper</strong>: appeals, reversibility and human review for consequential actions.</li>
<li><strong>Keep the group attribute for measurement</strong>, under access controls, even when the model does not use it.</li></ul>
{tests([("Why keep the protected attribute in the data if the model must not use it?", "<p>Without it you cannot measure whether outcomes differ by group, and proxies may be producing disparities that you would never see.</p>")])}"""

s9 = f"""<ul>
<li><strong>Which definition?</strong> Error-rate parity protects individuals from being wrongly judged because of their group. Predictive parity keeps a score meaning the same for everyone. Demographic parity addresses unequal starting points. Law, context and the cost of each error decide, and reasonable people disagree.</li>
<li><strong>Group-specific thresholds.</strong> They achieve a chosen parity directly, and are criticised as treating individuals differently by group. In some domains they are restricted by law.</li>
<li><strong>Fairness against accuracy.</strong> Some argue the trade-off is overstated, because label bias makes the "accurate" model wrong too. Others point to measurable losses from constraints.</li>
<li><strong>Who decides?</strong> Data scientists can compute the trade-offs. The choice belongs with the people accountable for the decision, informed by those affected.</li></ul>
{tests([("Make the case for predictive parity over equal error rates for a counterfeit model.", "<p>Reviewers and sellers should be able to trust that a flag means the same risk for everyone; otherwise reviewers learn to discount flags on one group, and appeals are judged inconsistently. Equal precision makes the score's meaning group-blind.</p>")])}"""

rungs = [
 {"ask": "Name three definitions of group fairness for a classifier and say what each equalises.", "follow": ["Which can hold together?", "Which needs the outcome to be known?"],
  "weak": "<p>\"Fairness means not using protected attributes.\"</p>",
  "strong": "<p>Demographic parity: selection rates. Equalised odds: true and false positive rates. Predictive parity: precision, or calibration within groups. With different base rates and an imperfect model, equalised odds and predictive parity cannot both hold. Error-rate definitions need outcome labels, which may themselves be biased.</p>"},
 {"ask": "A model has the same recall and false positive rate for two groups, yet flags in one group are right far more often. Explain.", "follow": ["Which group's flags are more reliable?", "What would it take to equalise precision?"],
  "model": "<p>precision depends on the base rate: TPR·π / (TPR·π + FPR·(1 − π)). With 80% recall and 5% false positives, a 4% base rate gives 40% precision and a 1% base rate gives 13.9%. Equalising precision at 40% needs a 1.2% false positive rate in the low-base-rate group, which breaks equal error rates.</p>",
  "weak": "<p>\"The model is biased.\"</p>",
  "strong": "<p><b>Must have.</b> Ties precision to base rate through Bayes' rule.</p><p><b>Strong signal.</b> States the impossibility result and quantifies who bears the errors under each choice.</p>"},
 {"ask": "Your team removed the protected attribute from the features. A regulator still finds a disparity. How?", "follow": ["How would you find the proxies?", "Should you put the attribute back?"],
  "weak": "<p>\"Remove more features.\"</p>",
  "strong": "<p>Proxies: features correlated with the attribute carry its information. Find them by predicting the attribute from the other features. Removing proxies one by one loses accuracy without guaranteeing parity. Measure outcomes by group, decide the target definition, and then adjust thresholds or train with a constraint; keep the attribute for measurement under access control.</p>"},
 {"ask": "Design a fairness review for every model that affects sellers' income.", "follow": ["Groups are small. What do you report?", "Who signs off?"],
  "weak": "<p>A one-off bias check before launch.</p>",
  "strong": "<p>Before launch: selection rate, error rates and calibration by group and by likely proxies, with intervals, plus the number of honest sellers wrongly affected; a written choice of fairness definition signed by the accountable business owner; appeal and reversal paths. After launch: the same metrics monthly, random-audit labels to check for label bias, and a trigger to review when ratios cross agreed limits.</p>", "roles": ["lead", "mle"]},
 {"ask": "Equalising error rates would let more counterfeits through and cost ₹2 crore a year. The policy team wants it anyway. What do you do?", "follow": ["The business head says that cost is unacceptable.", "Is there a third option?"],
  "weak": "<p>Implements whichever side is more senior, without stating the trade-off.</p>",
  "strong": "<p>Lays out the options with their costs in money and in honest sellers wrongly flagged per group, for the accountable decision-maker. Looks for options that change the cost of errors instead of their number: hold for review instead of block, faster appeals, better labels from audits. Records the decision and its reasons, and schedules a review.</p>", "roles": ["lead"]},
]

page(S, "E3", "Fairness and responsible models",
     "Why a model with equal error rates across groups can still flag one group's honest members far more often, why no model can satisfy every fairness definition when base rates differ, and how to choose, measure and document the trade-off.",
     "fairness bias responsible ai demographic parity equal opportunity equalised odds predictive parity calibration impossibility base rate proxy four-fifths rule adverse impact protected attribute audit appeals privacy",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "When groups differ in base rates, an imperfect model cannot equalise both its error rates and the meaning of its flags, so fairness is a documented choice among definitions, measured on outcomes by group with the attribute kept for auditing, and made cheaper to get wrong through appeals and reversible actions.",
     ["Different fairness definitions equalise different rates", "Base rates make some definitions incompatible", "Removing the attribute does not remove the disparity", "Count who bears the errors", "Choose and document the trade-off with the accountable owner"],
     [("a1-bayes-base-rates", "Bayes' rule and base rates"), ("b4-precision-recall", "Precision, recall and the threshold"), ("b4-calibration", "Calibration")],
     [("d3-feedback-loops", "Feedback loops and selective labels"), ("d3-system-design", "ML system design, end to end")],
     sources=[("Chouldechova, \"Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments\", Big Data, 2017", "https://doi.org/10.1089/big.2016.0047"),
              ("Kleinberg, Mullainathan and Raghavan, \"Inherent Trade-Offs in the Fair Determination of Risk Scores\", 2016", "https://arxiv.org/abs/1609.05807"),
              ("Hardt, Price and Srebro, \"Equality of Opportunity in Supervised Learning\", NeurIPS 2016", "https://arxiv.org/abs/1610.02413"),
              ("Uniform Guidelines on Employee Selection Procedures, 29 CFR 1607.4(D)", "https://www.law.cornell.edu/cfr/text/29/1607.4")],
     sec_roles={10: R})
