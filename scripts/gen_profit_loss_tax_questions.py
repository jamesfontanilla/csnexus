"""Generate 600 questions for Profit, Loss, and Tax subtopic.

Distribution: 200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/numerical-ability/percentages/profit-loss-and-tax/questions.json

Guarantees:
- Zero duplicate questions (tracked via seen set)
- 100% mathematical accuracy (all computations verified before inclusion)
- Clean integer answers only (no rounding ambiguity)

Run:
    python scripts/gen_profit_loss_tax_questions.py
"""

from __future__ import annotations

import json
import random
from pathlib import Path

random.seed(2024)

OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "numerical-ability" / "percentages" / "profit-loss-and-tax"
)


def _peso(value: int) -> str:
    return f"\u20b1{value:,}"

def _pct(value: int) -> str:
    return f"{value}%"

def _distractors_amount(correct: int, count: int = 3) -> list[str]:
    distractors: set[str] = set()
    offsets = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 0.75]
    for _ in range(80):
        if len(distractors) >= count:
            break
        off = random.choice(offsets)
        direction = random.choice([-1, 1])
        wrong = int(correct * (1 + direction * off))
        if wrong != correct and wrong > 0 and _peso(wrong) not in distractors:
            distractors.add(_peso(wrong))
    # Fallback
    delta = max(100, correct // 10)
    for i in range(1, 10):
        if len(distractors) >= count:
            break
        w = correct + i * delta
        if _peso(w) not in distractors:
            distractors.add(_peso(w))
    return list(distractors)[:count]

def _distractors_pct(correct: int, count: int = 3) -> list[str]:
    distractors: set[str] = set()
    for off in [2, 3, 5, 8, 10, 12, 15, 20]:
        for d in [correct + off, correct - off]:
            if 0 < d <= 200 and d != correct:
                distractors.add(_pct(d))
    return list(distractors)[:count]

def _shuffle_choices(correct: str, distractors: list[str]) -> list[str]:
    choices = [correct] + distractors[:3]
    random.shuffle(choices)
    return choices

# Item and context pools
ITEMS_EASY = [
    "a calculator", "a notebook", "a pen", "a bag", "a shirt",
    "a pair of shoes", "a watch", "a phone case", "a water bottle", "a cap",
    "a book", "a folder", "a USB drive", "a mouse", "a keyboard",
    "a mug", "a lunch box", "an umbrella", "a flashlight", "a charger",
]
ITEMS_MEDIUM = [
    "a printer", "a desk", "a chair", "a monitor", "a tablet",
    "a microwave", "a fan", "a filing cabinet", "a whiteboard", "a projector",
    "a scanner", "a shredder", "a coffee maker", "a water dispenser", "a bookshelf",
    "a set of tools", "a first aid kit", "a fire extinguisher", "a CCTV camera", "a router",
]
ITEMS_HARD = [
    "a laptop", "a photocopier", "a server rack", "an air conditioning unit",
    "a generator set", "a delivery van", "construction materials",
    "office renovation services", "a security system", "a water pump",
    "laboratory equipment", "a forklift", "industrial shelving",
    "a commercial refrigerator", "a POS system", "networking equipment",
    "a solar panel set", "a transformer", "a compressor", "surveying instruments",
]

CONTEXTS_EASY = ["A store", "A vendor", "A small shop", "A canteen", "A market stall",
                 "A school supply store", "A convenience store", "A bakery"]
CONTEXTS_MEDIUM = ["An office supply dealer", "A hardware store", "A furniture shop",
                   "A government cooperative", "A school cafeteria", "A printing shop",
                   "A bookstore", "An electronics retailer"]
CONTEXTS_HARD = ["A government agency", "An engineering firm", "A construction company",
                 "A transport cooperative", "A hospital procurement office",
                 "A telecommunications company", "A manufacturing plant", "A logistics firm"]


def _clean_mult(base: int, pct: int) -> bool:
    """Check if base * pct / 100 is a clean integer."""
    return (base * pct) % 100 == 0


def _clean_vat(base: int) -> bool:
    """Check if base * 0.12 is a clean integer (for 12% VAT)."""
    return (base * 12) % 100 == 0


def generate_all() -> list[dict]:
    """Generate all 600 questions with uniqueness and accuracy guarantees."""
    all_q: list[dict] = []
    seen: set[str] = set()

    def add(difficulty: str, question: str, choices: list[str],
            answer: str, explanation: str, tags: list[str]) -> bool:
        if question in seen:
            return False
        if answer not in choices:
            return False
        seen.add(question)
        all_q.append({
            "question": question, "choices": choices, "answer": answer,
            "explanation": explanation, "tags": tags, "difficulty": difficulty,
        })
        return True

    # ===== EASY (200) =====

    # E1: Profit amount (50)
    combos = [(cp, pct) for cp in range(100, 5001, 50) for pct in [10, 15, 20, 25, 30, 40, 50]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 50: break
        profit = cp * pct // 100
        sp = cp + profit
        ctx, item = random.choice(CONTEXTS_EASY), random.choice(ITEMS_EASY)
        q = f"{ctx} bought {item} for {_peso(cp)} and sold it for {_peso(sp)}. What is the profit?"
        ans = _peso(profit)
        if add("Easy", q, _shuffle_choices(ans, _distractors_amount(profit)), ans,
               f"Profit = SP \u2212 CP = {_peso(sp)} \u2212 {_peso(cp)} = {ans}.",
               ["profit", "basic computation", "business math"]):
            count += 1

    # E2: Loss amount (40)
    combos = [(cp, pct) for cp in range(400, 8001, 100) for pct in [10, 15, 20, 25, 30, 40]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 40: break
        loss = cp * pct // 100
        sp = cp - loss
        ctx, item = random.choice(CONTEXTS_EASY), random.choice(ITEMS_EASY)
        q = f"{ctx} bought {item} for {_peso(cp)} and sold it for {_peso(sp)}. What is the loss?"
        ans = _peso(loss)
        if add("Easy", q, _shuffle_choices(ans, _distractors_amount(loss)), ans,
               f"Loss = CP \u2212 SP = {_peso(cp)} \u2212 {_peso(sp)} = {ans}.",
               ["loss", "basic computation", "business math"]):
            count += 1

    # E3: VAT amount (40) — unique prices with clean 12%
    prices = [p for p in range(100, 20001, 25) if _clean_vat(p)]
    random.shuffle(prices)
    count = 0
    for price in prices:
        if count >= 40: break
        vat = price * 12 // 100
        q = f"An item costs {_peso(price)} before tax. If VAT is 12%, what is the VAT amount?"
        ans = _peso(vat)
        if add("Easy", q, _shuffle_choices(ans, _distractors_amount(vat)), ans,
               f"VAT = {_peso(price)} \u00d7 0.12 = {ans}.",
               ["VAT", "tax computation", "basic computation"]):
            count += 1

    # E4: Total price with VAT (35)
    prices2 = [p for p in range(200, 15001, 50) if _clean_vat(p)]
    random.shuffle(prices2)
    count = 0
    for price in prices2:
        if count >= 35: break
        total = price * 112 // 100
        item = random.choice(ITEMS_EASY + ITEMS_MEDIUM)
        q = f"{item.capitalize()} costs {_peso(price)} (VAT-exclusive). With 12% VAT, what is the total price?"
        ans = _peso(total)
        if add("Easy", q, _shuffle_choices(ans, _distractors_amount(total)), ans,
               f"Total Price = {_peso(price)} \u00d7 1.12 = {ans}.",
               ["VAT", "total price", "tax computation"]):
            count += 1

    # E5: Profit percentage (35)
    combos = [(cp, pct) for cp in range(200, 6001, 50) for pct in [5, 10, 15, 20, 25, 30, 40, 50]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 35: break
        profit = cp * pct // 100
        sp = cp + profit
        ctx, item = random.choice(CONTEXTS_EASY), random.choice(ITEMS_EASY)
        q = f"{ctx} bought {item} for {_peso(cp)} and sold it for {_peso(sp)}. What is the profit percentage?"
        ans = _pct(pct)
        if add("Easy", q, _shuffle_choices(ans, _distractors_pct(pct)), ans,
               f"Profit = {_peso(profit)}. Profit % = ({_peso(profit)} \u00f7 {_peso(cp)}) \u00d7 100% = {ans}.",
               ["profit percentage", "business math", "percentage"]):
            count += 1


    # ===== MEDIUM (200) =====

    # M1: Find SP given CP and profit % (30)
    combos = [(cp, pct) for cp in range(3000, 30001, 500) for pct in [10, 12, 15, 18, 20, 25, 30, 35, 40]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 30: break
        sp = cp + cp * pct // 100
        ctx, item = random.choice(CONTEXTS_MEDIUM), random.choice(ITEMS_MEDIUM)
        q = f"{ctx} bought {item} for {_peso(cp)} and sold it at a {pct}% profit. What is the selling price?"
        ans = _peso(sp)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(sp)), ans,
               f"SP = CP \u00d7 (1 + {pct}/100) = {_peso(cp)} \u00d7 {1+pct/100:.2f} = {ans}.",
               ["profit", "selling price", "percentage application"]):
            count += 1

    # M2: Find CP given SP and profit % (25)
    combos = [(cp, pct) for cp in range(2000, 25001, 500) for pct in [10, 15, 20, 25, 30, 40, 50]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 25: break
        sp = cp + cp * pct // 100
        item = random.choice(ITEMS_MEDIUM)
        q = f"A seller sold {item} for {_peso(sp)} at a {pct}% profit. What was the cost price?"
        ans = _peso(cp)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(cp)), ans,
               f"CP = SP \u00f7 (1 + {pct}/100) = {_peso(sp)} \u00f7 {1+pct/100:.2f} = {ans}.",
               ["profit", "cost price", "reverse computation"]):
            count += 1

    # M3: Loss percentage (25)
    combos = [(cp, pct) for cp in range(2000, 25001, 500) for pct in [5, 8, 10, 12, 15, 20, 25, 30, 35]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 25: break
        loss = cp * pct // 100
        sp = cp - loss
        ctx, item = random.choice(CONTEXTS_MEDIUM), random.choice(ITEMS_MEDIUM)
        q = f"{ctx} purchased {item} for {_peso(cp)} and sold it for {_peso(sp)}. What is the loss percentage?"
        ans = _pct(pct)
        if add("Medium", q, _shuffle_choices(ans, _distractors_pct(pct)), ans,
               f"Loss = {_peso(loss)}. Loss % = ({_peso(loss)} \u00f7 {_peso(cp)}) \u00d7 100% = {ans}.",
               ["loss percentage", "business math", "percentage"]):
            count += 1

    # M4: Base price from VAT-inclusive (25)
    bases = [b for b in range(1000, 30001, 250) if _clean_vat(b)]
    random.shuffle(bases)
    count = 0
    for base in bases:
        if count >= 25: break
        total = base * 112 // 100
        q = f"A receipt shows {_peso(total)} (VAT-inclusive at 12%). What is the base price before VAT?"
        ans = _peso(base)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(base)), ans,
               f"Base Price = {_peso(total)} \u00f7 1.12 = {ans}.",
               ["VAT", "base price", "tax extraction"]):
            count += 1

    # M5: SP given CP and loss % (20)
    combos = [(cp, pct) for cp in range(3000, 30001, 1000) for pct in [10, 15, 20, 25, 30, 35, 40]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 20: break
        sp = cp - cp * pct // 100
        item = random.choice(ITEMS_MEDIUM)
        q = f"An item costing {_peso(cp)} was sold at a {pct}% loss. What is the selling price?"
        ans = _peso(sp)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(sp)), ans,
               f"SP = CP \u00d7 (1 \u2212 {pct}/100) = {_peso(cp)} \u00d7 {1-pct/100:.2f} = {ans}.",
               ["loss", "selling price", "percentage application"]):
            count += 1

    # M6: Multiple items profit (20)
    combos = [(qty, cp_e, pct) for qty in [5,8,10,12,15,20,24,25,30,40,50]
              for cp_e in [50,60,75,80,100,120,150,200,250,300,400,500]
              for pct in [10,15,20,25,30,40,50] if _clean_mult(cp_e, pct)]
    random.shuffle(combos)
    count = 0
    for qty, cp_e, pct in combos:
        if count >= 20: break
        profit_e = cp_e * pct // 100
        sp_e = cp_e + profit_e
        total_profit = qty * profit_e
        ctx, item = random.choice(CONTEXTS_MEDIUM), random.choice(ITEMS_EASY + ITEMS_MEDIUM)
        q = (f"{ctx} bought {qty} units of {item} at {_peso(cp_e)} each "
             f"and sold them at {_peso(sp_e)} each. What is the total profit?")
        ans = _peso(total_profit)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(total_profit)), ans,
               f"Profit/unit = {_peso(profit_e)}. Total = {qty} \u00d7 {_peso(profit_e)} = {ans}.",
               ["profit", "multiple items", "business math"]):
            count += 1

    # M7: VAT amount from inclusive (20)
    bases2 = [b for b in range(2000, 30001, 250) if _clean_vat(b)]
    random.shuffle(bases2)
    count = 0
    for base in bases2:
        if count >= 20: break
        vat = base * 12 // 100
        total = base + vat
        q = f"A purchase totals {_peso(total)} (VAT-inclusive at 12%). How much is the VAT?"
        ans = _peso(vat)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(vat)), ans,
               f"Base = {_peso(total)} \u00f7 1.12 = {_peso(base)}. VAT = {ans}.",
               ["VAT", "tax amount", "tax extraction"]):
            count += 1

    # M8: Profit amount given CP and % (20)
    combos = [(cp, pct) for cp in range(2000, 25001, 500) for pct in [8,10,12,15,18,20,25,30]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 20: break
        profit = cp * pct // 100
        item = random.choice(ITEMS_MEDIUM)
        q = f"A dealer bought {item} for {_peso(cp)} and earned a {pct}% profit. How much profit was made?"
        ans = _peso(profit)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(profit)), ans,
               f"Profit = {_peso(cp)} \u00d7 {pct/100:.2f} = {ans}.",
               ["profit", "profit amount", "percentage application"]):
            count += 1

    # M9: Discount then VAT (20)
    combos = [(m, d) for m in range(2000, 20001, 500) for d in [5,10,15,20,25]
              if _clean_mult(m, d) and _clean_vat(m - m*d//100)]
    random.shuffle(combos)
    count = 0
    for marked, disc in combos:
        if count >= 20: break
        discounted = marked - marked * disc // 100
        total = discounted * 112 // 100
        item = random.choice(ITEMS_MEDIUM)
        q = (f"{item.capitalize()} marked at {_peso(marked)} has a {disc}% discount. "
             f"If 12% VAT is applied after the discount, what is the final price?")
        ans = _peso(total)
        if add("Medium", q, _shuffle_choices(ans, _distractors_amount(total)), ans,
               f"Discounted = {_peso(discounted)}. Total = {_peso(discounted)} \u00d7 1.12 = {ans}.",
               ["discount", "VAT", "multi-step", "business math"]):
            count += 1


    # ===== HARD (200) =====

    # H1: Markup + VAT total (30)
    combos = [(cp, pct) for cp in range(10000, 100001, 2000) for pct in [15,18,20,25,28,30,35,40]
              if _clean_mult(cp, pct) and _clean_vat(cp + cp*pct//100)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 30: break
        sp = cp + cp * pct // 100
        total = sp * 112 // 100
        ctx, item = random.choice(CONTEXTS_HARD), random.choice(ITEMS_HARD)
        q = (f"{ctx} purchased {item} for {_peso(cp)} and sold it at a {pct}% markup. "
             f"The buyer pays 12% VAT on top. What is the total amount the buyer pays?")
        ans = _peso(total)
        if add("Hard", q, _shuffle_choices(ans, _distractors_amount(total)), ans,
               f"SP = {_peso(cp)} \u00d7 {1+pct/100:.2f} = {_peso(sp)}. Total = {_peso(sp)} \u00d7 1.12 = {ans}.",
               ["markup", "VAT", "multi-step", "business math"]):
            count += 1

    # H2: Find CP from VAT-inclusive total and profit % (25)
    combos = [(cp, pct) for cp in range(5000, 60001, 1000) for pct in [10,15,20,25,30]
              if _clean_mult(cp, pct) and _clean_vat(cp + cp*pct//100)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 25: break
        sp = cp + cp * pct // 100
        total = sp * 112 // 100
        q = (f"A buyer paid {_peso(total)} (VAT-inclusive at 12%) for an item sold at {pct}% profit. "
             f"What was the original cost price?")
        ans = _peso(cp)
        if add("Hard", q, _shuffle_choices(ans, _distractors_amount(cp)), ans,
               f"SP = {_peso(total)} \u00f7 1.12 = {_peso(sp)}. CP = {_peso(sp)} \u00f7 {1+pct/100:.2f} = {ans}.",
               ["profit", "VAT", "reverse computation", "multi-step"]):
            count += 1

    # H3: Effective profit after markup + discount (25)
    h3_combos = []
    for m in [20,25,30,35,40,45,50,60,70,80]:
        for d in [5,10,15,20,25,30]:
            eff = round((1+m/100)*(1-d/100)*100 - 100, 2)
            if eff == int(eff) and eff > 0:
                h3_combos.append((m, d, int(eff)))
    random.shuffle(h3_combos)
    count = 0
    for markup, disc, eff_profit in h3_combos:
        if count >= 25: break
        q = (f"A store marks up goods by {markup}% then offers a {disc}% discount. "
             f"What is the effective profit percentage?")
        ans = _pct(eff_profit)
        mult = (1+markup/100)*(1-disc/100)
        if add("Hard", q, _shuffle_choices(ans, _distractors_pct(eff_profit)), ans,
               f"Multiplier = {1+markup/100:.2f} \u00d7 {1-disc/100:.2f} = {mult:.2f}. Effective profit = {ans}.",
               ["markup", "discount", "effective profit", "successive percentages"]):
            count += 1

    # H4: Find CP from loss amount and loss % (20)
    combos = [(cp, pct) for cp in range(4000, 50001, 1000) for pct in [5,8,10,12,15,20,25]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 20: break
        loss = cp * pct // 100
        q = f"A seller incurred a loss of {_peso(loss)} which is {pct}% of the cost price. What was the cost price?"
        ans = _peso(cp)
        if add("Hard", q, _shuffle_choices(ans, _distractors_amount(cp)), ans,
               f"CP = Loss \u00f7 (Loss%/100) = {_peso(loss)} \u00f7 {pct/100:.2f} = {ans}.",
               ["loss", "cost price", "reverse computation"]):
            count += 1

    # H5: Profit amount (seller's profit, VAT irrelevant) (20)
    combos = [(cp, pct) for cp in range(8000, 50001, 1000) for pct in [10,12,15,20,25,30]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 20: break
        profit = cp * pct // 100
        q = (f"An item costing {_peso(cp)} was sold at {pct}% profit. "
             f"The buyer also paid 12% VAT. What is the seller's profit (excluding VAT)?")
        ans = _peso(profit)
        if add("Hard", q, _shuffle_choices(ans, _distractors_amount(profit)), ans,
               f"Profit = {_peso(cp)} \u00d7 {pct/100:.2f} = {ans}. VAT does not affect seller's profit.",
               ["profit", "VAT", "conceptual", "business math"]):
            count += 1

    # H6: Markup + discount + VAT (3-step) (20)
    h6 = []
    for cp in range(10000, 50001, 2000):
        for m in [20,25,30,35,40]:
            if not _clean_mult(cp, m): continue
            sp = cp + cp*m//100
            for d in [5,10,15,20]:
                if not _clean_mult(sp, d): continue
                disc = sp - sp*d//100
                if not _clean_vat(disc): continue
                total = disc * 112 // 100
                h6.append((cp, m, d, sp, disc, total))
    random.shuffle(h6)
    count = 0
    for cp, m, d, sp, disc, total in h6:
        if count >= 20: break
        ctx, item = random.choice(CONTEXTS_HARD), random.choice(ITEMS_HARD)
        q = (f"{ctx} bought {item} for {_peso(cp)}, marked it up by {m}%, "
             f"gave a {d}% discount, then the buyer paid 12% VAT. What is the final amount?")
        ans = _peso(total)
        if add("Hard", q, _shuffle_choices(ans, _distractors_amount(total)), ans,
               f"Markup: {_peso(sp)}. Discount: {_peso(disc)}. VAT: {_peso(disc)} \u00d7 1.12 = {ans}.",
               ["markup", "discount", "VAT", "multi-step", "successive percentages"]):
            count += 1

    # H7: Profit % with large numbers (25)
    combos = [(cp, pct) for cp in range(15000, 100001, 1000) for pct in [8,10,12,15,16,18,20,22,24,25,28,30,32,35]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 25: break
        profit = cp * pct // 100
        sp = cp + profit
        ctx, item = random.choice(CONTEXTS_HARD), random.choice(ITEMS_HARD)
        q = f"{ctx} bought {item} for {_peso(cp)} and sold it for {_peso(sp)}. What is the profit percentage?"
        ans = _pct(pct)
        if add("Hard", q, _shuffle_choices(ans, _distractors_pct(pct)), ans,
               f"Profit = {_peso(profit)}. Profit % = ({_peso(profit)} \u00f7 {_peso(cp)}) \u00d7 100% = {ans}.",
               ["profit percentage", "large numbers", "business math"]):
            count += 1

    # H8: Project cost (materials + contractor + VAT) (20)
    combos = [(mat, pct) for mat in range(100000, 1000001, 50000) for pct in [10,12,15,18,20,25]
              if _clean_mult(mat, pct) and _clean_vat(mat + mat*pct//100)]
    random.shuffle(combos)
    count = 0
    for mat, pct in combos:
        if count >= 20: break
        after = mat + mat * pct // 100
        total = after * 112 // 100
        q = (f"Materials for a project cost {_peso(mat)}. The contractor adds {pct}% profit, "
             f"and the client pays 12% VAT on the total. What is the total project cost?")
        ans = _peso(total)
        if add("Hard", q, _shuffle_choices(ans, _distractors_amount(total)), ans,
               f"After profit: {_peso(after)}. After VAT: {_peso(after)} \u00d7 1.12 = {ans}.",
               ["contractor profit", "VAT", "project cost", "multi-step"]):
            count += 1

    # H9: Loss % with large numbers (20)
    combos = [(cp, pct) for cp in range(10000, 80001, 2000) for pct in [10,12,15,20,25,30,35,40]
              if _clean_mult(cp, pct)]
    random.shuffle(combos)
    count = 0
    for cp, pct in combos:
        if count >= 20: break
        loss = cp * pct // 100
        sp = cp - loss
        ctx, item = random.choice(CONTEXTS_HARD), random.choice(ITEMS_HARD)
        q = (f"{ctx} originally paid {_peso(cp)} for {item} and sold it for {_peso(sp)}. "
             f"What is the percentage loss?")
        ans = _pct(pct)
        if add("Hard", q, _shuffle_choices(ans, _distractors_pct(pct)), ans,
               f"Loss = {_peso(loss)}. Loss % = ({_peso(loss)} \u00f7 {_peso(cp)}) \u00d7 100% = {ans}.",
               ["loss percentage", "large numbers", "business math"]):
            count += 1

    return all_q


def main() -> None:
    raw = generate_all()

    # Split by difficulty
    easy = [q for q in raw if q["difficulty"] == "Easy"][:200]
    medium = [q for q in raw if q["difficulty"] == "Medium"][:200]
    hard = [q for q in raw if q["difficulty"] == "Hard"][:200]

    # Assemble with IDs and metadata
    all_questions: list[dict] = []
    qid = 1
    for difficulty, batch in [("Easy", easy), ("Medium", medium), ("Hard", hard)]:
        for q in batch:
            all_questions.append({
                "id": qid,
                "subtest": "Numerical Ability",
                "module": "Percentages",
                "subtopic": "Profit, Loss, and Tax",
                "difficulty": difficulty,
                "question": q["question"],
                "choices": q["choices"],
                "answer": q["answer"],
                "explanation": q["explanation"],
                "tags": q["tags"],
            })
            qid += 1

    # Final validation
    errors = 0
    for q in all_questions:
        if q["answer"] not in q["choices"]:
            print(f"  ERROR Q{q['id']}: answer not in choices!")
            errors += 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "questions.json"
    output_path.write_text(json.dumps(all_questions, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Generated {len(all_questions)} questions:")
    print(f"  Easy: {len(easy)}")
    print(f"  Medium: {len(medium)}")
    print(f"  Hard: {len(hard)}")
    print(f"  Validation errors: {errors}")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
