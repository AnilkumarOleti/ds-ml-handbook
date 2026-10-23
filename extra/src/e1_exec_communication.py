import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "e1-exec-communication"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>A checkout change raised conversion from <strong>2.0% to 2.3%</strong>. The 95% interval for the lift is <strong>+0.1 to +0.5 points</strong>. The site gets <strong>3 million</strong> visitors a month, and each order is worth <strong>₹900</strong> of contribution.</p>
<p>Your draft headline for the leadership update reads: <em>"Checkout v2 drives a 15% uplift in conversion (p &lt; 0.01)."</em></p>
<p>Rewrite it in one sentence for a chief executive who will read nothing else. Which number leads, and what must the sentence contain?</p></div>
{attempt(S, 1)}{reveal('''<p>One version: <strong>"Checkout v2 adds about ₹80 lakh a month, likely between ₹27 lakh and ₹1.35 crore, and we recommend keeping it."</strong></p>
<ul><li><strong>Money first.</strong> 0.3 points × 3,000,000 visitors = 9,000 extra orders a month, × ₹900 = ₹81 lakh. The range comes from the interval: 0.1 points is ₹27 lakh, 0.5 points is ₹1.35 crore.</li>
<li><strong>"15%" is true and misleading.</strong> A relative lift sounds four times larger than the "+0.3 points" it describes, and a reader cannot turn it into money without the base rate.</li>
<li><strong>"p &lt; 0.01" answers a question nobody asked.</strong> Replace it with the range, which says how big the effect could be.</li>
<li><strong>A recommendation.</strong> A headline that only reports leaves the reader to decide what it means.</li></ul>
<p>Over a year that is about ₹9.7 crore, with a range of ₹3.2 crore to ₹16.2 crore. Use whichever period the reader plans in.</p>''')}"""

s2 = f"""<p><strong>The newspaper's inverted pyramid.</strong> A news story puts who, what and when in the first sentence, the important details in the next paragraph, and background last. An editor can cut from the bottom and the story still stands. Most readers stop after the first paragraph, and they still got the news.</p>
<p><strong>The pilot's announcement.</strong> "We have a technical issue. We are returning to the airport and will land in twenty minutes. You are safe, and the crew will brief you shortly." What is happening, what it means for you, what happens next. No talk of hydraulic pressure.</p>
{table(["Idea", "Newspaper", "Pilot", "Analytics update"], [
["First line", "The news", "What is happening", "The answer, in the reader's units"],
["Second", "Key details", "What it means for you", "Confidence and what it means for the decision"],
["Third", "Background", "What happens next", "The recommendation and the ask"],
["Left out or last", "History of the story", "Engineering detail", "Method, caveats, charts"],
["If cut short", "Still the news", "Still safe and informed", "Still a decision"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>Both are written so that the reader can stop at any point and still have what they need, which forces the conclusion to the top and the method to the bottom.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>A news reader cannot ask questions.</strong> An executive can, and will ask the ones the method section answers. Keep it ready, behind the headline.</li>
<li><strong>The pilot has authority.</strong> An analyst recommends; the reader decides. The recommendation has to carry its reasons in one line.</li>
<li><strong>Both deliver certain news.</strong> Most analytics results are ranges, which neither form was built for.</li></ul>
{tests([("A memo opens with two paragraphs on data sources and method. What is the cost?", "<p>Most readers stop before the result and leave with the impression that the work was about data, not a decision. The ones who reach the answer have spent their attention on the method first.</p>")])}"""

s3 = f"""<div class="fx">answer first   situation → complication → question → ANSWER
               then the reasons, each with its evidence

the number     absolute change, in the reader's units,
               with a range; relative change second,
               always with the base

uncertainty    a range in money, or a frequency:
               "in about 7 of 10 quarters like this one"
               words like "likely" only beside a number

charts         one message per chart, written as its title
               bars start at zero
               lie factor = change shown ÷ change in data</div>
<ul>
<li><strong>Answer first.</strong> Lead with the conclusion, then the few reasons for it, then the evidence. Situation, complication and question can set it up in a sentence each. The structure is known as the pyramid principle.</li>
<li><strong>The reader's units.</strong> A product head thinks in conversion, a finance head in contribution, an operations head in tickets or hours. Translate once, correctly.</li>
<li><strong>Absolute before relative.</strong> "+0.3 points" and "+15%" describe the same change. Relative figures inflate small effects and hide the base.</li>
<li><strong>Frequencies over percentages for risk.</strong> People reason about Bayes problems far better when given counts than when given probabilities. {ref(1)}</li>
<li><strong>Calibrated words.</strong> In surveys, readers turn "likely" into probabilities spread from little better than even to near certain. {ref(2)} Put the number next to the word.</li>
<li><strong>Lie factor.</strong> The size of an effect as drawn, divided by its size in the data. Above about 1.05 the chart exaggerates. A bar chart whose axis starts near the values is the usual culprit.</li></ul>
{tests([("Why are relative lifts especially misleading on low-baseline metrics?", "<p>The same tiny absolute change is a large share of a small base. A 0.02-point change on a 0.1% rate is a 20% lift, which sounds important and may be worth almost nothing.</p>", True),
("A chart's title is \"Conversion by week\". Rewrite it.", "<p>Write the message: \"Conversion rose after checkout v2 and has held for six weeks.\" The reader should get the point without reading the axes.</p>")])}"""

s4 = f"""<h4>Worked: from nine slides to one page</h4>
<p>The deck for checkout v2 has nine slides: context, method, sample, three charts, a segment table, caveats, next steps. The one-page version:</p>
<ol><li><strong>Headline.</strong> "Checkout v2 adds about ₹80 lakh a month; we recommend keeping it."</li>
<li><strong>Why we believe it.</strong> A four-week experiment on 3 million visitors; the lift is between +0.1 and +0.5 points, so between ₹27 lakh and ₹1.35 crore a month. No guardrail moved.</li>
<li><strong>What it means.</strong> At ₹6 lakh a month to maintain, it pays for itself across the whole range.</li>
<li><strong>What we will do.</strong> Ship to all users this week; keep a 5% holdout for a quarter.</li>
<li><strong>Appendix.</strong> Method, segments, charts. Linked, not attached.</li></ol>
<p>The deck's three charts become one, titled with its message. The segment table goes to the appendix with a note that no segment was pre-registered: see <a href="#a2-multiple-testing">multiple testing</a>.</p>
<h4>Half-worked: the truncated axis</h4>
<p>A bar chart shows conversion of 2.0% and 2.3%. Its vertical axis starts at 1.9%. How much taller does the second bar look? What is the lie factor? Then try an axis from 1.0%.</p>
{reveal("<p>From 1.9%: the bars are 0.1 and 0.4 high, so the second looks <strong>4 times</strong> taller for a change of 15%. Lie factor (4 − 1) / 0.15 = <strong>20</strong>. From 1.0%: bars of 1.0 and 1.3, a ratio of 1.3, lie factor <strong>2</strong>. From zero the factor is 1. Bars encode size by length, so they must start at zero; a dot or line chart can zoom in honestly because it encodes position.</p>")}
<h4>Bare: say the uncertainty</h4>
<p>The forecast gives a 70% chance that next quarter's GMV beats the target. Write the sentence for the board, without the word "probability".</p>
{reveal("<p>\"In about seven of ten quarters like this one we would beat the target; in the other three we would miss, most likely by under 2%.\" A frequency, plus what the bad case looks like. \"We are likely to beat the target\" will be heard as anything from slightly better than even to almost certain.</p>")}
<h4>Predict, then play</h4>
<p>Keep the lift at +0.3 points and change the baseline from 2.0% to 0.5%. Predict the relative lift and whether the money changes.</p>
{reveal("<p>The relative lift jumps from 15% to <strong>60%</strong>. The money does not move at all: still 9,000 orders and ₹81 lakh a month. The relative figure describes the base as much as the effect.</p>")}
<div class="lab" data-lab="framing"></div>
{tests([("A colleague says the one-pager hides the method. How do you answer?", "<p>The method is one link away, and every number on the page can be traced to it. The page puts the decision first because that is what the reader came for, and an appendix serves the reader who wants the rest.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "What you see", "Response"], [
["Executives want the detail", "Most want the decision and the risk", "Questions about slide 2 never reach slide 7", "Answer first; method in an appendix"],
["A precise number sounds credible", "False precision is noticed later", "\"₹81.3 lakh\" is quoted back when the actual is ₹60 lakh", "Round, and give the range"],
["Relative lifts are clearer", "They hide the base", "Two \"20% lifts\" of very different value", "Absolute change and money first"],
["Uncertainty makes you look unsure", "Hidden uncertainty discredits you at the first miss", "Every later number is discounted", "State the range plainly and still recommend"],
["One version fits every audience", "Each reader has different units", "Finance re-derives the money and gets a different figure", "One set of numbers, translated per reader, from one source"]])}
{tests([("You present ₹81 lakh a month. Three months later the holdout shows ₹55 lakh. Was the original communication wrong?", "<p>Not if it said \"about ₹80 lakh, likely between ₹27 lakh and ₹1.35 crore\". ₹55 lakh is inside the range. It was wrong if only the point estimate was given, which is why the range belongs in the headline.</p>")])}"""

s6 = f"""{table(["Format", "Pick it when", "Watch out"], [
["One-line answer in chat", "A simple question with a clear answer", "No room for the range; add it anyway"],
["One-page memo", "A decision, read before a meeting", "Takes longer to write than slides"],
["Slide deck", "A live discussion with a group", "Slides alone rarely carry the reasoning"],
["Dashboard", "Recurring monitoring", "Answers no question by itself; needs a written read-out"],
["Four-sentence readout", "Delivering an experiment result to its sponsor", "Covered in <a href='#e2-stakeholders-pushback'>stakeholders and pushback</a>"],
["Appendix or notebook", "The reader who checks the work", "Must reproduce every number in the memo"]])}
{tests([("A director asks for \"a dashboard for the checkout experiment\". What do you ask?", "<p>What decision it will inform and when. Usually a one-page result plus a small monitoring view of the holdout serves better than a dashboard that people must interpret themselves.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>A quarterly business review.</strong> Twelve metrics on a slide.</p>
<p><strong>An incident update.</strong> Checkout errors spiked for two hours.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>A forecast for the board.</strong> GMV next quarter.</p>
<p><strong>A model launch note.</strong> The new fraud model catches more counterfeits.</p></div></div>
{reveal('''<p><strong>Pair 1 needs the "so what" before the numbers.</strong> Which of the twelve moved, why, and what is being done. An incident update follows the pilot: what happened, the impact in orders or money, the cause if known, and the next update time.</p>
<p><strong>Pair 2 needs uncertainty translated.</strong> A forecast as a range and a frequency. A model launch as counterfeits stopped per day and genuine sellers wrongly blocked per day, not AUC.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>"Up 15%, statistically significant" as a headline. It combines a relative figure that inflates the effect with a significance claim that says nothing about its size, and leaves out the money and the range. It is the most common sentence in experiment readouts, and the least useful one.</p>
{tests([("Rewrite \"The new model improves AUC from 0.91 to 0.93\" for an operations head.", "<p>\"The new model stops about 1,200 more counterfeits a week at the same review workload, and wrongly blocks about 300 fewer genuine listings.\" Translate to what changes in their team's work, using the operating point.</p>")])}"""

s8 = f"""<ul>
<li><strong>Write the headline before you build the deck.</strong> If you cannot, the analysis is not finished.</li>
<li><strong>Lead with money or the reader's unit, with a range.</strong> Relative lift second, with the base.</li>
<li><strong>Title every chart with its message.</strong> Bars start at zero.</li>
<li><strong>Give risk as frequencies</strong> and put numbers beside words such as "likely".</li>
<li><strong>Send the page a day before the meeting.</strong> Use the meeting for questions and the decision.</li>
<li><strong>Keep one source of numbers</strong>, so finance, product and operations quote the same figures.</li></ul>
{tests([("Why send the memo a day before the meeting rather than presenting it live?", "<p>People read faster than you can present, and they arrive with their questions formed. The meeting is then spent on the decision instead of on catching up.</p>")])}"""

s9 = f"""<ul>
<li><strong>Memos or slides?</strong> Some companies ban slides in decision meetings and start with silent reading of a narrative memo, arguing that prose forces complete reasoning. Others find that slides suit discussion and visual data. Many settle on a short memo with a few charts.</li>
<li><strong>Should analysts recommend?</strong> Covered in <a href="#e2-stakeholders-pushback">stakeholders and pushback</a>. For communication, the point is that a headline without a recommendation pushes the hardest step onto the reader.</li>
<li><strong>How much uncertainty to show?</strong> One side says executives want a number. The other says the range is the most decision-relevant fact. Showing a central figure with a range in the same sentence satisfies both.</li>
<li><strong>Is a truncated axis ever acceptable?</strong> For line charts of a rate over time, zooming in reveals variation that matters. For bars, almost never.</li></ul>
{tests([("Make the case for a slide deck over a memo.", "<p>When the audience needs to see patterns in data together and argue about them live, charts on a screen focus the discussion, and slides are faster to update between meetings.</p>")])}"""

rungs = [
 {"ask": "How do you structure a written update for a senior executive?", "follow": ["Where does the method go?", "What if the result is uncertain?"],
  "weak": "<p>Background, then method, then results, then conclusion.</p>",
  "strong": "<p>Answer first, in the reader's units and with a range; then the few reasons and evidence; then the recommendation and the ask. Method and caveats in an appendix that reproduces every number. Uncertainty stated in the headline as a range, not hidden in a footnote.</p>"},
 {"ask": "Why lead with the absolute change in money rather than the relative lift?", "follow": ["When is the relative lift the better number?", "How do you present both?"],
  "model": "<p>relative lift depends on the base and inflates small changes on small bases; it cannot be turned into money without knowing the base and the volume. +0.3 points on 2% is \"+15%\", the same money as +0.3 points on 0.5%, which is \"+60%\". The reader decides on money. Relative lift is useful for comparing effects across products with different bases.</p>",
  "weak": "<p>\"Executives like money.\"</p>",
  "strong": "<p><b>Must have.</b> Explains how the base distorts relative figures.</p><p><b>Strong signal.</b> Gives the money with a range from the interval, and keeps the relative figure as a secondary with the base stated.</p>"},
 {"ask": "A chart in your team's deck shows bars starting at 1.9% for values of 2.0% and 2.3%. What do you say?", "follow": ["The author says it makes the change visible.", "When is zooming in acceptable?"],
  "weak": "<p>\"It looks fine.\"</p>",
  "strong": "<p>The second bar looks four times taller for a 15% change: a lie factor of 20. Bars encode length, so they start at zero. To show the change, plot the difference with its interval, or use a dot or line chart, which encode position and can be zoomed honestly.</p>"},
 {"ask": "Design how your team reports experiment results to leadership every month.", "follow": ["Twenty experiments ran this month. What goes on the page?", "How do you keep numbers consistent across teams?"],
  "weak": "<p>A dashboard of all experiments with p-values.</p>",
  "strong": "<p>A one-page summary: decisions made and their value in money with ranges, the few results that change strategy, and failed ideas with what was learned. One shared source for every number. Each experiment has a four-sentence readout linked from the page. Relative lifts appear only with bases. A quarterly holdout check reports whether shipped wins held up.</p>", "roles": ["lead"]},
 {"ask": "Your CEO wants one number for the board: \"How much did the analytics team's experiments add this year?\" What do you give her?", "follow": ["Adding up the wins gives ₹40 crore. Is that the number?", "What would make the number trustworthy?"],
  "weak": "<p>Sums the point estimates of every shipped win.</p>",
  "strong": "<p>A summed figure with a range, adjusted for the winner's curse, since selected wins shrink when re-measured; better, the measured effect of a long-running holdout that saw none of the year's launches. States which it is and why. Offers a smaller defensible number over a larger fragile one.</p>", "roles": ["lead"]},
]

page(S, "E1", "Communicating results to executives",
     "How to turn an analysis into one sentence a busy reader acts on: the answer first, in money with a range, charts that do not exaggerate, and uncertainty stated so that everyone hears the same number.",
     "communication executive memo pyramid principle answer first headline relative absolute lift money range uncertainty frequency chart lie factor truncated axis slides one pager storytelling board update",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Put the answer first, in the reader's units and with a range, follow it with the reasons and a recommendation, push method to an appendix, and never let a relative lift, a significance claim or a truncated axis stand in for the size of the effect.",
     ["The answer and recommendation come first", "Lead with absolute change in money, with a range", "Relative lifts hide the base; give it", "Uncertainty as frequencies, numbers beside words", "Bars start at zero; title charts with the message"],
     [("a2-confidence-intervals", "Confidence intervals"), ("e2-stakeholders-pushback", "Stakeholders and pushback")],
     [("c3-launch-strategy", "Launch decisions and strategy answers"), ("e2-building-team", "Building an analytics function")],
     sources=[("Gigerenzer and Hoffrage, \"How to Improve Bayesian Reasoning Without Instruction: Frequency Formats\", Psychological Review, 1995", "https://doi.org/10.1037/0033-295X.102.4.684"),
              ("Mauboussin and Mauboussin, \"If You Say Something Is 'Likely,' How Likely Do People Think It Is?\", Harvard Business Review, 2018", "https://hbr.org/2018/07/if-you-say-something-is-likely-how-likely-do-people-think-it-is")],
     sec_roles={11: ["lead", "ic", "mle"]})
