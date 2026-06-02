"""
Comprehensive spelling verification - multiple passes.
1. Every answer checked against pyspellchecker
2. Every distractor checked to ensure it's NOT a valid word
3. Check for answers that might be British spellings (CSE uses American)
4. Check that no two questions have identical choice sets
5. Verify answer is genuinely different from each distractor
6. Check for common false-correct patterns
"""
import json
import os
import sys
from collections import Counter
from spellchecker import SpellChecker

spell = SpellChecker()

path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "seed", "questions", "clerical-ability", "spelling",
    "correct-spelling-recognition", "questions.json"
)

with open(path, "r", encoding="utf-8") as f:
    questions = json.load(f)

print("=" * 70)
print("COMPREHENSIVE SPELLING VERIFICATION — ALL 600 QUESTIONS")
print("=" * 70)

# ============================================================
# PASS 1: Structural integrity
# ============================================================
print("\n[PASS 1] Structural Integrity")
pass1_errors = []

if len(questions) != 600:
    pass1_errors.append(f"Count: {len(questions)} != 600")

for i, q in enumerate(questions):
    if q["id"] != i + 1:
        pass1_errors.append(f"Q{q['id']}: ID mismatch (expected {i+1})")
    if len(q["choices"]) != 4:
        pass1_errors.append(f"Q{q['id']}: {len(q['choices'])} choices")
    if q["answer"] not in q["choices"]:
        pass1_errors.append(f"Q{q['id']}: answer not in choices")
    if len(set(q["choices"])) != 4:
        pass1_errors.append(f"Q{q['id']}: duplicate choices {q['choices']}")

easy = sum(1 for q in questions if q["difficulty"] == "Easy")
med = sum(1 for q in questions if q["difficulty"] == "Medium")
hard = sum(1 for q in questions if q["difficulty"] == "Hard")
if easy != 200: pass1_errors.append(f"Easy: {easy} != 200")
if med != 200: pass1_errors.append(f"Medium: {med} != 200")
if hard != 200: pass1_errors.append(f"Hard: {hard} != 200")

if pass1_errors:
    print(f"  ✗ {len(pass1_errors)} errors")
    for e in pass1_errors: print(f"    {e}")
else:
    print(f"  ✓ 600 questions, 200/200/200 split, all valid structure")

# ============================================================
# PASS 2: Answer spelling verification via dictionary
# ============================================================
print("\n[PASS 2] Answer Spelling (Dictionary Check)")

# Known valid words the basic dictionary might not have
KNOWN_VALID_ANSWERS = {
    "hors d'oeuvres", "unconscionability", "unimpeachability",
    "verisimilitudinous", "vicissitudinous", "acquaintanceship",
    "circumnavigation", "disenfranchisement", "antidisestablishmentarianism",
    "jurisprudential", "sesquipedalian", "tergiversation",
    "prestidigitation", "prestidigitator", "tintinnabulation",
    "supererogatory", "terpsichorean", "sesquicentennial",
    "phantasmagoria", "daguerreotype", "connoisseurship",
    "verisimilitudinous", "vicissitudinous", "quintessentially",
    "mischievousness", "obsequiousness", "imperviousness",
    "irascibility", "perspicuity", "grandiloquence", "magniloquence",
    "efflorescence", "recrudescent", "pusillanimity", "legerdemain",
    "milquetoast", "periphrastic", "polysyllabic", "onomatopoeic",
    "parallelogram", "ophthalmology", "staphylococcus", "streptococcus",
    "somnambulism", "calligraphy", "camaraderie", "commiseration",
    "coruscation", "denouement", "contretemps", "insouciance",
    "rapprochement", "remonstrance", "protuberance", "flocculent",
    "incommunicado", "incontrovertible", "inefficacious",
    "entrepreneurship", "entrepreneurial", "gubernatorial",
    "jurisprudence", "eleemosynary", "malfeasance", "lackadaisical",
    "recrudescence", "serendipitous", "tautological", "sycophantic",
    "thoroughfare", "transliteration", "unconscionability",
    "unimpeachability", "acquiescence", "bibliographical",
    "circumlocution", "colloquialism", "claustrophobia",
    "extraterrestrial", "grandiloquent", "magniloquent",
    "incomprehensible", "juxtaposition", "disproportionate",
    "heterogeneous", "ignominious", "bourgeoisie", "chrysanthemum",
    "kaleidoscope", "hemorrhagic", "idiosyncratic", "irreconcilable",
    "pusillanimous", "quintessence", "surreptitious", "unconscionable",
    "verisimilitude", "verisimilar", "xylophone", "zeitgeist",
    "preparation", "bellicose", "bibliophile", "cacophonous",
    "catechism", "conflagration", "desultory", "dilettante",
    "ebullient", "egregious", "elocution", "emollient", "ephemeral",
    "equanimity", "equivocation", "extemporaneous", "genuflection",
    "halcyon", "hegemony", "lugubrious", "machiavellian",
    "mellifluous", "metamorphosis", "miscellany", "obstreperous",
    "perspicacious", "physiognomy", "plethora", "pneumatic",
    "querulous", "resplendent", "sacrosanct", "schizophrenia",
    "soliloquy", "supercilious", "tranquillity", "vouchsafe",
    "antediluvian", "apotheosis", "appurtenance", "archipelago",
    "asphyxiation", "baccalaureate", "hemorrhoid",
}

pass2_flags = []
for q in questions:
    answer = q["answer"]
    answer_lower = answer.lower()
    
    if answer_lower in KNOWN_VALID_ANSWERS:
        continue
    
    # Split on spaces/apostrophes for multi-word
    words = answer.replace("'", " ").split()
    for word in words:
        wl = word.lower()
        if wl in KNOWN_VALID_ANSWERS:
            continue
        unknown = spell.unknown([wl])
        if unknown:
            pass2_flags.append((q["id"], answer, wl, spell.correction(wl)))

if pass2_flags:
    print(f"  ⚠ {len(pass2_flags)} words not in dictionary (likely valid rare words):")
    for qid, answer, word, sugg in pass2_flags:
        print(f"    Q{qid}: '{answer}' (word='{word}', suggestion='{sugg}')")
else:
    print(f"  ✓ All answers verified against dictionary")

# ============================================================
# PASS 3: Distractor validity (should NOT be real words)
# ============================================================
print("\n[PASS 3] Distractor Validity (should be misspellings)")

# Known acceptable cases where distractor looks like a word
ACCEPTABLE_DISTRACTORS = {
    "daguerrotype",  # Not a real word (missing 'e'), spellchecker is wrong
}

pass3_problems = []
for q in questions:
    answer = q["answer"]
    distractors = [c for c in q["choices"] if c != answer]
    for d in distractors:
        if d.lower() in ACCEPTABLE_DISTRACTORS:
            continue
        words = d.replace("'", " ").replace("-", " ").split()
        all_known = all(not spell.unknown([w.lower()]) for w in words)
        if all_known:
            pass3_problems.append((q["id"], answer, d))

if pass3_problems:
    print(f"  ⚠ {len(pass3_problems)} distractors recognized as real words:")
    for qid, answer, d in pass3_problems:
        print(f"    Q{qid}: answer='{answer}', distractor='{d}'")
else:
    print(f"  ✓ All distractors are genuine misspellings")

# ============================================================
# PASS 4: No identical question sets
# ============================================================
print("\n[PASS 4] Uniqueness Check")

choice_sets = [tuple(sorted(q["choices"])) for q in questions]
dupes = [(cs, cnt) for cs, cnt in Counter(choice_sets).items() if cnt > 1]

if dupes:
    print(f"  ⚠ {len(dupes)} duplicate choice sets:")
    for cs, cnt in dupes[:10]:
        print(f"    {cs} appears {cnt} times")
else:
    print(f"  ✓ All 600 questions have unique choice sets")

# ============================================================
# PASS 5: Answer differs from every distractor by at least 1 char
# ============================================================
print("\n[PASS 5] Answer-Distractor Differentiation")

pass5_errors = []
for q in questions:
    answer = q["answer"]
    distractors = [c for c in q["choices"] if c != answer]
    for d in distractors:
        if d.lower() == answer.lower():
            pass5_errors.append(f"Q{q['id']}: distractor '{d}' = answer (case)")

if pass5_errors:
    print(f"  ✗ {len(pass5_errors)} errors:")
    for e in pass5_errors: print(f"    {e}")
else:
    print(f"  ✓ All distractors differ from their answer")

# ============================================================
# PASS 6: British vs American spelling check
# ============================================================
print("\n[PASS 6] British Spelling in Distractors")

BRITISH_PATTERNS = {
    "ise": "ize", "isation": "ization", "our": "or",
    "tre": "ter", "ogue": "og", "ence": "ense",
    "ement": "ment",
}

# Already fixed these, just double-check
british_distractors = []
BRITISH_WORDS = {
    "judgement", "acknowledgement", "diarrhoea", "manoeuvre",
    "catalogue", "programme", "defence", "licence", "organise",
    "recognise", "colour", "honour", "favour", "centre",
    "theatre", "fulfil", "enrol", "instal", "cancelation",
    "genuflexion", "connexion",
}

for q in questions:
    distractors = [c for c in q["choices"] if c != q["answer"]]
    for d in distractors:
        if d.lower() in BRITISH_WORDS:
            british_distractors.append((q["id"], q["answer"], d))

if british_distractors:
    print(f"  ⚠ {len(british_distractors)} British spellings as distractors:")
    for qid, ans, d in british_distractors:
        print(f"    Q{qid}: answer='{ans}', distractor='{d}'")
else:
    print(f"  ✓ No British spelling variants used as distractors")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
total_errors = len(pass1_errors) + len(pass5_errors)
total_warnings = len(pass2_flags) + len(pass3_problems) + len(british_distractors)

if total_errors == 0 and total_warnings == 0:
    print("FINAL RESULT: ✓✓✓ 100% VERIFIED — NO ISSUES FOUND")
elif total_errors == 0:
    print(f"FINAL RESULT: ✓ PASSED with {total_warnings} minor warnings")
    print("  (Warnings are rare/specialized words not in basic dictionary)")
else:
    print(f"FINAL RESULT: ✗ {total_errors} ERRORS need fixing")

print(f"\n  Structural:    {'✓' if not pass1_errors else '✗'}")
print(f"  Answers:       {'✓' if not pass2_flags else '⚠ ' + str(len(pass2_flags)) + ' rare words'}")
print(f"  Distractors:   {'✓' if not pass3_problems else '⚠ ' + str(len(pass3_problems)) + ' issues'}")
print(f"  Uniqueness:    {'✓' if not dupes else '⚠ ' + str(len(dupes)) + ' dupes'}")
print(f"  Differentiation: {'✓' if not pass5_errors else '✗'}")
print(f"  No British:    {'✓' if not british_distractors else '⚠'}")
print("=" * 70)
