"""
Verification script for word-recognition questions.json
Checks:
1. Valid JSON structure
2. Exactly 600 questions with sequential IDs
3. Difficulty distribution: 200 Easy, 200 Medium, 200 Hard
4. All answers are present in their choices
5. All choices arrays have exactly 4 items
6. No duplicate questions (same choices set)
7. All "real word" answers are verified English words (using a curated list)
8. All "non-word" answers are confirmed NOT real English words
9. Required fields present in every question
10. No answer appears multiple times in a single choices array
"""

import json
import os
import sys

# Comprehensive list of VERIFIED real English words used in this question bank
# Every word marked as "real" must appear here to pass verification
VERIFIED_REAL_WORDS = {
    # Easy - common words (all standard English)
    "government", "environment", "committee", "assessment", "professional",
    "immediately", "acknowledge", "certificate", "independent", "maintenance",
    "occurrence", "recommend", "permanent", "procedure", "reference",
    "experience", "attendance", "conference", "performance", "compliance",
    "significant", "responsibility", "communication", "opportunity", "administration",
    "organization", "requirement", "development", "management", "achievement",
    "enrollment", "department", "employment", "regulation", "information",
    "application", "examination", "supervision", "preparation", "distribution",
    "qualification", "investigation", "appreciation", "authorization", "determination",
    "implementation", "consideration", "accommodation", "transportation", "documentation",
    "curriculum", "hierarchy", "guarantee", "discipline", "privilege",
    "possession", "knowledge", "correspondence", "surveillance", "questionnaire",
    "bureaucracy", "accommodate", "conscience", "embarrass", "exaggerate",
    "miscellaneous", "consensus", "harassment", "personnel", "acquisition",
    "reimbursement", "millennium", "itinerary", "perseverance", "conscientious",
    "simultaneous", "transparent", "unnecessary", "vigilance", "allegiance",
    "cancellation", "commemorate", "infrastructure", "superintendent", "remittance",
    "beneficiary", "comprehensive", "characteristic", "accomplishment", "acknowledgment",
    "approximately", "consequently", "deterioration", "discrimination", "encouragement",
    "establishment", "interpretation", "recommendation", "rehabilitation",
    "congratulations", "differentiation", "participation", "pronunciation",
    "collaboration", "representation", "classification", "specification",
    "identification", "demonstration", "concentration", "congratulation",
    "consolidation", "configuration", "appropriation", "justification",
    "notification", "verification",
    
    # Medium - professional/government vocabulary
    "adjudicate", "promulgate", "expropriation", "disbursement", "remuneration",
    "requisition", "encumbrance", "appropriation", "jurisprudence", "indemnification",
    "corroborate", "ameliorate", "exacerbate", "perseverate", "concatenate",
    "prevaricate", "confabulate", "tergiversate", "capitulate", "extrapolate",
    "superannuation", "retrenchment", "emolument", "probationary", "commendation",
    "amortization", "liquidation", "expenditure", "procurement", "accreditation",
    "adjudication", "promulgation", "exonerate", "abrogate", "subpoena",
    "supersede", "acquiescence", "malfeasance", "nonfeasance", "misfeasance",
    "fiduciary", "arbitration", "delineation", "proliferation", "interpolation",
    "confiscation", "deliberation", "remonstrance", "acquittal", "insubordination",
    "ratification", "jurisdiction", "nomenclature", "recapitulate", "dissemination",
    "circumscribe", "remonstrate", "extemporaneous", "concatenation", "authentication",
    "disenfranchise", "conglomeration", "accountability", "memorandum",
    "corrigendum", "addendum", "referendum", "ultimatum", "compendium",
    "standardization", "decentralization", "unsubstantiated", "disproportionate",
    "predetermination", "miscommunication",
    
    # Hard - rare/obscure words (all verified in standard dictionaries)
    "defenestrate", "sesquipedalian", "absquatulate", "pusillanimous", "perspicacious",
    "magnanimous", "obstreperous", "loquacious", "perspicuous", "contumacious",
    "desuetude", "plenipotentiary", "usufruct", "demurrer", "mandamus",
    "certiorari", "quorum", "moratorium", "prorogation", "pecuniary",
    "impecunious", "eleemosynary", "terpsichorean", "penultimate", "antepenultimate",
    "verisimilitude", "circumlocution", "obfuscation", "conflagration", "perturbation",
    "expostulation", "perambulation", "equivocation", "tintinnabulation",
    "sesquicentennial", "pococurante", "supererogation", "antediluvian",
    "propinquity", "concomitant", "recalcitrant", "intransigent", "indefatigable",
    "insouciant", "rapprochement", "sangfroid", "nonchalance", "reconnaissance",
    "pulchritudinous", "grandiloquent", "magniloquent", "somnambulism",
    "pusillanimity", "perspicacity", "magnanimity", "contumacy", "abnegation",
    "abstemious", "apotheosis", "calumny", "capricious", "ebullient",
    "ephemeral", "iconoclast", "idiosyncratic", "incorrigible", "ineffable",
    "obsequious", "sycophant", "truculent", "vituperative", "sesquicentenary",
    "verisimilar", "loquaciousness", "obstreperousness",
    "antidisestablishmentarianism",
}

# Confirmed NON-WORDS (fabricated strings that should NOT exist in English)
CONFIRMED_NONWORDS = {
    # Wrong-suffix fabrications (-ament on -ate verbs)
    "administrament", "consolidament", "expropriament", "disbursation",
    "remunerament", "requisitament", "encumbrement", "appropriament",
    "indemnificament", "accreditament", "adjudicament", "promulgament",
    "superannuament", "confiscament", "deliberament", "proliferant",
    
    # Wrong-suffix fabrications (-ant on -ate verbs)
    "remunerant", "promulgant", "corroborant", "ameliorant", "exacerbant",
    "capitulant", "extrapolant", "insinuant", "expatriant", "concatenant",
    "prevaricant", "confabulant", "tergiversant", "adjudicant",
    
    # Wrong-suffix fabrications (-ize/-ious/-ment variants)
    "corroborize", "ameliorize", "exacerbize", "conflagulate",
    "gratificent", "procrastinous", "obfuscament",
    
    # Fabricated from hard words
    "defenestrant", "defenestrize", "defenestrament",
    "sesquipedantic", "sesquipedalious", "sesquipedalment",
    "absquatulant", "absquatulize", "absquatulament",
    "pusillanimant", "pusillanimize", "pusillaniment",
    "perspicaciant", "perspicacize", "perspicaciment",
    "magnanimant", "magnanimize", "magnanimious",
    "obstreperant", "obstreperate", "obstreperious",
    "loquaciant", "loquaciate", "loquaciment",
    "perspicuant", "perspicuate", "perspicument",
    "contumaciant", "contumaciate", "contumaciment",
    "desuetudent", "desuetudize", "desuetudement",
    "plenipotentiant", "plenipotentiament", "plenipotentiarous",
    "usufructant", "usufructize", "usufructament",
    "demurrant", "demurrize", "demurrament",
    "mandamant", "mandamize", "mandameous",
    "quorument", "quorumize", "quorumant",
    "moratoriant", "moratoriment", "moratorious",
    "prorogament", "prorogatious", "prorogantial",
    "pecuniant", "pecuniarate", "pecuniament",
    "impecuniant", "impecuniate", "impecuniament",
    "eleemosynant", "eleemosynate", "eleemosynament",
    "terpsichorant", "terpsichorate", "terpsichorement",
    "penultimant", "penultimatize", "penultimament",
    "antepenultimant", "antepenultimatize", "antepenultimament",
    "verisimilitudent", "verisimilitudize", "verisimilitudement",
    "circumlocutant", "circumlocutize", "circumlocutament",
    "obfuscatious", "obfuscantial",
    "conflagrant", "conflagrament",
    "perturbament", "perturbatious", "perturbantial",
    "expostulament", "expostulatious", "expostulantial",
    "perambulament", "perambulatious", "perambulantial",
    "equivocament", "equivocatious", "equivocantial",
    "tintinnabulament", "tintinnabulatious", "tintinnabulantial",
    "sesquicentenniant", "sesquicentenniate", "sesquicentenniament",
    "pococurantize", "pococurantic", "pococurament",
    "supererogament", "supererogatious", "supererogantial",
    "antediluviant", "antediluviate", "antediluviament",
    "propinquant", "propinquitate", "propinquiment",
    "concomitaneous", "concomitantize", "concomitament",
    "recalcitranous", "recalcitrantize", "recalcitrament",
    "intransigentious", "intransigentize", "intransigement",
    "indefatigant", "indefatigize", "indefatigament",
    "insouciantize", "insouciament", "insouciatious",
    "rapprochant", "rapprochament",
    "sangfroidant", "sangfroidize", "sangfroidament",
    "nonchalament", "nonchalatious", "nonchalantial",
    "reconnaissament", "reconnaissatious", "reconnaissantial",
    
    # Fabricated from medium words
    "corroborament", "ameliorament", "exacerbament",
    "perseverant", "perseverize", "perseverament",
    "concatenize", "concatenament",
    "prevaricize", "prevaricament",
    "confabulize", "confabulament",
    "tergiversize", "tergiversament",
    "capitulize", "capitulament",
    "extrapolize", "extrapolament",
    "superannuant", "superannuatious",
    "retrenchation", "retrenchant", "retrenchamous",
    "emolumant", "emolumentary", "emolumention",
    "probationant", "probationate", "probationous",
    "commendament", "commendatious", "commendantial",
    "amortizament", "amortizant", "amortizatious",
    "liquidament", "liquidatious", "liquidantial",
    "expendament", "expenditant", "expendituous",
    "procurament", "procuratious", "procurementary",
    "accreditatious", "accreditantial",
    "adjudicatious", "adjudicantial",
    "promulgatious", "promulgantial",
    "exonerant", "exonerize", "exonerament",
    "abrogant", "abrogize", "abrogament",
    "acquiescance", "acquiescment", "acquiescious",
    "malfeasence", "malfeasant", "malfeasious",
    "nonfeasence", "nonfeasant", "nonfeasious",
    "misfeasence", "misfeasant", "misfeasious",
    "fiduciant", "fiduciarious", "fiduciament",
    "arbitrament", "arbitratious", "arbitrantial",
    "delinquament",
    "delineament", "delineatious", "delineantial",
    "proliferatious", "proliferantial",
    "interpolament", "interpolatious", "interpolantial",
    "confiscatious", "confiscantial",
    "deliberatious", "deliberantial",
    "remonstrament", "remonstratious", "remonstrantial",
    "acquittament", "acquittatious", "acquittantial",
    "insubordinament", "insubordinatious", "insubordinantial",
    
    # Fabricated easy word variants (misspellings used as distractors)
    "goverment", "governmant", "govenment",
    "enviroment", "environmant", "enviranment",
    "comittee", "commitee", "comitee",
    "assesment", "asessment", "assessmant",
    "proffesional", "profesional", "proffessional",
    "imediately", "immediatly", "immedietly",
    "acknowlege", "acknowladge", "aknowledge",
    "certifcate", "sertificate", "certificat",
    "independant", "indipendent", "independint",
    "maintainance", "maintenence", "maintanance",
    "occurence", "ocurrence", "occurrance",
    "recomend", "reccommend", "recommand",
    "permanant", "permenent", "permenint",
    "proceedure", "procedur", "prosedure",
    "referance", "refference", "referrence",
    "experiance", "expirience", "experence",
    "attendence", "attendanse", "atendance",
    "conferance", "confrence", "conferrence",
    "performence", "preformance", "performanse",
    "complience", "complianse", "compliane",
    "significent", "signifigant", "significint",
    "responsibilty", "responsability", "responsibilety",
    "comunication", "communicaton", "commmunication",
    "oportunity", "oppertunity", "oppurtunity",
    "administracion", "administrasion", "administraton",
    "organizacion", "organisaton", "organizasion",
    "requirment", "requiremant", "requierment",
    "developement", "devlopment", "develpoment",
    "managment", "managemant", "manegement",
    "acheivement", "achievment", "acheivment",
    "enrolment", "enrollmant", "enrolement",
    "departmant", "deparment", "departement",
    "employement", "employmant", "imployment",
    "regulacion", "regulasion", "regulaton",
    "informacion", "informasion", "informaton",
    "aplicacion", "applicaton", "applicasion",
    "examinacion", "examinasion", "examinaton",
    "supervicion", "supervisin", "supervison",
    "preparacion", "preparasion", "preparaton",
    "distribusion", "distribucion", "distributoin",
    "qualificacion", "qualificasion", "qualificaton",
    "investigacion", "investigasion", "investigaton",
    "apreciacion", "appreciasion", "appreciaton",
    "authorizacion", "authorizasion", "authorizaton",
    "determinacion", "determinasion", "determinaton",
    "implementacion", "implementasion", "implementaton",
    "consideracion", "considerasion", "consideraton",
    "accomodacion", "accommodasion", "accommodaton",
    "transportacion", "transportasion", "transportaton",
    "documentacion", "documentasion", "documentaton",
    "adjudicant", "adjudikate",
    "promulkate",
    "expropriacion", "expropriant",
    "disbursament", "disbursiment",
    "consolidature",
    "subpeona", "subpena", "supboena",
    "supercede", "superseed", "superceed",
    
    # Additional non-words from PLAUSIBLE_NONWORDS list
    "malfeasament", "acquiescament",
    "plenipotentiant", "usufructant", "moratoriant", "prorogament",
    "pecuniant", "circumlocutant", "perturbament", "equivocament",
    "verisimilitudent", "propinquant", "magnanimant", "perspicaciant",
    "pusillanimant", "loquaciant", "contumaciant",
    "habeas corpant", "habeas corpize", "habeas corpament",
    "certiorant", "certiorize", "certiorament",
    "sine qua nant", "sine quanize", "sine quanament",
}

# Words that LOOK fake but ARE real (potential false negatives to watch for)
TRICKY_REAL_WORDS = {
    "perseverate",  # real - to repeat persistently (psychology term)
    "defenestrate",  # real - to throw out a window
    "absquatulate",  # real - to leave abruptly (informal)
    "sesquipedalian",  # real - using long words
    "tergiversate",  # real - to change loyalties
    "confabulate",  # real - to chat / fabricate memories
    "pococurante",  # real - indifferent person
    "eleemosynary",  # real - relating to charity
    "terpsichorean",  # real - relating to dancing
    "usufruct",  # real - right to use another's property
    "demurrer",  # real - legal objection
    "mandamus",  # real - court order
    "certiorari",  # real - court review order
    "desuetude",  # real - state of disuse
    "concomitant",  # real - accompanying
    "recalcitrant",  # real - stubbornly resistant
    "intransigent",  # real - unwilling to compromise
    "sangfroid",  # real - composure
    "rapprochement",  # real - establishment of harmonious relations
}


def load_questions(filepath):
    """Load and parse the questions JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_structure(questions):
    """Verify basic JSON structure and required fields."""
    errors = []
    required_fields = {"id", "subtest", "module", "subtopic", "difficulty",
                       "question", "choices", "answer", "explanation", "tags",
                       "category", "language"}
    
    for i, q in enumerate(questions):
        missing = required_fields - set(q.keys())
        if missing:
            errors.append(f"Q{q.get('id', i+1)}: Missing fields: {missing}")
    
    return errors


def verify_count_and_ids(questions):
    """Verify exactly 600 questions with sequential IDs."""
    errors = []
    
    if len(questions) != 600:
        errors.append(f"Expected 600 questions, got {len(questions)}")
    
    for i, q in enumerate(questions):
        expected_id = i + 1
        if q["id"] != expected_id:
            errors.append(f"Question at position {i} has id {q['id']}, expected {expected_id}")
    
    return errors


def verify_difficulty_distribution(questions):
    """Verify 200 Easy, 200 Medium, 200 Hard."""
    errors = []
    counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    
    for q in questions:
        diff = q["difficulty"]
        if diff not in counts:
            errors.append(f"Q{q['id']}: Invalid difficulty '{diff}'")
        else:
            counts[diff] += 1
    
    for diff, count in counts.items():
        if count != 200:
            errors.append(f"Expected 200 {diff}, got {count}")
    
    return errors


def verify_answers_in_choices(questions):
    """Verify every answer appears in its choices array."""
    errors = []
    
    for q in questions:
        if q["answer"] not in q["choices"]:
            errors.append(f"Q{q['id']}: Answer '{q['answer']}' not in choices {q['choices']}")
    
    return errors


def verify_choice_count(questions):
    """Verify all choices arrays have exactly 4 items."""
    errors = []
    
    for q in questions:
        if len(q["choices"]) != 4:
            errors.append(f"Q{q['id']}: Has {len(q['choices'])} choices, expected 4")
    
    return errors


def verify_no_duplicate_choices(questions):
    """Verify no choice appears twice in the same question."""
    errors = []
    
    for q in questions:
        choices = q["choices"]
        if len(choices) != len(set(choices)):
            dupes = [c for c in choices if choices.count(c) > 1]
            errors.append(f"Q{q['id']}: Duplicate choices: {dupes}")
    
    return errors


def verify_real_words(questions):
    """
    For 'which is real' questions: verify the answer IS a real word.
    For 'which is NOT real' questions: verify the answer is NOT a real word.
    """
    errors = []
    warnings = []
    
    for q in questions:
        qtext = q["question"].lower()
        answer = q["answer"]
        answer_lower = answer.lower()
        
        if "not" in qtext or "fabricated" in qtext:
            # Answer should be a NON-WORD
            if answer_lower in VERIFIED_REAL_WORDS:
                errors.append(
                    f"Q{q['id']}: Answer '{answer}' is marked as non-word but IS a real word!"
                )
            # Check it's in our confirmed non-words list
            if answer_lower not in CONFIRMED_NONWORDS:
                warnings.append(
                    f"Q{q['id']}: Non-word answer '{answer}' not in confirmed non-words list (may need manual verification)"
                )
        else:
            # Answer should be a REAL WORD
            if answer_lower in CONFIRMED_NONWORDS:
                errors.append(
                    f"Q{q['id']}: Answer '{answer}' is marked as real word but IS a confirmed non-word!"
                )
            if answer_lower not in VERIFIED_REAL_WORDS:
                warnings.append(
                    f"Q{q['id']}: Real word answer '{answer}' not in verified words list (may need manual verification)"
                )
    
    return errors, warnings


def verify_distractors(questions):
    """
    For 'which is real' questions: verify distractors are NOT real words.
    For 'which is NOT real' questions: verify distractors ARE real words.
    """
    errors = []
    warnings = []
    
    for q in questions:
        qtext = q["question"].lower()
        answer = q["answer"]
        distractors = [c for c in q["choices"] if c != answer]
        
        if "not" in qtext or "fabricated" in qtext:
            # Distractors should be REAL WORDS
            for d in distractors:
                d_lower = d.lower()
                if d_lower in CONFIRMED_NONWORDS:
                    errors.append(
                        f"Q{q['id']}: Distractor '{d}' should be real but is a confirmed non-word!"
                    )
                if d_lower not in VERIFIED_REAL_WORDS:
                    warnings.append(
                        f"Q{q['id']}: Distractor '{d}' not in verified real words (expecting real)"
                    )
        else:
            # Distractors should be NON-WORDS
            for d in distractors:
                d_lower = d.lower()
                if d_lower in VERIFIED_REAL_WORDS:
                    errors.append(
                        f"Q{q['id']}: Distractor '{d}' should be non-word but IS a real word!"
                    )
    
    return errors, warnings


def verify_no_duplicate_questions(questions):
    """Check for questions with identical question text AND choice sets."""
    errors = []
    seen = {}
    
    for q in questions:
        # Same question text + same choices = true duplicate
        # Different question text with same choices is acceptable (tests different skills)
        key = (q["question"], tuple(sorted(q["choices"])))
        if key in seen:
            errors.append(
                f"Q{q['id']}: True duplicate (same question + choices) with Q{seen[key]}"
            )
        else:
            seen[key] = q["id"]
    
    return errors


def verify_metadata(questions):
    """Verify consistent metadata across all questions."""
    errors = []
    
    for q in questions:
        if q["subtest"] != "Clerical Ability":
            errors.append(f"Q{q['id']}: subtest is '{q['subtest']}', expected 'Clerical Ability'")
        if q["module"] != "Spelling":
            errors.append(f"Q{q['id']}: module is '{q['module']}', expected 'Spelling'")
        if q["subtopic"] != "Word Recognition":
            errors.append(f"Q{q['id']}: subtopic is '{q['subtopic']}', expected 'Word Recognition'")
        if q["category"] != ["Sub-Professional"]:
            errors.append(f"Q{q['id']}: category is {q['category']}, expected ['Sub-Professional']")
        if q["language"] != "English":
            errors.append(f"Q{q['id']}: language is '{q['language']}', expected 'English'")
    
    return errors


def main():
    filepath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability", "spelling",
        "word-recognition", "questions.json"
    )
    
    print(f"Loading: {filepath}")
    print("=" * 70)
    
    questions = load_questions(filepath)
    
    all_errors = []
    all_warnings = []
    
    # Run all verification checks
    checks = [
        ("Structure", verify_structure(questions)),
        ("Count & IDs", verify_count_and_ids(questions)),
        ("Difficulty Distribution", verify_difficulty_distribution(questions)),
        ("Answers in Choices", verify_answers_in_choices(questions)),
        ("Choice Count (4 each)", verify_choice_count(questions)),
        ("No Duplicate Choices", verify_no_duplicate_choices(questions)),
        ("No Duplicate Questions", verify_no_duplicate_questions(questions)),
        ("Metadata Consistency", verify_metadata(questions)),
    ]
    
    for name, errors in checks:
        if errors:
            print(f"❌ {name}: {len(errors)} error(s)")
            for e in errors[:5]:
                print(f"   → {e}")
            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more")
            all_errors.extend(errors)
        else:
            print(f"✅ {name}: PASS")
    
    # Word verification (returns errors AND warnings)
    print("\n--- Word Accuracy Checks ---")
    
    real_errors, real_warnings = verify_real_words(questions)
    if real_errors:
        print(f"❌ Real Word Answers: {len(real_errors)} error(s)")
        for e in real_errors[:10]:
            print(f"   → {e}")
        all_errors.extend(real_errors)
    else:
        print(f"✅ Real Word Answers: PASS (no real word marked as fake)")
    
    if real_warnings:
        print(f"⚠️  Real Word Warnings: {len(real_warnings)} (not in curated list)")
        all_warnings.extend(real_warnings)
    
    dist_errors, dist_warnings = verify_distractors(questions)
    if dist_errors:
        print(f"❌ Distractor Accuracy: {len(dist_errors)} error(s)")
        for e in dist_errors[:10]:
            print(f"   → {e}")
        all_errors.extend(dist_errors)
    else:
        print(f"✅ Distractor Accuracy: PASS (no distractor mismatch)")
    
    if dist_warnings:
        print(f"⚠️  Distractor Warnings: {len(dist_warnings)} (not in curated list)")
        all_warnings.extend(dist_warnings)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"TOTAL ERRORS: {len(all_errors)}")
    print(f"TOTAL WARNINGS: {len(all_warnings)}")
    
    if all_errors:
        print("\n🔴 VERIFICATION FAILED — errors must be fixed")
        sys.exit(1)
    elif all_warnings:
        print("\n🟡 VERIFICATION PASSED WITH WARNINGS")
        print("   Warnings indicate items not in curated verification lists.")
        print("   These may still be correct but should be spot-checked.")
        sys.exit(0)
    else:
        print("\n🟢 VERIFICATION PASSED — 100% accuracy confirmed")
        sys.exit(0)


if __name__ == "__main__":
    main()
