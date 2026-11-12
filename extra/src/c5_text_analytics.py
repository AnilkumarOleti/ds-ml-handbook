import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c5-text-analytics"
R = ["lead", "ic", "mle"]

s1 = f"""<div class="problem"><p>An LLM tags 20,000 buyer feedback comments a month against a fixed list of 12 themes. It tags <strong>18%</strong> as \"delivery problem\" and <strong>4.7%</strong> as \"counterfeit concern\". Leadership wants both on the monthly dashboard, and plans a trust and safety push on counterfeits.</p>
<p>Two analysts each hand-labelled the same 200 comments for delivery: they agreed on 170, and each marked 65 as delivery. On a hand-labelled set, the model catches <strong>90%</strong> of true cases of any theme and wrongly tags <strong>3%</strong> of comments that do not have it.</p>
<p>What are the true shares? What would you put on the dashboard?</p></div>
{attempt(S, 1)}{reveal(f'''<p><strong>The humans first.</strong> 85% raw agreement sounds high, but with 65 of 200 marked by each, chance alone gives 56%. Cohen's kappa = (0.85 − 0.56) ÷ (1 − 0.56) = <strong>0.66</strong>: substantial, not perfect. The theme's boundary is fuzzy, and the model cannot be judged more precisely than people agree.</p>
<p><strong>Delivery.</strong> Observed 18% = 0.90 × true + 0.03 × (1 − true), so true = (0.18 − 0.03) ÷ 0.87 = <strong>17.2%</strong>. Close to the raw tag.</p>
<p><strong>Counterfeits.</strong> The same error rates give a true share of (0.047 − 0.03) ÷ 0.87 = <strong>about 2%</strong>. Over half the counterfeit tags are false alarms, because a 3% false-positive rate applied to the 98% of comments without the theme swamps the real cases.</p>
<p>Dashboard: corrected shares with intervals, the error rates and the date they were measured, a fixed model and prompt version, and a monthly re-check on a fresh hand-labelled sample. Read the counterfeit comments before planning a push. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>Sorting a mailbag.</strong> A charity reads thousands of letters and sorts them into piles: complaints, thanks, requests. Two volunteers will not always agree on a borderline letter, and a fast but careless sorter will drop a few thanks into every pile, which matters most for the smallest pile.</p>
<p><strong>A spam filter.</strong> It is right 97% of the time on normal mail. If only 2% of your mail is spam, most of what it flags is not spam.</p>
{table(["Idea", "Mailbag", "Spam filter", "Text tagging"], [
["The items", "Letters", "Emails", "Comments, tickets, queries"],
["The categories", "Piles", "Spam or not", "Themes in a taxonomy"],
["The ceiling", "Volunteers disagree on borderline letters", "People disagree on what is spam", "Human agreement (kappa)"],
["The trap", "A careless sorter inflates small piles", "Low base rate, many false flags", "Rare themes over-counted"],
["The fix", "Check a sample of each pile", "Measure error rates; adjust", "Hand-label a sample; correct shares"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>An automatic sorter's counts mix real cases with its errors, and for rare categories the errors can outnumber the cases, so the counts must be checked against a hand-labelled sample.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Letters stay the same.</strong> Feedback changes with the product: a new delivery partner brings new words, and a model's error rates shift.</li>
<li><strong>A spam filter is trained for one task.</strong> An LLM with a prompt can be changed in a minute, and a small prompt change can move every count. Versions must be fixed.</li>
<li><strong>Piles are exclusive.</strong> A comment can raise several themes; multi-label tagging needs per-theme error rates.</li></ul>
{tests([("Why can a tagger with 97% specificity still be wrong about most of its tags for a rare theme?", "<p>Specificity applies to the many comments without the theme. 3% of 98% is 2.9% of all comments, more than the 2% that truly have it. See <a href='#a1-bayes-base-rates'>Bayes' rule and base rates</a>.</p>", True)])}"""

s3 = f"""<div class="fx">approaches
   keyword rules        transparent, brittle, miss paraphrases
   topic models         discover themes (LDA, BERTopic on embeddings)
                        unstable; topics need naming and merging
   supervised classifier labelled examples → model per theme
   LLM tagging          fixed taxonomy + instructions; zero- or few-shot

measuring quality
   hand-label a random sample (several hundred), two people if possible
   human agreement      Cohen's κ = (p_o − p_e) / (1 − p_e)
   model vs consensus   sensitivity, specificity, precision per theme

correcting shares
   observed = se·π + (1 − sp)(1 − π)
   π = (observed − (1 − sp)) / (se + sp − 1)

keep it stable: fix the model version, prompt and taxonomy;
re-check on a fresh sample every month</div>
<ul>
<li><strong>Discover, then measure.</strong> Topic models and embedding clusters are good for finding themes nobody listed. Tracking needs a fixed taxonomy and a tagger with measured errors. {ref(2)}</li>
<li><strong>LLM tagging</strong> often matches a trained classifier with no training data, and lets the taxonomy change quickly. The price is drift when prompts or models change.</li>
<li><strong>Human agreement is the ceiling.</strong> If two careful people agree at κ = 0.66, the theme is fuzzy; sharpen its definition before blaming the model.</li>
<li><strong>Prevalence needs correction</strong> for rare themes; per-comment decisions, such as routing a ticket, need precision and recall instead.</li>
<li><strong>Search queries</strong> are short and noisy: cluster them by embedding, look at zero-result and reformulated queries, and map clusters to catalogue gaps.</li></ul>
{tests([("Why compute kappa instead of raw agreement?", "<p>Raw agreement includes agreement by chance, which is high when one answer is common. Kappa measures agreement beyond chance, so a lazy rater who always says 'no' does not look good.</p>", True),
("A topic model produced three topics full of delivery words. Should you report three delivery themes?", "<p>Only if they mean different things to the business, such as late, damaged and lost. Otherwise merge them. Topic models split and merge themes by word statistics, not by what matters.</p>")])}"""

s4 = f"""<h4>Worked: Cohen's kappa</h4>
<p>Two analysts, 200 comments, delivery theme: both yes 50, both no 120, one each way 15 and 15.</p>
<ul><li>Observed agreement p_o = 170 ÷ 200 = 0.85.</li>
<li>Each said yes 65 times. Chance agreement p_e = (65/200)² + (135/200)² = 0.106 + 0.456 = 0.561.</li>
<li>κ = (0.85 − 0.561) ÷ (1 − 0.561) = <strong>0.66</strong>.</li></ul>
<p>Conventional labels call 0.61 to 0.80 \"substantial\". Compare the model with the two analysts' consensus in the same way; a model near 0.66 is at human level for this theme.</p>
<h4>Half-worked: correcting a share</h4>
<p>The model's sensitivity is 0.90 and specificity 0.97. It tags 18% as delivery and 4.7% as counterfeit. Correct both, and say how precise the error rates themselves are if they came from 300 hand-labelled comments with 54 true delivery cases.</p>
{reveal("<p>Delivery: (0.18 − 0.03) ÷ 0.87 = <strong>17.2%</strong>. Counterfeit: (0.047 − 0.03) ÷ 0.87 = <strong>2.0%</strong>; precision of counterfeit tags is only about 38%. With 54 true delivery cases, the sensitivity estimate has an interval of roughly ±8 points, and for a theme with ten cases in the sample, far wider. Rare themes need a larger, stratified validation sample, oversampling comments the model tagged.</p>")}
<h4>Bare: a trend that is not there</h4>
<p>Delivery complaints jump from 17.8% to 20.3% the month after an engineer \"improved\" the prompt. What do you check, and what do you change in the process?</p>
{reveal("<p>Whether the jump is the prompt. If the new prompt catches more delivery comments and flags a few more wrongly (say sensitivity 0.95, specificity 0.95), the same true 17% gives 20.3%: a 14% rise from the tagger alone. Re-tag last month with the new prompt and compare. In future, version prompts and models, run changes in parallel on a back-month, and re-measure error rates before switching the dashboard.</p>")}
<h4>Predict, then play</h4>
<p>With sensitivity 0.90 and specificity 0.97, predict the observed share and precision for a theme whose true share is 5%.</p>
{reveal("<p>Observed 0.90 × 0.05 + 0.03 × 0.95 = <strong>7.4%</strong>; precision 0.045 ÷ 0.074 = <strong>61%</strong>. The rarer the theme, the more the tagger inflates it and the more its tags mislead.</p>")}
<div class="lab" data-lab="tagging"></div>
<pre class="code">THEMES = ["delivery problem", "item not as described", "counterfeit concern", ...]
PROMPT_VERSION = "feedback-tagger-v3"                # fixed; changes go through validation

def tag(comment):
    # ask the model for zero or more labels from THEMES only, as JSON, with a short quote as evidence
    ...

from sklearn.metrics import cohen_kappa_score
cohen_kappa_score(human_a, human_b)                  # ceiling for the theme
corrected = (observed - (1 - spec)) / (sens + spec - 1)</pre>
{tests([("Why ask the model for a supporting quote with each tag?", "<p>It makes validation fast, since a reviewer sees why each tag was given, and it discourages tags with no basis in the text. Tags whose quote does not support them are easy to count as errors.</p>", True),
("Comments in Hindi and Telugu are 15% of volume. What changes in validation?", "<p>Measure error rates separately by language: models often perform worse on some languages, and a pooled estimate hides it. Hand-labellers must read those languages too.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The taxonomy is clear", "Themes overlap or are vague", "Low human kappa; disagreements cluster on certain themes"],
["Error rates are stable", "New products, words, languages, or model updates", "Monthly re-check on a fresh sample"],
["The sample represents the stream", "Validation drawn from one week or one language", "Stratify by time, language, channel"],
["Feedback represents users", "Only unhappy or very happy users write", "Compare with survey or behaviour; see qual-quant"],
["One label per comment", "Comments raise several issues", "Multi-label tagging with per-theme metrics"],
["Topic models find stable themes", "Rerun gives different topics", "Compare runs; fix a taxonomy for tracking"]])}
{tests([("Feedback volume about 'returns' doubled after the returns page was redesigned to include a feedback box. What is the trend telling you?", "<p>Mostly that more people were asked. Normalise by the number of people who saw a feedback prompt, or by orders, before calling it a rise in returns problems.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Keyword rules", "Does the text mention X?", "Narrow, well-worded themes; audits", "Misses paraphrases and other languages"],
["Topic model / embedding clusters", "What themes exist?", "Discovery", "Unstable; needs naming"],
["Supervised classifier", "Which theme, at scale and low cost", "Stable taxonomy with labelled data", "Needs labels; retraining"],
["LLM tagging", "Which theme, without training data", "Changing taxonomies; many languages", "Drift; cost; must be validated"],
["Sentiment scores", "How positive or negative", "Broad mood tracking", "Sarcasm; domain words"],
["Human reading", "What do they actually say?", "Always, on a sample", "Slow; but nothing replaces it"]])}
{tests([("A new theme, 'payment app outage', appears overnight. Which rows help most?", "<p>Embedding clusters or a topic model on the last few days to surface it, human reading to confirm it, then adding it to the LLM taxonomy with a quick validation.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Routing support tickets</strong> to the right queue.</p>
<p><strong>Flagging listings</strong> whose descriptions suggest prohibited items.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Tracking the share of feedback</strong> about delivery each month.</p>
<p><strong>Sizing search demand</strong> for a category the catalogue lacks.</p></div></div>
{reveal('''<p><strong>Pair 1 makes per-item decisions.</strong> Precision and recall at a chosen threshold matter, with a human review path for the costly mistakes; see <a href="#b4-precision-recall">precision, recall and the threshold</a>.</p>
<p><strong>Pair 2 estimates shares.</strong> Individual errors matter less than their balance: correct prevalence with measured error rates, and keep the tagger fixed so trends are real.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Counting raw LLM tags as facts. A dashboard shows theme shares to one decimal place from a tagger that was never validated, and a rare theme's rise drives a quarter's roadmap. Over half of those tags may be false alarms, and the rise may be a prompt change. Text analytics needs the same measurement discipline as any other instrument.</p>
{tests([("A theme's share doubled this month from 1% to 2%. What three things do you check?", "<p>Whether the tagger or prompt changed; what the corrected shares are given the false-positive rate; and what the comments actually say, by reading a sample of the new tags.</p>")])}"""

s8 = f"""<ul>
<li><strong>Write the taxonomy with definitions and examples</strong>, test it with two human labellers, and revise themes with low kappa.</li>
<li><strong>Validate on a random, stratified sample</strong> of a few hundred, oversampling rare themes; report per-theme error rates.</li>
<li><strong>Version everything</strong>: model, prompt, taxonomy. Run changes on past data before switching.</li>
<li><strong>Correct shares and give intervals</strong> on dashboards; show raw counts too.</li>
<li><strong>Re-validate monthly</strong>, and when products, languages or channels change.</li>
<li><strong>Keep humans reading</strong> a sample of comments every month. Numbers lose the detail that drives action.</li></ul>
{tests([("How large should the monthly validation sample be?", "<p>Large enough that each theme you report has dozens of true cases. For a 2% theme that means oversampling: draw extra comments the model tagged with that theme, and weight back when estimating rates.</p>")])}"""

s9 = f"""<ul>
<li><strong>LLM tagging or a trained classifier?</strong> LLMs are fast to set up and flexible; classifiers are cheaper and more stable at scale. Many teams start with an LLM, then distil its validated tags into a small classifier.</li>
<li><strong>Is LLM agreement with humans enough?</strong> Matching human kappa is good, but humans and models may err on different comments, which matters for trends in particular themes.</li>
<li><strong>Should rare themes be reported at all?</strong> Corrected shares with wide intervals are honest but easily misread. Some teams report rare themes as counts of verified examples instead.</li>
<li><strong>Discovery versus tracking.</strong> Fixed taxonomies make trends comparable but miss new issues; open discovery finds new issues but breaks comparability. Most programmes need both.</li></ul>
{tests([("Make the case for distilling an LLM tagger into a small classifier.", "<p>Lower cost per comment, faster, deterministic outputs, and no drift from silent model updates. The LLM's validated tags become training data, so the taxonomy work is not lost.</p>")])}"""

rungs = [
 {"ask": "How would you track themes in customer feedback over time?", "follow": ["How do you know the tagging is right?", "What could create a fake trend?"],
  "weak": "<p>\"Run a topic model every month.\"</p>",
  "strong": "<p>Discover themes with embedding clusters or a topic model and human reading; fix a taxonomy with definitions; tag with a classifier or an LLM at a fixed version; validate on a hand-labelled sample against human agreement; correct shares for measured error rates; re-validate monthly. Fake trends come from prompt or model changes, new feedback prompts, and shifts in who writes.</p>"},
 {"ask": "An LLM tags 4.7% of comments as counterfeit concerns. Its sensitivity is 0.90 and specificity 0.97. What is the true share?", "follow": ["What is the precision of those tags?", "What would you tell the trust and safety team?"],
  "model": "<p>observed = 0.90 × π + 0.03 × (1 − π), so π = (0.047 − 0.03) ÷ 0.87 ≈ 2.0%. Precision is about 38%: most tags are false alarms because 3% of the non-counterfeit majority outnumbers the real cases. Report about 2% with an interval, and read the tagged comments before planning work.</p>",
  "weak": "<p>Reports 4.7%.</p>",
  "strong": "<p><b>Must have.</b> Corrects with sensitivity and specificity and explains the base-rate effect.</p><p><b>Strong signal.</b> Notes the uncertainty in the error rates themselves and proposes oversampling for validation.</p>"},
 {"ask": "Two labellers agree on 85% of comments. Is the theme well defined?", "follow": ["Compute kappa if each marked 65 of 200 as yes.", "What if kappa is 0.4?"],
  "weak": "<p>\"Yes, 85% is high.\"</p>",
  "strong": "<p>Chance agreement here is 56%, so kappa is (0.85 − 0.56) ÷ 0.44 ≈ 0.66: substantial but fuzzy. At 0.4, the definition needs work: add examples and boundary rules, relabel, and only then measure the model.</p>", "roles": ["ic", "mle"]},
 {"ask": "Design a system that turns 20,000 comments a month into themes leadership can trust.", "follow": ["How do you handle new themes?", "How do you keep trends comparable?"],
  "weak": "<p>\"Send them to an LLM and chart the results.\"</p>",
  "strong": "<p>A versioned taxonomy and tagger; monthly stratified validation with per-theme error rates; corrected shares with intervals; changes run in parallel on back data before switching; an embedding-cluster pass each month to surface new themes, reviewed by a person; a sample of comments read and quoted in every report; normalisation by the number of users prompted for feedback.</p>", "roles": ["ic", "mle"]},
 {"ask": "A product leader wants to cut LLM validation because 'the model is clearly good'. Respond.", "follow": ["What is the cheapest version you would accept?", "What is the risk if you skip it?"],
  "weak": "<p>Agrees, since spot checks looked fine.</p>",
  "strong": "<p>Spot checks do not show error rates, and rare themes can be mostly false alarms while looking fine to the eye. The cheapest acceptable version: 300 comments a month labelled by one person, oversampling rare themes, plus a parallel run whenever the prompt or model changes. The risk otherwise is a roadmap built on a trend created by the tagger.</p>", "roles": ["lead"]},
]

page(S, "C5", "Text analytics on search queries and feedback",
     "Search queries, reviews and support tickets hold what users say in their own words. Topic models and embeddings find the themes; classifiers and LLMs tag them at scale. Like any instrument, the tagger must be measured against people, and its counts corrected for its errors, especially for rare themes.",
     "text analytics topic modelling lda bertopic embeddings clustering llm tagging classification taxonomy cohen's kappa inter-rater agreement sensitivity specificity prevalence correction rogan gladen search queries customer feedback support tickets prompt versioning",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Find themes in text with clustering and reading, track them with a fixed, versioned tagger validated against human labels, and correct the shares for its measured error rates, because a small false-positive rate inflates rare themes and an unversioned prompt change creates trends that are not there.",
     ["Discover with clusters; track with a fixed taxonomy", "Human kappa is the ceiling", "Correct shares: π = (obs − (1 − sp)) / (se + sp − 1)", "Rare themes are inflated by false positives", "Version the model and prompt; re-validate monthly"],
     [("b5-embeddings", "Embeddings and similarity search"), ("b7-llm-evaluation", "Evaluating LLM features and hallucination"), ("a1-bayes-base-rates", "Bayes' rule and base rates")],
     [("c6-qual-quant", "Joining survey, PSAT and UXR findings to behavioural data"), ("c3-key-drivers", "Key driver analysis"), ("b4-precision-recall", "Precision, recall and the threshold")],
     sources=[("Rogan and Gladen, \"Estimating prevalence from the results of a screening test\", American Journal of Epidemiology, 1978", "https://doi.org/10.1093/oxfordjournals.aje.a112510"),
              ("Grootendorst, \"BERTopic: Neural topic modeling with a class-based TF-IDF procedure\", arXiv, 2022", "https://arxiv.org/abs/2203.05794")],
     sec_roles={11: ["lead", "ic", "mle"]})
