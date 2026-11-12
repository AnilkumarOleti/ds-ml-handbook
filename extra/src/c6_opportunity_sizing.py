import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c6-opportunity-sizing"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>A PM proposes \"Make an offer\" on fixed-price listings in a category with <strong>₹1,000 crore</strong> of GMV a year. The pitch: a competitor's blog reported a 10% GMV lift, so the opportunity is <strong>₹100 crore a year</strong>. The build costs <strong>₹2 crore</strong>.</p>
<p>What you know: 40% of the category's GMV is in listings that would be eligible; 60% of buyers on those listings would see the button. Of your company's last 20 experiments on similar pricing and negotiation features, 8 won, with an average measured lift of <strong>3.0%</strong> on exposed GMV; long-term holdouts kept about <strong>60%</strong> of measured lifts.</p>
<p>Size it. Is it worth building?</p></div>
{attempt(S, 1)}{reveal(f'''<p><strong>Decompose</strong>: GMV the feature can touch = 1,000 × 40% eligible × 60% exposed = <strong>₹240 crore</strong>. The 10% applies, at most, to that, not to the whole category.</p>
<p><strong>Use your own reference class</strong>, not a competitor's headline: if it works, about 3.0% × 60% persistence = 1.8% of ₹240 crore = <strong>₹4.3 crore a year</strong>. The pitch is 23 times that.</p>
<p><strong>Allow that it may not work</strong>: 8 of 20 similar ideas won, so the expected value of the idea is 40% × ₹4.3 crore = <strong>₹1.7 crore</strong> in the first year, less than the ₹2 crore build.</p>
<p>So do not commit the full build on this sizing. A cheap prototype test, say ₹0.3 crore, that tells winners from losers raises the expected first-year value to about 0.4 × (4.3 − 2.0) − 0.3 = <strong>₹0.6 crore</strong>, and caps the downside. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>Estimating a restaurant's takings from its street.</strong> Footfall past the door, share who look in, share who come in, average bill. Each step is checkable. A claim that \"restaurants on this street make ₹1 crore a month\" skips all of them.</p>
<p><strong>A film studio's slate.</strong> Most films lose money and a few make it all back. A studio prices a new film by what similar films earned, including the flops, not by the one blockbuster everyone remembers.</p>
{table(["Idea", "Restaurant", "Film slate", "Opportunity sizing"], [
["The structure", "Footfall × look in × come in × bill", "Budget, genre, past returns", "Reach × eligibility × exposure × lift × persistence"],
["The tempting shortcut", "Someone else's takings", "The famous hit", "A competitor's headline lift"],
["The reference class", "Similar streets", "Similar films, flops included", "Your own past tests, losers included"],
["The probability of success", "Some new places close", "Most films lose", "The share of similar ideas that won"],
["The check", "Count footfall yourself", "Box office tracking", "Top-down against bottom-up"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>A credible estimate is built from checkable pieces and anchored on how similar attempts actually turned out, failures included, rather than on the most memorable success.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Footfall is observable.</strong> Many sizing inputs, such as adoption of something new, can only be borrowed from analogues.</li>
<li><strong>Films are independent.</strong> Product features interact: a new feature may take GMV from another, so lifts do not add.</li>
<li><strong>Studios release many films.</strong> A team may get one shot, which makes the downside matter more than the average.</li></ul>
{tests([("Why should the reference class include the tests that lost?", "<p>Before building, you do not know whether this idea will be a winner. Only the full set, winners and losers, gives the chance of success and the expected value.</p>", True)])}"""

s3 = f"""<div class="fx">structure (multiply checkable pieces)
   value = base × share eligible × share exposed × lift on exposed
           × persistence × (1 − cannibalisation)

for each piece: low / likely / high, with a source
   your data first, then your past experiments, then analogues

reference class of past experiments
   P(win)          share of similar tests that won
   lift if win     measured, then discounted for the winner's curse
                   and novelty (long-term holdouts)
   expected value  = P(win) × value if it works

triangulate
   top-down    from the market or category down
   bottom-up   from actions per day × value per action × incrementality
   the two should agree within a factor of about two

decide
   compare with cost, and with the value of a cheap test first</div>
<ul>
<li><strong>Structure turns a guess into several smaller guesses</strong>, each of which someone can check or challenge.</li>
<li><strong>Past experiment lifts are the best evidence</strong> for effect sizes, but measured lifts of winners overstate truth: they were selected for being large, and novelty fades. Discount with long-term holdouts or <a href="#a6-partial-pooling">shrinkage</a>. See <a href="#a4-long-term-effects">novelty effects and long-term holdouts</a>.</li>
<li><strong>Expected value includes failure.</strong> Prioritisation by \"value if it works\" favours bold claims; by expected value, it favours ideas with a decent chance.</li>
<li><strong>Ranges, not points.</strong> Combine the pieces with <a href="#c2-monte-carlo">Monte Carlo simulation</a> when the decision is close.</li>
<li><strong>Value of information.</strong> When expected value is near cost, a cheap test is often worth more than the build decision; see <a href="#c3-problem-framing">framing a decision and the value of information</a>. {ref(2)}</li></ul>
{tests([("Why apply a competitor's lift only to exposed GMV, even if you believe it?", "<p>A lift is measured on the users and transactions a feature reaches. Applying it to the whole category assumes every rupee is exposed, which inflates the result by the inverse of the exposure share.</p>", True),
("What is the difference between 'value if it works' and 'expected value'?", "<p>The first assumes success; the second multiplies by the chance of success, from the reference class. Roadmaps built on the first overpromise.</p>")])}"""

s4 = f"""<h4>Worked: the decomposition</h4>
<ul><li>Base: ₹1,000 crore category GMV a year.</li>
<li>Eligible listings: 40% → ₹400 crore. Exposed buyers: 60% → <strong>₹240 crore</strong> touched.</li>
<li>Lift if it works: 3.0% measured × 60% kept in holdouts = 1.8% → <strong>₹4.3 crore a year</strong>.</li>
<li>Chance it works: 8 of 20 → expected <strong>₹1.7 crore</strong>.</li>
<li>Range if it works: low (35% eligible, 50% exposed, 1.5% lift, half kept) ₹1.3 crore; high (45%, 70%, 4.5%, 80% kept) ₹11.3 crore.</li></ul>
<p>Even the high end is a ninth of the pitch. The pitch's errors compound: whole category instead of exposed GMV, a competitor's headline instead of your own record, and no chance of failure.</p>
<h4>Half-worked: the bottom-up check</h4>
<p>From a similar feature in another category: about 2,000 offers a day would be made, 35% accepted, average order ₹1,800, and roughly 10% of accepted offers are purchases that would not otherwise have happened. Compute the bottom-up incremental GMV a year, and compare it with the top-down ₹4.3 crore.</p>
{reveal("<p>Offer GMV: 2,000 × 0.35 × ₹1,800 × 365 = <strong>₹46 crore</strong> a year. Incremental at 10%: <strong>₹4.6 crore</strong>. That agrees with the top-down ₹4.3 crore, which is reassuring. The weakest input is the 10% incrementality: most accepted offers come from buyers who would have bought at the list price, which is exactly what an experiment would measure.</p>")}
<h4>Bare: prioritising three ideas</h4>
<p>Idea A: ₹20 crore if it works, 10% chance, ₹3 crore to build. Idea B: ₹4 crore if it works, 50% chance, ₹1 crore. Idea C: ₹8 crore if it works, 30% chance, ₹1 crore, testable with a ₹0.2 crore prototype. Rank them for a team with ₹3 crore.</p>
{reveal("<p>Expected first-year value minus cost: A ₹2 − 3 = −₹1 crore; B ₹2 − 1 = +₹1 crore; C ₹2.4 − 1 = +₹1.4 crore, and testing first gives 0.3 × (8 − 1) − 0.2 = +₹1.9 crore with the downside capped. Do C via a prototype test and B, with ₹1.8 crore left if C fails. A needs a cheaper way to learn whether it works before it competes. Values in later years would raise all three, but not change the order much.</p>")}
<h4>Predict, then play</h4>
<p>Predict how the expected value changes if long-term holdouts kept 90% of measured lifts instead of 60%, everything else unchanged.</p>
{reveal("<p>It rises by half, from ₹1.7 crore to <strong>₹2.6 crore</strong>, above the build cost. Persistence and the chance of success move the answer as much as the lift itself, which is why a team's own experiment record is the most valuable sizing input it has.</p>")}
<div class="lab" data-lab="sizing"></div>
<pre class="code">base, eligible, exposed = 1000, 0.40, 0.60          # ₹ crore a year, shares
lift_if_win, persist, p_win = 0.030, 0.60, 8 / 20   # from your experiment record
if_works = base * eligible * exposed * lift_if_win * persist
expected = p_win * if_works
round(if_works, 1), round(expected, 1)              # 4.3 and 1.7 crore a year
# bottom-up check
2000 * 0.35 * 1800 * 0.10 * 365 / 1e7               # about 4.6 crore</pre>
{tests([("Why is the long-term holdout ratio a better persistence estimate than a guess?", "<p>It is measured on your own launches: what share of test lifts was still there months later. It captures novelty fading, the winner's curse and interactions together.</p>", True),
("The team's reference class has only 5 similar past tests. What do you do?", "<p>Widen the class to related features and give it less weight, combine it with broader company averages for win rate and persistence, and widen the ranges. Say how thin the evidence is.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The base is the right base", "Lift applied to all GMV, not exposed GMV", "Check what each lift was measured on"],
["Pieces are independent", "High eligibility comes with low exposure", "Ask what would make two inputs move together"],
["Past tests resemble this one", "Different surface, audience or season", "Compare designs; weight by similarity"],
["Measured lifts are true lifts", "Winner's curse and novelty", "Holdout ratios; shrinkage"],
["No cannibalisation", "Offers replace purchases at list price", "Bottom-up incrementality; marketplace-level tests"],
["External numbers transfer", "A competitor's market or definitions differ", "Use only as a sanity check"]])}
{tests([("Two sizings of the same idea, top-down and bottom-up, differ by a factor of ten. What do you do?", "<p>Find the input that explains the gap, usually the base or the incrementality, and resolve it with data before deciding. A tenfold disagreement means at least one structure is wrong, not that the truth is the average.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Top-down decomposition", "How much value is reachable?", "Early, with category data", "Wrong base; optimistic shares"],
["Bottom-up from actions", "What will usage produce?", "Analogous features exist", "Incrementality is the hard input"],
["Reference class of past tests", "Chance of success and realistic lift", "You have an experiment record", "Small or dissimilar classes"],
["Low / likely / high", "Plausible range", "Every sizing", "Ranges too narrow"],
["Monte Carlo", "Distribution and P(clears cost)", "Close decisions", "See <a href='#c2-monte-carlo'>Monte Carlo</a>"],
["Prioritisation scores (RICE)", "Ranking many ideas", "Comparing a backlog", "Hide uncertainty; see <a href='#e2-prioritisation-capacity'>prioritisation</a>"]])}
{tests([("A backlog of 30 ideas needs ranking by Friday. Which rows, and how deep for each?", "<p>A one-line decomposition and reference-class win rate for all 30, expected value against cost to rank, then bottom-up checks and ranges for the top five only.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>A new checkout feature</strong>, sized from past checkout tests.</p>
<p><strong>A ranking change</strong>, sized from past ranking tests.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Entering a new category.</strong></p>
<p><strong>A new seller subscription tier.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 have a rich reference class.</strong> Dozens of past tests on the same surface give the win rate, the typical lift and its persistence. The sizing is mostly arithmetic.</p>
<p><strong>Pair 2 have little internal precedent.</strong> Sizing leans on market data, analogues and bottom-up assumptions, with wide ranges, and a cheap pilot to learn quickly is worth a lot.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>The sum of sizings. Each team sizes its ideas \"if they work\", on the whole base, and the planning deck adds them up to a growth number the business has never come close to. A year later, actual growth is a fraction of it. Expected values on exposed bases, discounted by the team's own record, add up to something believable.</p>
{tests([("A planning deck sums 15 sized ideas to +35% GMV. Last year's equivalent deck said +30% and the business grew 6%. What do you propose?", "<p>Re-size each idea on its exposed base with expected values from the reference class, apply the holdout discount, and check the total against last year's realised growth. Then report the forecast with a range.</p>")])}"""

s8 = f"""<ul>
<li><strong>Write the formula first</strong>, with every share explicit and a source for each.</li>
<li><strong>Keep an experiment record</strong>: every test, its area, lift, interval, and whether a holdout confirmed it. It is the best sizing asset a team has.</li>
<li><strong>Report value if it works and expected value</strong>, and the range.</li>
<li><strong>Triangulate</strong> top-down and bottom-up; resolve big gaps before deciding.</li>
<li><strong>Price a cheap test</strong> whenever expected value is near cost.</li>
<li><strong>Score sizings against outcomes</strong> a year later to calibrate the team.</li></ul>
{tests([("What would you put in a one-page sizing template?", "<p>The decision and its cost; the formula; each input with low, likely and high and a source; reference-class win rate and persistence; value if it works, expected value and range; a bottom-up check; the biggest uncertainty and the cheapest test that would resolve it.</p>")])}"""

s9 = f"""<ul>
<li><strong>Should sizings include the probability of failure?</strong> Some leaders want \"the size of the prize\" to motivate teams. Others want expected values for planning. Showing both separates ambition from forecast.</li>
<li><strong>How much to trust analogues?</strong> Competitors' published numbers are selected and defined differently; internal tests are relevant but few. Weighting them is judgement.</li>
<li><strong>Precision theatre.</strong> Detailed sizings can create false confidence. A rough order of magnitude may be all a decision needs.</li>
<li><strong>Bold bets.</strong> Expected-value thinking can starve long shots with huge upside. Portfolios often reserve a share for bets that fail most of the time.</li></ul>
{tests([("Make the case for funding Idea A (₹20 crore if it works, 10% chance, ₹3 crore cost) despite its negative first-year expected value.", "<p>Value beyond the first year may be large; it may open a new market or capability; and a portfolio needs some long shots. Better still, find a cheaper way to learn whether it works before committing ₹3 crore.</p>")])}"""

rungs = [
 {"ask": "How do you size an opportunity for a new feature?", "follow": ["Where do the effect sizes come from?", "How do you check it?"],
  "weak": "<p>\"Market size times an assumed conversion rate.\"</p>",
  "strong": "<p>Decompose: base × eligible × exposed × lift × persistence × (1 − cannibalisation), each with a range and a source. Take lifts and win rates from the team's past experiments, discounted for the winner's curse and novelty using holdouts. Report value if it works and expected value; check top-down against bottom-up; compare with cost and with the value of a cheap test.</p>"},
 {"ask": "A PM sizes 'Make an offer' at ₹100 crore: 10% of a ₹1,000 crore category. 40% is eligible, 60% exposed; your record shows 8 of 20 similar tests won at 3% with 60% persistence. Re-size it.", "follow": ["Is it worth ₹2 crore to build?", "What would you do first?"],
  "model": "<p>exposed GMV is ₹240 crore; if it works, 3% × 60% = 1.8%, about ₹4.3 crore a year; with a 40% win rate, ₹1.7 crore expected, below the ₹2 crore build. A ₹0.3 crore prototype test first gives about ₹0.6 crore expected and caps the downside. A bottom-up check, 2,000 offers a day, 35% accepted, ₹1,800 each, 10% incremental, gives ₹4.6 crore, consistent.</p>",
  "weak": "<p>Trims the 10% to 5% and keeps the rest.</p>",
  "strong": "<p><b>Must have.</b> Fixes the base, uses the internal reference class and the win rate.</p><p><b>Strong signal.</b> Triangulates bottom-up and proposes a cheap test using value of information.</p>"},
 {"ask": "Why discount past experiment lifts when using them for sizing?", "follow": ["By how much?", "How do you measure it?"],
  "weak": "<p>\"To be conservative.\"</p>",
  "strong": "<p>Lifts of tests that won are selected for being large, the winner's curse, and early readings include novelty; launches also interact. Measure the discount with long-term holdouts, the ratio of realised to summed lifts, or shrink estimates towards the reference-class mean.</p>", "roles": ["ic"]},
 {"ask": "Design a sizing process for a product org's annual planning.", "follow": ["How do you stop inflation?", "How do you learn from it?"],
  "weak": "<p>\"Each team submits its estimates.\"</p>",
  "strong": "<p>A shared template with explicit formula and sourced ranges; win rates and persistence from the experiment record; value if it works and expected value; a bottom-up check for large items; an independent analyst review of the top items; the planning total compared with realised growth in past years; sizings scored against outcomes each year to calibrate teams.</p>", "roles": ["lead", "ic"]},
 {"ask": "The CPO wants a big number for the board and asks you to present the '₹100 crore opportunity'. What do you do?", "follow": ["How do you keep ambition without overpromising?", "What slide would you make?"],
  "weak": "<p>Presents ₹100 crore with a footnote.</p>",
  "strong": "<p>Offers two numbers clearly labelled: the size of the prize, the category's ₹1,000 crore where negotiation could matter, and the realistic first-year value of this feature, about ₹4 crore if it works. Explains in one line why, and proposes a test whose result will be ready before the next board meeting. Ambition and credibility both survive.</p>", "roles": ["lead"]},
]

page(S, "C6", "Opportunity sizing with ranges and past experiment lifts",
     "A sizing is only as good as its base, its effect size and its chance of success. Decompose the value into checkable pieces, take effect sizes and win rates from your own past experiments rather than someone else's headline, and report what the idea is worth if it works and in expectation.",
     "opportunity sizing top-down bottom-up decomposition reach eligibility exposure lift persistence cannibalisation reference class past experiments win rate winner's curse expected value range triangulation prioritisation value of information",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Size an idea by multiplying checkable pieces down to the value it can actually touch, borrowing effect sizes, win rates and persistence from your own experiment record, and report both its value if it works and its expected value, checked bottom-up and compared with the cost of building it and of testing it cheaply first.",
     ["Apply lifts to exposed value, not the whole base", "Use your own experiment record", "Discount measured lifts for winners' curse and novelty", "Expected value = P(win) × value if it works", "Triangulate top-down and bottom-up"],
     [("c3-problem-framing", "Framing a decision and the value of information"), ("c2-monte-carlo", "Monte Carlo simulation for sizing and scenarios"), ("a4-long-term-effects", "Novelty effects and long-term holdouts")],
     [("c6-price-elasticity", "Price and demand elasticity"), ("e2-prioritisation-capacity", "Prioritisation and capacity"), ("c3-launch-strategy", "Launch decisions and strategy answers")],
     sources=[("Kahneman and Lovallo, \"Delusions of Success: How Optimism Undermines Executives' Decisions\", Harvard Business Review, 2003", "https://hbr.org/2003/07/delusions-of-success-how-optimism-undermines-executives-decisions"),
              ("Hubbard, How to Measure Anything, 3rd edition, Wiley, 2014", "https://www.howtomeasureanything.com/")],
     sec_roles={11: ["lead", "ic", "mle"]})
