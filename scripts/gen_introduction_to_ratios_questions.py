"""
Generate 600 multiple-choice questions for Introduction to Ratios.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/numerical-ability/ratio-proportion-and-average/introduction-to-ratios/questions.json
"""

import json
import random
import math
import os
from pathlib import Path

random.seed(42)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def simplify(a, b):
    g = gcd(a, b)
    return a // g, b // g


def generate_distractors_simplified(correct_a, correct_b, count=3):
    """Generate plausible wrong answers for simplified ratio questions."""
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 100:
        attempts += 1
        strategy = random.choice(["swap", "off_by_one", "wrong_gcf", "random"])
        if strategy == "swap":
            d = (correct_b, correct_a)
        elif strategy == "off_by_one":
            da = correct_a + random.choice([-1, 1])
            db = correct_b + random.choice([-1, 1])
            if da < 1:
                da = correct_a + 1
            if db < 1:
                db = correct_b + 1
            d = (da, db)
        elif strategy == "wrong_gcf":
            factor = random.randint(2, 4)
            da = correct_a * factor
            db = correct_b * factor
            g2 = gcd(da, db)
            if g2 > 1:
                da2, db2 = da // (g2 // random.choice([1, 2])), db // (g2 // random.choice([1, 2]))
                if da2 > 0 and db2 > 0:
                    d = simplify(da2, db2) if random.random() > 0.5 else (da2, db2)
                else:
                    d = (correct_a + 2, correct_b + 1)
            else:
                d = (correct_a + 1, correct_b)
        else:
            d = (random.randint(1, max(correct_a + 3, 5)), random.randint(1, max(correct_b + 3, 5)))
        if d != (correct_a, correct_b) and d[0] > 0 and d[1] > 0:
            distractors.add(d)
    result = [f"{a}:{b}" for a, b in list(distractors)[:count]]
    # Ensure we have exactly count distractors
    while len(result) < count:
        result.append(f"{correct_a + len(result) + 1}:{correct_b + len(result)}")
    return result


def generate_number_distractor(correct, count=3):
    """Generate plausible wrong numeric answers."""
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 100:
        attempts += 1
        offset = random.choice([-3, -2, -1, 1, 2, 3, 4, 5, -4, -5])
        d = correct + offset
        if d > 0 and d != correct:
            distractors.add(d)
    result = list(distractors)[:count]
    while len(result) < count:
        result.append(correct + len(result) + 1)
    return [str(x) for x in result]


def shuffle_choices(correct, distractors):
    """Return shuffled choices list with correct answer included."""
    choices = [correct] + distractors[:3]
    random.shuffle(choices)
    return choices


questions = []
qid = 0

# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Category 1: Direct ratio writing (Easy, ~40 questions) ---
easy_contexts = [
    ("a class of {a} boys and {b} girls", "boys to girls", "boys", "girls"),
    ("a bag with {a} red balls and {b} blue balls", "red to blue balls", "red balls", "blue balls"),
    ("a garden with {a} roses and {b} sunflowers", "roses to sunflowers", "roses", "sunflowers"),
    ("{a} cats and {b} dogs in a shelter", "cats to dogs", "cats", "dogs"),
    ("{a} apples and {b} oranges in a basket", "apples to oranges", "apples", "oranges"),
    ("a parking lot with {a} cars and {b} motorcycles", "cars to motorcycles", "cars", "motorcycles"),
    ("{a} pencils and {b} pens on a desk", "pencils to pens", "pencils", "pens"),
    ("a farm with {a} chickens and {b} ducks", "chickens to ducks", "chickens", "ducks"),
]

for i in range(40):
    ctx = easy_contexts[i % len(easy_contexts)]
    a = random.randint(2, 15)
    b = random.randint(2, 15)
    while a == b:
        b = random.randint(2, 15)
    sa, sb = simplify(a, b)
    question_text = f"In {ctx[0].format(a=a, b=b)}, what is the ratio of {ctx[1]}?"
    correct = f"{sa}:{sb}"
    dists = generate_distractors_simplified(sa, sb)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"The ratio of {ctx[2]} to {ctx[3]} is {a}:{b}. "
                       f"GCF of {a} and {b} is {gcd(a, b)}. "
                       f"Dividing both terms: {a}÷{gcd(a, b)}={sa}, {b}÷{gcd(a, b)}={sb}. "
                       f"Simplified ratio: {sa}:{sb}.",
        "tags": ["ratios", "writing ratios", "simplifying ratios"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 2: Simple ratio simplification (Easy, ~40 questions) ---
for i in range(40):
    sa = random.randint(1, 9)
    sb = random.randint(1, 9)
    while gcd(sa, sb) != 1 or sa == sb:
        sa = random.randint(1, 9)
        sb = random.randint(1, 9)
    multiplier = random.randint(2, 6)
    a = sa * multiplier
    b = sb * multiplier
    question_text = f"What is the simplified form of the ratio {a}:{b}?"
    correct = f"{sa}:{sb}"
    dists = generate_distractors_simplified(sa, sb)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"The GCF of {a} and {b} is {multiplier}. "
                       f"Divide both terms: {a}÷{multiplier}={sa}, {b}÷{multiplier}={sb}. "
                       f"Simplified ratio: {sa}:{sb}.",
        "tags": ["ratios", "simplifying ratios", "GCF"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# --- Category 3: Ratio notation conversion (Easy, ~30 questions) ---
notations = [
    ("colon", "fraction", lambda a, b: f"{a}:{b}", lambda a, b: f"{a}/{b}"),
    ("colon", "word", lambda a, b: f"{a}:{b}", lambda a, b: f"{a} to {b}"),
    ("word", "colon", lambda a, b: f"{a} to {b}", lambda a, b: f"{a}:{b}"),
    ("fraction", "colon", lambda a, b: f"{a}/{b}", lambda a, b: f"{a}:{b}"),
]

for i in range(30):
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    while a == b:
        b = random.randint(1, 12)
    notation = notations[i % len(notations)]
    given = notation[2](a, b)
    correct = notation[3](a, b)
    # Generate distractors based on notation type
    if notation[1] == "fraction":
        dists = [f"{b}/{a}", f"{a+1}/{b}", f"{a}/{b+1}"]
    elif notation[1] == "colon":
        dists = [f"{b}:{a}", f"{a+1}:{b}", f"{a}:{b+1}"]
    else:
        dists = [f"{b} to {a}", f"{a+1} to {b}", f"{a} to {b+1}"]
    question_text = f"Express the ratio {given} in {notation[1]} notation."
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"The ratio {given} in {notation[0]} notation converts directly to "
                       f"{correct} in {notation[1]} notation. The order of terms stays the same.",
        "tags": ["ratios", "ratio notation", "conversion"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 4: Identifying equivalent ratios (Easy, ~30 questions) ---
for i in range(30):
    sa = random.randint(1, 8)
    sb = random.randint(1, 8)
    while gcd(sa, sb) != 1 or sa == sb:
        sa = random.randint(1, 8)
        sb = random.randint(1, 8)
    mult = random.randint(2, 6)
    equiv_a = sa * mult
    equiv_b = sb * mult
    question_text = f"Which of the following is equivalent to {sa}:{sb}?"
    correct = f"{equiv_a}:{equiv_b}"
    # Generate non-equivalent distractors
    dists = []
    dists.append(f"{equiv_a}:{equiv_b + random.randint(1, 3)}")
    dists.append(f"{equiv_a + random.randint(1, 3)}:{equiv_b}")
    dists.append(f"{sb * mult}:{sa * mult}")  # reversed
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"Multiply both terms of {sa}:{sb} by {mult}: "
                       f"{sa}×{mult}={equiv_a}, {sb}×{mult}={equiv_b}. "
                       f"So {equiv_a}:{equiv_b} is equivalent to {sa}:{sb}.",
        "tags": ["ratios", "equivalent ratios"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# --- Category 5: GCF identification (Easy, ~30 questions) ---
for i in range(30):
    g = random.randint(2, 12)
    m1 = random.randint(2, 8)
    m2 = random.randint(2, 8)
    while m1 == m2 or gcd(m1, m2) != 1:
        m2 = random.randint(2, 8)
    a = g * m1
    b = g * m2
    question_text = f"What is the greatest common factor (GCF) of {a} and {b}?"
    correct = str(g)
    dists = generate_number_distractor(g)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"{a} = {g}×{m1} and {b} = {g}×{m2}. "
                       f"Since {m1} and {m2} share no common factor, the GCF is {g}.",
        "tags": ["ratios", "GCF", "common factors"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# --- Category 6: Part-to-part vs part-to-whole (Easy, ~30 questions) ---
for i in range(30):
    part_a = random.randint(3, 20)
    part_b = random.randint(3, 20)
    while part_a == part_b:
        part_b = random.randint(3, 20)
    total = part_a + part_b
    items = [
        ("boys", "girls", "students"),
        ("red marbles", "blue marbles", "marbles"),
        ("passed", "failed", "examinees"),
        ("male employees", "female employees", "employees"),
        ("fiction books", "non-fiction books", "books"),
    ]
    item = items[i % len(items)]
    if i % 2 == 0:
        # Part-to-whole
        sa, sb = simplify(part_a, total)
        question_text = (f"A group has {part_a} {item[0]} and {part_b} {item[1]}. "
                        f"What is the ratio of {item[0]} to all {item[2]}?")
        correct = f"{sa}:{sb}"
        explanation = (f"Total {item[2]} = {part_a} + {part_b} = {total}. "
                      f"Ratio of {item[0]} to total = {part_a}:{total}. "
                      f"GCF = {gcd(part_a, total)}. Simplified: {sa}:{sb}.")
        tags = ["ratios", "part-to-whole"]
    else:
        # Part-to-part
        sa, sb = simplify(part_a, part_b)
        question_text = (f"A group has {part_a} {item[0]} and {part_b} {item[1]}. "
                        f"What is the ratio of {item[0]} to {item[1]}?")
        correct = f"{sa}:{sb}"
        explanation = (f"Ratio of {item[0]} to {item[1]} = {part_a}:{part_b}. "
                      f"GCF = {gcd(part_a, part_b)}. Simplified: {sa}:{sb}.")
        tags = ["ratios", "part-to-part"]
    dists = generate_distractors_simplified(sa, sb)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 7: Conceptual / definition questions (Easy, ~30 questions) ---
conceptual_easy = [
    {
        "question": "A ratio is a comparison of two quantities using which operation?",
        "choices": ["Addition", "Division", "Subtraction", "Multiplication"],
        "answer": "Division",
        "explanation": "A ratio compares two quantities by division. The ratio a:b means a divided by b.",
        "tags": ["ratios", "definition"]
    },
    {
        "question": "In the ratio 5:8, which number is the first term (antecedent)?",
        "choices": ["5", "8", "13", "3"],
        "answer": "5",
        "explanation": "In a ratio a:b, the first number (a) is called the antecedent. Here, 5 is the antecedent.",
        "tags": ["ratios", "terminology"]
    },
    {
        "question": "In the ratio 5:8, which number is the second term (consequent)?",
        "choices": ["5", "8", "13", "3"],
        "answer": "8",
        "explanation": "In a ratio a:b, the second number (b) is called the consequent. Here, 8 is the consequent.",
        "tags": ["ratios", "terminology"]
    },
    {
        "question": "What does the ratio 1:1 mean?",
        "choices": ["The first quantity is larger", "The quantities are equal",
                    "The second quantity is larger", "The quantities add up to 1"],
        "answer": "The quantities are equal",
        "explanation": "A ratio of 1:1 means both quantities are equal in size.",
        "tags": ["ratios", "interpretation"]
    },
    {
        "question": "Which notation correctly represents 'three is to seven'?",
        "choices": ["3:7", "7:3", "3+7", "3-7"],
        "answer": "3:7",
        "explanation": "'Three is to seven' means the first quantity is 3 and the second is 7, written as 3:7.",
        "tags": ["ratios", "ratio notation"]
    },
    {
        "question": "If a recipe uses 2 cups of sugar for every 5 cups of flour, what is the sugar-to-flour ratio?",
        "choices": ["2:5", "5:2", "2:7", "5:7"],
        "answer": "2:5",
        "explanation": "Sugar to flour = 2:5. The order matches the question: sugar first, flour second.",
        "tags": ["ratios", "writing ratios", "real-life"]
    },
    {
        "question": "Does the order of terms in a ratio matter?",
        "choices": ["Yes, order changes the meaning", "No, order does not matter",
                    "Only for fractions", "Only for large numbers"],
        "answer": "Yes, order changes the meaning",
        "explanation": "3:5 and 5:3 represent different relationships. The first term corresponds to the first quantity named.",
        "tags": ["ratios", "order"]
    },
    {
        "question": "A ratio of 4:1 means the first quantity is how many times the second?",
        "choices": ["4 times", "1 time", "5 times", "3 times"],
        "answer": "4 times",
        "explanation": "4:1 means for every 1 unit of the second quantity, there are 4 units of the first. The first is 4 times the second.",
        "tags": ["ratios", "interpretation"]
    },
    {
        "question": "Which of the following is NOT a valid way to write a ratio?",
        "choices": ["3:4", "3/4", "3 to 4", "3 × 4"],
        "answer": "3 × 4",
        "explanation": "Ratios can be written as 3:4 (colon), 3/4 (fraction), or '3 to 4' (word). Multiplication (3 × 4) is not ratio notation.",
        "tags": ["ratios", "ratio notation"]
    },
    {
        "question": "What type of ratio compares a subgroup to the entire group?",
        "choices": ["Part-to-whole", "Part-to-part", "Whole-to-part", "Rate"],
        "answer": "Part-to-whole",
        "explanation": "A part-to-whole ratio compares one subgroup to the total of all subgroups combined.",
        "tags": ["ratios", "part-to-whole", "definition"]
    },
    {
        "question": "What type of ratio compares one subgroup to another subgroup?",
        "choices": ["Part-to-part", "Part-to-whole", "Whole-to-whole", "Rate"],
        "answer": "Part-to-part",
        "explanation": "A part-to-part ratio compares two different subgroups within the same whole.",
        "tags": ["ratios", "part-to-part", "definition"]
    },
    {
        "question": "Two ratios are equivalent if they simplify to the same ratio. True or false?",
        "choices": ["True", "False", "Only for unit ratios", "Only for even numbers"],
        "answer": "True",
        "explanation": "Equivalent ratios have the same simplified form. For example, 4:6 and 6:9 both simplify to 2:3.",
        "tags": ["ratios", "equivalent ratios"]
    },
    {
        "question": "To simplify a ratio, you divide both terms by their:",
        "choices": ["Greatest Common Factor", "Least Common Multiple",
                    "Sum", "Difference"],
        "answer": "Greatest Common Factor",
        "explanation": "Dividing both terms by the GCF reduces the ratio to its simplest form.",
        "tags": ["ratios", "simplifying ratios", "GCF"]
    },
    {
        "question": "If a class has 10 boys and 15 girls, the ratio 10:15 simplifies to:",
        "choices": ["2:3", "3:2", "1:5", "5:3"],
        "answer": "2:3",
        "explanation": "GCF of 10 and 15 is 5. 10÷5=2, 15÷5=3. Simplified ratio: 2:3.",
        "tags": ["ratios", "simplifying ratios"]
    },
    {
        "question": "What is the ratio of 6 to 6 in simplest form?",
        "choices": ["1:1", "6:6", "0:0", "6:1"],
        "answer": "1:1",
        "explanation": "GCF of 6 and 6 is 6. 6÷6=1, 6÷6=1. Simplified: 1:1, meaning equal quantities.",
        "tags": ["ratios", "simplifying ratios"]
    },
]

for i, q in enumerate(conceptual_easy):
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": q["question"],
        "choices": q["choices"],
        "answer": q["answer"],
        "explanation": q["explanation"],
        "tags": q["tags"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# Fill remaining easy questions to reach 200
remaining_easy = 200 - len([q for q in questions if q["difficulty"] == "Easy"])


# Fill remaining easy with mixed simple ratio problems
easy_scenarios = [
    "In a library, there are {a} fiction books and {b} non-fiction books. What is the ratio of fiction to non-fiction in simplest form?",
    "A store has {a} shirts and {b} pants. What is the simplified ratio of shirts to pants?",
    "A team scored {a} goals in the first half and {b} goals in the second half. What is the ratio of first-half to second-half goals in simplest form?",
    "An office has {a} desktop computers and {b} laptops. What is the ratio of desktops to laptops in simplest form?",
    "A survey found {a} people prefer coffee and {b} prefer tea. What is the simplified ratio of coffee lovers to tea lovers?",
    "A box contains {a} white balls and {b} black balls. What is the ratio of white to black balls in simplest form?",
    "A school bus carries {a} elementary students and {b} high school students. What is the simplified ratio of elementary to high school students?",
    "A garden has {a} mango trees and {b} coconut trees. What is the ratio of mango to coconut trees in simplest form?",
]

for i in range(remaining_easy):
    scenario = easy_scenarios[i % len(easy_scenarios)]
    sa = random.randint(1, 7)
    sb = random.randint(1, 7)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(1, 7)
    mult = random.randint(2, 5)
    a = sa * mult
    b = sb * mult
    question_text = scenario.format(a=a, b=b)
    correct = f"{sa}:{sb}"
    dists = generate_distractors_simplified(sa, sb)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Easy",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"Ratio is {a}:{b}. GCF of {a} and {b} is {mult}. "
                       f"{a}÷{mult}={sa}, {b}÷{mult}={sb}. Simplified: {sa}:{sb}.",
        "tags": ["ratios", "simplifying ratios", "real-life"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Category 1: Ratio word problems with context (Medium, ~50 questions) ---
medium_word_problems = [
    ("A government office has {total} employees. The ratio of male to female employees is {sa}:{sb}. How many male employees are there?",
     "male employees", True),
    ("A school has students in the ratio of {sa}:{sb} (boys to girls). If there are {b_val} girls, how many boys are there?",
     "boys", False),
    ("A recipe requires flour and sugar in the ratio {sa}:{sb}. If {a_val} grams of flour are used, how many grams of sugar are needed?",
     "grams of sugar", False),
    ("A department allocates its budget for supplies and training in the ratio {sa}:{sb}. If the total budget is ₱{total}, how much goes to supplies?",
     "supplies budget", True),
    ("In a parking lot, the ratio of cars to motorcycles is {sa}:{sb}. If there are {a_val} cars, how many motorcycles are there?",
     "motorcycles", False),
]

for i in range(50):
    sa = random.randint(2, 7)
    sb = random.randint(2, 7)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 7)
    mult = random.randint(3, 15)
    a_val = sa * mult
    b_val = sb * mult
    total = a_val + b_val
    prob = medium_word_problems[i % len(medium_word_problems)]

    if prob[2]:  # total-based problem
        question_text = prob[0].format(total=total, sa=sa, sb=sb)
        correct_val = a_val
        explanation = (f"Total parts = {sa}+{sb} = {sa+sb}. "
                      f"Each part = {total}÷{sa+sb} = {mult}. "
                      f"First quantity = {sa}×{mult} = {a_val}.")
    else:  # one-value-given problem
        if "girls" in prob[0] or "sugar" in prob[0] or "motorcycles" in prob[0]:
            question_text = prob[0].format(sa=sa, sb=sb, a_val=a_val, b_val=b_val)
            if "boys" in prob[1]:
                correct_val = a_val
                explanation = (f"Ratio is {sa}:{sb}. Girls = {b_val}. "
                              f"Scale factor = {b_val}÷{sb} = {mult}. "
                              f"Boys = {sa}×{mult} = {a_val}.")
            elif "sugar" in prob[1]:
                correct_val = b_val
                explanation = (f"Ratio flour:sugar = {sa}:{sb}. Flour = {a_val}. "
                              f"Scale factor = {a_val}÷{sa} = {mult}. "
                              f"Sugar = {sb}×{mult} = {b_val}.")
            else:
                correct_val = b_val
                explanation = (f"Ratio cars:motorcycles = {sa}:{sb}. Cars = {a_val}. "
                              f"Scale factor = {a_val}÷{sa} = {mult}. "
                              f"Motorcycles = {sb}×{mult} = {b_val}.")
        else:
            question_text = prob[0].format(sa=sa, sb=sb, a_val=a_val, b_val=b_val, total=total)
            correct_val = a_val
            explanation = f"Scale factor = {mult}. Answer = {sa}×{mult} = {a_val}."

    correct = str(correct_val)
    dists = generate_number_distractor(correct_val)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Medium",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "word problems", "scaling"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 2: Unit conversion ratio problems (Medium, ~30 questions) ---
unit_conversions = [
    ("What is the ratio of {a_val} minutes to {b_hours} hour(s) in simplest form?",
     "minutes", 60, "minutes"),
    ("What is the ratio of {a_val} centimeters to {b_meters} meter(s) in simplest form?",
     "centimeters", 100, "centimeters"),
    ("What is the ratio of {a_val} grams to {b_kg} kilogram(s) in simplest form?",
     "grams", 1000, "grams"),
    ("What is the ratio of {a_val} seconds to {b_min} minute(s) in simplest form?",
     "seconds", 60, "seconds"),
]

for i in range(30):
    conv = unit_conversions[i % len(unit_conversions)]
    b_units = random.randint(1, 3)
    b_base = b_units * conv[2]  # convert to smaller unit
    a_val = random.choice([15, 20, 25, 30, 40, 45, 50, 60, 75, 80, 90, 100, 120, 150, 200, 250, 300, 500])
    while a_val >= b_base:
        a_val = random.choice([15, 20, 25, 30, 40, 45, 50, 60, 75, 80, 90])
    sa, sb = simplify(a_val, b_base)
    question_text = conv[0].format(a_val=a_val, b_hours=b_units, b_meters=b_units, b_kg=b_units, b_min=b_units)
    correct = f"{sa}:{sb}"
    dists = generate_distractors_simplified(sa, sb)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Medium",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"Convert to same unit: {b_units} larger unit = {b_base} {conv[3]}. "
                       f"Ratio = {a_val}:{b_base}. GCF = {gcd(a_val, b_base)}. "
                       f"Simplified: {sa}:{sb}.",
        "tags": ["ratios", "unit conversion", "simplifying ratios"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# --- Category 3: Finding missing term in equivalent ratios (Medium, ~40 questions) ---
for i in range(40):
    sa = random.randint(2, 9)
    sb = random.randint(2, 9)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 9)
    mult = random.randint(3, 12)
    a_val = sa * mult
    b_val = sb * mult
    if i % 2 == 0:
        # Given first term, find second
        question_text = f"Find the missing term: {sa}:{sb} = {a_val}:?"
        correct = str(b_val)
        explanation = (f"{sa} was multiplied by {mult} to get {a_val}. "
                      f"Multiply {sb} by {mult}: {sb}×{mult} = {b_val}.")
    else:
        # Given second term, find first
        question_text = f"Find the missing term: {sa}:{sb} = ?:{b_val}"
        correct = str(a_val)
        explanation = (f"{sb} was multiplied by {mult} to get {b_val}. "
                      f"Multiply {sa} by {mult}: {sa}×{mult} = {a_val}.")
    dists = generate_number_distractor(int(correct))
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Medium",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "equivalent ratios", "missing term"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 4: Three-term ratio simplification (Medium, ~30 questions) ---
for i in range(30):
    sa = random.randint(1, 6)
    sb = random.randint(1, 6)
    sc = random.randint(1, 6)
    # Ensure at least two are different and coprime as a triple
    while sa == sb == sc:
        sc = random.randint(1, 6)
    g_all = gcd(gcd(sa, sb), sc)
    sa, sb, sc = sa // g_all, sb // g_all, sc // g_all
    mult = random.randint(2, 7)
    a = sa * mult
    b = sb * mult
    c = sc * mult
    contexts_3 = [
        f"Simplify the ratio {a}:{b}:{c}.",
        f"A mixture uses ingredients in the ratio {a}:{b}:{c}. What is the simplified form?",
        f"Three departments share a budget in the ratio {a}:{b}:{c}. Express in simplest form.",
    ]
    question_text = contexts_3[i % len(contexts_3)]
    correct = f"{sa}:{sb}:{sc}"
    # Distractors for 3-term
    dists = [
        f"{sa+1}:{sb}:{sc}",
        f"{sa}:{sb+1}:{sc+1}",
        f"{sb}:{sa}:{sc}",
    ]
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Medium",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"GCF of {a}, {b}, and {c} is {mult}. "
                       f"Divide all terms: {a}÷{mult}={sa}, {b}÷{mult}={sb}, {c}÷{mult}={sc}. "
                       f"Simplified: {sa}:{sb}:{sc}.",
        "tags": ["ratios", "three-term ratios", "simplifying ratios"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# --- Category 5: Cross-multiplication to check equivalence (Medium, ~25 questions) ---
for i in range(25):
    sa = random.randint(2, 9)
    sb = random.randint(2, 9)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 9)
    mult1 = random.randint(2, 6)
    a1 = sa * mult1
    b1 = sb * mult1
    if i % 2 == 0:
        # Equivalent pair
        mult2 = random.randint(2, 8)
        while mult2 == mult1:
            mult2 = random.randint(2, 8)
        a2 = sa * mult2
        b2 = sb * mult2
        correct = "Yes, they are equivalent"
        explanation = (f"{a1}:{b1} simplifies to {sa}:{sb}. "
                      f"{a2}:{b2} simplifies to {sa}:{sb}. Same simplified form → equivalent.")
    else:
        # Non-equivalent pair
        a2 = sa * random.randint(2, 5)
        b2 = sb * random.randint(2, 5) + random.randint(1, 3)
        while simplify(a2, b2) == (sa, sb):
            b2 += 1
        correct = "No, they are not equivalent"
        s2a, s2b = simplify(a2, b2)
        explanation = (f"{a1}:{b1} simplifies to {sa}:{sb}. "
                      f"{a2}:{b2} simplifies to {s2a}:{s2b}. Different simplified forms → not equivalent.")
    question_text = f"Are the ratios {a1}:{b1} and {a2}:{b2} equivalent?"
    dists = ["Yes, they are equivalent", "No, they are not equivalent",
             "Cannot be determined", "Only if simplified"]
    dists = [d for d in dists if d != correct][:3]
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Medium",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "equivalent ratios", "cross-multiplication"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 6: Workplace/government context ratio problems (Medium, ~25 questions) ---
workplace_medium = [
    "A government agency has {a} professional staff and {b} administrative staff. What is the ratio of professional to total staff in simplest form?",
    "In a municipal office, {a} employees work full-time and {b} work part-time. What is the simplified ratio of full-time to part-time workers?",
    "A department processed {a} applications this month and {b} last month. What is the ratio of this month to last month in simplest form?",
    "A public school has {a} classrooms for elementary and {b} for high school. What is the ratio of elementary to total classrooms in simplest form?",
    "An agency fleet has {a} sedans and {b} SUVs. What is the simplified ratio of sedans to all vehicles?",
]

for i in range(25):
    sa = random.randint(2, 8)
    sb = random.randint(2, 8)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 8)
    mult = random.randint(3, 10)
    a = sa * mult
    b = sb * mult
    total = a + b
    scenario = workplace_medium[i % len(workplace_medium)]
    question_text = scenario.format(a=a, b=b)
    if "total" in scenario:
        # Part-to-whole
        ra, rb = simplify(a, total)
        correct = f"{ra}:{rb}"
        explanation = (f"Total = {a}+{b} = {total}. Ratio = {a}:{total}. "
                      f"GCF = {gcd(a, total)}. Simplified: {ra}:{rb}.")
    else:
        # Part-to-part
        correct = f"{sa}:{sb}"
        explanation = (f"Ratio = {a}:{b}. GCF = {gcd(a, b)}. Simplified: {sa}:{sb}.")
    ra_c, rb_c = [int(x) for x in correct.split(":")]
    dists = generate_distractors_simplified(ra_c, rb_c)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Medium",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "workplace", "government", "simplifying ratios"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# Fill remaining medium to reach 200
remaining_medium = 200 - len([q for q in questions if q["difficulty"] == "Medium"])

medium_fill_scenarios = [
    "The ratio of winners to losers in a contest is {sa}:{sb}. If there are {total} participants, how many winners are there?",
    "A bus carries passengers in the ratio of {sa} adults to {sb} children. If there are {b_val} children, how many adults are on the bus?",
    "A farmer plants rice and corn in the ratio {sa}:{sb}. If the total area is {total} hectares, how many hectares are planted with rice?",
    "An office supply order has pens and notebooks in the ratio {sa}:{sb}. If {a_val} pens were ordered, how many notebooks were ordered?",
    "A charity distributes food packs to families in two barangays in the ratio {sa}:{sb}. If {total} packs are distributed, how many go to the first barangay?",
]

for i in range(remaining_medium):
    sa = random.randint(2, 7)
    sb = random.randint(2, 7)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 7)
    mult = random.randint(4, 15)
    a_val = sa * mult
    b_val = sb * mult
    total = a_val + b_val
    scenario = medium_fill_scenarios[i % len(medium_fill_scenarios)]
    question_text = scenario.format(sa=sa, sb=sb, total=total, a_val=a_val, b_val=b_val)
    # Most ask for first quantity
    correct_val = a_val
    explanation = (f"Total parts = {sa}+{sb} = {sa+sb}. "
                  f"Each part = {total}÷{sa+sb} = {mult}. "
                  f"First quantity = {sa}×{mult} = {a_val}.")
    correct = str(correct_val)
    dists = generate_number_distractor(correct_val)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Medium",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "word problems", "scaling", "real-life"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Category 1: Multi-step ratio word problems (Hard, ~50 questions) ---
for i in range(50):
    sa = random.randint(2, 7)
    sb = random.randint(2, 7)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 7)
    mult = random.randint(5, 20)
    a_val = sa * mult
    b_val = sb * mult
    total = a_val + b_val
    diff = abs(a_val - b_val)

    problem_type = i % 5
    if problem_type == 0:
        # Given difference, find total
        question_text = (f"The ratio of two numbers is {sa}:{sb}. "
                        f"If the difference between them is {diff}, what is their sum?")
        correct_val = total
        explanation = (f"Difference in parts = |{sa}-{sb}| = {abs(sa-sb)}. "
                      f"Each part = {diff}÷{abs(sa-sb)} = {mult}. "
                      f"Sum = ({sa}+{sb})×{mult} = {sa+sb}×{mult} = {total}.")
    elif problem_type == 1:
        # Given total, find difference
        question_text = (f"Two quantities are in the ratio {sa}:{sb}. "
                        f"If their sum is {total}, what is the difference between them?")
        correct_val = diff
        explanation = (f"Total parts = {sa}+{sb} = {sa+sb}. "
                      f"Each part = {total}÷{sa+sb} = {mult}. "
                      f"Difference = |{sa}-{sb}|×{mult} = {abs(sa-sb)}×{mult} = {diff}.")
    elif problem_type == 2:
        # Given one value, find the other
        question_text = (f"The ratio of savings to expenses is {sa}:{sb}. "
                        f"If savings amount to ₱{a_val}, how much are the expenses?")
        correct_val = b_val
        explanation = (f"Scale factor = {a_val}÷{sa} = {mult}. "
                      f"Expenses = {sb}×{mult} = {b_val}.")
    elif problem_type == 3:
        # Three-part ratio, find one value
        sc = random.randint(1, 5)
        c_val = sc * mult
        total3 = a_val + b_val + c_val
        question_text = (f"A budget is divided among three departments in the ratio {sa}:{sb}:{sc}. "
                        f"If the total budget is ₱{total3}, how much does the first department receive?")
        correct_val = a_val
        explanation = (f"Total parts = {sa}+{sb}+{sc} = {sa+sb+sc}. "
                      f"Each part = {total3}÷{sa+sb+sc} = {mult}. "
                      f"First department = {sa}×{mult} = {a_val}.")
    else:
        # Ratio change problem
        increase = random.randint(2, 8)
        new_a = a_val + increase
        new_sa, new_sb = simplify(new_a, b_val)
        question_text = (f"The ratio of boys to girls is {sa}:{sb} with {a_val} boys and {b_val} girls. "
                        f"If {increase} more boys join, what is the new ratio of boys to girls in simplest form?")
        correct_val = None
        correct = f"{new_sa}:{new_sb}"
        explanation = (f"New boys = {a_val}+{increase} = {new_a}. Girls stay at {b_val}. "
                      f"New ratio = {new_a}:{b_val}. GCF = {gcd(new_a, b_val)}. "
                      f"Simplified: {new_sa}:{new_sb}.")

    if correct_val is not None:
        correct = str(correct_val)
        dists = generate_number_distractor(correct_val)
    else:
        dists = generate_distractors_simplified(new_sa, new_sb)

    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Hard",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "multi-step", "word problems"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 2: Complex simplification with larger numbers (Hard, ~35 questions) ---
for i in range(35):
    # Use larger GCFs and numbers
    sa = random.randint(2, 11)
    sb = random.randint(2, 11)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 11)
    mult = random.randint(7, 24)
    a = sa * mult
    b = sb * mult
    question_text = f"Simplify the ratio {a}:{b} to its lowest terms."
    correct = f"{sa}:{sb}"
    dists = generate_distractors_simplified(sa, sb)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Hard",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": f"GCF of {a} and {b} is {mult}. "
                       f"{a}÷{mult}={sa}, {b}÷{mult}={sb}. "
                       f"Simplified: {sa}:{sb}.",
        "tags": ["ratios", "simplifying ratios", "large numbers", "GCF"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# --- Category 3: Ratio comparison problems (Hard, ~30 questions) ---
for i in range(30):
    # Generate two ratios and ask which is larger
    sa1 = random.randint(1, 7)
    sb1 = random.randint(2, 9)
    while gcd(sa1, sb1) != 1:
        sb1 = random.randint(2, 9)
    sa2 = random.randint(1, 7)
    sb2 = random.randint(2, 9)
    while gcd(sa2, sb2) != 1 or (sa1/sb1 == sa2/sb2):
        sa2 = random.randint(1, 7)
        sb2 = random.randint(2, 9)

    val1 = sa1 / sb1
    val2 = sa2 / sb2

    if val1 > val2:
        correct = f"{sa1}:{sb1}"
        explanation = (f"Compare by cross-multiplication: {sa1}×{sb2} = {sa1*sb2} vs {sa2}×{sb1} = {sa2*sb1}. "
                      f"Since {sa1*sb2} > {sa2*sb1}, the ratio {sa1}:{sb1} is greater.")
    else:
        correct = f"{sa2}:{sb2}"
        explanation = (f"Compare by cross-multiplication: {sa1}×{sb2} = {sa1*sb2} vs {sa2}×{sb1} = {sa2*sb1}. "
                      f"Since {sa2*sb1} > {sa1*sb2}, the ratio {sa2}:{sb2} is greater.")

    question_text = f"Which ratio is greater: {sa1}:{sb1} or {sa2}:{sb2}?"
    other = f"{sa1}:{sb1}" if correct == f"{sa2}:{sb2}" else f"{sa2}:{sb2}"
    dists = [other, "They are equal", f"{sa1+sa2}:{sb1+sb2}"]
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Hard",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "comparing ratios", "cross-multiplication"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 4: Combined ratio problems (Hard, ~35 questions) ---
for i in range(35):
    # Two groups share a common term
    sa = random.randint(2, 6)
    sb = random.randint(2, 6)
    sc = random.randint(2, 6)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 6)
    while gcd(sb, sc) != 1 or sb == sc:
        sc = random.randint(2, 6)

    mult = random.randint(3, 10)
    a_val = sa * mult
    b_val = sb * mult
    c_val = sc * mult
    total = a_val + b_val + c_val

    problem_type = i % 5
    if problem_type == 0:
        question_text = (f"Three friends share money in the ratio {sa}:{sb}:{sc}. "
                        f"If the total amount is ₱{total}, how much does the person with the largest share receive?")
        largest = max(sa, sb, sc) * mult
        correct_val = largest
        explanation = (f"Total parts = {sa}+{sb}+{sc} = {sa+sb+sc}. "
                      f"Each part = ₱{total}÷{sa+sb+sc} = ₱{mult}. "
                      f"Largest share ({max(sa,sb,sc)} parts) = {max(sa,sb,sc)}×{mult} = ₱{largest}.")
    elif problem_type == 1:
        question_text = (f"The ratio of A:B is {sa}:{sb} and B:C is {sb}:{sc}. "
                        f"What is the ratio A:B:C?")
        correct = f"{sa}:{sb}:{sc}"
        correct_val = None
        explanation = (f"Since B is common in both ratios and already equal ({sb}), "
                      f"we can combine directly: A:B:C = {sa}:{sb}:{sc}.")
    elif problem_type == 2:
        diff_largest_smallest = (max(sa, sb, sc) - min(sa, sb, sc)) * mult
        question_text = (f"Prizes are distributed in the ratio {sa}:{sb}:{sc}. "
                        f"If the total prize pool is ₱{total}, what is the difference between the largest and smallest prizes?")
        correct_val = diff_largest_smallest
        explanation = (f"Each part = ₱{total}÷{sa+sb+sc} = ₱{mult}. "
                      f"Largest = {max(sa,sb,sc)}×{mult} = {max(sa,sb,sc)*mult}. "
                      f"Smallest = {min(sa,sb,sc)}×{mult} = {min(sa,sb,sc)*mult}. "
                      f"Difference = {diff_largest_smallest}.")
    elif problem_type == 3:
        question_text = (f"A mixture contains ingredients A, B, and C in the ratio {sa}:{sb}:{sc}. "
                        f"If the mixture weighs {total} grams, how many grams of ingredient B are there?")
        correct_val = b_val
        explanation = (f"Total parts = {sa+sb+sc}. Each part = {total}÷{sa+sb+sc} = {mult}g. "
                      f"Ingredient B = {sb}×{mult} = {b_val}g.")
    else:
        # What fraction of total is the middle value
        mid = sorted([sa, sb, sc])[1]
        mid_val = mid * mult
        frac_a, frac_b = simplify(mid, sa + sb + sc)
        question_text = (f"Items are distributed in the ratio {sa}:{sb}:{sc}. "
                        f"What fraction of the total does the middle share represent?")
        correct = f"{frac_a}/{frac_b}"
        correct_val = None
        explanation = (f"Middle value = {mid}. Total parts = {sa+sb+sc}. "
                      f"Fraction = {mid}/{sa+sb+sc} = {frac_a}/{frac_b}.")

    if correct_val is not None:
        correct = str(correct_val)
        dists = generate_number_distractor(correct_val)
    else:
        if ":" in correct:
            parts = correct.split(":")
            dists = [
                f"{parts[1]}:{parts[0]}:{parts[2]}" if len(parts) == 3 else f"{parts[1]}:{parts[0]}",
                f"{int(parts[0])+1}:{parts[1]}:{parts[2]}" if len(parts) == 3 else f"{int(parts[0])+1}:{parts[1]}",
                f"{parts[0]}:{int(parts[1])+1}:{parts[2]}" if len(parts) == 3 else f"{parts[0]}:{int(parts[1])+1}",
            ]
        else:
            # fraction answer
            fa, fb = correct.split("/")
            dists = [f"{int(fa)+1}/{fb}", f"{fa}/{int(fb)+1}", f"{int(fa)}/{int(fb)-1}" if int(fb) > 2 else f"{int(fa)+2}/{fb}"]

    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Hard",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "three-term ratios", "multi-step"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Category 5: Ratio with increase/decrease (Hard, ~25 questions) ---
for i in range(25):
    sa = random.randint(3, 8)
    sb = random.randint(3, 8)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(3, 8)
    mult = random.randint(4, 12)
    a_val = sa * mult
    b_val = sb * mult

    if i % 3 == 0:
        # Increase first term
        increase = random.randint(2, 15)
        new_a = a_val + increase
        new_sa, new_sb = simplify(new_a, b_val)
        question_text = (f"The ratio of apples to oranges is {sa}:{sb}, with {a_val} apples and {b_val} oranges. "
                        f"If {increase} more apples are added, what is the new simplified ratio?")
        correct = f"{new_sa}:{new_sb}"
        explanation = (f"New apples = {a_val}+{increase} = {new_a}. Oranges = {b_val}. "
                      f"New ratio = {new_a}:{b_val}. GCF = {gcd(new_a, b_val)}. "
                      f"Simplified: {new_sa}:{new_sb}.")
    elif i % 3 == 1:
        # Decrease second term
        decrease = random.randint(1, b_val // 2)
        new_b = b_val - decrease
        new_sa, new_sb = simplify(a_val, new_b)
        question_text = (f"A store has products A and B in the ratio {sa}:{sb} ({a_val} and {b_val} items). "
                        f"If {decrease} items of B are sold, what is the new ratio of A to B in simplest form?")
        correct = f"{new_sa}:{new_sb}"
        explanation = (f"New B = {b_val}-{decrease} = {new_b}. A stays at {a_val}. "
                      f"New ratio = {a_val}:{new_b}. GCF = {gcd(a_val, new_b)}. "
                      f"Simplified: {new_sa}:{new_sb}.")
    else:
        # Both increase
        inc_a = random.randint(2, 10)
        inc_b = random.randint(2, 10)
        new_a = a_val + inc_a
        new_b = b_val + inc_b
        new_sa, new_sb = simplify(new_a, new_b)
        question_text = (f"Originally there are {a_val} men and {b_val} women (ratio {sa}:{sb}). "
                        f"If {inc_a} men and {inc_b} women join, what is the new ratio in simplest form?")
        correct = f"{new_sa}:{new_sb}"
        explanation = (f"New men = {a_val}+{inc_a} = {new_a}. New women = {b_val}+{inc_b} = {new_b}. "
                      f"New ratio = {new_a}:{new_b}. GCF = {gcd(new_a, new_b)}. "
                      f"Simplified: {new_sa}:{new_sb}.")

    dists = generate_distractors_simplified(new_sa, new_sb)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Hard",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "ratio change", "increase decrease"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# --- Category 6: Complex government/workplace scenarios (Hard, ~25 questions) ---
hard_gov_scenarios = [
    ("A municipality allocates its ₱{total} budget to education, health, and infrastructure in the ratio {sa}:{sb}:{sc}. "
     "How much more does education receive than health?"),
    ("In a government exam, the ratio of passers to failers is {sa}:{sb}. "
     "If {diff} more people passed than failed, how many took the exam?"),
    ("A department has employees in three divisions in the ratio {sa}:{sb}:{sc}. "
     "If the smallest division has {min_val} employees, how many employees are in the largest division?"),
    ("The ratio of male to female voters in a barangay is {sa}:{sb}. "
     "If there are {total} registered voters, how many more female voters are there than male voters?"),
    ("A school's student-to-teacher ratio is {sa}:{sb_teacher}. "
     "If there are {teachers} teachers, how many students are enrolled?"),
]

for i in range(25):
    sa = random.randint(3, 8)
    sb = random.randint(2, 7)
    sc = random.randint(1, 5)
    while gcd(gcd(sa, sb), sc) != 1:
        sc = random.randint(1, 5)
    while sa == sb or sb == sc or sa == sc:
        sc = random.randint(1, 5)
    mult = random.randint(5, 15)

    scenario_idx = i % 5
    if scenario_idx == 0:
        a_val = sa * mult
        b_val = sb * mult
        c_val = sc * mult
        total = a_val + b_val + c_val
        diff_ab = a_val - b_val
        question_text = hard_gov_scenarios[0].format(total=total, sa=sa, sb=sb, sc=sc)
        correct_val = abs(diff_ab)
        explanation = (f"Total parts = {sa+sb+sc}. Each part = ₱{total}÷{sa+sb+sc} = ₱{mult}. "
                      f"Education = {sa}×{mult} = ₱{a_val}. Health = {sb}×{mult} = ₱{b_val}. "
                      f"Difference = ₱{abs(diff_ab)}.")
    elif scenario_idx == 1:
        diff = abs(sa - sb) * mult
        total = (sa + sb) * mult
        question_text = hard_gov_scenarios[1].format(sa=sa, sb=sb, diff=diff)
        correct_val = total
        explanation = (f"Difference in parts = |{sa}-{sb}| = {abs(sa-sb)}. "
                      f"Each part = {diff}÷{abs(sa-sb)} = {mult}. "
                      f"Total examinees = ({sa}+{sb})×{mult} = {total}.")
    elif scenario_idx == 2:
        min_ratio = min(sa, sb, sc)
        max_ratio = max(sa, sb, sc)
        min_val = min_ratio * mult
        max_val = max_ratio * mult
        question_text = hard_gov_scenarios[2].format(sa=sa, sb=sb, sc=sc, min_val=min_val)
        correct_val = max_val
        explanation = (f"Smallest division has {min_ratio} parts = {min_val} employees. "
                      f"Each part = {min_val}÷{min_ratio} = {mult}. "
                      f"Largest division ({max_ratio} parts) = {max_ratio}×{mult} = {max_val}.")
    elif scenario_idx == 3:
        # Ensure sb > sa for "more female"
        if sa >= sb:
            sa, sb = sb, sa
        total = (sa + sb) * mult
        diff = (sb - sa) * mult
        question_text = hard_gov_scenarios[3].format(sa=sa, sb=sb, total=total)
        correct_val = diff
        explanation = (f"Total parts = {sa+sb}. Each part = {total}÷{sa+sb} = {mult}. "
                      f"Males = {sa}×{mult} = {sa*mult}. Females = {sb}×{mult} = {sb*mult}. "
                      f"Difference = {diff}.")
    else:
        sb_teacher = 1
        teachers = random.randint(8, 30)
        students = sa * teachers
        question_text = hard_gov_scenarios[4].format(sa=sa, sb_teacher=sb_teacher, teachers=teachers)
        correct_val = students
        explanation = (f"Student:teacher = {sa}:1. With {teachers} teachers, "
                      f"students = {sa}×{teachers} = {students}.")

    correct = str(correct_val)
    dists = generate_number_distractor(correct_val)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Hard",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "government", "multi-step", "word problems"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# --- Fill remaining hard questions ---
remaining_hard = 200 - len([q for q in questions if q["difficulty"] == "Hard"])

hard_fill_scenarios = [
    ("The ages of two siblings are in the ratio {sa}:{sb}. "
     "In {years} years, the older sibling will be {older_future} years old. "
     "What is the current age of the younger sibling?"),
    ("A tank is filled by two pipes in the ratio {sa}:{sb}. "
     "If the total capacity is {total} liters, how many liters does the larger pipe contribute?"),
    ("Workers A and B complete tasks in the ratio {sa}:{sb}. "
     "If together they completed {total} tasks, how many more tasks did the faster worker complete?"),
    ("The ratio of investment between two partners is {sa}:{sb}. "
     "If the total profit of ₱{total} is divided in the same ratio, how much does the partner with the smaller investment receive?"),
    ("A school has boys and girls in the ratio {sa}:{sb}. "
     "If 10% of the boys and 20% of the girls are honor students, and there are {total} students total, "
     "how many honor students are there?"),
]

for i in range(remaining_hard):
    sa = random.randint(3, 9)
    sb = random.randint(2, 8)
    while gcd(sa, sb) != 1 or sa == sb:
        sb = random.randint(2, 8)
    mult = random.randint(3, 12)
    a_val = sa * mult
    b_val = sb * mult
    total = a_val + b_val

    scenario_idx = i % 5
    if scenario_idx == 0:
        # Age problem
        years = random.randint(2, 8)
        older = max(a_val, b_val)
        younger = min(a_val, b_val)
        older_future = older + years
        question_text = hard_fill_scenarios[0].format(
            sa=max(sa, sb), sb=min(sa, sb), years=years, older_future=older_future)
        correct_val = younger
        explanation = (f"Older sibling's current age = {older_future}-{years} = {older}. "
                      f"Ratio is {max(sa,sb)}:{min(sa,sb)}. Scale factor = {older}÷{max(sa,sb)} = {mult}. "
                      f"Younger sibling = {min(sa,sb)}×{mult} = {younger}.")
    elif scenario_idx == 1:
        larger = max(a_val, b_val)
        question_text = hard_fill_scenarios[1].format(sa=sa, sb=sb, total=total)
        correct_val = larger
        explanation = (f"Total parts = {sa+sb}. Each part = {total}÷{sa+sb} = {mult} liters. "
                      f"Larger pipe ({max(sa,sb)} parts) = {max(sa,sb)}×{mult} = {larger} liters.")
    elif scenario_idx == 2:
        diff = abs(a_val - b_val)
        question_text = hard_fill_scenarios[2].format(sa=sa, sb=sb, total=total)
        correct_val = diff
        explanation = (f"Total parts = {sa+sb}. Each part = {total}÷{sa+sb} = {mult}. "
                      f"Worker A = {sa}×{mult}={a_val}. Worker B = {sb}×{mult}={b_val}. "
                      f"Difference = {diff}.")
    elif scenario_idx == 3:
        smaller_val = min(a_val, b_val)
        question_text = hard_fill_scenarios[3].format(sa=sa, sb=sb, total=total)
        correct_val = smaller_val
        explanation = (f"Total parts = {sa+sb}. Each part = ₱{total}÷{sa+sb} = ₱{mult}. "
                      f"Smaller share ({min(sa,sb)} parts) = {min(sa,sb)}×{mult} = ₱{smaller_val}.")
    else:
        # Honor students problem - use clean numbers
        mult2 = 10  # ensure divisible by 10 for percentage
        a_val2 = sa * mult2
        b_val2 = sb * mult2
        total2 = a_val2 + b_val2
        honor_boys = a_val2 // 10  # 10%
        honor_girls = b_val2 // 5   # 20%
        honor_total = honor_boys + honor_girls
        question_text = hard_fill_scenarios[4].format(sa=sa, sb=sb, total=total2)
        correct_val = honor_total
        explanation = (f"Boys = {sa}×10 = {a_val2}. Girls = {sb}×10 = {b_val2}. "
                      f"Honor boys (10%) = {honor_boys}. Honor girls (20%) = {honor_girls}. "
                      f"Total honor students = {honor_boys}+{honor_girls} = {honor_total}.")

    correct = str(correct_val)
    dists = generate_number_distractor(correct_val)
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Introduction to Ratios",
        "difficulty": "Hard",
        "question": question_text,
        "choices": shuffle_choices(correct, dists),
        "answer": correct,
        "explanation": explanation,
        "tags": ["ratios", "complex problems", "multi-step", "real-life"],
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# ============================================================
# OUTPUT
# ============================================================

# Verify counts
easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
medium_count = len([q for q in questions if q["difficulty"] == "Medium"])
hard_count = len([q for q in questions if q["difficulty"] == "Hard"])

print(f"Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}, Total: {len(questions)}")

# Reassign IDs sequentially
for idx, q in enumerate(questions, 1):
    q["id"] = idx

# Write output
output_dir = Path("data/seed/questions/numerical-ability/ratio-proportion-and-average/introduction-to-ratios")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written {len(questions)} questions to {output_path}")
