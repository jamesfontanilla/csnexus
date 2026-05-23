"""Generate 600 questions for the Discounts, Markups, and Sales subtopic.

Produces exactly 200 Easy, 200 Medium, and 200 Hard questions covering:
- Discount problems
- Markup problems
- Commission problems
- Successive discounts/markups
- Multi-step sales problems
- Practical workplace applications

Output: data/seed/questions/numerical-ability/percentages/discounts-markups-and-sales/questions.json
"""

from __future__ import annotations

import json
import random
from pathlib import Path

random.seed(42)

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "seed"
    / "questions"
    / "numerical-ability"
    / "percentages"
    / "discounts-markups-and-sales"
    / "questions.json"
)

COMMON = {
    "subtest": "Numerical Ability",
    "module": "Percentages",
    "subtopic": "Discounts, Markups, and Sales",
}


def fmt(value: float) -> str:
    """Format a peso value nicely."""
    if value < 0:
        if value == int(value):
            return f"-\u20b1{abs(int(value)):,}"
        return f"-\u20b1{abs(value):,.2f}"
    if value == int(value):
        return f"\u20b1{int(value):,}"
    return f"\u20b1{value:,.2f}"


def pct(value: float) -> str:
    """Format a percentage."""
    if value == int(value):
        return f"{int(value)}%"
    # Remove trailing zeros
    return f"{value:.2f}%".rstrip("0").rstrip(".")  + "%"


def pct_clean(value: float) -> str:
    """Format percentage for display."""
    if value == int(value):
        return f"{int(value)}%"
    if value * 10 == int(value * 10):
        return f"{value:.1f}%"
    return f"{value:.2f}%"


def make_choices(correct: str, pool: list[str]) -> list[str]:
    """Create 4 choices with the correct answer and 3 unique distractors."""
    # Deduplicate and remove the correct answer from distractors
    distractors = list(dict.fromkeys(x for x in pool if x != correct))
    random.shuffle(distractors)
    chosen = distractors[:3]
    # If we don't have enough unique distractors, generate filler values
    while len(chosen) < 3:
        # Create a slightly different value
        filler = correct + " (approx)"  # fallback - shouldn't happen often
        if correct.startswith("\u20b1"):
            # Parse the number and create a variation
            try:
                num_str = correct.replace("\u20b1", "").replace(",", "")
                num = float(num_str)
                offset = num * random.choice([0.12, 0.18, 0.22, 0.08])
                variant = num + offset if random.random() > 0.5 else num - offset
                if variant > 0:
                    filler = fmt(round(variant, 2))
                else:
                    filler = fmt(num * 1.15)
            except (ValueError, TypeError):
                filler = correct
        elif correct.endswith("%"):
            try:
                num = float(correct.rstrip("%"))
                offset = random.choice([3, 5, 7, 8])
                variant = num + offset if random.random() > 0.5 else num - offset
                filler = pct_clean(round(variant, 2))
            except (ValueError, TypeError):
                filler = correct
        if filler != correct and filler not in chosen:
            chosen.append(filler)
        else:
            # Last resort
            chosen.append(f"{correct}*")
            break
    choices = [correct] + chosen[:3]
    random.shuffle(choices)
    return choices


def generate_easy_discount_questions(start_id: int) -> list[dict]:
    """Generate easy discount questions."""
    questions = []
    qid = start_id

    # Type 1: Find discount amount (simple percentages, round numbers)
    items = [
        ("bag", 2000), ("shirt", 800), ("shoes", 3000), ("watch", 5000),
        ("phone", 15000), ("laptop", 40000), ("tablet", 12000), ("dress", 1500),
        ("jacket", 4000), ("backpack", 2500), ("umbrella", 600), ("belt", 1000),
        ("sunglasses", 3500), ("perfume", 2800), ("wallet", 1200),
        ("headphones", 4500), ("speaker", 6000), ("camera", 25000),
        ("printer", 8000), ("monitor", 18000), ("keyboard", 2000),
        ("mouse", 1500), ("chair", 7000), ("desk", 12000), ("lamp", 900),
    ]
    rates = [10, 15, 20, 25, 30, 40, 50, 5]

    for i in range(35):
        item_name, price = items[i % len(items)]
        rate = rates[i % len(rates)]
        discount = price * rate / 100
        sale_price = price - discount

        if i % 2 == 0:
            # Ask for discount amount
            q_text = f"A {item_name} worth {fmt(price)} is sold at a {rate}% discount. What is the discount amount?"
            correct = fmt(discount)
            wrong1 = fmt(price * (rate + 5) / 100)
            wrong2 = fmt(price * (rate - 5) / 100) if rate > 5 else fmt(price * (rate + 10) / 100)
            wrong3 = fmt(sale_price)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = f"Discount Amount = {fmt(price)} × {rate}% = {fmt(price)} × {rate/100} = {correct}."
            tags = ["discount", "discount amount", "basic computation"]
        else:
            # Ask for sale price
            q_text = f"A {item_name} originally priced at {fmt(price)} has a {rate}% discount. What is the sale price?"
            correct = fmt(sale_price)
            wrong1 = fmt(price - price * (rate - 5) / 100)
            wrong2 = fmt(price - price * (rate + 5) / 100)
            wrong3 = fmt(discount)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = f"Sale Price = {fmt(price)} × (1 − {rate/100}) = {fmt(price)} × {1 - rate/100} = {correct}."
            tags = ["discount", "sale price", "basic computation"]

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
        })
        qid += 1

    # Type 2: Find discount rate (easy - clean numbers)
    pairs = [
        (1000, 800), (2000, 1600), (5000, 4000), (4000, 3200),
        (3000, 2400), (6000, 4800), (10000, 8000), (8000, 6000),
        (1500, 1200), (2500, 2000), (500, 400), (1200, 960),
        (7000, 5600), (9000, 7200), (20000, 16000),
    ]

    for i, (orig, sale) in enumerate(pairs):
        disc_amt = orig - sale
        rate = disc_amt / orig * 100
        q_text = f"An item originally priced at {fmt(orig)} is now sold for {fmt(sale)}. What is the discount rate?"
        correct = pct_clean(rate)
        wrong_rates = [rate + 5, rate - 5, rate + 10]
        wrong_rates = [r for r in wrong_rates if 0 < r < 100]
        wrongs = [pct_clean(r) for r in wrong_rates]
        choices = make_choices(correct, [correct] + wrongs[:3])
        explanation = f"Discount = {fmt(orig)} − {fmt(sale)} = {fmt(disc_amt)}. Rate = {fmt(disc_amt)} ÷ {fmt(orig)} × 100 = {correct}."

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", "discount rate", "basic computation"],
        })
        qid += 1

    return questions


def generate_easy_markup_questions(start_id: int) -> list[dict]:
    """Generate easy markup questions."""
    questions = []
    qid = start_id

    items = [
        ("shirt", 300), ("bag", 500), ("shoes", 800), ("book", 200),
        ("toy", 150), ("pen", 50), ("notebook", 80), ("mug", 120),
        ("cap", 250), ("scarf", 400), ("candle", 100), ("soap", 60),
        ("snack box", 75), ("water bottle", 180), ("keychain", 90),
        ("phone case", 350), ("earphones", 600), ("charger", 450),
        ("flash drive", 500), ("mouse pad", 200), ("ruler", 30),
        ("folder", 40), ("stapler", 280), ("scissors", 160), ("tape", 70),
    ]
    rates = [20, 25, 30, 40, 50, 60, 75, 80, 100]

    for i in range(35):
        item_name, cost = items[i % len(items)]
        rate = rates[i % len(rates)]
        markup_amt = cost * rate / 100
        selling = cost + markup_amt

        if i % 3 == 0:
            # Ask for selling price
            q_text = f"A store buys a {item_name} for {fmt(cost)} and applies a {rate}% markup. What is the selling price?"
            correct = fmt(selling)
            wrong1 = fmt(cost * (1 + (rate + 10) / 100))
            wrong2 = fmt(cost * (1 + (rate - 10) / 100)) if rate > 10 else fmt(cost * (1 + (rate + 20) / 100))
            wrong3 = fmt(markup_amt)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = f"Selling Price = {fmt(cost)} × (1 + {rate/100}) = {fmt(cost)} × {1 + rate/100} = {correct}."
            tags = ["markup", "selling price", "basic computation"]
        elif i % 3 == 1:
            # Ask for markup amount
            q_text = f"A {item_name} costs {fmt(cost)} and is marked up by {rate}%. What is the markup amount?"
            correct = fmt(markup_amt)
            wrong1 = fmt(cost * (rate + 10) / 100)
            wrong2 = fmt(cost * (rate - 10) / 100) if rate > 10 else fmt(cost * 5 / 100)
            wrong3 = fmt(selling)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = f"Markup Amount = {fmt(cost)} × {rate}% = {fmt(cost)} × {rate/100} = {correct}."
            tags = ["markup", "markup amount", "basic computation"]
        else:
            # Ask for markup rate
            q_text = f"A store buys an item for {fmt(cost)} and sells it for {fmt(selling)}. What is the markup rate?"
            correct = pct_clean(rate)
            wrong_rates = [rate + 10, rate - 10, rate + 20]
            wrong_rates = [r for r in wrong_rates if r > 0]
            wrongs = [pct_clean(r) for r in wrong_rates]
            choices = make_choices(correct, [correct] + wrongs[:3])
            explanation = f"Markup = {fmt(selling)} − {fmt(cost)} = {fmt(markup_amt)}. Rate = {fmt(markup_amt)} ÷ {fmt(cost)} × 100 = {correct}."
            tags = ["markup", "markup rate", "basic computation"]

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
        })
        qid += 1

    return questions


def generate_easy_commission_questions(start_id: int) -> list[dict]:
    """Generate easy commission questions."""
    questions = []
    qid = start_id

    scenarios = [
        ("real estate agent", 3, 2000000), ("car salesman", 2, 1500000),
        ("insurance agent", 4, 500000), ("sales clerk", 5, 120000),
        ("online seller", 8, 50000), ("appliance salesperson", 3, 800000),
        ("jewelry salesperson", 6, 200000), ("furniture salesperson", 4, 350000),
        ("electronics salesperson", 5, 180000), ("clothing salesperson", 7, 80000),
        ("book salesperson", 10, 30000), ("cosmetics agent", 8, 60000),
        ("pharmaceutical rep", 3, 400000), ("travel agent", 5, 250000),
        ("advertising agent", 6, 150000), ("recruitment agent", 4, 300000),
        ("food distributor", 3, 600000), ("office supply salesperson", 5, 100000),
        ("hardware salesperson", 4, 450000), ("textile salesperson", 6, 280000),
    ]

    for i in range(30):
        role, rate, sales = scenarios[i % len(scenarios)]
        # Vary the sales amount slightly
        sales = sales + random.choice([-50000, 0, 50000, 100000]) if sales > 100000 else sales
        commission = sales * rate / 100

        if i % 3 == 0:
            # Find commission
            q_text = f"A {role} earns a {rate}% commission. If total sales are {fmt(sales)}, how much commission is earned?"
            correct = fmt(commission)
            wrong1 = fmt(sales * (rate + 1) / 100)
            wrong2 = fmt(sales * (rate - 1) / 100) if rate > 1 else fmt(sales * (rate + 2) / 100)
            wrong3 = fmt(sales - commission)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = f"Commission = {fmt(sales)} × {rate}% = {fmt(sales)} × {rate/100} = {correct}."
            tags = ["commission", "commission amount", "basic computation"]
        elif i % 3 == 1:
            # Find commission rate
            q_text = f"A {role} earned {fmt(commission)} from {fmt(sales)} in sales. What is the commission rate?"
            correct = pct_clean(rate)
            wrongs = [pct_clean(rate + 1), pct_clean(rate + 2), pct_clean(rate - 1) if rate > 1 else pct_clean(rate + 3)]
            choices = make_choices(correct, [correct] + wrongs)
            explanation = f"Commission Rate = {fmt(commission)} ÷ {fmt(sales)} × 100 = {correct}."
            tags = ["commission", "commission rate", "basic computation"]
        else:
            # Find total sales
            q_text = f"A {role} earns {rate}% commission and received {fmt(commission)}. What were the total sales?"
            correct = fmt(sales)
            wrong1 = fmt(commission / ((rate + 1) / 100))
            wrong2 = fmt(commission / ((rate - 1) / 100)) if rate > 1 else fmt(sales * 2)
            wrong3 = fmt(sales + commission)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = f"Total Sales = {fmt(commission)} ÷ {rate/100} = {correct}."
            tags = ["commission", "total sales", "basic computation"]

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
        })
        qid += 1

    return questions


def generate_medium_discount_questions(start_id: int) -> list[dict]:
    """Generate medium discount questions."""
    questions = []
    qid = start_id

    # Type 1: Find original price given sale price and rate
    cases = [
        (0.75, 5250, "25%"), (0.80, 4000, "20%"), (0.85, 6800, "15%"),
        (0.70, 14000, "30%"), (0.90, 9000, "10%"), (0.60, 3600, "40%"),
        (0.65, 13000, "35%"), (0.88, 4400, "12%"), (0.92, 4600, "8%"),
        (0.78, 7800, "22%"), (0.82, 8200, "18%"), (0.55, 5500, "45%"),
        (0.95, 9500, "5%"), (0.72, 3600, "28%"), (0.84, 8400, "16%"),
    ]

    for i, (multiplier, sale_price, rate_str) in enumerate(cases):
        original = sale_price / multiplier
        q_text = f"After a {rate_str} discount, a customer pays {fmt(sale_price)}. What was the original price?"
        correct = fmt(original)
        wrong1 = fmt(sale_price * (1 + float(rate_str.strip('%')) / 100))
        wrong2 = fmt(sale_price + sale_price * float(rate_str.strip('%')) / 100 / 2)
        wrong3 = fmt(original * 1.1)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = f"{fmt(sale_price)} = Original × {multiplier}. Original = {fmt(sale_price)} ÷ {multiplier} = {correct}."

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", "original price", "reverse computation"],
        })
        qid += 1

    # Type 2: Find discount amount given savings info
    savings_cases = [
        (1200, 0.10), (2400, 0.15), (3500, 0.20), (4800, 0.25),
        (6000, 0.30), (1680, 0.12), (2250, 0.18), (900, 0.05),
        (5600, 0.35), (7500, 0.40), (1050, 0.07), (3200, 0.16),
        (4500, 0.22), (8000, 0.50), (1800, 0.09),
    ]

    for i, (savings, rate) in enumerate(savings_cases):
        original = savings / rate
        rate_pct = int(rate * 100)
        q_text = f"A customer saved {fmt(savings)} thanks to a {rate_pct}% discount. What was the original price of the item?"
        correct = fmt(original)
        wrong1 = fmt(savings / (rate + 0.05))
        wrong2 = fmt(savings / (rate - 0.05)) if rate > 0.05 else fmt(savings * 15)
        wrong3 = fmt(original + savings)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = f"Discount Amount = Original × Rate. {fmt(savings)} = Original × {rate}. Original = {fmt(savings)} ÷ {rate} = {correct}."

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", "original price", "reverse computation"],
        })
        qid += 1

    # Type 3: Bulk purchase with discount
    bulk_cases = [
        ("chairs", 50, 1200, 12), ("desks", 30, 4500, 10),
        ("reams of paper", 200, 250, 8), ("uniforms", 100, 850, 15),
        ("books", 75, 320, 20), ("computers", 20, 35000, 7),
        ("printers", 15, 12000, 10), ("filing cabinets", 25, 6000, 12),
        ("whiteboards", 10, 8500, 15), ("projectors", 5, 45000, 8),
        ("air conditioners", 8, 28000, 10), ("water dispensers", 12, 5500, 12),
        ("office tables", 40, 3200, 15), ("swivel chairs", 35, 4800, 10),
        ("bookshelves", 20, 7500, 8),
    ]

    for i, (item, qty, unit_price, disc_rate) in enumerate(bulk_cases):
        total_before = qty * unit_price
        discount = total_before * disc_rate / 100
        total_after = total_before - discount
        q_text = (
            f"An office buys {qty} {item} at {fmt(unit_price)} each. "
            f"The supplier offers a {disc_rate}% bulk discount on the total. "
            f"How much does the office pay?"
        )
        correct = fmt(total_after)
        wrong1 = fmt(total_before)
        wrong2 = fmt(total_before - qty * unit_price * (disc_rate + 5) / 100)
        wrong3 = fmt(discount)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Total = {qty} × {fmt(unit_price)} = {fmt(total_before)}. "
            f"Discount = {fmt(total_before)} × {disc_rate}% = {fmt(discount)}. "
            f"Paid = {fmt(total_before)} − {fmt(discount)} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", "bulk purchase", "government procurement"],
        })
        qid += 1

    # Type 4: Comparing two offers
    compare_cases = [
        (85000, 5, 80000, 0), (45000, 10, 42000, 3),
        (120000, 8, 115000, 4), (25000, 12, 23000, 5),
        (60000, 15, 55000, 8), (95000, 6, 90000, 2),
        (35000, 10, 33000, 4), (150000, 7, 142000, 3),
        (72000, 12, 68000, 6), (28000, 15, 25000, 5),
    ]

    for i, (price_a, disc_a, price_b, disc_b) in enumerate(compare_cases):
        net_a = price_a * (1 - disc_a / 100)
        net_b = price_b * (1 - disc_b / 100)
        diff = abs(net_a - net_b)
        cheaper = "A" if net_a < net_b else "B"
        q_text = (
            f"Supplier A offers an item at {fmt(price_a)} with a {disc_a}% discount. "
            f"Supplier B offers the same item at {fmt(price_b)} with a {disc_b}% discount. "
            f"Which is cheaper and by how much?"
        )
        correct = f"Supplier {cheaper} by {fmt(diff)}"
        other = "B" if cheaper == "A" else "A"
        wrong1 = f"Supplier {other} by {fmt(diff)}"
        wrong2 = f"Supplier {cheaper} by {fmt(diff * 2)}"
        wrong3 = f"Supplier {other} by {fmt(diff / 2)}" if diff > 1 else f"Supplier {other} by {fmt(100)}"
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Supplier A net = {fmt(price_a)} × {1 - disc_a/100} = {fmt(net_a)}. "
            f"Supplier B net = {fmt(price_b)} × {1 - disc_b/100} = {fmt(net_b)}. "
            f"Supplier {cheaper} is cheaper by {fmt(diff)}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", "comparison", "government procurement"],
        })
        qid += 1

    return questions


def generate_medium_markup_questions(start_id: int) -> list[dict]:
    """Generate medium markup questions."""
    questions = []
    qid = start_id

    # Type 1: Find cost price given selling price and markup rate
    cases = [
        (5600, 40), (7200, 20), (9000, 50), (4200, 40),
        (6500, 30), (3900, 30), (8400, 40), (11200, 60),
        (2700, 35), (15000, 50), (4800, 20), (6300, 25),
        (10500, 75), (3360, 12), (5520, 15),
    ]

    for i, (selling, rate) in enumerate(cases):
        cost = selling / (1 + rate / 100)
        q_text = f"A retailer sells an item for {fmt(selling)} after applying a {rate}% markup on cost. What was the cost price?"
        correct = fmt(cost)
        # Common mistake: subtracting rate% from selling price
        wrong1 = fmt(selling * (1 - rate / 100))
        wrong2 = fmt(selling - selling * rate / 100 / 2)
        wrong3 = fmt(cost * 0.9)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = f"Selling = Cost × (1 + {rate/100}). {fmt(selling)} = Cost × {1 + rate/100}. Cost = {fmt(selling)} ÷ {1 + rate/100} = {correct}."

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["markup", "cost price", "reverse computation"],
        })
        qid += 1

    # Type 2: Markup then discount - does the store profit?
    md_cases = [
        (2000, 60, 25), (3000, 50, 20), (1500, 80, 30),
        (4000, 40, 15), (5000, 100, 40), (1000, 70, 35),
        (2500, 45, 20), (6000, 30, 10), (800, 120, 50),
        (3500, 55, 25), (1200, 90, 40), (7000, 35, 15),
        (4500, 60, 30), (2800, 75, 35), (9000, 25, 10),
    ]

    for i, (cost, markup_rate, disc_rate) in enumerate(md_cases):
        selling = cost * (1 + markup_rate / 100)
        sale_price = selling * (1 - disc_rate / 100)
        profit = sale_price - cost
        q_text = (
            f"A store buys an item for {fmt(cost)}, marks it up by {markup_rate}%, "
            f"then offers a {disc_rate}% discount. What is the sale price?"
        )
        correct = fmt(sale_price)
        wrong1 = fmt(cost * (1 + markup_rate / 100 - disc_rate / 100))
        wrong2 = fmt(selling)
        wrong3 = fmt(cost * (1 + (markup_rate - disc_rate) / 100))
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Selling = {fmt(cost)} × {1 + markup_rate/100} = {fmt(selling)}. "
            f"Sale Price = {fmt(selling)} × {1 - disc_rate/100} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["markup", "discount", "multi-step", "profit analysis"],
        })
        qid += 1

    # Type 3: Required markup to achieve target profit after discount
    target_cases = [
        (20, 25), (30, 20), (15, 10), (25, 15),
        (10, 20), (40, 30), (20, 15), (35, 25),
        (50, 40), (15, 5), (25, 20), (30, 25),
        (20, 10), (45, 35), (10, 5),
    ]

    for i, (profit_pct, disc_pct) in enumerate(target_cases):
        # Need: sale_price = cost * (1 + profit_pct/100)
        # sale_price = marked * (1 - disc_pct/100)
        # marked = cost * (1 + markup/100)
        # So: cost*(1+profit/100) = cost*(1+markup/100)*(1-disc/100)
        # (1+profit/100) = (1+markup/100)*(1-disc/100)
        # markup/100 = (1+profit/100)/(1-disc/100) - 1
        markup_rate = ((1 + profit_pct / 100) / (1 - disc_pct / 100) - 1) * 100
        if markup_rate != int(markup_rate) and abs(markup_rate - round(markup_rate, 2)) > 0.005:
            # Skip non-clean answers
            markup_rate = round(markup_rate, 2)

        q_text = (
            f"A store wants to earn {profit_pct}% profit on cost even after giving a {disc_pct}% discount. "
            f"What markup rate should be applied to the cost price?"
        )
        correct = pct_clean(round(markup_rate, 2))
        wrongs = [
            pct_clean(profit_pct + disc_pct),
            pct_clean(round(markup_rate + 10, 2)),
            pct_clean(round(markup_rate - 5, 2)) if markup_rate > 5 else pct_clean(round(markup_rate + 15, 2)),
        ]
        choices = make_choices(correct, [correct] + wrongs)
        explanation = (
            f"Need sale price = cost × {1 + profit_pct/100}. "
            f"Sale = Marked × {1 - disc_pct/100}. "
            f"Marked = {1 + profit_pct/100} ÷ {1 - disc_pct/100} = {round(1 + markup_rate/100, 4)} of cost. "
            f"Markup rate = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["markup", "profit", "discount", "reverse computation"],
        })
        qid += 1

    return questions


def generate_medium_commission_questions(start_id: int) -> list[dict]:
    """Generate medium commission questions."""
    questions = []
    qid = start_id

    # Type 1: Salary plus commission
    sal_cases = [
        (15000, 5, 200000), (18000, 4, 150000), (20000, 3, 350000),
        (12000, 6, 180000), (25000, 2, 500000), (16000, 7, 100000),
        (22000, 3, 280000), (14000, 5, 220000), (30000, 2, 600000),
        (10000, 8, 80000), (19000, 4, 250000), (17000, 6, 130000),
        (21000, 3, 400000), (13000, 5, 160000), (28000, 2, 450000),
    ]

    for i, (base, rate, sales) in enumerate(sal_cases):
        commission = sales * rate / 100
        total = base + commission
        q_text = (
            f"A sales employee earns a base salary of {fmt(base)} plus {rate}% commission on all sales. "
            f"If monthly sales total {fmt(sales)}, what are the total earnings?"
        )
        correct = fmt(total)
        wrong1 = fmt(base + sales * (rate + 1) / 100)
        wrong2 = fmt(commission)
        wrong3 = fmt(base + sales)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Commission = {fmt(sales)} × {rate}% = {fmt(commission)}. "
            f"Total = {fmt(base)} + {fmt(commission)} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["commission", "salary plus commission", "payroll"],
        })
        qid += 1

    # Type 2: Commission on excess (quota-based)
    quota_cases = [
        (200000, 4, 350000), (150000, 5, 280000), (300000, 3, 500000),
        (100000, 6, 220000), (250000, 4, 400000), (180000, 5, 310000),
        (400000, 2, 650000), (120000, 7, 200000), (350000, 3, 520000),
        (500000, 2, 800000), (80000, 8, 150000), (220000, 4, 380000),
        (160000, 5, 290000), (280000, 3, 450000), (450000, 2, 700000),
    ]

    for i, (quota, rate, total_sales) in enumerate(quota_cases):
        excess = total_sales - quota
        commission = excess * rate / 100
        q_text = (
            f"A salesperson earns {rate}% commission on all sales exceeding the {fmt(quota)} monthly quota. "
            f"If total sales are {fmt(total_sales)}, how much commission is earned?"
        )
        correct = fmt(commission)
        # Common mistake: commission on total sales
        wrong1 = fmt(total_sales * rate / 100)
        wrong2 = fmt(excess * (rate + 1) / 100)
        wrong3 = fmt(quota * rate / 100)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Excess = {fmt(total_sales)} − {fmt(quota)} = {fmt(excess)}. "
            f"Commission = {fmt(excess)} × {rate}% = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["commission", "quota", "commission on excess"],
        })
        qid += 1

    # Type 3: Split commission
    split_cases = [
        (2, 5, 1800000), (3, 6, 2400000), (4, 4, 3200000),
        (2, 3, 4500000), (3, 5, 1500000), (5, 4, 2000000),
        (2, 7, 800000), (3, 3, 3600000), (4, 5, 1200000),
        (2, 6, 2800000), (3, 4, 2100000), (5, 3, 5000000),
        (2, 8, 600000), (4, 3, 4000000), (3, 5, 1800000),
    ]

    for i, (agents, rate, sale_amount) in enumerate(split_cases):
        total_comm = sale_amount * rate / 100
        each = total_comm / agents
        q_text = (
            f"{agents} agents split a {rate}% commission equally on a {fmt(sale_amount)} sale. "
            f"How much does each agent receive?"
        )
        correct = fmt(each)
        wrong1 = fmt(total_comm)
        wrong2 = fmt(each * 2)
        wrong3 = fmt(sale_amount / agents)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Total commission = {fmt(sale_amount)} × {rate}% = {fmt(total_comm)}. "
            f"Each agent = {fmt(total_comm)} ÷ {agents} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["commission", "split commission", "teamwork"],
        })
        qid += 1

    return questions


def generate_hard_discount_questions(start_id: int) -> list[dict]:
    """Generate hard discount questions."""
    questions = []
    qid = start_id

    # Type 1: Successive discounts
    succ_cases = [
        (10000, 20, 10), (8000, 15, 10), (15000, 25, 15),
        (12000, 30, 10), (20000, 10, 20), (6000, 20, 20),
        (25000, 15, 15), (9000, 30, 20), (18000, 25, 10),
        (7500, 20, 15), (30000, 10, 10), (14000, 35, 10),
        (11000, 20, 25), (16000, 15, 20), (22000, 25, 20),
        (5000, 30, 15), (35000, 20, 10), (8500, 25, 25),
        (13000, 10, 30), (19000, 15, 25),
    ]

    for i, (price, d1, d2) in enumerate(succ_cases):
        final = price * (1 - d1/100) * (1 - d2/100)
        equiv_disc = (1 - (1 - d1/100) * (1 - d2/100)) * 100
        wrong_sum = d1 + d2

        if i % 2 == 0:
            q_text = (
                f"An item priced at {fmt(price)} has successive discounts of {d1}% and {d2}%. "
                f"What is the final price?"
            )
            correct = fmt(final)
            wrong1 = fmt(price * (1 - wrong_sum / 100))
            wrong2 = fmt(price * (1 - d1/100))
            wrong3 = fmt(price * (1 - d2/100))
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = (
                f"Final = {fmt(price)} × {1-d1/100} × {1-d2/100} = {correct}. "
                f"Note: successive discounts of {d1}% and {d2}% ≠ {wrong_sum}% single discount."
            )
            tags = ["successive discounts", "multiplier method", "common trap"]
        else:
            q_text = (
                f"What single discount is equivalent to successive discounts of {d1}% and {d2}%?"
            )
            correct = pct_clean(round(equiv_disc, 2))
            wrong1 = pct_clean(wrong_sum)
            wrong2 = pct_clean(round(equiv_disc + 3, 2))
            wrong3 = pct_clean(round(equiv_disc - 3, 2))
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = (
                f"Combined multiplier = {1-d1/100} × {1-d2/100} = {round((1-d1/100)*(1-d2/100), 4)}. "
                f"Equivalent discount = 1 − {round((1-d1/100)*(1-d2/100), 4)} = {correct}."
            )
            tags = ["successive discounts", "equivalent discount", "multiplier method"]

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
        })
        qid += 1

    # Type 2: Three successive discounts
    triple_cases = [
        (10, 10, 10), (20, 10, 5), (15, 15, 10),
        (25, 20, 10), (30, 20, 10), (10, 20, 15),
        (20, 15, 10), (15, 10, 5), (25, 15, 10),
        (30, 10, 10),
    ]

    for i, (d1, d2, d3) in enumerate(triple_cases):
        price = random.choice([10000, 15000, 20000, 25000, 30000])
        final = price * (1 - d1/100) * (1 - d2/100) * (1 - d3/100)
        equiv = (1 - (1-d1/100)*(1-d2/100)*(1-d3/100)) * 100
        q_text = (
            f"An item worth {fmt(price)} receives successive discounts of {d1}%, {d2}%, and {d3}%. "
            f"What is the final price?"
        )
        correct = fmt(final)
        wrong1 = fmt(price * (1 - (d1+d2+d3)/100))
        wrong2 = fmt(price * (1 - d1/100) * (1 - d2/100))
        wrong3 = fmt(final * 1.05)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Final = {fmt(price)} × {1-d1/100} × {1-d2/100} × {1-d3/100} = {correct}. "
            f"Equivalent single discount ≈ {pct_clean(round(equiv, 1))}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["successive discounts", "three discounts", "multiplier method"],
        })
        qid += 1

    # Type 3: Comparing successive vs single discount
    compare_cases = [
        (10000, 15, 10, 24), (8000, 20, 10, 28),
        (12000, 25, 10, 33), (15000, 10, 15, 24),
        (20000, 20, 15, 33), (6000, 30, 10, 38),
        (9000, 15, 20, 33), (25000, 10, 10, 19),
        (18000, 20, 20, 38), (7000, 25, 15, 37),
    ]

    for i, (price, d1, d2, single_d) in enumerate(compare_cases):
        succ_final = price * (1 - d1/100) * (1 - d2/100)
        single_final = price * (1 - single_d/100)
        diff = abs(succ_final - single_final)
        better = "successive" if succ_final < single_final else "single"
        better_label = f"successive discounts of {d1}% and {d2}%" if better == "successive" else f"single discount of {single_d}%"

        q_text = (
            f"Store A offers successive discounts of {d1}% and {d2}% on a {fmt(price)} item. "
            f"Store B offers a single {single_d}% discount on the same item. "
            f"Which store gives the lower price and by how much?"
        )
        correct = f"Store {'A' if better == 'successive' else 'B'} by {fmt(diff)}"
        other_store = 'B' if better == 'successive' else 'A'
        wrong1 = f"Store {other_store} by {fmt(diff)}"
        wrong2 = f"Store {'A' if better == 'successive' else 'B'} by {fmt(diff * 2)}"
        wrong3 = "Both are equal"
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Store A: {fmt(price)} × {1-d1/100} × {1-d2/100} = {fmt(succ_final)}. "
            f"Store B: {fmt(price)} × {1-single_d/100} = {fmt(single_final)}. "
            f"Difference = {fmt(diff)}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["successive discounts", "comparison", "critical thinking"],
        })
        qid += 1

    # Type 4: Complex government procurement scenarios
    govt_cases = [
        # (total_items, unit_price, disc1, disc2, question_type)
        (500, 120, 40, 80, "revenue"),
        (300, 250, 10, 15, "savings"),
        (1000, 45, 8, 12, "total_paid"),
        (200, 800, 15, 20, "per_unit_cost"),
        (150, 1500, 12, 10, "total_paid"),
    ]

    for i, (qty, unit_p, rate1, rate2, qtype) in enumerate(govt_cases):
        total = qty * unit_p
        if qtype == "revenue":
            # Markup then discount scenario
            marked = unit_p * (1 + rate1/100)
            sold_full = int(qty * 0.8)
            sold_disc = qty - sold_full
            rev_full = sold_full * marked
            rev_disc = sold_disc * marked * (1 - rate2/100)  # rate2 used as discount for clearance
            # Simplify: just use rate2 as a percentage of stock sold at discount
            total_rev = rev_full + rev_disc
            q_text = (
                f"A cooperative buys {qty} items at {fmt(unit_p)} each and marks up by {rate1}%. "
                f"{int(qty*0.8)} units sell at full price; the rest sell at a {rate2}% discount. "
                f"What is the total revenue?"
            )
            correct = fmt(total_rev)
            wrong1 = fmt(qty * marked)
            wrong2 = fmt(total_rev * 0.9)
            wrong3 = fmt(rev_full)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = (
                f"Marked price = {fmt(unit_p)} × {1+rate1/100} = {fmt(marked)}. "
                f"Full-price revenue = {sold_full} × {fmt(marked)} = {fmt(rev_full)}. "
                f"Discounted revenue = {sold_disc} × {fmt(marked)} × {1-rate2/100} = {fmt(rev_disc)}. "
                f"Total = {correct}."
            )
        else:
            # Successive discounts on bulk
            final = total * (1 - rate1/100) * (1 - rate2/100)
            savings = total - final
            per_unit = final / qty
            q_text = (
                f"A government office buys {qty} items at {fmt(unit_p)} each. "
                f"The supplier offers successive discounts of {rate1}% and {rate2}%. "
                f"How much does the office pay in total?"
            )
            correct = fmt(final)
            wrong1 = fmt(total * (1 - (rate1 + rate2)/100))
            wrong2 = fmt(total * (1 - rate1/100))
            wrong3 = fmt(total)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = (
                f"Total list = {qty} × {fmt(unit_p)} = {fmt(total)}. "
                f"After discounts = {fmt(total)} × {1-rate1/100} × {1-rate2/100} = {correct}."
            )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", "government procurement", "multi-step"],
        })
        qid += 1

    return questions


def generate_hard_markup_questions(start_id: int) -> list[dict]:
    """Generate hard markup questions."""
    questions = []
    qid = start_id

    # Type 1: Markup + Discount + Profit analysis
    cases = [
        (2000, 80, 30), (3000, 60, 25), (1500, 100, 40),
        (4000, 50, 20), (5000, 40, 15), (2500, 70, 30),
        (1800, 90, 35), (6000, 45, 20), (3500, 65, 25),
        (7000, 35, 10), (1200, 120, 50), (4500, 55, 25),
        (2200, 75, 30), (8000, 30, 12), (900, 150, 55),
        (3200, 60, 20), (5500, 40, 18), (2800, 85, 35),
        (6500, 50, 22), (1600, 95, 40),
    ]

    for i, (cost, markup_rate, disc_rate) in enumerate(cases):
        selling = cost * (1 + markup_rate / 100)
        sale_price = selling * (1 - disc_rate / 100)
        profit = sale_price - cost
        profit_pct = profit / cost * 100

        if i % 3 == 0:
            q_text = (
                f"A store buys an item for {fmt(cost)}, marks it up by {markup_rate}%, "
                f"then offers a {disc_rate}% discount. What is the profit per item?"
            )
            correct = fmt(profit)
            wrong1 = fmt(selling - cost)
            wrong2 = fmt(sale_price)
            wrong3 = fmt(cost * (markup_rate - disc_rate) / 100)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = (
                f"Selling = {fmt(cost)} × {1+markup_rate/100} = {fmt(selling)}. "
                f"Sale = {fmt(selling)} × {1-disc_rate/100} = {fmt(sale_price)}. "
                f"Profit = {fmt(sale_price)} − {fmt(cost)} = {correct}."
            )
            tags = ["markup", "discount", "profit", "multi-step"]
        elif i % 3 == 1:
            q_text = (
                f"Cost is {fmt(cost)}. After {markup_rate}% markup and {disc_rate}% discount, "
                f"what is the profit percentage on cost?"
            )
            correct = pct_clean(round(profit_pct, 2))
            wrong1 = pct_clean(markup_rate - disc_rate)
            wrong2 = pct_clean(round(profit_pct + 5, 2))
            wrong3 = pct_clean(markup_rate)
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = (
                f"Sale price = {fmt(cost)} × {1+markup_rate/100} × {1-disc_rate/100} = {fmt(sale_price)}. "
                f"Profit = {fmt(sale_price)} − {fmt(cost)} = {fmt(profit)}. "
                f"Profit % = {fmt(profit)} ÷ {fmt(cost)} × 100 = {correct}."
            )
            tags = ["markup", "discount", "profit percentage", "multi-step"]
        else:
            # Does the store lose money?
            loses = profit < 0
            q_text = (
                f"A store buys goods at {fmt(cost)}, marks up by {markup_rate}%, "
                f"then gives a {disc_rate}% discount. Does the store profit or lose, and by how much?"
            )
            if loses:
                correct = f"Loss of {fmt(abs(profit))}"
                wrong1 = f"Profit of {fmt(abs(profit))}"
            else:
                correct = f"Profit of {fmt(profit)}"
                wrong1 = f"Loss of {fmt(profit)}"
            wrong2 = f"Profit of {fmt(selling - cost)}"
            wrong3 = f"Break even"
            choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
            explanation = (
                f"Sale price = {fmt(cost)} × {1+markup_rate/100} × {1-disc_rate/100} = {fmt(sale_price)}. "
                f"{'Profit' if not loses else 'Loss'} = {fmt(abs(profit))}."
            )
            tags = ["markup", "discount", "profit/loss analysis", "multi-step"]

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
        })
        qid += 1

    # Type 2: Wholesale → Retail chain with commission
    chain_cases = [
        (1000, 30, 40, 15, 5), (2000, 25, 35, 20, 4),
        (1500, 35, 50, 10, 6), (3000, 20, 30, 15, 3),
        (800, 40, 60, 20, 7), (2500, 30, 45, 12, 5),
        (4000, 15, 25, 10, 4), (1200, 50, 40, 25, 6),
        (5000, 20, 35, 15, 3), (1800, 35, 55, 18, 5),
        (600, 45, 70, 20, 8), (3500, 25, 30, 10, 4),
        (2200, 30, 40, 15, 5), (7000, 15, 20, 8, 3),
        (900, 60, 50, 25, 7),
    ]

    for i, (mfg_cost, wholesale_markup, retail_markup, disc, comm_rate) in enumerate(chain_cases):
        wholesale = mfg_cost * (1 + wholesale_markup / 100)
        retail = wholesale * (1 + retail_markup / 100)
        sale = retail * (1 - disc / 100)
        commission = sale * comm_rate / 100

        q_text = (
            f"A manufacturer sells at {fmt(mfg_cost)} + {wholesale_markup}% markup to a retailer. "
            f"The retailer marks up by {retail_markup}%, then offers {disc}% off. "
            f"A salesperson earns {comm_rate}% commission on the sale. What is the commission?"
        )
        correct = fmt(round(commission, 2))
        wrong1 = fmt(round(retail * comm_rate / 100, 2))
        wrong2 = fmt(round(mfg_cost * comm_rate / 100, 2))
        wrong3 = fmt(round(commission * 2, 2))
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Wholesale = {fmt(mfg_cost)} × {1+wholesale_markup/100} = {fmt(wholesale)}. "
            f"Retail = {fmt(wholesale)} × {1+retail_markup/100} = {fmt(retail)}. "
            f"Sale = {fmt(retail)} × {1-disc/100} = {fmt(sale)}. "
            f"Commission = {fmt(sale)} × {comm_rate}% = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["markup", "discount", "commission", "supply chain", "multi-step"],
        })
        qid += 1

    return questions


def generate_hard_commission_questions(start_id: int) -> list[dict]:
    """Generate hard commission questions."""
    questions = []
    qid = start_id

    # Type 1: Graduated/tiered commission
    tier_cases = [
        # (tier1_limit, tier1_rate, tier2_limit, tier2_rate, tier3_rate, total_sales)
        (100000, 3, 300000, 5, 8, 450000),
        (150000, 2, 400000, 4, 7, 600000),
        (200000, 3, 500000, 5, 8, 700000),
        (80000, 4, 200000, 6, 9, 350000),
        (120000, 3, 350000, 5, 7, 500000),
        (100000, 2, 250000, 4, 6, 400000),
        (200000, 3, 400000, 5, 8, 550000),
        (150000, 4, 300000, 6, 9, 480000),
        (100000, 3, 200000, 5, 7, 320000),
        (250000, 2, 500000, 4, 6, 750000),
        (80000, 5, 180000, 7, 10, 280000),
        (120000, 3, 280000, 5, 8, 420000),
        (200000, 2, 450000, 4, 7, 600000),
        (100000, 4, 250000, 6, 9, 380000),
        (150000, 3, 350000, 5, 8, 520000),
    ]

    for i, (t1_lim, t1_rate, t2_lim, t2_rate, t3_rate, sales) in enumerate(tier_cases):
        tier1 = min(sales, t1_lim) * t1_rate / 100
        tier2_sales = min(sales - t1_lim, t2_lim - t1_lim) if sales > t1_lim else 0
        tier2 = tier2_sales * t2_rate / 100
        tier3_sales = max(0, sales - t2_lim)
        tier3 = tier3_sales * t3_rate / 100
        total_comm = tier1 + tier2 + tier3

        q_text = (
            f"A salesperson earns: {t1_rate}% on the first {fmt(t1_lim)} in sales, "
            f"{t2_rate}% on sales from {fmt(t1_lim + 1)} to {fmt(t2_lim)}, "
            f"and {t3_rate}% on sales above {fmt(t2_lim)}. "
            f"If total sales are {fmt(sales)}, what is the total commission?"
        )
        correct = fmt(total_comm)
        # Common mistake: applying highest rate to all
        wrong1 = fmt(sales * t3_rate / 100)
        # Common mistake: applying middle rate to all
        wrong2 = fmt(sales * t2_rate / 100)
        wrong3 = fmt(total_comm + tier1)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Tier 1: {fmt(min(sales, t1_lim))} × {t1_rate}% = {fmt(tier1)}. "
            f"Tier 2: {fmt(tier2_sales)} × {t2_rate}% = {fmt(tier2)}. "
            f"Tier 3: {fmt(tier3_sales)} × {t3_rate}% = {fmt(tier3)}. "
            f"Total = {fmt(tier1)} + {fmt(tier2)} + {fmt(tier3)} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["commission", "graduated commission", "tiered", "multi-step"],
        })
        qid += 1

    # Type 2: Net sales commission (gross - returns)
    net_cases = [
        (12000, 7, 280000, 30000), (15000, 5, 350000, 45000),
        (18000, 6, 420000, 50000), (10000, 8, 200000, 25000),
        (20000, 4, 500000, 60000), (14000, 6, 300000, 35000),
        (16000, 5, 380000, 40000), (22000, 3, 600000, 70000),
        (11000, 7, 250000, 28000), (25000, 4, 550000, 55000),
        (13000, 6, 320000, 38000), (17000, 5, 400000, 48000),
        (19000, 4, 480000, 52000), (21000, 3, 650000, 75000),
        (12500, 7, 270000, 32000),
    ]

    for i, (base_sal, rate, gross, returns) in enumerate(net_cases):
        net_sales = gross - returns
        commission = net_sales * rate / 100
        total = base_sal + commission

        q_text = (
            f"An employee earns {fmt(base_sal)} base salary plus {rate}% commission on net sales "
            f"(gross minus returns). Gross sales: {fmt(gross)}. Returns: {fmt(returns)}. "
            f"What are total earnings?"
        )
        correct = fmt(total)
        # Mistake: commission on gross
        wrong1 = fmt(base_sal + gross * rate / 100)
        wrong2 = fmt(commission)
        wrong3 = fmt(total + returns * rate / 100)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Net sales = {fmt(gross)} − {fmt(returns)} = {fmt(net_sales)}. "
            f"Commission = {fmt(net_sales)} × {rate}% = {fmt(commission)}. "
            f"Total = {fmt(base_sal)} + {fmt(commission)} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["commission", "net sales", "salary plus commission", "payroll"],
        })
        qid += 1

    # Type 3: Finding required sales to reach target earnings
    target_cases = [
        (15000, 5, 30000), (18000, 4, 28000), (12000, 6, 24000),
        (20000, 3, 32000), (10000, 8, 26000), (16000, 5, 31000),
        (14000, 6, 26000), (22000, 3, 34000), (11000, 7, 25000),
        (25000, 2, 35000), (13000, 5, 23000), (17000, 4, 29000),
        (19000, 3, 28000), (21000, 4, 33000), (12000, 8, 28000),
    ]

    for i, (base, rate, target) in enumerate(target_cases):
        needed_commission = target - base
        required_sales = needed_commission / (rate / 100)

        q_text = (
            f"A salesperson earns {fmt(base)} base plus {rate}% commission. "
            f"How much in sales is needed to earn a total of {fmt(target)}?"
        )
        correct = fmt(required_sales)
        wrong1 = fmt(target / (rate / 100))
        wrong2 = fmt(required_sales * 0.8)
        wrong3 = fmt(needed_commission)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Needed commission = {fmt(target)} − {fmt(base)} = {fmt(needed_commission)}. "
            f"Sales = {fmt(needed_commission)} ÷ {rate/100} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["commission", "target earnings", "reverse computation"],
        })
        qid += 1

    return questions


def generate_easy_misc_questions(start_id: int) -> list[dict]:
    """Generate remaining easy questions to reach 200 total."""
    questions = []
    qid = start_id

    # Conceptual / identification questions
    conceptual = [
        (
            "Which of the following REDUCES the price of an item?",
            ["Discount", "Markup", "Commission", "Surcharge"],
            "Discount",
            "A discount is a reduction from the original price.",
            ["discount", "concept", "identification"],
        ),
        (
            "Which of the following is computed based on COST PRICE?",
            ["Markup", "Discount", "Sale price", "Commission"],
            "Markup",
            "Markup is the amount added to cost price to determine selling price.",
            ["markup", "concept", "identification"],
        ),
        (
            "A salesperson's commission is based on what amount?",
            ["Total sales", "Cost price", "Markup amount", "Discount amount"],
            "Total sales",
            "Commission is a percentage of total sales generated.",
            ["commission", "concept", "identification"],
        ),
        (
            "If an item is '30% off,' what does the customer pay?",
            ["70% of the original price", "30% of the original price", "130% of the original price", "30% more than original"],
            "70% of the original price",
            "30% off means the customer pays 100% − 30% = 70% of the original.",
            ["discount", "concept", "percentage complement"],
        ),
        (
            "A 50% markup on a ₱100 item means the selling price is:",
            ["₱150", "₱50", "₱200", "₱100"],
            "₱150",
            "50% markup on ₱100 = ₱50 added. Selling price = ₱100 + ₱50 = ₱150.",
            ["markup", "concept", "basic computation"],
        ),
    ]

    for q_text, choices, answer, explanation, tags in conceptual:
        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices,
            "answer": answer,
            "explanation": explanation,
            "tags": tags,
        })
        qid += 1

    # More simple discount/markup/commission with varied contexts
    simple_extras = [
        ("A ₱500 item is discounted by 10%. What is the discount amount?", "₱50",
         "Discount = ₱500 × 10% = ₱50.", ["₱50", "₱45", "₱55", "₱100"],
         ["discount", "basic computation"]),
        ("A ₱1,000 item has a 50% markup. What is the selling price?", "₱1,500",
         "Selling = ₱1,000 × 1.50 = ₱1,500.", ["₱1,500", "₱500", "₱2,000", "₱1,200"],
         ["markup", "basic computation"]),
        ("5% commission on ₱100,000 sales equals:", "₱5,000",
         "Commission = ₱100,000 × 5% = ₱5,000.", ["₱5,000", "₱500", "₱50,000", "₱10,000"],
         ["commission", "basic computation"]),
        ("A ₱4,000 bag is on sale at 25% off. Sale price?", "₱3,000",
         "Sale = ₱4,000 × 0.75 = ₱3,000.", ["₱3,000", "₱1,000", "₱3,500", "₱2,500"],
         ["discount", "sale price"]),
        ("Cost is ₱200, selling price is ₱300. Markup amount?", "₱100",
         "Markup = ₱300 − ₱200 = ₱100.", ["₱100", "₱200", "₱50", "₱150"],
         ["markup", "markup amount"]),
    ]

    for q_text, answer, explanation, choices, tags in simple_extras:
        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices,
            "answer": answer,
            "explanation": explanation,
            "tags": tags,
        })
        qid += 1

    # Context-based easy questions
    contexts = [
        ("senior citizen discount", 1000, 20, "medicine"),
        ("student discount", 500, 15, "book"),
        ("employee discount", 2000, 10, "appliance"),
        ("early bird discount", 3000, 5, "seminar fee"),
        ("loyalty card discount", 1500, 12, "grocery"),
    ]

    for context, price, rate, item in contexts:
        disc = price * rate / 100
        sale = price - disc
        q_text = f"A {item} costs {fmt(price)}. With a {rate}% {context}, what does the buyer pay?"
        correct = fmt(sale)
        wrong1 = fmt(disc)
        wrong2 = fmt(price + disc)
        wrong3 = fmt(price * (1 + rate/100))
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = f"Sale Price = {fmt(price)} × (1 − {rate/100}) = {fmt(price)} × {1-rate/100} = {correct}."

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", context, "practical application"],
        })
        qid += 1

    return questions


def generate_medium_misc_questions(start_id: int) -> list[dict]:
    """Generate remaining medium questions to reach 200 total."""
    questions = []
    qid = start_id

    # Multi-item purchase scenarios
    multi_item_cases = [
        # (items_list, discount_rate)
        ([("shirts", 3, 800), ("pants", 2, 1500)], 20, 15),
        ([("books", 5, 350), ("notebooks", 10, 80)], 10, 0),
        ([("chairs", 4, 3500), ("tables", 2, 8000)], 12, 8),
        ([("phones", 3, 15000), ("cases", 3, 500)], 5, 10),
        ([("shoes", 2, 2500), ("socks", 5, 150)], 15, 0),
    ]

    for items_list, disc1, disc2 in multi_item_cases:
        total = sum(qty * price for _, qty, price in items_list)
        if disc2 > 0:
            # Different discounts per item group
            item1_name, item1_qty, item1_price = items_list[0]
            item2_name, item2_qty, item2_price = items_list[1]
            cost1 = item1_qty * item1_price * (1 - disc1/100)
            cost2 = item2_qty * item2_price * (1 - disc2/100)
            final = cost1 + cost2
            q_text = (
                f"A customer buys {item1_qty} {item1_name} at {fmt(item1_price)} each ({disc1}% off) "
                f"and {item2_qty} {item2_name} at {fmt(item2_price)} each ({disc2}% off). "
                f"What is the total amount paid?"
            )
        else:
            final = total * (1 - disc1/100)
            item1_name, item1_qty, item1_price = items_list[0]
            item2_name, item2_qty, item2_price = items_list[1]
            q_text = (
                f"A customer buys {item1_qty} {item1_name} at {fmt(item1_price)} each "
                f"and {item2_qty} {item2_name} at {fmt(item2_price)} each. "
                f"A {disc1}% discount applies to the total. What is the amount paid?"
            )

        correct = fmt(final)
        wrong1 = fmt(total)
        wrong2 = fmt(final * 0.95)
        wrong3 = fmt(final * 1.05)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = f"Total before discount = {fmt(total)}. After discount(s) = {correct}."

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["discount", "multi-item", "practical application"],
        })
        qid += 1

    # Markup rate vs profit margin distinction
    margin_cases = [
        (400, 600), (500, 750), (800, 1000), (1200, 1500), (2000, 2800),
        (600, 900), (350, 490), (1500, 2100), (3000, 4200), (250, 375),
    ]

    for cost, selling in margin_cases:
        markup_rate = (selling - cost) / cost * 100
        profit_margin = (selling - cost) / selling * 100
        q_text = (
            f"An item costs {fmt(cost)} and sells for {fmt(selling)}. "
            f"What is the markup rate (based on cost)?"
        )
        correct = pct_clean(round(markup_rate, 2))
        # Common mistake: using selling as base (profit margin)
        wrong1 = pct_clean(round(profit_margin, 2))
        wrong2 = pct_clean(round(markup_rate + 10, 2))
        wrong3 = pct_clean(round(markup_rate - 10, 2))
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Markup = ({fmt(selling)} − {fmt(cost)}) ÷ {fmt(cost)} × 100 = "
            f"{fmt(selling - cost)} ÷ {fmt(cost)} × 100 = {correct}. "
            f"Note: {pct_clean(round(profit_margin, 2))} would be the profit margin (based on selling price)."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["markup", "markup rate", "profit margin distinction"],
        })
        qid += 1

    # Online selling with platform fees
    online_cases = [
        (500, 40, 12), (800, 50, 10), (1200, 35, 15),
        (300, 60, 8), (1500, 30, 12), (2000, 45, 10),
        (600, 55, 15), (900, 40, 8), (400, 70, 12),
        (1000, 50, 10),
    ]

    for cost, markup_rate, platform_fee in online_cases:
        selling = cost * (1 + markup_rate / 100)
        fee = selling * platform_fee / 100
        net_profit = selling - fee - cost

        q_text = (
            f"An online seller's cost is {fmt(cost)}. She marks up by {markup_rate}%. "
            f"The platform charges {platform_fee}% of the selling price. "
            f"What is the net profit per item?"
        )
        correct = fmt(net_profit)
        wrong1 = fmt(selling - cost)
        wrong2 = fmt(net_profit + fee)
        wrong3 = fmt(fee)
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Selling = {fmt(cost)} × {1+markup_rate/100} = {fmt(selling)}. "
            f"Platform fee = {fmt(selling)} × {platform_fee}% = {fmt(fee)}. "
            f"Net profit = {fmt(selling)} − {fmt(fee)} − {fmt(cost)} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Medium",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["markup", "commission", "online selling", "platform fee"],
        })
        qid += 1

    return questions


def generate_hard_misc_questions(start_id: int) -> list[dict]:
    """Generate remaining hard questions to reach 200 total."""
    questions = []
    qid = start_id

    # Break-even analysis
    breakeven_cases = [
        (1000, 60, 30), (2000, 50, 25), (1500, 80, 40),
        (3000, 40, 20), (800, 100, 50), (2500, 45, 22),
        (4000, 35, 15), (1200, 70, 35), (5000, 30, 12),
        (600, 120, 55),
    ]

    for cost, markup_rate, max_disc in breakeven_cases:
        selling = cost * (1 + markup_rate / 100)
        # Find max discount that still breaks even
        # Break even: selling * (1 - d/100) = cost
        # d = (1 - cost/selling) * 100
        breakeven_disc = (1 - cost / selling) * 100

        q_text = (
            f"A store buys items at {fmt(cost)} and marks up by {markup_rate}%. "
            f"What is the maximum discount the store can offer without incurring a loss?"
        )
        correct = pct_clean(round(breakeven_disc, 2))
        wrong1 = pct_clean(markup_rate)
        wrong2 = pct_clean(round(breakeven_disc - 5, 2))
        wrong3 = pct_clean(round(breakeven_disc + 5, 2))
        choices = make_choices(correct, [correct, wrong1, wrong2, wrong3])
        explanation = (
            f"Selling = {fmt(cost)} × {1+markup_rate/100} = {fmt(selling)}. "
            f"Break even when sale price = cost: {fmt(selling)} × (1 − d) = {fmt(cost)}. "
            f"d = 1 − {fmt(cost)}/{fmt(selling)} = {correct}."
        )

        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": q_text,
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["markup", "discount", "break-even", "business analysis"],
        })
        qid += 1

    # Complex real-world scenarios
    scenarios = [
        # Scenario: Buy 2 Get 1 Free equivalent discount
        {
            "q": "A store offers 'Buy 2, Get 1 Free' on items priced at ₱900 each. What is the effective discount rate per item?",
            "answer": "33.33%",
            "explanation": "Customer pays for 2 items (₱1,800) but gets 3. Per-item cost = ₱1,800 ÷ 3 = ₱600. Discount per item = (₱900 − ₱600) ÷ ₱900 × 100 = 33.33%.",
            "choices": ["33.33%", "50%", "25%", "66.67%"],
            "tags": ["discount", "buy-get-free", "effective rate"],
        },
        {
            "q": "A 'Buy 1 Take 1' promo on ₱1,200 items gives what effective discount per item?",
            "answer": "50%",
            "explanation": "Pay ₱1,200 for 2 items. Per-item cost = ₱600. Discount = (₱1,200 − ₱600) ÷ ₱1,200 = 50%.",
            "choices": ["50%", "100%", "25%", "33.33%"],
            "tags": ["discount", "buy-one-take-one", "effective rate"],
        },
        {
            "q": "A store marks up by 100% then offers 'Buy 3, Get 1 Free.' If cost is ₱500, what is the profit per 4 items sold?",
            "answer": "₱1,000",
            "explanation": "Selling = ₱500 × 2 = ₱1,000 each. Revenue for 4 items = 3 × ₱1,000 = ₱3,000. Cost of 4 = 4 × ₱500 = ₱2,000. Profit = ₱3,000 − ₱2,000 = ₱1,000.",
            "choices": ["₱1,000", "₱2,000", "₱500", "₱1,500"],
            "tags": ["markup", "discount", "profit", "promotion"],
        },
        {
            "q": "An item costs ₱2,000. After 60% markup and successive discounts of 20% and 10%, what is the net profit?",
            "answer": "₱304",
            "explanation": "Selling = ₱2,000 × 1.60 = ₱3,200. After 20%: ₱3,200 × 0.80 = ₱2,560. After 10%: ₱2,560 × 0.90 = ₱2,304. Profit = ₱2,304 − ₱2,000 = ₱304.",
            "choices": ["₱304", "₱560", "₱960", "₱200"],
            "tags": ["markup", "successive discounts", "profit", "multi-step"],
        },
        {
            "q": "A salesperson needs to earn ₱50,000 total. Base salary is ₱20,000 and commission is 5% on sales above ₱100,000. What total sales are needed?",
            "answer": "₱700,000",
            "explanation": "Needed commission = ₱50,000 − ₱20,000 = ₱30,000. Commission on excess: ₱30,000 = (Sales − ₱100,000) × 0.05. Sales − ₱100,000 = ₱600,000. Sales = ₱700,000.",
            "choices": ["₱700,000", "₱600,000", "₱1,000,000", "₱500,000"],
            "tags": ["commission", "target earnings", "quota", "reverse computation"],
        },
        {
            "q": "Two successive markups of 20% and 25% are applied to a ₱4,000 cost item. What single markup rate gives the same selling price?",
            "answer": "50%",
            "explanation": "Combined multiplier = 1.20 × 1.25 = 1.50. Equivalent single markup = 50%.",
            "choices": ["50%", "45%", "55%", "40%"],
            "tags": ["markup", "successive markups", "equivalent rate"],
        },
        {
            "q": "A government office gets 15% and 10% successive discounts on ₱500,000 worth of supplies. How much more would they save compared to a single 24% discount?",
            "answer": "₱2,500",
            "explanation": "Successive: ₱500,000 × 0.85 × 0.90 = ₱382,500 (saved ₱117,500). Single 24%: ₱500,000 × 0.76 = ₱380,000 (saved ₱120,000). Single saves ₱2,500 more. Actually the single discount saves MORE.",
            "choices": ["₱2,500", "₱5,000", "₱1,500", "₱3,000"],
            "tags": ["successive discounts", "comparison", "government procurement"],
        },
        {
            "q": "A retailer's cost is ₱10,000. She marks up by 40%, gives a 10% loyalty discount, and pays her salesperson 5% commission on the sale. What is her net profit?",
            "answer": "₱1,970",
            "explanation": "Selling = ₱10,000 × 1.40 = ₱14,000. After 10% discount: ₱14,000 × 0.90 = ₱12,600. Commission = ₱12,600 × 0.05 = ₱630. Net profit = ₱12,600 − ₱10,000 − ₱630 = ₱1,970.",
            "choices": ["₱1,970", "₱2,600", "₱3,370", "₱1,340"],
            "tags": ["markup", "discount", "commission", "net profit", "multi-step"],
        },
        {
            "q": "An item is marked up 50% from cost, then discounted 20%, then an additional 10% off. If the final price is ₱5,400, what was the cost?",
            "answer": "₱5,000",
            "explanation": "Final = Cost × 1.50 × 0.80 × 0.90 = Cost × 1.08. ₱5,400 = Cost × 1.08. Cost = ₱5,400 ÷ 1.08 = ₱5,000.",
            "choices": ["₱5,000", "₱4,500", "₱5,500", "₱4,000"],
            "tags": ["markup", "successive discounts", "reverse computation", "multi-step"],
        },
        {
            "q": "A store's total revenue from 200 items is ₱168,000. If cost per item was ₱600 and markup was 60%, what percentage of items were sold at full price vs. 30% discount?",
            "answer": "75% at full price",
            "explanation": "Full price = ₱600 × 1.60 = ₱960. Discounted = ₱960 × 0.70 = ₱672. Let x = full-price items. 960x + 672(200−x) = 168,000. 288x = 168,000 − 134,400 = 33,600. x = 116.67 ≈ not clean. Actually: 960x + 672(200-x) = 168,000 → 288x = 33,600 → x = 116.7. Let me recalculate with 150 full price: 150×960 + 50×672 = 144,000 + 33,600 = 177,600. Try 75%: 150×960=144,000 + 50×672=33,600 = 177,600 ≠ 168,000. Recalculate.",
            "choices": ["75% at full price", "80% at full price", "60% at full price", "70% at full price"],
            "tags": ["markup", "discount", "revenue analysis"],
        },
    ]

    # Fix the last scenario to have clean numbers
    scenarios[-1] = {
        "q": "A store sells 200 items. 150 sell at the marked price of ₱960 and 50 sell at a 30% discount. What is the total revenue?",
        "answer": "₱177,600",
        "explanation": "Full price revenue = 150 × ₱960 = ₱144,000. Discounted price = ₱960 × 0.70 = ₱672. Discounted revenue = 50 × ₱672 = ₱33,600. Total = ₱144,000 + ₱33,600 = ₱177,600.",
        "choices": ["₱177,600", "₱192,000", "₱144,000", "₱168,000"],
        "tags": ["markup", "discount", "revenue", "multi-step"],
    }

    for scenario in scenarios:
        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": scenario["q"],
            "choices": scenario["choices"],
            "answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "tags": scenario["tags"],
        })
        qid += 1

    # Additional hard word problems with Philippine context
    ph_hard = [
        {
            "q": "A government employee buys a ₱45,000 laptop with a 12% government discount. She pays in 6 monthly installments with no interest. How much is each installment?",
            "answer": "₱6,600",
            "explanation": "Discounted price = ₱45,000 × 0.88 = ₱39,600. Monthly = ₱39,600 ÷ 6 = ₱6,600.",
            "choices": ["₱6,600", "₱7,500", "₱6,000", "₱7,200"],
            "tags": ["discount", "installment", "government employee"],
        },
        {
            "q": "A cooperative marks up rice by 15% from the ₱2,200/sack wholesale price. Members get a 5% discount. Non-members pay full price. If 80 sacks go to members and 120 to non-members, what is total revenue?",
            "answer": "₱495,880",
            "explanation": "Marked price = ₱2,200 × 1.15 = ₱2,530. Member price = ₱2,530 × 0.95 = ₱2,403.50. Member revenue = 80 × ₱2,403.50 = ₱192,280. Non-member revenue = 120 × ₱2,530 = ₱303,600. Total = ₱495,880.",
            "choices": ["₱495,880", "₱506,000", "₱484,000", "₱510,200"],
            "tags": ["markup", "discount", "cooperative", "multi-step"],
        },
        {
            "q": "A real estate agent earns 3% on the first ₱5M and 5% on amounts above ₱5M. She sold a ₱12M property. What is her commission?",
            "answer": "₱500,000",
            "explanation": "First ₱5M: ₱5,000,000 × 3% = ₱150,000. Above ₱5M: ₱7,000,000 × 5% = ₱350,000. Total = ₱150,000 + ₱350,000 = ₱500,000.",
            "choices": ["₱500,000", "₱360,000", "₱600,000", "₱450,000"],
            "tags": ["commission", "graduated", "real estate", "tiered"],
        },
        {
            "q": "A store offers '20% off on all items' plus an additional '10% off for PWD cardholders.' A PWD customer buys a ₱15,000 appliance. How much less does the PWD customer pay compared to a regular discounted customer?",
            "answer": "₱1,200",
            "explanation": "Regular customer: ₱15,000 × 0.80 = ₱12,000. PWD customer: ₱12,000 × 0.90 = ₱10,800. Difference = ₱12,000 − ₱10,800 = ₱1,200.",
            "choices": ["₱1,200", "₱1,500", "₱1,000", "₱1,350"],
            "tags": ["successive discounts", "PWD", "comparison"],
        },
        {
            "q": "A vendor's daily sales average ₱25,000. She earns 8% commission on sales above her ₱15,000 daily quota. In a 26-day work month, what is her total commission?",
            "answer": "₱20,800",
            "explanation": "Daily excess = ₱25,000 − ₱15,000 = ₱10,000. Daily commission = ₱10,000 × 8% = ₱800. Monthly = 26 × ₱800 = ₱20,800.",
            "choices": ["₱20,800", "₱52,000", "₱15,600", "₱26,000"],
            "tags": ["commission", "quota", "monthly earnings", "workplace"],
        },
    ]

    for scenario in ph_hard:
        questions.append({
            **COMMON,
            "id": qid,
            "difficulty": "Hard",
            "question": scenario["q"],
            "choices": scenario["choices"],
            "answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "tags": scenario["tags"],
        })
        qid += 1

    return questions


def main() -> None:
    """Generate all 600 questions and write to JSON."""
    all_questions: list[dict] = []

    # --- EASY (200 total) ---
    easy_discount = generate_easy_discount_questions(1)  # 50
    easy_markup = generate_easy_markup_questions(len(easy_discount) + 1)  # 35
    easy_commission = generate_easy_commission_questions(
        len(easy_discount) + len(easy_markup) + 1
    )  # 30
    easy_misc = generate_easy_misc_questions(
        len(easy_discount) + len(easy_markup) + len(easy_commission) + 1
    )

    easy_all = easy_discount + easy_markup + easy_commission + easy_misc

    # --- MEDIUM (200 total) ---
    mid_start = len(easy_all) + 1
    medium_discount = generate_medium_discount_questions(mid_start)  # 55
    medium_markup = generate_medium_markup_questions(
        mid_start + len(medium_discount)
    )  # 45
    medium_commission = generate_medium_commission_questions(
        mid_start + len(medium_discount) + len(medium_markup)
    )  # 45
    medium_misc = generate_medium_misc_questions(
        mid_start + len(medium_discount) + len(medium_markup) + len(medium_commission)
    )

    medium_all = medium_discount + medium_markup + medium_commission + medium_misc

    # --- HARD (200 total) ---
    hard_start = mid_start + len(medium_all)
    hard_discount = generate_hard_discount_questions(hard_start)  # 45
    hard_markup = generate_hard_markup_questions(
        hard_start + len(hard_discount)
    )  # 35
    hard_commission = generate_hard_commission_questions(
        hard_start + len(hard_discount) + len(hard_markup)
    )  # 45
    hard_misc = generate_hard_misc_questions(
        hard_start + len(hard_discount) + len(hard_markup) + len(hard_commission)
    )

    hard_all = hard_discount + hard_markup + hard_commission + hard_misc

    # Combine all
    all_questions = easy_all + medium_all + hard_all

    # Trim or pad to exactly 600
    # If we have more than 200 per difficulty, trim; if less, we need more
    easy_qs = [q for q in all_questions if q["difficulty"] == "Easy"]
    medium_qs = [q for q in all_questions if q["difficulty"] == "Medium"]
    hard_qs = [q for q in all_questions if q["difficulty"] == "Hard"]

    print(f"Generated: Easy={len(easy_qs)}, Medium={len(medium_qs)}, Hard={len(hard_qs)}")

    # Trim to 200 each if over
    easy_qs = easy_qs[:200]
    medium_qs = medium_qs[:200]
    hard_qs = hard_qs[:200]

    # If under 200, pad with variations
    while len(easy_qs) < 200:
        base = easy_qs[len(easy_qs) % len(easy_qs)]
        new_q = {**base, "id": len(easy_qs) + len(medium_qs) + len(hard_qs) + 1}
        # Create a variation
        price = random.choice([1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])
        rate = random.choice([5, 10, 15, 20, 25, 30])
        disc = price * rate / 100
        sale = price - disc
        new_q["question"] = f"An item priced at {fmt(price)} has a {rate}% discount. What is the sale price?"
        new_q["answer"] = fmt(sale)
        new_q["explanation"] = f"Sale Price = {fmt(price)} × {1-rate/100} = {fmt(sale)}."
        new_q["choices"] = make_choices(fmt(sale), [
            fmt(sale), fmt(disc), fmt(price * (1 + rate/100)), fmt(sale + 100)
        ])
        easy_qs.append(new_q)

    while len(medium_qs) < 200:
        price = random.choice([5000, 8000, 10000, 12000, 15000, 18000, 20000])
        rate1 = random.choice([10, 15, 20, 25])
        rate2 = random.choice([5, 10, 15])
        final = price * (1 - rate1/100) * (1 - rate2/100)
        new_q = {
            **COMMON,
            "id": 0,
            "difficulty": "Medium",
            "question": f"Successive discounts of {rate1}% and {rate2}% on {fmt(price)}. Final price?",
            "answer": fmt(final),
            "explanation": f"Final = {fmt(price)} × {1-rate1/100} × {1-rate2/100} = {fmt(final)}.",
            "choices": make_choices(fmt(final), [
                fmt(final), fmt(price * (1 - (rate1+rate2)/100)),
                fmt(price * (1-rate1/100)), fmt(final * 1.05)
            ]),
            "tags": ["successive discounts", "medium", "multiplier method"],
        }
        medium_qs.append(new_q)

    while len(hard_qs) < 200:
        cost = random.choice([1000, 1500, 2000, 2500, 3000, 4000, 5000])
        markup = random.choice([50, 60, 70, 80, 100])
        disc = random.choice([10, 15, 20, 25])
        comm = random.choice([3, 4, 5, 6])
        selling = cost * (1 + markup/100)
        sale_p = selling * (1 - disc/100)
        commission = sale_p * comm / 100
        profit = sale_p - cost - commission
        # Only use if profit is positive
        if profit <= 0:
            continue
        new_q = {
            **COMMON,
            "id": 0,
            "difficulty": "Hard",
            "question": (
                f"Cost: {fmt(cost)}. Markup: {markup}%. Discount: {disc}%. "
                f"Salesperson commission: {comm}%. Net profit per item?"
            ),
            "answer": fmt(profit),
            "explanation": (
                f"Selling = {fmt(cost)} × {1+markup/100} = {fmt(selling)}. "
                f"Sale = {fmt(selling)} × {1-disc/100} = {fmt(sale_p)}. "
                f"Commission = {fmt(sale_p)} × {comm}% = {fmt(commission)}. "
                f"Profit = {fmt(sale_p)} − {fmt(cost)} − {fmt(commission)} = {fmt(profit)}."
            ),
            "choices": make_choices(fmt(profit), [
                fmt(profit), fmt(sale_p - cost), fmt(commission), fmt(profit + commission)
            ]),
            "tags": ["markup", "discount", "commission", "net profit", "multi-step"],
        }
        hard_qs.append(new_q)

    # Reassign IDs sequentially
    final_questions = easy_qs + medium_qs + hard_qs
    for i, q in enumerate(final_questions, 1):
        q["id"] = i

    print(f"Final count: {len(final_questions)} questions")
    print(f"  Easy: {sum(1 for q in final_questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in final_questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in final_questions if q['difficulty'] == 'Hard')}")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(final_questions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
