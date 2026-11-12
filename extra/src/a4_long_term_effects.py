import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "a4-long-term-effects"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>A new "picked for you" carousel on the home page ran for two weeks against the old page. The lift in items viewed per user, by day:</p>
<p><strong>Day 1: +8.0%. Day 4: +4.6%. Day 7: +3.0%. Day 10: +2.2%. Day 14: +1.8%.</strong></p>
<p>The readout says <strong>+3.5%</strong>, the average over the fourteen days, and the PM's annual plan books +3.5%. Among users who signed up during the test, and so had never seen the old page, the lift was about <strong>+1.5%</strong> on every day.</p>
<p>What is the carousel worth in the long run? What would you write in the readout?</p></div>
{attempt(S, 1)}{reveal('''<p>The daily lift is falling and flattening out, and new users, for whom nothing is new, sit at about 1.5% from the start. Both point to a <strong>novelty effect</strong> that decays towards a lasting lift of roughly <strong>+1.5%</strong>.</p>
<p>The fourteen-day average of 3.5% is <strong>2.4 times</strong> the lasting effect. Week one averaged 5.0%, week two 2.1%. Even the last week overstates it, because the decay has not finished.</p>
<p>The readout should say: the carousel is a win, worth about 1.5% at steady state, with the evidence (the daily curve and the new-user cut). Book 1.5%, and confirm it with a holdout that keeps a small share of users on the old page for a quarter.</p>''')}"""

s2 = f"""<p><strong>A new café on the high street.</strong> In the first week it has a queue round the corner. Everyone wants to try it. By the third month the queue has gone and a steady crowd of regulars is left. Judge it by opening week and you will open three more.</p>
<p><strong>A new gym membership in January.</strong> Attendance is high for three weeks, then most members settle into twice a month. The gym's revenue depends on that later number, which no January count shows.</p>
{table(["Idea", "Café", "Gym", "Product change"], [
["What you see first", "Opening queue", "January attendance", "The first week's lift"],
["Why it is inflated", "Curiosity", "Resolutions", "Users explore anything new"],
["What lasts", "Regulars", "The habit that stuck", "The steady-state lift"],
["Who shows the lasting level early", "People who moved to town this month", "Members who joined in June", "New users who never saw the old version"],
["How to measure it", "Count customers in month three", "Count visits in March", "A long run, a decay fit, or a holdout"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>In both, the first response mixes curiosity with value, and only time, or people for whom it is not new, separates the part that lasts.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Both only decay.</strong> Product changes can also grow: users who first resist a new layout learn it and use it more. That is a <strong>primacy</strong> or <strong>learning</strong> effect, and a short test understates it.</li>
<li><strong>The café sees everyone.</strong> An experiment sees only the users who arrived during the test, so heavy users dominate its first days.</li>
<li><strong>Nothing else changes in the café story.</strong> In a product, other launches, seasons and competitors move the long-run number too, which is why a holdout, not a longer test, is the clean measure.</li></ul>
{tests([("A test's lift rises from +0.5% in week one to +2% in week three. What is the likely story?", "<p>A primacy or learning effect. Users had to learn the change before it helped them. The test was too short to see the full effect, and the steady state may be higher still.</p>")])}"""

s3 = f"""<div class="fx">observed lift(t)  = lasting lift + novelty(t)
novelty(t)        → 0 as users get used to the change
                    often close to  (first lift − lasting) × e^(−t/τ)

signs of novelty     daily lift trends down
                     new users show the lasting level from day 1
                     heavy users, who saw it most, decay fastest
signs of learning    daily lift trends up; returning users gain most

long-term holdout   a small share of users kept on the old product
                    for months, across many launches
                    measures what all the launches did together
surrogate           a short-term metric that predicts the long-term one
                    well enough to decide on</div>
<ul>
<li><strong>The lift is a function of time</strong>, not one number. Plot it by day, or by days since each user's first exposure, before reading any average.</li>
<li><strong>New users are a natural control for novelty.</strong> They never saw the old version, so nothing is new to them. Their lift is a rough estimate of the lasting one, though new users differ from established users in other ways too.</li>
<li><strong>A long-term holdout</strong> answers a different question from any single test: what did this quarter's launches add, together, after novelty, interactions and cannibalisation. {ref(1)}</li>
<li><strong>Surrogates</strong> make long-term effects decidable in a short test, if a short-term metric (or a combination of several, a surrogate index) has been shown to predict the long-term outcome. {ref(2)}</li>
<li><strong>User learning</strong> can change behaviour beyond the feature itself. Google found that showing fewer, better ads raised ad clicks in the long run because users learned to trust ads more, an effect only a months-long holdout revealed. {ref(3)}</li></ul>
{tests([("Why do new users give a cleaner view of the lasting effect than returning users?", "<p>Novelty is a reaction to change. New users have no old version to compare against, so their response contains no novelty. It may still differ from the lasting effect for established users, because new users behave differently in general.</p>", True),
("A team ran twelve tests this year with lifts summing to 14%. The year-long holdout shows 5%. Name three reasons.", "<p>Novelty: tests read early, inflated lifts. The winner's curse: significant tests overstate their effects. Interactions and cannibalisation: launches compete for the same users and attention, so lifts do not add.</p>")])}"""

s4 = f"""<h4>Worked: reading a decaying lift</h4>
<p>The daily lifts in section 1 follow 1.5% + 6.5% × e^(−(day − 1)/4) closely. The pieces:</p>
<ul><li><strong>Lasting lift</strong>, the level the curve flattens to: <strong>1.5%</strong>. New users confirm it.</li>
<li><strong>Novelty at day 1</strong>: 8.0% − 1.5% = 6.5 points, decaying with a time constant of four days, a half-life of 2.8 days.</li>
<li><strong>Fourteen-day average</strong>: 3.54%. Week one 4.97%, week two 2.10%. By day 14 the curve is at 1.75%, still 0.25 points above the lasting level.</li></ul>
<p>Two practical readings follow. Report the week-two or last-days lift alongside the average, and treat the new-user lift as a floor-to-central estimate. And extend the test, or keep a holdout, when the daily curve has not flattened by the end.</p>
<h4>Half-worked: sizing a long-term holdout</h4>
<p>You have 8,000,000 active users. Orders per user per quarter average <strong>0.9</strong>, standard deviation <strong>2.4</strong>. Leadership asks for a holdout that keeps some users off every launch for a quarter. Two-sided 5%, 80% power. The 1% holdout: 80,000 users, standard error 2.4 × √(1/80,000 + 1/7,920,000) = 0.0085, so the smallest detectable change is 2.8 × 0.0085 = <strong>0.024 orders, 2.6%</strong>. Finish the 2% and 5% holdouts, and say what each costs if the quarter's launches really are worth 5%.</p>
{reveal("<p>2%: 160,000 users, detects <strong>1.9%</strong>, and forgoes 160,000 × 0.9 × 5% = <strong>7,200 orders</strong> a quarter. 5%: 400,000 users, detects <strong>1.2%</strong>, at a cost of <strong>18,000 orders</strong>. A quarter's worth of launches usually aims at several percent, so 1 to 2% is enough to see it. A 5% holdout buys precision you only need if launches are expected to add very little. The cost falls on a fixed group of users, so rotate them each quarter.</p>")}
<h4>Bare: the lifts that do not add up</h4>
<p>Twelve launches this year had lifts of 2.1, 1.4, 0.9, 1.8, 0.6, 1.2, 0.8, 1.5, 1.1, 0.7, 1.0 and 0.9%. The finance deck adds them to 14% (compounded, 14.9%). The year-long 2% holdout shows <strong>+5.0%</strong>, interval 3.1% to 6.9%. Which number goes in the plan for next year's launches, and what changes in how tests are read?</p>
{reveal("<p>The holdout's 5%: it is the only number that measures the launches together, in the long run. The gap of about 9 points is the sum of novelty, the winner's curse and overlapping launches. Plan with a discount of roughly two-thirds on summed test lifts, read each test's lift from its last week or from new users, and shrink test estimates towards a prior (see <a href='#a6-partial-pooling'>partial pooling and shrinkage</a>).</p>")}
<h4>Predict, then play</h4>
<p>The carousel's novelty has a half-life of 2.8 days. Predict how long the test must run before its overall average is within 1.5 times the lasting lift, and within 1.25 times.</p>
{reveal("<p>About <strong>six weeks</strong> (40 days) for 1.5 times, and about <strong>eleven weeks</strong> for 1.25 times, even though the novelty has a half-life under three days. The average falls slowly because the early days stay in it. Running longer is an expensive way to remove novelty. It is cheaper to read the later days or the new users, or to fit the decay.</p>")}
<div class="lab" data-lab="novelty"></div>
<pre class="code">import numpy as np
from scipy.optimize import curve_fit

day = np.arange(1, 15)
lift = np.array([8.0, 6.56, 5.44, 4.57, 3.89, 3.36, 2.95, 2.63, 2.38, 2.19, 2.03, 1.92, 1.82, 1.75])
f = lambda t, L, A, tau: L + A * np.exp(-(t - 1) / tau)
(L, A, tau), _ = curve_fit(f, day, lift, p0=[1, 5, 3])
L, tau            # about 1.5 points lasting, time constant 4 days</pre>
{tests([("Why is the fourteen-day average a poor estimate even though it uses all the data?", "<p>It estimates the average effect during the test, which includes the novelty. The decision is about the effect after the test, when the novelty is gone. More data on the wrong quantity does not help.</p>", True),
("The decay fit gives a lasting lift of 1.5% with a wide interval, 0.2% to 2.8%. What do you do?", "<p>Ship if the lower end is acceptable, and keep a small holdout to measure the steady state directly. A fitted curve extrapolates, so its interval is wider than a direct measurement's.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The lift settles to a level", "It keeps falling to zero, or reverses, as users tire of it", "The curve has not flattened by the end; extend or hold out"],
["New users show the lasting effect", "New users differ: different intent, devices, markets", "Compare new users' lift with returning users' lift late in the test"],
["The holdout stays clean", "Held-out users see launches through shared features, other devices or word of mouth", "Audit exposure; randomise at the account level"],
["The holdout represents everyone", "Users join and leave, so the holdout drifts towards old, loyal users", "Refresh the holdout each quarter; compare cohorts"],
["The surrogate predicts the long-term outcome", "The change moves the surrogate through a path that does not lead to the outcome", "Validate the surrogate on past tests with known long-term results"],
["The trend in the lift is about the change", "A sale or season starts mid-test and changes everyone's behaviour", "Compare with the control arm's own trend and with past years"]])}
{tests([("A notification test shows a lift that does not decay at all over four weeks, but unsubscribes are slowly rising in the treatment arm. What long-term risk is hidden?", "<p>Notification fatigue. Users who unsubscribe can no longer be reached, so the channel's future value shrinks. The short-term lift borrows from it. Treat unsubscribes as a guardrail and measure reachable users at the end of a holdout.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Effect by day or by exposure day", "Is the lift stable?", "Every test, as a standard chart", "Noisy with small samples"],
["New versus returning users", "How big is the lift without novelty?", "The change is visible and new users are numerous", "New users differ in other ways"],
["Decay fit", "Where will the lift settle?", "The curve is clearly flattening", "Extrapolation; wide intervals"],
["Longer test", "The effect after novelty", "The decay is quick and traffic is cheap", "Costs time; other changes pile up"],
["Long-term holdout", "What launches add together, after months", "Planning, and judging a programme of launches", "Small; drifts; costs the held-out users"],
["Surrogate index", "A long-term outcome from short-term data", "You have history linking short- and long-term metrics", "Needs validation; can be gamed"]])}
{tests([("Which rows would you use to defend a roadmap forecast to finance?", "<p>A long-term holdout for the total, and test readouts adjusted for novelty and shrinkage for the parts. A decay fit or new-user cut for any single large launch.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>A redesigned search results page.</strong> Week one +5%, then falling.</p>
<p><strong>A "new" badge on listings.</strong> Clicks on badged items jump, then fade.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A keyboard shortcut for power sellers.</strong> Use is low at first, then climbs.</p>
<p><strong>Fewer but better ads.</strong> Ad revenue falls at first, then recovers as users trust ads more.</p></div></div>
{reveal('''<p><strong>Pair 1 is novelty.</strong> Attention goes to whatever changed. The first-week lift is curiosity and fades.</p>
<p><strong>Pair 2 is learning.</strong> The value appears only after users adjust, so a short test understates it, and the second case can look like a loss. Both call for a longer view: an exposure-day chart and a holdout.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Summing test lifts into a forecast. A growth team presents a year of wins adding to 20% while the business grew 4%. Every number was measured honestly, in a two-week window, on the tests that passed. The sum counts novelty, chance and overlap as growth. Teams that keep a holdout typically find the combined effect is a fraction of the summed lifts.</p>
{tests([("Your team's tests summed to 20% last year and the company grew 4%. A VP asks whether the experimentation programme works. What do you say?", "<p>The tests may well have worked, but summed short-term lifts are the wrong measure. Propose a standing holdout to measure the programme's combined effect, and shrink future estimates. The answer to the VP should be a number from the holdout, not a defence of the sum.</p>")])}"""

s8 = f"""<ul>
<li><strong>Chart the lift by day as a standard part of every readout</strong>, with new and returning users separately.</li>
<li><strong>Run at least two full weeks</strong>, and longer for visible UI changes, which have the strongest novelty.</li>
<li><strong>Keep a standing holdout</strong> of 1 to 2% from all launches, refreshed each quarter or half, and report the combined effect against the summed lifts.</li>
<li><strong>Use the holdout's ratio to discount forecasts.</strong> If summed lifts overstate the holdout by three times, plan with a third.</li>
<li><strong>Validate surrogates on history</strong> before using them to decide long-term questions, and re-check them each year.</li>
<li><strong>Hold back the riskiest changes longer</strong>: notifications, pricing, ad load, where short-term gains can cost long-term reach or trust.</li></ul>
{tests([("Product asks to end the standing holdout because \"users in it are getting a worse product\". How do you respond?", "<p>They are, slightly, and that is the cost of knowing whether launches work. Keep it small, rotate users through it so nobody stays for long, and exempt critical fixes such as security and bugs. Without it, planning rests on numbers known to be inflated.</p>")])}"""

s9 = f"""<ul>
<li><strong>How long is long-term?</strong> A quarter catches novelty and most learning. Effects on churn, trust or seller supply can take a year. Longer holdouts cost more and drift more.</li>
<li><strong>Is a universal holdout fair to the users in it?</strong> Some teams find it unacceptable to withhold improvements. Others argue the held-out users get exactly what everyone had a quarter ago, and that rotation spreads the cost.</li>
<li><strong>Can a model replace the holdout?</strong> Surrogate indices and decay fits are cheaper and faster, but rest on assumptions a holdout does not need. Most teams use models for decisions and holdouts to check the models.</li>
<li><strong>Should the readout use the decayed or the measured effect?</strong> Reporting a fitted lasting effect invites the charge of second-guessing the data. Reporting the test average invites booking novelty as growth. Reporting both, with the reasoning, is the usual compromise.</li></ul>
{tests([("Make the case against a universal holdout.", "<p>It is small, so it detects only large combined effects. It drifts away from the active user base. It complicates every launch, and it costs revenue every day. Validated surrogates and careful readouts may give most of the answer for far less.</p>")])}"""

rungs = [
 {"ask": "What is a novelty effect, and how would you detect one?", "follow": ["What is the opposite effect called?", "Why do new users help?"],
  "weak": "<p>\"Users like new things, so run the test longer.\"</p>",
  "strong": "<p>Users react to change itself, so an early lift fades as the change becomes familiar. Detect it with the lift by day or by days since first exposure, which trends down, and with new users, who never saw the old version and show the lasting level from the start. The opposite, a primacy or learning effect, trends up.</p>"},
 {"ask": "A two-week test of a home page carousel averaged +3.5%, falling from +8% on day 1 to +1.8% on day 14. New users show +1.5% throughout. What do you report?", "follow": ["The PM says the test was positive on every day. Why not book 3.5%?", "How would you confirm the lasting effect?"],
  "model": "<p>the lift decays towards about 1.5%, which the new users confirm. The test average of 3.5% is 2.4 times that. Report a lasting lift of about 1.5%, with the daily curve and the new-user cut as evidence, and confirm it with a holdout kept on the old page for a quarter.</p>",
  "weak": "<p>Reports the 3.5% average, or calls the test unreliable and asks to rerun it.</p>",
  "strong": "<p><b>Must have.</b> Separates the decaying novelty from the lasting level and uses the new users.</p><p><b>Strong signal.</b> Proposes a holdout or decay fit, and points out that the last day still overstates the steady state.</p>"},
 {"ask": "Twelve launches had lifts summing to 14%. The year-long holdout shows 5%. Explain the gap.", "follow": ["Which of your reasons is largest, and how would you find out?", "What do you change in how tests are read?"],
  "weak": "<p>\"The holdout is too small to trust.\"</p>",
  "strong": "<p>Novelty inflates early readings; the winner's curse inflates the lifts of tests that passed; launches overlap and cannibalise each other, so lifts do not add. To split them: compare last-week lifts with test averages for novelty, shrink estimates for the winner's curse, and look for pairs of launches aimed at the same behaviour. Then discount forecasts by the holdout ratio.</p>", "roles": ["lead", "ic"]},
 {"ask": "Design how your company measures the long-term effect of product launches.", "follow": ["How big is the holdout, and how often is it refreshed?", "Which launches get a longer holdout of their own?"],
  "weak": "<p>\"Run every test for three months.\"</p>",
  "strong": "<p>Standard day-by-day and new-user charts in every readout; a standing universal holdout of 1 to 2%, sized for the combined effect a quarter of launches should produce, refreshed each quarter; dedicated longer holdouts for changes with long-term risk such as notifications, pricing and ad load; surrogate metrics validated on past tests; forecasts discounted by the holdout's ratio to summed lifts.</p>", "roles": ["lead", "ic"]},
 {"ask": "A launch that the CEO championed shows a decaying lift that is heading towards zero. The team wants to report the two-week average. What do you do?", "follow": ["The CEO asks you directly whether it worked. What do you say?", "Is there a version of this where you agree to report the average?"],
  "weak": "<p>Reports the average because it is technically correct, or calls the launch a failure in public.</p>",
  "strong": "<p>Shows the team the daily curve and the new-user cut first, so the finding is theirs before it is anyone else's. Reports both numbers, saying plainly which one predicts next quarter. Proposes a holdout to settle it. To the CEO: it produced a strong early response that is fading, the lasting effect looks small, and here is how we will know for certain by a date.</p>", "roles": ["lead"]},
]

page(S, "A4", "Novelty effects and long-term holdouts",
     "A two-week test measures the first two weeks. Users react to change itself, then settle, or learn and gain more later. This page covers reading the lift over time, using new users as a control for novelty, and the long-term holdout that measures what launches add together.",
     "novelty effect primacy learning effect long-term holdout universal holdout decay steady state new users surrogate index winner's curse cumulative impact roadmap forecast",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "A test's lift changes over time because users react to novelty and then learn, so read it by day, use new users as a control for novelty, and measure what launches add together in the long run with a small standing holdout rather than by summing short-term lifts.",
     ["Novelty decays; learning grows", "Chart the lift by day and by new versus returning users", "The test average includes the novelty", "A holdout measures launches together, in the long run", "Summed lifts overstate growth; discount by the holdout ratio"],
     [("a3-validity-checks", "Validity checks and sample ratio mismatch"), ("a3-sample-size-power", "Sample size and power"), ("a6-partial-pooling", "Partial pooling and shrinkage")],
     [("c3-launch-strategy", "Launch decisions and strategy answers"), ("a4-interference", "Interference and marketplace experiments"), ("c4-incrementality", "Incrementality, attribution and marketing mix")],
     sources=[("Kohavi, Tang and Xu, Trustworthy Online Controlled Experiments, Cambridge University Press, 2020, chapter 23", "https://experimentguide.com/"),
              ("Athey, Chetty, Imbens and Kang, \"The Surrogate Index: Combining Short-Term Proxies to Estimate Long-Term Treatment Effects\", NBER Working Paper 26463, 2019", "https://www.nber.org/papers/w26463"),
              ("Hohnhold, O'Brien and Tang, \"Focusing on the Long-term: It's Good for Users and Business\", KDD 2015", "https://doi.org/10.1145/2783258.2788583")],
     sec_roles={11: ["lead", "ic", "mle"]})
