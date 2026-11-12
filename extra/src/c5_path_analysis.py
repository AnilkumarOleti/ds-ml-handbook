import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c5-path-analysis"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>Sessions move between five pages until they buy or leave. From last month's click data, the chance of each next step:</p>
{table(["From", "Search", "Listing", "Cart", "Checkout", "Buy", "Leave"], [
["Home", "50%", "20%", "", "", "", "30%"], ["Search", "20%", "55%", "", "", "", "25%"],
["Listing", "25%", "10%", "20%", "", "", "45%"], ["Cart", "", "15%", "", "60%", "", "25%"],
["Checkout", "", "", "", "", "70%", "30%"]], narrow=True)}
<p>Two teams pitch goals for next quarter. The listing team will raise listing → cart from <strong>20% to 25%</strong>. The checkout team will raise cart → checkout from <strong>60% to 70%</strong>. Both are taken from the "leave" share. Which goal is worth more to sessions that start on the home page, and why might a funnel chart mislead you?</p></div>
{attempt(S, 1)}{reveal(f'''<p>Treat the journey as a <strong>Markov chain</strong> and compute the chance of eventually buying from the home page: <strong>6.5%</strong> today.</p>
<ul><li>Listing → cart at 25%: conversion rises to <strong>8.3%, +26%</strong>.</li>
<li>Cart → checkout at 70%: <strong>7.6%, +17%</strong>.</li></ul>
<p>The listing goal is worth more, though its change is smaller in points. Listings are visited again and again, after searches and after other listings, so a better listing page gets many chances per session; and every extra cart still passes the later steps. A funnel chart of "share reaching each step" (100% home, 54% listing, 15% cart, 9% checkout, 6.5% buy) shows where people drop, but not what a change at one step does once people loop back. {ref(1)}</p>''')}"""

s2 = f"""<p><strong>A board game with snakes and ladders.</strong> Your chance of finishing depends on every square and every arrow, including the ones that send you back. Fixing a square you land on often matters more than fixing a rare one near the end.</p>
<p><strong>Traffic through a city.</strong> A count of cars at each junction tells you where traffic is. Where to widen a road needs the flows between junctions, including the cars that circle back.</p>
{table(["Idea", "Board game", "City traffic", "User journeys"], [
["States", "Squares", "Junctions", "Pages or events"],
["Transitions", "Dice and arrows", "Turns at each junction", "Next-step probabilities"],
["Loops", "Snakes", "Circling the block", "Search → listing → search"],
["The question", "Chance of finishing", "Where to widen a road", "Chance of buying; which step to fix"],
["What a simple count misses", "How often you revisit a square", "Where cars go next", "Revisits and loops"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>In both, the outcome depends on how the pieces connect, including the paths that loop back, so the value of improving one step comes from the whole network rather than from that step's own numbers.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Dice have no memory, and neither does a basic Markov chain.</strong> Real users do: someone on their third search is less likely to buy than someone on their first. Higher-order chains or features of the path fix part of this.</li>
<li><strong>Traffic flows are physical.</strong> Journey probabilities are averages over very different users; splitting by segment often changes the picture.</li>
<li><strong>Both are fixed boards.</strong> Changing one page can change how people use the others, so a chain's \"what if\" is a model estimate, not a test result.</li></ul>
{tests([("Why can the share of sessions that ever reach the cart (15%) not be multiplied by the later rates to get conversion?", "<p>Sessions can leave the cart and come back via a listing, so a session may pass the cart step several times. The funnel shares count sessions, not passes, and the chain accounts for the loops.</p>", True)])}"""

s3 = f"""<div class="fx">Sankey diagram   width of each flow = number of sessions
                 good for showing the main paths; the long tail is hidden

sequence mining  frequent ordered patterns: "search → filter → listing → cart"
                 (PrefixSpan, SPADE); compare buyers with non-buyers

Markov chain     states, transition matrix P
   transient part Q, absorbing part R (buy, leave)
   fundamental matrix  N = (I − Q)⁻¹   expected visits to each state
   absorption          B = N · R       chance of ending in buy or leave
   what if: change a transition, recompute B
   removal effect: send a state's traffic to "leave";
                   the fall in conversion is that state's importance</div>
<ul>
<li><strong>Sankeys are for showing</strong>, not for deciding. They make the top few paths vivid and lump everything else.</li>
<li><strong>Sequence mining</strong> finds ordered patterns that distinguish groups, such as paths common among buyers and rare among abandoners. Patterns found are associations.</li>
<li><strong>Markov chains</strong> turn many journeys into a small model you can compute with: the chance of buying from any page, the expected pages per session, and the effect of changing one step.</li>
<li><strong>Removal effects</strong> are used for channel attribution: remove a channel from the chain and measure the loss. They describe the journey data, not the channel's causal effect. {ref(2)}</li>
<li><strong>Memory.</strong> A first-order chain assumes the next step depends only on the current page. Add the previous page, or the session count, as part of the state if behaviour depends on them.</li></ul>
{tests([("What does N = (I − Q)⁻¹ give you, in plain words?", "<p>For a session starting on each page, the expected number of times it visits every page before buying or leaving. Its row sums are the expected session length in pages.</p>", True),
("Removing 'search' from the chain cuts conversion by 70%. Does that mean search causes 70% of purchases?", "<p>No. It means 70% of purchase paths in the data passed through search. Without search, many users would find items another way. The removal effect is a property of observed paths, not a counterfactual.</p>")])}"""

s4 = f"""<h4>Worked: conversion from each page</h4>
<p>Solving B = (I − Q)⁻¹R for the table in section 1 gives the chance of eventually buying from each page:</p>
{table(["Starting page", "Home", "Search", "Listing", "Cart", "Checkout"], [["Chance of buying", "6.5%", "8.3%", "12.0%", "43.8%", "70.0%"]], narrow=True)}
<p>A session on the home page visits 2.9 pages on average before it ends. Cart → checkout → buy is short and strong. The weakness is the listing page: only 12% of sessions that reach a listing end up buying, and listings are where sessions spend their visits.</p>
<p>Check one value by hand: from checkout, 70% buy directly. From cart: 60% go to checkout (then 70% buy), 15% go back to a listing (then 12.0% buy): 0.6 × 0.7 + 0.15 × 0.120 = 0.420 + 0.018 = <strong>0.438</strong>.</p>
<h4>Half-worked: three goals compared</h4>
<p>Each goal moves one transition and takes the difference from \"leave\". From the home page, conversion becomes 8.3% with listing → cart at 25%; 7.6% with cart → checkout at 70%; 7.5% with checkout → buy at 80%. The checkout team says their change is the cheapest. What else do you need before ranking the goals?</p>
{reveal("<p>The chain gives the value of each change if it happens: +26%, +17%, +14%. To rank goals you also need how likely each team is to hit its target, what it costs, and whether the changes interact. Then check the model: a listing change that pushes marginal items into carts may also lower cart → checkout, which the chain holds fixed. Treat the chain as a sizing tool, and confirm with an experiment.</p>")}
<h4>Bare: the long tail</h4>
<p>The Sankey for the home page shows the top 10 paths, covering 38% of sessions. A PM concludes \"most users go home → search → listing\". What is wrong, and what would you show instead?</p>
{reveal("<p>62% of sessions follow paths outside the top 10, and the picture says nothing about them. Show the share covered on the chart itself, collapse paths into states and transitions (the Markov view covers everything), and add a sequence-mining comparison of buyers and non-buyers to find the patterns that matter.</p>")}
<h4>Predict, then play</h4>
<p>Predict whether raising checkout → buy from 70% to 90%, a big change, beats raising listing → cart from 20% to 25%.</p>
{reveal("<p>It does: checkout → buy at 90% gives 8.4%, slightly above the listing goal's 8.3%. A 20-point change at the last step is about worth a 5-point change at the listing, because only 9% of sessions reach checkout, while listings are visited by over half and revisited.</p>")}
<div class="lab" data-lab="markov"></div>
<pre class="code">import numpy as np

# transient states: home, search, listing, cart, checkout; absorbing: buy, leave
Q = np.array([[0, .50, .20, 0, 0], [0, .20, .55, 0, 0], [0, .25, .10, .20, 0],
              [0, 0, .15, 0, .60], [0, 0, 0, 0, 0]])
R = np.array([[0, .30], [0, .25], [0, .45], [0, .25], [.70, .30]])
N = np.linalg.inv(np.eye(5) - Q)      # expected visits
B = N @ R                             # chance of buy / leave from each state
B[0, 0], N[0].sum()                   # 0.065 conversion, 2.9 pages per session</pre>
{tests([("Why must every row of [Q R] sum to 1?", "<p>Each row lists every possible next step from that page, including buying and leaving, so the probabilities must cover all outcomes exactly once.</p>", True),
("Your chain is built from all sessions, but mobile users loop through search far more. What could go wrong?", "<p>The pooled chain averages two different journeys and can misstate the value of a change for both. Build chains by segment, or add the segment to the state.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["The next step depends only on the current page", "Users behave differently on their fifth search", "Compare transition rates by step number; add history to the state"],
["Transitions are stable when one changes", "A better listing page changes what people put in carts", "Experiment; watch downstream rates after launches"],
["Sessions are the right unit", "Users buy over several sessions", "Chain over users and days; include return visits"],
["Events are logged consistently", "A page fires its event twice or not at all", "Validate counts against server logs"],
["One population", "Segments have very different journeys", "Chains by device, new or returning, intent"],
["Paths are causal", "Search users are more motivated", "Treat what-ifs as sizing, then test"]])}
{tests([("Removing 'wish list' from the chain cuts conversion by 20%, yet a test that hid the wish list changed nothing. Explain.", "<p>Motivated buyers use the wish list, so many purchase paths pass through it. Hidden, those buyers took another path. The removal effect measured where buyers walk, not what the wish list causes.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["Funnel", "Share reaching each fixed step", "A linear flow such as checkout", "Ignores loops and order; see <a href='#c1-retention-funnels'>funnels in SQL</a>"],
["Sankey", "The main flows", "Showing, not deciding", "Hides the long tail"],
["Sequence mining", "Which ordered patterns differ between groups", "Finding behaviours to investigate", "Many patterns; associations only"],
["Markov chain", "Conversion from any state; what-if per step", "Sizing changes across a looping journey", "Memoryless; holds other steps fixed"],
["Removal effect", "How much traffic flows through a state", "Attribution reporting", "Not causal"],
["Survival or time-to-event", "When people convert, with censoring", "Journeys spread over days", "See <a href='#b8-survival-analysis'>survival analysis</a>"]])}
{tests([("Checkout is a fixed five-step form. Funnel or Markov chain?", "<p>A funnel. With no loops and a fixed order, the funnel's step rates multiply to the conversion rate, and it is easier to read.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Which page to improve next.</strong> Browse, search, listing, cart.</p>
<p><strong>Seller onboarding.</strong> Sign-up, verification, first listing, first sale, with sellers bouncing between steps.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Marketing channel attribution.</strong> Paid search, email, social, direct.</p>
<p><strong>Support journeys.</strong> Help article, chat, call, resolution.</p></div></div>
{reveal('''<p><strong>Pair 1 uses the chain for what-ifs.</strong> Steps loop and repeat; the chain sizes the gain from improving each step before committing a team to it.</p>
<p><strong>Pair 2 uses removal effects.</strong> They describe how much flow passes through each channel or support route. For marketing budgets, they must be checked against <a href="#c4-incrementality">incrementality</a> tests, because channels that sit on many paths may add little.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Markov attribution presented as causal. A removal-effect table credits email with 25% of conversions, and the email budget doubles. Removal effects redistribute credit along observed paths, like any attribution model. They cannot see that the people who open emails were going to buy anyway.</p>
{tests([("A Markov attribution model gives email 25% of conversions. What would you need before increasing email spend?", "<p>A holdout test: withhold email from a random group and measure the difference in conversion. That is the incremental effect, which can be far below the removal effect.</p>")])}"""

s8 = f"""<ul>
<li><strong>Define states with care</strong>: few enough to estimate well, specific enough to act on. Merge rare pages.</li>
<li><strong>Check the memory assumption</strong> by comparing transitions by step number; add history to the state if needed.</li>
<li><strong>Build chains by segment</strong> for decisions that target a segment.</li>
<li><strong>Use the chain to size, then test.</strong> The what-if is a prioritisation tool.</li>
<li><strong>Label Sankeys with coverage</strong>: \"top 10 paths, 38% of sessions\".</li>
<li><strong>Validate events</strong> before modelling paths; one double-firing event distorts every transition.</li></ul>
{tests([("How would you validate a journey chain before using it to rank roadmap items?", "<p>Simulate sessions from the chain and compare with real data: conversion, session length, share reaching each page. Then check its what-if predictions against past experiments that changed one step.</p>")])}"""

s9 = f"""<ul>
<li><strong>Markov models or machine learning?</strong> Sequence models such as RNNs or transformers predict journeys better but are harder to interrogate. Markov chains stay popular because their what-ifs are transparent.</li>
<li><strong>Is removal-effect attribution better than last-click?</strong> It spreads credit more sensibly, but shares the same flaw: it describes paths, not causes.</li>
<li><strong>Sessions or users?</strong> Session chains are simple and miss purchases that take several visits. User-level chains capture them and are harder to define.</li>
<li><strong>How many states?</strong> More states capture more behaviour and need more data per transition. There is no general answer; validate against held-out data.</li></ul>
{tests([("Make the case for a simple funnel over a Markov chain in a leadership review.", "<p>It is instantly readable, and for a mostly linear flow it gives nearly the same answer. The chain earns its place only when loops and revisits change which step is worth fixing.</p>")])}"""

rungs = [
 {"ask": "How would you analyse user paths through a product?", "follow": ["When is a Sankey enough?", "What does a Markov chain add?"],
  "weak": "<p>\"Draw a Sankey diagram.\"</p>",
  "strong": "<p>Sankeys to show the main flows, with their coverage; sequence mining to find ordered patterns that separate buyers from abandoners; and a Markov chain over pages to compute the chance of buying from any page and the value of improving each transition, accounting for loops. Then test the most valuable change, because the chain describes paths, not causes.</p>"},
 {"ask": "Listing → cart could go from 20% to 25%, or cart → checkout from 60% to 70%. Which is worth more, given this transition table?", "follow": ["Why does the smaller change win?", "What does the chain hold fixed?"],
  "model": "<p>solving the absorbing chain gives conversion from home of 6.5% today, 8.3% with the listing change (+26%) and 7.6% with the cart change (+17%). Listings are visited by most sessions and revisited, and every extra cart still flows through later steps. The chain holds other transitions fixed, so confirm with a test.</p>",
  "weak": "<p>Picks the cart change because it is bigger in points.</p>",
  "strong": "<p><b>Must have.</b> Uses absorption probabilities, not a product of funnel rates, and explains revisits.</p><p><b>Strong signal.</b> Notes that the model is a sizing tool and that changes may interact.</p>"},
 {"ask": "What is a removal effect, and why is it not a causal effect?", "follow": ["Where is it used?", "How would you get the causal number?"],
  "weak": "<p>\"It is how much conversion falls if you remove a channel.\"</p>",
  "strong": "<p>The fall in modelled conversion when a state's transitions are redirected to \"leave\". It shows how much observed flow passes through that state. Users who took that path would often have found another way, so it overstates causal importance. The causal number needs a holdout test or another causal design.</p>", "roles": ["ic"]},
 {"ask": "Design a journey analytics capability for a marketplace with web and app.", "follow": ["How do you define states?", "How do teams use it?"],
  "weak": "<p>\"A dashboard of Sankeys.\"</p>",
  "strong": "<p>A validated event layer; sessions and user-level journeys; a state taxonomy of 10 to 20 pages and actions; chains by platform and new or returning users; a what-if tool that sizes changes to any transition; sequence mining comparing buyers and non-buyers; Sankeys labelled with coverage. Every what-if used for a roadmap call is followed by a test, and the predictions are checked against results.</p>", "roles": ["lead", "ic"]},
 {"ask": "Marketing presents a Markov attribution model to justify doubling the email budget. What do you say?", "follow": ["They say it is better than last-click. Is that true?", "What would you propose?"],
  "weak": "<p>Accepts it because it is more sophisticated than last-click.</p>",
  "strong": "<p>It spreads credit more fairly than last-click, but it is still attribution: it measures paths, not what email causes. Propose a randomised email holdout for a month, with the budget decision tied to the incremental return measured there.</p>", "roles": ["lead"]},
]

page(S, "C5", "Path and sequence analysis",
     "Users do not move through a product in a straight line: they search, browse, go back and return. Sankeys show the main flows, sequence mining finds patterns that separate buyers from abandoners, and Markov chains turn journeys into a model that sizes the value of improving each step.",
     "path analysis sequence analysis user journey sankey markov chain transition matrix absorbing chain fundamental matrix removal effect markov attribution sequence mining prefixspan clickstream funnel loops",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Model user journeys as a network of steps with the chance of each next move, so the probability of buying from any page and the value of improving any step account for loops and revisits, and treat the model's what-ifs and removal effects as sizing tools to be confirmed by tests.",
     ["Sankeys show; they do not decide", "Absorbing Markov chain: B = (I − Q)⁻¹R", "Revisited steps are worth more to improve", "Removal effects describe paths, not causes", "Check memory, segments and events before trusting it"],
     [("c1-retention-funnels", "Cohort retention and funnels"), ("c1-sessions-streaks", "Sessions, streaks and gaps-and-islands"), ("a1-expectation-variance", "Expectation, variance and sums")],
     [("c4-incrementality", "Incrementality, attribution and marketing mix"), ("c5-segmentation-rfm", "Behavioural segmentation and RFM"), ("c5-activation", "Activation and aha-moment analysis")],
     sources=[("Kemeny and Snell, Finite Markov Chains, Springer, 1976, chapter 3 (absorbing chains)", "https://link.springer.com/book/9780387901923"),
              ("Anderl, Becker, von Wangenheim and Schumann, \"Mapping the customer journey: Lessons learned from graph-based online attribution modeling\", International Journal of Research in Marketing, 2016", "https://doi.org/10.1016/j.ijresmar.2016.03.001")],
     sec_roles={11: ["lead", "ic", "mle"]})
