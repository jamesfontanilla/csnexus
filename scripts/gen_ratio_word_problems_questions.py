"""
Generate 600 multiple-choice questions for Ratio Word Problems subtopic.
200 Easy / 200 Medium / 200 Hard
"""

import json
import random
import os

random.seed(42)

questions = []
qid = 0


def add_q(difficulty, question, choices, answer, explanation, tags):
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Ratio Word Problems",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

def gen_easy():
    """Generate 200 easy ratio word problems."""

    # Type 1: Simple missing value (45 questions)
    contexts = [
        ("pens", "pencils"), ("boys", "girls"), ("cats", "dogs"),
        ("apples", "oranges"), ("men", "women"), ("cars", "trucks"),
        ("teachers", "students"), ("roses", "tulips"), ("chairs", "tables"),
        ("fiction books", "non-fiction books"),
    ]
    for i in range(45):
        a_part = random.randint(1, 7)
        b_part = random.randint(1, 7)
        while b_part == a_part:
            b_part = random.randint(1, 7)
        scale = random.randint(2, 12)
        a_val = a_part * scale
        b_val = b_part * scale
        ctx = contexts[i % len(contexts)]

        question = (
            f"The ratio of {ctx[0]} to {ctx[1]} is {a_part}:{b_part}. "
            f"If there are {a_val} {ctx[0]}, how many {ctx[1]} are there?"
        )
        correct = str(b_val)
        distractors = set()
        distractors.add(str(a_val + b_val))
        distractors.add(str(b_val + a_part))
        distractors.add(str(b_val - a_part if b_val - a_part > 0 else b_val + 2))
        while len(distractors) < 3:
            distractors.add(str(b_val + random.randint(-5, 5)))
        distractors.discard(correct)
        dist_list = list(distractors)[:3]
        choices = dist_list + [correct]
        random.shuffle(choices)

        explanation = (
            f"Scale factor = {a_val} ÷ {a_part} = {scale}. "
            f"{ctx[1].capitalize()} = {b_part} × {scale} = {b_val}."
        )
        add_q("Easy", question, choices, correct, explanation,
               ["ratios", "word problems", "missing value", "scaling"])

    # Type 2: Split total into two parts (45 questions)
    items = [
        ("boys", "girls", "students"), ("men", "women", "employees"),
        ("fiction", "non-fiction", "books"), ("red balls", "blue balls", "balls"),
        ("passed", "failed", "examinees"), ("cars", "motorcycles", "vehicles"),
        ("adults", "children", "attendees"), ("local", "imported", "products"),
        ("permanent", "contractual", "workers"), ("savings", "expenses", "income"),
    ]
    for i in range(45):
        a_part = random.randint(1, 6)
        b_part = random.randint(1, 6)
        while b_part == a_part:
            b_part = random.randint(1, 6)
        total_parts = a_part + b_part
        scale = random.randint(3, 15)
        total = total_parts * scale
        a_val = a_part * scale
        ctx = items[i % len(items)]
        ask_first = random.choice([True, False])

        if ask_first:
            question = (
                f"In a group of {total} {ctx[2]}, the ratio of {ctx[0]} to {ctx[1]} is "
                f"{a_part}:{b_part}. How many {ctx[0]} are there?"
            )
            correct = str(a_val)
            explanation = (
                f"Total parts = {a_part} + {b_part} = {total_parts}. "
                f"Each part = {total} ÷ {total_parts} = {scale}. "
                f"{ctx[0].capitalize()} = {a_part} × {scale} = {a_val}."
            )
        else:
            b_val = b_part * scale
            question = (
                f"In a group of {total} {ctx[2]}, the ratio of {ctx[0]} to {ctx[1]} is "
                f"{a_part}:{b_part}. How many {ctx[1]} are there?"
            )
            correct = str(b_val)
            explanation = (
                f"Total parts = {a_part} + {b_part} = {total_parts}. "
                f"Each part = {total} ÷ {total_parts} = {scale}. "
                f"{ctx[1].capitalize()} = {b_part} × {scale} = {b_val}."
            )

        distractors = set()
        distractors.add(str(total))
        distractors.add(str(int(correct) + scale))
        distractors.add(str(abs(int(correct) - scale)))
        while len(distractors) < 3:
            distractors.add(str(int(correct) + random.randint(-8, 8)))
        distractors.discard(correct)
        dist_list = list(distractors)[:3]
        choices = dist_list + [correct]
        random.shuffle(choices)

        add_q("Easy", question, choices, correct, explanation,
               ["ratios", "word problems", "splitting totals", "part-to-whole"])

    # Type 3: Translate verbal statement to ratio (20 questions)
    statements = [
        ("There are {a} boys for every {b} girls in the class.", f"{{}}:{{}}", "boys to girls"),
        ("A store sells {a} shirts for every {b} pants.", f"{{}}:{{}}", "shirts to pants"),
        ("For every {a} wins, the team has {b} losses.", f"{{}}:{{}}", "wins to losses"),
        ("The recipe uses {a} cups of flour for every {b} cups of sugar.", f"{{}}:{{}}", "flour to sugar"),
        ("There are {a} teachers for every {b} students.", f"{{}}:{{}}", "teachers to students"),
    ]
    for i in range(20):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        while b == a:
            b = random.randint(1, 9)
        tmpl = statements[i % len(statements)]
        stmt = tmpl[0].format(a=a, b=b)
        question = f'{stmt} What is the ratio of {tmpl[2]}?'
        correct = f"{a}:{b}"
        wrong1 = f"{b}:{a}"
        wrong2 = f"{a}:{a+b}"
        wrong3 = f"{b}:{a+b}"
        choices = [wrong1, wrong2, wrong3, correct]
        random.shuffle(choices)
        explanation = (
            f'The statement says "{a} ... for every {b} ..." so the ratio of {tmpl[2]} is {a}:{b}.'
        )
        add_q("Easy", question, choices, correct, explanation,
               ["ratios", "word problems", "translation", "verbal to ratio"])

    # Type 4: Part-to-whole identification (25 questions)
    for i in range(25):
        a = random.randint(2, 8)
        b = random.randint(2, 8)
        while b == a:
            b = random.randint(2, 8)
        total = a + b
        scale = random.randint(2, 10)
        actual_total = total * scale
        actual_a = a * scale

        contexts_pw = [
            ("red marbles", "blue marbles", "marbles"),
            ("boys", "girls", "students"),
            ("passed", "failed", "examinees"),
            ("local", "imported", "goods"),
            ("fiction", "non-fiction", "books"),
        ]
        ctx = contexts_pw[i % len(contexts_pw)]
        question = (
            f"A bag contains {ctx[0]} and {ctx[1]} in the ratio {a}:{b}. "
            f"If there are {actual_total} {ctx[2]} in total, how many are {ctx[0]}?"
        )
        correct = str(actual_a)
        d1 = str(actual_total - actual_a)
        d2 = str(actual_a + a)
        d3 = str(actual_a - b if actual_a - b > 0 else actual_a + b)
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Total parts = {a} + {b} = {total}. Each part = {actual_total} ÷ {total} = {scale}. "
            f"{ctx[0].capitalize()} = {a} × {scale} = {actual_a}."
        )
        add_q("Easy", question, choices, correct, explanation,
               ["ratios", "word problems", "part-to-whole", "splitting totals"])

    # Type 5: Simple ratio with money (20 questions)
    for i in range(20):
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        while b == a:
            b = random.randint(1, 5)
        total_parts = a + b
        amounts = [10000, 20000, 30000, 40000, 50000, 60000, 80000, 90000, 100000, 120000]
        # Pick a total divisible by total_parts
        base = random.choice([1000, 2000, 5000, 10000])
        total_money = total_parts * base * random.randint(1, 5)
        scale_m = total_money // total_parts
        a_share = a * scale_m
        b_share = b * scale_m

        names = [("Ana", "Ben"), ("Carlo", "Diana"), ("Ella", "Frank"),
                 ("Grace", "Henry"), ("Iris", "Jake")]
        n = names[i % len(names)]
        question = (
            f"₱{total_money:,} is divided between {n[0]} and {n[1]} in the ratio {a}:{b}. "
            f"How much does {n[0]} receive?"
        )
        correct = f"₱{a_share:,}"
        d1 = f"₱{b_share:,}"
        d2 = f"₱{total_money:,}"
        d3 = f"₱{a_share + base:,}"
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Total parts = {a} + {b} = {total_parts}. "
            f"Each part = ₱{total_money:,} ÷ {total_parts} = ₱{scale_m:,}. "
            f"{n[0]}'s share = {a} × ₱{scale_m:,} = ₱{a_share:,}."
        )
        add_q("Easy", question, choices, correct, explanation,
               ["ratios", "word problems", "money", "splitting totals"])

    # Type 6: Unit rate / "per" problems (20 questions)
    for i in range(20):
        unit_cost = random.choice([5, 8, 10, 12, 15, 20, 25, 30, 40, 50])
        qty1 = random.randint(2, 6)
        cost1 = unit_cost * qty1
        qty2 = random.randint(7, 15)
        cost2 = unit_cost * qty2

        items_list = ["notebooks", "pens", "folders", "markers", "erasers",
                      "envelopes", "stamps", "clips", "rulers", "tapes"]
        item = items_list[i % len(items_list)]
        question = (
            f"If {qty1} {item} cost ₱{cost1}, how much do {qty2} {item} cost?"
        )
        correct = f"₱{cost2}"
        d1 = f"₱{cost2 + unit_cost}"
        d2 = f"₱{cost2 - unit_cost}"
        d3 = f"₱{cost1 * 2}"
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Unit cost = ₱{cost1} ÷ {qty1} = ₱{unit_cost}. "
            f"Cost of {qty2} = {qty2} × ₱{unit_cost} = ₱{cost2}."
        )
        add_q("Easy", question, choices, correct, explanation,
               ["ratios", "word problems", "unit rate", "scaling"])

    # Type 7: Simple "for every" with total (25 questions)
    for i in range(25):
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        while a == b:
            b = random.randint(1, 5)
        total_parts = a + b
        scale = random.randint(3, 12)
        total = total_parts * scale

        pairs = [
            ("buses on Route A", "buses on Route B", "buses"),
            ("male applicants", "female applicants", "applicants"),
            ("senior citizens", "young adults", "people"),
            ("hardcover books", "paperback books", "books"),
            ("desktop computers", "laptops", "computers"),
        ]
        ctx = pairs[i % len(pairs)]
        question = (
            f"For every {a} {ctx[0]}, there are {b} {ctx[1]}. "
            f"If there are {total} {ctx[2]} in total, how many are {ctx[0]}?"
        )
        correct_val = a * scale
        correct = str(correct_val)
        d1 = str(b * scale)
        d2 = str(total)
        d3 = str(correct_val + a)
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Ratio = {a}:{b}, total parts = {total_parts}. "
            f"Each part = {total} ÷ {total_parts} = {scale}. "
            f"{ctx[0].capitalize()} = {a} × {scale} = {correct_val}."
        )
        add_q("Easy", question, choices, correct, explanation,
               ["ratios", "word problems", "for every", "part-to-whole"])


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

def gen_medium():
    """Generate 200 medium ratio word problems."""

    # Type 1: Three-part ratio split (40 questions)
    for i in range(40):
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        c = random.randint(1, 5)
        while a == b or b == c or a == c:
            a, b, c = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
        total_parts = a + b + c
        scale = random.randint(2, 10)
        total = total_parts * scale

        contexts = [
            ("education", "health", "infrastructure", "budget"),
            ("salaries", "operations", "capital outlay", "fund"),
            ("Partner A", "Partner B", "Partner C", "investment"),
            ("gold", "silver", "bronze", "medals"),
            ("small", "medium", "large", "items"),
            ("Grade 1", "Grade 2", "Grade 3", "students"),
            ("Department A", "Department B", "Department C", "employees"),
            ("rice", "corn", "wheat", "supply"),
        ]
        ctx = contexts[i % len(contexts)]

        # Ask for one of the three parts randomly
        ask_idx = random.randint(0, 2)
        parts = [a, b, c]
        vals = [a * scale, b * scale, c * scale]

        if "₱" in ctx[3] or ctx[3] in ["budget", "fund", "investment"]:
            total_display = f"₱{total * 1000:,}"
            correct = f"₱{vals[ask_idx] * 1000:,}"
            d1 = f"₱{vals[(ask_idx + 1) % 3] * 1000:,}"
            d2 = f"₱{vals[(ask_idx + 2) % 3] * 1000:,}"
            d3 = f"₱{(vals[ask_idx] + scale) * 1000:,}"
        else:
            total_display = str(total)
            correct = str(vals[ask_idx])
            d1 = str(vals[(ask_idx + 1) % 3])
            d2 = str(vals[(ask_idx + 2) % 3])
            d3 = str(vals[ask_idx] + scale)

        question = (
            f"A {ctx[3]} of {total_display} is divided among {ctx[0]}, {ctx[1]}, and {ctx[2]} "
            f"in the ratio {a}:{b}:{c}. How much does {ctx[ask_idx]} receive?"
        )
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(vals[ask_idx] + random.randint(1, 5) * (1000 if "₱" in correct else 1)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)

        explanation = (
            f"Total parts = {a} + {b} + {c} = {total_parts}. "
            f"Each part = {total_display} ÷ {total_parts} = {scale if '₱' not in total_display else f'₱{scale * 1000:,}'}. "
            f"{ctx[ask_idx].capitalize()} = {parts[ask_idx]} × {scale if '₱' not in total_display else f'₱{scale * 1000:,}'} = {correct}."
        )
        add_q("Medium", question, choices, correct, explanation,
               ["ratios", "word problems", "three-part ratio", "splitting totals"])

    # Type 2: Find the difference between shares (30 questions)
    for i in range(30):
        a = random.randint(2, 7)
        b = random.randint(2, 7)
        while a == b:
            b = random.randint(2, 7)
        if a < b:
            a, b = b, a  # ensure a > b for positive difference
        diff_parts = a - b
        scale = random.randint(3, 15)
        total = (a + b) * scale
        a_val = a * scale
        b_val = b * scale
        diff_val = diff_parts * scale

        pairs = [
            ("men", "women", "employees"), ("boys", "girls", "students"),
            ("senior", "junior", "staff"), ("local", "foreign", "tourists"),
            ("approved", "rejected", "applications"),
        ]
        ctx = pairs[i % len(pairs)]
        question = (
            f"The ratio of {ctx[0]} to {ctx[1]} in a group of {total} {ctx[2]} is {a}:{b}. "
            f"How many more {ctx[0]} than {ctx[1]} are there?"
        )
        correct = str(diff_val)
        d1 = str(a_val)
        d2 = str(b_val)
        d3 = str(diff_val + scale)
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Total parts = {a + b}. Each part = {total} ÷ {a + b} = {scale}. "
            f"{ctx[0].capitalize()} = {a} × {scale} = {a_val}. "
            f"{ctx[1].capitalize()} = {b} × {scale} = {b_val}. "
            f"Difference = {a_val} - {b_val} = {diff_val}."
        )
        add_q("Medium", question, choices, correct, explanation,
               ["ratios", "word problems", "difference", "multi-step"])

    # Type 3: Given one part, find total (30 questions)
    for i in range(30):
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        while a == b:
            b = random.randint(2, 6)
        total_parts = a + b
        scale = random.randint(3, 12)
        a_val = a * scale
        total = total_parts * scale

        contexts = [
            ("passed", "failed", "took the exam"),
            ("men", "women", "attended the seminar"),
            ("fiction", "non-fiction", "are in the library"),
            ("cars", "motorcycles", "are in the parking lot"),
            ("teachers", "staff", "work at the school"),
        ]
        ctx = contexts[i % len(contexts)]
        question = (
            f"The ratio of {ctx[0]} to {ctx[1]} is {a}:{b}. "
            f"If {a_val} {ctx[0]} {ctx[2]}, how many people/items are there in total?"
        )
        correct = str(total)
        d1 = str(a_val)
        d2 = str(total + scale)
        d3 = str(total - a)
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Scale factor = {a_val} ÷ {a} = {scale}. "
            f"Total = ({a} + {b}) × {scale} = {total_parts} × {scale} = {total}."
        )
        add_q("Medium", question, choices, correct, explanation,
               ["ratios", "word problems", "find total", "scaling"])

    # Type 4: Ratio with "difference given" (30 questions)
    for i in range(30):
        a = random.randint(3, 9)
        b = random.randint(1, a - 1)
        diff_parts = a - b
        scale = random.randint(2, 10)
        diff_val = diff_parts * scale
        a_val = a * scale
        b_val = b * scale
        total = a_val + b_val

        contexts = [
            ("winners", "losers"), ("adults", "children"),
            ("boys", "girls"), ("passed", "failed"),
            ("domestic", "international"),
        ]
        ctx = contexts[i % len(contexts)]
        question = (
            f"The ratio of {ctx[0]} to {ctx[1]} is {a}:{b}. "
            f"If there are {diff_val} more {ctx[0]} than {ctx[1]}, "
            f"how many {ctx[0]} are there?"
        )
        correct = str(a_val)
        d1 = str(b_val)
        d2 = str(total)
        d3 = str(a_val + diff_parts)
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Difference in parts = {a} - {b} = {diff_parts}. "
            f"Each part = {diff_val} ÷ {diff_parts} = {scale}. "
            f"{ctx[0].capitalize()} = {a} × {scale} = {a_val}."
        )
        add_q("Medium", question, choices, correct, explanation,
               ["ratios", "word problems", "difference given", "multi-step"])

    # Type 5: Map scale problems (20 questions)
    for i in range(20):
        map_cm = random.randint(2, 15)
        scale_val = random.choice([10000, 20000, 25000, 50000, 100000, 200000])
        actual_cm = map_cm * scale_val
        # Convert to km
        actual_km = actual_cm / 100000

        question = (
            f"A map has a scale of 1:{scale_val:,}. If two locations are {map_cm} cm apart "
            f"on the map, what is the actual distance in kilometers?"
        )
        correct = f"{actual_km:g}"
        d1 = f"{actual_km * 2:g}"
        d2 = f"{actual_km / 2:g}"
        d3 = f"{actual_km + 1:g}"
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Actual distance = {map_cm} × {scale_val:,} = {actual_cm:,} cm = "
            f"{actual_cm:,} ÷ 100,000 = {actual_km:g} km."
        )
        add_q("Medium", question, choices, correct, explanation,
               ["ratios", "word problems", "map scale", "unit conversion"])

    # Type 6: Ratio in recipes/mixtures (25 questions)
    for i in range(25):
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        c = random.randint(1, 5)
        while a == b or b == c:
            b = random.randint(1, 5)
            c = random.randint(1, 5)
        total_parts = a + b + c
        # Given total mixture
        scale = random.randint(2, 8)
        total = total_parts * scale

        ingredients = [
            ("cement", "sand", "gravel", "bags"),
            ("flour", "sugar", "butter", "cups"),
            ("water", "vinegar", "oil", "liters"),
            ("red paint", "blue paint", "white paint", "liters"),
            ("rice", "beans", "corn", "kilograms"),
        ]
        ctx = ingredients[i % len(ingredients)]
        ask_idx = random.randint(0, 2)
        parts = [a, b, c]
        vals = [a * scale, b * scale, c * scale]

        question = (
            f"A mixture requires {ctx[0]}, {ctx[1]}, and {ctx[2]} in the ratio {a}:{b}:{c}. "
            f"If the total mixture is {total} {ctx[3]}, how many {ctx[3]} of {ctx[ask_idx]} are needed?"
        )
        correct = str(vals[ask_idx])
        d1 = str(vals[(ask_idx + 1) % 3])
        d2 = str(vals[(ask_idx + 2) % 3])
        d3 = str(vals[ask_idx] + scale)
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(vals[ask_idx] + random.randint(1, 5)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        explanation = (
            f"Total parts = {a} + {b} + {c} = {total_parts}. "
            f"Each part = {total} ÷ {total_parts} = {scale}. "
            f"{ctx[ask_idx].capitalize()} = {parts[ask_idx]} × {scale} = {vals[ask_idx]}."
        )
        add_q("Medium", question, choices, correct, explanation,
               ["ratios", "word problems", "mixture", "three-part ratio"])

    # Type 7: Percentage-ratio hybrid (25 questions)
    for i in range(25):
        a = random.randint(1, 4)
        b = random.randint(1, 4)
        while a == b:
            b = random.randint(1, 4)
        total_parts = a + b
        scale = random.randint(5, 20)
        total = total_parts * scale
        a_val = a * scale

        # What fraction/percentage is a of total?
        from fractions import Fraction
        frac = Fraction(a, total_parts)

        contexts = [
            ("boys", "girls", "class"), ("passed", "failed", "batch"),
            ("local", "foreign", "visitors"), ("new", "returning", "customers"),
            ("full-time", "part-time", "employees"),
        ]
        ctx = contexts[i % len(contexts)]
        question = (
            f"The ratio of {ctx[0]} to {ctx[1]} in a {ctx[2]} is {a}:{b}. "
            f"What fraction of the {ctx[2]} are {ctx[0]}?"
        )
        correct = f"{a}/{total_parts}"
        d1 = f"{a}/{b}"
        d2 = f"{b}/{total_parts}"
        d3 = f"{b}/{a}"
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Total parts = {a} + {b} = {total_parts}. "
            f"Fraction of {ctx[0]} = {a}/{total_parts}."
        )
        add_q("Medium", question, choices, correct, explanation,
               ["ratios", "word problems", "fraction", "part-to-whole"])


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

def gen_hard():
    """Generate 200 hard ratio word problems."""

    # Type 1: Changing ratios (35 questions)
    for i in range(35):
        # Original ratio a:b, after adding/removing, new ratio c:d
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        while a == b:
            b = random.randint(2, 6)
        scale = random.randint(2, 8)
        a_val = a * scale
        b_val = b * scale

        # Add some to one side
        add_amount = random.randint(2, 15)
        new_a = a_val + add_amount
        # Find new ratio (may not simplify nicely, so let's engineer it)
        # Instead, engineer: original ratio a:b with scale x, add k to first
        # Let's use a cleaner approach
        x = random.randint(2, 6)
        orig_a_part = random.randint(2, 5)
        orig_b_part = random.randint(2, 5)
        while orig_a_part == orig_b_part:
            orig_b_part = random.randint(2, 5)

        orig_a_val = orig_a_part * x
        orig_b_val = orig_b_part * x
        total_orig = orig_a_val + orig_b_val

        # After adding k to first group
        k = random.randint(2, 10)
        new_a_val = orig_a_val + k
        new_total = total_orig + k

        contexts = [
            ("boys", "girls", "class"), ("men", "women", "office"),
            ("red marbles", "blue marbles", "bag"), ("cats", "dogs", "shelter"),
            ("fiction", "non-fiction", "collection"),
        ]
        ctx = contexts[i % len(contexts)]

        question = (
            f"In a {ctx[2]}, the ratio of {ctx[0]} to {ctx[1]} is {orig_a_part}:{orig_b_part}. "
            f"If {k} more {ctx[0]} join, the total becomes {new_total}. "
            f"How many {ctx[1]} are there?"
        )
        correct = str(orig_b_val)
        d1 = str(orig_a_val)
        d2 = str(new_a_val)
        d3 = str(orig_b_val + k)
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(orig_b_val + random.randint(1, 5)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        explanation = (
            f"Original total = {new_total} - {k} = {total_orig}. "
            f"Total parts = {orig_a_part} + {orig_b_part} = {orig_a_part + orig_b_part}. "
            f"Each part = {total_orig} ÷ {orig_a_part + orig_b_part} = {x}. "
            f"{ctx[1].capitalize()} = {orig_b_part} × {x} = {orig_b_val}."
        )
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "changing ratios", "multi-step"])

    # Type 2: Combined ratios (25 questions)
    for i in range(25):
        # A:B = p:q, B:C = q:r (B is common)
        p = random.randint(2, 5)
        q = random.randint(2, 5)
        r = random.randint(2, 5)
        while p == q or q == r:
            q = random.randint(2, 5)
            r = random.randint(2, 5)

        # Combined A:B:C = p:q:r
        total_parts = p + q + r
        scale = random.randint(2, 8)
        total = total_parts * scale

        question = (
            f"The ratio of A to B is {p}:{q}, and the ratio of B to C is {q}:{r}. "
            f"If the total of A, B, and C is {total}, find the value of C."
        )
        c_val = r * scale
        correct = str(c_val)
        d1 = str(p * scale)
        d2 = str(q * scale)
        d3 = str(c_val + scale)
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(c_val + random.randint(1, 5)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        explanation = (
            f"Since B = {q} in both ratios, A:B:C = {p}:{q}:{r}. "
            f"Total parts = {p} + {q} + {r} = {total_parts}. "
            f"Each part = {total} ÷ {total_parts} = {scale}. "
            f"C = {r} × {scale} = {c_val}."
        )
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "combined ratios", "multi-step"])

    # Type 3: Working backwards (25 questions)
    for i in range(25):
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        while a == b:
            b = random.randint(2, 6)
        scale = random.randint(3, 10)
        current_a = a * scale
        current_b = b * scale

        removed = random.randint(2, min(current_a, current_b) - 1)
        # Ask: what was the original count before removal?
        original_a = current_a + removed

        contexts = [
            ("boys", "girls"), ("red", "blue"), ("passed", "failed"),
            ("local", "foreign"), ("new", "old"),
        ]
        ctx = contexts[i % len(contexts)]
        question = (
            f"After {removed} {ctx[0]} left a group, the ratio of {ctx[0]} to {ctx[1]} "
            f"became {a}:{b}. If there are now {current_b} {ctx[1]}, "
            f"how many {ctx[0]} were there originally?"
        )
        correct = str(original_a)
        d1 = str(current_a)
        d2 = str(original_a + removed)
        d3 = str(current_a + current_b)
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(original_a + random.randint(1, 5)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        explanation = (
            f"Current {ctx[0]} = {a} × ({current_b} ÷ {b}) = {a} × {scale} = {current_a}. "
            f"Original {ctx[0]} = {current_a} + {removed} = {original_a}."
        )
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "working backwards", "multi-step"])

    # Type 4: Income/expenditure/savings (25 questions)
    for i in range(25):
        # Income ratio a:b, each saves fixed amount
        a_inc = random.randint(3, 7)
        b_inc = random.randint(2, 6)
        while a_inc == b_inc:
            b_inc = random.randint(2, 6)
        savings = random.choice([1000, 2000, 3000, 4000, 5000])
        # A's income = a_inc * x, B's income = b_inc * x
        # A's expenditure = a_inc * x - savings
        # B's expenditure = b_inc * x - savings
        # We need expenditure ratio to be nice
        # Let x be chosen so both expenditures are positive
        x = random.randint(2, 5)
        while a_inc * x <= savings // 1000 or b_inc * x <= savings // 1000:
            x += 1

        a_income = a_inc * x * 1000
        b_income = b_inc * x * 1000
        a_exp = a_income - savings
        b_exp = b_income - savings

        question = (
            f"The ratio of A's income to B's income is {a_inc}:{b_inc}. "
            f"If each saves ₱{savings:,} and A's income is ₱{a_income:,}, "
            f"what is B's expenditure?"
        )
        correct = f"₱{b_exp:,}"
        d1 = f"₱{a_exp:,}"
        d2 = f"₱{b_income:,}"
        d3 = f"₱{b_exp + savings:,}"
        choices = [d1, d2, d3, correct]
        random.shuffle(choices)
        explanation = (
            f"Scale factor = ₱{a_income:,} ÷ {a_inc} = ₱{x * 1000:,}. "
            f"B's income = {b_inc} × ₱{x * 1000:,} = ₱{b_income:,}. "
            f"B's expenditure = ₱{b_income:,} - ₱{savings:,} = ₱{b_exp:,}."
        )
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "income expenditure", "multi-step"])

    # Type 5: Ratio with algebra (20 questions)
    for i in range(20):
        # Two numbers in ratio a:b, their sum/product/difference given
        a = random.randint(2, 7)
        b = random.randint(2, 7)
        while a == b:
            b = random.randint(2, 7)
        x = random.randint(2, 8)
        a_val = a * x
        b_val = b * x
        total = a_val + b_val
        diff = abs(a_val - b_val)

        # Randomly ask sum or difference
        if random.choice([True, False]):
            question = (
                f"Two numbers are in the ratio {a}:{b}. If their sum is {total}, "
                f"find the larger number."
            )
            correct = str(max(a_val, b_val))
            explanation = (
                f"Let the numbers be {a}x and {b}x. "
                f"Sum = {a}x + {b}x = {a + b}x = {total}. "
                f"x = {total} ÷ {a + b} = {x}. "
                f"Larger number = {max(a, b)} × {x} = {max(a_val, b_val)}."
            )
        else:
            question = (
                f"Two numbers are in the ratio {a}:{b}. If their difference is {diff}, "
                f"find the smaller number."
            )
            correct = str(min(a_val, b_val))
            explanation = (
                f"Let the numbers be {a}x and {b}x. "
                f"Difference = {max(a, b)}x - {min(a, b)}x = {abs(a - b)}x = {diff}. "
                f"x = {diff} ÷ {abs(a - b)} = {x}. "
                f"Smaller number = {min(a, b)} × {x} = {min(a_val, b_val)}."
            )

        d1 = str(a_val + b_val)
        d2 = str(int(correct) + x)
        d3 = str(abs(int(correct) - x))
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(int(correct) + random.randint(1, 10)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "algebra", "sum and difference"])

    # Type 6: Multi-group comparison (20 questions)
    for i in range(20):
        # Department A has ratio of men:women = a:b
        # Department B has ratio of men:women = c:d
        # Total men given, find total women or vice versa
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        c = random.randint(2, 5)
        d = random.randint(2, 5)
        while a == b:
            b = random.randint(2, 5)
        while c == d:
            d = random.randint(2, 5)

        scale_a = random.randint(2, 6)
        scale_b = random.randint(2, 6)
        men_a = a * scale_a
        women_a = b * scale_a
        men_b = c * scale_b
        women_b = d * scale_b
        total_men = men_a + men_b
        total_women = women_a + women_b
        grand_total = total_men + total_women

        question = (
            f"Department X has men and women in the ratio {a}:{b} with {men_a + women_a} employees. "
            f"Department Y has men and women in the ratio {c}:{d} with {men_b + women_b} employees. "
            f"How many women are there in total across both departments?"
        )
        correct = str(total_women)
        d1 = str(total_men)
        d2 = str(women_a)
        d3 = str(women_b)
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(total_women + random.randint(1, 8)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        explanation = (
            f"Dept X: total parts = {a + b}, each part = {men_a + women_a} ÷ {a + b} = {scale_a}. "
            f"Women in X = {b} × {scale_a} = {women_a}. "
            f"Dept Y: total parts = {c + d}, each part = {men_b + women_b} ÷ {c + d} = {scale_b}. "
            f"Women in Y = {d} × {scale_b} = {women_b}. "
            f"Total women = {women_a} + {women_b} = {total_women}."
        )
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "multi-group", "multi-step"])

    # Type 7: Successive ratio changes (25 questions)
    for i in range(25):
        # Original ratio, then increase one part by percentage or fixed amount
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        while a == b:
            b = random.randint(2, 5)
        scale = random.randint(4, 10)
        a_val = a * scale
        b_val = b * scale
        total_orig = a_val + b_val

        # Transfer some from one to another
        transfer = random.randint(1, min(a_val, b_val) - 1)
        new_a = a_val - transfer
        new_b = b_val + transfer

        from math import gcd
        g = gcd(new_a, new_b)
        new_ratio_a = new_a // g
        new_ratio_b = new_b // g

        contexts = [
            ("Team A", "Team B"), ("Box 1", "Box 2"),
            ("Account A", "Account B"), ("Shelf 1", "Shelf 2"),
            ("Group X", "Group Y"),
        ]
        ctx = contexts[i % len(contexts)]
        question = (
            f"{ctx[0]} and {ctx[1]} have items in the ratio {a}:{b}. "
            f"If {transfer} items are moved from {ctx[0]} to {ctx[1]}, "
            f"and the total is {total_orig}, what is the new ratio?"
        )
        correct = f"{new_ratio_a}:{new_ratio_b}"
        # Generate wrong ratios
        d1 = f"{new_ratio_b}:{new_ratio_a}"
        d2 = f"{a}:{b}"
        d3 = f"{new_ratio_a + 1}:{new_ratio_b}"
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(f"{new_ratio_a}:{new_ratio_b + random.randint(1, 3)}")
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        explanation = (
            f"Each part = {total_orig} ÷ {a + b} = {scale}. "
            f"Original: {ctx[0]} = {a_val}, {ctx[1]} = {b_val}. "
            f"After transfer: {ctx[0]} = {a_val} - {transfer} = {new_a}, "
            f"{ctx[1]} = {b_val} + {transfer} = {new_b}. "
            f"New ratio = {new_a}:{new_b} = {new_ratio_a}:{new_ratio_b}."
        )
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "ratio change", "transfer"])

    # Type 8: Age-related ratio problems (25 questions)
    for i in range(25):
        # Current age ratio a:b, after n years ratio becomes c:d
        # Let ages be ax and bx now
        # After n years: (ax+n):(bx+n) = c:d ... but this gets complex
        # Simpler: give current ratio and one age, find the other
        a = random.randint(2, 7)
        b = random.randint(2, 7)
        while a == b:
            b = random.randint(2, 7)
        x = random.randint(2, 6)
        age_a = a * x
        age_b = b * x
        years = random.randint(2, 8)
        future_a = age_a + years
        future_b = age_b + years

        from math import gcd
        g = gcd(future_a, future_b)
        fut_ratio_a = future_a // g
        fut_ratio_b = future_b // g

        question = (
            f"The present ages of A and B are in the ratio {a}:{b}. "
            f"If A is {age_a} years old now, what will be B's age after {years} years?"
        )
        correct = str(future_b)
        d1 = str(age_b)
        d2 = str(future_a)
        d3 = str(age_b + years + 2)
        choices = list(set([d1, d2, d3, correct]))
        while len(choices) < 4:
            choices.append(str(future_b + random.randint(1, 5)))
        choices = choices[:4]
        if correct not in choices:
            choices[0] = correct
        random.shuffle(choices)
        explanation = (
            f"Scale factor = {age_a} ÷ {a} = {x}. "
            f"B's current age = {b} × {x} = {age_b}. "
            f"B's age after {years} years = {age_b} + {years} = {future_b}."
        )
        add_q("Hard", question, choices, correct, explanation,
               ["ratios", "word problems", "ages", "multi-step"])


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    gen_easy()
    gen_medium()
    gen_hard()

    # Verify counts
    easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
    medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

    print(f"Easy: {easy_count}")
    print(f"Medium: {medium_count}")
    print(f"Hard: {hard_count}")
    print(f"Total: {len(questions)}")

    # Reassign IDs sequentially
    for idx, q in enumerate(questions, 1):
        q["id"] = idx

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "numerical-ability",
        "ratio-proportion-and-average", "ratio-word-problems"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"\nWritten to: {output_path}")
