import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c4-incrementality"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>Brand search ads, the ones shown when someone types your marketplace's name, cost <strong>₹40 lakh a month</strong>. Last-click attribution credits them with <strong>8,000 orders</strong>, each worth <strong>₹800</strong> of contribution.</p>
<p>A test held back 10% of 4,000,000 eligible users from seeing the ads for a month. Exposed users converted at <strong>2.00%</strong>, held-out users at <strong>1.95%</strong>.</p>
<p>What return does attribution report? How many orders did the ads actually add, and what return is that? Keep, cut or change the spend?</p></div>
{attempt(S, 1)}{reveal('''<p><strong>Attribution:</strong> 8,000 × ₹800 = ₹64 lakh on ₹40 lakh, a return of <strong>1.6</strong>. It reports a profit of ₹24 lakh a month.</p>
<p><strong>Incrementality:</strong> the ads lifted conversion by 0.05 points across 3,600,000 exposed users: 3,600,000 × 0.0005 = <strong>1,800 orders</strong>. That is ₹14.4 lakh on ₹40 lakh, a return of <strong>0.36</strong>, and a loss of ₹25.6 lakh a month. Only 22.5% of the credited orders were caused by the ad. The rest were people who had already decided to buy and clicked the first link they saw.</p>
<p>The test's 95% interval runs from about <strong>170 to 3,430</strong> incremental orders. Break-even needs 5,000. Even the top of the range loses money, so the case for cutting is firm despite the noise.</p>
<p>Cut or sharply reduce, and keep a holdout running to watch whether competitors bidding on your name start taking the orders. eBay ran this experiment on its own brand keywords and found the ads added little. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>The rooster and the sunrise.</strong> The rooster crows every morning just before the sun comes up. Count the crows and the sunrises and the rooster looks indispensable. The test is to keep him quiet for a week.</p>
<p><strong>The greeter at the shop door.</strong> A greeter says hello to everyone who walks in. Credit each sale to the last person who spoke to the customer and the greeter is the best salesperson in the shop. He is standing where buyers pass, which is a different thing from causing them to buy.</p>
{table(["Idea", "Rooster", "Greeter", "Marketing"], [
["The credited cause", "The crow", "The greeting", "The ad click"],
["Why it looks effective", "It always comes first", "Everyone passes him", "Ads target people already on their way"],
["Attribution says", "Crows cause sunrises", "He made every sale", "The ad made every order it touched"],
["The test", "Silence him for a week", "Give him a day off", "A holdout that sees no ads"],
["Incremental effect", "None", "Some customers like being greeted", "Orders that would not have happened"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>In both, the credited cause sits on the path to the outcome without changing it, so only a comparison with a world where it is absent shows what it adds.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>The rooster has no effect at all.</strong> Most marketing has some. The question is whether the effect pays for the spend, which needs a size, not a yes or no.</li>
<li><strong>Silencing the rooster is free.</strong> Holding back ads costs the orders they would have caused, so the size of the holdout is a business decision.</li>
<li><strong>Both are one channel.</strong> A real buyer sees several ads, and channels can substitute for each other: turn off brand search and some buyers click the organic result instead, which is the point.</li></ul>
{tests([("A channel's last-click orders fall 40% when you pause it, but total orders fall 1%. What does that tell you?", "<p>Most of the credited orders moved to other paths, such as organic search or direct visits. The channel was mostly taking credit. Its incremental contribution is closer to the 1%.</p>")])}"""

s3 = f"""<div class="fx">attribution      share the credit for each order among its touches
                 (last click, linear, data-driven)
                 never says what would have happened anyway

incrementality   orders with marketing − orders without it
                 needs a comparison group:
  holdout        withhold ads from random users; compare
  geo test       switch spend by region; difference-in-differences
  mix model      sales on spend over time, with carry-over and
                 saturation; correlational, so calibrate it

incremental return (iROAS) = incremental contribution ÷ spend
                             break-even at 1
marginal return  = extra contribution from the next rupee</div>
<ul>
<li><strong>Attribution</strong> divides credit. Its numbers always add up to the orders that saw an ad, so they cannot reveal that some of those orders were going to happen anyway.</li>
<li><strong>Incrementality</strong> is the causal effect: the orders that exist because of the marketing. It needs a counterfactual, which only a comparison group provides.</li>
<li><strong>Ghost ads.</strong> In a user-level holdout, log the users who <em>would</em> have been shown an ad, in both groups. Comparing those subsets cuts the noise from users who were never in the auction. {ref(3)}</li>
<li><strong>Media mix models</strong> work on aggregate data, so they cover TV and offline channels and survive the loss of user-level tracking. They are correlational, and need experiments to calibrate them.</li>
<li><strong>Average and marginal return differ.</strong> Spend has diminishing returns. A channel can return 1.2 on average while the last ₹10 lakh returns 0.3.</li></ul>
{tests([("Why can no attribution model, however clever, measure incrementality on its own?", "<p>Attribution only sees orders that had ad touches and divides their credit. The question is how many of those orders would have happened without the touches, which is a world it never observes.</p>", True),
("Spend ₹10 lakh, incremental contribution ₹14 lakh. What is the iROAS, and is the channel profitable?", "<p>1.4, and yes on average. Whether the next rupee is profitable depends on the marginal return, which may be below 1.</p>")])}"""

s4 = f"""<h4>Worked: reading the holdout</h4>
<p>From section 1: 3,600,000 exposed at 2.00%, 400,000 held out at 1.95%.</p>
<ul><li>Lift per exposed user: 0.05 points. Incremental orders: 3,600,000 × 0.0005 = <strong>1,800</strong>.</li>
<li>Standard error of the difference: √(0.02 × 0.98 / 3,600,000 + 0.0195 × 0.9805 / 400,000) = 0.023 points. The held-out group is small, so it supplies almost all of the noise.</li>
<li>95% interval for the lift: 0.005 to 0.095 points, or <strong>170 to 3,430 orders</strong>.</li>
<li>Break-even: ₹40 lakh ÷ ₹800 = <strong>5,000 orders</strong>, a lift of 0.14 points. The whole interval is below it.</li></ul>
<p>The lift is barely distinguishable from zero, and that does not matter: the decision is whether the lift clears break-even, and it clearly does not. Compare with <a href="#a2-confidence-intervals">confidence intervals</a>: the interval against the line that matters, not against zero.</p>
<h4>Half-worked: a geo test</h4>
<p>Non-brand search is paused in ten regions for a month and left on in ten similar ones. Paused regions went from <strong>50,000</strong> orders to <strong>47,000</strong>. The others went from <strong>60,000</strong> to <strong>61,200</strong>. Spend saved in the paused regions: <strong>₹10 lakh</strong>. Each order is worth ₹800. Find the counterfactual for the paused regions, then the incremental orders and the iROAS.</p>
{reveal("<p>The other regions grew 2%, so the paused regions would have reached 51,000. They reached 47,000: the ads were adding <strong>4,000 orders</strong>, worth ₹32 lakh, for ₹10 lakh. iROAS <strong>3.2</strong>. Keep this channel. The method is <a href='#a5-diff-in-diff'>difference-in-differences</a>, and it rests on the two groups of regions moving in parallel without the change.</p>")}
<h4>Bare: average against marginal</h4>
<p>A media mix model says brand awareness ads add 6,000 orders a month at ₹40 lakh of spend, and 6,400 at ₹50 lakh. Each order is worth ₹800. Is the channel profitable? Should the budget go up to ₹50 lakh?</p>
{reveal("<p>Average return at ₹40 lakh: 6,000 × 800 / 40 lakh = <strong>1.2</strong>, profitable. The extra ₹10 lakh buys 400 orders, ₹3.2 lakh: a marginal return of <strong>0.32</strong>. Keep the channel and do not raise the budget. Trimming it below ₹40 lakh might even raise profit, which the curve below ₹40 lakh would show.</p>")}
<h4>Predict, then play</h4>
<p>The brand-search holdout used 10% of users and had about a 58% chance of detecting the true 0.05-point lift. Predict the holdout share needed for 80% power, and what that holdout costs in orders.</p>
{reveal("<p>About <strong>20%</strong>, which gives roughly 82% power. It forgoes the ads' effect on 800,000 users, about <strong>400 orders</strong> a month, worth ₹3.2 lakh, against a decision worth ₹25 lakh a month. A holdout is cheap insurance next to a wrong budget.</p>")}
<div class="lab" data-lab="holdout"></div>
<pre class="code">from statsmodels.stats.proportion import confint_proportions_2indep

exp_n, hold_n = 3_600_000, 400_000
lo, hi = confint_proportions_2indep(int(exp_n * .0200), exp_n, int(hold_n * .0195), hold_n, method="wald")
round(lo * exp_n), round(hi * exp_n)     # about 170 to 3,430 incremental orders
40e5 / 800                               # 5,000 orders to break even</pre>
{tests([("Why does a 10% holdout give a much wider interval than a 50% one with the same total traffic?", "<p>The standard error of a difference is dominated by the smaller group. Moving users into the holdout shrinks the larger term a little and the smaller term a lot.</p>", True),
("The geo test's control regions had a festival that the paused regions did not. Which way is the estimate biased?", "<p>Control regions grew faster than they otherwise would, so the counterfactual for the paused regions is too high, and the incremental effect of the ads is overstated.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The holdout really saw no ads", "Other channels, retargeting or offline media still reach held-out users", "Check exposure logs for the holdout; the measured lift is only for the channel withheld"],
["Users stay in their group", "People switch devices or log out, and the 'held-out' user sees ads on another device", "Randomise at the account level and measure leakage"],
["Regions move in parallel", "One region has a festival, a competitor's sale or a delivery outage", "Plot the pre-period; use synthetic controls"],
["The effect shows up within the test", "Brand ads build demand that converts months later", "Run longer, or measure later cohorts' purchases"],
["The test window is typical", "A test in a sale week measures a different response curve", "Repeat across seasons; calibrate a mix model with several tests"],
["Competitors stand still", "Pause brand search and a rival bids on your name", "Monitor share of the brand query in the paused group"]])}
{tests([("A one-month holdout shows a display campaign adds nothing. The brand team says its effect is long-term. How do you settle it?", "<p>Agree a longer test, or follow the held-out users' purchases for several months after the campaign. If the effect is real it should appear as a gap that opens later. Writing the measurement window down first stops the argument recurring.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Last-click attribution", "Which touch came last", "Debugging journeys, a quick sanity check", "Over-credits brand search and retargeting"],
["Multi-touch or data-driven attribution", "How to share credit among touches", "Reporting within digital channels", "Still credit, not causation"],
["User-level holdout", "The causal effect of one channel", "Digital channels you control at the user level", "Leakage across devices; costs the held-out orders"],
["Geo experiment", "The causal effect in regions", "Channels you can switch by region, including TV and offline", "Few regions, so wide intervals; needs parallel trends"],
["Media mix model", "Effect by channel from aggregate history", "Budget allocation across many channels", "Correlational; calibrate with experiments"],
["Uplift model", "Who is moved by the marketing", "Targeting coupons or ads", "Needs experimental data to train on"]])}
{tests([("You must allocate a ₹20 crore budget across eight channels next quarter. Which rows, in what combination?", "<p>A media mix model for the allocation, calibrated with geo or holdout tests on the two or three largest channels, and attribution only for day-to-day journey diagnostics.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Brand search ads.</strong> Shown to people who typed your name.</p>
<p><strong>Retargeting.</strong> Ads to people who put an item in their basket and left.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A coupon to every lapsed buyer.</strong> Redemptions are high.</p>
<p><strong>A loyalty programme.</strong> Members spend twice as much as non-members.</p></div></div>
{reveal('''<p><strong>Pair 1 targets people already on their way.</strong> Attribution looks superb because the audience was chosen for its intent. Incrementality is often small. Both deserve a standing holdout.</p>
<p><strong>Pair 2 confuses who takes the offer with what it did.</strong> Redeemers and members were the most engaged buyers to begin with. Compare against a randomly held-out group, and target the coupon at those it moves, which is <a href="#a5-uplift-hte">uplift modelling</a>.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Reporting attributed return as profit. A dashboard shows every channel above a return of 1, so the business looks like it is buying orders at a profit. Add up the attributed orders across channels and they often exceed total orders, because each channel claims the same buyer. Large field experiments have found that observational methods, even sophisticated ones, often misstate advertising effects badly. {ref(2)}</p>
{tests([("Every channel's attributed return is above 1, and total marketing spend doubled last year while orders grew 5%. What do you suspect?", "<p>Attribution is crediting the same orders several times and crediting orders that would have happened anyway. The 5% growth against doubled spend suggests a low marginal return. Ask for holdouts on the largest channels.</p>")])}"""

s8 = f"""<ul>
<li><strong>Keep a standing holdout</strong> of a few percent from all paid marketing. It is the cheapest way to know total incrementality every month.</li>
<li><strong>Decide against break-even, not against zero.</strong> A significant lift can still lose money.</li>
<li><strong>Size holdouts like experiments</strong>: the smaller group sets the precision. See <a href="#a3-sample-size-power">sample size and power</a>.</li>
<li><strong>Report average and marginal return side by side.</strong> Budgets are set at the margin.</li>
<li><strong>Calibrate the mix model with tests.</strong> Use experimental results as priors or as checks on its channel estimates.</li>
<li><strong>Agree the measurement window first</strong>, especially for brand campaigns that claim long-term effects.</li></ul>
{tests([("A standing 3% holdout from all paid marketing costs some orders. How would you justify it to the marketing head?", "<p>It turns every spend decision from an argument into a measurement. Price it: the held-out users lose the incremental effect, often a small number of orders, against budgets of crores whose effect is otherwise unknown.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is attribution worth keeping?</strong> One view: it is misleading and should be retired. The other: it is the only measure available daily and at keyword level, and it is fine for comparing keywords within a channel once the channel's incrementality is known. A common settlement is to scale attributed numbers by a factor measured in holdouts.</li>
<li><strong>Holdouts or mix models?</strong> Experiments are causal but narrow, short and costly. Mix models are broad and cheap but correlational. Most teams use both and let experiments correct the model.</li>
<li><strong>How long is long-term?</strong> Brand teams argue that awareness pays off over years, beyond any test. Sceptics reply that an unmeasurable effect is an unfalsifiable one. A defensible middle is a long, small holdout with an agreed window.</li>
<li><strong>Who owns the number?</strong> Marketing teams are often judged on attributed return, which gives them a reason to prefer it. Measurement that sits outside the spending team is harder to argue with.</li></ul>
{tests([("Make the best case for keeping last-click attribution in the weekly report.", "<p>It is available daily, at keyword and creative level, and it moves when something breaks. For comparing options inside a channel whose overall incrementality has been measured, the ranking it gives is often good enough.</p>")])}"""

rungs = [
 {"ask": "What is the difference between attribution and incrementality?", "follow": ["Can a data-driven attribution model measure incrementality?", "Which channels are most over-credited?"],
  "weak": "<p>\"Incrementality is a better attribution model.\"</p>",
  "strong": "<p>Attribution divides credit for orders that had marketing touches. Incrementality is the causal effect: orders that would not have happened without the marketing, measured against a comparison group. No attribution model sees the counterfactual. Brand search and retargeting are usually most over-credited because they reach people already intending to buy.</p>"},
 {"ask": "Last-click credits brand search with 8,000 orders a month at a cost of ₹40 lakh. A 10% holdout shows 1,800 incremental orders. Each order is worth ₹800. What do you recommend?", "follow": ["The holdout interval runs from 170 to 3,430 orders. Does that change it?", "What could go wrong if you cut brand search?"],
  "model": "<p>attributed return is 1.6; incremental return is 1,800 × 800 / 40 lakh = 0.36, a loss of about ₹25.6 lakh a month. Break-even needs 5,000 orders, above the whole interval, so cut or sharply reduce spend. Keep a holdout running to see whether competitors start bidding on the brand name and taking orders.</p>",
  "weak": "<p>Keeps the spend because attributed return is above 1, or cuts it without checking the uncertainty.</p>",
  "strong": "<p><b>Must have.</b> Computes the incremental return and compares the interval with break-even, not with zero.</p><p><b>Strong signal.</b> Names competitor bidding as the risk and proposes a monitored reduction rather than a blind cut.</p>"},
 {"ask": "Marketing wants to test TV, which cannot be targeted at users. How do you measure it?", "follow": ["You have 30 regions. Is that enough?", "How do you choose which regions get TV?"],
  "weak": "<p>\"Compare sales before and after the campaign.\"</p>",
  "strong": "<p>A geo experiment: randomise or match regions, switch TV on in some, and compare with the rest using difference-in-differences or a synthetic control. Check pre-period trends. Thirty regions give wide intervals, so run long enough, stratify by size, and use the result to calibrate a media mix model rather than as the final word.</p>", "roles": ["lead", "ic"]},
 {"ask": "Design a measurement programme for a marketplace spending ₹20 crore a quarter across eight channels.", "follow": ["How big is the standing holdout?", "How do the experiments and the mix model talk to each other?"],
  "weak": "<p>\"Buy a multi-touch attribution tool.\"</p>",
  "strong": "<p>A standing holdout of a few percent from all paid marketing for total incrementality; rotating holdout or geo tests on the largest channels each quarter; a media mix model for allocation, calibrated with those results; attribution kept for in-channel optimisation only. Decisions use marginal return against break-even, with measurement owned outside the spending team.</p>", "roles": ["lead", "ic"]},
 {"ask": "The CMO says brand search is \"non-negotiable\" and that cutting it would hand customers to competitors. Your test says it loses ₹25 lakh a month. What do you do?", "follow": ["She asks for a test that cannot fail. What do you offer?", "Who decides?"],
  "weak": "<p>Argues the numbers harder, or drops the finding.</p>",
  "strong": "<p>Treats her risk as a hypothesis worth testing: propose cutting bids in a set of regions or for a share of queries, with competitor share of the brand query and total orders as the metrics, and a rule agreed in advance. If competitors take the orders, the test shows it. The decision is hers; the cost of not testing is ₹25 lakh a month, stated in writing.</p>", "roles": ["lead"]},
]

page(S, "C4", "Incrementality, attribution and marketing mix",
     "Attribution divides the credit for orders that would often have happened anyway. This page covers how holdouts, geo experiments and media mix models measure what marketing actually adds, and how to decide against break-even.",
     "incrementality attribution last click roas iroas holdout ghost ads geo experiment media mix model mmm marketing brand search retargeting coupon marginal return saturation adstock",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Attribution shares out credit for orders that were often going to happen anyway, so the value of marketing has to be measured as incrementality against a holdout, a geo test or a calibrated mix model, and judged at the margin against break-even rather than against zero.",
     ["Attribution divides credit; incrementality needs a comparison group", "Brand search and retargeting look best and add least", "Decide against break-even, not zero", "The smaller group sets a holdout's precision", "Budgets are set by marginal, not average, return"],
     [("a2-confidence-intervals", "Confidence intervals"), ("a5-diff-in-diff", "Difference-in-differences and synthetic control"), ("c4-unit-economics", "Unit economics, LTV and CAC")],
     [("a5-uplift-hte", "Uplift and heterogeneous effects"), ("c3-launch-strategy", "Launch decisions and strategy answers"), ("a4-interference", "Interference and marketplace experiments")],
     sources=[("Blake, Nosko and Tadelis, \"Consumer Heterogeneity and Paid Search Effectiveness: A Large-Scale Field Experiment\", Econometrica, 2015", "https://doi.org/10.3982/ECTA12423"),
              ("Gordon, Zettelmeyer, Bhargava and Chapsky, \"A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook\", Marketing Science, 2019", "https://doi.org/10.1287/mksc.2018.1135"),
              ("Johnson, Lewis and Nubbemeyer, \"Ghost Ads: Improving the Economics of Measuring Online Ad Effectiveness\", Journal of Marketing Research, 2017", "https://doi.org/10.1509/jmr.15.0297")],
     sec_roles={11: ["lead", "ic", "mle"]})
