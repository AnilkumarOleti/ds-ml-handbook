import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from pagekit import page, reveal, table, tests, attempt, ref

S = "e2-building-team"
R = ["lead"]

s1 = f"""<div class="problem"><p>You are asked to set up product analytics for <strong>six product squads</strong>: search, listings, checkout, payments, seller tools and buyer growth. You have <strong>eight</strong> headcount, four of them still to hire. Today every squad sends requests to a shared inbox, waits a week, and each squad defines "active seller" its own way.</p>
<p>Choose an operating model: <strong>central</strong> (one team, one queue), <strong>embedded</strong> (an analyst in each squad, reporting to the squad), or <strong>hub and spoke</strong> (analysts sit in squads and report to you, with a small central hub). Say who does what with the eight, and what you will have fixed in 90 days.</p></div>
{attempt(S, 1)}{reveal('''<p><strong>Hub and spoke.</strong> Six analysts, one per squad, sit in squad rituals and report to you. Two form the hub: one owns the metric layer, definitions and experiment review; one takes cross-squad questions and covers absences.</p>
<ul><li><strong>Why not central:</strong> a shared queue is why squads wait a week. Analysts never learn a product well enough to suggest the question.</li>
<li><strong>Why not fully embedded:</strong> an analyst whose review is written by the squad lead whose launches they judge is under pressure, and six squads drift into six definitions of every metric.</li>
<li><strong>The hub</strong> keeps one definition of each metric and reviews readouts from outside the squad.</li></ul>
<p><strong>In 90 days:</strong> one definition each of the ten metrics leadership reads; an experiment brief template with a decision rule; the four hires made; each squad's analyst able to name the two decisions they changed. Not in 90 days: a new data platform.</p>''')}"""

s2 = f"""<p><strong>The hospital.</strong> Ward doctors are embedded with patients and know each case. The pathology lab is central: it runs tests for every ward to one standard. A hospital with only ward doctors gets inconsistent tests. One with only a lab has nobody who knows the patient.</p>
<p><strong>The newspaper.</strong> Bureau correspondents live in their beats and find the stories. The central desk sets the style, checks facts and decides what runs. The correspondent reports to the desk, not to the people being covered.</p>
{table(["Idea", "Hospital", "Newspaper", "Analytics"], [
["Embedded role", "Ward doctor", "Bureau correspondent", "Squad analyst"],
["Central role", "Pathology lab", "Central desk", "Hub: metrics, review, platform"],
["What the centre guarantees", "Test standards", "Style and fact checking", "One definition per metric, sound methods"],
["Reports to", "Medical director", "Editor", "Head of analytics"],
["Failure without a centre", "Every ward tests differently", "Each bureau has its own facts", "Six definitions of \"active seller\""],
["Failure without the embedded", "Nobody knows the patient", "No stories", "Numbers nobody asked for"]])}
<p>What does the newspaper teach that the hospital does not? One sentence.</p>
{attempt(S, 2, "One sentence.")}{reveal("<p>The correspondent's independence comes from the reporting line: they live with the people they cover but answer to an editor, which is what lets an embedded analyst deliver an unwelcome result.</p>", "Compare with mine", "Hide")}
<h4>Where each analogy breaks</h4><ul>
<li><strong>Doctors and journalists have professions that set standards.</strong> Analytics standards are mostly set by the team itself.</li>
<li><strong>Bureaus are far apart.</strong> Squads share users and metrics, so their work collides: a checkout win can be a payments loss.</li>
<li><strong>Both are mature.</strong> A new analytics function also has to build the data it reports on.</li></ul>
{tests([("A squad lead asks for her analyst to report to her \"so priorities are clear\". What do you offer instead?", "<p>Priorities set jointly each quarter, with the analyst in all her squad's rituals, while the reporting line stays with analytics so readouts stay independent and methods consistent.</p>")])}"""

s3 = f"""<div class="fx">operating model   central · embedded · hub and spoke
                  (seats in squads, reporting line central)
the hub owns      metric definitions · experiment review
                  shared tools · the hiring bar
squad analysts    the squad's questions · decision briefs
                  readouts · the squad's metric health

hiring funnel     entering a stage = hires ÷ product of
                  the pass rates from that stage on
                  hours = Σ entering × hours per candidate

career paths      IC ladder to staff and principal,
                  manager ladder, equal pay at equal level
first 90 days     listen (30) · fix one pain, agree
                  definitions (60) · set the cadence (90)</div>
<ul>
<li><strong>Central.</strong> Consistent methods, flexible allocation, shallow product knowledge and a queue. Suits a small team or a company with few products.</li>
<li><strong>Embedded.</strong> Deep context and speed, divergent definitions, isolated analysts with no peer review, and a reporting line to the person being evaluated.</li>
<li><strong>Hub and spoke.</strong> The common settlement: seats in squads, reporting line and standards central. Its cost is two bosses in practice, which needs a written agreement on priorities.</li>
<li><strong>Analytics maturity.</strong> Companies that compete on analytics treat it as an enterprise capability with senior sponsorship, not as scattered local efforts. {ref(1)}</li>
<li><strong>The hiring bar</strong> is set by the questions you ask and the rubric you score against, written down before the first interview.</li></ul>
{tests([("What does a hub-and-spoke team gain over a fully embedded one, and what does it pay?", "<p>It gains one set of definitions, peer review and independence of readouts. It pays in a double line of accountability that must be managed: the squad sets day-to-day priorities and the hub sets standards and the career.</p>"),
("Why is the reporting line, rather than where people sit, the thing that protects independence?", "<p>Whoever writes the appraisal shapes what an analyst is willing to say. Sitting with a squad builds context; reporting to it creates pressure to agree.</p>", True)])}"""

s4 = f"""<h4>Worked: the hiring funnel for four analysts</h4>
<p>Past hiring gives these pass rates and interviewer hours per candidate entering each stage:</p>
{table(["Stage", "Pass rate", "Hours per candidate", "Candidates entering", "Interviewer hours"], [
["Application screen", "30%", "0.1", "242", "24"], ["Phone screen", "50%", "1.0", "73", "73"], ["Take-home and review", "45%", "1.5", "36", "54"],
["Onsite loop", "35%", "5.0", "16", "82"], ["Offer accepted", "70%", "", "5.7 offers", ""]], narrow=True)}
<p>Work backwards: 4 hires ÷ 0.70 = 5.7 offers; ÷ 0.35 = 16 onsites; ÷ 0.45 = 36 take-homes; ÷ 0.50 = 73 phone screens; ÷ 0.30 = <strong>242 applications</strong>, about 60 per hire. Interviewer time: <strong>233 hours</strong>, about six weeks of one person's time, spread over the team. The onsite loop is the largest single cost, and the place where a sharper earlier screen saves the most.</p>
<h4>Half-worked: where the funnel leaks</h4>
<p>Offer acceptance drops from 70% to 50% because a competitor pays more. Redo the applications and the interviewer hours. Then consider tightening the phone screen to pass 40%, which raises the take-home pass rate to 60%.</p>
{reveal("<p>At 50% acceptance: 8 offers, <strong>339 applications and 326 hours</strong>, 40% more of everyone's time. Losing candidates at the last stage is the most expensive leak, because every earlier stage was spent on them. Fix pay or speed before anything else. The tighter phone screen, at 70% acceptance, cuts hours from 233 to <strong>213</strong>: fewer take-homes are reviewed for the same hires.</p>")}
<h4>Bare: the first quarter's output</h4>
<p>The four new analysts start together. Assume they produce half an experienced analyst's output in months one and two, and 80% in month three. How much do the four add in the first quarter, in analyst-months, and what do you promise the squads?</p>
{reveal("<p>4 × (0.5 + 0.5 + 0.8) = <strong>7.2 analyst-months</strong> of 12, and they also take time from the experienced four who onboard them. Promise the squads named analysts in month one and full service from month four. Stagger starts by a few weeks if you can, so onboarding does not land on the same mentors at once.</p>")}
<h4>Predict, then play</h4>
<p>Raise the onsite pass rate from 35% to 50% by making the take-home more selective. Predict how much applications and interviewer hours fall.</p>
{reveal("<p>Both fall by the same 30%: every stage before the offer scales with the number of onsites needed. Applications fall from 242 to 169 and hours from 233 to 163. An efficient funnel depends on early stages that predict the late ones.</p>")}
<div class="lab" data-lab="funnel"></div>
{tests([("Why is a candidate who declines your offer the most expensive outcome in the funnel?", "<p>Every stage before the offer was spent on them, including the onsite, the costliest. One decline at the end costs as much as several rejections at the start.</p>", True)])}"""

s5 = f"""{table(["Assumption", "When it is false", "What you see", "Response"], [
["Squads know what to ask", "They ask for numbers, not decisions", "Many dashboards, no decisions changed", "Each analyst writes the decision brief with the squad"],
["Embedded analysts stay consistent", "Definitions drift without a central owner", "Two squads report different seller counts", "One metric layer owned by the hub"],
["Hiring fast fills the gap", "A low bar lowers the team's credibility", "Readouts get re-done by seniors", "A written rubric; never hire under pressure of a deadline"],
["Seniors will mentor naturally", "Mentoring competes with deadlines", "New hires stall at month three", "Name a mentor and budget their time"],
["IC work is a step toward management", "The best analysts leave for staff roles elsewhere", "Strong ICs ask for reports they do not want", "A real IC ladder to staff and principal"],
["The team's value is obvious", "Leadership sees cost, not decisions", "Headcount is cut first in a downturn", "A decision log with the value of each changed decision"]])}
{tests([("A year in, the team is busy and well liked, but the business head cannot name anything it changed. What do you fix first?", "<p>Start a decision log: for each piece of work, the decision it informed and what happened. Then redirect effort towards work tied to decisions. The team has become a service desk.</p>")])}"""

s6 = f"""{table(["Model", "Fits when", "Strength", "Cost"], [
["Central", "Under about five analysts, or few products", "Consistency, flexible allocation", "Queue, shallow context"],
["Embedded", "Large, mature teams with strong standards elsewhere", "Speed, context", "Drift, isolation, independence"],
["Hub and spoke", "Most growing product organisations", "Context with standards", "Two lines of accountability"],
["Centre of excellence", "Analysts spread across functions already", "Shared methods without reorganising", "Little authority"],
["Platform team", "Self-serve analytics at scale", "Leverage through tools", "Distance from decisions"]])}
{tests([("The company grows from six squads to twenty. What happens to your hub?", "<p>It splits into a metrics and platform group and a methods group for experiment review, and squads are grouped into areas, each with a lead analyst. The hub must grow slower than the spokes or it becomes a bureaucracy.</p>")])}"""

s7 = f"""<div class="links"><div><p class="label">Pair 1</p>
<p><strong>Setting up analytics at a new capability centre.</strong> Stakeholders are in another time zone.</p>
<p><strong>Inheriting a team of ten.</strong> Half of them maintain dashboards nobody reads.</p></div>
<div><p class="label">Pair 2</p>
<p><strong>Hiring your first staff-level IC.</strong></p>
<p><strong>Promoting a strong analyst to manager.</strong></p></div></div>
{reveal('''<p><strong>Pair 1 is earning a seat at the decision.</strong> Distance and legacy work both push a team towards output nobody uses. In both, find the two or three decisions that matter most to each stakeholder, attach a named person to each, and retire work that serves none. A remote team needs written decision briefs and overlap hours more than a co-located one.</p>
<p><strong>Pair 2 is the career ladder.</strong> A staff IC needs a scope larger than one squad, such as owning experimentation methods, or the role is a title only. Promotion to manager should be a choice between two ladders of equal standing, not the only way up.</p>''', "What does each pair share?", "Hide")}
<h4>A well-known misuse</h4>
<p>Measuring the team by requests closed. It rewards fast, small, uncontroversial work and penalises the analyst who spends three weeks on the one question that changes the roadmap. Measure decisions informed and their value, imperfect as that is.</p>
{tests([("Your stakeholders are mostly in the US and your team is in India. Name two practices that matter more than in a co-located team.", "<p>Written decision briefs agreed before the work starts, and readouts sent as documents before a short overlap-hour meeting. Asynchronous writing replaces the hallway conversation.</p>")])}"""

s8 = f"""<ul>
<li><strong>Spend the first 30 days listening</strong>: each stakeholder's top three decisions and what they currently use to make them.</li>
<li><strong>Fix one visible pain by day 60</strong>, such as one definition of active seller, to earn trust for the larger changes.</li>
<li><strong>Write the rubric before the first interview</strong>: problem framing, statistics, SQL, communication, each with weak and strong answers. The ladders in this handbook are a template.</li>
<li><strong>Keep a decision log</strong>, and review it with leadership each quarter.</li>
<li><strong>Protect deep work.</strong> Reserve a share of each analyst's time for proactive analysis the squad did not ask for.</li>
<li><strong>Build two ladders</strong>, IC and manager, with equal levels and pay.</li></ul>
{tests([("What does a quarterly review of the decision log give you that a satisfaction survey does not?", "<p>Evidence of impact, in decisions and money, that survives a budget review. A survey shows whether people like the team, which is a different thing.</p>")])}"""

s9 = f"""<ul>
<li><strong>Embedded or central?</strong> Advocates of embedding say context is everything and central teams become ticket queues. Advocates of centralisation say embedded analysts lose independence and standards. The hub-and-spoke model is a compromise, and its success depends on the written agreement between squad leads and the head of analytics.</li>
<li><strong>Specialists or generalists?</strong> Some teams hire separate experimentation, modelling and analytics engineering roles. Others hire full-stack analysts who do all three. Specialists go deeper; generalists finish work without hand-offs.</li>
<li><strong>Take-home exercises?</strong> They test real work and favour candidates with free time. Live exercises are fairer on time and more stressful. Paid or short take-homes are a middle path.</li>
<li><strong>Who owns the metric layer?</strong> Analytics, data engineering or a platform team. Ownership by analytics keeps definitions close to their use; by engineering, close to their production.</li></ul>
{tests([("Make the case for a fully embedded model.", "<p>Analysts who report to the squad are part of its decisions from the start, are never stuck in a queue, and are judged on the squad's outcomes. Standards can be kept through a guild and shared tools without a central reporting line.</p>")])}"""

rungs = [
 {"ask": "Compare central, embedded and hub-and-spoke analytics teams.", "follow": ["Which would you choose for six squads and eight people?", "What does each model's failure look like?"],
  "weak": "<p>Lists the three with no criteria.</p>",
  "strong": "<p>Central: consistency and flexible allocation, at the cost of a queue and shallow context. Embedded: context and speed, at the cost of drifting definitions and independence. Hub and spoke: seats in squads, reporting line and standards central, at the cost of managing two lines of accountability. Chooses by team size, product count and how mature the shared standards are.</p>"},
 {"ask": "Why should embedded analysts report to the head of analytics rather than to the squad lead?", "follow": ["The squad lead says she cannot set priorities otherwise.", "When would you let them report to the squad?"],
  "model": "<p>whoever writes the appraisal shapes what an analyst is willing to say, and analysts often judge the launches of the person they would report to. A central line protects unwelcome readouts, keeps methods and definitions consistent, and gives a career path. Priorities are set jointly with the squad each quarter.</p>",
  "weak": "<p>\"For consistency.\"</p>",
  "strong": "<p><b>Must have.</b> Independence of readouts tied to the appraisal.</p><p><b>Strong signal.</b> Offers a joint priority-setting process so the squad lead keeps control of what gets worked on.</p>"},
 {"ask": "Offer acceptance fell from 70% to 50%. What does that do to your hiring plan for four analysts?", "follow": ["Where else in the funnel would you look?", "What would you change first?"],
  "weak": "<p>\"Interview more people.\"</p>",
  "strong": "<p>Works back through the funnel: offers rise from 5.7 to 8, applications from 242 to 339, interviewer hours from 233 to 326. Treats late-stage loss as the costliest leak, so first checks pay, speed and the candidate experience; then tightens early stages so the onsite pass rate rises.</p>"},
 {"ask": "Design the first 90 days of a new product analytics function.", "follow": ["What will you not do in 90 days?", "How will leadership know it is working?"],
  "weak": "<p>\"Build dashboards for every squad.\"</p>",
  "strong": "<p>Days 1–30: interview each stakeholder for their top decisions, audit existing metrics and requests. Days 31–60: one agreed definition of the leadership metrics, a decision-brief template, the operating model agreed in writing, hiring started with a rubric. Days 61–90: each squad's analyst attached to named decisions, a weekly readout cadence, a decision log. Not in 90 days: a new data platform. Success is decisions changed, reported quarterly.</p>"},
 {"ask": "Budgets are cut and you must lose two of eight analysts. How do you decide what the team stops doing?", "follow": ["A squad lead says losing their analyst will hurt the roadmap.", "How do you tell the team?"],
  "weak": "<p>Cuts evenly across squads.</p>",
  "strong": "<p>Uses the decision log: what each piece of work changed and what it was worth. Stops work that informs no decision, moves recurring reporting to self-serve, and covers the lowest-value squads from the hub rather than leaving none. States openly to leadership what will no longer be possible. Tells the team the reasons and criteria in person before any announcement.</p>"},
]

page(S, "E2", "Building an analytics function",
     "How to set up a product analytics team: choosing between central, embedded and hub-and-spoke models, keeping readouts independent, running a hiring funnel by the numbers, and what to fix in the first 90 days.",
     "building analytics team org design operating model central embedded hub and spoke hiring funnel interview rubric career ladder staff ic manager first 90 days decision log capability centre",
     R, {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9}, rungs,
     "Give analysts seats in the squads and a reporting line to analytics, keep one central owner for metric definitions and review, hire by a written rubric and a funnel worked backwards from the hires, and prove the team's value with a log of the decisions it changed.",
     ["Central, embedded and hub-and-spoke, and when each fits", "The reporting line protects independence", "One owner for metric definitions", "Work the hiring funnel backwards; late losses cost most", "A decision log shows the team's value"],
     [("e2-prioritisation-capacity", "Prioritisation and capacity"), ("e2-stakeholders-pushback", "Stakeholders and pushback")],
     [("e1-exec-communication", "Communicating results to executives"), ("c3-metric-design", "Designing metrics")],
     sources=[("Davenport, \"Competing on Analytics\", Harvard Business Review, 2006", "https://pubmed.ncbi.nlm.nih.gov/16447373/")],
     sec_roles={11: ["lead", "ic"]})
