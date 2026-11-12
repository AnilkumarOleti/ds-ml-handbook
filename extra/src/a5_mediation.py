import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "a5-mediation"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>A randomised test of a new seller onboarding flow raised 90-day GMV by <strong>₹12 thousand</strong> per seller. The flow nags sellers to add photos, and the team believes photos are why it worked.</p>
<p>Treated sellers added <strong>1.5 more photos</strong> per listing. A regression of GMV on the treatment and photo count gives <strong>₹4 thousand per photo</strong>, holding treatment fixed. The analyst reports: 1.5 × 4 = ₹6 thousand through photos, <strong>50%</strong> of the effect.</p>
<p>The team now plans to drop the rest of the flow and keep only the photo nag. What is wrong with the 50%, and what would you check before they do it?</p></div>
{attempt(S, 1)}{reveal(f'''<p>Treatment was randomised; photos were not. Sellers who add more photos tend to be experienced and careful, and those sellers sell more anyway. So the ₹4 thousand per photo mixes the effect of photos with the effect of being the kind of seller who adds them, and the indirect effect is overstated.</p>
<p>A separate test that randomised only a photo prompt found <strong>₹2.5 thousand</strong> per added photo. With that, the photo path carries 1.5 × 2.5 = <strong>₹3.75 thousand, about 31%</strong>, and the other parts of the flow carry ₹8.25 thousand. Keeping only the photo nag would give up most of the gain.</p>
<p>Mediation needs two causal effects, of treatment on the mediator and of the mediator on the outcome. Randomising the treatment secures only the first. {ref(2)}</p>''')}"""

s2 = f"""<p><strong>A tutoring programme and homework.</strong> Pupils in a tutoring programme score higher, and they also do more homework. How much of the gain comes through the homework? Pupils who do more homework are also more diligent, so comparing pupils by homework done credits homework with diligence.</p>
<p><strong>A painkiller and sleep.</strong> A painkiller improves next-day mood. Is that because people sleep better, or directly? People who sleep well differ in many ways, so the sleep path needs its own evidence.</p>
{table(["Idea", "Tutoring", "Painkiller", "Onboarding flow"], [
["Treatment", "Tutoring", "The drug", "New flow"],
["Mediator", "Homework done", "Hours slept", "Photos per listing"],
["Outcome", "Test score", "Mood", "90-day GMV"],
["What is randomised", "Who gets tutoring", "Who gets the drug", "Who gets the flow"],
["What is not", "How much homework each pupil does", "How long each person sleeps", "How many photos each seller adds"],
["The confounder of the second step", "Diligence", "Health, stress", "Experience, care"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>In both, randomising the treatment tells you how it moves the mediator, but how the mediator moves the outcome is an observational question with its own confounders.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Homework can be assigned.</strong> When the mediator can be manipulated directly, a second experiment answers the second question cleanly. Many mediators, such as trust or satisfaction, cannot.</li>
<li><strong>Both imply one path.</strong> Real treatments work through several mediators that may affect each other, and the shares need not add up neatly.</li>
<li><strong>Both suggest a constant effect.</strong> If photos help more for sellers who also got the rest of the flow, the split into direct and indirect depends on which reference you choose.</li></ul>
{tests([("Why does randomising the treatment not make the mediator–outcome relationship causal?", "<p>Randomisation balances everything between arms, but within an arm the mediator still varies for non-random reasons. The comparison of high- and low-mediator units inside an arm is observational.</p>", True)])}"""

s3 = f"""<div class="fx">total effect       = natural direct effect + natural indirect effect
                    TE  =  NDE  +  NIE

linear, no interaction (product of coefficients)
   M = α₀ + a·T + e₁            a = effect of T on M
   Y = β₀ + c′·T + b·M + e₂     b = effect of M on Y, holding T
   NIE = a × b        NDE = c′        TE = c′ + a·b

with an interaction  Y = … + d·T·M
   NDE = c′ + d·E[M | T = 0]
   NIE = (b + d) × a              (the indirect effect at T = 1)

assumptions (sequential ignorability)
   1. T is as good as random              an experiment gives this
   2. given T and X, M is as good as random   an experiment does not</div>
<ul>
<li><strong>The natural indirect effect</strong> is how much the outcome would change if treated units' mediator moved from its untreated value to its treated value, with treatment held fixed. The direct effect is everything else. {ref(1)}</li>
<li><strong>The product of coefficients</strong> (the Baron–Kenny approach) is right only for linear models without interaction, and only if the mediator–outcome link is unconfounded. {ref(3)}</li>
<li><strong>The second assumption is the hard one.</strong> It needs every confounder of mediator and outcome to be measured, and none of them may be affected by treatment.</li>
<li><strong>Testing the mediator directly</strong> by randomising it in a second experiment is the cleanest fix.</li>
<li><strong>Sensitivity analysis</strong> asks how strong mediator–outcome confounding would need to be to change the conclusion, as for any observational estimate.</li></ul>
{tests([("A colleague adjusts for 'seller engagement after onboarding' when estimating the photo effect. What is the risk?", "<p>Post-treatment engagement may itself be changed by the flow. Adjusting for it blocks part of the effect and can open collider paths. Mediator–outcome confounders must not be affected by the treatment.</p>", True),
("If the NIE is 6 and the total effect is 12, can you say photos 'explain 50%'?", "<p>Only under the assumptions, and only in the sense of this decomposition. With interactions, the shares depend on the reference level and need not add up in an obvious way.</p>")])}"""

s4 = f"""<h4>Worked: product of coefficients, then a correction</h4>
<ul><li>From the onboarding test: total effect 12, a = 1.5 photos, b = 4 per photo from the regression.</li>
<li>Naive split: NIE = 1.5 × 4 = <strong>6</strong>, NDE = 12 − 6 = <strong>6</strong>, 50% mediated.</li>
<li>A second test randomised a photo prompt alone and found 2.5 per extra photo. With b = 2.5: NIE = <strong>3.75</strong>, NDE = <strong>8.25</strong>, 31% mediated.</li></ul>
<p>The gap between 4 and 2.5 is the confounding of the mediator: careful sellers add photos and also sell more. In a simulation in which experience raises both photos and GMV, the regression recovers exactly the biased 4.0, while the total effect is estimated correctly at 12.0. Randomising the treatment protected the total and nothing else.</p>
<h4>Half-worked: an interaction</h4>
<p>Suppose photos are worth more for sellers who also got the rest of the flow: Y = c′T + 3M + 2·T·M, untreated sellers average 4 photos, a = 1.5, total effect 12. Then c′ = 12 − 2 × 4 − 5 × 1.5 = −3.5. Find the natural direct and indirect effects.</p>
{reveal("<p>NDE = c′ + d × 4 = −3.5 + 8 = <strong>4.5</strong>. NIE = (b + d) × a = 5 × 1.5 = <strong>7.5</strong>. They add to 12. The other decomposition, with the indirect effect measured at T = 0, gives 3 × 1.5 = 4.5 indirect and 7.5 direct. With an interaction, \"how much is mediated\" has two defensible answers, 37.5% and 62.5%, and the readout must say which.</p>")}
<h4>Bare: designing the evidence</h4>
<p>The team wants to know how much of the flow's effect works through faster first sales, which make sellers stay. First-sale speed cannot be assigned directly. What would you do?</p>
{reveal("<p>Find something that changes first-sale speed for new sellers without touching the other parts of the flow, such as a random boost in search ranking for a seller's first listing, and run it as its own experiment. That gives the effect of faster first sales on retention. Combine it with the onboarding test's effect on first-sale speed. If no such lever exists, measure the obvious confounders of speed and retention, estimate with them, and report a sensitivity analysis.</p>")}
<h4>Predict, then play</h4>
<p>The regression overstates the photo effect when experience drives both photos and GMV. Predict what happens to the estimated share mediated as that confounding doubles.</p>
{reveal("<p>It rises towards and past 50%, while the true share stays at 31%. The total effect does not move at all, so the error is invisible unless you test the mediator's effect separately.</p>")}
<div class="lab" data-lab="mediation"></div>
<pre class="code">import statsmodels.formula.api as smf

a = smf.ols("photos ~ treated", df).fit().params["treated"]
out = smf.ols("gmv_90d ~ treated * photos + tenure + category", df).fit()
# with an interaction, compute NDE and NIE from the coefficients and E[M | T=0],
# and bootstrap the whole procedure for intervals
# packages: statsmodels.stats.mediation.Mediation; R: mediation (Imai et al.)</pre>
{tests([("Why should intervals for the indirect effect come from the bootstrap rather than from a formula for a × b?", "<p>The product of two estimates has a skewed sampling distribution, especially when either is small, so a normal interval for it is unreliable. Bootstrapping the whole two-model procedure gives better intervals.</p>", True),
("The direct effect comes out negative. Is that a sign of an error?", "<p>Not necessarily. The flow might help through photos and hurt slightly through another path, such as more time spent before listing. But a surprising sign is worth checking for mediator–outcome confounding first.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The mediator–outcome link is unconfounded", "Experience or care drives both", "Compare with a test that randomises the mediator; sensitivity analysis"],
["No confounder of M and Y is affected by T", "The flow changes engagement, which drives both photos and GMV", "Map post-treatment variables on a causal diagram"],
["The model's form is right", "Effects are non-linear or interact", "Fit interactions; use the general NDE and NIE definitions"],
["One mediator", "Photos and descriptions both improve, and interact", "Model them together; report joint paths"],
["The mediator is measured well", "Photo count misses photo quality", "A noisy mediator understates the indirect effect"],
["Timing", "The mediator is measured after the outcome begins to move", "Measure M before Y's window"]])}
{tests([("The mediator is measured with a lot of noise. Which way does that bias the indirect effect?", "<p>Typically down: measurement error in M attenuates b, so less appears to flow through M and more is assigned to the direct effect.</p>")])}"""

s6 = f"""{table(["Approach", "Answers", "Pick it when", "Watch out"], [
["Product of coefficients", "Indirect = a × b", "Linear, no interaction, unconfounded M", "Strong assumptions; bootstrap intervals"],
["Natural effects with interaction", "NDE and NIE under a model", "Effects of M depend on T", "Two decompositions; say which"],
["Second experiment on the mediator", "Causal effect of M on Y", "M can be manipulated directly", "The manipulation may differ from how T moves M"],
["Controlled direct effect", "Effect of T with M fixed at a level", "Policy questions: what if photos were always 6?", "Not a decomposition of the total"],
["Sensitivity analysis for mediation", "How strong confounding of M and Y must be", "Any observational second step", "Needs a benchmark"],
["Front-door adjustment", "Total effect through a fully mediating, unconfounded path", "Rare: T is confounded, the path is not", "Assumptions seldom hold"]])}
{tests([("A PM asks: if every seller added six photos, how much would GMV change? Which row answers that?", "<p>Not mediation at all: it is the effect of setting the mediator, best answered by an experiment on the photo prompt, or a controlled direct and mediator effect under strong assumptions.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Free shipping raises conversion.</strong> Through lower total price, or through the badge's signal of trust?</p>
<p><strong>A recommendation model raises GMV.</strong> Through more clicks, or through better items per click?</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A loyalty programme raises retention.</strong> Through points redeemed?</p>
<p><strong>A seller course raises sales.</strong> Through better pricing?</p></div></div>
{reveal('''<p><strong>Pair 1 has mediators you can manipulate.</strong> Show the badge without the free shipping, or a price cut without the badge; change ranking to alter clicks. Separate experiments answer the mechanism directly.</p>
<p><strong>Pair 2 has self-selected mediators.</strong> Who redeems points and who reprices are choices made by the most engaged users. The product-of-coefficients answer will credit the mediator with engagement unless you test it or bound it with sensitivity analysis.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>"X% of the effect is explained by Y" from a regression after an A/B test. The test is randomised, so the result feels causal, and the analyst adds the mediator as a control and calls the drop in the treatment coefficient the mediated share. The randomisation covered the treatment only. The mediator's coefficient is as observational as any other, and decisions to cut "the unexplained part" of a product often remove what was working.</p>
{tests([("After adding 'sessions' as a control, the treatment coefficient on purchases drops from 5% to 1%. The analyst says 80% works through sessions. What do you ask?", "<p>Whether sessions are confounded with purchases by things like intent, which they almost certainly are; whether the treatment could change those confounders; and whether there is any test that moved sessions directly. Without that, 80% is an upper bound at best.</p>")])}"""

s8 = f"""<ul>
<li><strong>Ask the mechanism question before the test</strong>, and measure the mediator in a window before the outcome.</li>
<li><strong>Plan a second experiment</strong> on the mediator when it can be manipulated. It is often cheaper than a convincing observational argument.</li>
<li><strong>Adjust for pre-treatment confounders of M and Y</strong>, chosen from a causal diagram.</li>
<li><strong>Bootstrap intervals</strong> for indirect effects.</li>
<li><strong>Report the total effect first</strong>, which the experiment protects, and the split second, with its assumptions.</li>
<li><strong>Never cut features on mediation evidence alone.</strong> Test the stripped-down version.</li></ul>
{tests([("The team wants to ship only the photo nag based on a mediation analysis. What do you propose?", "<p>A three-arm test: old flow, full new flow, photo nag only. It answers the decision directly, without relying on the mediation assumptions.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is mediation analysis worth doing with observational second steps?</strong> Some methodologists say it should not be done without randomising the mediator. Others say a careful analysis with sensitivity bounds is informative and better than guessing.</li>
<li><strong>Which decomposition?</strong> With interactions, natural effects have two versions; controlled direct effects answer different questions. Fields differ in which they default to.</li>
<li><strong>Do mechanisms matter for product decisions?</strong> One view: only total effects of shippable options matter, so test those. Another: understanding the mechanism is how teams find the next good idea.</li>
<li><strong>Baron–Kenny's legacy.</strong> Its step-by-step significance tests are still widely taught, though modern work replaced them with counterfactual definitions and explicit assumptions.</li></ul>
{tests([("Make the case that a product team should rarely run mediation analysis.", "<p>Its key step is observational even inside an experiment, the assumptions are hard to defend, and the decisions it informs, such as which part of a feature to keep, can usually be tested directly with an extra arm.</p>")])}"""

rungs = [
 {"ask": "What is mediation analysis, and what does it need to be causal?", "follow": ["What are the direct and indirect effects?", "Does an A/B test make it causal?"],
  "weak": "<p>\"Add the mediator to the regression and see how much the treatment coefficient drops.\"</p>",
  "strong": "<p>It splits a total effect into the part that flows through a mediator and the rest. It needs the treatment to be as good as random, which an A/B test gives, and the mediator to be as good as random given treatment and pre-treatment covariates, which an A/B test does not give. Without the second, the indirect effect mixes the mediator's effect with whatever drives it.</p>"},
 {"ask": "A test lifted GMV by 12; treatment added 1.5 photos; regression gives 4 per photo. A photo-prompt test gives 2.5 per photo. How much flows through photos?", "follow": ["Why do the two per-photo numbers differ?", "The team wants to keep only the photo nag. Advise."],
  "model": "<p>with the regression's 4 the indirect effect is 6, half the total; with the experimental 2.5 it is 3.75, about 31%. The regression is inflated because careful sellers add more photos and sell more anyway. Most of the effect works through other parts of the flow, so dropping them would lose about 8 of the 12; test a photo-only arm before deciding.</p>",
  "weak": "<p>Reports 50% because the main test was randomised.</p>",
  "strong": "<p><b>Must have.</b> Identifies mediator–outcome confounding and uses the experimental estimate.</p><p><b>Strong signal.</b> Proposes a three-arm test to settle the product decision directly.</p>"},
 {"ask": "With an interaction between treatment and the mediator, the share mediated is 37.5% or 62.5% depending on the decomposition. Explain.", "follow": ["Which would you report?", "When does the choice not matter?"],
  "weak": "<p>\"One of the calculations must be wrong.\"</p>",
  "strong": "<p>The indirect effect can be measured holding treatment at its treated or untreated value. With an interaction, the mediator's effect differs between those, so the two decompositions differ. Report the one that matches the question, usually the indirect effect at T = 1 for \"how much of what the treatment did\", and state it. Without an interaction they coincide.</p>", "roles": ["ic"]},
 {"ask": "Design a study to find out how much of a loyalty programme's retention effect works through points redemption.", "follow": ["Can redemption be randomised?", "What would the readout look like?"],
  "weak": "<p>\"Compare redeemers with non-redeemers.\"</p>",
  "strong": "<p>Use the randomised rollout for the total effect and for the programme's effect on redemption. For redemption's effect on retention, randomise something that changes redemption alone, such as reminders or a temporary bonus on redemption, as a second test. If that is impossible, adjust for pre-programme engagement and spending, bootstrap, and add a sensitivity analysis. Report the total effect first and the split as an estimate under stated assumptions.</p>", "roles": ["lead", "ic"]},
 {"ask": "A director wants to cut 60% of a feature because an analysis showed 'only 40% of its effect' comes through the part they value. How do you respond?", "follow": ["The analysis was done inside a randomised test. Does that help?", "What would you recommend?"],
  "weak": "<p>Accepts the analysis because it came from an experiment.</p>",
  "strong": "<p>Explains that the experiment protected the total effect, not the split; the mediator was not randomised, so the 40% could be badly off in either direction. Recommends testing the cut-down version against the full one before removing anything. The cost is a few weeks, against the risk of losing an effect that the analysis may have misattributed.</p>", "roles": ["lead"]},
]

page(S, "A5", "Mediation analysis",
     "Knowing that a change worked is one question; knowing how is another. Mediation analysis splits a total effect into the part that flows through a mediator and the rest. Its second step is observational even inside an A/B test, and that is where most analyses go wrong.",
     "mediation analysis mediator direct effect indirect effect natural direct effect natural indirect effect nde nie product of coefficients baron kenny sequential ignorability controlled direct effect mechanism proportion mediated interaction",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Mediation splits a total effect into the part that flows through a mediator and the rest, but it needs the mediator's own effect on the outcome to be unconfounded, which randomising the treatment does not provide, so test the mediator directly or bound the answer with sensitivity analysis.",
     ["Total = direct + indirect", "An A/B test randomises the treatment, not the mediator", "Product of coefficients only for linear, no interaction, unconfounded", "With interaction, two decompositions", "Test the stripped-down version before cutting anything"],
     [("a5-confounding-dags", "Confounders, mediators and colliders"), ("a3-experiment-design", "Designing an A/B test"), ("b2-linear-regression", "Linear regression and its assumptions")],
     [("a5-sensitivity-falsification", "Sensitivity to hidden confounding and falsification tests"), ("c3-launch-strategy", "Launch decisions and strategy answers"), ("c3-key-drivers", "Key driver analysis")],
     sources=[("Pearl, \"Direct and Indirect Effects\", Proceedings of the 17th Conference on Uncertainty in Artificial Intelligence, 2001", "https://arxiv.org/abs/1301.2300"),
              ("Imai, Keele and Tingley, \"A General Approach to Causal Mediation Analysis\", Psychological Methods, 2010", "https://doi.org/10.1037/a0020761"),
              ("Baron and Kenny, \"The moderator–mediator variable distinction in social psychological research\", Journal of Personality and Social Psychology, 1986", "https://doi.org/10.1037/0022-3514.51.6.1173")],
     sec_roles={11: ["lead", "ic", "mle"]})
