"""
Generate 600 questions for Percentage Applications (CSE Numerical Ability).
200 Easy / 200 Medium / 200 Hard

Covers:
- Population problems (growth, decline, migration)
- Grade computation (scores, weighted averages, passing rates)
- Statistics and surveys (response distributions, approval ratings)
- Financial applications (budgets, savings, expenses, interest)
- Multi-step percentage application problems
- Percentage interpretation and analysis

Run: python scripts/gen_percentage_applications_questions.py
Output: data/seed/questions/numerical-ability/percentages/percentage-applications/questions.json
"""

import json
import random
from pathlib import Path

random.seed(42)

questions: list[dict] = []
qid = 0

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "numerical-ability" / "percentages"
    / "percentage-applications" / "questions.json"
)


def add_q(difficulty: str, question: str, choices: list[str],
           answer: str, explanation: str, tags: list[str]) -> None:
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Percentage Applications",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    })


def fmt_num(val: float) -> str:
    """Format a number nicely (no trailing zeros)."""
    if val == int(val):
        return f"{int(val):,}"
    s = f"{val:,.4f}".rstrip("0").rstrip(".")
    return s


def fmt_pct(val: float) -> str:
    """Format a percentage value."""
    if val == int(val):
        return f"{int(val)}%"
    s = f"{val:.2f}".rstrip("0").rstrip(".")
    return f"{s}%"


def make_choices_numeric(correct: float, unit: str = "",
                         prefix: str = "", spread: float = 0.0) -> tuple[list[str], str]:
    """Generate 4 numeric choices with plausible distractors."""
    if spread == 0.0:
        spread = max(abs(correct) * 0.3, 5)

    correct_str = f"{prefix}{fmt_num(correct)}{unit}"
    distractors: set[str] = set()
    attempts = 0

    offsets = [
        correct * 0.5, correct * 1.5, correct * 2,
        correct + spread, correct - spread,
        correct + spread * 0.5, correct - spread * 0.5,
        correct * 0.8, correct * 1.2,
        correct + spread * 1.5, correct - spread * 1.5,
    ]
    random.shuffle(offsets)

    for d in offsets:
        if d <= 0 and correct > 0:
            continue
        d_rounded = round(d, 2) if d != int(d) else int(d)
        d_str = f"{prefix}{fmt_num(d_rounded)}{unit}"
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)
        if len(distractors) >= 3:
            break

    while len(distractors) < 3:
        d = correct + random.choice([-1, 1]) * random.randint(1, int(spread) + 5)
        if d <= 0 and correct > 0:
            d = correct + random.randint(1, int(spread) + 5)
        d_str = f"{prefix}{fmt_num(round(d, 2))}{unit}"
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1
        if attempts > 50:
            break

    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str


def make_pct_choices(correct_pct: float) -> tuple[list[str], str]:
    """Generate 4 percentage choices with plausible distractors."""
    correct_str = fmt_pct(correct_pct)
    distractors: set[str] = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 200:
        error_type = random.choice([
            "off_small", "off_large", "complement", "half", "double", "swap_digits"
        ])
        if error_type == "off_small":
            d = correct_pct + random.choice([-5, -3, -2, 2, 3, 5, 8, 10, -10])
        elif error_type == "off_large":
            d = correct_pct + random.choice([-15, -20, 15, 20, 25, -25])
        elif error_type == "complement":
            d = 100 - correct_pct
        elif error_type == "half":
            d = correct_pct / 2
        elif error_type == "double":
            d = correct_pct * 2
        elif error_type == "swap_digits":
            s = str(int(correct_pct))
            if len(s) >= 2:
                d = float(s[1] + s[0]) if s[0] != s[1] else correct_pct + 11
            else:
                d = correct_pct + 10
        else:
            d = correct_pct + random.randint(-10, 10)

        d = round(d, 2)
        d_str = fmt_pct(d)
        if d_str != correct_str and d > 0 and d < 200 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    while len(distractors) < 3:
        d = correct_pct + random.randint(1, 20)
        d_str = fmt_pct(d)
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)
    random.shuffle(choices)
    return choices, correct_str


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- E1: Population Problems (Easy) - 40 questions ---

pop_easy_data = [
    (5000, 10, "Barangay Maligaya"), (8000, 5, "Barangay San Jose"),
    (10000, 20, "Municipality of Taguig"), (3000, 15, "Barangay Rizal"),
    (6000, 25, "Sitio Mabuhay"), (12000, 8, "Barangay Bagong Silang"),
    (4000, 12, "Barangay Pag-asa"), (15000, 6, "Municipality of Calamba"),
    (2000, 30, "Barangay Masagana"), (9000, 4, "Barangay Kalinaw"),
    (7000, 10, "Barangay Maginhawa"), (20000, 5, "City of San Fernando"),
    (1500, 20, "Sitio Bulaklak"), (11000, 15, "Barangay Maunlad"),
    (5500, 8, "Barangay Tahimik"), (25000, 2, "Province of Laguna"),
    (3500, 40, "Barangay Bagong Bayan"), (8500, 12, "Barangay Luntian"),
    (4500, 6, "Barangay Payapa"), (16000, 10, "Municipality of Biñan"),
]

for pop, rate, place in pop_easy_data:
    increase = int(pop * rate / 100)
    new_pop = pop + increase
    choices, answer = make_choices_numeric(increase, "")
    add_q(
        "Easy",
        f"The population of {place} is {fmt_num(pop)}. If the population "
        f"increased by {rate}%, how many people were added?",
        choices, answer,
        f"{rate}% of {fmt_num(pop)} = {rate}/100 × {fmt_num(pop)} = {fmt_num(increase)}.",
        ["population", "percentage applications", "find the part"]
    )

# Population: find the new total
for pop, rate, place in pop_easy_data:
    increase = int(pop * rate / 100)
    new_pop = pop + increase
    choices, answer = make_choices_numeric(new_pop, "")
    add_q(
        "Easy",
        f"{place} had a population of {fmt_num(pop)}. After a {rate}% increase, "
        f"what is the new population?",
        choices, answer,
        f"Increase = {rate}% of {fmt_num(pop)} = {fmt_num(increase)}. "
        f"New population = {fmt_num(pop)} + {fmt_num(increase)} = {fmt_num(new_pop)}.",
        ["population", "percentage applications", "find total"]
    )


# --- E2: Grade Computation (Easy) - 40 questions ---
grade_easy_data = [
    (36, 50), (45, 60), (72, 80), (18, 25), (27, 30),
    (40, 50), (54, 60), (64, 80), (20, 25), (24, 30),
    (35, 50), (48, 60), (56, 80), (22, 25), (21, 30),
    (42, 50), (51, 60), (68, 80), (19, 25), (28, 30),
]

for correct_items, total_items in grade_easy_data:
    pct = round(correct_items / total_items * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Easy",
        f"A student answered {correct_items} out of {total_items} questions correctly. "
        f"What is the student's percentage score?",
        choices, answer,
        f"Percentage = {correct_items} ÷ {total_items} × 100 = "
        f"{correct_items}/{total_items} × 100 = {fmt_pct(pct)}.",
        ["grade computation", "percentage applications", "find the rate"]
    )

# Grade: find how many items needed to pass
passing_data = [
    (40, 75), (60, 80), (40, 70), (80, 75), (100, 60),
    (30, 80), (45, 60), (70, 80), (90, 80), (25, 60),
    (50, 80), (60, 75), (40, 60), (80, 70), (100, 75),
    (35, 80), (55, 60), (75, 80), (85, 60), (20, 75),
]

for total, pass_rate in passing_data:
    needed = total * pass_rate // 100
    # Skip if not exact
    if total * pass_rate % 100 != 0:
        continue
    choices, answer = make_choices_numeric(needed, "")
    add_q(
        "Easy",
        f"An exam has {total} items. A student needs at least {pass_rate}% to pass. "
        f"How many items must the student answer correctly?",
        choices, answer,
        f"{pass_rate}% of {total} = {pass_rate}/100 × {total} = {needed} items.",
        ["grade computation", "percentage applications", "passing rate"]
    )


# --- E3: Survey/Statistics (Easy) - 40 questions ---
survey_easy_data = [
    (500, 60, "approved of the new policy"),
    (400, 75, "were satisfied with the service"),
    (1000, 45, "preferred public transportation"),
    (200, 80, "agreed with the proposal"),
    (300, 55, "voted in favor of the resolution"),
    (600, 70, "supported the infrastructure project"),
    (800, 35, "reported experiencing delays"),
    (250, 40, "chose Option A in the survey"),
    (1500, 20, "filed a complaint"),
    (350, 90, "attended the community meeting"),
    (450, 65, "rated the service as excellent"),
    (700, 30, "disagreed with the new schedule"),
    (150, 60, "completed the training program"),
    (900, 85, "passed the qualifying exam"),
    (550, 50, "preferred the morning shift"),
    (1200, 15, "requested a transfer"),
    (650, 72, "were regular employees"),
    (180, 25, "were absent during the inspection"),
    (2000, 10, "submitted late reports"),
    (750, 48, "participated in the wellness program"),
]

for respondents, pct, description in survey_easy_data:
    count = int(respondents * pct / 100)
    choices, answer = make_choices_numeric(count, "")
    add_q(
        "Easy",
        f"In a survey of {fmt_num(respondents)} respondents, {pct}% {description}. "
        f"How many respondents is this?",
        choices, answer,
        f"{pct}% of {fmt_num(respondents)} = {pct}/100 × {fmt_num(respondents)} = {fmt_num(count)}.",
        ["survey", "statistics", "percentage applications", "find the part"]
    )

# Survey: find the percentage
survey_rate_easy = [
    (120, 400, "passed the exam"),
    (75, 300, "were female applicants"),
    (180, 600, "chose the new design"),
    (50, 200, "reported issues"),
    (90, 500, "were late to work"),
    (210, 700, "preferred online services"),
    (36, 150, "requested overtime"),
    (160, 800, "attended the seminar"),
    (45, 250, "filed for leave"),
    (280, 1000, "used the new system"),
    (63, 350, "were promoted"),
    (48, 120, "scored above 90%"),
    (100, 500, "were contractual workers"),
    (72, 240, "completed the survey"),
    (150, 600, "owned a vehicle"),
    (35, 175, "had graduate degrees"),
    (84, 420, "lived within 5 km"),
    (60, 300, "were first-time applicants"),
    (200, 800, "received commendations"),
    (55, 220, "volunteered for the project"),
]

for part, whole, description in survey_rate_easy:
    pct = round(part / whole * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Easy",
        f"Out of {fmt_num(whole)} employees, {fmt_num(part)} {description}. "
        f"What percentage is this?",
        choices, answer,
        f"Percentage = {fmt_num(part)} ÷ {fmt_num(whole)} × 100 = {fmt_pct(pct)}.",
        ["survey", "statistics", "percentage applications", "find the rate"]
    )


# --- E4: Financial Applications (Easy) - 40 questions ---
budget_easy_data = [
    (50000, 30, "food"), (40000, 25, "rent"), (35000, 20, "transportation"),
    (60000, 15, "savings"), (45000, 10, "utilities"), (55000, 40, "housing"),
    (30000, 35, "groceries"), (70000, 12, "education"), (25000, 50, "rent"),
    (80000, 8, "entertainment"), (48000, 20, "food"), (65000, 15, "transportation"),
    (38000, 25, "savings"), (52000, 30, "housing"), (42000, 18, "utilities"),
    (75000, 5, "clothing"), (28000, 45, "rent"), (90000, 10, "insurance"),
    (33000, 22, "food"), (58000, 28, "housing"),
]

for salary, pct, category in budget_easy_data:
    amount = int(salary * pct / 100)
    choices, answer = make_choices_numeric(amount, "", "₱")
    add_q(
        "Easy",
        f"An employee earns ₱{fmt_num(salary)} per month and allocates {pct}% "
        f"for {category}. How much is allocated for {category}?",
        choices, answer,
        f"{pct}% of ₱{fmt_num(salary)} = {pct}/100 × {fmt_num(salary)} = ₱{fmt_num(amount)}.",
        ["financial", "budget", "percentage applications", "find the part"]
    )

# Financial: find remaining after allocation
for salary, pct, category in budget_easy_data:
    amount = int(salary * pct / 100)
    remaining = salary - amount
    choices, answer = make_choices_numeric(remaining, "", "₱")
    add_q(
        "Easy",
        f"From a monthly salary of ₱{fmt_num(salary)}, an employee spends {pct}% "
        f"on {category}. How much remains after this expense?",
        choices, answer,
        f"Amount spent = {pct}% of ₱{fmt_num(salary)} = ₱{fmt_num(amount)}. "
        f"Remaining = ₱{fmt_num(salary)} − ₱{fmt_num(amount)} = ₱{fmt_num(remaining)}.",
        ["financial", "budget", "percentage applications", "remainder"]
    )

# Trim easy to exactly 200
easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
if easy_count > 200:
    # Remove excess from the end
    excess = easy_count - 200
    to_remove = []
    for i in range(len(questions) - 1, -1, -1):
        if questions[i]["difficulty"] == "Easy" and excess > 0:
            to_remove.append(i)
            excess -= 1
    for i in sorted(to_remove, reverse=True):
        questions.pop(i)


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- M1: Population Problems (Medium) - 35 questions ---
pop_medium_data = [
    (45000, 12, "City of Meycauayan"), (32000, 8, "Municipality of Marilao"),
    (18500, 15, "Barangay Commonwealth"), (72000, 6, "City of Malolos"),
    (28000, 18, "Municipality of Bocaue"), (55000, 9, "City of San Jose del Monte"),
    (15000, 22, "Barangay Payatas"), (63000, 7, "Municipality of Obando"),
    (41000, 11, "City of Valenzuela"), (22000, 14, "Barangay Bagumbayan"),
    (85000, 4, "Province of Bulacan"), (37000, 16, "Municipality of Norzagaray"),
    (19500, 25, "Barangay Kamuning"), (48000, 13, "City of Caloocan"),
    (26000, 19, "Municipality of Angat"),
]

# Population growth: find the rate
for pop, rate, place in pop_medium_data:
    increase = int(pop * rate / 100)
    new_pop = pop + increase
    choices, answer = make_pct_choices(rate)
    add_q(
        "Medium",
        f"The population of {place} grew from {fmt_num(pop)} to {fmt_num(new_pop)}. "
        f"What is the percentage increase?",
        choices, answer,
        f"Increase = {fmt_num(new_pop)} − {fmt_num(pop)} = {fmt_num(increase)}. "
        f"Rate = {fmt_num(increase)} ÷ {fmt_num(pop)} × 100 = {fmt_pct(rate)}.",
        ["population", "percentage applications", "find the rate"]
    )

# Population decline
pop_decline_medium = [
    (50000, 8, "Municipality of Plaridel"), (35000, 12, "Barangay Tandang Sora"),
    (28000, 15, "Barangay Culiat"), (62000, 5, "City of Marikina"),
    (44000, 10, "Municipality of Rodriguez"), (18000, 20, "Barangay Batasan"),
    (75000, 6, "City of Antipolo"), (31000, 14, "Barangay Holy Spirit"),
    (53000, 9, "Municipality of Taytay"), (21000, 18, "Barangay Bagong Pag-asa"),
]

for pop, rate, place in pop_decline_medium:
    decrease = int(pop * rate / 100)
    new_pop = pop - decrease
    choices, answer = make_choices_numeric(new_pop, "")
    add_q(
        "Medium",
        f"{place} had a population of {fmt_num(pop)}. Due to migration, "
        f"the population decreased by {rate}%. What is the new population?",
        choices, answer,
        f"Decrease = {rate}% of {fmt_num(pop)} = {fmt_num(decrease)}. "
        f"New population = {fmt_num(pop)} − {fmt_num(decrease)} = {fmt_num(new_pop)}.",
        ["population", "percentage applications", "population decline"]
    )

# Population: find original given new and rate
pop_reverse_medium = [
    (11000, 10, "Barangay Pinyahan"), (13800, 15, "Barangay Sikatuna"),
    (16800, 20, "Municipality of Cainta"), (21600, 8, "City of Pasig"),
    (27500, 25, "Barangay Ugong"), (9360, 12, "Barangay Mandaluyong"),
    (15400, 10, "Municipality of San Mateo"), (23000, 15, "City of Taguig"),
    (33600, 12, "Barangay Pembo"), (19200, 20, "Municipality of Pateros"),
]

for new_pop, rate, place in pop_reverse_medium:
    original = int(new_pop / (1 + rate / 100))
    choices, answer = make_choices_numeric(original, "")
    add_q(
        "Medium",
        f"After a {rate}% population increase, {place} now has {fmt_num(new_pop)} "
        f"residents. What was the population before the increase?",
        choices, answer,
        f"Original = {fmt_num(new_pop)} ÷ (1 + {rate}/100) = "
        f"{fmt_num(new_pop)} ÷ {1 + rate/100:.2f} = {fmt_num(original)}.",
        ["population", "percentage applications", "find the whole", "reverse"]
    )


# --- M2: Grade Computation (Medium) - 35 questions ---
# Weighted grades
weighted_grade_medium = [
    # (component, weight, score) tuples, then question about final grade
    ([("Quiz", 30, 85), ("Midterm", 30, 78), ("Final", 40, 90)], "Math"),
    ([("Attendance", 10, 100), ("Assignments", 20, 88), ("Exam", 70, 82)], "English"),
    ([("Project", 25, 92), ("Quiz", 25, 76), ("Final Exam", 50, 84)], "Science"),
    ([("Recitation", 15, 90), ("Homework", 25, 85), ("Exam", 60, 80)], "Filipino"),
    ([("Lab Work", 20, 95), ("Written Exam", 40, 78), ("Practical", 40, 88)], "Computer"),
    ([("Quiz", 20, 80), ("Project", 30, 90), ("Final", 50, 75)], "History"),
    ([("Participation", 10, 95), ("Midterm", 40, 82), ("Final", 50, 88)], "Economics"),
    ([("Homework", 15, 90), ("Quiz", 25, 84), ("Exam", 60, 76)], "Physics"),
    ([("Report", 20, 88), ("Midterm", 30, 80), ("Final", 50, 86)], "Chemistry"),
    ([("Activity", 25, 92), ("Quiz", 25, 78), ("Exam", 50, 82)], "Biology"),
    ([("Oral", 15, 88), ("Written", 35, 82), ("Final", 50, 90)], "Literature"),
    ([("Lab", 30, 94), ("Theory", 30, 76), ("Final", 40, 84)], "Electronics"),
    ([("Drill", 20, 85), ("Quiz", 30, 80), ("Exam", 50, 88)], "Accounting"),
    ([("Case Study", 25, 90), ("Midterm", 25, 78), ("Final", 50, 82)], "Management"),
    ([("Practicum", 30, 92), ("Written", 30, 84), ("Final", 40, 78)], "Nursing"),
]

for components, subject in weighted_grade_medium:
    weighted_sum = sum(w * s / 100 for _, w, s in components)
    weighted_grade = round(weighted_sum, 2)
    component_desc = ", ".join(
        f"{name} ({w}%) = {s}" for name, w, s in components
    )
    choices, answer = make_choices_numeric(weighted_grade, "")
    add_q(
        "Medium",
        f"A student's {subject} grade is computed as follows: {component_desc}. "
        f"What is the student's weighted average?",
        choices, answer,
        f"Weighted average = " +
        " + ".join(f"({w}/100 × {s})" for _, w, s in components) +
        f" = {fmt_num(weighted_grade)}.",
        ["grade computation", "weighted average", "percentage applications"]
    )

# Grade: how many more items needed
# Only use combinations where target_pct * total_possible / 100 is a whole number
grade_needed_medium = [
    (60, 40, 75, 80), (50, 32, 80, 100), (45, 30, 70, 100),
    (80, 55, 75, 100), (70, 48, 80, 100), (55, 38, 75, 80),
    (65, 42, 70, 100), (40, 28, 75, 60), (90, 60, 70, 100),
    (75, 50, 80, 100), (85, 58, 75, 100), (48, 32, 70, 80),
    (35, 22, 60, 50), (95, 68, 75, 100), (60, 40, 80, 80),
    (70, 50, 75, 100), (50, 35, 75, 80), (68, 45, 70, 100),
    (42, 28, 70, 60), (88, 62, 75, 100),
]

for total, current_correct, target_pct, total_possible in grade_needed_medium[:20]:
    needed_total = total_possible * target_pct // 100
    # Verify it's exact (no rounding ambiguity)
    if total_possible * target_pct % 100 != 0:
        continue
    still_needed = needed_total - current_correct
    remaining_items = total_possible - total
    if still_needed <= 0 or still_needed > remaining_items:
        continue
    choices, answer = make_choices_numeric(still_needed, "")
    add_q(
        "Medium",
        f"A student has answered {current_correct} correctly out of {total} items so far. "
        f"The exam has {total_possible} items total. To achieve at least {target_pct}% overall, "
        f"how many more correct answers does the student need from the remaining items?",
        choices, answer,
        f"Total needed = {target_pct}% of {total_possible} = {needed_total}. "
        f"Still needed = {needed_total} − {current_correct} = {still_needed}.",
        ["grade computation", "percentage applications", "multi-step"]
    )


# --- M3: Survey/Statistics (Medium) - 35 questions ---
# Multi-category surveys
survey_medium_data = [
    (1000, {"Excellent": 35, "Good": 40, "Fair": 15, "Poor": 10}, "service quality"),
    (800, {"Agree": 45, "Neutral": 30, "Disagree": 25}, "new work schedule"),
    (1500, {"Bus": 40, "Jeepney": 30, "MRT": 20, "Taxi": 10}, "transportation mode"),
    (600, {"Very Satisfied": 50, "Satisfied": 30, "Dissatisfied": 20}, "office facilities"),
    (2000, {"Yes": 65, "No": 25, "Undecided": 10}, "proposed policy change"),
    (500, {"Morning": 55, "Afternoon": 30, "Night": 15}, "preferred shift"),
    (1200, {"Online": 60, "In-person": 25, "Hybrid": 15}, "training format"),
    (900, {"Strongly Agree": 40, "Agree": 35, "Disagree": 25}, "salary increase"),
    (750, {"Public": 45, "Private": 35, "Self-employed": 20}, "employment sector"),
    (1800, {"Satisfied": 70, "Neutral": 20, "Unsatisfied": 10}, "health services"),
]

for total_resp, categories, topic in survey_medium_data:
    # Ask about the difference between two categories
    cat_list = list(categories.items())
    cat1_name, cat1_pct = cat_list[0]
    cat2_name, cat2_pct = cat_list[1]
    cat1_count = int(total_resp * cat1_pct / 100)
    cat2_count = int(total_resp * cat2_pct / 100)
    diff = abs(cat1_count - cat2_count)
    choices, answer = make_choices_numeric(diff, "")
    add_q(
        "Medium",
        f"In a survey of {fmt_num(total_resp)} respondents about {topic}, "
        f"{cat1_pct}% chose \"{cat1_name}\" and {cat2_pct}% chose \"{cat2_name}\". "
        f"How many more respondents chose \"{cat1_name}\" than \"{cat2_name}\"?",
        choices, answer,
        f"\"{cat1_name}\" = {cat1_pct}% of {fmt_num(total_resp)} = {fmt_num(cat1_count)}. "
        f"\"{cat2_name}\" = {cat2_pct}% of {fmt_num(total_resp)} = {fmt_num(cat2_count)}. "
        f"Difference = {fmt_num(cat1_count)} − {fmt_num(cat2_count)} = {fmt_num(diff)}.",
        ["survey", "statistics", "percentage applications", "comparison"]
    )

# Survey: combined percentages
for total_resp, categories, topic in survey_medium_data:
    cat_list = list(categories.items())
    if len(cat_list) >= 3:
        # Combine first two categories
        combined_pct = cat_list[0][1] + cat_list[1][1]
        combined_count = int(total_resp * combined_pct / 100)
        choices, answer = make_choices_numeric(combined_count, "")
        add_q(
            "Medium",
            f"A survey of {fmt_num(total_resp)} people about {topic} showed: "
            f"{cat_list[0][1]}% chose \"{cat_list[0][0]}\" and {cat_list[1][1]}% "
            f"chose \"{cat_list[1][0]}\". How many respondents chose either of these two options?",
            choices, answer,
            f"Combined = {cat_list[0][1]}% + {cat_list[1][1]}% = {combined_pct}%. "
            f"{combined_pct}% of {fmt_num(total_resp)} = {fmt_num(combined_count)}.",
            ["survey", "statistics", "percentage applications", "combined"]
        )

# Survey: find total respondents given count and percentage
survey_reverse_medium = [
    (180, 30, "preferred online filing"),
    (240, 40, "supported the new regulation"),
    (150, 25, "reported dissatisfaction"),
    (360, 60, "completed the training"),
    (90, 15, "requested reassignment"),
    (280, 35, "used public transport"),
    (420, 70, "passed the assessment"),
    (108, 12, "filed a grievance"),
    (225, 45, "attended the orientation"),
    (320, 80, "met the deadline"),
    (135, 27, "were promoted last year"),
    (200, 50, "chose early retirement"),
    (168, 24, "worked overtime regularly"),
    (350, 50, "were satisfied with benefits"),
    (96, 16, "transferred to another office"),
]

for count, pct, description in survey_reverse_medium:
    total = int(count / (pct / 100))
    choices, answer = make_choices_numeric(total, "")
    add_q(
        "Medium",
        f"In a government office, {fmt_num(count)} employees ({pct}% of the total) "
        f"{description}. How many employees are there in total?",
        choices, answer,
        f"Total = {fmt_num(count)} ÷ ({pct}/100) = {fmt_num(count)} ÷ {pct/100:.2f} = {fmt_num(total)}.",
        ["survey", "statistics", "percentage applications", "find the whole"]
    )


# --- M4: Financial Applications (Medium) - 35 questions ---
# Budget allocation with multiple categories
budget_medium_data = [
    (85000, [("Housing", 30), ("Food", 25), ("Transport", 15), ("Savings", 20), ("Others", 10)]),
    (65000, [("Rent", 35), ("Groceries", 20), ("Utilities", 10), ("Savings", 25), ("Leisure", 10)]),
    (95000, [("Mortgage", 40), ("Food", 20), ("Education", 15), ("Savings", 15), ("Misc", 10)]),
    (50000, [("Rent", 30), ("Food", 30), ("Transport", 20), ("Savings", 10), ("Bills", 10)]),
    (72000, [("Housing", 25), ("Food", 25), ("Education", 20), ("Savings", 20), ("Health", 10)]),
    (110000, [("Mortgage", 35), ("Food", 15), ("Transport", 10), ("Savings", 30), ("Others", 10)]),
    (45000, [("Rent", 40), ("Food", 25), ("Transport", 15), ("Savings", 10), ("Utilities", 10)]),
    (78000, [("Housing", 30), ("Food", 20), ("Education", 25), ("Savings", 15), ("Health", 10)]),
]

for salary, allocations in budget_medium_data:
    # Ask about savings amount
    savings_pct = next(pct for name, pct in allocations if "Sav" in name)
    savings_amt = int(salary * savings_pct / 100)
    # Ask about total non-housing expenses
    non_housing = [(name, pct) for name, pct in allocations
                   if "Hous" not in name and "Rent" not in name and "Mort" not in name]
    non_housing_pct = sum(p for _, p in non_housing)
    non_housing_amt = int(salary * non_housing_pct / 100)

    choices, answer = make_choices_numeric(savings_amt, "", "₱")
    add_q(
        "Medium",
        f"An employee earning ₱{fmt_num(salary)} monthly allocates: " +
        ", ".join(f"{name} ({pct}%)" for name, pct in allocations) +
        f". How much goes to Savings?",
        choices, answer,
        f"Savings = {savings_pct}% of ₱{fmt_num(salary)} = ₱{fmt_num(savings_amt)}.",
        ["financial", "budget allocation", "percentage applications"]
    )

    choices2, answer2 = make_choices_numeric(non_housing_amt, "", "₱")
    add_q(
        "Medium",
        f"From a ₱{fmt_num(salary)} salary with allocations: " +
        ", ".join(f"{name} ({pct}%)" for name, pct in allocations) +
        f". How much is spent on non-housing expenses combined?",
        choices2, answer2,
        f"Non-housing = {non_housing_pct}% of ₱{fmt_num(salary)} = ₱{fmt_num(non_housing_amt)}.",
        ["financial", "budget allocation", "percentage applications", "combined"]
    )

# Simple interest problems
interest_medium = [
    (100000, 5, 1), (200000, 3, 2), (150000, 4, 1), (80000, 6, 1),
    (250000, 2, 3), (120000, 5, 2), (50000, 8, 1), (300000, 3, 1),
    (180000, 4, 2), (75000, 6, 2), (400000, 2, 1), (90000, 7, 1),
    (160000, 5, 1), (220000, 3, 2), (130000, 4, 3),
]

for principal, rate, years in interest_medium[:15]:
    interest = int(principal * rate * years / 100)
    choices, answer = make_choices_numeric(interest, "", "₱")
    add_q(
        "Medium",
        f"An employee deposited ₱{fmt_num(principal)} in a savings account with "
        f"{rate}% simple annual interest. How much interest is earned after "
        f"{years} year{'s' if years > 1 else ''}?",
        choices, answer,
        f"Interest = Principal × Rate × Time = ₱{fmt_num(principal)} × {rate}/100 × {years} "
        f"= ₱{fmt_num(interest)}.",
        ["financial", "interest", "percentage applications", "simple interest"]
    )

# Trim medium to exactly 200
medium_count = len([q for q in questions if q["difficulty"] == "Medium"])
if medium_count > 200:
    excess = medium_count - 200
    to_remove = []
    for i in range(len(questions) - 1, -1, -1):
        if questions[i]["difficulty"] == "Medium" and excess > 0:
            to_remove.append(i)
            excess -= 1
    for i in sorted(to_remove, reverse=True):
        questions.pop(i)


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- H1: Population Multi-Step (Hard) - 30 questions ---
pop_hard_data = [
    (80000, 10, 5, "City of Meycauayan"),
    (45000, 8, 12, "Municipality of Marilao"),
    (120000, 6, 15, "City of San Jose del Monte"),
    (35000, 15, 3, "Barangay Commonwealth"),
    (95000, 4, 20, "City of Malolos"),
    (28000, 12, 8, "Municipality of Bocaue"),
    (150000, 3, 25, "Province of Bulacan"),
    (62000, 7, 10, "City of Valenzuela"),
    (18000, 20, 4, "Barangay Payatas"),
    (73000, 5, 18, "Municipality of Obando"),
    (42000, 9, 7, "Barangay Bagumbayan"),
    (88000, 6, 14, "City of Caloocan"),
    (55000, 11, 6, "Municipality of Norzagaray"),
    (31000, 14, 9, "Barangay Kamuning"),
    (105000, 5, 16, "City of Antipolo"),
]

# Two successive population changes
for pop, rate1, rate2, place in pop_hard_data:
    after_first = round(pop * (1 + rate1 / 100))
    after_second = round(after_first * (1 - rate2 / 100))
    choices, answer = make_choices_numeric(after_second, "")
    add_q(
        "Hard",
        f"{place} had a population of {fmt_num(pop)}. The population increased by "
        f"{rate1}% in the first year, then decreased by {rate2}% in the second year. "
        f"What is the population after two years?",
        choices, answer,
        f"After Year 1: {fmt_num(pop)} × {1 + rate1/100:.2f} = {fmt_num(after_first)}. "
        f"After Year 2: {fmt_num(after_first)} × {1 - rate2/100:.2f} = {fmt_num(after_second)}.",
        ["population", "percentage applications", "successive changes", "multi-step"]
    )

# Population: find original given two changes and final
for pop, rate1, rate2, place in pop_hard_data:
    after_first = round(pop * (1 + rate1 / 100))
    after_second = round(after_first * (1 + rate2 / 100))
    # Given after_second, find original
    multiplier = (1 + rate1 / 100) * (1 + rate2 / 100)
    original_calc = round(after_second / multiplier)
    choices, answer = make_choices_numeric(pop, "")
    add_q(
        "Hard",
        f"After a {rate1}% increase followed by a {rate2}% increase, "
        f"{place} now has {fmt_num(after_second)} residents. "
        f"What was the original population?",
        choices, answer,
        f"Combined multiplier = {1 + rate1/100:.2f} × {1 + rate2/100:.2f} = {multiplier:.4f}. "
        f"Original = {fmt_num(after_second)} ÷ {multiplier:.4f} ≈ {fmt_num(pop)}.",
        ["population", "percentage applications", "reverse", "successive changes"]
    )


# --- H2: Grade Computation (Hard) - 30 questions ---
# Complex weighted grades with passing threshold
grade_hard_data = [
    # (components, passing_grade, subject)
    ([("Quiz 1", 15, 82), ("Quiz 2", 15, 78), ("Midterm", 30, 85), ("Final", 40, 0)], 80, "Math"),
    ([("Homework", 10, 90), ("Quiz", 20, 75), ("Project", 20, 88), ("Exam", 50, 0)], 82, "Science"),
    ([("Recitation", 10, 95), ("Assignment", 15, 85), ("Midterm", 25, 80), ("Final", 50, 0)], 78, "English"),
    ([("Lab", 20, 92), ("Quiz", 20, 76), ("Midterm", 20, 84), ("Final", 40, 0)], 80, "Chemistry"),
    ([("Oral", 15, 88), ("Written", 15, 82), ("Project", 20, 90), ("Exam", 50, 0)], 85, "Filipino"),
    ([("Activity", 10, 94), ("Quiz", 20, 80), ("Midterm", 30, 78), ("Final", 40, 0)], 80, "History"),
    ([("Drill", 15, 86), ("Quiz", 15, 80), ("Project", 20, 92), ("Exam", 50, 0)], 82, "Physics"),
    ([("Case Study", 20, 88), ("Quiz", 20, 74), ("Midterm", 20, 82), ("Final", 40, 0)], 80, "Economics"),
    ([("Practicum", 25, 90), ("Quiz", 15, 78), ("Midterm", 20, 84), ("Final", 40, 0)], 82, "Nursing"),
    ([("Report", 15, 92), ("Quiz", 20, 76), ("Midterm", 25, 80), ("Final", 40, 0)], 80, "Accounting"),
    ([("Lab Work", 20, 88), ("Quiz", 15, 82), ("Project", 15, 94), ("Exam", 50, 0)], 84, "Biology"),
    ([("Participation", 10, 96), ("Quiz", 20, 78), ("Midterm", 30, 82), ("Final", 40, 0)], 80, "Sociology"),
    ([("Homework", 15, 84), ("Quiz", 15, 80), ("Project", 20, 90), ("Exam", 50, 0)], 82, "Statistics"),
    ([("Oral Exam", 20, 86), ("Written", 20, 80), ("Midterm", 20, 84), ("Final", 40, 0)], 82, "Literature"),
    ([("Activity", 15, 90), ("Quiz", 15, 76), ("Midterm", 30, 82), ("Final", 40, 0)], 80, "Geography"),
]

for components, passing, subject in grade_hard_data:
    # Calculate what score is needed on the Final to achieve passing grade
    known_weighted = sum(w * s / 100 for _, w, s in components if s > 0)
    final_weight = next(w for _, w, s in components if s == 0)
    # passing = known_weighted + (final_weight * x / 100)
    # x = (passing - known_weighted) * 100 / final_weight
    needed_score = round((passing - known_weighted) * 100 / final_weight, 2)
    if needed_score < 0 or needed_score > 100:
        continue

    component_desc = ", ".join(
        f"{name} ({w}%) = {s}" for name, w, s in components if s > 0
    )
    final_name = next(name for name, w, s in components if s == 0)
    choices, answer = make_choices_numeric(needed_score, "")
    add_q(
        "Hard",
        f"A student's {subject} grades so far: {component_desc}. "
        f"The {final_name} is worth {final_weight}% of the total grade. "
        f"What minimum score must the student get on the {final_name} to achieve "
        f"an overall grade of {passing}?",
        choices, answer,
        f"Known weighted sum = " +
        " + ".join(f"({w}% × {s})" for _, w, s in components if s > 0) +
        f" = {known_weighted:.2f}. "
        f"Need: {passing} = {known_weighted:.2f} + ({final_weight}/100 × x). "
        f"x = ({passing} − {known_weighted:.2f}) × 100 ÷ {final_weight} = {fmt_num(needed_score)}.",
        ["grade computation", "weighted average", "percentage applications", "reverse"]
    )

# Class performance comparison
class_hard_data = [
    (45, 36, 50, 40, "Section A", "Section B"),
    (60, 48, 55, 44, "Morning Class", "Afternoon Class"),
    (40, 30, 35, 28, "Group 1", "Group 2"),
    (50, 42, 48, 38, "Batch 2024", "Batch 2025"),
    (55, 44, 45, 36, "Regular", "Irregular"),
    (65, 52, 70, 56, "Male", "Female"),
    (38, 30, 42, 34, "Science Major", "Arts Major"),
    (72, 54, 68, 51, "Day Shift", "Night Shift"),
    (48, 36, 52, 39, "Online", "Face-to-face"),
    (80, 64, 75, 60, "Senior", "Junior"),
    (56, 42, 44, 33, "Local", "Transferee"),
    (62, 50, 58, 46, "Scholars", "Non-scholars"),
    (35, 28, 40, 32, "First-takers", "Retakers"),
    (90, 72, 85, 68, "With Review", "Without Review"),
    (46, 37, 54, 43, "Public School", "Private School"),
]

for total_a, pass_a, total_b, pass_b, name_a, name_b in class_hard_data:
    rate_a = round(pass_a / total_a * 100, 2)
    rate_b = round(pass_b / total_b * 100, 2)
    higher = name_a if rate_a > rate_b else name_b
    diff = round(abs(rate_a - rate_b), 2)
    choices = [
        f"{name_a} by {fmt_pct(abs(rate_a - rate_b))}",
        f"{name_b} by {fmt_pct(abs(rate_a - rate_b))}",
        f"{name_a} by {fmt_pct(abs(rate_a - rate_b) + 5)}",
        f"They have equal passing rates",
    ]
    answer = f"{higher} by {fmt_pct(diff)}"
    if answer not in choices:
        choices[0] = answer
    random.shuffle(choices)
    add_q(
        "Hard",
        f"{name_a} had {pass_a} passers out of {total_a} students. "
        f"{name_b} had {pass_b} passers out of {total_b} students. "
        f"Which group has a higher passing rate, and by how many percentage points?",
        choices, answer,
        f"{name_a} rate = {pass_a}/{total_a} × 100 = {fmt_pct(rate_a)}. "
        f"{name_b} rate = {pass_b}/{total_b} × 100 = {fmt_pct(rate_b)}. "
        f"Difference = {fmt_pct(diff)} in favor of {higher}.",
        ["grade computation", "percentage applications", "comparison", "analysis"]
    )


# --- H3: Survey/Statistics (Hard) - 35 questions ---
# Survey with percentage point changes
survey_hard_changes = [
    (1200, 65, 72, "approved of the mayor's performance"),
    (800, 48, 55, "supported the infrastructure project"),
    (2000, 70, 62, "were satisfied with public transport"),
    (1500, 55, 60, "favored the new tax policy"),
    (900, 80, 74, "rated healthcare as adequate"),
    (1100, 42, 50, "preferred online government services"),
    (600, 75, 68, "trusted the local government"),
    (1800, 58, 65, "supported environmental regulations"),
    (750, 35, 42, "planned to relocate"),
    (2500, 60, 52, "were satisfied with their salary"),
    (1000, 45, 53, "approved of the education reform"),
    (1400, 72, 65, "felt safe in their community"),
    (500, 38, 46, "used digital payment systems"),
    (1600, 55, 48, "supported the curfew policy"),
    (950, 68, 75, "were satisfied with water supply"),
]

for total, old_pct, new_pct, description in survey_hard_changes:
    old_count = int(total * old_pct / 100)
    new_count = int(total * new_pct / 100)
    pct_point_change = new_pct - old_pct
    direction = "increase" if pct_point_change > 0 else "decrease"
    abs_change = abs(new_count - old_count)
    choices, answer = make_choices_numeric(abs_change, "")
    add_q(
        "Hard",
        f"A survey of {fmt_num(total)} residents showed that those who {description} "
        f"changed from {old_pct}% to {new_pct}%. How many more (or fewer) residents "
        f"does this represent?",
        choices, answer,
        f"Old count = {old_pct}% of {fmt_num(total)} = {fmt_num(old_count)}. "
        f"New count = {new_pct}% of {fmt_num(total)} = {fmt_num(new_count)}. "
        f"Change = |{fmt_num(new_count)} − {fmt_num(old_count)}| = {fmt_num(abs_change)}.",
        ["survey", "statistics", "percentage applications", "percentage point change"]
    )

# Survey: relative percentage change in a rate
for total, old_pct, new_pct, description in survey_hard_changes:
    relative_change = round(abs(new_pct - old_pct) / old_pct * 100, 2)
    direction = "increase" if new_pct > old_pct else "decrease"
    choices, answer = make_pct_choices(relative_change)
    add_q(
        "Hard",
        f"The percentage of residents who {description} changed from {old_pct}% to "
        f"{new_pct}%. What is the relative percentage {direction} in this rate?",
        choices, answer,
        f"Change = |{new_pct} − {old_pct}| = {abs(new_pct - old_pct)} percentage points. "
        f"Relative change = {abs(new_pct - old_pct)} ÷ {old_pct} × 100 = {fmt_pct(relative_change)}.",
        ["survey", "statistics", "percentage applications", "relative change"]
    )

# Stratified survey analysis
strat_survey_hard = [
    (500, 300, 80, 60, "male", "female", "supported the sports program"),
    (400, 600, 70, 85, "senior", "junior", "preferred flexible hours"),
    (350, 450, 65, 72, "permanent", "contractual", "were satisfied with benefits"),
    (600, 400, 55, 45, "urban", "rural", "used online services"),
    (250, 750, 90, 70, "managers", "staff", "attended the training"),
]

for count_a, count_b, pct_a, pct_b, group_a, group_b, description in strat_survey_hard:
    total = count_a + count_b
    yes_a = int(count_a * pct_a / 100)
    yes_b = int(count_b * pct_b / 100)
    overall_pct = round((yes_a + yes_b) / total * 100, 2)
    choices, answer = make_pct_choices(overall_pct)
    add_q(
        "Hard",
        f"In a survey, {fmt_num(count_a)} {group_a} respondents and "
        f"{fmt_num(count_b)} {group_b} respondents were asked about a topic. "
        f"{pct_a}% of {group_a} and {pct_b}% of {group_b} {description}. "
        f"What is the overall percentage who {description}?",
        choices, answer,
        f"{group_a}: {pct_a}% of {fmt_num(count_a)} = {fmt_num(yes_a)}. "
        f"{group_b}: {pct_b}% of {fmt_num(count_b)} = {fmt_num(yes_b)}. "
        f"Overall = ({fmt_num(yes_a)} + {fmt_num(yes_b)}) ÷ {fmt_num(total)} × 100 = {fmt_pct(overall_pct)}.",
        ["survey", "statistics", "percentage applications", "stratified", "weighted"]
    )


# --- H4: Financial Applications (Hard) - 35 questions ---
# Multi-step budget problems
budget_hard_data = [
    (95000, 30, 10, "housing", "maintenance"),
    (120000, 25, 15, "rent", "utilities"),
    (80000, 35, 8, "mortgage", "insurance"),
    (65000, 20, 12, "food", "dining out"),
    (110000, 28, 5, "housing", "repairs"),
    (75000, 22, 18, "rent", "furnishing"),
    (88000, 32, 7, "mortgage", "property tax"),
    (55000, 40, 10, "rent", "internet and cable"),
    (130000, 15, 20, "savings", "investments"),
    (70000, 25, 12, "food", "health supplements"),
    (100000, 30, 8, "housing", "home improvement"),
    (85000, 20, 15, "transportation", "vehicle maintenance"),
    (60000, 35, 10, "rent", "water and electricity"),
    (140000, 18, 25, "savings", "emergency fund"),
    (92000, 28, 6, "housing", "association dues"),
]

for salary, pct1, pct2, cat1, cat2 in budget_hard_data:
    amt1 = int(salary * pct1 / 100)
    amt2_of_amt1 = int(amt1 * pct2 / 100)
    choices, answer = make_choices_numeric(amt2_of_amt1, "", "₱")
    add_q(
        "Hard",
        f"An employee earning ₱{fmt_num(salary)} allocates {pct1}% for {cat1}. "
        f"Of the {cat1} budget, {pct2}% goes to {cat2}. "
        f"How much is spent on {cat2}?",
        choices, answer,
        f"{cat1} = {pct1}% of ₱{fmt_num(salary)} = ₱{fmt_num(amt1)}. "
        f"{cat2} = {pct2}% of ₱{fmt_num(amt1)} = ₱{fmt_num(amt2_of_amt1)}.",
        ["financial", "budget", "percentage applications", "multi-step", "percentage of percentage"]
    )

# Salary after deductions
deduction_hard = [
    (45000, [("Tax", 12), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (60000, [("Tax", 15), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (35000, [("Tax", 10), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (80000, [("Tax", 20), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (55000, [("Tax", 12), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (100000, [("Tax", 25), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (42000, [("Tax", 10), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (72000, [("Tax", 18), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (38000, [("Tax", 8), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
    (90000, [("Tax", 22), ("SSS", 4), ("PhilHealth", 3), ("Pag-IBIG", 2)]),
]

for gross, deductions in deduction_hard:
    total_deduction_pct = sum(pct for _, pct in deductions)
    total_deduction_amt = int(gross * total_deduction_pct / 100)
    net = gross - total_deduction_amt
    deduction_desc = ", ".join(f"{name} ({pct}%)" for name, pct in deductions)
    choices, answer = make_choices_numeric(net, "", "₱")
    add_q(
        "Hard",
        f"An employee's gross salary is ₱{fmt_num(gross)}. Monthly deductions are: "
        f"{deduction_desc}. What is the net take-home pay?",
        choices, answer,
        f"Total deductions = {total_deduction_pct}% of ₱{fmt_num(gross)} = ₱{fmt_num(total_deduction_amt)}. "
        f"Net pay = ₱{fmt_num(gross)} − ₱{fmt_num(total_deduction_amt)} = ₱{fmt_num(net)}.",
        ["financial", "salary", "deductions", "percentage applications", "multi-step"]
    )

# Compound savings / successive financial changes
compound_hard = [
    (50000, 10, 5, "bonus", "tax on bonus"),
    (80000, 15, 8, "raise", "increased rent"),
    (120000, 8, 12, "bonus", "investment"),
    (65000, 20, 10, "overtime pay", "savings from overtime"),
    (95000, 12, 6, "performance bonus", "charity donation"),
    (40000, 25, 15, "side income", "tax on side income"),
    (110000, 6, 20, "allowance increase", "education fund"),
    (75000, 18, 5, "commission", "professional development"),
    (55000, 10, 30, "year-end bonus", "holiday spending"),
    (85000, 14, 8, "hazard pay", "health insurance upgrade"),
]

for base, pct_add, pct_of_add, desc_add, desc_use in compound_hard:
    added = int(base * pct_add / 100)
    new_total = base + added
    used = int(added * pct_of_add / 100)
    final = new_total - used
    choices, answer = make_choices_numeric(final, "", "₱")
    add_q(
        "Hard",
        f"An employee earning ₱{fmt_num(base)} receives a {pct_add}% {desc_add}. "
        f"From the {desc_add} amount, {pct_of_add}% is used for {desc_use}. "
        f"What is the employee's total income after the {desc_use} deduction?",
        choices, answer,
        f"{desc_add} = {pct_add}% of ₱{fmt_num(base)} = ₱{fmt_num(added)}. "
        f"New total = ₱{fmt_num(base)} + ₱{fmt_num(added)} = ₱{fmt_num(new_total)}. "
        f"{desc_use} = {pct_of_add}% of ₱{fmt_num(added)} = ₱{fmt_num(used)}. "
        f"Final = ₱{fmt_num(new_total)} − ₱{fmt_num(used)} = ₱{fmt_num(final)}.",
        ["financial", "percentage applications", "multi-step", "successive"]
    )


# --- H5: Multi-Step Application Problems (Hard) - 40 questions ---
# Government office scenarios
office_hard = [
    # (total_employees, pct_permanent, pct_promoted_from_permanent)
    (500, 70, 15), (800, 65, 20), (350, 80, 10), (1200, 60, 25),
    (600, 75, 12), (450, 72, 18), (900, 68, 14), (250, 85, 8),
    (700, 62, 22), (1000, 55, 30), (400, 78, 16), (550, 70, 20),
    (650, 66, 24), (300, 82, 12), (850, 58, 28),
]

for total, pct_perm, pct_promoted in office_hard:
    permanent = int(total * pct_perm / 100)
    promoted = int(permanent * pct_promoted / 100)
    choices, answer = make_choices_numeric(promoted, "")
    add_q(
        "Hard",
        f"A government office has {fmt_num(total)} employees. {pct_perm}% are permanent. "
        f"Of the permanent employees, {pct_promoted}% were promoted this year. "
        f"How many employees were promoted?",
        choices, answer,
        f"Permanent = {pct_perm}% of {fmt_num(total)} = {fmt_num(permanent)}. "
        f"Promoted = {pct_promoted}% of {fmt_num(permanent)} = {fmt_num(promoted)}.",
        ["government", "percentage applications", "multi-step", "percentage of percentage"]
    )

# Project completion scenarios
project_hard = [
    (2000000, 35, 80, "road construction"),
    (5000000, 42, 75, "building renovation"),
    (1500000, 60, 90, "IT system upgrade"),
    (3500000, 28, 85, "bridge repair"),
    (800000, 55, 70, "office renovation"),
    (4200000, 38, 82, "water system project"),
    (1200000, 45, 88, "school building"),
    (6000000, 30, 78, "hospital expansion"),
    (2800000, 50, 85, "drainage system"),
    (900000, 65, 92, "park development"),
]

for budget, pct_spent, pct_complete, project in project_hard:
    spent = int(budget * pct_spent / 100)
    remaining_budget = budget - spent
    remaining_work_pct = 100 - pct_complete
    # How much budget per percentage point of work done so far
    cost_per_pct = spent / pct_complete if pct_complete > 0 else 0
    estimated_remaining_cost = int(cost_per_pct * remaining_work_pct)

    choices, answer = make_choices_numeric(remaining_budget, "", "₱")
    add_q(
        "Hard",
        f"A {project} has a budget of ₱{fmt_num(budget)}. So far, {pct_spent}% of the "
        f"budget has been spent and the project is {pct_complete}% complete. "
        f"How much budget remains?",
        choices, answer,
        f"Spent = {pct_spent}% of ₱{fmt_num(budget)} = ₱{fmt_num(spent)}. "
        f"Remaining = ₱{fmt_num(budget)} − ₱{fmt_num(spent)} = ₱{fmt_num(remaining_budget)}.",
        ["government", "financial", "percentage applications", "project management"]
    )

# Workforce reduction and hiring
workforce_hard = [
    (1000, 15, 8, "due to automation", "for new positions"),
    (750, 10, 12, "through early retirement", "as fresh graduates"),
    (1200, 20, 5, "due to restructuring", "for specialized roles"),
    (500, 12, 18, "through attrition", "for expansion"),
    (900, 8, 15, "due to budget cuts", "after new funding"),
    (600, 25, 10, "through voluntary separation", "for critical positions"),
    (1500, 6, 20, "due to merger", "for the merged entity"),
    (400, 18, 14, "through redundancy", "for digital transformation"),
    (1100, 14, 9, "due to downsizing", "for customer service"),
    (800, 10, 16, "through natural attrition", "for IT department"),
]

for total, pct_reduce, pct_hire, reason_reduce, reason_hire in workforce_hard:
    reduced = int(total * pct_reduce / 100)
    after_reduction = total - reduced
    hired = int(after_reduction * pct_hire / 100)
    final = after_reduction + hired
    choices, answer = make_choices_numeric(final, "")
    add_q(
        "Hard",
        f"A company with {fmt_num(total)} employees reduced its workforce by {pct_reduce}% "
        f"{reason_reduce}. Later, it hired new employees equal to {pct_hire}% of the "
        f"remaining workforce {reason_hire}. How many employees does the company have now?",
        choices, answer,
        f"After reduction: {fmt_num(total)} − {pct_reduce}% = {fmt_num(total)} − {fmt_num(reduced)} "
        f"= {fmt_num(after_reduction)}. "
        f"New hires: {pct_hire}% of {fmt_num(after_reduction)} = {fmt_num(hired)}. "
        f"Final: {fmt_num(after_reduction)} + {fmt_num(hired)} = {fmt_num(final)}.",
        ["workforce", "percentage applications", "multi-step", "successive changes"]
    )

# Inventory / supply problems
inventory_hard = [
    (5000, 30, 20, "office supplies"),
    (8000, 25, 15, "medical supplies"),
    (3000, 40, 10, "construction materials"),
    (12000, 15, 25, "food supplies"),
    (6000, 35, 12, "cleaning supplies"),
    (4500, 20, 30, "educational materials"),
    (10000, 18, 22, "IT equipment"),
    (7500, 28, 8, "vehicle parts"),
    (2500, 45, 15, "laboratory chemicals"),
    (9000, 22, 18, "agricultural supplies"),
]

for stock, pct_used, pct_restock, item in inventory_hard[:5]:
    used = int(stock * pct_used / 100)
    after_use = stock - used
    restocked = int(after_use * pct_restock / 100)
    final_stock = after_use + restocked
    choices, answer = make_choices_numeric(final_stock, "")
    add_q(
        "Hard",
        f"A warehouse has {fmt_num(stock)} units of {item}. After a month, {pct_used}% "
        f"was consumed. Then {pct_restock}% of the remaining stock was replenished. "
        f"How many units are in stock now?",
        choices, answer,
        f"Used: {pct_used}% of {fmt_num(stock)} = {fmt_num(used)}. "
        f"Remaining: {fmt_num(stock)} − {fmt_num(used)} = {fmt_num(after_use)}. "
        f"Restocked: {pct_restock}% of {fmt_num(after_use)} = {fmt_num(restocked)}. "
        f"Final: {fmt_num(after_use)} + {fmt_num(restocked)} = {fmt_num(final_stock)}.",
        ["inventory", "percentage applications", "multi-step", "successive"]
    )


# Trim hard to exactly 200
hard_count = len([q for q in questions if q["difficulty"] == "Hard"])
if hard_count > 200:
    excess = hard_count - 200
    to_remove = []
    for i in range(len(questions) - 1, -1, -1):
        if questions[i]["difficulty"] == "Hard" and excess > 0:
            to_remove.append(i)
            excess -= 1
    for i in sorted(to_remove, reverse=True):
        questions.pop(i)

# ============================================================
# FILL TO EXACT COUNTS IF NEEDED
# ============================================================

easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
medium_count = len([q for q in questions if q["difficulty"] == "Medium"])
hard_count = len([q for q in questions if q["difficulty"] == "Hard"])

# Fill easy if under 200
extra_easy_scenarios = [
    ("A class has {total} students. {pct}% are male. How many male students are there?",
     "male students", "find the part"),
    ("A shipment contains {total} items. {pct}% passed quality control. How many passed?",
     "quality control", "find the part"),
    ("A library has {total} books. {pct}% are fiction. How many fiction books are there?",
     "library", "find the part"),
    ("A parking lot has {total} spaces. {pct}% are occupied. How many spaces are occupied?",
     "parking", "find the part"),
    ("A hospital has {total} beds. {pct}% are currently in use. How many beds are in use?",
     "hospital", "find the part"),
]

fill_idx = 0
while easy_count < 200:
    scenario = extra_easy_scenarios[fill_idx % len(extra_easy_scenarios)]
    total = random.choice([100, 150, 200, 250, 300, 400, 500, 600, 800, 1000])
    pct = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80])
    result = int(total * pct / 100)
    q_text = scenario[0].format(total=total, pct=pct)
    choices, answer = make_choices_numeric(result, "")
    add_q(
        "Easy", q_text, choices, answer,
        f"{pct}% of {total} = {pct}/100 × {total} = {result}.",
        ["percentage applications", scenario[1], scenario[2]]
    )
    easy_count += 1
    fill_idx += 1


# Fill medium if under 200
extra_medium_scenarios = [
    "A government project allocated ₱{budget:,} for supplies. If {pct}% was spent in Q1, how much remains for the rest of the year?",
    "An office has {total} employees. If {pct}% took leave this month, how many reported to work?",
    "A school collected ₱{budget:,} in fees. If {pct}% goes to faculty salaries, how much is left for operations?",
    "A department processed {total} applications. If {pct}% were approved, how many were denied?",
    "A training program has {total} participants. If {pct}% completed it, how many did not finish?",
]

while medium_count < 200:
    template = extra_medium_scenarios[fill_idx % len(extra_medium_scenarios)]
    total = random.choice([200, 350, 450, 550, 650, 750, 850, 950, 1100, 1250])
    budget = random.choice([100000, 250000, 500000, 750000, 1000000, 1500000])
    pct = random.choice([12, 18, 22, 28, 32, 38, 42, 48, 52, 58, 62, 68, 72, 78])

    if "budget" in template and "total" not in template:
        result = int(budget * (100 - pct) / 100)
        q_text = template.format(budget=budget, pct=pct)
        choices, answer = make_choices_numeric(result, "", "₱")
    elif "total" in template and "budget" not in template:
        result = int(total * (100 - pct) / 100)
        q_text = template.format(total=total, pct=pct)
        choices, answer = make_choices_numeric(result, "")
    else:
        result = int(budget * (100 - pct) / 100)
        q_text = template.format(budget=budget, total=total, pct=pct)
        choices, answer = make_choices_numeric(result, "", "₱")

    add_q(
        "Medium", q_text, choices, answer,
        f"Remaining = (100 − {pct})% = {100 - pct}%. "
        f"{100 - pct}% of the total = {fmt_num(result)}.",
        ["percentage applications", "remainder", "government"]
    )
    medium_count += 1
    fill_idx += 1

# Fill hard if under 200
extra_hard_scenarios = [
    (80000, 12, 8, 5, "salary with raise, tax increase, and savings goal"),
    (95000, 10, 15, 3, "income with bonus, investment, and emergency fund"),
    (60000, 18, 6, 10, "wage with overtime, deduction, and loan payment"),
    (110000, 8, 20, 4, "salary with allowance, rent increase, and insurance"),
    (72000, 14, 10, 7, "income with commission, tax, and retirement fund"),
]

while hard_count < 200:
    base, r1, r2, r3, desc = extra_hard_scenarios[fill_idx % len(extra_hard_scenarios)]
    # Vary the numbers slightly
    base = base + random.randint(-5000, 5000)
    step1 = int(base * (1 + r1 / 100))
    step2 = int(step1 * (1 - r2 / 100))
    step3 = int(step2 * (1 - r3 / 100))
    choices, answer = make_choices_numeric(step3, "", "₱")
    add_q(
        "Hard",
        f"An employee's base pay is ₱{fmt_num(base)}. After a {r1}% increase, "
        f"a {r2}% mandatory deduction is applied to the new amount, "
        f"then {r3}% of the remaining is set aside for savings. "
        f"What is the final disposable income?",
        choices, answer,
        f"After {r1}% increase: ₱{fmt_num(base)} × {1 + r1/100:.2f} = ₱{fmt_num(step1)}. "
        f"After {r2}% deduction: ₱{fmt_num(step1)} × {1 - r2/100:.2f} = ₱{fmt_num(step2)}. "
        f"After {r3}% savings: ₱{fmt_num(step2)} × {1 - r3/100:.2f} = ₱{fmt_num(step3)}.",
        ["financial", "percentage applications", "multi-step", "successive deductions"]
    )
    hard_count += 1
    fill_idx += 1


# ============================================================
# FINAL VALIDATION AND OUTPUT
# ============================================================

# Remove duplicate question texts (keep first occurrence)
seen_texts: set[str] = set()
deduped: list[dict] = []
for q in questions:
    if q["question"] not in seen_texts:
        seen_texts.add(q["question"])
        deduped.append(q)
questions = deduped

# Re-assign sequential IDs
for i, q in enumerate(questions, 1):
    q["id"] = i

# Validate counts
easy_final = len([q for q in questions if q["difficulty"] == "Easy"])
medium_final = len([q for q in questions if q["difficulty"] == "Medium"])
hard_final = len([q for q in questions if q["difficulty"] == "Hard"])

print(f"After dedup — Easy: {easy_final}, Medium: {medium_final}, Hard: {hard_final}")
print(f"Total: {len(questions)}")

# If dedup removed questions, we need to ensure we still have 600
# The fill loops above should have generated enough surplus
if len(questions) < 600:
    print(f"WARNING: Only {len(questions)} unique questions. Adding fillers...")
    # Add simple filler questions for any deficit
    deficit_easy = 200 - easy_final
    deficit_medium = 200 - medium_final
    deficit_hard = 200 - hard_final

    filler_idx = 0
    while deficit_easy > 0:
        filler_idx += 1
        total = random.choice([120, 180, 220, 280, 320, 380, 420, 480, 520, 580])
        pct = random.choice([5, 8, 12, 16, 22, 28, 32, 36, 44, 48, 52, 56, 64, 68, 72, 76, 84, 88, 92])
        result = int(total * pct / 100)
        q_text = f"A government office has {total} staff members. If {pct}% are assigned to fieldwork, how many work in the field?"
        if q_text not in seen_texts:
            choices, answer = make_choices_numeric(result, "")
            add_q("Easy", q_text, choices, answer,
                  f"{pct}% of {total} = {result}.",
                  ["percentage applications", "government", "find the part"])
            seen_texts.add(q_text)
            deficit_easy -= 1

    while deficit_medium > 0:
        filler_idx += 1
        total = random.choice([350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1250])
        pct = random.choice([14, 18, 23, 27, 33, 37, 43, 47, 53, 57, 63, 67, 73, 77, 83])
        result = int(total * pct / 100)
        remainder = total - result
        q_text = f"Out of {total} government transactions, {pct}% were processed online. How many were processed in person?"
        if q_text not in seen_texts:
            choices, answer = make_choices_numeric(remainder, "")
            add_q("Medium", q_text, choices, answer,
                  f"Online = {pct}% of {total} = {result}. In person = {total} − {result} = {remainder}.",
                  ["percentage applications", "government", "remainder"])
            seen_texts.add(q_text)
            deficit_medium -= 1

    while deficit_hard > 0:
        filler_idx += 1
        base = random.choice([45000, 55000, 65000, 75000, 85000, 95000, 105000])
        r1 = random.choice([6, 8, 10, 12, 14, 16, 18])
        r2 = random.choice([5, 7, 9, 11, 13, 15])
        step1 = int(base * (1 + r1 / 100))
        step2 = int(step1 * (1 - r2 / 100))
        q_text = (f"A project budget of ₱{fmt_num(base)} was increased by {r1}% for inflation. "
                  f"Then {r2}% of the adjusted budget was cut due to austerity measures. "
                  f"What is the final budget?")
        if q_text not in seen_texts:
            choices, answer = make_choices_numeric(step2, "", "₱")
            add_q("Hard", q_text, choices, answer,
                  f"After {r1}% increase: ₱{fmt_num(base)} × {1 + r1/100:.2f} = ₱{fmt_num(step1)}. "
                  f"After {r2}% cut: ₱{fmt_num(step1)} × {1 - r2/100:.2f} = ₱{fmt_num(step2)}.",
                  ["financial", "percentage applications", "multi-step", "budget"])
            seen_texts.add(q_text)
            deficit_hard -= 1

    # Re-assign IDs after fillers
    for i, q in enumerate(questions, 1):
        q["id"] = i

    easy_final = len([q for q in questions if q["difficulty"] == "Easy"])
    medium_final = len([q for q in questions if q["difficulty"] == "Medium"])
    hard_final = len([q for q in questions if q["difficulty"] == "Hard"])
    print(f"After fill — Easy: {easy_final}, Medium: {medium_final}, Hard: {hard_final}")
    print(f"Total: {len(questions)}")

assert easy_final == 200, f"Expected 200 Easy, got {easy_final}"
assert medium_final == 200, f"Expected 200 Medium, got {medium_final}"
assert hard_final == 200, f"Expected 200 Hard, got {hard_final}"
assert len(questions) == 600, f"Expected 600 total, got {len(questions)}"

# Final duplicate check
q_texts = [q["question"] for q in questions]
dupes = len(q_texts) - len(set(q_texts))
if dupes > 0:
    print(f"WARNING: {dupes} duplicate question texts remain")

# Verify all answers are in choices
for q in questions:
    assert q["answer"] in q["choices"], (
        f"Q{q['id']}: Answer '{q['answer']}' not in choices {q['choices']}"
    )

# Write output
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"\nWritten {len(questions)} questions to {OUTPUT_PATH}")
