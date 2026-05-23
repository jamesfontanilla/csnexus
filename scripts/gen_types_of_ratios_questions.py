"""
Generate 600 multiple-choice questions on Types of Ratios for the CSE Numerical Ability section.
Distribution: 200 Easy, 200 Medium, 200 Hard
Output: data/seed/questions/numerical-ability/ratio-proportion-and-average/types-of-ratios/questions.json
"""

import json
import random
import os
from math import gcd

random.seed(42)

questions = []
current_id = 0


def next_id():
    global current_id
    current_id += 1
    return current_id


def make_q(difficulty, question, choices, answer, explanation, tags):
    return {
        "id": next_id(),
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Types of Ratios",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English",
    }


def simplify(a, b):
    """Return simplified ratio tuple."""
    g = gcd(a, b)
    return (a // g, b // g)


def ratio_str(a, b):
    """Format ratio as string."""
    return f"{a}:{b}"


def shuffle_choices(choices, answer):
    """Shuffle choices and return (shuffled_list, answer_string)."""
    random.shuffle(choices)
    return choices


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Category 1: Identify ratio type (conceptual) --- (40 questions)

type_definitions = [
    ("Which type of ratio compares one category to another category (not the total)?",
     "Part-to-part ratio",
     ["Part-to-whole ratio", "Equivalent ratio", "Unit ratio"],
     "A part-to-part ratio compares one subgroup to another subgroup, not to the total.",
     ["ratio types", "part-to-part", "definition"]),
    ("Which type of ratio compares a category to the total of all categories?",
     "Part-to-whole ratio",
     ["Part-to-part ratio", "Equivalent ratio", "Unit ratio"],
     "A part-to-whole ratio compares one subgroup to the entire group (the total).",
     ["ratio types", "part-to-whole", "definition"]),
    ("Which type of ratio has 1 as its second term?",
     "Unit ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Equivalent ratio"],
     "A unit ratio expresses a quantity per one unit, so the second term is always 1.",
     ["ratio types", "unit ratio", "definition"]),
    ("Which type of ratio represents the same relationship using different numbers?",
     "Equivalent ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Unit ratio"],
     "Equivalent ratios express the same proportional relationship with different numbers (e.g., 2:3 = 4:6).",
     ["ratio types", "equivalent", "definition"]),
    ("The ratio 'boys to girls = 3:5' is an example of what type of ratio?",
     "Part-to-part ratio",
     ["Part-to-whole ratio", "Unit ratio", "Equivalent ratio"],
     "Boys and girls are both subgroups of the class. Comparing one subgroup to another is part-to-part.",
     ["ratio types", "part-to-part", "classification"]),
    ("The ratio 'boys to total students = 3:8' is an example of what type of ratio?",
     "Part-to-whole ratio",
     ["Part-to-part ratio", "Unit ratio", "Equivalent ratio"],
     "Boys are a subgroup and total students is the whole. Comparing a part to the whole is part-to-whole.",
     ["ratio types", "part-to-whole", "classification"]),
    ("The expression '60 km per hour' represents what type of ratio?",
     "Unit ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Equivalent ratio"],
     "'Per hour' means per 1 hour. A ratio with 1 as the second term is a unit ratio.",
     ["ratio types", "unit ratio", "classification"]),
    ("If 2:3 = 4:6 = 6:9, these are examples of what type of ratio?",
     "Equivalent ratios",
     ["Part-to-part ratios", "Part-to-whole ratios", "Unit ratios"],
     "These ratios all simplify to 2:3 — they represent the same relationship with different numbers.",
     ["ratio types", "equivalent", "classification"]),
]

# Generate conceptual identification questions
for q_text, correct, distractors, expl, tags in type_definitions:
    choices = [correct] + distractors
    shuffle_choices(choices, correct)
    questions.append(make_q("Easy", q_text, choices, correct, expl, tags))

# More conceptual questions with varied wording
conceptual_easy = [
    ("What keyword signals a part-to-whole ratio?",
     "Out of the total",
     ["For every", "Compared to", "Versus"],
     "'Out of the total' indicates comparing a part to the whole group.",
     ["ratio types", "keywords", "part-to-whole"]),
    ("What keyword signals a unit ratio?",
     "Per",
     ["Out of", "To", "Versus"],
     "'Per' means 'for every one,' which is the definition of a unit ratio.",
     ["ratio types", "keywords", "unit ratio"]),
    ("In the statement 'for every 3 boys there are 5 girls,' what type of ratio is expressed?",
     "Part-to-part",
     ["Part-to-whole", "Unit ratio", "Equivalent ratio"],
     "'For every 3 boys there are 5 girls' compares one group to another — part-to-part.",
     ["ratio types", "part-to-part", "interpretation"]),
    ("In the statement '3 out of 8 students are boys,' what type of ratio is expressed?",
     "Part-to-whole",
     ["Part-to-part", "Unit ratio", "Equivalent ratio"],
     "'3 out of 8' compares a part (boys) to the whole (all students) — part-to-whole.",
     ["ratio types", "part-to-whole", "interpretation"]),
    ("Which ratio type can be directly converted to a fraction?",
     "Part-to-whole ratio",
     ["Part-to-part ratio", "Unit ratio", "None of these"],
     "A part-to-whole ratio a:total converts directly to the fraction a/total.",
     ["ratio types", "part-to-whole", "fractions"]),
    ("If a class has 10 boys and 15 girls, what is the 'whole' for a part-to-whole ratio?",
     "25",
     ["10", "15", "5"],
     "The whole is the total of all parts: 10 + 15 = 25.",
     ["ratio types", "part-to-whole", "total"]),
    ("What must you do to BOTH terms of a ratio to create an equivalent ratio?",
     "Multiply or divide by the same number",
     ["Add the same number", "Subtract the same number", "Square both terms"],
     "Equivalent ratios are created by multiplying or dividing both terms by the same non-zero number.",
     ["ratio types", "equivalent", "procedure"]),
    ("The ratio 5:1 means what in the context '5 students per teacher'?",
     "There are 5 students for every 1 teacher",
     ["There are 5 teachers for every student", "5 out of 6 are students", "The total is 5"],
     "A unit ratio of 5:1 means 5 of the first quantity for every 1 of the second.",
     ["ratio types", "unit ratio", "interpretation"]),
    ("Which is TRUE about part-to-part ratios?",
     "Neither term represents the total",
     ["The second term is always the total", "The first term must be larger", "They always simplify to 1:n"],
     "In a part-to-part ratio, both terms are subgroups — neither is the total.",
     ["ratio types", "part-to-part", "properties"]),
    ("Which is TRUE about part-to-whole ratios?",
     "The first term must be less than or equal to the second term",
     ["The first term is always larger", "Both terms are subgroups", "The second term equals 1"],
     "A part cannot exceed the whole, so the first term ≤ second term in a part-to-whole ratio.",
     ["ratio types", "part-to-whole", "properties"]),
    ("What type of ratio is '₱50 per kilogram'?",
     "Unit ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Equivalent ratio"],
     "'Per kilogram' means per 1 kg — this is a unit ratio (rate).",
     ["ratio types", "unit ratio", "rates"]),
    ("If the ratio of cats to dogs is 4:7, what is the ratio of cats to total animals (assuming only cats and dogs)?",
     "4:11",
     ["4:7", "7:11", "7:4"],
     "Total = 4 + 7 = 11. Cats to total = 4:11 (converting part-to-part to part-to-whole).",
     ["ratio types", "conversion", "part-to-whole"]),
]

for q_text, correct, distractors, expl, tags in conceptual_easy:
    choices = [correct] + distractors
    shuffle_choices(choices, correct)
    questions.append(make_q("Easy", q_text, choices, correct, expl, tags))

# --- Category 2: Simple part-to-part ratios --- (40 questions)

ptp_contexts = [
    ("boys", "girls", "class"),
    ("men", "women", "office"),
    ("cars", "motorcycles", "parking lot"),
    ("passed", "failed", "examinees"),
    ("red balls", "blue balls", "bag"),
    ("fiction books", "non-fiction books", "shelf"),
    ("desktop computers", "laptops", "office"),
    ("teachers", "students", "school"),
    ("managers", "staff", "department"),
    ("apples", "oranges", "basket"),
]

for i in range(40):
    ctx = ptp_contexts[i % len(ptp_contexts)]
    a_name, b_name, place = ctx
    # Generate numbers that simplify nicely
    base_a = random.randint(1, 5)
    base_b = random.randint(1, 5)
    while base_a == base_b:
        base_b = random.randint(1, 5)
    multiplier = random.randint(2, 8)
    a_val = base_a * multiplier
    b_val = base_b * multiplier
    sa, sb = simplify(a_val, b_val)
    correct = ratio_str(sa, sb)

    # Generate distractors
    dist = set()
    dist.add(ratio_str(sb, sa))  # reversed
    dist.add(ratio_str(sa, sa + sb))  # part-to-whole mistake
    dist.add(ratio_str(a_val, b_val))  # unsimplified (if different from correct)
    # Add a random wrong one
    dist.add(ratio_str(sa + 1, sb))
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(ratio_str(sa + random.randint(1, 3), sb + random.randint(1, 3)))

    q_text = f"A {place} has {a_val} {a_name} and {b_val} {b_name}. What is the simplified ratio of {a_name} to {b_name}?"
    expl = f"Ratio of {a_name} to {b_name} = {a_val}:{b_val}. GCF = {a_val // sa}. Simplified: {correct}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Easy", q_text, choices, correct, expl,
                            ["part-to-part", "simplification", "ratios"]))

# --- Category 3: Simple part-to-whole ratios --- (40 questions)

ptw_contexts = [
    ("boys", "students", "class"),
    ("female employees", "employees", "office"),
    ("defective items", "items produced", "factory"),
    ("absent students", "enrolled students", "section"),
    ("red marbles", "marbles", "jar"),
    ("fiction books", "books", "library"),
    ("passed applicants", "applicants", "exam"),
    ("registered voters", "residents", "barangay"),
    ("smartphones", "devices", "inventory"),
    ("vegetarian meals", "meals served", "cafeteria"),
]

for i in range(40):
    ctx = ptw_contexts[i % len(ptw_contexts)]
    part_name, whole_name, place = ctx
    # Generate part and whole
    base_part = random.randint(1, 4)
    base_whole = random.randint(base_part + 1, base_part + 6)
    multiplier = random.randint(2, 10)
    part_val = base_part * multiplier
    whole_val = base_whole * multiplier
    sp, sw = simplify(part_val, whole_val)
    correct = ratio_str(sp, sw)

    dist = set()
    dist.add(ratio_str(sw, sp))  # reversed
    dist.add(ratio_str(sp, sw - sp))  # part-to-part mistake
    dist.add(ratio_str(part_val, whole_val))  # unsimplified
    dist.add(ratio_str(sp + 1, sw))
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(ratio_str(sp, sw + random.randint(1, 3)))

    q_text = f"In a {place}, there are {part_val} {part_name} out of {whole_val} {whole_name}. What is the simplified ratio of {part_name} to total {whole_name}?"
    expl = f"{part_name} to total = {part_val}:{whole_val}. GCF = {part_val // sp}. Simplified: {correct}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Easy", q_text, choices, correct, expl,
                            ["part-to-whole", "simplification", "ratios"]))

# --- Category 4: Simple equivalent ratio identification --- (40 questions)

for i in range(40):
    base_a = random.randint(1, 6)
    base_b = random.randint(1, 6)
    while base_a == base_b:
        base_b = random.randint(1, 6)
    g = gcd(base_a, base_b)
    base_a, base_b = base_a // g, base_b // g  # ensure simplest form

    mult = random.randint(2, 8)
    equiv_a = base_a * mult
    equiv_b = base_b * mult

    correct = ratio_str(equiv_a, equiv_b)

    # Distractors: wrong scaling
    dist = set()
    dist.add(ratio_str(equiv_a + 1, equiv_b))
    dist.add(ratio_str(equiv_a, equiv_b + 1))
    dist.add(ratio_str(base_a * (mult + 1), base_b * (mult - 1)))  # different multipliers
    dist.add(ratio_str(equiv_a + base_a, equiv_b))  # added instead of multiplied
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(ratio_str(equiv_a + random.randint(1, 4), equiv_b + random.randint(1, 4)))

    q_text = f"Which ratio is equivalent to {base_a}:{base_b}?"
    expl = f"Multiply both terms of {base_a}:{base_b} by {mult}: {base_a}×{mult}={equiv_a}, {base_b}×{mult}={equiv_b}. So {correct} is equivalent."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Easy", q_text, choices, correct, expl,
                            ["equivalent ratios", "scaling", "ratios"]))

# --- Category 5: Simple unit ratio calculations --- (40 questions)

unit_contexts = [
    ("km", "hours", "speed", "km per hour"),
    ("pages", "days", "reading rate", "pages per day"),
    ("items", "workers", "productivity", "items per worker"),
    ("pesos", "notebooks", "price", "pesos per notebook"),
    ("liters", "hours", "flow rate", "liters per hour"),
    ("students", "teachers", "class size", "students per teacher"),
    ("words", "minutes", "typing speed", "words per minute"),
    ("calls", "hours", "call rate", "calls per hour"),
]

for i in range(40):
    ctx = unit_contexts[i % len(unit_contexts)]
    unit_a, unit_b, context_name, rate_label = ctx
    # Generate clean division
    unit_rate = random.randint(3, 60)
    num_b = random.randint(2, 10)
    total_a = unit_rate * num_b
    correct = str(unit_rate)

    dist = set()
    dist.add(str(unit_rate + random.randint(1, 5)))
    dist.add(str(unit_rate - random.randint(1, min(3, unit_rate - 1))) if unit_rate > 3 else str(unit_rate + 7))
    dist.add(str(num_b))  # common mistake: giving the divisor
    dist.add(str(total_a))  # common mistake: giving the total
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(str(unit_rate + random.randint(2, 8)))

    q_text = f"If there are {total_a} {unit_a} in {num_b} {unit_b}, what is the unit ratio ({rate_label})?"
    expl = f"Unit ratio = {total_a} ÷ {num_b} = {unit_rate} {rate_label}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Easy", q_text, choices, correct, expl,
                            ["unit ratio", "rates", "division"]))

# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Category 6: Convert part-to-part to part-to-whole --- (35 questions)

convert_contexts = [
    ("boys", "girls", "students"),
    ("male employees", "female employees", "employees"),
    ("passed", "failed", "examinees"),
    ("cars", "motorcycles", "vehicles"),
    ("fiction", "non-fiction", "books"),
    ("approved", "rejected", "applications"),
    ("domestic", "imported", "products"),
]

for i in range(35):
    ctx = convert_contexts[i % len(convert_contexts)]
    a_name, b_name, total_name = ctx
    base_a = random.randint(1, 7)
    base_b = random.randint(1, 7)
    while base_a == base_b:
        base_b = random.randint(1, 7)
    g = gcd(base_a, base_b)
    base_a, base_b = base_a // g, base_b // g
    total_parts = base_a + base_b

    # Ask for part-to-whole given part-to-part
    correct = ratio_str(base_a, total_parts)
    dist = set()
    dist.add(ratio_str(base_a, base_b))  # gave part-to-part
    dist.add(ratio_str(base_b, total_parts))  # wrong part
    dist.add(ratio_str(total_parts, base_a))  # reversed
    dist.add(ratio_str(base_a + 1, total_parts))
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(ratio_str(base_a, total_parts + random.randint(1, 3)))

    q_text = f"The ratio of {a_name} to {b_name} is {base_a}:{base_b}. What is the ratio of {a_name} to total {total_name}?"
    expl = f"Total parts = {base_a} + {base_b} = {total_parts}. {a_name} to total = {base_a}:{total_parts}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Medium", q_text, choices, correct, expl,
                            ["part-to-part", "part-to-whole", "conversion"]))

# --- Category 7: Find missing term in equivalent ratio --- (35 questions)

for i in range(35):
    base_a = random.randint(1, 8)
    base_b = random.randint(1, 8)
    while base_a == base_b:
        base_b = random.randint(1, 8)
    g = gcd(base_a, base_b)
    base_a, base_b = base_a // g, base_b // g

    mult = random.randint(2, 9)
    target_b = base_b * mult
    correct_a = base_a * mult
    correct = str(correct_a)

    dist = set()
    dist.add(str(correct_a + base_a))
    dist.add(str(correct_a - base_a) if correct_a > base_a else str(correct_a + 2 * base_a))
    dist.add(str(target_b))  # used wrong term
    dist.add(str(base_a + target_b))  # added instead
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(str(correct_a + random.randint(1, 5)))

    q_text = f"If {base_a}:{base_b} = n:{target_b}, what is the value of n?"
    expl = f"Since {base_b} × {mult} = {target_b}, multiply {base_a} by {mult}: {base_a} × {mult} = {correct_a}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Medium", q_text, choices, correct, expl,
                            ["equivalent ratios", "missing term", "proportion"]))

# --- Category 8: Unit price comparison --- (30 questions)

items_for_price = ["notebooks", "pens", "folders", "reams of paper", "markers",
                   "envelopes", "stamps", "USB drives", "batteries", "ink cartridges"]

for i in range(30):
    item = items_for_price[i % len(items_for_price)]
    # Store A
    qty_a = random.randint(3, 10)
    unit_price_a = random.randint(15, 80)
    total_a = qty_a * unit_price_a
    # Store B - different unit price
    qty_b = random.randint(3, 10)
    while qty_b == qty_a:
        qty_b = random.randint(3, 10)
    unit_price_b = unit_price_a + random.choice([-5, -3, -2, 3, 5, 7, 10])
    if unit_price_b <= 0:
        unit_price_b = unit_price_a + 5
    total_b = qty_b * unit_price_b

    if unit_price_a < unit_price_b:
        correct = f"Store A (₱{unit_price_a} per {item[:-1] if item.endswith('s') else item})"
        cheaper = "A"
    else:
        correct = f"Store B (₱{unit_price_b} per {item[:-1] if item.endswith('s') else item})"
        cheaper = "B"

    other_store = "B" if cheaper == "A" else "A"
    other_price = unit_price_b if cheaper == "A" else unit_price_a
    dist = [
        f"Store {other_store} (₱{other_price} per {item[:-1] if item.endswith('s') else item})",
        f"Both have the same unit price",
        f"Cannot be determined",
    ]

    q_text = f"Store A sells {qty_a} {item} for ₱{total_a}. Store B sells {qty_b} {item} for ₱{total_b}. Which store offers the cheaper unit price?"
    expl = f"Store A: ₱{total_a} ÷ {qty_a} = ₱{unit_price_a} each. Store B: ₱{total_b} ÷ {qty_b} = ₱{unit_price_b} each. Store {cheaper} is cheaper."
    choices = [correct] + dist
    shuffle_choices(choices, correct)
    questions.append(make_q("Medium", q_text, choices, correct, expl,
                            ["unit ratio", "comparison", "unit price"]))

# --- Category 9: Identify ratio type from word problem --- (35 questions)

medium_type_id = [
    ("A government office has 15 clerks and 5 supervisors. The ratio of clerks to supervisors is 3:1. What type of ratio is this?",
     "Part-to-part ratio",
     ["Part-to-whole ratio", "Unit ratio", "Equivalent ratio"],
     "Clerks and supervisors are both subgroups of the office. Comparing one subgroup to another is part-to-part.",
     ["ratio types", "part-to-part", "classification"]),
    ("In a barangay, 2,400 out of 8,000 residents are registered voters. The ratio 2,400:8,000 is what type?",
     "Part-to-whole ratio",
     ["Part-to-part ratio", "Unit ratio", "Equivalent ratio"],
     "Registered voters (part) compared to all residents (whole) is a part-to-whole ratio.",
     ["ratio types", "part-to-whole", "classification"]),
    ("A delivery truck covers 450 km in 9 hours. The ratio 50:1 (km per hour) is what type?",
     "Unit ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Equivalent ratio"],
     "50 km per 1 hour has 1 as the second term — this is a unit ratio (rate).",
     ["ratio types", "unit ratio", "classification"]),
    ("A recipe uses sugar and flour in the ratio 1:4. For a bigger batch, 3 cups sugar and 12 cups flour are used. The ratios 1:4 and 3:12 are what type?",
     "Equivalent ratios",
     ["Part-to-part ratios", "Part-to-whole ratios", "Unit ratios"],
     "1:4 and 3:12 represent the same relationship (both simplify to 1:4) — they are equivalent.",
     ["ratio types", "equivalent", "classification"]),
    ("A school report states that 3/5 of students passed the exam. This fraction represents what ratio type?",
     "Part-to-whole ratio",
     ["Part-to-part ratio", "Unit ratio", "Equivalent ratio"],
     "A fraction (3/5) compares a part (passed) to the whole (all students) — part-to-whole.",
     ["ratio types", "part-to-whole", "fractions"]),
    ("In a parking lot, for every 4 cars there are 3 motorcycles. This is what type of ratio?",
     "Part-to-part ratio",
     ["Part-to-whole ratio", "Unit ratio", "Equivalent ratio"],
     "'For every 4 cars there are 3 motorcycles' compares one group to another — part-to-part.",
     ["ratio types", "part-to-part", "interpretation"]),
    ("A government agency processes 120 applications per day. This rate is what type of ratio?",
     "Unit ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Equivalent ratio"],
     "'Per day' means per 1 day. A ratio with 1 as the second term is a unit ratio.",
     ["ratio types", "unit ratio", "rates"]),
    ("The population density of a city is 5,000 people per square kilometer. What type of ratio is this?",
     "Unit ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Equivalent ratio"],
     "'Per square kilometer' means per 1 sq km — this is a unit ratio.",
     ["ratio types", "unit ratio", "population"]),
    ("A budget allocates ₱200,000 for salaries out of a total ₱500,000. The ratio 200,000:500,000 is what type?",
     "Part-to-whole ratio",
     ["Part-to-part ratio", "Unit ratio", "Equivalent ratio"],
     "Salaries (part) compared to total budget (whole) is a part-to-whole ratio.",
     ["ratio types", "part-to-whole", "budget"]),
    ("A team's win-loss record is 18:6. This is what type of ratio?",
     "Part-to-part ratio",
     ["Part-to-whole ratio", "Unit ratio", "Equivalent ratio"],
     "Wins and losses are both subgroups of total games. Comparing them is part-to-part.",
     ["ratio types", "part-to-part", "sports"]),
    ("If 2:5 = 6:15, what relationship do these ratios have?",
     "They are equivalent ratios",
     ["They are part-to-part ratios", "They are unit ratios", "They have no relationship"],
     "2:5 and 6:15 both simplify to 2:5 (multiply by 3). They are equivalent.",
     ["ratio types", "equivalent", "verification"]),
    ("A factory's defect rate is 1 defective item for every 50 produced. The ratio 1:50 is what type?",
     "Part-to-whole ratio",
     ["Part-to-part ratio", "Unit ratio", "Equivalent ratio"],
     "1 defective out of 50 total produced compares a part to the whole — part-to-whole.",
     ["ratio types", "part-to-whole", "quality"]),
    ("An employee earns ₱800 per hour. What type of ratio does this represent?",
     "Unit ratio",
     ["Part-to-part ratio", "Part-to-whole ratio", "Equivalent ratio"],
     "'Per hour' means per 1 hour — this is a unit ratio (₱800:1 hour).",
     ["ratio types", "unit ratio", "salary"]),
    ("In a survey, the ratio of 'agree' to 'disagree' responses is 7:3. What type of ratio is this?",
     "Part-to-part ratio",
     ["Part-to-whole ratio", "Unit ratio", "Equivalent ratio"],
     "Agree and disagree are both subgroups of respondents. Comparing them is part-to-part.",
     ["ratio types", "part-to-part", "survey"]),
    ("A map uses a scale of 1 cm : 5 km. The ratios 1:5 and 3:15 are what type?",
     "Equivalent ratios",
     ["Part-to-part ratios", "Part-to-whole ratios", "Unit ratios"],
     "1:5 and 3:15 represent the same scale relationship — they are equivalent ratios.",
     ["ratio types", "equivalent", "map scale"]),
]

for q_text, correct, distractors, expl, tags in medium_type_id:
    choices = [correct] + distractors
    shuffle_choices(choices, correct)
    questions.append(make_q("Medium", q_text, choices, correct, expl, tags))

# --- Category 10: Part-to-whole with multiple categories --- (30 questions)

multi_cat_contexts = [
    (["red", "blue", "green"], "marbles", "bag"),
    (["shirts", "pants", "shoes"], "items", "store"),
    (["engineers", "accountants", "clerks"], "employees", "agency"),
    (["sedans", "SUVs", "trucks"], "vehicles", "fleet"),
    (["rice", "corn", "wheat"], "grains", "warehouse"),
]

for i in range(30):
    ctx = multi_cat_contexts[i % len(multi_cat_contexts)]
    categories, total_name, place = ctx
    # Generate 3 values
    vals = [random.randint(2, 6) * random.randint(2, 5) for _ in range(3)]
    total = sum(vals)
    # Pick which category to ask about
    ask_idx = i % 3
    ask_cat = categories[ask_idx]
    ask_val = vals[ask_idx]

    sp, sw = simplify(ask_val, total)
    correct = ratio_str(sp, sw)

    dist = set()
    # Common mistakes
    other_idx = (ask_idx + 1) % 3
    dist.add(ratio_str(ask_val, vals[other_idx]))  # part-to-part mistake
    so, st = simplify(vals[other_idx], total)
    dist.add(ratio_str(so, st))  # wrong category
    dist.add(ratio_str(sp, sw - sp))  # subtracted
    dist.add(ratio_str(sw, sp))  # reversed
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(ratio_str(sp + 1, sw))

    q_text = f"A {place} contains {vals[0]} {categories[0]}, {vals[1]} {categories[1]}, and {vals[2]} {categories[2]}. What is the simplified ratio of {ask_cat} to total {total_name}?"
    expl = f"Total = {vals[0]} + {vals[1]} + {vals[2]} = {total}. {ask_cat} to total = {ask_val}:{total}. GCF = {ask_val // sp}. Simplified: {correct}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Medium", q_text, choices, correct, expl,
                            ["part-to-whole", "multiple categories", "simplification"]))

# --- Category 11: Equivalent ratio verification (cross-multiply) --- (35 questions)

for i in range(35):
    base_a = random.randint(1, 7)
    base_b = random.randint(1, 7)
    while base_a == base_b:
        base_b = random.randint(1, 7)
    g = gcd(base_a, base_b)
    base_a, base_b = base_a // g, base_b // g

    mult = random.randint(2, 7)
    # Create one equivalent and three non-equivalent
    eq_a = base_a * mult
    eq_b = base_b * mult

    # Wrong ratios
    wrong1_a = base_a * mult + 1
    wrong1_b = base_b * mult
    wrong2_a = base_a * (mult + 1)
    wrong2_b = base_b * mult
    wrong3_a = base_a * mult
    wrong3_b = base_b * mult + 2

    correct = ratio_str(eq_a, eq_b)
    distractors = [
        ratio_str(wrong1_a, wrong1_b),
        ratio_str(wrong2_a, wrong2_b),
        ratio_str(wrong3_a, wrong3_b),
    ]

    q_text = f"Which of the following ratios is equivalent to {base_a}:{base_b}?"
    expl = f"{base_a}:{base_b} × {mult} = {eq_a}:{eq_b}. Cross-check: {base_a}×{eq_b} = {base_a * eq_b} and {base_b}×{eq_a} = {base_b * eq_a}. Equal, so they are equivalent."
    choices = [correct] + distractors
    shuffle_choices(choices, correct)
    questions.append(make_q("Medium", q_text, choices, correct, expl,
                            ["equivalent ratios", "cross-multiplication", "verification"]))

# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Category 12: Multi-step part-to-part → find actual values → part-to-whole --- (40 questions)

hard_contexts = [
    ("male", "female", "employees"),
    ("passed", "failed", "examinees"),
    ("fiction", "non-fiction", "books"),
    ("domestic", "imported", "products"),
    ("approved", "rejected", "applications"),
    ("urban", "rural", "residents"),
    ("regular", "contractual", "workers"),
    ("online", "walk-in", "customers"),
]

for i in range(40):
    ctx = hard_contexts[i % len(hard_contexts)]
    a_name, b_name, total_name = ctx
    # Part-to-part ratio
    ra = random.randint(2, 7)
    rb = random.randint(2, 7)
    while ra == rb:
        rb = random.randint(2, 7)
    g = gcd(ra, rb)
    ra, rb = ra // g, rb // g

    # Given one actual value
    mult = random.randint(5, 20)
    actual_a = ra * mult
    actual_b = rb * mult
    total = actual_a + actual_b

    # Ask: what fraction of total is b_name?
    sb, st = simplify(actual_b, total)
    correct = ratio_str(sb, st)

    dist = set()
    dist.add(ratio_str(rb, ra + rb))  # used ratio parts directly (might be same as correct)
    dist.add(ratio_str(ra, ra + rb))  # wrong part
    dist.add(ratio_str(rb, ra))  # part-to-part
    dist.add(ratio_str(st, sb))  # reversed
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(ratio_str(sb + 1, st))

    q_text = f"The ratio of {a_name} to {b_name} {total_name} is {ra}:{rb}. If there are {actual_a} {a_name} {total_name}, what is the ratio of {b_name} {total_name} to the total?"
    expl = f"{ra} parts = {actual_a}, so 1 part = {mult}. {b_name} = {rb} × {mult} = {actual_b}. Total = {actual_a} + {actual_b} = {total}. {b_name}:total = {actual_b}:{total} = {correct}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Hard", q_text, choices, correct, expl,
                            ["part-to-part", "part-to-whole", "multi-step"]))

# --- Category 13: Unit ratio comparison with non-obvious division --- (35 questions)

comparison_items = [
    ("kg of rice", "₱", "store"),
    ("liters of fuel", "km", "vehicle"),
    ("hours", "tasks completed", "employee"),
    ("reams of paper", "₱", "supplier"),
    ("meters of fabric", "₱", "shop"),
]

for i in range(35):
    ctx = comparison_items[i % len(comparison_items)]
    qty_unit, value_unit, entity = ctx

    # Generate two options with different unit rates
    qty1 = random.randint(3, 12)
    rate1 = random.randint(20, 95)
    total1 = qty1 * rate1

    qty2 = random.randint(3, 12)
    while qty2 == qty1:
        qty2 = random.randint(3, 12)
    rate2 = rate1 + random.choice([-7, -5, -3, 3, 5, 7])
    if rate2 <= 0:
        rate2 = rate1 + 5
    total2 = qty2 * rate2

    # Determine which is better (context-dependent)
    if "₱" in value_unit:
        # Lower price is better
        if rate1 < rate2:
            better = "A"
            correct = f"{entity.title()} A ({value_unit}{rate1} per {qty_unit.replace('s of ', ' of ').rstrip('s')})"
        else:
            better = "B"
            correct = f"{entity.title()} B ({value_unit}{rate2} per {qty_unit.replace('s of ', ' of ').rstrip('s')})"
    else:
        # Higher rate is better (more km per liter, more tasks per hour)
        if rate1 > rate2:
            better = "A"
            correct = f"{entity.title()} A ({rate1} {value_unit} per {qty_unit.rstrip('s')})"
        else:
            better = "B"
            correct = f"{entity.title()} B ({rate2} {value_unit} per {qty_unit.rstrip('s')})"

    dist = [
        f"{entity.title()} {'B' if better == 'A' else 'A'}",
        "Both are equal",
        "Cannot be determined from the given information",
    ]

    q_text = f"{entity.title()} A: {total1} {value_unit} for {qty1} {qty_unit}. {entity.title()} B: {total2} {value_unit} for {qty2} {qty_unit}. Which offers the better rate?"
    expl = f"{entity.title()} A: {total1} ÷ {qty1} = {rate1} per unit. {entity.title()} B: {total2} ÷ {qty2} = {rate2} per unit. {entity.title()} {better} is better."
    choices = [correct] + dist
    shuffle_choices(choices, correct)
    questions.append(make_q("Hard", q_text, choices, correct, expl,
                            ["unit ratio", "comparison", "multi-step"]))

# --- Category 14: Three-part ratios and finding specific values --- (35 questions)

three_part_contexts = [
    ("engineers", "accountants", "clerks", "employees"),
    ("rice", "corn", "wheat", "grains (in kg)"),
    ("salaries", "utilities", "supplies", "budget (in thousands)"),
    ("sedans", "SUVs", "vans", "vehicles"),
    ("Grade 1", "Grade 2", "Grade 3", "students"),
]

for i in range(35):
    ctx = three_part_contexts[i % len(three_part_contexts)]
    cat_a, cat_b, cat_c, total_name = ctx

    # Generate a 3-part ratio
    ra = random.randint(1, 5)
    rb = random.randint(1, 5)
    rc = random.randint(1, 5)
    # Ensure at least two are different
    while ra == rb == rc:
        rc = random.randint(1, 5)

    total_parts = ra + rb + rc
    mult = random.randint(4, 15)
    total_actual = total_parts * mult

    # Ask for one category's actual value
    ask_idx = i % 3
    ask_names = [cat_a, cat_b, cat_c]
    ask_ratios = [ra, rb, rc]
    ask_name = ask_names[ask_idx]
    ask_ratio = ask_ratios[ask_idx]
    correct_val = ask_ratio * mult
    correct = str(correct_val)

    dist = set()
    dist.add(str(ask_ratio))  # gave ratio part, not actual
    dist.add(str(total_actual - correct_val))  # gave the rest
    dist.add(str(correct_val + mult))  # off by one part
    dist.add(str(correct_val - mult) if correct_val > mult else str(correct_val + 2 * mult))
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(str(correct_val + random.randint(1, 10)))

    q_text = f"The ratio of {cat_a} to {cat_b} to {cat_c} is {ra}:{rb}:{rc}. If the total number of {total_name} is {total_actual}, how many are {ask_name}?"
    expl = f"Total parts = {ra}+{rb}+{rc} = {total_parts}. One part = {total_actual} ÷ {total_parts} = {mult}. {ask_name} = {ask_ratio} × {mult} = {correct_val}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Hard", q_text, choices, correct, expl,
                            ["three-part ratio", "actual values", "division"]))

# --- Category 15: Ratio word problems requiring multiple conversions --- (30 questions)

for i in range(30):
    # Scenario: Given part-to-part, one actual value, find percentage (part-to-whole as %)
    ra = random.randint(2, 7)
    rb = random.randint(2, 7)
    while ra == rb:
        rb = random.randint(2, 7)
    g = gcd(ra, rb)
    ra, rb = ra // g, rb // g
    total_parts = ra + rb

    mult = random.randint(5, 20)
    actual_b = rb * mult
    actual_a = ra * mult
    total = actual_a + actual_b

    # What percentage is a of total?
    percentage = (actual_a / total) * 100
    # Ensure clean percentage
    if percentage != int(percentage):
        # Adjust to get clean percentage
        # Use ratio parts directly: ra/(ra+rb) * 100
        percentage = (ra * 100) / total_parts
        if percentage != int(percentage):
            # Force clean values
            ra, rb = 1, 3
            total_parts = 4
            mult = random.randint(5, 25)
            actual_a = ra * mult
            actual_b = rb * mult
            total = actual_a + actual_b
            percentage = 25.0

    pct_str = f"{percentage:.0f}%" if percentage == int(percentage) else f"{percentage:.1f}%"
    correct = pct_str

    # Distractors
    dist = set()
    other_pct = (rb * 100) / total_parts
    dist.add(f"{other_pct:.0f}%" if other_pct == int(other_pct) else f"{other_pct:.1f}%")
    dist.add(f"{ra * 10}%")
    dist.add(f"{(ra + rb) * 5}%")
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        fake_pct = int(percentage) + random.choice([-10, -5, 5, 10, 15])
        if fake_pct > 0 and fake_pct < 100:
            distractors.append(f"{fake_pct}%")
        else:
            distractors.append(f"{int(percentage) + 12}%")

    names = [("boys", "girls", "students"), ("passed", "failed", "examinees"),
             ("male", "female", "employees"), ("approved", "rejected", "applications"),
             ("urban", "rural", "households")]
    ctx = names[i % len(names)]
    a_name, b_name, total_name = ctx

    q_text = f"The ratio of {a_name} to {b_name} is {ra}:{rb}. What percentage of all {total_name} are {a_name}?"
    expl = f"Total parts = {ra} + {rb} = {total_parts}. {a_name} fraction = {ra}/{total_parts} = {percentage:.0f}% (or {percentage:.1f}%)."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Hard", q_text, choices, correct, expl,
                            ["part-to-part", "percentage", "conversion"]))

# --- Category 16: Complex equivalent ratio with scaling --- (30 questions)

for i in range(30):
    # Given a ratio and a total, find both actual values
    ra = random.randint(2, 6)
    rb = random.randint(2, 6)
    while ra == rb:
        rb = random.randint(2, 6)
    g = gcd(ra, rb)
    ra, rb = ra // g, rb // g
    total_parts = ra + rb

    total_actual = total_parts * random.randint(5, 20)
    mult = total_actual // total_parts
    val_a = ra * mult
    val_b = rb * mult

    # Ask for the difference between the two groups
    diff = abs(val_a - val_b)
    correct = str(diff)

    dist = set()
    dist.add(str(val_a))
    dist.add(str(val_b))
    dist.add(str(total_actual))
    dist.add(str(diff + mult))
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(str(diff + random.randint(1, 10)))

    names = [("boys", "girls", "class"), ("winners", "losers", "contestants"),
             ("approved", "pending", "requests"), ("senior", "junior", "staff"),
             ("local", "foreign", "tourists")]
    ctx = names[i % len(names)]
    a_name, b_name, total_name = ctx

    q_text = f"In a {total_name} of {total_actual}, the ratio of {a_name} to {b_name} is {ra}:{rb}. What is the difference between the number of {a_name} and {b_name}?"
    expl = f"Total parts = {total_parts}. One part = {total_actual} ÷ {total_parts} = {mult}. {a_name} = {val_a}, {b_name} = {val_b}. Difference = |{val_a} - {val_b}| = {diff}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Hard", q_text, choices, correct, expl,
                            ["equivalent ratios", "actual values", "difference"]))

# --- Category 17: Ratio change problems --- (30 questions)

for i in range(30):
    # Original ratio, then one quantity changes, find new ratio
    ra = random.randint(2, 5)
    rb = random.randint(2, 5)
    while ra == rb:
        rb = random.randint(2, 5)
    g = gcd(ra, rb)
    ra, rb = ra // g, rb // g

    mult = random.randint(3, 10)
    orig_a = ra * mult
    orig_b = rb * mult

    # Change: add or remove from one group
    change = random.randint(2, 8)
    add_or_remove = random.choice(["added to", "removed from"])
    if add_or_remove == "added to":
        new_a = orig_a + change
    else:
        new_a = orig_a - change
        if new_a <= 0:
            new_a = orig_a + change
            add_or_remove = "added to"

    new_sa, new_sb = simplify(new_a, orig_b)
    correct = ratio_str(new_sa, new_sb)

    dist = set()
    dist.add(ratio_str(ra, rb))  # original ratio
    dist.add(ratio_str(new_sb, new_sa))  # reversed
    if add_or_remove == "added to":
        wrong_a = orig_a - change
    else:
        wrong_a = orig_a + change
    if wrong_a > 0:
        ws, wb = simplify(wrong_a, orig_b)
        dist.add(ratio_str(ws, wb))
    dist.add(ratio_str(new_sa + 1, new_sb))
    dist.discard(correct)
    distractors = list(dist)[:3]
    while len(distractors) < 3:
        distractors.append(ratio_str(new_sa + random.randint(1, 3), new_sb + random.randint(0, 2)))

    names = [("boys", "girls", "class"), ("engineers", "technicians", "team"),
             ("cats", "dogs", "shelter"), ("desktops", "laptops", "office"),
             ("fiction", "non-fiction", "collection")]
    ctx = names[i % len(names)]
    a_name, b_name, place = ctx

    q_text = f"A {place} originally has {orig_a} {a_name} and {orig_b} {b_name}. If {change} {a_name} are {add_or_remove} the {place}, what is the new ratio of {a_name} to {b_name}?"
    expl = f"New {a_name} = {new_a}. {b_name} unchanged = {orig_b}. New ratio = {new_a}:{orig_b} = {correct}."
    choices = [correct] + distractors[:3]
    shuffle_choices(choices, correct)
    questions.append(make_q("Hard", q_text, choices, correct, expl,
                            ["ratio change", "simplification", "multi-step"]))

# ============================================================
# OUTPUT
# ============================================================

# Verify counts
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}, Total: {len(questions)}")

# Pad if needed to reach exactly 200 per difficulty
def pad_easy(target=200):
    """Generate additional easy questions to reach target."""
    additional = []
    needed = target - sum(1 for q in questions if q["difficulty"] == "Easy")
    if needed <= 0:
        return additional

    simple_ratios = [(2, 3), (3, 4), (1, 2), (3, 5), (4, 5), (1, 3), (2, 5), (5, 6), (1, 4), (3, 7)]
    contexts = [
        "In a box, there are {a} red pens and {b} blue pens.",
        "A garden has {a} rose bushes and {b} sunflower plants.",
        "A shelf holds {a} textbooks and {b} notebooks.",
        "An office has {a} male staff and {b} female staff.",
        "A plate has {a} slices of mango and {b} slices of papaya.",
    ]

    for j in range(needed):
        base = simple_ratios[j % len(simple_ratios)]
        m = random.randint(2, 7)
        a_val = base[0] * m
        b_val = base[1] * m
        ctx_template = contexts[j % len(contexts)]
        ctx_text = ctx_template.format(a=a_val, b=b_val)

        correct = ratio_str(base[0], base[1])
        dist = [
            ratio_str(base[1], base[0]),
            ratio_str(base[0], base[0] + base[1]),
            ratio_str(a_val, b_val) if ratio_str(a_val, b_val) != correct else ratio_str(base[0] + 1, base[1]),
        ]

        q_text = f"{ctx_text} What is the simplified ratio of the first item to the second?"
        expl = f"Ratio = {a_val}:{b_val}. GCF = {m}. Simplified: {base[0]}:{base[1]}."
        additional.append(make_q("Easy", q_text, [correct] + dist, correct, expl,
                                 ["part-to-part", "simplification", "ratios"]))
    return additional


def pad_medium(target=200):
    """Generate additional medium questions to reach target."""
    additional = []
    needed = target - sum(1 for q in questions if q["difficulty"] == "Medium")
    if needed <= 0:
        return additional

    for j in range(needed):
        # Generate "find the whole given part-to-part and one value" questions
        ra = random.randint(2, 6)
        rb = random.randint(2, 6)
        while ra == rb:
            rb = random.randint(2, 6)
        g = gcd(ra, rb)
        ra, rb = ra // g, rb // g

        mult = random.randint(4, 15)
        actual_a = ra * mult
        total = (ra + rb) * mult
        correct = str(total)

        dist = set()
        dist.add(str(actual_a + rb))
        dist.add(str(rb * mult))
        dist.add(str(total + mult))
        dist.add(str(total - mult))
        dist.discard(correct)
        distractors = list(dist)[:3]
        while len(distractors) < 3:
            distractors.append(str(total + random.randint(1, 10)))

        names = [("apples", "oranges", "fruits"), ("boys", "girls", "students"),
                 ("cats", "dogs", "pets"), ("passed", "failed", "test takers"),
                 ("red", "blue", "marbles")]
        ctx = names[j % len(names)]
        a_name, b_name, total_name = ctx

        q_text = f"The ratio of {a_name} to {b_name} is {ra}:{rb}. If there are {actual_a} {a_name}, how many total {total_name} are there?"
        expl = f"{ra} parts = {actual_a}, so 1 part = {mult}. Total parts = {ra}+{rb} = {ra + rb}. Total = {ra + rb} × {mult} = {total}."
        additional.append(make_q("Medium", q_text, [correct] + distractors[:3], correct, expl,
                                 ["equivalent ratios", "total", "multi-step"]))
    return additional


def pad_hard(target=200):
    """Generate additional hard questions to reach target."""
    additional = []
    needed = target - sum(1 for q in questions if q["difficulty"] == "Hard")
    if needed <= 0:
        return additional

    for j in range(needed):
        # Combined ratio problems
        # "Ratio of A:B is 2:3 and B:C is 4:5. Find A:C"
        ab_a = random.randint(1, 5)
        ab_b = random.randint(1, 5)
        while ab_a == ab_b:
            ab_b = random.randint(1, 5)
        g1 = gcd(ab_a, ab_b)
        ab_a, ab_b = ab_a // g1, ab_b // g1

        bc_b = random.randint(1, 5)
        bc_c = random.randint(1, 5)
        while bc_b == bc_c:
            bc_c = random.randint(1, 5)
        g2 = gcd(bc_b, bc_c)
        bc_b, bc_c = bc_b // g2, bc_c // g2

        # Make B common: A:B = ab_a:ab_b, B:C = bc_b:bc_c
        # Common B = LCM(ab_b, bc_b)
        from math import lcm
        common_b = lcm(ab_b, bc_b)
        new_a = ab_a * (common_b // ab_b)
        new_c = bc_c * (common_b // bc_b)

        ga = gcd(new_a, new_c)
        final_a = new_a // ga
        final_c = new_c // ga
        correct = ratio_str(final_a, final_c)

        dist = set()
        dist.add(ratio_str(final_c, final_a))
        dist.add(ratio_str(ab_a, bc_c))
        dist.add(ratio_str(ab_a * bc_b, ab_b * bc_c))
        dist.add(ratio_str(final_a + 1, final_c))
        dist.discard(correct)
        distractors = list(dist)[:3]
        while len(distractors) < 3:
            distractors.append(ratio_str(final_a + random.randint(1, 3), final_c + random.randint(1, 3)))

        q_text = f"If A:B = {ab_a}:{ab_b} and B:C = {bc_b}:{bc_c}, what is the ratio A:C in simplest form?"
        expl = f"Make B common: LCM({ab_b},{bc_b})={common_b}. A={ab_a}×{common_b // ab_b}={new_a}, C={bc_c}×{common_b // bc_b}={new_c}. A:C={new_a}:{new_c}={correct}."
        additional.append(make_q("Hard", q_text, [correct] + distractors[:3], correct, expl,
                                 ["combined ratios", "LCM", "multi-step"]))
    return additional


questions.extend(pad_easy(200))
questions.extend(pad_medium(200))
questions.extend(pad_hard(200))

# Re-assign IDs sequentially
for idx, q in enumerate(questions, 1):
    q["id"] = idx

# Final count check
easy_final = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_final = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_final = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"Final - Easy: {easy_final}, Medium: {medium_final}, Hard: {hard_final}, Total: {len(questions)}")

# Write output
output_dir = os.path.join("data", "seed", "questions", "numerical-ability",
                          "ratio-proportion-and-average", "types-of-ratios")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "questions.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written to {output_path}")
