import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "a5-sensitivity-falsification"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>A matched observational study finds that loyalty programme members are more likely to buy again within a year: risk ratio <strong>1.30</strong>, 95% interval <strong>1.18 to 1.43</strong>, after matching on 25 covariates with every standardised difference below 0.05.</p>
<p>The programme owner says the matching settles it. You know motivation was not measured.</p>
<p>Two questions. How strong would an unmeasured confounder need to be to explain the whole effect away? And the strongest measured confounder, prior purchase count, was associated with joining by a risk ratio of <strong>1.8</strong> and with buying again by <strong>2.5</strong>. What does that suggest?</p></div>
{attempt(S, 1)}{reveal(f'''<p>The <strong>E-value</strong> answers the first: RR + √(RR × (RR − 1)) = 1.30 + √0.39 = <strong>1.92</strong>. An unmeasured confounder associated with both membership and buying again by a risk ratio of 1.92 each, beyond the measured covariates, could fully explain the result. To move the lower end of the interval to 1, it would need only <strong>1.64</strong>. {ref(1)}</p>
<p>The second gives a benchmark. A confounder as strong as prior purchase count, 1.8 and 2.5, produces a bias factor of 1.8 × 2.5 ÷ (1.8 + 2.5 − 1) = <strong>1.36</strong>, more than the whole effect: the adjusted estimate would be 1.30 ÷ 1.36 = 0.95.</p>
<p>So the result is fragile: an unmeasured factor about as important as the strongest measured one would erase it, and motivation plausibly is. Report it as suggestive, and look for a design that does not depend on measuring motivation.</p>''')}"""

s2 = f"""<p><strong>A bridge's load rating.</strong> Engineers do not certify a bridge as "safe". They say how much weight it can bear before it fails, and you compare that with the heaviest lorry that might cross. A conclusion is robust if it survives loads far beyond any realistic one.</p>
<p><strong>A smoke alarm test button.</strong> Before trusting an alarm, you press the test button: a situation where you know the right answer. An alarm that sounds when there is no smoke, or stays silent when you hold a match to it, has told you something about itself, not about fire.</p>
{table(["Idea", "Bridge", "Smoke alarm", "Causal estimate"], [
["The question", "How much load until failure?", "Does it respond correctly to known cases?", "How much bias to erase it? Does it pass checks with known answers?"],
["The tool", "Load rating", "Test button", "Sensitivity analysis; falsification tests"],
["What you compare with", "The heaviest realistic lorry", "No smoke, then smoke", "The strongest measured confounder; placebo outcomes"],
["A good result", "Rating far above realistic loads", "Silent without smoke, loud with it", "Large E-value; null placebo effects"],
["What it cannot do", "Prove nothing heavier will come", "Prove every fire will be caught", "Prove no confounder exists"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Neither proves the thing works; one measures how much it can withstand, the other checks it against cases where the right answer is known.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Lorry weights are known.</strong> The strength of an unmeasured confounder is not, which is why benchmarking against measured ones matters.</li>
<li><strong>The test button exercises the real mechanism.</strong> A placebo outcome only tests the confounding that would also affect the placebo; a bias that touches only the real outcome passes unseen.</li>
<li><strong>Both are one-off.</strong> Causal estimates need several checks, each catching a different failure.</li></ul>
{tests([("A placebo test passes: members and matched non-members had the same purchases in the year before joining. Does that prove there is no unmeasured confounding?", "<p>No. It shows the matching removed differences that showed up in past purchases. A confounder that affects future behaviour but did not show in the past, such as a planned move or new income, is untouched.</p>")])}"""

s3 = f"""<div class="fx">E-value (for a risk ratio RR &gt; 1)
   E = RR + √(RR × (RR − 1))
   the minimum strength, on the risk-ratio scale, that an unmeasured
   confounder needs with both treatment and outcome to explain RR away
   compute it for the estimate and for the interval bound nearer 1

bias factor of a confounder with strengths a (treatment), b (outcome)
   B = a × b / (a + b − 1)       adjusted RR = observed RR ÷ B

Rosenbaum Γ (matched pairs)
   within a pair, hidden bias may make one unit up to Γ times
   more likely to be treated; find the Γ at which the result
   stops being significant

falsification (placebo) tests
   placebo outcome    something the treatment cannot affect
   placebo timing     a fake treatment date before the real one
   negative control   a treatment that should do nothing</div>
<ul>
<li><strong>Sensitivity analysis</strong> does not ask whether there is unmeasured confounding, which there almost always is. It asks how much there would need to be, and compares that with something you can measure.</li>
<li><strong>Benchmark against measured covariates.</strong> "An unmeasured confounder as strong as prior purchases would erase it" is far more useful than "the E-value is 1.92". {ref(2)}</li>
<li><strong>Rosenbaum bounds</strong> suit matched designs: Γ = 1 is no hidden bias; Γ = 2 lets hidden bias double one unit's odds of treatment within a pair. {ref(3)}</li>
<li><strong>Falsification tests</strong> look for effects that should not exist. Finding one shows something is wrong; finding none is weaker evidence that all is well.</li></ul>
{tests([("Why compute an E-value for the lower confidence limit as well as the estimate?", "<p>The estimate's E-value says how much bias would move it to no effect. The limit's E-value says how much would make the interval include no effect, often the more relevant threshold, since that is when you could no longer claim an effect at all.</p>", True),
("An E-value is 1.15. Is the result fragile?", "<p>Very. A confounder associated with treatment and outcome by only 15% each could explain it, and almost any omitted factor is that strong.</p>")])}"""

s4 = f"""<h4>Worked: E-values and a benchmark</h4>
<ul><li>Estimate RR = 1.30: E = 1.30 + √(1.30 × 0.30) = 1.30 + 0.62 = <strong>1.92</strong>.</li>
<li>Lower limit 1.18: E = 1.18 + √(1.18 × 0.18) = 1.18 + 0.46 = <strong>1.64</strong>.</li>
<li>Benchmark, prior purchases (1.8, 2.5): B = 4.5 ÷ 3.3 = <strong>1.36</strong>, adjusted RR = 0.95.</li>
<li>A weaker benchmark, an unmeasured factor at 1.5 and 1.5: B = 2.25 ÷ 2.0 = 1.125, adjusted RR = <strong>1.16</strong>, still above 1.</li></ul>
<p>The conclusion is conditional: the effect survives confounding of moderate strength and does not survive confounding as strong as the strongest known factor. Whether motivation is that strong is the question to argue about, now with numbers.</p>
<h4>Half-worked: Rosenbaum's Γ</h4>
<p>In 1,000 matched pairs that disagree, the member bought again and the non-member did not in <strong>600</strong>. With no hidden bias, each pair would go either way with probability 0.5, and 600 of 1,000 is far beyond chance. With hidden bias Γ, the worst case gives the member probability Γ ÷ (1 + Γ) of being the one who bought. At Γ = 1.3, that is 0.565, and 600 is still significant (worst-case p = 0.014). Find the Γ at which the worst-case p-value reaches 0.05, and say what it means.</p>
{reveal("<p>At Γ = 1.4, the probability is 0.583, the expected count 583 with sd 15.6, and p = 0.15. The threshold is about <strong>Γ = 1.35</strong>. Hidden bias that made one person in a matched pair 35% more likely to join than the other, for reasons unmeasured, could produce this result by itself. That is modest: the finding is sensitive.</p>")}
<h4>Bare: a placebo outcome</h4>
<p>After matching, members bought <strong>9% more</strong> in the six months before they joined than their matched non-members, interval 4% to 14%. What does this tell you, and what do you do?</p>
{reveal("<p>The matching failed on something that predicts purchasing: members were already more active, in a way the 25 covariates did not capture. The 1.30 likely includes that difference. Options: match on detailed pre-period purchase history, use the pre-period gap in a difference-in-differences, or report that the design cannot separate selection from effect. Another reading is anticipation, people buying more just before joining because they planned to, which also argues for anchoring the comparison earlier.</p>")}
<h4>Predict, then play</h4>
<p>Predict the E-value of a risk ratio of 2.0, and of 1.1.</p>
{reveal("<p><strong>3.41</strong> and <strong>1.43</strong>. The E-value rises faster than the risk ratio: a doubling needs a strong confounder, while a 10% effect is erased by a modest one.</p>")}
<div class="lab" data-lab="evalue"></div>
<pre class="code">import numpy as np

def e_value(rr):
    rr = max(rr, 1 / rr)               # works for protective effects too
    return rr + np.sqrt(rr * (rr - 1))

e_value(1.30), e_value(1.18)        # 1.92 and 1.64

# Rosenbaum bound for a sign test on matched pairs
from scipy.stats import binom
p_worst = lambda gamma, k=600, n=1000: binom.sf(k - 1, n, gamma / (1 + gamma))</pre>
{tests([("For an odds ratio from a common outcome, why can you not plug it straight into the E-value formula?", "<p>The formula is for risk ratios. When the outcome is common, an odds ratio exaggerates the risk ratio, so convert it first, for example with the square root of the odds ratio as an approximation.</p>", True),
("Your E-value for the lower limit is 1.64, and the strongest measured covariate has strengths 1.3 and 1.4. How do you read that?", "<p>The bias factor of a confounder like that is 1.82 ÷ 1.7 = 1.07, well below what is needed. The result would survive an unmeasured confounder as strong as anything measured, which is fairly reassuring if the measured set is rich.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["Benchmarks resemble the unmeasured confounders", "The missing factor is of a different kind and much stronger", "Domain knowledge; say what is missing and why it might be strong"],
["The placebo outcome shares the confounding", "Motivation affects future purchases but not past ones", "A passing placebo is weaker evidence; use several"],
["The placebo outcome cannot be affected", "Pre-period purchases include anticipation of joining", "Move the placebo window further back"],
["The sensitivity model fits", "E-values assume a worst case on the risk-ratio scale; effects on means need conversion", "Use the version for your outcome type"],
["Matched pairs are independent", "Pairs share shocks or reuse controls", "Account for reuse; use the matching-aware analysis"],
["One check is enough", "Each check covers one failure", "Combine sensitivity, placebo outcomes and placebo timing"]])}
{tests([("A placebo outcome, 'buying office supplies', shows no effect of a fashion loyalty programme. Is that a good test?", "<p>Weak. A useful placebo shares the suspected confounding with the real outcome. Office supplies are driven by different things than fashion purchases, so passing says little. Prior fashion purchases would be a better placebo.</p>")])}"""

s6 = f"""{table(["Check", "Answers", "Pick it when", "Watch out"], [
["E-value", "How strong must hidden confounding be?", "Any risk-ratio-like estimate", "Needs a benchmark to interpret"],
["Benchmarking (e.g. Cinelli–Hazlett)", "Would a confounder like X erase it?", "Regression estimates with measured covariates", "Assumes the unmeasured resemble the measured"],
["Rosenbaum Γ", "How much hidden bias in treatment assignment?", "Matched designs", "Abstract; translate Γ into a story"],
["Placebo outcome", "Is there residual confounding?", "An outcome the treatment cannot affect exists", "Must share the confounding"],
["Placebo timing", "Is there an effect before treatment?", "Panel data, DiD, ITS", "Anticipation can produce real early effects"],
["Negative control treatment", "Does a do-nothing 'treatment' show an effect?", "A similar but inert exposure exists", "Hard to find a truly inert one"]])}
{tests([("You have a difference-in-differences estimate. Which two rows would you run first?", "<p>Placebo timing, an event study with pre-treatment periods, and a placebo outcome that the treatment cannot affect but shares the trend drivers.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Premium subscribers churn less.</strong> Observational, matched.</p>
<p><strong>Sellers who use the pricing tool sell more.</strong> Opt-in, regression-adjusted.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A city launch measured by DiD.</strong> The event study shows a dip two months before launch.</p>
<p><strong>A new onboarding flow measured by ITS.</strong> A fake launch date also shows a jump.</p></div></div>
{reveal('''<p><strong>Pair 1 needs sensitivity analysis.</strong> Self-selection by motivated users is the obvious unmeasured confounder. Report E-values benchmarked against the strongest measured covariate, and test a placebo outcome from before adoption.</p>
<p><strong>Pair 2 has failed a falsification test.</strong> Effects before the treatment, or at fake dates, mean the design is picking up something else: a pre-existing trend, a coincident change, or a mis-specified model. Fix the design before reporting any effect.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>"We controlled for everything." A study adjusts for dozens of variables, reports a precise effect, and treats the number of covariates as proof of causality. The number of covariates says nothing about the ones missing. Sensitivity analysis turns the unanswerable claim, "there is no unmeasured confounding", into an answerable one: how strong would it have to be. {ref(1)}</p>
{tests([("A colleague says sensitivity analysis is pointless because you can never know the unmeasured confounder's strength. Respond.", "<p>True, but you can compare the required strength with the strengths you can measure and with what domain experts believe. If the required strength is implausibly large, the conclusion is robust; if it is small, it is fragile. Either is decision-relevant.</p>")])}"""

s8 = f"""<ul>
<li><strong>Put the E-value, or Γ, in every observational readout</strong>, for the estimate and the interval limit.</li>
<li><strong>Benchmark</strong> against the two or three strongest measured confounders. A sentence such as "a confounder as strong as prior purchases would erase this" is what leaders can use.</li>
<li><strong>Name the suspected unmeasured confounder</strong> and argue its strength from domain knowledge.</li>
<li><strong>Choose placebo outcomes and dates before seeing the results</strong>, and report them even when they pass.</li>
<li><strong>Prefer designs to adjustments.</strong> A fragile result is a reason to run an experiment or find a natural one, not to add covariates.</li></ul>
{tests([("Your estimate's E-value is 4.2 and every placebo passes. Leadership asks if it is now proven. What do you say?", "<p>Not proven, but robust: only an unmeasured confounder far stronger than anything we measured could explain it, and the checks we could run with known answers came back as expected. That is about as strong as observational evidence gets.</p>")])}"""

s9 = f"""<ul>
<li><strong>Are E-values too lenient?</strong> Critics note that the E-value assumes the confounder is equally strong with treatment and outcome, the worst-case allocation, and that reading it without a benchmark invites over-confidence. Its authors agree it needs context.</li>
<li><strong>Which sensitivity model?</strong> E-values, Rosenbaum bounds, partial R² approaches and Bayesian models make different assumptions. Results under different models are not directly comparable.</li>
<li><strong>Should a failed placebo kill a result?</strong> One view: yes, the design is broken. Another: a small placebo effect can be subtracted, as DiD does. It depends on whether the placebo measures the same bias.</li>
<li><strong>Do sensitivity analyses get gamed?</strong> Choosing benchmarks or placebo outcomes after seeing results lets an analyst show robustness. Pre-specifying them is the defence.</li></ul>
{tests([("Make the case that a failed placebo outcome can be used to correct, rather than discard, an estimate.", "<p>If the placebo shares the same confounding in the same amount, its effect estimates the bias, and subtracting it is a difference-in-differences. That works only under that equal-bias assumption, which needs its own justification.</p>")])}"""

rungs = [
 {"ask": "You have an observational estimate. How do you assess unmeasured confounding?", "follow": ["What is an E-value?", "What is a placebo outcome?"],
  "weak": "<p>\"Add more control variables.\"</p>",
  "strong": "<p>Sensitivity analysis: how strong a hidden confounder must be to erase the effect, via an E-value, Rosenbaum Γ or partial R², benchmarked against the strongest measured confounders. Falsification tests: placebo outcomes the treatment cannot affect, fake treatment dates, and inert treatments, which should all show nothing.</p>"},
 {"ask": "A loyalty programme shows a risk ratio of 1.30 for repeat purchase, interval 1.18 to 1.43. The strongest measured confounder has strengths 1.8 and 2.5. How robust is it?", "follow": ["Compute the E-values.", "What would you tell the programme owner?"],
  "model": "<p>E-value for 1.30 is 1.92, and 1.64 for the lower limit. A confounder like prior purchases has a bias factor of 4.5 ÷ 3.3 = 1.36, enough to bring the estimate to 0.95. So the result does not survive confounding as strong as the strongest known factor; motivation plausibly is that strong. Report it as suggestive.</p>",
  "weak": "<p>Computes the E-value and calls it robust because it is above 1.</p>",
  "strong": "<p><b>Must have.</b> Both E-values and the benchmark comparison.</p><p><b>Strong signal.</b> Names motivation, proposes a placebo outcome and an experiment or encouragement design.</p>"},
 {"ask": "After matching, the treated group had 9% higher purchases in the six months before treatment. What does that mean?", "follow": ["Could it be anticipation?", "How would you fix the design?"],
  "weak": "<p>\"It is a small difference; the matching was good enough.\"</p>",
  "strong": "<p>A failed placebo: residual selection the covariates missed, so the effect estimate includes it. Or anticipation, if people buy before joining because they planned to. Match on detailed pre-period history, move the placebo window back to test anticipation, or use the pre-period gap in a difference-in-differences. Report it either way.</p>", "roles": ["lead", "ic"]},
 {"ask": "Design the robustness section every observational study at your company must include.", "follow": ["Who chooses the placebos, and when?", "What result sends a study back?"],
  "weak": "<p>\"Try a few model specifications.\"</p>",
  "strong": "<p>Pre-specified before results: the main suspected unmeasured confounder and why; E-values for estimate and limit; a benchmark against the two strongest measured confounders; one placebo outcome sharing the suspected confounding; placebo timing where there is time structure. A failed placebo or an E-value below the benchmark sends it back or changes the headline to \"suggestive\".</p>", "roles": ["lead", "ic"]},
 {"ask": "A VP wants to cite a 30% effect from an observational study in a board memo. The E-value for the lower limit is 1.2. What do you do?", "follow": ["The VP says every study has caveats. Respond.", "What wording would you accept?"],
  "weak": "<p>Adds a footnote and lets it go.</p>",
  "strong": "<p>Explains in one line: a hidden factor that made members 20% more likely to join and to buy would erase the result, and such factors are common. Offers wording such as \"associated with\", or a range that includes no effect, and proposes the experiment that would settle it. A board memo is the place where a fragile number does most harm.</p>", "roles": ["lead"]},
]

page(S, "A5", "Sensitivity to hidden confounding and falsification tests",
     "Every observational estimate assumes no unmeasured confounding, and that assumption cannot be tested directly. It can be stress-tested: how strong would a hidden confounder need to be to erase the effect, and does the method find effects where it should find none?",
     "sensitivity analysis unmeasured confounding e-value bias factor rosenbaum bounds gamma benchmarking omitted variable bias placebo test falsification negative control placebo outcome placebo timing robustness",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Since unmeasured confounding can never be ruled out, state how strong it would have to be to erase the effect, compare that with the strongest confounders you did measure, and run falsification tests where the right answer is known to be no effect.",
     ["The question is how much confounding, not whether", "E-value for the estimate and the interval limit", "Benchmark against measured confounders", "Rosenbaum Γ for matched pairs", "Placebo outcomes, timing and treatments must show nothing"],
     [("a5-confounding-dags", "Confounders, mediators and colliders"), ("a5-matching-propensity", "Matching and propensity scores"), ("a5-balance-overlap", "Covariate balance, overlap and coarsened exact matching")],
     [("a5-diff-in-diff", "Difference-in-differences and synthetic control"), ("e1-exec-communication", "Communicating results to executives"), ("a5-mediation", "Mediation analysis")],
     sources=[("VanderWeele and Ding, \"Sensitivity Analysis in Observational Research: Introducing the E-Value\", Annals of Internal Medicine, 2017", "https://doi.org/10.7326/M16-2607"),
              ("Cinelli and Hazlett, \"Making Sense of Sensitivity: Extending Omitted Variable Bias\", Journal of the Royal Statistical Society Series B, 2020", "https://doi.org/10.1111/rssb.12348"),
              ("Rosenbaum, Observational Studies, 2nd edition, Springer, 2002", "https://doi.org/10.1007/978-1-4757-3692-2")],
     sec_roles={11: ["lead", "ic", "mle"]})
