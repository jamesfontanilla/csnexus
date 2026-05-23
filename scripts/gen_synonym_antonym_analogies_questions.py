"""
Generate 600 synonym and antonym analogy questions for the Analytical Ability module.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/analytical-ability/word-analogy/synonym-and-antonym-analogies/questions.json
"""
import json
import random
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "seed" / "questions" / "analytical-ability" / "word-analogy" / "synonym-and-antonym-analogies" / "questions.json"

B = {
    "subtest": "Analytical Ability",
    "module": "Word Analogy",
    "subtopic": "Synonym and Antonym Analogies",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}

# ---------------------------------------------------------------------------
# Word pair banks: (word_a, word_b) where A and B are synonyms
# ---------------------------------------------------------------------------

EASY_SYNONYMS = [
    ("brave","courageous"),("happy","joyful"),("big","large"),("small","tiny"),
    ("quick","fast"),("slow","sluggish"),("angry","mad"),("scared","frightened"),
    ("silent","quiet"),("loud","noisy"),("glad","happy"),("thin","slim"),
    ("smart","intelligent"),("sick","ill"),("calm","peaceful"),("brave","bold"),
    ("pretty","beautiful"),("tired","exhausted"),("funny","humorous"),("kind","nice"),
    ("correct","right"),("wealthy","rich"),("huge","enormous"),("scared","afraid"),
    ("rapid","swift"),("joyful","cheerful"),("honest","truthful"),("repair","fix"),
    ("shout","yell"),("grab","seize"),("leap","jump"),("shut","close"),
    ("gaze","stare"),("toss","throw"),("damp","moist"),("chilly","cold"),
    ("odd","strange"),("rip","tear"),("weary","tired"),("dull","boring"),
    ("wealthy","affluent"),("fearful","afraid"),("assist","aid"),("vanish","disappear"),
    ("foe","enemy"),("vacant","empty"),("sturdy","strong"),("loyal","faithful"),
    ("clever","smart"),("wealthy","prosperous"),("enormous","gigantic"),
    ("furious","enraged"),("swift","rapid"),("depart","leave"),("conceal","hide"),
    ("hazard","danger"),("cease","stop"),("imitate","copy"),
]

EASY_ANTONYMS = [
    ("hot","cold"),("fast","slow"),("happy","sad"),("strong","weak"),
    ("old","young"),("clean","dirty"),("open","close"),("love","hate"),
    ("win","lose"),("true","false"),("hard","soft"),("empty","full"),
    ("near","far"),("early","late"),("cheap","expensive"),("accept","refuse"),
    ("arrive","depart"),("bright","dim"),("awake","asleep"),("noisy","quiet"),
    ("increase","decrease"),("smooth","rough"),("polite","rude"),("remember","forget"),
    ("laugh","cry"),("build","destroy"),("borrow","lend"),("reward","punish"),
    ("appear","disappear"),("gather","scatter"),("narrow","wide"),("loose","tight"),
    ("major","minor"),("advance","retreat"),("innocent","guilty"),("bitter","sweet"),
    ("visible","invisible"),("generous","stingy"),("expand","shrink"),("praise","blame"),
    ("ascend","descend"),("permit","forbid"),("temporary","permanent"),
    ("victory","defeat"),("abundant","scarce"),("agree","disagree"),
    ("brave","timid"),("genuine","fake"),("generous","greedy"),
    ("optimistic","pessimistic"),("flexible","rigid"),("ancient","modern"),
    ("majority","minority"),("maximum","minimum"),("voluntary","compulsory"),
    ("high","low"),("light","dark"),("rich","poor"),("tall","short"),
]

MEDIUM_SYNONYMS = [
    ("commence","initiate"),("diligent","industrious"),("sufficient","adequate"),
    ("concur","agree"),("allocate","distribute"),("facilitate","enable"),
    ("collaborate","cooperate"),("evaluate","assess"),("stipulate","specify"),
    ("disseminate","distribute"),("pertinent","relevant"),("comprehensive","thorough"),
    ("preliminary","initial"),("concurrent","simultaneous"),("ambiguous","vague"),
    ("mitigate","alleviate"),("prudent","cautious"),("meticulous","scrupulous"),
    ("tenacious","persistent"),("pragmatic","practical"),("arduous","strenuous"),
    ("elicit","extract"),("endorse","advocate"),("resilient","robust"),
    ("exemplary","outstanding"),("expedite","accelerate"),("consolidate","merge"),
    ("scrutinize","examine"),("reprimand","scold"),("delegate","assign"),
    ("innate","inherent"),("plausible","credible"),("corroborate","confirm"),
    ("amiable","friendly"),("frugal","thrifty"),("obsolete","outdated"),
    ("sporadic","intermittent"),("admonish","warn"),("clandestine","covert"),
    ("vindicate","justify"),("acquiesce","consent"),("bolster","reinforce"),
    ("curtail","reduce"),("substantiate","verify"),("emulate","imitate"),
    ("ratify","approve"),("advocate","champion"),("alleviate","ease"),
    ("relinquish","surrender"),("impeccable","flawless"),("revere","respect"),
    ("coerce","compel"),("rescind","revoke"),("diminish","lessen"),
    ("sanction","authorize"),("defer","postpone"),("rebuke","reprimand"),
    ("circumvent","bypass"),("rectify","correct"),("exemplify","illustrate"),
]

MEDIUM_ANTONYMS = [
    ("transparent","opaque"),("mandatory","optional"),("promote","demote"),
    ("centralize","decentralize"),("comply","violate"),("approve","reject"),
    ("permanent","temporary"),("surplus","deficit"),("formal","informal"),
    ("transparent","secretive"),("augment","diminish"),("affluent","impoverished"),
    ("lenient","strict"),("objective","subjective"),("proactive","reactive"),
    ("benevolent","malevolent"),("coherent","incoherent"),("prolific","barren"),
    ("gregarious","reclusive"),("verbose","concise"),("authentic","counterfeit"),
    ("abundant","meager"),("trivial","significant"),("autonomous","dependent"),
    ("impartial","partisan"),("affluent","indigent"),("benign","malignant"),
    ("unanimous","divided"),("affluence","poverty"),("integral","peripheral"),
    ("tangible","intangible"),("homogeneous","heterogeneous"),("lucid","obscure"),
    ("altruistic","selfish"),("exonerate","incriminate"),("affluent","destitute"),
    ("prolific","unproductive"),("ephemeral","eternal"),("benevolent","malicious"),
    ("candid","deceitful"),("lucrative","unprofitable"),("conspicuous","inconspicuous"),
    ("prolific","sparse"),("exacerbate","ameliorate"),("austere","lavish"),
    ("coherent","disjointed"),("succinct","verbose"),("dormant","active"),
    ("prolific","scarce"),("inclusive","exclusive"),("feasible","impractical"),
    ("voluntary","involuntary"),("diligent","indolent"),("nascent","mature"),
    ("explicit","implicit"),("convergent","divergent"),("equitable","inequitable"),
    ("dogmatic","open-minded"),("prolific","negligible"),("archaic","contemporary"),
]

HARD_SYNONYMS = [
    ("loquacious","verbose"),("sycophantic","obsequious"),("magnanimous","munificent"),
    ("recalcitrant","intractable"),("perfunctory","cursory"),("pusillanimous","craven"),
    ("sagacious","perspicacious"),("truculent","bellicose"),("vituperate","excoriate"),
    ("obdurate","adamant"),("querulous","petulant"),("insouciant","nonchalant"),
    ("propitiate","mollify"),("enervate","debilitate"),("impecunious","indigent"),
    ("supercilious","haughty"),("inimical","deleterious"),("contumacious","recalcitrant"),
    ("perspicuous","lucid"),("ineffable","indescribable"),("indefatigable","tireless"),
    ("punctilious","fastidious"),("equanimity","composure"),("opprobrium","ignominy"),
    ("impugn","assail"),("vitriolic","caustic"),("lugubrious","doleful"),
    ("mendacious","prevaricating"),("imperturbable","unflappable"),("concomitant","attendant"),
    ("acrimonious","rancorous"),("circumlocution","periphrasis"),("malfeasance","misconduct"),
    ("soporific","sedative"),("calumny","defamation"),("truculent","pugnacious"),
    ("nugatory","inconsequential"),("inveterate","entrenched"),("exigent","pressing"),
    ("impervious","impenetrable"),("redolent","fragrant"),("inimitable","matchless"),
    ("inexorable","relentless"),("inscrutable","enigmatic"),("ineluctable","inevitable"),
    ("contrite","penitent"),("sententious","pithy"),("propitious","auspicious"),
    ("perspicacity","acumen"),("invidious","odious"),("unctuous","sycophantic"),
    ("meretricious","specious"),("inveigle","beguile"),("impecunious","necessitous"),
    ("vitiate","impair"),("abnegate","renounce"),("excoriate","lambaste"),
    ("inimical","antagonistic"),("obfuscate","obscure"),("impugn","gainsay"),
    ("effulgent","resplendent"),("pusillanimous","timorous"),("exiguous","scanty"),
    ("contumely","opprobrium"),("ineluctable","inexorable"),("captious","censorious"),
    ("importunate","insistent"),("trenchant","incisive"),("indefeasible","irrevocable"),
    ("ineffable","inexpressible"),("malediction","imprecation"),("inculcate","instill"),
    ("extemporaneous","impromptu"),("inchoate","rudimentary"),("desultory","haphazard"),
    ("implacable","inexorable"),("vituperative","scathing"),("anodyne","palliative"),
    ("sagacious","sapient"),("propinquity","proximity"),("mendacious","duplicitous"),
    ("obsequious","fawning"),("pulchritude","comeliness"),("circumspect","judicious"),
    ("insouciance","nonchalance"),("encomium","panegyric"),("probity","rectitude"),
    ("perspicacious","discerning"),("inveterate","habitual"),("opprobrium","obloquy"),
    ("exigency","urgency"),("impecunious","penurious"),("calumniate","defame"),
    ("contumacious","insubordinate"),("inimitable","peerless"),("equivocate","prevaricate"),
    ("perfidious","treacherous"),("indefatigable","untiring"),("perspicuous","transparent"),
    ("incontrovertible","irrefutable"),("incorrigible","irredeemable"),
    ("ineluctable","unavoidable"),("indefeasible","unassailable"),
    ("ineffable","unspeakable"),("inveterate","chronic"),
]

HARD_ANTONYMS = [
    ("parsimonious","profligate"),("ephemeral","perpetual"),("sanguine","despondent"),
    ("garrulous","laconic"),("munificent","penurious"),("mellifluous","cacophonous"),
    ("surreptitious","overt"),("prodigal","abstemious"),("limpid","turbid"),
    ("ebullient","phlegmatic"),("prolixity","brevity"),("temerity","circumspection"),
    ("alacrity","reluctance"),("surfeit","dearth"),("magniloquent","understated"),
    ("sycophancy","candor"),("ameliorate","exacerbate"),("pernicious","innocuous"),
    ("inchoate","consummate"),("fecund","sterile"),("propinquity","remoteness"),
    ("plethoric","exiguous"),("sedulous","desultory"),("apposite","inapposite"),
    ("dilatory","expeditious"),("risible","solemn"),("munificent","niggardly"),
    ("voluble","taciturn"),("plangent","muted"),("recondite","accessible"),
    ("halcyon","tumultuous"),("protean","immutable"),("assiduous","perfunctory"),
    ("diffuse","concentrated"),("specious","cogent"),("plethora","paucity"),
    ("sycophantic","forthright"),("ossified","flexible"),("venal","incorruptible"),
    ("salubrious","insalubrious"),("perspicuous","abstruse"),("irascible","placid"),
    ("heterodox","orthodox"),("abstemious","intemperate"),("sanguine","saturnine"),
    ("prolix","laconic"),("magnanimous","vindictive"),("ascetic","sybaritic"),
    ("loquacious","reticent"),("ephemeral","sempiternal"),("parochial","cosmopolitan"),
    ("sycophantic","autonomous"),("recondite","patent"),("turgid","austere"),
    ("peripatetic","sedentary"),("munificent","parsimonious"),("pellucid","turbid"),
    ("ebullient","lugubrious"),("prodigious","negligible"),("quiescent","frenetic"),
    ("alacrity","torpor"),("garrulous","terse"),("truculent","irenic"),
    ("supererogatory","obligatory"),("mellifluous","strident"),("surreptitious","flagrant"),
    ("profligate","provident"),("recalcitrant","amenable"),("querulous","complaisant"),
    ("sanguine","morose"),("verisimilitude","implausibility"),("plangent","pianissimo"),
    ("insipid","piquant"),("obdurate","yielding"),("fecund","arid"),
    ("laconic","prolix"),("magniloquent","laconic"),("ebullience","apathy"),
    ("supine","vigilant"),("penurious","munificent"),("sycophantic","imperious"),
    ("risible","lugubrious"),("plethoric","exiguous"),
]

# ---------------------------------------------------------------------------
# Distractor banks for generating plausible wrong answers
# ---------------------------------------------------------------------------

EASY_DISTRACTORS = [
    "angry","sad","tired","bored","weak","slow","dark","heavy","bright","sharp",
    "kind","mean","ugly","rude","deep","flat","long","wide","short","thin",
    "hard","soft","warm","cool","dry","wet","old","new","good","bad",
    "strong","gentle","rough","smooth","loud","quiet","fast","dull","plain",
    "simple","complex","cheap","free","safe","wild","calm","mild","harsh","bold",
]

MEDIUM_DISTRACTORS = [
    "efficient","productive","strategic","systematic","progressive","conservative",
    "moderate","extreme","flexible","stable","dynamic","static","formal","casual",
    "abstract","concrete","theoretical","practical","subjective","objective",
    "proactive","passive","inclusive","selective","comprehensive","partial",
    "preliminary","final","concurrent","sequential","mandatory","optional",
    "transparent","ambiguous","coherent","fragmented","resilient","vulnerable",
    "autonomous","dependent","integral","peripheral","tangible","abstract",
    "lucrative","costly","feasible","impractical","equitable","biased",
]

HARD_DISTRACTORS = [
    "perspicacious","obtuse","sanguine","morose","truculent","placid",
    "munificent","parsimonious","ephemeral","perpetual","loquacious","taciturn",
    "ebullient","phlegmatic","recondite","patent","halcyon","tumultuous",
    "protean","immutable","sedulous","desultory","apposite","inapposite",
    "salubrious","deleterious","pellucid","turbid","fecund","sterile",
    "magniloquent","understated","surreptitious","overt","prodigal","abstemious",
    "contrite","impenitent","propitious","inauspicious","exigent","trivial",
    "indefatigable","indolent","punctilious","perfunctory","implacable","clement",
]


# ---------------------------------------------------------------------------
# Question generation logic
# ---------------------------------------------------------------------------

def _make_synonym_question(
    pair1: tuple[str, str],
    pair2: tuple[str, str],
    distractors: list[str],
    rng: random.Random,
) -> tuple[str, list[str], str, str, list[str]]:
    """Build a synonym analogy question from two synonym pairs."""
    a1, b1 = pair1[0].capitalize(), pair1[1].capitalize()
    a2, b2 = pair2[0].capitalize(), pair2[1].capitalize()

    question = f"{a1} : {b1} :: {a2} : _____"
    answer = b2

    # Pick 3 distractors that aren't the answer
    pool = [d.capitalize() for d in distractors if d.lower() != b2.lower() and d.lower() != a2.lower()]
    chosen = rng.sample(pool, min(3, len(pool)))
    while len(chosen) < 3:
        chosen.append("None")

    choices = chosen + [answer]
    rng.shuffle(choices)

    explanation = (
        f"{a1} means the same as {b1}. "
        f"{a2} means the same as {b2}. Both pairs are synonyms."
    )
    tags = ["word analogy", "synonyms"]
    return question, choices, answer, explanation, tags


def _make_antonym_question(
    pair1: tuple[str, str],
    pair2: tuple[str, str],
    distractors: list[str],
    rng: random.Random,
) -> tuple[str, list[str], str, str, list[str]]:
    """Build an antonym analogy question from two antonym pairs."""
    a1, b1 = pair1[0].capitalize(), pair1[1].capitalize()
    a2, b2 = pair2[0].capitalize(), pair2[1].capitalize()

    question = f"{a1} : {b1} :: {a2} : _____"
    answer = b2

    pool = [d.capitalize() for d in distractors if d.lower() != b2.lower() and d.lower() != a2.lower()]
    chosen = rng.sample(pool, min(3, len(pool)))
    while len(chosen) < 3:
        chosen.append("None")

    choices = chosen + [answer]
    rng.shuffle(choices)

    explanation = (
        f"{a1} is the opposite of {b1}. "
        f"{a2} is the opposite of {b2}. Both pairs are antonyms."
    )
    tags = ["word analogy", "antonyms"]
    return question, choices, answer, explanation, tags


def generate_questions(
    syn_pairs: list[tuple[str, str]],
    ant_pairs: list[tuple[str, str]],
    distractors: list[str],
    count: int,
    difficulty: str,
    rng: random.Random,
) -> list[dict]:
    """Generate `count` questions split evenly between synonym and antonym types."""
    questions = []
    half = count // 2

    # Generate synonym questions
    syn_shuffled = list(syn_pairs)
    rng.shuffle(syn_shuffled)
    for i in range(half):
        p1 = syn_shuffled[i % len(syn_shuffled)]
        p2 = syn_shuffled[(i + 1) % len(syn_shuffled)]
        # Ensure pairs are different
        if p1 == p2:
            p2 = syn_shuffled[(i + 2) % len(syn_shuffled)]
        q, choices, answer, explanation, tags = _make_synonym_question(
            p1, p2, distractors, rng
        )
        questions.append((q, choices, answer, explanation, tags))

    # Generate antonym questions
    ant_shuffled = list(ant_pairs)
    rng.shuffle(ant_shuffled)
    for i in range(count - half):
        p1 = ant_shuffled[i % len(ant_shuffled)]
        p2 = ant_shuffled[(i + 1) % len(ant_shuffled)]
        if p1 == p2:
            p2 = ant_shuffled[(i + 2) % len(ant_shuffled)]
        q, choices, answer, explanation, tags = _make_antonym_question(
            p1, p2, distractors, rng
        )
        questions.append((q, choices, answer, explanation, tags))

    rng.shuffle(questions)
    return questions


def main() -> None:
    rng = random.Random(42)  # Fixed seed for reproducibility

    easy_qs = generate_questions(
        EASY_SYNONYMS, EASY_ANTONYMS, EASY_DISTRACTORS, 200, "Easy", rng
    )
    medium_qs = generate_questions(
        MEDIUM_SYNONYMS, MEDIUM_ANTONYMS, MEDIUM_DISTRACTORS, 200, "Medium", rng
    )
    hard_qs = generate_questions(
        HARD_SYNONYMS, HARD_ANTONYMS, HARD_DISTRACTORS, 200, "Hard", rng
    )

    all_questions = []
    idx = 1
    for difficulty, bank in [("Easy", easy_qs), ("Medium", medium_qs), ("Hard", hard_qs)]:
        for q, choices, answer, explanation, tags in bank:
            all_questions.append({
                "id": idx,
                **B,
                "difficulty": difficulty,
                "question": q,
                "choices": choices,
                "answer": answer,
                "explanation": explanation,
                "tags": tags,
            })
            idx += 1

    assert len(all_questions) == 600, f"Expected 600, got {len(all_questions)}"

    # Validate all answers are in choices
    for q in all_questions:
        assert q["answer"] in q["choices"], (
            f"Answer '{q['answer']}' not in choices for Q{q['id']}: {q['choices']}"
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(all_questions, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {len(all_questions)} questions to {OUTPUT}")


if __name__ == "__main__":
    main()
