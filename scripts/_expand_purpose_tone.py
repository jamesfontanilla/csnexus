"""
Expand Author's Purpose and Tone questions to reach 600 total.
Adds additional Medium and Hard questions to the existing JSON.
"""

import json
import os

QUESTIONS_PATH = os.path.join(
    os.path.dirname(__file__), "..",
    "data", "seed", "questions", "verbal-ability",
    "reading-comprehension", "authors-purpose-and-tone",
    "questions.json"
)

BASE = {
    "subtest": "Verbal Ability",
    "module": "Reading Comprehension",
    "subtopic": "Author's Purpose and Tone",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}


def q(id, difficulty, passage, question, choices, answer, explanation, tags):
    return {
        **BASE,
        "id": id,
        "difficulty": difficulty,
        "passage": passage,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    }


# Load existing
with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
    existing = json.load(f)

_id = max(item["id"] for item in existing)


def next_id():
    global _id
    _id += 1
    return _id


# ============================================================
# ADDITIONAL MEDIUM QUESTIONS
# ============================================================

extra_medium = [
    q(next_id(), "Medium",
      "The urban garden project transformed a vacant lot into a productive space growing vegetables for 30 families. The city government, which had ignored the lot for a decade, now claims credit for 'supporting community-led food security initiatives' in its annual report.",
      "What is the author's tone?",
      ["Supportive of the government", "Ironic about credit-claiming", "Neutral", "Hostile"],
      "Ironic about credit-claiming",
      "The contrast between a decade of neglect and now claiming credit creates irony about institutional opportunism.",
      ["author's tone", "ironic"]),

    q(next_id(), "Medium",
      "The hospital's new wing was built with private donations after the government failed to fund it for fifteen years. At the inauguration, the governor cut the ribbon and delivered a speech about 'our administration's commitment to healthcare.' The donors were seated in the third row.",
      "What is the author's tone?",
      ["Impressed by the governor", "Pointedly ironic about misattributed credit", "Neutral", "Supportive"],
      "Pointedly ironic about misattributed credit",
      "Fifteen years of government failure, private funding, then the governor claiming credit while donors sit in the back — pointed irony.",
      ["author's tone", "ironic", "pointed"]),

    q(next_id(), "Medium",
      "The environmental impact assessment was conducted by a firm hired and paid by the mining company seeking approval. Unsurprisingly, it concluded that the project posed 'minimal environmental risk.' Independent scientists who reviewed the same data reached the opposite conclusion.",
      "What is the author's tone?",
      ["Neutral", "Skeptically exposing conflict of interest", "Supportive of the assessment", "Confused"],
      "Skeptically exposing conflict of interest",
      "'Hired and paid by the mining company' and 'unsurprisingly' reveal skepticism about the assessment's independence.",
      ["author's tone", "skeptical", "exposing"]),

    q(next_id(), "Medium",
      "The public school teacher creates lesson plans at midnight, grades papers during her commute, and spends weekends preparing materials — all unpaid labor that the system depends on but refuses to acknowledge. Teaching is the only profession where overtime is called 'dedication' instead of 'exploitation.'",
      "What is the author's tone?",
      ["Neutral", "Sympathetic to teachers with systemic criticism", "Critical of teachers", "Indifferent"],
      "Sympathetic to teachers with systemic criticism",
      "Detailing unpaid labor and reframing 'dedication' as 'exploitation' — sympathy for teachers combined with systemic critique.",
      ["author's tone", "sympathetic", "critical"]),

    q(next_id(), "Medium",
      "The youth summit produced a 'declaration of commitment' signed by 500 young leaders. The declaration commits to 'fostering dialogue,' 'building bridges,' and 'creating sustainable change.' It does not specify what dialogue, which bridges, or what change. Commitment without specificity is just enthusiasm with a signature.",
      "What is the author's tone?",
      ["Inspired by the youth", "Skeptically critical of vague commitments", "Neutral", "Hostile to youth engagement"],
      "Skeptically critical of vague commitments",
      "Listing vague phrases and 'enthusiasm with a signature' — skepticism about declarations that commit to nothing concrete.",
      ["author's tone", "skeptical", "critical"]),

    q(next_id(), "Medium",
      "The indigenous textile sells for ₱15,000 in a Manila gallery. The weaver who spent three months creating it received ₱1,500. The gallery owner explains that the markup covers 'curation, marketing, and cultural contextualization.' The weaver has a different word for it.",
      "What is the author's tone?",
      ["Supportive of the gallery", "Critically sympathetic to the weaver", "Neutral", "Confused"],
      "Critically sympathetic to the weaver",
      "The 10x markup, jargon justification, and 'the weaver has a different word' — sympathy for the exploited artisan, criticism of the system.",
      ["author's tone", "sympathetic", "critical"]),

    q(next_id(), "Medium",
      "The disaster drill was conducted with textbook precision. Evacuation routes were followed, assembly points were reached, and the exercise was completed in record time. It was also conducted on a sunny Tuesday morning with advance notice, full staffing, and no actual emergency. Whether this performance would survive contact with reality remains untested.",
      "What is the author's tone?",
      ["Impressed", "Skeptically realistic about untested preparedness", "Hostile", "Neutral"],
      "Skeptically realistic about untested preparedness",
      "Acknowledging the drill's success but noting ideal conditions and 'whether this would survive reality' — skeptical realism.",
      ["author's tone", "skeptical", "realistic"]),

    q(next_id(), "Medium",
      "The senator's 'listening tour' visited twelve provinces in fourteen days. Each stop lasted exactly ninety minutes — thirty for the senator's speech, thirty for pre-selected questions, and thirty for photographs. Listening, in this format, is a generous description.",
      "What is the author's tone?",
      ["Impressed by the tour", "Dismissively critical of performative listening", "Neutral", "Supportive"],
      "Dismissively critical of performative listening",
      "The rigid format (speech, pre-selected questions, photos) and 'generous description' dismiss the tour as performance, not genuine listening.",
      ["author's tone", "dismissive", "critical"]),

    q(next_id(), "Medium",
      "The community's water system was built by an international NGO with the best of intentions and the worst of assumptions — that the community could maintain equipment they had never seen, repair parts available only in Manila, and pay monthly fees on incomes that fluctuate with the harvest.",
      "What is the author's tone?",
      ["Hostile to the NGO", "Critically compassionate — understanding intent while identifying failure", "Neutral", "Supportive"],
      "Critically compassionate — understanding intent while identifying failure",
      "'Best of intentions and worst of assumptions' — the author understands the NGO's motives while clearly identifying the design failures.",
      ["author's tone", "critical", "compassionate"]),

    q(next_id(), "Medium",
      "The company's 'mental health day' policy allows employees one day per quarter for self-care. The same company expects responses to emails within fifteen minutes, schedules meetings during lunch breaks, and considers leaving before 7 PM as 'lack of commitment.' Four days of wellness cannot compensate for 361 days of burnout.",
      "What is the author's tone?",
      ["Supportive of the policy", "Ironic about contradictory corporate wellness", "Neutral", "Enthusiastic"],
      "Ironic about contradictory corporate wellness",
      "The policy versus daily reality and '4 days cannot compensate for 361 days of burnout' — irony about performative wellness.",
      ["author's tone", "ironic", "critical"]),
]


extra_medium_2 = [
    q(next_id(), "Medium",
      "The free trade agreement was celebrated by economists and opposed by farmers. Economists cited GDP growth projections; farmers cited the price of imported rice that would undercut their harvest. Both were right — about different things, for different people, on different timescales.",
      "What is the author's tone?",
      ["Pro-free trade", "Balanced and observational about competing truths", "Anti-free trade", "Indifferent"],
      "Balanced and observational about competing truths",
      "'Both were right — about different things' — the author observes that both perspectives have validity without choosing sides.",
      ["author's tone", "balanced", "observational"]),

    q(next_id(), "Medium",
      "The heritage building's demolition permit was approved on a Friday afternoon, the demolition began Saturday morning, and by Monday — when preservation groups could have filed an injunction — only rubble remained. Speed, in this case, was not efficiency but strategy.",
      "What is the author's tone?",
      ["Neutral", "Accusatory about deliberate circumvention", "Supportive of the demolition", "Confused"],
      "Accusatory about deliberate circumvention",
      "The timeline (Friday approval, Saturday demolition, Monday too late) and 'speed was strategy' accuse the developers of deliberate circumvention.",
      ["author's tone", "accusatory"]),

    q(next_id(), "Medium",
      "The children's feeding program serves nutritious meals to 200 students daily. It is funded entirely by a retired teacher's pension and the donations of neighbors who are themselves barely above the poverty line. The government's contribution to child nutrition in this barangay: a poster about the food pyramid.",
      "What is the author's tone?",
      ["Neutral", "Admiring of community while critical of government absence", "Hostile", "Indifferent"],
      "Admiring of community while critical of government absence",
      "The community's sacrifice versus 'a poster about the food pyramid' — admiration for grassroots effort, criticism of institutional absence.",
      ["author's tone", "admiring", "critical"]),

    q(next_id(), "Medium",
      "The 'smart city' initiative installed sensors on every street corner to monitor traffic, air quality, and pedestrian flow. The data is collected, processed, and stored. It has not yet been used to make a single policy decision. The city is now very well-monitored. Whether it is better-governed remains to be seen.",
      "What is the author's tone?",
      ["Impressed by the technology", "Wryly skeptical about data without action", "Neutral", "Hostile to technology"],
      "Wryly skeptical about data without action",
      "'Very well-monitored' versus 'better-governed remains to be seen' — wry skepticism about collecting data without using it.",
      ["author's tone", "wry", "skeptical"]),

    q(next_id(), "Medium",
      "The veteran nurse has seen hospital administrators come and go — each with a new 'vision,' each reorganizing departments, each introducing forms that duplicate existing forms. The patients remain the same. Their needs remain the same. She continues doing her job regardless of which organizational chart is currently pinned to the bulletin board.",
      "What is the author's tone?",
      ["Critical of the nurse", "Admiring her constancy while weary of institutional churn", "Neutral", "Enthusiastic about reform"],
      "Admiring her constancy while weary of institutional churn",
      "The parade of administrators versus the nurse's steady service — admiration for her constancy, weariness about pointless reorganization.",
      ["author's tone", "admiring", "weary"]),

    q(next_id(), "Medium",
      "The scholarship essay prompt asks students to describe 'a challenge they have overcome.' For students whose challenges include hunger, homelessness, and family violence, this prompt demands the performance of trauma for an audience of strangers who will judge its authenticity. Vulnerability should not be an admission requirement.",
      "What is the author's tone?",
      ["Supportive of the prompt", "Critically protective of student dignity", "Neutral", "Indifferent"],
      "Critically protective of student dignity",
      "'Performance of trauma' and 'vulnerability should not be an admission requirement' — the author protects student dignity while criticizing the system.",
      ["author's tone", "protective", "critical"]),

    q(next_id(), "Medium",
      "The town's only ATM broke down three weeks ago. The nearest alternative is 45 kilometers away. Residents now pay ₱50 in transportation costs to withdraw their own money. The bank has 'escalated the repair request.' In banking terminology, this means nothing will happen soon.",
      "What is the author's tone?",
      ["Neutral", "Frustrated and wryly critical of corporate indifference", "Supportive of the bank", "Indifferent"],
      "Frustrated and wryly critical of corporate indifference",
      "Three weeks, 45km, ₱50 cost, and 'means nothing will happen soon' — frustration with corporate indifference to rural customers.",
      ["author's tone", "frustrated", "wry"]),

    q(next_id(), "Medium",
      "The artist's work was rejected by every gallery in the city for being 'too political.' She exhibited instead on the walls of the community she painted — the same walls the galleries would later photograph for their 'street art' exhibitions, without crediting her or paying her a centavo.",
      "What is the author's tone?",
      ["Neutral", "Indignant about exploitation of marginalized artists", "Supportive of the galleries", "Indifferent"],
      "Indignant about exploitation of marginalized artists",
      "Rejection then uncredited appropriation — indignation at how institutions exploit the work they initially rejected.",
      ["author's tone", "indignant"]),

    q(next_id(), "Medium",
      "The reforestation project's success is measured in seedlings planted — 100,000 this year alone. Its failure is measured in seedlings surviving — approximately 15,000. The difference between planting and growing is maintenance, which costs money, requires patience, and does not photograph as well as planting day.",
      "What is the author's tone?",
      ["Celebratory of the planting", "Critically pragmatic about the gap between planting and growing", "Neutral", "Hostile"],
      "Critically pragmatic about the gap between planting and growing",
      "The 85% failure rate and 'does not photograph as well' — pragmatic criticism of projects that prioritize optics over outcomes.",
      ["author's tone", "pragmatic", "critical"]),

    q(next_id(), "Medium",
      "The public transportation system was designed by people who have never used public transportation. This is evident in the bus stops placed on highways without pedestrian crossings, the schedules that assume passengers do not have jobs, and the routes that connect government offices to each other rather than communities to services.",
      "What is the author's tone?",
      ["Neutral", "Critically observant about disconnected planning", "Supportive of the system", "Indifferent"],
      "Critically observant about disconnected planning",
      "Each design failure traced to planners' disconnect from users — critical observation about who designs systems and for whom.",
      ["author's tone", "critical", "observational"]),
]


# ============================================================
# ADDITIONAL HARD QUESTIONS
# ============================================================

extra_hard = [
    q(next_id(), "Hard",
      "The poverty simulation exercise — where executives spend one day 'experiencing' poverty through role-play — costs ₱100,000 per session. Participants report feeling 'deeply moved' and 'more empathetic.' They return to their offices the next day. Nothing changes in policy, in budget allocation, or in the lives of the people whose poverty was briefly performed for educational purposes. Empathy without action is just tourism of suffering.",
      "What is the author's tone?",
      ["Supportive of the exercise", "Contemptuous of performative empathy", "Neutral", "Confused"],
      "Contemptuous of performative empathy",
      "'Briefly performed,' 'nothing changes,' and 'tourism of suffering' — contempt for empathy exercises that produce feelings but not action.",
      ["author's tone", "contemptuous"]),

    q(next_id(), "Hard",
      "The language of the loan modification letter was a masterpiece of bureaucratic obfuscation: 'Your request for forbearance has been evaluated in accordance with applicable guidelines and, upon review of submitted documentation, has been determined to be inconsistent with program eligibility criteria as currently defined.' Translation: no. But 'no' would have been too clear, too honest, and too easy to challenge.",
      "What is the author's tone?",
      ["Neutral", "Indignant about weaponized complexity", "Supportive of the bank", "Academic"],
      "Indignant about weaponized complexity",
      "'Masterpiece of obfuscation,' the translation to 'no,' and 'too clear, too honest' — indignation at language designed to confuse and disempower.",
      ["author's tone", "indignant", "critical"]),

    q(next_id(), "Hard",
      "The documentary about indigenous land rights won the festival's top prize. The filmmaker — not indigenous — accepted the award, thanked the community for 'sharing their story,' and announced plans for a sequel. The community, which had requested final cut approval and been denied, learned about the sequel from a news article. Their story, it seems, belongs to whoever holds the camera.",
      "What is the author's tone?",
      ["Celebratory of the film", "Bitterly critical of extractive storytelling", "Neutral", "Supportive of the filmmaker"],
      "Bitterly critical of extractive storytelling",
      "Denied approval, learning from news, and 'belongs to whoever holds the camera' — bitter criticism of extractive documentary practices.",
      ["author's tone", "bitter", "critical"]),

    q(next_id(), "Hard",
      "The standardized test's reading comprehension section asks students to identify the 'author's purpose' from four options. The irony is that actual authorial purpose is rarely singular, often contradictory, and almost never reducible to a multiple-choice answer. But the test must be scored by machine, and machines require certainty. So we teach students that meaning is simple, that texts have one purpose, and that ambiguity is a wrong answer.",
      "What is the author's tone?",
      ["Supportive of standardized testing", "Intellectually critical of reductive assessment", "Neutral", "Hostile to reading"],
      "Intellectually critical of reductive assessment",
      "The meta-commentary on testing purpose/tone questions and 'we teach students that ambiguity is a wrong answer' — intellectual criticism of oversimplification.",
      ["author's tone", "intellectual", "critical"]),

    q(next_id(), "Hard",
      "The corporation's 'stakeholder engagement' process invited community input through an online portal — in English, requiring an email address, accessible only with broadband internet. The affected community speaks Waray, has 15% internet penetration, and communicates primarily through face-to-face interaction at the barangay hall. The portal received zero community submissions. The company reported that 'stakeholders were given the opportunity to participate.'",
      "What is the author's tone?",
      ["Neutral", "Scathingly exposing designed exclusion", "Supportive of the process", "Confused"],
      "Scathingly exposing designed exclusion",
      "Each barrier (language, email, broadband) versus community reality, then 'given the opportunity' — scathing exposure of exclusion disguised as inclusion.",
      ["author's tone", "scathing", "exposing"]),

    q(next_id(), "Hard",
      "The retirement ceremony honored thirty years of service with a plaque, a handshake, and a cake from the office canteen. The retiree had trained every person in the room, solved problems that no one else could solve, and kept the department functioning through three reorganizations. Her replacement was hired at a higher salary. The plaque said 'Thank You.' It did not say 'We're Sorry.'",
      "What is the author's tone?",
      ["Celebratory", "Bitterly sympathetic about undervalued service", "Neutral", "Indifferent"],
      "Bitterly sympathetic about undervalued service",
      "The gap between contribution and recognition, the higher-paid replacement, and 'did not say We're Sorry' — bitter sympathy for undervalued workers.",
      ["author's tone", "bitter", "sympathetic"]),

    q(next_id(), "Hard",
      "The 'community consultation' lasted exactly as long as the law required — not a minute more. Questions were taken but not answered. Concerns were 'noted' — a verb that, in bureaucratic usage, means 'acknowledged and immediately forgotten.' The minutes of the meeting, when finally released, bore little resemblance to what was actually said. But they were official, and official is what matters in court.",
      "What is the author's tone?",
      ["Neutral", "Cynically critical of procedural compliance without substance", "Supportive", "Confused"],
      "Cynically critical of procedural compliance without substance",
      "'Exactly as long as required,' 'noted means forgotten,' and 'official is what matters in court' — cynical criticism of form over substance.",
      ["author's tone", "cynical", "critical"]),

    q(next_id(), "Hard",
      "The aid worker's Instagram shows smiling children, grateful mothers, and sunlit classrooms. It does not show the power dynamics that make those smiles obligatory, the dependency that gratitude masks, or the structural conditions that make aid necessary in the first place. The camera captures what the photographer wants to see; the story it tells is the photographer's, not the subject's.",
      "What is the author's tone?",
      ["Supportive of aid work", "Critically deconstructing the aid gaze", "Neutral", "Hostile to aid workers"],
      "Critically deconstructing the aid gaze",
      "'Smiles obligatory,' 'dependency that gratitude masks,' and 'photographer's story, not the subject's' — critical deconstruction of how aid is represented.",
      ["author's tone", "critical", "deconstructive"]),

    q(next_id(), "Hard",
      "The think tank's policy paper recommends 'market-based solutions to housing affordability.' Translated: let developers build luxury condominiums and hope that increased supply eventually reduces prices for everyone. This theory has been tested in every major city for thirty years. In every case, luxury supply increased and affordable housing decreased. The theory persists because it benefits those who fund think tanks.",
      "What is the author's tone?",
      ["Supportive of market solutions", "Scornfully critical of self-serving policy recommendations", "Neutral", "Academic"],
      "Scornfully critical of self-serving policy recommendations",
      "The translation, thirty-year failure record, and 'benefits those who fund think tanks' — scornful criticism of ideology serving wealth.",
      ["author's tone", "scornful", "critical"]),

    q(next_id(), "Hard",
      "The museum's 'decolonization initiative' added three indigenous artworks to its collection of 10,000 pieces. It also hired a 'diversity consultant' (on a six-month contract), created an 'inclusion committee' (advisory, non-binding), and published a statement acknowledging that the museum 'exists on ancestral land.' The land remains the museum's. The artworks remain behind glass. The initiative was declared complete.",
      "What is the author's tone?",
      ["Impressed by the initiative", "Mordantly satirical about tokenistic decolonization", "Neutral", "Supportive"],
      "Mordantly satirical about tokenistic decolonization",
      "Three artworks out of 10,000, temporary consultant, non-binding committee, and 'declared complete' — mordant satire of performative decolonization.",
      ["author's tone", "satirical", "mordant"]),
]


extra_hard_2 = [
    q(next_id(), "Hard",
      "The elected official's 'transparency' consists of posting his daily schedule on social media — meetings with business leaders, ribbon-cuttings, and photo opportunities. What is not posted: the meetings with campaign donors, the text messages to regulators, or the family members appointed to government positions. Selective transparency is just curated opacity.",
      "What is the author's tone?",
      ["Impressed by the transparency", "Acidly critical of performative openness", "Neutral", "Supportive"],
      "Acidly critical of performative openness",
      "What's shown versus hidden and 'curated opacity' — acid criticism of transparency that conceals more than it reveals.",
      ["author's tone", "acidly critical"]),

    q(next_id(), "Hard",
      "The international conference on hunger was catered by a five-star hotel. Between sessions on 'food insecurity in the Global South,' delegates enjoyed a seven-course lunch with wine pairings. The conference produced a 'declaration of intent' to 'address the root causes of hunger by 2030.' It is now 2026. The root causes remain unaddressed. The hotel has been booked for next year's conference.",
      "What is the author's tone?",
      ["Supportive of the conference", "Devastatingly satirical", "Neutral", "Hopeful"],
      "Devastatingly satirical",
      "Seven-course lunch at a hunger conference, unfulfilled declaration, and 'hotel booked for next year' — devastating satire of institutional self-perpetuation.",
      ["author's tone", "satirical", "devastating"]),

    q(next_id(), "Hard",
      "The 'participatory budgeting' process allows residents to vote on how 5% of the barangay budget is spent. The remaining 95% — including the items that most affect daily life — is decided behind closed doors by officials who were elected on platforms they have since abandoned. Participation, in this model, is the illusion of power offered as a substitute for the real thing.",
      "What is the author's tone?",
      ["Supportive of participatory budgeting", "Critically analytical about controlled participation", "Neutral", "Enthusiastic"],
      "Critically analytical about controlled participation",
      "The 5% versus 95% split and 'illusion of power as substitute for the real thing' — analytical criticism of participation as containment strategy.",
      ["author's tone", "analytical", "critical"]),

    q(next_id(), "Hard",
      "The disaster memorial was built five years after the event, at a cost of ₱50 million. It is beautiful — polished granite, engraved names, a reflecting pool. The survivors, many of whom still live in temporary shelters within sight of the memorial, were not consulted on its design. They would have preferred permanent housing. But housing does not photograph as well as granite.",
      "What is the author's tone?",
      ["Impressed by the memorial", "Bitterly ironic about misplaced priorities", "Neutral", "Supportive"],
      "Bitterly ironic about misplaced priorities",
      "₱50M memorial versus temporary shelters, and 'housing does not photograph as well as granite' — bitter irony about prioritizing symbols over substance.",
      ["author's tone", "bitter", "ironic"]),

    q(next_id(), "Hard",
      "The research ethics board approved the study on the grounds that participants gave 'informed consent.' The consent form was eight pages long, written at a graduate-school reading level, and presented to participants — subsistence farmers with an average of four years of formal education — minutes before the procedure. They signed because a person in a white coat asked them to. This is not consent; it is compliance dressed in legal language.",
      "What is the author's tone?",
      ["Supportive of the study", "Indignant about the fiction of informed consent", "Neutral", "Academic"],
      "Indignant about the fiction of informed consent",
      "'Not consent but compliance dressed in legal language' — indignation at how power imbalances make 'informed consent' a fiction.",
      ["author's tone", "indignant"]),

    q(next_id(), "Hard",
      "The city's 'affordable housing' program defines affordable as costing no more than 30% of household income. For a family earning minimum wage, this means a monthly housing budget of ₱5,400. The cheapest unit in the program costs ₱8,000 per month. Affordable housing, by the program's own definition, is unaffordable to those who need it most. The program continues to be called 'affordable.'",
      "What is the author's tone?",
      ["Supportive of the program", "Mordantly exposing definitional absurdity", "Neutral", "Confused"],
      "Mordantly exposing definitional absurdity",
      "The math (₱5,400 budget vs ₱8,000 cost) and 'continues to be called affordable' — mordant exposure of a program that fails its own definition.",
      ["author's tone", "mordant", "exposing"]),

    q(next_id(), "Hard",
      "The company's exit interview data has identified 'toxic management culture' as the primary reason for turnover for five consecutive years. Each year, the data is presented to the same managers who create the culture. Each year, they commission a 'workplace wellness initiative.' Each year, turnover increases. The system is not broken; it is functioning exactly as designed — to acknowledge problems without solving them.",
      "What is the author's tone?",
      ["Supportive of management", "Coldly analytical about systemic dysfunction", "Neutral", "Confused"],
      "Coldly analytical about systemic dysfunction",
      "'Not broken, functioning as designed' — cold analytical precision about how systems perpetuate problems while appearing to address them.",
      ["author's tone", "analytical", "cold"]),

    q(next_id(), "Hard",
      "The indigenous community's oral tradition contains detailed astronomical knowledge — star positions that predict monsoon timing, constellation patterns that guide navigation, and lunar cycles that determine planting schedules. A visiting astronomer called it 'surprisingly sophisticated.' Surprisingly. As if knowledge accumulated over millennia by careful observers requires surprise when it proves accurate.",
      "What is the author's tone?",
      ["Neutral", "Pointedly critical of condescending surprise", "Supportive of the astronomer", "Indifferent"],
      "Pointedly critical of condescending surprise",
      "Isolating 'surprisingly' and explaining why it's condescending — pointed criticism of the assumption that indigenous knowledge should be surprising.",
      ["author's tone", "pointed", "critical"]),

    q(next_id(), "Hard",
      "The newspaper's editorial independence is guaranteed by its charter. Its advertising revenue comes 60% from real estate developers. Its coverage of housing policy has never, in fifteen years, published an investigation critical of the development industry. The charter guarantees independence; the revenue structure guarantees its irrelevance.",
      "What is the author's tone?",
      ["Supportive of the newspaper", "Exposing structural compromise of editorial independence", "Neutral", "Confused"],
      "Exposing structural compromise of editorial independence",
      "'Charter guarantees independence; revenue guarantees its irrelevance' — exposing how financial dependence neutralizes formal independence.",
      ["author's tone", "exposing", "critical"]),

    q(next_id(), "Hard",
      "The 'innovation hub' occupies prime real estate in the city center — open floor plans, exposed brick, artisanal coffee. It has produced, in three years of operation, two mobile apps (both defunct), one 'disruption framework' (unpublished), and forty-seven pitch decks. The hub's greatest innovation may be its ability to consume public funding while producing nothing of public value, and to do so with such aesthetic confidence that no one questions the return on investment.",
      "What is the author's tone?",
      ["Impressed by the hub", "Devastatingly contemptuous", "Neutral", "Supportive"],
      "Devastatingly contemptuous",
      "The output list (defunct apps, unpublished framework, pitch decks) and 'aesthetic confidence that no one questions' — devastating contempt for funded emptiness.",
      ["author's tone", "contemptuous", "devastating"]),
]


extra_hard_3 = [
    q(next_id(), "Hard",
      "The university's 'community immersion' program sends students to rural areas for one week per semester. They build walls, paint classrooms, and take selfies with children. They do not ask what the community actually needs, do not return to maintain what they built, and do not examine why a community with abundant natural resources remains poor. Immersion without analysis is just voluntourism with academic credit.",
      "What is the author's tone?",
      ["Supportive of the program", "Critically dismissive of shallow engagement", "Neutral", "Hostile to students"],
      "Critically dismissive of shallow engagement",
      "'Do not ask, do not return, do not examine' and 'voluntourism with academic credit' — critical dismissal of engagement without depth.",
      ["author's tone", "critical", "dismissive"]),

    q(next_id(), "Hard",
      "The politician's 'poverty tour' — a single afternoon in a relocation site, cameras in tow — produced a social media post about 'understanding the struggles of ordinary Filipinos.' The post received 50,000 likes. The relocation site still has no running water. Understanding, in this context, is a photograph, not a policy.",
      "What is the author's tone?",
      ["Impressed by the politician's empathy", "Contemptuously ironic about performative concern", "Neutral", "Supportive"],
      "Contemptuously ironic about performative concern",
      "One afternoon, cameras, likes versus no water — contemptuous irony about concern performed for social media rather than enacted through policy.",
      ["author's tone", "contemptuous", "ironic"]),

    q(next_id(), "Hard",
      "The climate adaptation plan acknowledges that sea levels will rise, that coastal communities will flood, and that millions will be displaced. It then recommends 'further study' and 'stakeholder dialogue.' The ocean does not wait for stakeholder dialogue. It rises on its own schedule, indifferent to our preference for process over action.",
      "What is the author's tone?",
      ["Supportive of the plan", "Urgently critical of inadequate response to known threats", "Neutral", "Academic"],
      "Urgently critical of inadequate response to known threats",
      "'Ocean does not wait' and 'indifferent to our preference for process' — urgent criticism of delay in the face of certain threat.",
      ["author's tone", "urgent", "critical"]),

    q(next_id(), "Hard",
      "The food security report measures hunger in calories — whether a person consumes the minimum 2,100 per day. By this measure, a diet of nothing but white rice satisfies the requirement. The report does not measure nutrition, dignity, or the slow violence of a diet that keeps you alive while making you sick. We have defined survival so narrowly that it excludes living.",
      "What is the author's tone?",
      ["Supportive of the measurement", "Humanistically critical of reductive metrics", "Neutral", "Academic"],
      "Humanistically critical of reductive metrics",
      "'Slow violence,' 'keeps you alive while making you sick,' and 'defined survival so narrowly it excludes living' — humanistic criticism of dehumanizing metrics.",
      ["author's tone", "humanistic", "critical"]),

    q(next_id(), "Hard",
      "The 'digital divide' is not merely about access to technology — it is about access to the future. When government services move online, when job applications require email, when education assumes internet access, those without connectivity are not merely inconvenienced — they are systematically excluded from participation in modern civic life. The divide is not digital; it is democratic.",
      "What is the author's primary purpose?",
      ["To inform about internet statistics", "To persuade readers that digital exclusion is a democratic crisis", "To describe technology", "To explain how the internet works"],
      "To persuade readers that digital exclusion is a democratic crisis",
      "Reframing 'digital divide' as 'democratic divide' and arguing exclusion from civic life — persuasive purpose elevating the issue's urgency.",
      ["author's purpose", "to persuade"]),

    q(next_id(), "Hard",
      "The oral history project records stories that official history ignores — the washerwoman who hid guerrillas in her laundry baskets, the market vendor who smuggled medicine past checkpoints, the teacher who taught forbidden lessons in her kitchen. These are not footnotes to history; they are history itself, told by those who lived it rather than those who wrote about it from a comfortable distance.",
      "What is the author's tone?",
      ["Neutral", "Passionately valuing marginalized narratives", "Academic", "Critical of oral history"],
      "Passionately valuing marginalized narratives",
      "'Not footnotes but history itself' and 'those who lived it rather than those who wrote from a comfortable distance' — passionate advocacy for marginalized voices.",
      ["author's tone", "passionate", "valuing"]),

    q(next_id(), "Hard",
      "The efficiency metric shows that the automated system processes claims 300% faster than human reviewers. What the metric does not show: the 15% error rate that denies legitimate claims, the appeals process that takes six months, or the human cost of a wrong decision made at machine speed. Speed without accuracy is not efficiency — it is automated injustice.",
      "What is the author's tone?",
      ["Supportive of automation", "Critically humanistic about the limits of efficiency metrics", "Neutral", "Anti-technology"],
      "Critically humanistic about the limits of efficiency metrics",
      "Acknowledging speed but revealing errors, delays, and human cost — humanistic criticism that values accuracy and justice over speed.",
      ["author's tone", "humanistic", "critical"]),

    q(next_id(), "Hard",
      "The gentrification study was funded by the same development corporation driving gentrification in the study area. Its conclusion — that gentrification 'brings economic vitality to underserved communities' — was cited in the corporation's next planning application. Research, when funded by those with interests in its conclusions, is not inquiry — it is ammunition purchased in advance.",
      "What is the author's tone?",
      ["Supportive of the research", "Scornfully exposing compromised research", "Neutral", "Academic"],
      "Scornfully exposing compromised research",
      "'Ammunition purchased in advance' — scornful exposure of research designed to serve funder interests rather than truth.",
      ["author's tone", "scornful", "exposing"]),

    q(next_id(), "Hard",
      "The teacher's performance bonus is tied to student test scores. This incentivizes teaching to the test, discourages working with struggling students (who lower averages), and punishes teachers in under-resourced schools where scores are structurally depressed. The policy was designed by people who have never taught a class, never met a struggling student, and never worked in a school without air conditioning or functioning toilets.",
      "What is the author's tone?",
      ["Supportive of performance bonuses", "Indignant about disconnected policy design", "Neutral", "Academic"],
      "Indignant about disconnected policy design",
      "Listing perverse incentives and 'designed by people who have never taught' — indignation at policy made without understanding its impact.",
      ["author's tone", "indignant"]),

    q(next_id(), "Hard",
      "The country's 'creative economy' strategy envisions artists, writers, and musicians driving economic growth. It does not envision paying them fairly, providing healthcare, or recognizing their work as labor deserving of protection. The creative economy, as currently conceived, is an economy that consumes creativity without compensating creators — extraction dressed in the language of inspiration.",
      "What is the author's tone?",
      ["Supportive of the strategy", "Bitterly critical of exploitation disguised as opportunity", "Neutral", "Indifferent"],
      "Bitterly critical of exploitation disguised as opportunity",
      "'Consumes creativity without compensating creators' and 'extraction dressed in inspiration' — bitter criticism of systemic exploitation of creative workers.",
      ["author's tone", "bitter", "critical"]),
]


# ============================================================
# ADDITIONAL MEDIUM QUESTIONS (batch 3)
# ============================================================

extra_medium_3 = [
    q(next_id(), "Medium",
      "The literacy program teaches adults to read using government-approved textbooks. The textbooks contain passages about 'the importance of paying taxes,' 'respecting authority,' and 'the benefits of government programs.' Literacy, in this curriculum, is not liberation — it is indoctrination with better reading skills.",
      "What is the author's tone?",
      ["Supportive of the program", "Critically suspicious of ideological content", "Neutral", "Enthusiastic"],
      "Critically suspicious of ideological content",
      "Noting the textbook content and 'indoctrination with better reading skills' — critical suspicion about literacy used for ideological purposes.",
      ["author's tone", "critical", "suspicious"]),

    q(next_id(), "Medium",
      "The organic certification process costs ₱50,000 annually — more than many small farmers earn in a year. Farmers who have grown food without chemicals for generations cannot afford to prove what they have always practiced. Certification, designed to protect consumers, has become a barrier that excludes the very producers it should celebrate.",
      "What is the author's tone?",
      ["Supportive of certification", "Critically sympathetic to excluded farmers", "Neutral", "Hostile to organic farming"],
      "Critically sympathetic to excluded farmers",
      "The cost barrier and 'excludes the very producers it should celebrate' — sympathy for farmers combined with criticism of the system.",
      ["author's tone", "sympathetic", "critical"]),

    q(next_id(), "Medium",
      "The city's noise ordinance prohibits sound above 55 decibels after 10 PM. It is enforced against karaoke bars in poor neighborhoods. It is not enforced against construction sites owned by developers who fund political campaigns. The law is the same for everyone; its application is not.",
      "What is the author's tone?",
      ["Neutral", "Pointedly critical of selective enforcement", "Supportive of the ordinance", "Confused"],
      "Pointedly critical of selective enforcement",
      "The enforcement disparity based on wealth/connections and 'law is the same; application is not' — pointed criticism of unequal justice.",
      ["author's tone", "pointed", "critical"]),

    q(next_id(), "Medium",
      "The public hospital's emergency room has a sign that reads 'No patient shall be denied treatment regardless of ability to pay.' Below it, a smaller sign reads 'Please proceed to the billing office before discharge.' The first sign is the law. The second is the reality. Between them lies the gap where dignity goes to die.",
      "What is the author's tone?",
      ["Neutral", "Bitterly observant about the gap between law and practice", "Supportive of the hospital", "Indifferent"],
      "Bitterly observant about the gap between law and practice",
      "The two signs and 'where dignity goes to die' — bitter observation about how billing undermines the right to treatment.",
      ["author's tone", "bitter", "observant"]),

    q(next_id(), "Medium",
      "The youth employment program offers 'skills training' in resume writing and interview techniques. It does not offer jobs. The assumption — that unemployment is caused by inadequate resumes rather than inadequate job creation — is never examined. We train people to compete more effectively for positions that do not exist.",
      "What is the author's tone?",
      ["Supportive of the program", "Analytically critical of misdiagnosed problems", "Neutral", "Hostile to youth"],
      "Analytically critical of misdiagnosed problems",
      "'Assumption never examined' and 'compete for positions that do not exist' — analytical criticism of programs that address symptoms, not causes.",
      ["author's tone", "analytical", "critical"]),

    q(next_id(), "Medium",
      "The cooperative's success story is told and retold at development conferences — how a group of women transformed their community through collective enterprise. What is not told: the fifteen failed cooperatives in the same region, the structural conditions that made this one succeed where others could not, or the fact that its success has not been replicated despite numerous attempts.",
      "What is the author's tone?",
      ["Celebratory of the cooperative", "Skeptically contextualizing a success narrative", "Hostile", "Indifferent"],
      "Skeptically contextualizing a success narrative",
      "Noting what's untold (failures, unreplicability) — skeptical contextualization that questions whether one success proves a model works.",
      ["author's tone", "skeptical", "contextualizing"]),

    q(next_id(), "Medium",
      "The company's 'flexible work arrangement' allows employees to choose their hours — as long as they attend all meetings (scheduled by management at varying times), respond to messages within 30 minutes (at any hour), and meet deadlines that assume full-time availability. Flexibility, in this arrangement, flows in one direction only.",
      "What is the author's tone?",
      ["Supportive of the arrangement", "Ironic about one-sided flexibility", "Neutral", "Enthusiastic"],
      "Ironic about one-sided flexibility",
      "The constraints that negate flexibility and 'flows in one direction only' — irony about flexibility that benefits only the employer.",
      ["author's tone", "ironic"]),

    q(next_id(), "Medium",
      "The documentary about the fishing community won international acclaim for its 'authentic portrayal of resilience.' The fishermen featured in the film were paid ₱500 each for three months of filming access. The filmmaker's speaking fee at festivals discussing the film is ₱200,000 per appearance.",
      "What is the author's tone?",
      ["Impressed by the film", "Pointedly exposing extractive economics of storytelling", "Neutral", "Supportive"],
      "Pointedly exposing extractive economics of storytelling",
      "₱500 for subjects versus ₱200,000 for the filmmaker — pointed exposure of who profits from whose story.",
      ["author's tone", "pointed", "exposing"]),

    q(next_id(), "Medium",
      "The government's 'one-stop shop' for business permits requires visits to seven different windows, submission of 23 documents, and an average processing time of 45 days. The 'one stop' refers to the building, not the experience. Naming something convenient does not make it so.",
      "What is the author's tone?",
      ["Impressed by the system", "Sarcastically critical of misleading branding", "Neutral", "Supportive"],
      "Sarcastically critical of misleading branding",
      "Seven windows, 23 documents, 45 days versus 'one-stop shop' — sarcasm about a name that contradicts the reality.",
      ["author's tone", "sarcastic", "critical"]),

    q(next_id(), "Medium",
      "The elder statesman's advice to young activists — 'be patient, change takes time' — comes from a man who has held power for forty years and changed nothing. Patience, recommended by those who benefit from the status quo, is not wisdom — it is a request to stop making them uncomfortable.",
      "What is the author's tone?",
      ["Respectful of the elder", "Sharply critical of patience as a tool of power", "Neutral", "Supportive"],
      "Sharply critical of patience as a tool of power",
      "'Held power for forty years and changed nothing' and 'request to stop making them uncomfortable' — sharp criticism of patience weaponized by the powerful.",
      ["author's tone", "sharp", "critical"]),
]

# ============================================================
# ADDITIONAL HARD QUESTIONS (batch 4)
# ============================================================

extra_hard_4 = [
    q(next_id(), "Hard",
      "The 'evidence-based policy' framework sounds unimpeachable — who could argue against evidence? But evidence is not neutral. It is produced by those with funding, published by those with access, and interpreted by those with power. When the only evidence that counts is the evidence that institutions produce about themselves, 'evidence-based' becomes a synonym for 'self-justifying.'",
      "What is the author's tone?",
      ["Supportive of evidence-based policy", "Philosophically critical of how evidence is produced and used", "Neutral", "Anti-science"],
      "Philosophically critical of how evidence is produced and used",
      "Questioning who produces, publishes, and interprets evidence — philosophical criticism of the politics of knowledge production.",
      ["author's tone", "philosophical", "critical"]),

    q(next_id(), "Hard",
      "The social enterprise sells products made by marginalized women at 'fair trade' prices. The women receive 40% of the retail price — better than exploitative alternatives, certainly, but still less than half the value their labor creates. The enterprise's founder, who contributes no labor to production, receives the other 60%. Fair trade, it seems, is a relative term — relative to exploitation, anything looks fair.",
      "What is the author's tone?",
      ["Supportive of fair trade", "Critically questioning what 'fair' means in practice", "Neutral", "Hostile"],
      "Critically questioning what 'fair' means in practice",
      "The 40/60 split and 'relative to exploitation, anything looks fair' — critical questioning of whether 'fair trade' is truly fair.",
      ["author's tone", "critical", "questioning"]),

    q(next_id(), "Hard",
      "The museum's audio guide describes the colonial-era sugar hacienda as 'a testament to the ingenuity and enterprise of the planter class.' It does not describe the forced labor, the debt bondage, or the malnutrition of the workers whose bodies built the wealth the hacienda represents. Heritage tourism, when it celebrates only the powerful, is not preservation — it is propaganda with an admission fee.",
      "What is the author's tone?",
      ["Supportive of the museum", "Passionately critical of selective heritage narratives", "Neutral", "Academic"],
      "Passionately critical of selective heritage narratives",
      "'Propaganda with an admission fee' — passionate criticism of heritage presentation that celebrates oppressors while erasing the oppressed.",
      ["author's tone", "passionate", "critical"]),

    q(next_id(), "Hard",
      "The 'resilience training' workshop teaches government employees to manage stress through breathing exercises and positive affirmations. It does not address the understaffing that causes the stress, the unpaid overtime that compounds it, or the management practices that normalize it. Teaching individuals to cope with systemic dysfunction is cheaper than fixing the system — and it places responsibility for wellness on those least empowered to create it.",
      "What is the author's tone?",
      ["Supportive of resilience training", "Analytically critical of individualizing systemic problems", "Neutral", "Hostile"],
      "Analytically critical of individualizing systemic problems",
      "'Cheaper than fixing the system' and 'places responsibility on those least empowered' — analytical criticism of individual solutions to structural problems.",
      ["author's tone", "analytical", "critical"]),

    q(next_id(), "Hard",
      "The elected official's wealth declaration shows assets of ₱5 million. Public records show properties worth ₱200 million registered to immediate family members who have no independent income. The law requires officials to declare their assets. It does not require them to declare their family's assets. The gap between these two requirements is not an oversight — it is architecture.",
      "What is the author's tone?",
      ["Neutral", "Coldly accusatory about designed loopholes", "Supportive of the official", "Confused"],
      "Coldly accusatory about designed loopholes",
      "'Not an oversight — it is architecture' — cold accusation that the legal gap was deliberately designed to enable hidden wealth.",
      ["author's tone", "accusatory", "cold"]),

    q(next_id(), "Hard",
      "The 'community-driven development' model asks communities to identify their own priorities, design their own projects, and contribute their own labor. It does not ask why these communities lack basic services in the first place, why the government that collects their taxes does not provide them, or why self-help has become a substitute for state responsibility. Empowerment, in this model, is the freedom to do for yourself what your government should have done for you.",
      "What is the author's tone?",
      ["Supportive of community-driven development", "Critically questioning the ideology of self-help as policy", "Neutral", "Hostile to communities"],
      "Critically questioning the ideology of self-help as policy",
      "'Freedom to do for yourself what government should have done' — critical questioning of how 'empowerment' rhetoric masks state abandonment.",
      ["author's tone", "critical", "questioning"]),

    q(next_id(), "Hard",
      "The peace agreement's language is carefully calibrated to offend no one — which means it commits to nothing. 'Both parties acknowledge past grievances' (without specifying them). 'Both parties commit to future dialogue' (without scheduling it). 'Both parties envision a just resolution' (without defining justice). The agreement is a masterpiece of diplomatic ambiguity — which is another way of saying it is a beautifully written postponement of everything that matters.",
      "What is the author's tone?",
      ["Hopeful about peace", "Wearily contemptuous of empty diplomatic language", "Neutral", "Supportive"],
      "Wearily contemptuous of empty diplomatic language",
      "'Commits to nothing,' parenthetical exposures, and 'beautifully written postponement' — weary contempt for language designed to avoid substance.",
      ["author's tone", "weary", "contemptuous"]),

    q(next_id(), "Hard",
      "The child's essay about 'What I Want to Be When I Grow Up' said she wanted to be rich so her mother would not have to work three jobs. The teacher marked it as 'off-topic' — the assignment asked about careers, not economic critique. But the child had answered honestly: in her world, the purpose of a career is not self-actualization but family survival. The teacher's rubric had no category for that kind of truth.",
      "What is the author's tone?",
      ["Critical of the child", "Poignantly critical of systems that cannot recognize lived reality", "Neutral", "Supportive of the teacher"],
      "Poignantly critical of systems that cannot recognize lived reality",
      "'Off-topic' versus honest truth and 'no category for that kind of truth' — poignant criticism of educational frameworks that exclude poverty's reality.",
      ["author's tone", "poignant", "critical"]),

    q(next_id(), "Hard",
      "The 'smart farming' initiative provides sensors, drones, and data analytics to farmers who cannot afford fertilizer. The technology monitors soil moisture with precision while the farmer's children go to school without breakfast. We have built systems sophisticated enough to measure the exact nutrient content of soil but not compassionate enough to notice the hunger of the person standing on it.",
      "What is the author's tone?",
      ["Supportive of smart farming", "Bitterly critical of technological solutions that ignore human needs", "Neutral", "Anti-technology"],
      "Bitterly critical of technological solutions that ignore human needs",
      "Soil sensors versus hungry children and 'not compassionate enough to notice hunger' — bitter criticism of technology divorced from human welfare.",
      ["author's tone", "bitter", "critical"]),

    q(next_id(), "Hard",
      "The annual report's executive summary begins: 'Despite challenging market conditions, the company delivered strong results for shareholders.' Translated: despite laying off 2,000 workers, closing three factories, and cutting healthcare benefits, the stock price went up. 'Strong results' is a phrase that means different things depending on whether you own shares or used to own a job.",
      "What is the author's tone?",
      ["Supportive of the company", "Bitterly ironic about whose 'results' matter", "Neutral", "Confused"],
      "Bitterly ironic about whose 'results' matter",
      "The translation revealing human cost behind 'strong results' and 'depends on whether you own shares or a job' — bitter irony about corporate language.",
      ["author's tone", "bitter", "ironic"]),
]


# ============================================================
# FINAL MEDIUM BATCH (to reach 200)
# ============================================================

extra_medium_4 = [
    q(next_id(), "Medium", "The town's public market was demolished to make way for a modern commercial center. Vendors were promised stalls in the new building at 'affordable rates.' The rates turned out to be five times their previous rent. Most vendors now sell from makeshift stalls on the sidewalk outside the building they were promised a place in.", "What is the author's tone?", ["Supportive of modernization", "Sympathetically critical of broken promises", "Neutral", "Enthusiastic"], "Sympathetically critical of broken promises", "The promise-versus-reality gap and vendors on sidewalks outside their promised building — sympathy for vendors, criticism of the process.", ["author's tone", "sympathetic", "critical"]),
    q(next_id(), "Medium", "The company's annual team-building retreat costs ₱2 million. Employees report that it does not improve teamwork, does not address workplace conflicts, and primarily benefits the resort owner. When asked what would actually improve morale, employees consistently answer: higher pay. But higher pay does not produce Instagram-worthy content.", "What is the author's tone?", ["Supportive of team-building", "Wryly critical of performative corporate culture", "Neutral", "Hostile"], "Wryly critical of performative corporate culture", "'Does not produce Instagram-worthy content' — wry criticism of spending on optics rather than substance.", ["author's tone", "wry", "critical"]),
    q(next_id(), "Medium", "The heritage conservation award went to a developer who preserved the facade of a 200-year-old building while gutting its interior and converting it into a luxury hotel. The facade — two inches of original stone — is all that remains of the original structure. Conservation, in this case, is a mask worn by demolition.", "What is the author's tone?", ["Impressed by the conservation", "Bitingly ironic about facade preservation", "Neutral", "Supportive"], "Bitingly ironic about facade preservation", "'Two inches of original stone' and 'mask worn by demolition' — biting irony about preservation that preserves nothing meaningful.", ["author's tone", "ironic", "biting"]),
    q(next_id(), "Medium", "The public consultation received 500 written submissions opposing the project and 3 supporting it. The project was approved. The decision document states that 'public input was carefully considered and weighed against technical and economic factors.' Translation: we asked, you answered, and we did what we planned to do anyway.", "What is the author's tone?", ["Neutral", "Cynically critical of meaningless consultation", "Supportive of the decision", "Confused"], "Cynically critical of meaningless consultation", "500 vs 3 submissions, approval anyway, and the 'translation' — cynical criticism of consultation as theater.", ["author's tone", "cynical", "critical"]),
    q(next_id(), "Medium", "The indigenous community's forest has been declared a 'protected area' by the government. This means the community can no longer hunt, gather, or farm on land they have managed sustainably for centuries. The logging company that applied for a concession in the adjacent area, however, received its permit within 30 days.", "What is the author's tone?", ["Supportive of protection", "Indignant about double standards", "Neutral", "Confused"], "Indignant about double standards", "Community restricted from sustainable use while loggers get permits — indignation at protection that restricts indigenous people but not industry.", ["author's tone", "indignant"]),
    q(next_id(), "Medium", "The school's 'character education' program teaches honesty, integrity, and respect through weekly assemblies. The same school tolerates a grading system where students with connected parents receive preferential treatment, where complaints about teacher misconduct are buried, and where the principal's nephew was admitted despite failing the entrance exam.", "What is the author's tone?", ["Supportive of character education", "Ironic about institutional hypocrisy", "Neutral", "Hostile to schools"], "Ironic about institutional hypocrisy", "Teaching honesty while practicing favoritism — irony about institutions that preach values they do not practice.", ["author's tone", "ironic"]),
    q(next_id(), "Medium", "The flood control project was designed for a '25-year flood event.' Climate scientists warned that rainfall patterns have changed and that 50-year events now occur every decade. The engineers acknowledged this but explained that the budget only covered 25-year protection. We are building infrastructure for a climate that no longer exists.", "What is the author's tone?", ["Supportive of the project", "Gravely critical of inadequate planning", "Neutral", "Optimistic"], "Gravely critical of inadequate planning", "'Infrastructure for a climate that no longer exists' — grave criticism of planning based on outdated assumptions.", ["author's tone", "grave", "critical"]),
    q(next_id(), "Medium", "The volunteer fire brigade responds to an average of 200 calls per year with equipment donated in 1995. They have requested new equipment annually for a decade. Each request is 'under review.' Last month, the municipal government purchased a new SUV for the mayor's office. Priorities, as always, are clearly communicated through budgets rather than speeches.", "What is the author's tone?", ["Neutral", "Bitterly critical of misplaced priorities", "Supportive of the mayor", "Indifferent"], "Bitterly critical of misplaced priorities", "Decade of denied requests versus new SUV and 'priorities communicated through budgets' — bitter criticism of where money actually goes.", ["author's tone", "bitter", "critical"]),
    q(next_id(), "Medium", "The 'green building' certification was awarded based on energy-efficient lighting and low-flow toilets. The building's construction required demolishing a mangrove forest, its materials were shipped from three continents, and its parking garage accommodates 500 cars. Green, in architecture as in politics, is a flexible color.", "What is the author's tone?", ["Impressed by the certification", "Sarcastically critical of superficial environmentalism", "Neutral", "Supportive"], "Sarcastically critical of superficial environmentalism", "Efficient toilets versus destroyed mangroves and 'green is a flexible color' — sarcasm about certification that ignores larger environmental harm.", ["author's tone", "sarcastic", "critical"]),
    q(next_id(), "Medium", "The community health worker walks three hours each way to reach her most remote patients. She carries vaccines in a cooler, delivers babies by flashlight, and treats infections with whatever supplies she can scrounge. Her monthly allowance is ₱3,000 — less than the daily rate of the consultant who designed the health program she implements.", "What is the author's tone?", ["Neutral", "Admiring of the worker while indignant about compensation disparity", "Critical of the worker", "Indifferent"], "Admiring of the worker while indignant about compensation disparity", "Heroic details versus ₱3,000 and the consultant comparison — admiration for the worker, indignation at the system's values.", ["author's tone", "admiring", "indignant"]),
    q(next_id(), "Medium", "The anti-corruption hotline received 10,000 calls last year. Of these, 8,500 were investigated. Of those investigated, 200 resulted in formal charges. Of those charged, 15 were convicted. The hotline's existence proves the government takes corruption seriously. Its results prove something else entirely.", "What is the author's tone?", ["Supportive of the hotline", "Dryly ironic about the gap between process and outcomes", "Neutral", "Hostile"], "Dryly ironic about the gap between process and outcomes", "The funnel (10,000 → 15 convictions) and 'proves something else entirely' — dry irony about a system that processes complaints without producing justice.", ["author's tone", "ironic", "dry"]),
    q(next_id(), "Medium", "The children's art program was defunded to redirect resources toward 'core academic subjects.' Test scores in those subjects have not improved. What has changed: children no longer have a space where failure is safe, where expression is valued, and where the student who struggles with math can discover she excels at something else.", "What is the author's tone?", ["Supportive of the defunding", "Mourning the loss while criticizing the decision", "Neutral", "Indifferent"], "Mourning the loss while criticizing the decision", "No improvement in scores but loss of safe creative space — mourning what was taken combined with criticism of the rationale.", ["author's tone", "mourning", "critical"]),
]

# ============================================================
# FINAL HARD BATCH (to reach 200)
# ============================================================

extra_hard_5 = [
    q(next_id(), "Hard", "The 'capacity building' workshop taught community leaders to write project proposals in the format required by international donors. It did not teach them why their community needs external funding in the first place, why their government does not provide basic services, or why the solution to local problems must be written in English and submitted to an office in Geneva. Capacity building, in this model, is the capacity to ask for help in the language of those who have it.", "What is the author's tone?", ["Supportive of capacity building", "Critically deconstructing the aid paradigm", "Neutral", "Hostile to communities"], "Critically deconstructing the aid paradigm", "'Capacity to ask for help in the language of those who have it' — critical deconstruction of how aid systems reproduce dependency.", ["author's tone", "critical", "deconstructive"]),
    q(next_id(), "Hard", "The city's 'inclusive playground' was designed with wheelchair ramps, sensory panels, and accessible swings. It was built in a gated subdivision accessible only to residents. Inclusion, apparently, has a membership fee.", "What is the author's tone?", ["Impressed by the design", "Acidly ironic about exclusive inclusion", "Neutral", "Supportive"], "Acidly ironic about exclusive inclusion", "Inclusive design in an exclusive location and 'inclusion has a membership fee' — acid irony about accessibility limited to the privileged.", ["author's tone", "ironic", "acid"]),
    q(next_id(), "Hard", "The development agency measures success in 'lives touched' — a metric so vague it could include anyone who received a pamphlet, attended a seminar, or was counted in a survey. By this measure, handing a flyer to a person on the street constitutes development impact. The metric exists not to measure change but to justify budgets — and at this, it is remarkably effective.", "What is the author's tone?", ["Impressed by the metric", "Contemptuously analytical about meaningless measurement", "Neutral", "Supportive"], "Contemptuously analytical about meaningless measurement", "'Lives touched' deconstructed to absurdity and 'exists to justify budgets' — contemptuous analysis of metrics designed to impress rather than inform.", ["author's tone", "contemptuous", "analytical"]),
    q(next_id(), "Hard", "The farmer's suicide was reported as an individual tragedy — mental health issues, personal problems, isolation. What was not reported: the crop failure caused by climate change, the debt from seeds that did not grow, the bank's foreclosure notice, or the government program that promised support and delivered paperwork. Individual tragedies, examined closely, often reveal systemic murders committed slowly, by policy rather than by hand.", "What is the author's tone?", ["Neutral", "Indignant about systemic violence disguised as individual failure", "Supportive of the reporting", "Academic"], "Indignant about systemic violence disguised as individual failure", "'Systemic murders committed slowly, by policy' — indignation at framing structural violence as personal tragedy.", ["author's tone", "indignant", "critical"]),
    q(next_id(), "Hard", "The 'world-class city' vision includes a new airport, a subway system, and a waterfront development. It does not include the 3 million informal settlers who will be displaced to build them, the communities that will lose access to the waterfront they have fished for generations, or any plan for where these people will go. World-class, in urban planning, often means 'designed for visitors, not residents.'", "What is the author's tone?", ["Supportive of the vision", "Critically exposing whose city is being built", "Neutral", "Enthusiastic"], "Critically exposing whose city is being built", "3 million displaced, lost fishing access, no relocation plan — critical exposure of development that serves visitors while displacing residents.", ["author's tone", "critical", "exposing"]),
    q(next_id(), "Hard", "The textbook's chapter on Philippine history devotes fifteen pages to the American colonial period's 'contributions' — public education, infrastructure, democratic institutions. It devotes one paragraph to the Philippine-American War, in which 200,000 to 1,000,000 Filipinos died. Proportion, in textbook design, is an editorial choice — and this one speaks volumes about whose perspective shapes what children learn.", "What is the author's tone?", ["Neutral", "Pointedly critical of colonial apologetics in education", "Supportive of the textbook", "Academic"], "Pointedly critical of colonial apologetics in education", "Fifteen pages of 'contributions' versus one paragraph of mass death — pointed criticism of how textbooks minimize colonial violence.", ["author's tone", "pointed", "critical"]),
    q(next_id(), "Hard", "The microfinance program charges 24% annual interest to borrowers earning less than ₱10,000 monthly. It calls this 'financial inclusion.' The borrowers call it something else. When the poor must pay more to access money than the rich pay for the same service, 'inclusion' is just a polite word for a system that profits from those with the fewest alternatives.", "What is the author's tone?", ["Supportive of microfinance", "Bitterly critical of exploitation branded as inclusion", "Neutral", "Academic"], "Bitterly critical of exploitation branded as inclusion", "'Financial inclusion' versus 24% interest and 'profits from those with fewest alternatives' — bitter criticism of predatory lending disguised as empowerment.", ["author's tone", "bitter", "critical"]),
    q(next_id(), "Hard", "The 'participatory mapping' exercise asked indigenous communities to draw their ancestral boundaries on government-issued maps. The communities complied, sharing knowledge accumulated over centuries. The maps were then used by mining companies to identify exactly where to file concession applications. Participation, without protection, is just intelligence-gathering by another name.", "What is the author's tone?", ["Supportive of participatory mapping", "Indignant about weaponized participation", "Neutral", "Academic"], "Indignant about weaponized participation", "Community knowledge used against them and 'intelligence-gathering by another name' — indignation at participation exploited for extraction.", ["author's tone", "indignant", "critical"]),
    q(next_id(), "Hard", "The wellness app tracks sleep, steps, heart rate, and stress levels with impressive precision. It cannot track the anxiety caused by job insecurity, the insomnia caused by financial worry, or the elevated heart rate caused by a toxic workplace. It measures the body's response to problems it cannot name, then recommends meditation. Technology that monitors symptoms while ignoring causes is not healthcare — it is surveillance with a soothing interface.", "What is the author's tone?", ["Supportive of wellness apps", "Critically analytical about technology that individualizes systemic problems", "Neutral", "Anti-technology"], "Critically analytical about technology that individualizes systemic problems", "'Surveillance with a soothing interface' — critical analysis of how wellness tech monitors effects while ignoring structural causes.", ["author's tone", "critical", "analytical"]),
    q(next_id(), "Hard", "The elected official's legacy project — a massive sports complex — will be completed six months before the next election. It will bear his name in letters visible from the highway. The community's request for a dialysis center, submitted eight years ago, remains 'under study.' Monuments to politicians are built with public money on public schedules; services for the public wait indefinitely.", "What is the author's tone?", ["Supportive of the sports complex", "Bitterly critical of self-serving political priorities", "Neutral", "Indifferent"], "Bitterly critical of self-serving political priorities", "Sports complex before election versus 8-year-old dialysis request — bitter criticism of politicians who build monuments to themselves while ignoring community needs.", ["author's tone", "bitter", "critical"]),
]


# ============================================================
# MERGE AND OUTPUT
# ============================================================

new_questions = extra_medium + extra_medium_2 + extra_hard + extra_hard_2 + extra_hard_3 + extra_medium_3 + extra_hard_4 + extra_medium_4 + extra_hard_5
all_questions = existing + new_questions

# Summary
easy = [q for q in all_questions if q["difficulty"] == "Easy"]
medium = [q for q in all_questions if q["difficulty"] == "Medium"]
hard = [q for q in all_questions if q["difficulty"] == "Hard"]

print(f"Total questions: {len(all_questions)}")
print(f"  Easy:   {len(easy)}")
print(f"  Medium: {len(medium)}")
print(f"  Hard:   {len(hard)}")

if len(all_questions) < 600:
    print(f"\n⚠️  WARNING: Only {len(all_questions)} questions. Target is 600.")

with open(QUESTIONS_PATH, "w", encoding="utf-8") as f:
    json.dump(all_questions, f, indent=2, ensure_ascii=False)

print(f"\nWritten to: {QUESTIONS_PATH}")
