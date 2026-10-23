import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "b0-likelihood-entropy"
R = ["ic", "mle"]

s1 = f"""<div class="problem"><p>Two fraud models score four transactions. Only the first is fraud.</p>
{table(["Transaction", "Truth", "Model A", "Model B"], [["1", "Fraud", "0.60", "0.95"], ["2", "Genuine", "0.40", "0.05"], ["3", "Genuine", "0.40", "0.05"], ["4", "Genuine", "0.40", "0.70"]], narrow=True)}
<p>At a 0.5 threshold, what is each model's accuracy? Now score each by log loss, the average of −ln(probability given to what actually happened). Which model would you rather have pricing risk on your marketplace?</p></div>
{attempt(S, 1)}{reveal('''<p><strong>Accuracy:</strong> A gets 4 of 4. B gets 3 of 4, because it puts 0.70 on a genuine transaction.</p>
<p><strong>Log loss:</strong> A gives 0.60 to the truth every time: −ln 0.60 = <strong>0.511</strong>. B gives 0.95 to the truth three times and 0.30 once: (3 × 0.051 + 1.204) / 4 = <strong>0.339</strong>.</p>
<p>The two scores disagree. Accuracy only asks which side of 0.5 each score falls. Log loss asks how much probability the model put on what happened. B is nearly certain and right three times, and its one mistake is not a confident one. A is never wrong and never sure.</p>
<p>For pricing risk you want B: its numbers can be multiplied by a loss to get an expected cost, and A's cannot. Notice also where B's loss comes from: 1.204 of its 1.358 total, almost 90%, is the one transaction. Log loss is dominated by the few cases a model gets wrong with confidence.</p>''')}"""

s2 = f"""<p><strong>The forecaster scored by surprise.</strong> A weather forecaster says 90% rain. If it rains she is barely surprised. If it stays dry she is very surprised. Score her by how surprised she was on each day, averaged over a season. Saying 50% every day keeps her safe from big surprises and earns a mediocre score. Saying 99% when she should have said 70% earns the occasional enormous one.</p>
<p><strong>The phrasebook for the wrong country.</strong> A traveller packs a phrasebook that gives the shortest phrases to the things it expects you to say most. Packed for Spain and used in Spain, conversations are as short as they can be. Used in Portugal, the phrases still work, but every exchange runs longer. The extra length is the price of preparing for the wrong place.</p>
{table(["Idea", "Forecaster", "Phrasebook", "A model"], [
["What happened", "Rain or no rain", "What you needed to say", "The label"],
["The prediction", "Her stated chance", "The phrasebook's expectations", "The predicted probability q"],
["Surprise", "How shocked she is", "How long the phrase is", "−ln q(outcome)"],
["Entropy", "Her surprise if she knew the true odds", "Length with the right phrasebook", "The best possible log loss, H(p)"],
["Cross-entropy", "Her average surprise", "Length with the phrasebook you packed", "The log loss, H(p, q)"],
["KL divergence", "The surprise she could have avoided", "Extra length from the wrong book", "H(p, q) − H(p)"]])}
<p>What does the phrasebook show that the forecaster does not? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Even a perfect forecaster has a floor of unavoidable surprise, the entropy, and the phrasebook separates that floor from the extra cost of the wrong beliefs, which is the KL divergence and the only part a better model can remove.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>The forecaster is scored on one kind of event.</strong> A model's log loss averages over many examples with different true probabilities, so a single number hides which examples carry the loss.</li>
<li><strong>Phrase lengths are whole words.</strong> Information is measured in fractions of a bit or a nat, and the formulas allow any length.</li>
<li><strong>Both treat the true odds as knowable.</strong> In practice you only ever see outcomes, never p, so entropy is estimated, and KL is only defined between distributions you have written down.</li></ul>
{tests([("The forecaster says 100% rain and it stays dry. What is her log loss for the day, and what does a training library do about it?", "<p>−ln 0, which is infinite. Libraries clip probabilities to a range such as 10⁻¹⁵ to 1 − 10⁻¹⁵, so one confident miss costs about 34.5 nats instead of breaking the average.</p>"),
("Why does a forecaster who always says the base rate never get a terrible day?", "<p>She never puts a tiny probability on anything that happens often, so her surprise is bounded. Her average surprise equals the entropy of the outcome, which is the score to beat.</p>", True)])}"""

s3 = f"""<div class="fx">likelihood      L(θ) = Π P(xᵢ | θ)       a function of θ, data fixed
log-likelihood  ℓ(θ) = Σ ln P(xᵢ | θ)    sums beat products
MLE             θ̂ = argmax ℓ(θ)          Bernoulli: θ̂ = k / n
MAP             θ̂ = argmax [ℓ(θ) + ln P(θ)]   the prior is a penalty

entropy         H(p)    = − Σ p(x) ln p(x)
cross-entropy   H(p, q) = − Σ p(x) ln q(x)    = log loss, averaged
KL divergence   KL(p ‖ q) = Σ p(x) ln( p(x) / q(x) )
                          = H(p, q) − H(p)    ≥ 0, not symmetric</div>
<ul>
<li><strong>Likelihood.</strong> How probable the observed data is under a parameter value. It is not the probability of the parameter, and it does not sum to one over θ.</li>
<li><strong>Maximum likelihood.</strong> Pick the parameter that makes the data most probable. For a conversion rate it is the observed share. For a linear model with normal noise of fixed spread it is least squares. For a classifier it is minimum log loss.</li>
<li><strong>MAP.</strong> Add the log of a prior and maximise. A normal prior on weights adds −λΣw², which is L2 regularisation. A Laplace prior adds −λΣ|w|, which is L1.</li>
<li><strong>Entropy.</strong> The average surprise when you know the true distribution. A fair coin has 1 bit, or 0.693 nats. A label that is 2% positive has 0.141 bits. {ref(1)}</li>
<li><strong>Cross-entropy.</strong> The average surprise when outcomes come from p and you predict q. Minimising it over q is the same as maximising the likelihood, because the training labels are draws from p.</li>
<li><strong>KL divergence.</strong> The gap between the two. It is zero only when q = p. The direction matters: KL(p ‖ q) punishes q for putting little mass where p has a lot. {ref(3)}</li></ul>
<p>The chain to carry into an interview: <em>minimise log loss = maximise likelihood = minimise KL from the data to the model</em>. The entropy term is fixed by the data, so the three move together.</p>
{tests([("Why can likelihood not be read as the probability that θ is the true value?", "<p>It is P(data | θ). Turning it into P(θ | data) needs a prior through Bayes' rule, exactly as a p-value cannot be read as the probability of the null.</p>", True),
("A model's log loss is 0.110 on data whose labels are 2% positive. Split it into the part a better model could remove and the part it could not.", "<p>The entropy of a 2% label is 0.098 nats, which no model can beat without better features. The remaining 0.012 is the KL divergence, the room left for improvement.</p>")])}"""

s4 = f"""<h4>Worked: the likelihood of a conversion rate</h4>
<p>A new seller tool is shown to 200 sellers and 12 use it. The log-likelihood of a rate p is 12 ln p + 188 ln(1 − p). It peaks at <strong>p̂ = 12 / 200 = 6%</strong>.</p>
<p>The data favour 6% over 5% by a likelihood ratio of only <strong>1.22</strong>, and over 3% by <strong>11.2</strong>. A common summary is the set of p whose log-likelihood is within 1.92 of the peak, which matches a 95% interval in large samples: <strong>3.3% to 9.9%</strong>. It is lopsided, wider above 6% than below, because a rate cannot go below zero. The symmetric normal interval, 2.7% to 9.3%, ignores that.</p>
<h4>Half-worked: a prior pulls the estimate</h4>
<p>Past seller tools were used by about 5% of sellers. Encode that as a Beta(2, 38) prior. The MAP estimate is (k + a − 1) / (n + a + b − 2) = (12 + 1) / (200 + 38). Finish it, then redo it for 1 user out of 10.</p>
{reveal("<p>13 / 238 = <strong>5.5%</strong>, close to the 6% the data say, because 200 sellers outweigh a prior worth about 40. With 1 of 10, the MLE is 10% and the MAP is 2 / 48 = <strong>4.2%</strong>. With little data the prior dominates. This is the mechanism behind shrinkage in <a href='#a6-partial-pooling'>partial pooling</a>.</p>")}
<h4>Bare: the log loss to beat</h4>
<p>Fraud is 2% of transactions. A model reports a validation log loss of 0.09. Is that good? Find the log loss of a model that predicts 0.02 for every transaction, and say how much better 0.09 is.</p>
{reveal("<p>Predicting the base rate gives the entropy: −(0.02 ln 0.02 + 0.98 ln 0.98) = <strong>0.098</strong>. The model is only <strong>8%</strong> better than knowing nothing about individual transactions. At a 50% base rate the same baseline is 0.693, so 0.09 would be superb. Always report log loss next to the base-rate log loss, or as the share of it removed.</p>")}
<h4>Bare: KL in both directions</h4>
<p>Training data had 2% fraud. Live traffic has 5%. Compute KL(live ‖ train) and KL(train ‖ live) for the label alone.</p>
{reveal("<p>KL(0.05 ‖ 0.02) = 0.05 ln 2.5 + 0.95 ln(0.95 / 0.98) = <strong>0.0163</strong>. KL(0.02 ‖ 0.05) = <strong>0.0121</strong>. The direction changes the number. Drift monitors such as the population stability index add the two directions together to avoid choosing.</p>")}
<h4>Predict, then play</h4>
<p>Keep the observed rate at 6% and raise the sample from 200 to 2,000. Predict how much narrower the likelihood interval gets.</p>
{reveal("<p>About √10 ≈ 3.2 times narrower, from 3.3%–9.9% to <strong>5.0%–7.1%</strong>, and nearly symmetric. More data sharpens the peak of the log-likelihood, which is the same √n you met in <a href='#a1-clt'>the central limit theorem</a>.</p>")}
<div class="lab" data-lab="likelihood"></div>
<pre class="code">import numpy as np

y = np.array([1, 0, 0, 0])
def log_loss(p, eps=1e-15):
    p = np.clip(p, eps, 1 - eps)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

log_loss(np.array([.60, .40, .40, .40]))   # 0.511
log_loss(np.array([.95, .05, .05, .70]))   # 0.339
log_loss(np.full(4, y.mean()))             # 0.562, the base-rate model for this tiny sample</pre>
{tests([("A model trained by minimising mean squared error on 0/1 labels. Is it doing maximum likelihood?", "<p>Not for a Bernoulli outcome. Squared error is the likelihood for normal noise. On 0/1 labels it is the Brier score, a proper score but a different one, and it punishes confident mistakes far less than log loss.</p>"),
("Why does the interval for 12 of 200 extend further above 6% than below?", "<p>The log-likelihood is steeper towards zero, because a rate near zero makes 12 successes very unlikely, and flatter above. The interval follows the curve, so it is lopsided.</p>", True)])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The examples are independent", "Many rows per user: the likelihood counts one user's behaviour many times and intervals come out too narrow", "Refit on one row per user and compare"],
["The model family can describe the data", "A misspecified model has an MLE, but it is the closest wrong answer in KL, not the truth", "Calibration plots show systematic bends"],
["The maximum exists", "Perfect separation in logistic regression: the weights run off to infinity", "Coefficients and standard errors explode; add a penalty"],
["The sample is large", "The MLE of a variance divides by n and is biased low; 1 success in 10 gives a 10% rate with huge uncertainty", "Compare with MAP or a posterior"],
["The probabilities can be trusted at the extremes", "One prediction of 0.999 on a negative costs 6.9 nats and can dominate a validation loss", "Inspect the largest per-example losses before comparing models"],
["The base rate is the same in training and use", "Log loss and KL shift with prevalence, so a model's loss is not comparable across periods", "Report loss relative to the base-rate loss of each period"]])}
<p>The row that bites in interviews is the misspecified one. Maximum likelihood always returns an answer. It says nothing about whether the model could have been right.</p>
{tests([("A logistic regression on a small fraud sample returns a coefficient of 41 with a standard error of 9,000. What happened and what do you do?", "<p>A feature separates the classes perfectly in this sample, so the likelihood keeps rising as the coefficient grows. Add an L2 penalty, which is a prior that makes the maximum finite, or merge rare categories.</p>")])}"""

s6 = f"""{table(["Tool", "What it gives", "Pick it when", "Watch out"], [
["Maximum likelihood", "The parameter that makes the data most probable", "Plenty of data, a sensible model", "Overconfident with little data"],
["MAP", "Likelihood plus a prior penalty", "You need a point estimate and have prior knowledge or many parameters", "Depends on how the prior is written"],
["Full Bayesian posterior", "A distribution over parameters", "Small samples, decisions that need uncertainty", "Costs computation, needs a prior"],
["Method of moments", "Match sample averages to model averages", "A quick estimate, or a starting point for an optimiser", "Can be inefficient or give impossible values"],
["Log loss (cross-entropy)", "A score for probabilities", "You will act on the probabilities", "Dominated by confident errors"],
["Brier score", "Squared error on probabilities", "You want a bounded, more forgiving score", "Less sensitive to rare-event quality"],
["Accuracy", "Share on the right side of a threshold", "Only the decision matters, at one fixed threshold", "Ignores confidence and the base rate"]])}
{tests([("You fit 2,000 seller-level conversion rates, many with under 20 visits. Which row?", "<p>MAP with a shared prior, or the full posterior: the hierarchical version is partial pooling. Raw MLEs would put the top of the ranking full of sellers with 2 sales from 3 visits.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Training a logistic regression.</strong> Minimise log loss on clicks.</p>
<p><strong>Pretraining a language model.</strong> Minimise cross-entropy on the next token.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Distillation.</strong> Train a small model to match a large model's predicted distribution.</p>
<p><strong>Drift monitoring.</strong> Compare this week's feature distribution with the training one.</p></div></div>
{reveal('''<p><strong>Pair 1 is maximum likelihood.</strong> Both models are trained by the same objective: make the observed label probable. A language model's loss is often reported as perplexity, e<sup>loss</sup>. A loss of 2.3 nats per token is a perplexity of 10, as if the model were choosing evenly among 10 tokens.</p>
<p><strong>Pair 2 is KL divergence between two distributions.</strong> Distillation minimises KL from the teacher to the student, so the student learns the teacher's uncertainty as well as its answers. Drift monitors compute a divergence between two histograms, often the symmetric population stability index used in <a href="#d3-monitoring-drift">monitoring and drift</a>.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Comparing log loss across datasets. "The new model's log loss is 0.07, down from 0.10" can mean nothing if the validation period's fraud rate fell from 3% to 2%: the base-rate loss alone falls from 0.135 to 0.098. Compare each model's loss with the base-rate loss of the same data, or compare models on the same rows.</p>
{tests([("A vendor says its model has a log loss of 0.05. What two numbers do you ask for?", "<p>The base rate of the evaluation data, to compute the log loss of predicting it, and the log loss of your current model on the same rows.</p>")])}"""

s8 = f"""<ul>
<li><strong>Write the likelihood before choosing the loss.</strong> Counts suggest Poisson, yes/no suggests Bernoulli, positive skewed amounts suggest a lognormal or gamma. The loss follows.</li>
<li><strong>Report log loss with its baseline.</strong> "0.090 against 0.098 for the base rate" is honest. "0.09" alone is not.</li>
<li><strong>Look at the worst 20 examples by loss.</strong> They are usually label errors, leakage or a missing feature.</li>
<li><strong>Clip predictions and check calibration.</strong> A model that is right but overconfident loses on log loss and on decisions: see <a href="#b4-calibration">calibration</a>.</li>
<li><strong>Read regularisation as a prior.</strong> It makes the strength of λ a statement about how large you expect effects to be, which is easier to defend.</li>
<li><strong>Use likelihood ratios to compare nested models.</strong> Twice the gain in log-likelihood is roughly chi-square with as many degrees of freedom as added parameters.</li></ul>
{tests([("Two models differ by one feature. The larger one improves the total log-likelihood on 10,000 rows by 1.5. Is the feature worth keeping on that evidence?", "<p>Twice the gain is 3.0, against a chi-square critical value of 3.84 at 5% with one degree of freedom. Not convincing. Check it on held-out data, where the gain may vanish.</p>")])}"""

s9 = f"""<ul>
<li><strong>MLE or Bayesian?</strong> One camp prefers the MLE because it needs no prior and is what most libraries compute. The other notes that for small samples and many parameters a prior is not optional, and that regularised models are already MAP estimates with an unstated prior. In large-sample product work they usually agree.</li>
<li><strong>Which direction of KL?</strong> Minimising KL(p ‖ q) makes q cover all of p's mass and can blur across modes. Minimising KL(q ‖ p) lets q settle on one mode. Variational inference uses the second and is criticised for understating uncertainty.</li>
<li><strong>Log loss or Brier for model selection?</strong> Both are proper scores, which reward honest probabilities. {ref(2)} Log loss weighs rare confident errors heavily, which suits fraud and safety. Brier is bounded and more stable on small validation sets.</li>
<li><strong>Is perplexity a good LLM metric?</strong> It measures how well a model predicts text, which tracks fluency. It does not measure whether answers are correct or useful, which is why <a href="#b7-llm-evaluation">LLM evaluation</a> needs task-level tests.</li></ul>
{tests([("Give one case where you would choose Brier score over log loss.", "<p>Comparing models on a small validation set where one or two mislabelled rows would dominate log loss. Brier caps the damage of each row at 1.</p>")])}"""

rungs = [
 {"ask": "What is maximum likelihood estimation, and what does it give for a conversion rate?", "follow": ["Is the likelihood a probability distribution over the parameter?", "What does it give for a linear model with normal errors?"],
  "weak": "<p>\"It finds the most likely parameter.\"</p>",
  "strong": "<p>It picks the parameter value under which the observed data are most probable: k / n for a rate. The likelihood is a function of the parameter with the data fixed, and it is not a probability of the parameter. With normal errors of fixed spread it reduces to least squares, and for a classifier to minimising log loss.</p>"},
 {"ask": "Why do we train classifiers with log loss rather than accuracy?", "follow": ["When would accuracy and log loss pick different models?", "What is the log loss of a model that always predicts the base rate?"],
  "model": "<p>log loss is the negative log-likelihood of a Bernoulli outcome, so minimising it is maximum likelihood, and it is smooth, so gradients exist. Accuracy is flat almost everywhere and ignores how confident the model was. Log loss rewards honest probabilities, which matter whenever a score is multiplied by a cost or a price.</p>",
  "weak": "<p>\"Accuracy is not differentiable.\" True, and only half the reason.</p>",
  "strong": "<p><b>Must have.</b> Links log loss to likelihood and to probabilities that can be acted on.</p><p><b>Strong signal.</b> Gives the base-rate baseline, 0.098 at 2%, and an example where accuracy and log loss disagree.</p>"},
 {"ask": "How are cross-entropy, entropy and KL divergence related, and why does it matter for training?", "follow": ["Which of the three can a better model reduce?", "Is KL symmetric?"],
  "weak": "<p>Gives three formulas without connecting them.</p>",
  "strong": "<p>Cross-entropy = entropy + KL. The entropy is fixed by the data, so minimising cross-entropy is minimising KL from the data distribution to the model. Only the KL part can be reduced. KL is not symmetric: the direction decides whether the model covers every mode or settles on one.</p>", "roles": ["mle"]},
 {"ask": "Your logistic regression returns a coefficient of 41 with an enormous standard error. Diagnose and fix it, in terms of the likelihood.", "follow": ["Why does adding L2 fix it?", "What prior does L2 correspond to?"],
  "weak": "<p>\"Drop the feature.\"</p>",
  "strong": "<p>Perfect or near-perfect separation: the likelihood keeps increasing as the coefficient grows, so the maximum is at infinity. L2 adds −λw² to the log-likelihood, which is a normal prior centred on zero and makes the maximum finite. Alternatives: merge rare categories, or use Firth's penalised likelihood.</p>", "roles": ["ic", "mle"]},
 {"ask": "A team reports that a new fraud model cut validation log loss from 0.10 to 0.07 and wants to replace the old one. What do you check before you agree?", "follow": ["The validation months differ. Does that matter?", "Log loss improved but precision at the review threshold did not. Which wins?"],
  "weak": "<p>Accepts a 30% improvement.</p>",
  "strong": "<p>Were both models scored on the same rows, and what is the base-rate loss of those rows? A fall in prevalence alone lowers log loss. Looks at calibration and at the largest per-row losses. Then checks the decision metric at the operating threshold, because a better log loss can come from better probabilities in a region where no decision is made.</p>", "roles": ["ic", "mle"]},
]

page(S, "B0", "Likelihood, cross-entropy and KL divergence",
     "Why minimising log loss is the same as maximising likelihood, what a log loss of 0.09 is worth, and how entropy and KL divergence split a model's error into the part you can remove and the part you cannot.",
     "maximum likelihood mle map prior log loss cross-entropy entropy kl divergence perplexity brier proper scoring rule bernoulli separation regularisation information theory nats bits",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Training by log loss is maximum likelihood, and the loss splits into the entropy of the data, which nothing removes, and the KL divergence from the data to the model, which is the only part a better model can shrink, so every log loss must be read against the base-rate loss.",
     ["Likelihood is the probability of the data as a function of the parameter", "Log loss is negative log-likelihood, so minimising it is maximum likelihood", "Cross-entropy = entropy + KL; only KL can be reduced", "Judge a log loss against the base-rate log loss", "A prior turns MLE into MAP, which is regularisation"],
     ["Logarithms and the product rule", ("a1-distributions", "Matching a distribution to a process")],
     [("b2-logistic-regression", "Logistic regression, odds and log loss"), ("b4-calibration", "Calibration"), ("a6-bayesian-updating", "Bayesian updating and credible intervals"), ("b7-model-families-sampling", "Encoders, decoders and sampling")],
     sources=[("Shannon, \"A Mathematical Theory of Communication\", Bell System Technical Journal, 1948", "https://doi.org/10.1002/j.1538-7305.1948.tb01338.x"),
              ("Gneiting and Raftery, \"Strictly Proper Scoring Rules, Prediction, and Estimation\", Journal of the American Statistical Association, 2007", "https://doi.org/10.1198/016214506000001437"),
              ("Kullback and Leibler, \"On Information and Sufficiency\", Annals of Mathematical Statistics, 1951", "https://doi.org/10.1214/aoms/1177729694")],
     sec_roles={1: R, 11: ["lead", "ic", "mle"]})
