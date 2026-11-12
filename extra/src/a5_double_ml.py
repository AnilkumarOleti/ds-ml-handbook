import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "a5-double-ml"
R = ["ic", "mle"]

s1 = f"""<div class="problem"><p>Sellers choose whether to offer free shipping. You want its effect on 90-day GMV, in ₹ thousand. You have 20,000 sellers and 20 covariates, including size, category, rating and tenure. Shipping choice and GMV both depend on those covariates in curved, interacting ways.</p>
<p>Three analysts report:</p>
<ul><li>A: free-shipping sellers average <strong>7.3</strong> more.</li>
<li>B: a linear regression of GMV on free shipping and all 20 covariates gives <strong>5.2</strong>.</li>
<li>C: a gradient-boosted model predicts GMV from free shipping and the covariates; switching free shipping on for everyone raises predictions by <strong>2.3</strong>.</li></ul>
<p>The data was simulated, so the true effect is known: <strong>2.0</strong>. Why is each one off, and what would get it right?</p></div>
{attempt(S, 1)}{reveal(f'''<p><strong>A</strong> ignores confounding: big, well-rated sellers both offer free shipping and sell more.</p>
<p><strong>B</strong> adjusts, but only for straight-line effects. The confounding is curved, so most of it survives.</p>
<p><strong>C</strong> models the curves, but a predictive model is tuned to predict GMV, not to isolate one coefficient. Regularisation shrinks and blurs the treatment's role, and nothing gives it a valid interval.</p>
<p><strong>Double/debiased machine learning</strong> uses two flexible models: one predicts GMV from the covariates, one predicts free shipping from the covariates. It then regresses the part of GMV the covariates did not predict on the part of free shipping they did not predict. With cross-fitting, it gives <strong>2.00</strong>, interval 1.84 to 2.16, here. It still assumes every confounder is among the 20 covariates. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>Judging a runner's shoes.</strong> To see whether new shoes make a runner faster, first predict each runner's time from age, training and course. Separately, predict who buys the new shoes from the same things. Then ask: among the surprises, do runners who bought the shoes unexpectedly also run unexpectedly fast?</p>
<p><strong>Grading a teacher.</strong> To credit a teacher fairly, predict each pupil's mark from their past marks and background, and predict which pupils were put in that teacher's class. A teacher who gets better-than-predicted marks from pupils they were not expected to get has shown something.</p>
{table(["Idea", "Shoes", "Teacher", "Double ML"], [
["The outcome", "Race time", "Exam mark", "GMV"],
["The treatment", "Bought the shoes", "In this class", "Offers free shipping"],
["Model 1", "Predict time from the runner", "Predict mark from the pupil", "Predict GMV from covariates"],
["Model 2", "Predict who buys the shoes", "Predict who is placed in the class", "Predict free shipping from covariates"],
["The estimate", "Do surprise buyers run surprisingly fast?", "Do unexpected pupils do unexpectedly well?", "Regress residual on residual"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Both remove what the background explains from the outcome and from the treatment, and judge the treatment only by whether its unexplained part lines up with the outcome's unexplained part.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Both assume the background is measured.</strong> A runner's motivation is not; neither is a seller's ambition. DML handles measured confounding flexibly and unmeasured confounding not at all.</li>
<li><strong>Neither says how to fit the predictions.</strong> If the same data both fits a model and is scored by it, an overfitted model explains away too much. Cross-fitting predicts each unit from a model that never saw it.</li>
<li><strong>Both imply one effect for everyone.</strong> The basic estimate is an average; heterogeneous effects need extensions such as causal forests or DR-learners.</li></ul>
{tests([("Why predict the treatment as well as the outcome? Is predicting the outcome not enough?", "<p>Predicting only the outcome leaves the bias from any error in that model. Predicting both makes the remaining bias depend on the product of the two models' errors, which is much smaller when both are reasonable.</p>")])}"""

s3 = f"""<div class="fx">partially linear model
   Y = θ·D + g(X) + ε        effect θ, any shape g
   D = m(X) + v              treatment depends on X through m

DML, partialling out
   1. split the data into K folds
   2. for each fold, fit on the other folds:
        ĝ(X) ≈ E[Y | X]     m̂(X) ≈ E[D | X]
      and predict the held-out fold        (cross-fitting)
   3. residuals   Ỹ = Y − ĝ(X)   D̃ = D − m̂(X)
   4. θ̂ = Σ D̃·Ỹ / Σ D̃²        regress Ỹ on D̃
   5. standard error from the residuals; ordinary interval

why it works: the error in θ̂ depends on
   (error in ĝ) × (error in m̂)     so each may be fairly rough</div>
<ul>
<li><strong>Neyman orthogonality.</strong> The residual-on-residual estimate barely moves when either nuisance model is slightly wrong, because the first-order effect of each error cancels. Only the product of the two errors remains. {ref(1)}</li>
<li><strong>Cross-fitting.</strong> Each unit's residual comes from models fitted without it. This stops overfitting from making the residuals artificially small and keeps the interval valid.</li>
<li><strong>Any learner can be used</strong>: gradient boosting, random forests, lasso, neural networks. Pick them by out-of-fold prediction error, as you would for any prediction task.</li>
<li><strong>Binary treatments and effects that vary</strong> use the interactive version, which is the doubly robust AIPW score from <a href="#a5-matching-propensity">matching and propensity scores</a> with cross-fitting.</li>
<li><strong>It does not fix the identification.</strong> No unmeasured confounders, overlap, and pre-treatment covariates are still needed.</li></ul>
{tests([("Why is DML said to be 'debiased'? Debiased relative to what?", "<p>Relative to plugging a regularised machine-learning model straight into the effect estimate. Regularisation and overfitting bias that plug-in; orthogonalisation and cross-fitting remove the first-order part of that bias.</p>", True),
("Your treatment model predicts free shipping with an AUC of 0.99. What problem do you expect?", "<p>Little variation in the treatment remains after removing what the covariates predict, so D̃ is tiny, the estimate rests on few units, and the interval is wide. It is the overlap problem in another form.</p>")])}"""

s4 = f"""<h4>Worked: residual on residual</h4>
<p>Six sellers, after cross-fitting. Ỹ is GMV minus its out-of-fold prediction; D̃ is free shipping minus its out-of-fold predicted probability.</p>
{table(["Seller", "Ỹ", "D̃", "Ỹ × D̃", "D̃²"], [
["1", "1.5", "0.6", "0.90", "0.36"], ["2", "−0.5", "−0.4", "0.20", "0.16"], ["3", "1.0", "0.5", "0.50", "0.25"],
["4", "−1.0", "−0.3", "0.30", "0.09"], ["5", "0.5", "0.2", "0.10", "0.04"], ["6", "−1.0", "−0.6", "0.60", "0.36"]], narrow=True)}
<p>θ̂ = 2.60 ÷ 1.26 = <strong>2.06</strong>. Seller 1 offered free shipping when it was unlikely (D̃ = 0.6) and sold 1.5 more than predicted; seller 6 did not offer it when it was likely, and sold less. Sellers whose choice was well predicted, with D̃ near zero, contribute little: the estimate is driven by the unexpected choices.</p>
<h4>Half-worked: the simulation, side by side</h4>
<p>On the full simulated data, 20,000 sellers, true effect 2.0:</p>
{table(["Estimator", "Estimate"], [
["Raw difference", "7.25"], ["Linear regression with all covariates", "5.17"], ["Boosted model of GMV, switch treatment on and off", "2.33"],
["DML, boosting for both models, 5-fold cross-fitting", "2.00 (1.84 to 2.16)"], ["DML without cross-fitting, overfitted forests", "1.95"]], narrow=True)}
<p>Explain why the linear regression is still biased with all 20 covariates in it, and why the no-cross-fitting row landing near 2 is not reassuring.</p>
{reveal("<p>The covariates enter the truth through curves, squares, thresholds and an interaction. A linear term in each removes only the linear part of the confounding; the rest stays in the treatment coefficient. The no-cross-fitting row happens to land close here, but its residuals were computed on data the forests had memorised, so its standard error has no guarantee, and on other data the bias can be large. Cross-fitting is what makes the interval honest.</p>")}
<h4>Bare: choosing the models</h4>
<p>Your outcome model explains 60% of GMV's variance out of fold, and your treatment model has an AUC of 0.70. A colleague says the models are too weak for DML to work. Respond.</p>
{reveal("<p>DML needs the product of the two errors to be small, not each to be perfect, and weak models are not a reason for bias if they capture the confounding that exists. What the colleague should worry about instead: whether the covariates include the confounders at all, and whether a better model, tuned by out-of-fold error, explains more. Try a few learners, compare the residual errors, and check that the estimate is stable across them.</p>")}
<h4>Predict, then play</h4>
<p>A confounder adds 2.5 to the raw estimate. Each model captures 80% of the confounder's effect. Predict the remaining bias with only the outcome model, and with both.</p>
{reveal("<p>About <strong>0.5</strong> with the outcome model alone (20% of 2.5), and about <strong>0.19</strong> with both, roughly 20% of 20% of the original, slightly more because removing part of the treatment's variation also shrinks the denominator. That product is the whole idea.</p>")}
<div class="lab" data-lab="dml"></div>
<pre class="code">from doubleml import DoubleMLData, DoubleMLPLR
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier

data = DoubleMLData(df, y_col="gmv_90d", d_cols="free_shipping", x_cols=covariates)
plr = DoubleMLPLR(data, ml_l=HistGradientBoostingRegressor(),   # E[Y | X]
                  ml_m=HistGradientBoostingClassifier(),        # E[D | X]
                  n_folds=5)
plr.fit()
plr.summary            # coefficient, standard error, interval</pre>
{tests([("Why is the D̃ of a seller whose choice was perfectly predictable close to zero, and what does that mean for the estimate?", "<p>If the covariates predict the choice, nothing is left over. Such sellers carry no information about the effect beyond what the covariates explain, so they get almost no weight. The estimate rests on sellers whose choice the covariates could not predict.</p>", True),
("You get 2.0 with boosting and 3.1 with lasso for the nuisance models. What do you do?", "<p>Compare their out-of-fold prediction errors. The better-predicting pair is more credible. A large gap suggests one learner misses the confounding's shape. Report the choice and the sensitivity, and consider an ensemble.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["Every confounder is in X", "Seller motivation or a competitor's pricing is missing", "Nothing in the data shows it; use sensitivity analysis"],
["X is measured before treatment", "Covariates include post-treatment GMV or reviews", "Check timestamps for every column"],
["Overlap", "Some sellers always or never offer free shipping", "Treatment predictions near 0 or 1; tiny D̃"],
["The nuisance models are good enough", "Both models miss the same strong pattern", "Out-of-fold errors; estimate unstable across learners"],
["The effect is constant (partially linear model)", "The effect varies with size or category", "Use the interactive model or a causal forest; it estimates a weighted average otherwise"],
["Units are independent", "Sellers in the same shop group or region share shocks", "Cluster the folds and the standard errors"]])}
{tests([("Under the partially linear model, if the true effect varies across sellers, what does θ̂ estimate?", "<p>A weighted average of the effects, with weights proportional to each seller's treatment variance given X. Sellers whose choice was most uncertain count most. That can differ from the average effect over all sellers.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Linear regression with controls", "Effect if confounding is linear", "Few confounders, simple relationships", "Curved confounding stays in"],
["Propensity weighting or matching", "Effect after balancing on measured X", "Binary treatment, interpretable balance", "Extreme weights; one model"],
["Doubly robust AIPW", "Effect if either model is right", "Binary treatment", "Needs cross-fitting with ML models"],
["DML, partially linear", "One effect, flexible confounding", "Continuous or binary treatment, many covariates", "Weighted average if effects vary"],
["Causal forest or DR-learner", "Effects that vary by X", "Targeting, segment questions", "Noisier; needs more data; see <a href='#a5-uplift-hte'>uplift</a>"],
["Instrumental variables", "Effect despite unmeasured confounding", "A valid instrument exists", "Strong assumptions; see <a href='#a5-instrumental-variables'>IV</a>"]])}
{tests([("When would you choose plain AIPW over DML's partially linear model?", "<p>For a binary treatment when you want the average effect over the whole population, rather than a variance-weighted average. With cross-fitted ML models, AIPW is itself a DML estimator.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Price and demand.</strong> The effect of a seller's price on units sold, with dozens of listing features.</p>
<p><strong>Discount depth.</strong> The effect of a coupon's size, which marketing set by segment.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A feature adopted by choice.</strong> Effect of using saved searches on purchases.</p>
<p><strong>An ops change.</strong> Effect of faster delivery promises, which depend on location and inventory.</p></div></div>
{reveal('''<p><strong>Pair 1 has continuous treatments</strong> set partly by rules on observed features, a natural fit for the partially linear model: residualise price and demand on the features. The price case is the classic one, an <a href="#c6-price-elasticity">elasticity</a>.</p>
<p><strong>Pair 2 has binary treatments with rich, curved confounding</strong>, suited to the interactive version (AIPW with cross-fitting). The adoption case also has an unmeasured motivation problem that no model fixes.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Reading a causal effect off a predictive model. A churn model with high accuracy has "discount received" as a feature with a negative SHAP value, and someone concludes discounts reduce churn by that amount. The model learned to predict, with regularisation and correlated features sharing credit; the number is not an effect. DML is one way to answer the causal question with the same tools. {ref(2)}</p>
{tests([("A model's SHAP value for 'received coupon' is −0.04 on churn probability. Why is that not the effect of a coupon?", "<p>Coupons were targeted, for example at at-risk users, and SHAP shares credit among correlated features to explain predictions. Neither makes it a causal effect. Estimate the effect with an experiment or a method that adjusts for the targeting.</p>")])}"""

s8 = f"""<ul>
<li><strong>Draw the causal diagram first</strong> and choose X from it. DML makes adjustment flexible; it does not decide what to adjust for.</li>
<li><strong>Tune the nuisance models on out-of-fold error</strong>, separately, and report it.</li>
<li><strong>Use five or more folds</strong>, and repeat the split a few times to see how much the estimate moves.</li>
<li><strong>Check overlap</strong> through the treatment model's predictions, and trim if needed.</li>
<li><strong>Cluster</strong> folds and standard errors when units share shocks.</li>
<li><strong>Compare with simpler estimators.</strong> If DML and linear regression agree, the confounding was linear. If they disagree, explain why before reporting either.</li></ul>
{tests([("Repeating the cross-fitting with different random splits gives estimates from 1.7 to 2.4. What do you report?", "<p>The median across splits, with a standard error that includes the split-to-split variation, as the DML literature recommends. Wide variation also suggests the nuisance models are unstable; check them.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is flexibility worth the opacity?</strong> A linear model with chosen terms is easy to explain and audit. DML is a black box twice over. Proponents answer that its only output is one coefficient with an interval, and its assumptions are the same as regression's.</li>
<li><strong>Does DML encourage throwing in every column?</strong> Easy flexible adjustment tempts analysts to include colliders and post-treatment variables. Covariate choice still needs causal reasoning.</li>
<li><strong>How large must the data be?</strong> The guarantees are asymptotic. With a few thousand units and many covariates, the nuisance errors may not be small enough, and simulations calibrated to your data are the best check.</li>
<li><strong>Which flavour?</strong> Partialling out, AIPW, targeted maximum likelihood (TMLE): they share the core idea and differ in finite-sample behaviour. Practitioners disagree on a default.</li></ul>
{tests([("Make the case for a well-specified linear regression over DML.", "<p>When the confounders are few and known, a regression with sensible terms is transparent, efficient and auditable, and stakeholders can see what was adjusted. DML adds variance and complexity for little gain when the confounding is close to linear.</p>")])}"""

rungs = [
 {"ask": "What is double/debiased machine learning, in two sentences?", "follow": ["What are the two models?", "Why cross-fit?"],
  "weak": "<p>\"Using machine learning to estimate causal effects.\"</p>",
  "strong": "<p>Fit one flexible model for the outcome and one for the treatment, both from the confounders, and estimate the effect by regressing the outcome's residual on the treatment's residual. Because the result depends on the product of the two models' errors, rough models still give an unbiased estimate with a valid interval, provided residuals are cross-fitted and all confounders are measured.</p>"},
 {"ask": "A raw comparison gives 7.3, a linear regression with all covariates 5.2, and DML 2.0. Explain the gap to a product manager.", "follow": ["Which do you believe, and why?", "What could still make 2.0 wrong?"],
  "model": "<p>the raw number credits free shipping with the fact that big, well-rated sellers choose it. The regression removes the straight-line part of that, but the real relationships are curved, so much of the bias remains. DML removes the curved part too. 2.0 is the best estimate, assuming every confounder was measured; seller ambition, if unmeasured, could still bias it.</p>",
  "weak": "<p>Picks the DML number because it uses machine learning.</p>",
  "strong": "<p><b>Must have.</b> Explains confounding and why linear adjustment leaves curved confounding behind.</p><p><b>Strong signal.</b> Names the remaining assumption, no unmeasured confounding, and proposes a sensitivity check.</p>"},
 {"ask": "Why does DML need cross-fitting, and what happens without it?", "follow": ["Is sample splitting wasteful?", "How many folds?"],
  "weak": "<p>\"To avoid overfitting.\"</p>",
  "strong": "<p>If a flexible model predicts the same data it was fitted on, its residuals are too small and correlated with the treatment's residuals in ways that bias the estimate and invalidate the standard error. Cross-fitting predicts each unit from a model that never saw it, and rotating the folds uses all the data. Five folds is common; repeat the split to check stability.</p>", "roles": ["ic", "mle"]},
 {"ask": "Design an analysis of how a seller's price affects units sold, using a year of listing data.", "follow": ["What goes in X, and what must stay out?", "How would you report it to the pricing team?"],
  "weak": "<p>\"Regress units on price.\"</p>",
  "strong": "<p>Log units and log price, a partially linear DML with X covering pre-period demand signals, category, seasonality, competition and listing quality, but not post-price outcomes such as views. Boosting for both nuisance models, cross-fitted by seller. The coefficient is an elasticity with an interval; check overlap in price variation within similar listings, cluster by seller, and compare with any price experiments.</p>", "roles": ["ic", "mle"]},
 {"ask": "A team uses DML to claim a 15% causal lift from an opt-in feature and wants to skip the experiment. Do you agree?", "follow": ["Their nuisance models are excellent. Does that settle it?", "What would make you agree?"],
  "weak": "<p>Agrees, because DML is a rigorous causal method.</p>",
  "strong": "<p>No, not on that alone. DML adjusts flexibly for measured confounders; an opt-in feature is chosen by motivated users, and motivation is rarely measured. Excellent nuisance models do not touch that. I would ask for a sensitivity analysis and a placebo outcome, and if the decision is large, a holdout or an encouragement experiment. I would agree if the feature can be launched to a random half first anyway.</p>", "roles": ["lead", "ic"]},
]

page(S, "A5", "Double/debiased machine learning",
     "Flexible models can adjust for confounding that a linear regression misses, but a model tuned to predict does not give an honest causal coefficient. DML fits one model for the outcome and one for the treatment, then regresses residual on residual, with cross-fitting, so rough models still give a valid estimate and interval.",
     "double machine learning debiased dml partialling out residual on residual neyman orthogonality cross-fitting nuisance model partially linear model aipw doubleml econml continuous treatment elasticity",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Double machine learning removes what the measured confounders predict from both the outcome and the treatment with two cross-fitted flexible models, and regresses one residual on the other, so the effect estimate and its interval stay valid even when each model is only roughly right, though it still cannot see unmeasured confounders.",
     ["Two models: outcome from X, treatment from X", "Regress the outcome's residual on the treatment's residual", "Bias depends on the product of the two models' errors", "Cross-fitting keeps the interval honest", "Unmeasured confounding is still unmeasured"],
     [("a5-matching-propensity", "Matching and propensity scores"), ("b1-validation-leakage", "Validation, cross-validation and leakage"), ("b3-gradient-boosting", "Gradient boosting")],
     [("a5-uplift-hte", "Uplift and heterogeneous effects"), ("c6-price-elasticity", "Price and demand elasticity"), ("a5-sensitivity-falsification", "Sensitivity to hidden confounding and falsification tests")],
     sources=[("Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey and Robins, \"Double/debiased machine learning for treatment and structural parameters\", The Econometrics Journal, 2018", "https://doi.org/10.1111/ectj.12097"),
              ("Bach, Chernozhukov, Kurz and Spindler, \"DoubleML: An Object-Oriented Implementation of Double Machine Learning in Python\", Journal of Machine Learning Research, 2022", "https://www.jmlr.org/papers/v23/21-0862.html")],
     sec_roles={11: ["lead", "ic", "mle"]})
