"""
Fix issues in discounts-markups-and-sales/questions.json:
1. Replace 35 duplicate questions with unique ones
2. Fix Q542 wording
3. Fix Q248 (replace with non-equal comparison)
4. Fix Q253 floating point in explanation
5. Fix Q441 floating point in explanation

Run: python scripts/fix_discounts_questions.py
"""

import json
import random
from pathlib import Path

random.seed(99)

QUESTIONS_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "numerical-ability" / "percentages"
    / "discounts-markups-and-sales" / "questions.json"
)


def make_peso(val: float) -> str:
    """Format a peso value."""
    if val == int(val):
        v = int(val)
        if v >= 1000:
            return f"₱{v:,}"
        return f"₱{v}"
    # Handle decimals
    s = f"{val:.2f}"
    parts = s.split('.')
    int_part = int(parts[0])
    dec_part = parts[1].rstrip('0')
    if not dec_part:
        if int_part >= 1000:
            return f"₱{int_part:,}"
        return f"₱{int_part}"
    if int_part >= 1000:
        return f"₱{int_part:,}.{dec_part}"
    return f"₱{int_part}.{dec_part}"


def generate_sale_price_question(qid: int, difficulty: str) -> dict:
    """Generate a unique sale price question."""
    items = [
        ("blouse", 800, 15), ("jacket", 3500, 20), ("watch", 6500, 25),
        ("tablet", 12000, 10), ("headphones", 4500, 30), ("backpack", 2800, 15),
        ("sneakers", 5500, 20), ("sunglasses", 3200, 25), ("wallet", 1800, 10),
        ("perfume", 4000, 30), ("dress", 2200, 15), ("belt", 1500, 20),
        ("umbrella", 900, 25), ("towel", 650, 10), ("pillow", 1100, 30),
        ("lamp", 2400, 15), ("clock", 3800, 20), ("vase", 1700, 25),
        ("blanket", 2600, 10), ("curtain", 4200, 30), ("rug", 5800, 15),
        ("mirror", 3100, 20), ("frame", 1400, 25), ("candle set", 950, 10),
        ("planner", 750, 30), ("mug set", 1200, 15), ("thermos", 1600, 20),
        ("speaker", 2900, 25), ("keyboard", 3400, 10), ("mouse", 1300, 30),
        ("charger", 800, 15), ("cable", 450, 20), ("case", 1100, 25),
        ("stand", 2000, 10), ("holder", 600, 30), ("organizer", 1500, 15),
        ("notebook", 350, 20), ("pen set", 500, 25), ("scissors", 280, 10),
        ("stapler", 420, 30),
    ]
    
    item, price, rate = random.choice(items)
    # Randomize price slightly
    price = price + random.choice([-100, 0, 100, 200, -200, 50, -50])
    if price < 100:
        price = 100
    rate = random.choice([5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40])
    
    sale_price = price * (1 - rate / 100)
    sale_price = round(sale_price, 2)
    
    # Generate distractors
    distractors = set()
    distractors.add(round(price * (rate / 100), 2))  # Discount amount (common mistake)
    distractors.add(round(price * (1 + rate / 100), 2))  # Added instead of subtracted
    distractors.add(round(price - rate, 2))  # Subtracted rate directly
    
    # Remove correct answer from distractors
    distractors.discard(sale_price)
    distractors = [d for d in distractors if d > 0 and d != sale_price]
    
    while len(distractors) < 3:
        d = sale_price + random.choice([-200, -100, 100, 200, -50, 50, 150, -150])
        if d > 0 and d != sale_price and d not in distractors:
            distractors.append(round(d, 2))
    
    distractors = distractors[:3]
    choices = [make_peso(sale_price)] + [make_peso(d) for d in distractors]
    random.shuffle(choices)
    
    return {
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Discounts, Markups, and Sales",
        "difficulty": difficulty,
        "question": f"A {item} priced at {make_peso(price)} has a {rate}% discount. What is the sale price?",
        "choices": choices,
        "answer": make_peso(sale_price),
        "explanation": f"Sale Price = {make_peso(price)} × {(100-rate)/100} = {make_peso(sale_price)}.",
        "tags": ["discount", "sale price", "basic computation"]
    }


def generate_discount_rate_question(qid: int, difficulty: str) -> dict:
    """Generate a unique discount rate question."""
    rates = [5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40]
    rate = random.choice(rates)
    
    originals = [500, 600, 750, 800, 900, 1000, 1200, 1500, 1800, 2000, 
                 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7500, 8000, 10000,
                 12000, 15000, 18000, 20000, 25000]
    original = random.choice(originals)
    
    sale_price = original * (1 - rate / 100)
    discount_amount = original - sale_price
    
    distractors = set()
    distractors.add(rate + 5)
    distractors.add(rate - 5 if rate > 5 else rate + 10)
    distractors.add(round(discount_amount / sale_price * 100))  # Wrong base
    distractors.discard(rate)
    distractors = [d for d in distractors if 0 < d <= 100 and d != rate]
    
    while len(distractors) < 3:
        d = rate + random.choice([-3, -2, 2, 3, 7, 8, -8])
        if 0 < d <= 100 and d != rate and d not in distractors:
            distractors.append(d)
    
    distractors = distractors[:3]
    choices = [f"{rate}%"] + [f"{int(d)}%" for d in distractors]
    random.shuffle(choices)
    
    return {
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Discounts, Markups, and Sales",
        "difficulty": difficulty,
        "question": f"An item originally priced at {make_peso(original)} is sold for {make_peso(sale_price)}. What is the discount rate?",
        "choices": choices,
        "answer": f"{rate}%",
        "explanation": f"Discount = {make_peso(original)} − {make_peso(sale_price)} = {make_peso(discount_amount)}. Rate = {make_peso(discount_amount)} ÷ {make_peso(original)} × 100 = {rate}%.",
        "tags": ["discount", "discount rate", "basic computation"]
    }


def generate_markup_rate_question(qid: int, difficulty: str) -> dict:
    """Generate a unique markup rate question."""
    rates = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 75, 80, 100]
    rate = random.choice(rates)
    
    costs = [100, 150, 200, 250, 300, 400, 500, 600, 750, 800, 1000,
             1200, 1500, 2000, 2500, 3000, 4000, 5000]
    cost = random.choice(costs)
    
    selling = cost * (1 + rate / 100)
    markup_amount = selling - cost
    
    distractors = set()
    distractors.add(round(markup_amount / selling * 100))  # Profit margin (wrong base)
    distractors.add(rate + 10)
    distractors.add(rate - 10 if rate > 10 else rate + 15)
    distractors.discard(rate)
    distractors = [d for d in distractors if 0 < d and d != rate]
    
    while len(distractors) < 3:
        d = rate + random.choice([-5, 5, 12, -12, 8, -8])
        if 0 < d and d != rate and d not in distractors:
            distractors.append(d)
    
    distractors = distractors[:3]
    choices = [f"{rate}%"] + [f"{int(d)}%" for d in distractors]
    random.shuffle(choices)
    
    return {
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Discounts, Markups, and Sales",
        "difficulty": difficulty,
        "question": f"A vendor buys an item for {make_peso(cost)} and sells it for {make_peso(selling)}. What is the markup rate?",
        "choices": choices,
        "answer": f"{rate}%",
        "explanation": f"Markup = {make_peso(selling)} − {make_peso(cost)} = {make_peso(markup_amount)}. Rate = {make_peso(markup_amount)} ÷ {make_peso(cost)} × 100 = {rate}%.",
        "tags": ["markup", "markup rate", "basic computation"]
    }


def generate_commission_question(qid: int, difficulty: str) -> dict:
    """Generate a unique commission question."""
    rates = [2, 3, 4, 5, 6, 7, 8, 10]
    rate = random.choice(rates)
    
    sales_options = [50000, 80000, 100000, 120000, 150000, 180000, 200000,
                     250000, 300000, 350000, 400000, 500000, 750000, 1000000]
    sales = random.choice(sales_options)
    
    commission = sales * rate / 100
    
    distractors = set()
    distractors.add(commission * 2)
    distractors.add(commission / 2)
    distractors.add(sales - commission)
    distractors.discard(commission)
    distractors = [d for d in distractors if d > 0 and d != commission]
    
    while len(distractors) < 3:
        d = commission + random.choice([-5000, -2000, 2000, 5000, -1000, 1000])
        if d > 0 and d != commission and d not in distractors:
            distractors.append(d)
    
    distractors = distractors[:3]
    choices = [make_peso(commission)] + [make_peso(d) for d in distractors]
    random.shuffle(choices)
    
    jobs = ["sales agent", "insurance agent", "real estate broker", "car salesman",
            "retail associate", "marketing officer", "account executive"]
    job = random.choice(jobs)
    
    return {
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Discounts, Markups, and Sales",
        "difficulty": difficulty,
        "question": f"A {job} earns a {rate}% commission on total sales of {make_peso(sales)}. How much commission is earned?",
        "choices": choices,
        "answer": make_peso(commission),
        "explanation": f"Commission = {make_peso(sales)} × {rate}% = {make_peso(sales)} × {rate/100} = {make_peso(commission)}.",
        "tags": ["commission", "basic computation", "sales"]
    }


def main():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    print(f"Loaded {len(questions)} questions")
    
    # Find duplicates
    seen = {}
    duplicate_ids = []
    for q in questions:
        text = q["question"].strip()
        if text in seen:
            duplicate_ids.append(q["id"])
        else:
            seen[text] = q["id"]
    
    print(f"Found {len(duplicate_ids)} duplicate question IDs: {duplicate_ids}")
    
    # Generate replacements for duplicates
    existing_questions = {q["question"].strip() for q in questions}
    generators = [
        generate_sale_price_question,
        generate_discount_rate_question,
        generate_markup_rate_question,
        generate_commission_question,
    ]
    
    replacements = {}
    for dup_id in duplicate_ids:
        # Find the question to replace
        orig_q = next(q for q in questions if q["id"] == dup_id)
        difficulty = orig_q["difficulty"]
        
        # Generate a unique replacement
        attempts = 0
        while attempts < 100:
            gen = random.choice(generators)
            new_q = gen(dup_id, difficulty)
            if new_q["question"].strip() not in existing_questions:
                existing_questions.add(new_q["question"].strip())
                replacements[dup_id] = new_q
                break
            attempts += 1
        
        if dup_id not in replacements:
            print(f"  WARNING: Could not generate unique replacement for Q{dup_id}")
    
    print(f"Generated {len(replacements)} replacement questions")
    
    # Apply replacements
    for i, q in enumerate(questions):
        if q["id"] in replacements:
            questions[i] = replacements[q["id"]]
    
    # Fix Q542: Reword the question
    for q in questions:
        if q["id"] == 542:
            q["question"] = "A government office gets 15% and 10% successive discounts on ₱500,000 worth of supplies. A single 24% discount is also available. What is the difference in savings between the two options?"
            q["explanation"] = "Successive: ₱500,000 × 0.85 × 0.90 = ₱382,500 (saved ₱117,500). Single 24%: ₱500,000 × 0.76 = ₱380,000 (saved ₱120,000). Difference = ₱120,000 − ₱117,500 = ₱2,500."
            break
    
    # Fix Q248: Replace with a non-equal comparison
    for q in questions:
        if q["id"] == 248:
            q["question"] = "Supplier A offers an item at ₱120,000 with a 8% discount. Supplier B offers the same item at ₱115,000 with a 3% discount. Which is cheaper and by how much?"
            # A: 120000 × 0.92 = 110,400
            # B: 115000 × 0.97 = 111,550
            # A is cheaper by 1,150
            q["choices"] = ["Supplier A by ₱1,150", "Supplier B by ₱1,150", "Supplier A by ₱5,000", "Supplier B by ₱5,000"]
            q["answer"] = "Supplier A by ₱1,150"
            q["explanation"] = "Supplier A net = ₱120,000 × 0.92 = ₱110,400. Supplier B net = ₱115,000 × 0.97 = ₱111,550. Supplier A is cheaper by ₱1,150."
            break
    
    # Fix Q253: Clean up floating point
    for q in questions:
        if q["id"] == 253:
            q["explanation"] = q["explanation"].replace("0.9299999999999999", "0.93")
            break
    
    # Fix Q441: Clean up floating point
    for q in questions:
        if q["id"] == 441:
            q["explanation"] = "Marked price = ₱120 × 1.4 = ₱168. Full-price revenue = 400 × ₱168 = ₱67,200. Discounted revenue = 100 × ₱168 × 0.2 = ₱3,360. Total = ₱70,560."
            break
    
    # Verify no duplicates remain
    seen2 = {}
    remaining_dups = 0
    for q in questions:
        text = q["question"].strip()
        if text in seen2:
            remaining_dups += 1
        else:
            seen2[text] = q["id"]
    
    print(f"Remaining duplicates after fix: {remaining_dups}")
    
    # Verify all answers are in choices
    aic_errors = sum(1 for q in questions if q["answer"] not in q["choices"])
    print(f"Answer-in-choices errors: {aic_errors}")
    
    # Write fixed file
    with open(QUESTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Fixed file written to {QUESTIONS_PATH}")
    print(f"  - Replaced {len(replacements)} duplicate questions")
    print(f"  - Fixed Q542 wording")
    print(f"  - Fixed Q248 (non-equal comparison)")
    print(f"  - Fixed Q253, Q441 floating point")


if __name__ == "__main__":
    main()
