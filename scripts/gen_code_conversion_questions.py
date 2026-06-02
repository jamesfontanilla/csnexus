"""
Generate 600-question bank for Code Conversion.
200 Easy (IDs 1-200), 200 Medium (IDs 201-400), 200 Hard (IDs 401-600).
"""
import json
import random
import os
import string

random.seed(2024)

# ============================================================
# DATA
# ============================================================

KEYWORDS_10 = [kw for kw in [
    "BLACKHORSE", "PRODUCTIVE", "NIGHTSWORE", "REPUBLICAN",
    "THUMBSCREW", "FLASHPOINT", "FLOWCHARTS"
] if len(kw) == 10 and len(set(kw)) == 10]

FIXED_KEYS = [{"letters": kw, "digits": "1234567890"} for kw in KEYWORDS_10]

SYMBOL_SETS = [
    ["@", "#", "$", "%", "&", "!", "^", "~"],
    ["★", "●", "▲", "■", "△", "◆", "◇", "○"],
]

WORDS_3 = ["ACE","AID","BAD","BIG","CAB","COP","DIG","DIM","FIG","FIN",
           "GAP","GEM","HOP","ICE","INK","JAM","JOB","KEY","LAP","LOG",
           "MAP","MIX","NAP","NET","OAK","ODD","PAN","PIG","RAG","RIM",
           "SAP","SIP","TAP","TIN","VAN","VET","WAR","WIG","YAM","ZAP"]

WORDS_4 = ["AIDE","BACK","BAND","CAGE","CARD","DARE","DESK","FACE","FILE",
           "FORM","GAIN","GRID","HALF","HAND","ITEM","JACK","JUMP","KEEP",
           "KING","LAMP","LAND","MAIL","MARK","NAME","NODE","OPEN","PACK",
           "PAGE","RANK","RISK","SAFE","SEAL","SIGN","TASK","TERM","UNIT",
           "VAST","VOTE","WAGE","WARD","WORK","YEAR","ZONE","MEMO","CODE",
           "PLAN","COST","FUND","RULE"]

WORDS_5 = ["BADGE","BRIEF","CHAIR","CLAIM","CLERK","COVER","DRAFT","ENTRY",
           "FILED","FORMS","GRANT","INDEX","JUDGE","LABOR","LEGAL","MERIT",
           "NOTED","ORDER","PANEL","PRINT","QUOTA","RANGE","STAMP","TRACK",
           "VALID","WRITE","AUDIT","BOARD","CHIEF","FUNDS","LEAVE","MINOR",
           "OFFER","PRIME","RULES","SCORE","SHIFT","STAFF","TERMS","UNION",
           "VALUE","WORKS"]

WORDS_6 = ["BUDGET","CLAIMS","DESIGN","EXPORT","FILING","GRANTS","HONEST",
           "IMPORT","JOINED","KNIGHT","LEDGER","MASTER","NOTICE","OFFICE",
           "PERMIT","RECORD","SUBMIT","TRAVEL","UPDATE","VERIFY","WORKER",
           "BACKER","SCORED","STRONG","HANDLE","BRANCH","FILTER","MORALS"]


# ============================================================
# HELPERS
# ============================================================

def shift_letter(ch, n):
    return chr((ord(ch.upper()) - 65 + n) % 26 + 65)

def shift_word(word, n):
    return "".join(shift_letter(c, n) for c in word.upper())

def encode_key(word, kl, kd):
    return "".join(kd[kl.index(c)] if c in kl else c for c in word.upper())

def decode_key(code, kl, kd):
    return "".join(kl[kd.index(c)] if c in kd else c for c in code)

def num_to_letters(num_str, kl, kd):
    return "".join(kl[kd.index(c)] if c in kd else c for c in num_str)

def fmt_key(kl, kd):
    return " | ".join(f"{kl[i]}={kd[i]}" for i in range(len(kl)))

def make_distractors(correct, gen_fn, n=3):
    """Generate n distractors using gen_fn, with hard cap on attempts."""
    pool = set()
    for _ in range(50):
        d = gen_fn()
        if d != correct:
            pool.add(d)
        if len(pool) >= n:
            break
    # Fill with numbered fallbacks if needed
    idx = 1
    while len(pool) < n:
        pool.add(f"{correct[:-1]}{idx}" if len(correct) > 1 else f"X{idx}")
        idx += 1
    return list(pool)[:n]

def four_choices(correct, distractors):
    """Return shuffled list of 4 choices with correct guaranteed present."""
    c = [correct] + distractors[:3]
    random.shuffle(c)
    return c

def q(qid, diff, question, choices, answer, explanation, tags):
    return {
        "id": qid, "subtest": "Clerical Ability", "module": "Coding and Decoding",
        "subtopic": "Code Conversion", "difficulty": diff, "question": question,
        "choices": choices, "answer": answer, "explanation": explanation,
        "tags": tags, "category": ["Sub-Professional"], "language": "English",
    }


# ============================================================
# EASY (1-200)
# ============================================================

def gen_easy():
    qs = []
    qid = 1

    # Type 1: Fixed sub encoding 3-4 letters (50)
    for i in range(50):
        fk = FIXED_KEYS[i % len(FIXED_KEYS)]
        kl, kd = fk["letters"], fk["digits"]
        ln = 3 if i < 25 else 4
        pool = [w for w in (WORDS_3 if ln == 3 else WORDS_4) if all(c in kl for c in w)]
        if not pool:
            pool = ["".join(random.sample(kl, ln)) for _ in range(10)]
        word = pool[i % len(pool)]
        correct = encode_key(word, kl, kd)
        ds = make_distractors(correct, lambda: "".join(
            kd[random.randint(0, 9)] for _ in range(len(correct))))
        step = ", ".join(f"{c}→{kd[kl.index(c)]}" for c in word if c in kl)
        qs.append(q(qid, "Easy",
            f"Code key: [{fmt_key(kl,kd)}]. Encode: {word}",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["fixed-substitution", "encoding"]))
        qid += 1

    # Type 2: Fixed sub decoding 3-4 digits (50)
    for i in range(50):
        fk = FIXED_KEYS[i % len(FIXED_KEYS)]
        kl, kd = fk["letters"], fk["digits"]
        ln = 3 if i < 25 else 4
        code = "".join(random.choice(kd) for _ in range(ln))
        correct = decode_key(code, kl, kd)
        ds = make_distractors(correct, lambda: "".join(
            kl[random.randint(0, 9)] for _ in range(len(correct))))
        step = ", ".join(f"{c}→{kl[kd.index(c)]}" for c in code)
        qs.append(q(qid, "Easy",
            f"Code key: [{fmt_key(kl,kd)}]. Decode: {code}",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["fixed-substitution", "decoding"]))
        qid += 1

    # Type 3: Caesar encoding +1/+2/+3, 3-letter (40)
    for i in range(40):
        shift = (i % 3) + 1
        word = WORDS_3[i % len(WORDS_3)]
        correct = shift_word(word, shift)
        ds = make_distractors(correct, lambda: shift_word(word, random.choice(
            [s for s in range(1, 7) if s != shift])))
        step = ", ".join(f"{c}→{shift_letter(c, shift)}" for c in word)
        qs.append(q(qid, "Easy",
            f"+{shift} letter shift. Encode: {word}",
            four_choices(correct, ds), correct,
            f"Shift +{shift}: {step} = {correct}.",
            ["shifted-alphabet", "encoding"]))
        qid += 1

    # Type 4: Keyword number→letters, 3-4 digits (30)
    for i in range(30):
        kw = KEYWORDS_10[i % len(KEYWORDS_10)]
        ds_str = "1234567890"
        ln = 3 if i < 15 else 4
        number = "".join(random.choice(ds_str) for _ in range(ln))
        correct = num_to_letters(number, kw, ds_str)
        ds = make_distractors(correct, lambda: "".join(
            kw[random.randint(0, 9)] for _ in range(ln)))
        step = ", ".join(f"{d}→{kw[ds_str.index(d)]}" for d in number)
        qs.append(q(qid, "Easy",
            f"Keyword: {kw} (1-2-3-4-5-6-7-8-9-0). Convert {number} to letters:",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["keyword-cipher", "number-to-letter"]))
        qid += 1

    # Type 5: Keyword letters→number, 3-4 letters (30)
    for i in range(30):
        kw = KEYWORDS_10[i % len(KEYWORDS_10)]
        ds_str = "1234567890"
        ln = 3 if i < 15 else 4
        word = "".join(random.choice(kw) for _ in range(ln))
        correct = encode_key(word, kw, ds_str)
        ds = make_distractors(correct, lambda: "".join(
            ds_str[random.randint(0, 9)] for _ in range(ln)))
        step = ", ".join(f"{c}→{ds_str[kw.index(c)]}" for c in word)
        qs.append(q(qid, "Easy",
            f"Keyword: {kw} (1-2-3-4-5-6-7-8-9-0). Convert {word} to digits:",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["keyword-cipher", "letter-to-number"]))
        qid += 1

    return qs[:200]


# ============================================================
# MEDIUM (201-400)
# ============================================================

def gen_medium():
    qs = []
    qid = 201

    # Type 1: Fixed sub encoding 5-letter (40)
    for i in range(40):
        fk = FIXED_KEYS[i % len(FIXED_KEYS)]
        kl, kd = fk["letters"], fk["digits"]
        pool = [w for w in WORDS_5 if all(c in kl for c in w)]
        if not pool:
            pool = ["".join(random.sample(kl, 5)) for _ in range(10)]
        word = pool[i % len(pool)]
        correct = encode_key(word, kl, kd)
        ds = make_distractors(correct, lambda: "".join(
            kd[random.randint(0, 9)] for _ in range(5)))
        step = ", ".join(f"{c}→{kd[kl.index(c)]}" for c in word if c in kl)
        qs.append(q(qid, "Medium",
            f"Code key: [{fmt_key(kl,kd)}]. Encode: {word}",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["fixed-substitution", "encoding", "5-letter"]))
        qid += 1

    # Type 2: Fixed sub decoding 5-digit (40)
    for i in range(40):
        fk = FIXED_KEYS[i % len(FIXED_KEYS)]
        kl, kd = fk["letters"], fk["digits"]
        code = "".join(random.choice(kd) for _ in range(5))
        correct = decode_key(code, kl, kd)
        ds = make_distractors(correct, lambda: "".join(
            kl[random.randint(0, 9)] for _ in range(5)))
        step = ", ".join(f"{c}→{kl[kd.index(c)]}" for c in code)
        qs.append(q(qid, "Medium",
            f"Code key: [{fmt_key(kl,kd)}]. Decode: {code}",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["fixed-substitution", "decoding", "5-digit"]))
        qid += 1

    # Type 3: Caesar decoding +2 to +5, 4-letter (30)
    for i in range(30):
        shift = (i % 4) + 2
        word = WORDS_4[i % len(WORDS_4)]
        encoded = shift_word(word, shift)
        correct = word
        ds = make_distractors(correct, lambda: shift_word(encoded,
            -random.choice([s for s in range(1, 9) if s != shift])))
        qs.append(q(qid, "Medium",
            f"Encoded with +{shift} shift: {encoded}. Original word?",
            four_choices(correct, ds), correct,
            f"Shift back {shift}: {encoded} → {correct}.",
            ["shifted-alphabet", "decoding"]))
        qid += 1

    # Type 4: Symbol substitution encoding (30)
    for i in range(30):
        n = 6
        letters = random.sample(string.ascii_uppercase, n)
        syms = random.sample(random.choice(SYMBOL_SETS), n)
        sm = dict(zip(letters, syms))
        wlen = random.choice([4, 5])
        word = "".join(random.choices(letters, k=wlen))
        correct = "".join(sm[c] for c in word)
        ds = make_distractors(correct, lambda: "".join(
            random.choice(syms) for _ in range(wlen)))
        key_d = " | ".join(f"{l}={s}" for l, s in sm.items())
        step = ", ".join(f"{c}→{sm[c]}" for c in word)
        qs.append(q(qid, "Medium",
            f"Key: {key_d}. Encode: {word}",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["symbol-substitution", "encoding"]))
        qid += 1

    # Type 5: Keyword 5-6 digit → letters (30)
    for i in range(30):
        kw = KEYWORDS_10[i % len(KEYWORDS_10)]
        ds_str = "1234567890"
        ln = 5 if i < 15 else 6
        number = "".join(random.choice(ds_str) for _ in range(ln))
        correct = num_to_letters(number, kw, ds_str)
        ds = make_distractors(correct, lambda: "".join(
            kw[random.randint(0, 9)] for _ in range(ln)))
        step = ", ".join(f"{d}→{kw[ds_str.index(d)]}" for d in number)
        qs.append(q(qid, "Medium",
            f"Keyword: {kw} (1-2-3-4-5-6-7-8-9-0). Convert {number} to letters:",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["keyword-cipher", "number-to-letter"]))
        qid += 1

    # Type 6: Keyword 5-6 letters → number (30)
    for i in range(30):
        kw = KEYWORDS_10[i % len(KEYWORDS_10)]
        ds_str = "1234567890"
        ln = 5 if i < 15 else 6
        word = "".join(random.choice(kw) for _ in range(ln))
        correct = encode_key(word, kw, ds_str)
        ds = make_distractors(correct, lambda: "".join(
            ds_str[random.randint(0, 9)] for _ in range(ln)))
        step = ", ".join(f"{c}→{ds_str[kw.index(c)]}" for c in word)
        qs.append(q(qid, "Medium",
            f"Keyword: {kw} (1-2-3-4-5-6-7-8-9-0). Convert {word} to digits:",
            four_choices(correct, ds), correct,
            f"{step} = {correct}.",
            ["keyword-cipher", "letter-to-number"]))
        qid += 1

    return qs[:200]


# ============================================================
# HARD (401-600)
# ============================================================

def gen_hard():
    qs = []
    qid = 401

    # Type 1: Conditional encoding (45)
    for i in range(45):
        fk = FIXED_KEYS[i % len(FIXED_KEYS)]
        kl, kd = fk["letters"], fk["digits"]
        pool = [w for w in WORDS_5 if all(c in kl for c in w)]
        if not pool:
            pool = ["".join(random.sample(kl, 5)) for _ in range(20)]
        word = pool[i % len(pool)]
        base = encode_key(word, kl, kd)

        rt = i % 4
        if rt == 0:
            rule = "If first letter is a VOWEL, REVERSE the code."
            if word[0] in "AEIOU":
                correct = base[::-1]
                expl = f"Base: {base}. '{word[0]}' vowel → reverse: {correct}."
            else:
                correct = base
                expl = f"Base: {base}. '{word[0]}' consonant → unchanged: {correct}."
        elif rt == 1:
            rule = "If last letter is a CONSONANT, append '0'."
            if word[-1] not in "AEIOU":
                correct = base + "0"
                expl = f"Base: {base}. '{word[-1]}' consonant → +0: {correct}."
            else:
                correct = base
                expl = f"Base: {base}. '{word[-1]}' vowel → unchanged: {correct}."
        elif rt == 2:
            rule = "If word has a REPEATED letter, prepend first digit."
            if len(set(word)) < len(word):
                correct = base[0] + base
                expl = f"Base: {base}. Repeat found → prepend: {correct}."
            else:
                correct = base
                expl = f"Base: {base}. No repeats → unchanged: {correct}."
        else:
            rule = "If word length is EVEN, swap first and last digits."
            if len(word) % 2 == 0:
                correct = base[-1] + base[1:-1] + base[0]
                expl = f"Base: {base}. Even length → swap ends: {correct}."
            else:
                correct = base
                expl = f"Base: {base}. Odd length → unchanged: {correct}."

        alts = [base, base[::-1], base + "0", base[0] + base]
        ds = [a for a in alts if a != correct][:3]
        while len(ds) < 3:
            ds.append("".join(kd[random.randint(0, 9)] for _ in range(len(correct))))
        qs.append(q(qid, "Hard",
            f"Key: [{fmt_key(kl,kd)}]. Rule: {rule} Encode: {word}",
            four_choices(correct, ds), correct, expl,
            ["multi-rule", "conditional"]))
        qid += 1

    # Type 2: Caesar decoding +4 to +8, 5-letter (30)
    for i in range(30):
        shift = (i % 5) + 4
        word = WORDS_5[i % len(WORDS_5)]
        encoded = shift_word(word, shift)
        correct = word
        ds = make_distractors(correct, lambda: shift_word(encoded,
            -random.choice([s for s in range(1, 12) if s != shift])))
        qs.append(q(qid, "Hard",
            f"Encoded with +{shift} Caesar: {encoded}. Original?",
            four_choices(correct, ds), correct,
            f"Shift back {shift}: {encoded} → {correct}.",
            ["shifted-alphabet", "decoding", "large-shift"]))
        qid += 1

    # Type 3: Symbol + conditional (30)
    for i in range(30):
        n = 7
        letters = random.sample(string.ascii_uppercase, n)
        syms = random.sample(random.choice(SYMBOL_SETS), min(n, 8))
        while len(syms) < n:
            syms.append(random.choice(syms))
        sm = dict(zip(letters, syms))
        wlen = random.choice([5, 6])
        word = "".join(random.choices(letters, k=wlen))
        base = "".join(sm[c] for c in word)

        rt = i % 3
        if rt == 0:
            rule = "If starts with vowel, add ● at start."
            correct = ("●" + base) if word[0] in "AEIOU" else base
            expl = f"Base: {base}. First='{word[0]}' → {'add ●' if word[0] in 'AEIOU' else 'no change'}: {correct}."
        elif rt == 1:
            rule = "If ends with consonant, add ★ at end."
            correct = (base + "★") if word[-1] not in "AEIOU" else base
            expl = f"Base: {base}. Last='{word[-1]}' → {'add ★' if word[-1] not in 'AEIOU' else 'no change'}: {correct}."
        else:
            rule = "If repeated letter, reverse code."
            has_rep = len(set(word)) < len(word)
            correct = base[::-1] if has_rep else base
            expl = f"Base: {base}. {'Repeat' if has_rep else 'No repeat'} → {correct}."

        alts = ["●" + base, base + "★", base[::-1], base]
        ds = [a for a in alts if a != correct][:3]
        key_d = " | ".join(f"{l}={s}" for l, s in sm.items())
        qs.append(q(qid, "Hard",
            f"Key: {key_d}. Rule: {rule} Encode: {word}",
            four_choices(correct, ds), correct, expl,
            ["symbol-substitution", "conditional"]))
        qid += 1

    # Type 4: Position-based two-step (25)
    for i in range(25):
        fk = FIXED_KEYS[i % len(FIXED_KEYS)]
        kl, kd = fk["letters"], fk["digits"]
        pool = [w for w in WORDS_5 if all(c in kl for c in w)]
        if not pool:
            pool = ["".join(random.sample(kl, 5)) for _ in range(20)]
        word = pool[i % len(pool)]
        base = encode_key(word, kl, kd)
        correct = "".join(str((int(d) + j + 1) % 10) if d.isdigit() else d
                         for j, d in enumerate(base))
        wrong0 = base
        wrong1 = "".join(str((int(d) + j) % 10) if d.isdigit() else d for j, d in enumerate(base))
        wrong2 = "".join(str((int(d) - j - 1) % 10) if d.isdigit() else d for j, d in enumerate(base))
        ds = [a for a in [wrong0, wrong1, wrong2] if a != correct][:3]
        while len(ds) < 3:
            ds.append("".join(str(random.randint(0, 9)) for _ in range(len(correct))))
        expl = f"Base: {base}. Add positions (1-indexed): " + ", ".join(
            f"{base[j]}+{j+1}={correct[j]}" for j in range(len(base))) + "."
        qs.append(q(qid, "Hard",
            f"Key: [{fmt_key(kl,kd)}]. Rule: After encoding, add position# (1,2,3...) to each digit (mod 10). Encode: {word}",
            four_choices(correct, ds), correct, expl,
            ["position-based", "two-step"]))
        qid += 1

    # Type 5: Long keyword 7-char (25)
    for i in range(25):
        kw = KEYWORDS_10[i % len(KEYWORDS_10)]
        ds_str = "1234567890"
        if i < 13:
            number = "".join(random.choice(ds_str) for _ in range(7))
            correct = num_to_letters(number, kw, ds_str)
            txt = f"Keyword: {kw} (1-2-3-4-5-6-7-8-9-0). Convert {number} to letters:"
            step = ", ".join(f"{d}→{kw[ds_str.index(d)]}" for d in number)
            expl = f"{step} = {correct}."
            ds = make_distractors(correct, lambda: "".join(
                kw[random.randint(0, 9)] for _ in range(7)))
        else:
            word = "".join(random.choice(kw) for _ in range(7))
            correct = encode_key(word, kw, ds_str)
            txt = f"Keyword: {kw} (1-2-3-4-5-6-7-8-9-0). Convert {word} to digits:"
            step = ", ".join(f"{c}→{ds_str[kw.index(c)]}" for c in word)
            expl = f"{step} = {correct}."
            ds = make_distractors(correct, lambda: "".join(
                ds_str[random.randint(0, 9)] for _ in range(7)))
        qs.append(q(qid, "Hard", txt,
            four_choices(correct, ds), correct, expl,
            ["keyword-cipher", "7-character"]))
        qid += 1

    # Type 6: Mixed system (half key, half Caesar) (20)
    for i in range(20):
        fk = FIXED_KEYS[i % len(FIXED_KEYS)]
        kl, kd = fk["letters"], fk["digits"]
        word = WORDS_6[i % len(WORDS_6)]
        first = encode_key(word[:3], kl, kd)
        second = shift_word(word[3:], 3)
        correct = first + second
        wrong1 = shift_word(word[:3], 3) + encode_key(word[3:], kl, kd)
        wrong2 = encode_key(word, kl, kd)
        wrong3 = shift_word(word, 3)
        ds = [a for a in [wrong1, wrong2, wrong3] if a != correct][:3]
        while len(ds) < 3:
            ds.append(correct[::-1])
        expl = f"'{word[:3]}'→key→{first}, '{word[3:]}'→+3 shift→{second}. Combined: {correct}."
        qs.append(q(qid, "Hard",
            f"Key: [{fmt_key(kl,kd)}]. Rule: First 3 letters use number key, last 3 use +3 shift. Encode: {word}",
            four_choices(correct, ds), correct, expl,
            ["mixed-system", "two-step"]))
        qid += 1

    # Type 7: Reverse-engineer the shift (25)
    for i in range(25):
        shift = random.randint(3, 9)
        word = WORDS_4[i % len(WORDS_4)]
        encoded = shift_word(word, shift)
        correct = f"+{shift}"
        wrongs = random.sample([s for s in range(1, 13) if s != shift], 3)
        ds = [f"+{s}" for s in wrongs]
        qs.append(q(qid, "Hard",
            f"'{word}' was encoded as '{encoded}'. What shift was used?",
            four_choices(correct, ds), correct,
            f"{word[0]}→{encoded[0]} = {shift} positions. Shift: +{shift}.",
            ["shifted-alphabet", "reverse-engineer"]))
        qid += 1

    return qs[:200]


# ============================================================
# MAIN
# ============================================================

def main():
    print("Generating Code Conversion questions...")
    easy = gen_easy()
    medium = gen_medium()
    hard = gen_hard()
    all_q = easy + medium + hard

    # Sequential IDs
    for i, question in enumerate(all_q):
        question["id"] = i + 1

    # Validate
    errors = []
    for question in all_q:
        if question["answer"] not in question["choices"]:
            errors.append(f"Q{question['id']}: answer not in choices")
        if len(question["choices"]) != 4:
            errors.append(f"Q{question['id']}: {len(question['choices'])} choices")
    if errors:
        for e in errors[:10]:
            print(f"  ERROR: {e}")
        print(f"  {len(errors)} total errors")
        return

    # Write
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability", "coding-and-decoding", "code-conversion")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "questions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_q, f, indent=2, ensure_ascii=False)

    diffs = {"Easy": 0, "Medium": 0, "Hard": 0}
    for question in all_q:
        diffs[question["difficulty"]] += 1
    print(f"  Easy={diffs['Easy']}, Medium={diffs['Medium']}, Hard={diffs['Hard']}")
    print(f"  Total: {len(all_q)}")
    print(f"  Output: {out_path}")
    print("Done!")

if __name__ == "__main__":
    main()
