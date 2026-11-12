import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "c6-qual-quant"
R = ["lead", "ic"]

s1 = f"""<div class="problem"><p>After the new checkout launched, a product satisfaction (PSAT) survey went to 100,000 recent buyers. <strong>8%</strong> answered; average PSAT is <strong>4.39 out of 5</strong>, and the PM's slide says \"buyers love the new checkout\". UX research interviewed 12 buyers; 6 were confused by how fees are shown.</p>
<p>Joining responses to behaviour by buyer ID shows who answered:</p>
{table(["Buyer segment", "Share of buyers", "Response rate", "Share of respondents", "Mean PSAT"], [
["Heavy", "20%", "18%", "45%", "4.6"], ["Medium", "30%", "9.3%", "35%", "4.4"], ["Light", "50%", "3.2%", "20%", "3.9"]], narrow=True)}
<p>What is a fairer estimate of PSAT among all buyers? What do the 12 interviews add, and how would you size the fee problem?</p></div>
{attempt(S, 1)}{reveal(f'''<p><strong>Weight respondents back to the population.</strong> Heavy buyers answered at more than five times the rate of light buyers, and they like the product more. Weighted by segment: 0.2 × 4.6 + 0.3 × 4.4 + 0.5 × 3.9 = <strong>4.19</strong>, and the share satisfied falls from 81% to 75%. The weights cost precision: 8,000 answers carry the information of about <strong>5,000</strong>.</p>
<p>Weighting fixes only what was measured: within each segment, people who answer may still be happier than those who do not. {ref(1)}</p>
<p><strong>The interviews</strong> say what is wrong and why, which no score can. Six of twelve does not mean half of buyers; it means the problem is real and worth sizing. Size it with behaviour (drop-off at the fee step, fee-info taps, support contacts about fees) and a short in-product question to a random sample at that step. Then test a clearer fee display.</p>''')}"""

s2 = f"""<p><strong>A restaurant's comment cards.</strong> The cards come mostly from regulars who love the place and the occasional furious diner. The silent majority who found it fine and never came back leave no card. The owner who reads only cards misjudges both how good the food is and why tables are empty.</p>
<p><strong>A doctor's appointment.</strong> The patient's account of symptoms says what hurts and when; the blood test says how much and whether it is changing. Neither alone gives the diagnosis.</p>
{table(["Idea", "Comment cards", "Doctor", "Qual and quant"], [
["What people say", "Cards", "The patient's account", "Surveys, PSAT, interviews"],
["What they do", "Who returns", "Blood test, scans", "Behavioural data"],
["Who speaks", "Regulars and the furious", "The patient who came in", "Respondents, not everyone"],
["What words give", "Reasons", "Where it hurts", "Why, and what to change"],
["What numbers give", "How many come back", "How much, how fast", "How many, how much it costs"]])}
<p>What do the two share? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>What people say explains why but comes from those who chose to speak, and what they do shows how much and for whom, so each corrects the other.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Comment cards cannot be weighted.</strong> Linked surveys can: when responses join to behaviour, you know who did not answer.</li>
<li><strong>A patient is one person.</strong> Twelve interviews are twelve people chosen by a recruiter, which shows what exists, not how common it is.</li>
<li><strong>Doctors order the right test.</strong> Analytics often has only the data that happened to be logged; qual research may reveal what should have been.</li></ul>
{tests([("Why can twelve interviews establish that a problem exists but not how common it is?", "<p>Twelve people chosen for availability or fit are not a random sample, and twelve is too few to estimate a share. One clear case shows the problem is possible; behaviour or a random survey sizes it.</p>", True)])}"""

s3 = f"""<div class="fx">join what people say to what they do (by user ID, consented)
   survey responses  + behaviour before and after the survey

non-response
   compare respondents with everyone on behaviour you have
   weight respondents to the population (post-stratification, raking)
   cost: effective sample size  n_eff = (Σw)² / Σw²
   still assumes respondents resemble non-respondents within cells

stated vs revealed
   check what people say against what they do
   ("price is why I left" vs. response to a price change)

sequence
   qual finds what and why  →  quant sizes how many and how much
   →  experiment tests whether changing it helps  →  qual explains surprises

PSAT, CSAT, NPS: link to retention and spend to learn what a point is worth</div>
<ul>
<li><strong>Linking is the key move.</strong> A survey joined to behaviour reveals who answered, lets you weight, and lets you ask whether satisfaction predicts what people later do.</li>
<li><strong>Sampling decides validity</strong> more than sample size: triggered surveys after support contacts reach unhappy users; surveys in a newsletter reach engaged ones. Random sampling from the population of interest is the default.</li>
<li><strong>Weighting</strong> corrects for measured differences and shrinks the effective sample. {ref(2)} It cannot correct for differences you did not measure.</li>
<li><strong>Stated reasons</strong> are hypotheses about behaviour. People explain their choices with reasons that sound sensible, not always the ones that drove them.</li>
<li><strong>Qual and quant are a loop</strong>: interviews suggest what to measure, data sizes it, experiments test it, and interviews explain surprising results.</li></ul>
{tests([("Why does weighting reduce the effective sample size?", "<p>A few respondents with large weights count for many people, so their individual noise counts many times. The estimate behaves as if it came from fewer, equally weighted respondents.</p>", True),
("A satisfaction survey is triggered only after a support chat. What will it measure?", "<p>Satisfaction among buyers who had a problem and contacted support, a very different group from buyers overall. Useful for support quality; misleading as a product-wide score.</p>")])}"""

s4 = f"""<h4>Worked: weighting PSAT</h4>
<ul><li>Response rates: heavy 18%, medium 9.3%, light 3.2%; overall 8%. Respondent shares: 45%, 35%, 20%.</li>
<li>Unweighted mean: 0.45 × 4.6 + 0.35 × 4.4 + 0.20 × 3.9 = <strong>4.39</strong>.</li>
<li>Weighted to the population: 0.2 × 4.6 + 0.3 × 4.4 + 0.5 × 3.9 = <strong>4.19</strong>.</li>
<li>Weights per respondent: heavy 0.44, medium 0.86, light 2.5. Effective sample: <strong>5,010</strong> of 7,990, 63%.</li></ul>
<p>A 0.2-point drop sounds small, but light buyers are half the base and the least satisfied. The weighted share satisfied is 75%, not 81%, and the gap between segments is the more useful finding.</p>
<h4>Half-worked: stated against revealed</h4>
<p>Asked why they stopped buying, 40% of lapsed buyers chose \"prices too high\". A price-cut test for lapsed buyers raised their return rate by 1 point; a delivery-speed test raised it by 3 points, although only 15% had cited delivery. How do you reconcile them, and what would you tell the pricing team?</p>
{reveal("<p>Stated reasons reflect what is easy and acceptable to say; price is the default answer. Behaviour in randomised tests shows what changes decisions. Tell the pricing team the survey is a signal that price perception matters, but the measured lever for win-back is delivery speed. Follow up with interviews of lapsed buyers who did return after the delivery test, to understand why.</p>")}
<h4>Bare: sizing an interview finding</h4>
<p>Six of 12 interviewees were confused by fees at checkout. Design the measurement that tells you how many buyers are affected and what it costs.</p>
{reveal("<p>From behaviour: drop-off at the fee step against other steps; taps on fee-info icons; back-navigation from the fee line; support contacts mentioning fees. From a short in-product question shown to a random 2% of buyers at the fee step: \"Is anything unclear about the total?\" Then size lost orders from the drop-off gap, and test a clearer fee display with an A/B test to confirm the cost and the fix.</p>")}
<h4>Predict, then play</h4>
<p>Predict what happens to the weighted estimate and the effective sample size if light buyers' response rate falls from 3.2% to 1%.</p>
{reveal("<p>The weighted estimate barely moves, since it is anchored to population shares, but light respondents' weights grow large and the effective sample falls sharply, so the estimate gets noisier. Worse, the few light buyers who still answer are likely to be unusual ones, which no weight can fix. Low response in a key group is a reason to change how you ask, not only how you weight.</p>")}
<div class="lab" data-lab="weighting"></div>
<pre class="code">import pandas as pd

r = survey.merge(users[["user_id", "segment"]], on="user_id")          # consented join
pop = users.segment.value_counts(normalize=True)
resp = r.segment.value_counts(normalize=True)
r["w"] = r.segment.map(pop / resp)                                     # post-stratification
weighted_psat = (r.psat * r.w).sum() / r.w.sum()
n_eff = r.w.sum() ** 2 / (r.w ** 2).sum()
# raking (several margins at once): weights adjusted in turn to each margin until they all match</pre>
{tests([("Why weight by behavioural segment rather than by demographics?", "<p>Behaviour is what you have for everyone, and it is often what drives both response and satisfaction. Demographics may be unknown for many users and less related to the answers.</p>", True),
("After weighting by segment, respondents in the light segment still bought twice as often as non-respondents in it. What does that tell you?", "<p>Non-response within the segment is still related to engagement. Add finer cells or more margins, such as purchase frequency within segment, and treat the estimate as an upper bound on satisfaction.</p>")])}"""

s5 = f"""{table(["You are assuming", "When it is false", "How you would notice"], [
["Respondents resemble non-respondents within cells", "Happier users answer more, even within a segment", "Compare behaviour of respondents and non-respondents within cells"],
["The survey reached the population of interest", "Triggered after support contacts, or sent only to app users", "Compare the sampled base with all users"],
["Answers mean the same across groups", "Scales used differently by language or culture", "Anchor with behaviour; check by group"],
["Stated reasons are causes", "People rationalise", "Compare with test results and behaviour"],
["Interviews are representative", "Recruited from engaged users", "Report how participants were chosen"],
["Linking is permitted", "Consent or privacy rules forbid the join", "Design consent in; aggregate where needed"]])}
{tests([("Response to the PSAT survey doubled after a reminder email. Is the new estimate more trustworthy?", "<p>More respondents help if the reminder reached less engaged buyers. Check whether the second-wave respondents look more like the population. If they are the same kind of people, precision rose but bias did not fall.</p>")])}"""

s6 = f"""{table(["Method", "Answers", "Pick it when", "Watch out"], [
["User interviews, usability studies", "What and why", "Early, and to explain surprises", "Not for how many"],
["Random-sample surveys", "How common an attitude is", "Measuring perceptions", "Non-response; wording"],
["Post-stratification or raking", "Population estimate from respondents", "Response varies by known traits", "Only measured traits; smaller n_eff"],
["Linked survey and behaviour", "Who answered; does attitude predict action?", "Consent allows", "Privacy, governance"],
["Behavioural analytics", "What people do, at scale", "Sizing, tracking", "Silent on why"],
["Experiments", "Does changing it help?", "Before investing", "See <a href='#a3-experiment-design'>A/B design</a>"]])}
{tests([("A new feature launched; usage is low. Which two rows first?", "<p>Behavioural analytics to see where users drop off, and five to ten interviews with users who tried it once and stopped, to learn why. Then a test of the most promising fix.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>NPS by seller tier</strong> for a quarterly business review.</p>
<p><strong>CSAT after support chats</strong> for the support team's goals.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Interviews</strong> before redesigning search filters.</p>
<p><strong>A diary study</strong> of how sellers manage stock.</p></div></div>
{reveal('''<p><strong>Pair 1 are scores that need weighting and linking.</strong> Who answers drives the number; linking to behaviour shows who is missing and whether the score predicts retention or spend.</p>
<p><strong>Pair 2 are qualitative discovery.</strong> They find problems and language for them; their output is hypotheses and designs, sized and tested afterwards with data.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Quoting survey scores as if they described all users. A product review shows an average PSAT from respondents, who are the most engaged fifth of the user base, and declares success, while light users, half the base, are quietly unhappy. Joining responses to behaviour exposes it in an afternoon.</p>
{tests([("A team reports NPS rose from 32 to 40 after a launch. What two questions do you ask?", "<p>Did the mix of respondents change, for example more heavy users answering, and does the rise show up in behaviour, such as retention or referrals? Weight to a fixed population and check against behaviour before crediting the launch.</p>")])}"""

s8 = f"""<ul>
<li><strong>Sample at random</strong> from the population the decision is about, and record who was asked.</li>
<li><strong>Link responses to behaviour</strong> with consent; compare respondents with non-respondents on every metric you have.</li>
<li><strong>Weight to the population</strong> and report the effective sample size; show segment results, not only the total.</li>
<li><strong>Calibrate scores</strong> against later behaviour: what is a point of PSAT worth in retention?</li>
<li><strong>Run the loop</strong>: interviews to find, data to size, tests to fix, interviews to explain.</li>
<li><strong>Quote people</strong> in reports. A sentence from a buyer often moves a team more than a chart.</li></ul>
{tests([("How would you make PSAT useful for prioritisation rather than a vanity score?", "<p>Link it to retention and spend to estimate what a point is worth; break it down by segment and journey step; pair low-scoring steps with interview findings; and track it on a weighted, fixed population so changes reflect the product, not the respondents.</p>")])}"""

s9 = f"""<ul>
<li><strong>Is NPS worth tracking?</strong> Critics say one question with arbitrary cut-offs predicts little. Supporters say its simplicity makes it a shared language. Linking it to behaviour settles its value for your business.</li>
<li><strong>Weight or not?</strong> Weighting removes known bias and adds variance. With extreme weights, some teams prefer reporting by segment unweighted.</li>
<li><strong>Who owns the insight?</strong> Research and analytics teams often work separately. Joint ownership of questions, rather than handing over findings, makes the loop work.</li>
<li><strong>Privacy.</strong> Joining what people say to what they do is powerful and sensitive. Consent, aggregation and access controls decide what is acceptable.</li></ul>
{tests([("Make the case for running interviews before looking at any data.", "<p>Data can only answer questions about what was logged, framed by what the team already believes. Interviews surface problems and words nobody thought to measure, so the analysis that follows asks better questions.</p>")])}"""

rungs = [
 {"ask": "How do you combine survey results with behavioural data?", "follow": ["Why join by user?", "What does weighting fix and not fix?"],
  "weak": "<p>\"Show both on the same dashboard.\"</p>",
  "strong": "<p>Join responses to behaviour by user, with consent. Compare respondents with non-respondents to see who is missing; weight to the population on behaviour and report the effective sample; break results down by segment; and check whether attitudes predict later behaviour. Weighting fixes measured differences, not unmeasured ones within cells.</p>"},
 {"ask": "8% answered a PSAT survey; heavy buyers answered at 18% and light at 3%; PSAT is 4.6, 4.4 and 3.9 by segment, with population shares 20%, 30% and 50%. Re-estimate PSAT.", "follow": ["What is the effective sample size?", "What is still biased?"],
  "model": "<p>unweighted 4.39 because heavy buyers are 45% of respondents. Weighted: 0.2 × 4.6 + 0.3 × 4.4 + 0.5 × 3.9 = 4.19. Weights of 0.44, 0.86 and 2.5 cut the effective sample from about 8,000 to 5,000. Within segments, happier buyers may still answer more, so 4.19 may still be optimistic.</p>",
  "weak": "<p>Reports 4.39 or simply drops light buyers.</p>",
  "strong": "<p><b>Must have.</b> Post-stratifies to population shares and explains the gap.</p><p><b>Strong signal.</b> Gives the effective sample and flags within-cell non-response.</p>"},
 {"ask": "40% of churned buyers say price drove them away, but a price-cut test barely moved win-back. Explain.", "follow": ["Which do you trust?", "What would you do next?"],
  "weak": "<p>\"The test was too small.\"</p>",
  "strong": "<p>Stated reasons are what people find easy to say; price is the default. A randomised test shows what changes behaviour. Trust the test for the lever, treat the survey as a signal about price perception, and interview buyers who responded to other tests, such as faster delivery, to learn what actually brings them back.</p>", "roles": ["lead", "ic"]},
 {"ask": "Design a voice-of-customer programme that product teams can act on.", "follow": ["How do research and analytics work together?", "How do you avoid survey fatigue?"],
  "weak": "<p>\"A monthly NPS survey.\"</p>",
  "strong": "<p>Random, rotating samples so no buyer is asked often; responses linked to behaviour and weighted; scores calibrated against retention and spend; open-text tagged and validated; quarterly interview rounds on the weakest journey steps; findings sized with behavioural data and tested with experiments; reports that pair numbers with quotes; joint research and analytics ownership of the question list.</p>", "roles": ["lead", "ic"]},
 {"ask": "A PM's launch review says 'buyers love it' based on a survey of respondents. You know light buyers are underrepresented and less happy. What do you do?", "follow": ["How do you say it in the review?", "What do you offer instead?"],
  "weak": "<p>Says nothing, since the survey was positive.</p>",
  "strong": "<p>Before the review, shows the PM the respondent mix and the weighted result, so the correction is theirs. In the review: heavy buyers love it; light buyers, half our base, are lukewarm, and interviews point to fee confusion. Offers a sizing and a test of the fee display as the next step, which turns a correction into a plan.</p>", "roles": ["lead"]},
]

page(S, "C6", "Joining survey, PSAT and UXR findings to behavioural data",
     "Surveys and interviews say why; behaviour says how many and how much. Joining them shows who answered and who did not, lets you weight answers back to everyone, tests stated reasons against what people do, and turns a research finding into a sized, testable opportunity.",
     "qual quant survey psat csat nps uxr user research interviews non-response bias weighting post-stratification raking effective sample size kish stated preference revealed preference linking surveys to behaviour voice of customer",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Join what people say to what they do so you can see who answered, weight answers back to the whole population at a known cost in precision, check stated reasons against behaviour, and use interviews to find problems that data then sizes and experiments test.",
     ["Link responses to behaviour, with consent", "Respondents are not the population: weight and report n_eff", "Weighting fixes only measured differences", "Stated reasons are hypotheses; tests decide", "Qual finds, quant sizes, experiments test"],
     [("c3-metric-design", "Designing metrics"), ("a2-confidence-intervals", "Confidence intervals"), ("c5-text-analytics", "Text analytics on search queries and feedback")],
     [("c3-key-drivers", "Key driver analysis"), ("c6-opportunity-sizing", "Opportunity sizing with ranges and past experiment lifts"), ("e1-exec-communication", "Communicating results to executives")],
     sources=[("Groves, \"Nonresponse Rates and Nonresponse Bias in Household Surveys\", Public Opinion Quarterly, 2006", "https://doi.org/10.1093/poq/nfl033"),
              ("Kish, Survey Sampling, Wiley, 1965", "https://www.wiley.com/en-us/Survey+Sampling-p-9780471109495")],
     sec_roles={11: ["lead", "ic", "mle"]})
