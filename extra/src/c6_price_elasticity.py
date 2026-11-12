import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c6-price-elasticity"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>A marketplace charges buyers a <strong>₹40</strong> delivery fee on 100,000 orders a day and earns <strong>₹80</strong> commission per order. Finance proposes raising the fee to <strong>₹50</strong>.</p>
<p>An analyst regresses log orders on log fee across 300 city-weeks and finds an elasticity of <strong>+0.77</strong>: \"higher fees go with more orders\". A two-week switchback test that alternated ₹40 and ₹50 by city and day finds <strong>−0.4</strong>.</p>
<p>Which elasticity do you believe? Should the fee go up?</p></div>
{attempt(S, 1)}{reveal(f'''<p><strong>Believe the test.</strong> Across cities, fees were set higher where demand was strong, so the regression mixes \"high demand\" with \"high fee\" and even gets the sign wrong. In the simulated data behind it, adding a demand index recovers −0.39. The switchback randomised the fee, so demand cannot confound it.</p>
<p><strong>Then do the arithmetic for the whole business.</strong> At −0.4, a 25% fee rise cuts orders by 1 − 1.25<sup>−0.4</sup> = <strong>8.5%</strong>, to 91,460 a day.</p>
<ul><li>Fee revenue: ₹40 lakh → <strong>₹45.7 lakh</strong> a day. Finance's view: +₹5.7 lakh.</li>
<li>Commission lost: 8,540 orders × ₹80 = <strong>₹6.8 lakh</strong>.</li>
<li>Net: <strong>−₹1.1 lakh a day</strong>.</li></ul>
<p>The fee rise loses money once lost commission is counted. It would break even only if demand were less sensitive than −0.36. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>A cinema's ticket price.</strong> On Saturdays, tickets cost more and the hall is full; on Tuesdays, cheap and empty. Plot price against attendance and higher prices seem to fill seats. The cinema set prices high on Saturdays because people come anyway.</p>
<p><strong>A café's coffee and pastries.</strong> Raising the coffee price earns more per cup and loses some customers, and each lost customer also takes a pastry sale with them.</p>
{table(["Idea", "Cinema", "Café", "Delivery fee"], [
["The price", "Ticket", "Coffee", "Delivery fee"],
["Why the raw relationship misleads", "Prices follow demand", "—", "Fees were set higher where demand was high"],
["The clean evidence", "Vary price on the same day", "Try a price for a week", "Randomised price test"],
["What else is lost", "Popcorn", "Pastries", "Commission on lost orders"],
["The decision rule", "Total takings", "Total takings", "Fee revenue plus commission, net"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Price and demand move together for reasons other than the price itself, and a price change affects everything a lost customer would have bought, so both the measurement and the decision must look past the price line alone.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>A cinema has one product.</strong> Marketplaces have thousands of sellers' prices and the platform's own fees, and buyers compare across them: cross-price effects matter.</li>
<li><strong>The café sees its customers.</strong> Online, a price rise may shift buyers to a competitor, delay the purchase, or change the basket, each with a different long-run cost.</li>
<li><strong>Both are short-run.</strong> Elasticities grow over time as buyers find alternatives; a two-week test measures the short run.</li></ul>
{tests([("Why can a regression of quantity on price across stores give a positive elasticity even when every store's customers dislike higher prices?", "<p>Stores with high demand set higher prices. Across stores, the price variation mostly reflects demand, so the regression picks up demand's effect on quantity. It is confounding, also called endogeneity.</p>", True)])}"""

s3 = f"""<div class="fx">price elasticity of demand
   ε = %Δ quantity / %Δ price  ≈  Δ ln Q / Δ ln P
   |ε| &lt; 1 inelastic: revenue from the price rises with price
   |ε| &gt; 1 elastic: revenue from the price falls with price
   constant-elasticity form  Q = Q₀ (P / P₀)^ε   (a local approximation)

cross-price elasticity
   %Δ quantity of B / %Δ price of A    (+ substitutes, − complements)

estimating it
   randomised price test (user, city, time; switchbacks)   best
   natural experiments: tax or cost changes, rule changes (IV)
   regression with controls or DML                          confounded
   conjoint or survey                                       stated, not revealed

deciding
   total contribution = (price margin + other margin per unit) × Q(P)
   profit-maximising markup  (P − MC) / P = −1 / ε   (single product)</div>
<ul>
<li><strong>Endogeneity</strong> is the central problem: prices are set by people who see demand. Only variation unrelated to demand identifies the elasticity: randomisation, or an <a href="#a5-instrumental-variables">instrument</a> such as a cost shock that moves price but not demand. {ref(2)}</li>
<li><strong>Observational methods</strong> such as <a href="#a5-double-ml">double ML</a> with rich controls can help where tests are impossible, but they still assume the confounders are measured.</li>
<li><strong>Marketplaces have several prices</strong>: sellers' item prices, buyer fees, seller fees. A change in one affects volume, and every margin earned on that volume.</li>
<li><strong>Short and long run</strong> differ: buyers learn, compare and switch. Long holdouts, or tests that persist, reveal the long-run response.</li></ul>
{tests([("Demand is inelastic at −0.4. Does that mean the platform should raise the fee?", "<p>Not on its own. Fee revenue rises, but each lost order also loses commission and possibly future purchases. Here the net effect is negative. Decide on total contribution, short and long run.</p>", True),
("Why is a switchback by city and day a good design for a delivery fee test?", "<p>Fees affect couriers and delivery times shared by everyone in a city, so user-level randomisation would interfere across arms. Alternating whole city-days avoids that, at the cost of fewer independent units; see <a href='#a4-interference'>interference</a>.</p>")])}"""

s4 = f"""<h4>Worked: from elasticity to orders</h4>
<p>A 25% fee rise with ε = −0.4: Q₁ ÷ Q₀ = 1.25<sup>−0.4</sup> = 0.9146, so orders fall <strong>8.5%</strong>. In logs: ln 0.9146 ÷ ln 1.25 = −0.089 ÷ 0.223 = −0.40. For small changes, \"1% higher price, 0.4% fewer orders\" is close enough; for 25%, use the power form.</p>
<h4>Half-worked: the full business case</h4>
<p>Net daily change = (new fee + commission) × new orders − (old fee + commission) × old orders. With ₹80 commission: at ε = −0.4, (50 + 80) × 91,461 − (40 + 80) × 100,000 = −₹1.1 lakh. Work out ε = −0.8, and the break-even elasticity.</p>
{reveal("<p>At −0.8: orders 83,651, fee revenue ₹41.8 lakh, commission lost ₹13.1 lakh, net <strong>−₹11.3 lakh a day</strong>. Break-even: 1.25<sup>ε</sup> = 120 ÷ 130, so ε = ln(0.923) ÷ ln(1.25) = <strong>−0.36</strong>. The fee rise pays only if demand is less sensitive than that. The same arithmetic shows lowering the fee to ₹30 at −0.4 would gain about ₹3.4 lakh a day, a test worth running.</p>")}
<h4>Bare: reading the observational regression</h4>
<p>Across 300 city-weeks the slope of log orders on log fee is +0.77. Adding a city demand index changes it to −0.39. A colleague asks why not just use the controlled regression and skip the test.</p>
{reveal("<p>Because the result depends on the demand index capturing everything that drove fee setting. If fees also responded to courier supply, competitor promotions or weather, those confound too, and nothing in the data says which were missed. The controlled estimate is a good prior and a check; the randomised test is what a pricing decision worth crores should rest on.</p>")}
<h4>Predict, then play</h4>
<p>Predict whether raising the fee could ever pay with ₹80 commission at ε = −0.2.</p>
{reveal("<p>Yes: −0.2 is less sensitive than the break-even −0.36. Orders fall 4.4%, fee revenue rises to ₹47.8 lakh, commission lost is ₹3.5 lakh, net about <strong>+₹4.3 lakh a day</strong>. The decision turns on where the elasticity sits relative to break-even, which is why its interval matters more than its point estimate.</p>")}
<div class="lab" data-lab="elasticity"></div>
<pre class="code">import numpy as np
import statsmodels.formula.api as smf

# switchback data: one row per city-day, fee alternated at random between 40 and 50
m = smf.ols("np.log(orders) ~ np.log(fee) + C(city) + C(weekday)", sb).fit(
        cov_type="cluster", cov_kwds={{"groups": sb.city}})
eps = m.params["np.log(fee)"]          # about -0.4, with a clustered interval
net = lambda F, e, F0=40, Q0=100_000, c=80: (F + c) * Q0 * (F / F0) ** e - (F0 + c) * Q0</pre>
{tests([("Why cluster standard errors by city in the switchback analysis?", "<p>Days within a city share unobserved conditions, so they are not independent. Treating every city-day as independent overstates precision. Cluster by city, or by the randomisation blocks.</p>", True),
("A seller-side price test shows elasticity −2.5 for one seller's item. Why is the category's elasticity much smaller?", "<p>One seller's buyers can switch to other sellers' identical items, so the seller faces very elastic demand. The category as a whole has fewer substitutes. Elasticity depends on the level at which the price changes.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["Price variation is unrelated to demand", "Prices follow demand, seasons, promotions", "Sign or size changes with controls; compare with tests"],
["Constant elasticity", "Response differs for large changes or thresholds such as 'free'", "Test several price points; look for a kink at zero"],
["Short-run equals long-run", "Buyers adapt, switch or delay", "Long holdouts; repeat-purchase effects"],
["No interference", "Shared couriers, sellers' stock, or competitor responses", "City-level or switchback designs"],
["Only this price matters", "Cross-effects on other products or fees", "Measure total basket and other margins"],
["Stated response equals behaviour", "Survey or conjoint answers", "Validate against revealed-preference tests"]])}
{tests([("A test cut the fee from ₹40 to ₹0 for some users and orders rose 30%. Can you use that to predict ₹30?", "<p>Not linearly. 'Free' has a special pull, so the jump from ₹1 to ₹0 is often larger than any other ₹1 step. Test ₹30 directly, or several points, before extrapolating.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Randomised price test", "Causal short-run elasticity", "Prices can be varied fairly and legally", "Fairness, interference, short horizon"],
["Switchback or geo test", "Elasticity with shared supply", "Fees, delivery, marketplace-wide prices", "Few units; carry-over"],
["Instrumental variable", "Elasticity from cost or tax shocks", "A shock moves price but not demand", "Instrument validity"],
["Regression or DML with controls", "Adjusted observational elasticity", "No test possible", "Unmeasured demand shifters"],
["Conjoint analysis", "Stated trade-offs, new products", "Before launch", "Hypothetical answers"],
["Cross-price test", "Substitution between items or fees", "Bundles, category pricing", "Needs larger tests"]])}
{tests([("A government raised a tax that shifted delivery fees in one state only. What can you do with it?", "<p>Use it as a natural experiment: compare that state's orders before and after with similar states, by difference-in-differences, treating the tax change as an instrument for the fee.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>A buyer delivery fee.</strong></p>
<p><strong>A seller listing fee.</strong></p></div>
<div><p class="label">Pair 2</p>
<p><strong>A premium shipping option</strong> priced above standard.</p>
<p><strong>A subscription</strong> for free delivery.</p></div></div>
{reveal('''<p><strong>Pair 1 are platform fees with knock-on margins.</strong> Each lost order or listing also loses commission and, for sellers, supply that buyers see. Decide on total contribution across both sides.</p>
<p><strong>Pair 2 involve cross-price effects.</strong> Pricing the premium option or the subscription shifts buyers between options; the question is the mix and total margin, not one option's demand curve.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Fitting a demand curve to historical prices and quantities and reading off the elasticity. The prices were chosen by people reacting to demand, so the curve is a mix of supply and demand, and can slope upwards. Economists have called this the identification problem for a century. {ref(2)}</p>
{tests([("An analyst plots monthly average price against units for a category over three years and finds a positive slope. What would you tell them?", "<p>Prices rose in high-demand months and seasons, so the plot traces demand shifts, not a demand curve. To estimate elasticity, use variation in price unrelated to demand: a test, or a cost or tax shock.</p>")])}"""

s8 = f"""<ul>
<li><strong>Test prices whenever you can</strong>, with designs that respect interference and fairness.</li>
<li><strong>Test more than one price point</strong> to see the shape, especially near thresholds such as free.</li>
<li><strong>Decide on total contribution</strong>, including other margins lost with each order, and on the break-even elasticity.</li>
<li><strong>Report the interval</strong> and where it sits against break-even.</li>
<li><strong>Watch the long run</strong> with a holdout at the old price for a while.</li>
<li><strong>Use observational elasticities as priors</strong>, with stated confounders, not as the basis for large decisions.</li></ul>
{tests([("The elasticity interval is −0.2 to −0.6 and break-even is −0.36. What do you recommend?", "<p>The data cannot tell yet whether the rise pays. Run the test longer or with more cities to narrow the interval, or test a smaller change. Do not roll out on the point estimate.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is price testing fair?</strong> Showing different prices to different buyers can feel unfair and may be regulated. Switchbacks by time and place, or testing on new users, reduce the concern; some companies avoid it entirely.</li>
<li><strong>Short-run tests, long-run decisions.</strong> A two-week test may understate how buyers adapt. Some teams keep long holdouts; others accept the risk.</li>
<li><strong>Fees or commission?</strong> Marketplaces debate who should pay, buyers or sellers. Elasticities on each side, and how each side's volume affects the other, decide it.</li>
<li><strong>Personalised pricing.</strong> Elasticities by segment invite different prices per buyer, which is profitable and contentious.</li></ul>
{tests([("Make the case against personalised delivery fees, even if elasticities differ by segment.", "<p>Buyers who learn they pay more lose trust; regulators may object; and the extra margin may be small against the risk. Uniform, simple fees with targeted promotions can capture most of the value.</p>")])}"""

rungs = [
 {"ask": "What is price elasticity, and how would you estimate it?", "follow": ["Why not regress quantity on price?", "What is break-even elasticity?"],
  "weak": "<p>\"Regress sales on price.\"</p>",
  "strong": "<p>The percentage change in quantity for a 1% change in price, often estimated as the slope in logs. Historical prices respond to demand, so a raw regression is confounded and can even be positive. Use randomised price tests, switchbacks for shared supply, or natural experiments such as cost or tax shocks as instruments; observational methods with controls only as priors.</p>"},
 {"ask": "Raising the delivery fee from ₹40 to ₹50 on 100,000 orders a day, with ₹80 commission per order and ε = −0.4. Does it pay?", "follow": ["What is the break-even elasticity?", "What about lowering the fee?"],
  "model": "<p>orders fall to 100,000 × 1.25<sup>−0.4</sup> ≈ 91,460. Fee revenue rises from ₹40 to ₹45.7 lakh a day, but 8,540 lost orders cost ₹6.8 lakh of commission: net −₹1.1 lakh a day. Break-even needs ε above −0.36. Lowering to ₹30 at −0.4 would gain about ₹3.4 lakh a day, worth testing.</p>",
  "weak": "<p>Says yes because demand is inelastic and fee revenue rises.</p>",
  "strong": "<p><b>Must have.</b> Includes lost commission and computes the net.</p><p><b>Strong signal.</b> Gives break-even elasticity and suggests testing a lower fee.</p>"},
 {"ask": "An observational regression gives +0.77, a switchback gives −0.4. Explain.", "follow": ["What would an instrument look like here?", "Why cluster in the switchback?"],
  "weak": "<p>\"The regression has too little data.\"</p>",
  "strong": "<p>Fees were set higher where demand was strong, so across city-weeks the regression measures demand's effect on orders: endogeneity. The switchback randomised the fee. An instrument would be something that moved fees without moving demand, such as a courier cost change or a tax. Cluster by city because days within a city share conditions.</p>", "roles": ["ic"]},
 {"ask": "Design a pricing study for a marketplace's buyer fees.", "follow": ["How do you handle interference and fairness?", "What is the decision rule?"],
  "weak": "<p>\"A/B test two fees on users.\"</p>",
  "strong": "<p>Switchbacks or geo tests across several fee levels including a lower one, randomised by city and time, long enough for weekly cycles; outcomes: orders, GMV, fee revenue, commission, delivery times, repeat purchase; clustered intervals; decision on total contribution with break-even elasticity; a small long-run holdout at the old fee; legal and fairness review before launch.</p>", "roles": ["lead", "ic"]},
 {"ask": "Finance wants the fee rise booked in next quarter's plan based on fee revenue alone. What do you do?", "follow": ["They say commission loss is speculative.", "What would you put in the plan?"],
  "weak": "<p>Lets the plan go through.</p>",
  "strong": "<p>Shows the net calculation with the test's elasticity, including the interval against break-even, and the case for testing a lower fee. Proposes booking only the tested net effect, or nothing until a longer test settles it. Lost commission is not speculative: it is orders that the test measured as lost.</p>", "roles": ["lead"]},
]

page(S, "C6", "Price and demand elasticity",
     "How much demand falls when price rises decides every fee, commission and price change. Historical prices follow demand, so the raw relationship misleads, sometimes with the wrong sign. Tests or natural experiments give the elasticity; the decision needs every margin that rides on each order.",
     "price elasticity demand elasticity log-log regression endogeneity identification confounding price test switchback instrumental variable cross-price elasticity substitutes complements break-even elasticity delivery fee commission markup revenue contribution",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Elasticity is the percentage change in demand per percentage change in price, but prices are set in response to demand, so estimate it from randomised or natural variation and decide on total contribution, including every margin lost with each order, against the break-even elasticity.",
     ["ε ≈ Δ ln Q / Δ ln P", "Historical prices follow demand: endogeneity", "Tests, switchbacks or instruments identify it", "Decide on total contribution, not price revenue", "Compare the interval with break-even"],
     [("a5-instrumental-variables", "Instrumental variables and regression discontinuity"), ("a4-interference", "Interference and marketplace experiments"), ("c4-unit-economics", "Unit economics, LTV and CAC")],
     [("c6-opportunity-sizing", "Opportunity sizing with ranges and past experiment lifts"), ("a5-double-ml", "Double/debiased machine learning"), ("c3-launch-strategy", "Launch decisions and strategy answers")],
     sources=[("Phillips, Pricing and Revenue Optimization, 2nd edition, Stanford University Press, 2021", "https://www.sup.org/books/business/pricing-and-revenue-optimization-second-edition"),
              ("Angrist and Pischke, Mostly Harmless Econometrics, Princeton University Press, 2009, chapter 4", "https://press.princeton.edu/books/paperback/9780691120355/mostly-harmless-econometrics")],
     sec_roles={11: ["lead", "ic", "mle"]})
