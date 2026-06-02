"""
Diversity audit for homophones/questions.json
Reports: tag distribution, question type distribution, homophone pair coverage,
sentence template repetition, and flags over-represented patterns.
"""
import json
from collections import Counter, defaultdict
import re

PATH = "data/seed/questions/clerical-ability/spelling/homophones/questions.json"
data = json.load(open(PATH, encoding="utf-8"))

# ── 1. Tag distribution ────────────────────────────────────────────────────
tag_counts = Counter()
for q in data:
    for t in q["tags"]:
        tag_counts[t] += 1

# ── 2. Homophone pair coverage ─────────────────────────────────────────────
PAIR_TAGS = [
    "affect-effect", "principal-principle", "their-there-theyre",
    "ensure-insure-assure", "complement-compliment", "stationary-stationery",
    "counsel-council", "precede-proceed", "moral-morale", "discrete-discreet",
    "formally-formerly", "passed-past", "weather-whether", "weak-week",
    "waste-waist", "vain-vane-vein", "cite-site-sight", "right-write-rite",
    "role-roll", "sole-soul", "bail-bale", "altar-alter", "brake-break",
    "forth-fourth", "profit-prophet", "its-its", "your-youre", "whose-whos",
    "hear-here", "their-there-theyre", "grate-great", "groan-grown",
    "hail-hale", "heal-heel", "idle-idol", "miner-minor", "naval-navel",
    "peer-pier", "pleas-please", "tide-tied", "wear-where-ware",
    "ring-wring", "soar-sore", "steal-steel", "straight-strait",
    "threw-through", "toad-towed", "wail-whale", "seam-seem",
    "shear-sheer", "stake-steak", "stair-stare", "meat-meet-mete",
    "pair-pare-pear", "peace-piece", "plain-plane", "pray-prey",
    "rap-wrap", "raze-raise", "reign-rain-rein", "loot-lute",
    "loose-lose", "made-maid", "mail-male", "board-bored",
    "capital-capitol", "coarse-course", "dual-duel", "flair-flare",
    "hole-whole", "hour-our", "know-no", "knew-new", "lead-led",
    "lessen-lesson", "bare-bear", "allowed-aloud",
]
pair_counts = {p: tag_counts.get(p, 0) for p in PAIR_TAGS}

# ── 3. Question type distribution ─────────────────────────────────────────
type_counts = Counter()
for q in data:
    txt = q["question"].lower()
    if "fill" in txt or "correctly completes" in txt or "correctly fills" in txt:
        type_counts["fill-in-blank"] += 1
    elif "which sentence" in txt and "incorrect" in txt:
        type_counts["find-incorrect-sentence"] += 1
    elif "which sentence" in txt and "correct" in txt and "incorrect" not in txt:
        type_counts["find-correct-sentence"] += 1
    elif "which sentence contains a homophone error" in txt:
        type_counts["find-error-in-set"] += 1
    elif "read the memo" in txt or "memo reads" in txt or "memo excerpt" in txt or "memo states" in txt or "document states" in txt or "report states" in txt or "order states" in txt or "advisory states" in txt or "resolution states" in txt or "ordinance states" in txt or "brief states" in txt or "record states" in txt or "posting states" in txt or "description states" in txt or "statement states" in txt or "note states" in txt or "evaluation states" in txt or "report states" in txt or "timeline states" in txt or "schedule states" in txt or "circular states" in txt:
        type_counts["memo-error-detection"] += 1
    elif "all homophones" in txt or "all homophones are used correctly" in txt:
        type_counts["multi-homophone-sentence"] += 1
    elif "which word" in txt and "incorrectly" in txt:
        type_counts["find-incorrect-word"] += 1
    elif "which word" in txt and "correctly" in txt:
        type_counts["find-correct-word"] += 1
    elif "which sentence is correct" in txt:
        type_counts["verify-two-sentences"] += 1
    else:
        type_counts["other"] += 1

# ── 4. Sentence template repetition ───────────────────────────────────────
# Extract the core sentence pattern (strip the blank word)
templates = Counter()
for q in data:
    # Normalize: lowercase, strip leading instruction
    txt = q["question"]
    # Extract the quoted sentence if present
    match = re.search(r"'([^']+)'", txt)
    if match:
        sentence = match.group(1)
        # Replace the blank
        sentence = re.sub(r"_+", "BLANK", sentence)
        templates[sentence] += 1
    else:
        templates[txt[:80]] += 1

repeated = {k: v for k, v in templates.items() if v > 1}

# ── 5. Exact question text duplicates ─────────────────────────────────────
question_texts = Counter(q["question"] for q in data)
exact_dupes = {k: v for k, v in question_texts.items() if v > 1}

# ── 6. affect-effect dominance check ──────────────────────────────────────
ae_count = tag_counts.get("affect-effect", 0)
ae_pct = ae_count / len(data) * 100

# ── Report ─────────────────────────────────────────────────────────────────
print(f"\n{'='*65}")
print(f"DIVERSITY AUDIT — {len(data)} questions")
print(f"{'='*65}")

print(f"\n── QUESTION TYPE DISTRIBUTION ──")
for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
    bar = "█" * (c // 5)
    print(f"  {t:<35} {c:>4}  {bar}")

print(f"\n── HOMOPHONE PAIR COVERAGE ──")
zero_coverage = []
low_coverage = []
for pair in sorted(PAIR_TAGS):
    c = pair_counts.get(pair, 0)
    if c == 0:
        zero_coverage.append(pair)
    elif c < 3:
        low_coverage.append((pair, c))

print(f"  Pairs with ZERO coverage ({len(zero_coverage)}):")
for p in zero_coverage:
    print(f"    ✗ {p}")
print(f"  Pairs with LOW coverage (<3) ({len(low_coverage)}):")
for p, c in low_coverage:
    print(f"    △ {p}: {c}")

print(f"\n── TOP 15 MOST-USED TAGS ──")
for tag, count in tag_counts.most_common(15):
    bar = "█" * (count // 10)
    pct = count / len(data) * 100
    print(f"  {tag:<35} {count:>4} ({pct:4.1f}%)  {bar}")

print(f"\n── AFFECT/EFFECT DOMINANCE ──")
print(f"  affect-effect questions: {ae_count} ({ae_pct:.1f}% of bank)")
if ae_pct > 40:
    print(f"  ⚠ OVER-REPRESENTED — should be ≤25% for a diverse bank")
else:
    print(f"  ✓ Within acceptable range")

print(f"\n── EXACT QUESTION DUPLICATES ──")
if exact_dupes:
    print(f"  ⚠ {len(exact_dupes)} duplicate question texts found:")
    for k, v in list(exact_dupes.items())[:10]:
        print(f"    ({v}x) {k[:80]}")
else:
    print(f"  ✓ No exact duplicates")

print(f"\n── REPEATED SENTENCE TEMPLATES ──")
high_repeat = {k: v for k, v in repeated.items() if v >= 10}
if high_repeat:
    print(f"  ⚠ {len(high_repeat)} templates used 5+ times:")
    for k, v in sorted(high_repeat.items(), key=lambda x: -x[1])[:10]:
        print(f"    ({v}x) {k[:80]}")
else:
    print(f"  ✓ No template used 5+ times")

print(f"\n{'='*65}")
print("VERDICT")
print(f"{'='*65}")
issues = []
if ae_pct > 40:
    issues.append(f"affect-effect is {ae_pct:.0f}% of the bank (target ≤25%)")
if zero_coverage:
    issues.append(f"{len(zero_coverage)} homophone pairs have zero coverage")
if exact_dupes:
    issues.append(f"{len(exact_dupes)} exact duplicate questions")
if high_repeat:
    issues.append(f"{len(high_repeat)} sentence templates repeated 5+ times")
if issues:
    print("  DIVERSITY PROBLEMS:")
    for i in issues:
        print(f"  ✗ {i}")
else:
    print("  ✓ Bank is sufficiently diverse")
