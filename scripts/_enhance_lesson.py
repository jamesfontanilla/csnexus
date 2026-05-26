"""Enhance a single lesson file with evidence-based pedagogical sections."""

import os
import re
import sys


def find_section_boundaries(lines):
    """Find line numbers of key section boundaries."""
    boundaries = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("### Mini Practice Set"):
            boundaries["mini_practice"] = i
        elif stripped.startswith("### Quick Recap") or stripped.startswith("## Quick Recap") or stripped.startswith("### Mastery Checklist") or stripped.startswith("## Mastery Checklist"):
            if "mastery" not in boundaries:
                boundaries["mastery_start"] = i
        elif stripped.startswith("### Exam Strategies") or stripped.startswith("## Exam Strategies"):
            boundaries["exam_strategies"] = i
        elif stripped.startswith("### Memory Aids") or stripped.startswith("## Memory Aids"):
            boundaries["memory_aids"] = i
        elif stripped.startswith("### Connections"):
            boundaries["connections"] = i
        elif stripped.startswith("### Mini Practice Set") or stripped.startswith("#### Practice Problems"):
            boundaries["mini_practice"] = i
    # Find the last content section (### 4.X) before exam strategies
    content_end = 0
    for i, line in enumerate(lines):
        if re.match(r"^###\s+4\.\d+", line.strip()):
            content_end = i
    boundaries["last_content_section_end"] = content_end
    return boundaries


def get_check_your_understanding(topic_slug):
    """Generate Check Your Understanding blocks for a topic."""
    prompts = {
        "types-of-ratios": [
            {
                "after_section": "part-to-whole",
                "questions": [
                    ("What is the key difference between part-to-part and part-to-whole ratios?",
                     "Part-to-part compares two subgroups; part-to-whole compares one subgroup to the total (the second term IS the whole in part-to-whole)"),
                    ("If the ratio of passed to failed examinees is 5:3, what is the total number of parts?",
                     "8 parts (add 5 + 3; the whole equals the sum of both parts)"),
                    ("You have 8 red balls and 12 blue balls. What is the part-to-part ratio? What is red:total?",
                     "red:blue = 8:12 = 2:3 (part-to-part); red:total = 8:20 = 2:5 (part-to-whole)"),
                ]
            },
            {
                "after_section": "unit-ratios",
                "questions": [
                    ("How do you test if 6:9 and 10:15 are equivalent?",
                     "Cross-multiply: 6×15=90 and 9×10=90; equal products → equivalent (both simplify to 2:3)"),
                    ("A car travels 450 km on 30 liters. What is the unit ratio?",
                     "15:1, or 15 km per liter (divide both terms by 30: 450÷30=15, 30÷30=1)"),
                    ("What separates a unit ratio from a regular simplified ratio?",
                     "The second term must be exactly 1 (a simplified ratio like 2:3 is not a unit ratio because the second term is not 1)"),
                ]
            },
        ],
        "direct-and-inverse-proportions": [
            {
                "after_section": "direct",
                "questions": [
                    ("If 5 pens cost ₱75, what type of proportion relates the number of pens to their cost?",
                     "Direct proportion (more pens → more cost; the ratio pens:cost stays constant)"),
                    ("What is the formula for solving a direct proportion a₁/b₁ = a₂/b₂?",
                     "Cross-multiply: a₁×b₂ = b₁×a₂, then solve for the unknown"),
                    ("A car travels 210 km on 15 liters. How can you verify this is a direct proportion situation?",
                     "Check if km per liter (210÷15=14) stays constant — if the rate per unit is fixed, it's a direct proportion"),
                ]
            },
            {
                "after_section": "inverse-work",
                "questions": [
                    ("If 6 workers finish a job in 10 days, what type of proportion relates workers to days?",
                     "Inverse proportion (more workers → fewer days; the product workers×days stays constant)"),
                    ("What is the fundamental difference between direct and inverse proportion formulas?",
                     "Direct: a₁/b₁ = a₂/b₂ (ratio constant); Inverse: a₁×b₁ = a₂×b₂ (product constant)"),
                    ("A tank fills in 6 hours with 4 taps. If you open 8 taps, will the time double, halve, or stay the same?",
                     "Halve to 3 hours (inverse: 4×6 = 8×x → x=3) — twice the taps mean half the time"),
                ]
            },
        ],
    }
    return prompts.get(topic_slug, [
        {
            "after_section": "default",
            "questions": [
                ("What is the key concept from this section?",
                 "Review the preceding content to recall the main principle"),
                ("How would you apply this concept to a practical problem?",
                 "Identify the type of relationship, set up the correct equation, and solve step by step"),
                ("What common mistake should you avoid here?",
                 "Check the Common Mistakes section — verify your answer doesn't fall into these traps"),
            ]
        },
    ])


def get_elaborative_interrogations(topic_slug):
    """Generate elaborative interrogation callouts."""
    callouts = {
        "types-of-ratios": [
            ("> 🤔 **Why does this work?** A part-to-part ratio compares two disjoint subsets — neither includes the other. The two parts together may or may not equal the whole (there could be a third category). This is why adding the terms of a part-to-part ratio only gives you the total when exactly two categories cover everything. Understanding this distinction is what separates correct from incorrect answers on the CSE.\n"),
            ("> 🤔 **Why does this work?** Equivalent ratios preserve the proportional relationship because multiplying or dividing both terms by the same number (k) is equivalent to multiplying by k/k = 1 — you're not changing the value of the ratio, just expressing it differently. Cross-multiplication works because a:b = c:d means a/b = c/d, and multiplying both sides by b×d gives a×d = b×c.\n"),
            ("> 🤔 **Why does this work?** A unit ratio normalizes the second quantity to 1 so you can compare \"apples to apples.\" Dividing both terms by the second term's value is the same operation you use to convert any ratio to a unit ratio: a:b becomes (a÷b):1. This works because division by the same number preserves proportionality — exactly the same principle behind equivalent ratios.\n"),
        ],
        "direct-and-inverse-proportions": [
            ("> 🤔 **Why does this work?** In a direct proportion, the ratio of corresponding values stays constant because both quantities scale together by the same factor. If one value doubles, the other must also double to maintain the proportion. This is why a₁/b₁ = a₂/b₂ — you're asserting that the two ratios represent the same relationship.\n"),
            ("> 🤔 **Why does this work?** Inverse proportion follows from the work-done principle: the total amount of work (or distance, or volume) is fixed. If you increase the rate (more workers, higher speed), the time must decrease proportionally so that rate × time = constant. This constant represents the total work being done.\n"),
            ("> 🤔 **Why does this work?** Cross-multiplication works because a proportion is an equation of two equal fractions. When a/b = c/d, multiplying both sides by b×d yields a×d = b×c. This eliminates the fractions and gives you a simple equation to solve, which is why it's the universal tool for any proportion problem.\n"),
        ],
    }
    return callouts.get(topic_slug, [
        ("> 🤔 **Why does this work?** The principle behind this operation follows from the fundamental properties of arithmetic. Understanding the \"why\" — not just the \"how\" — lets you recognize when to apply this method in unfamiliar problem contexts on the CSE.\n"),
        ("> 🤔 **Why does this work?** When you follow this procedure, you're exploiting a mathematical invariant — something that stays constant regardless of how you manipulate the numbers. Identifying that invariant is the key to solving problems efficiently rather than memorizing steps.\n"),
        ("> 🤔 **Why does this work?** This shortcut works because it's a special case of the more general rule. By understanding the underlying principle, you can verify your answer logically even if you forget the exact formula under exam pressure.\n"),
    ])


def get_misconceptions(topic_slug):
    """Generate misconception confrontation blocks."""
    misconceptions = {
        "types-of-ratios": [
            """> ⚠️ **Misconception:** "If the ratio of boys to girls is 2:3, then 2/3 of the students are boys."

> **Why it fails:** This confuses part-to-part with part-to-whole. The ratio 2:3 compares boys to girls — neither is the total. Since 2+3=5 parts total, boys represent 2/5 (40%) of the students, not 2/3 (67%). This error would overstate the boy population by 27 percentage points.

> **Correct model:** When you see a ratio written as A:B, always check whether the second term is another part or the total. Part-to-part ratios require you to ADD the parts to find the whole before computing any fraction or percentage.
""",
            """> ⚠️ **Misconception:** "6:10 and 3:5 are different ratios because the numbers are different."

> **Why it fails:** A ratio is about the *relationship*, not the specific numbers. Both 6:10 and 3:5 represent the same proportional relationship — the first term is 0.6 times the second term in both cases. In a classroom, "6 boys for every 10 girls" and "3 boys for every 5 girls" describe the exact same situation at different scales.

> **Correct model:** Two ratios are equivalent if they can be reduced to the same simplified form OR if cross-multiplication produces equal products. The numbers themselves can be completely different while describing identical proportions.
""",
        ],
        "direct-and-inverse-proportions": [
            """> ⚠️ **Misconception:** "If more workers are added, the work will always finish in less time."

> **Why it fails:** This only holds for inverse proportion. In direct proportion problems (like "more workers produce more items"), adding workers INCREASES output rather than decreasing time. You must first determine which type of proportion applies before deciding the direction of change.

> **Correct model:** Check the relationship: if both quantities move in the same direction (more → more), it's direct proportion. If they move in opposite directions (more → less), it's inverse proportion. The problem's context — not intuition — determines which rule applies.
""",
            """> ⚠️ **Misconception:** "All proportion problems can be solved by setting up a:b = c:d and cross-multiplying."

> **Why it fails:** This setup only works for direct proportion. For inverse proportion, the correct setup is a×b = c×d (product constant). Using the wrong formula gives a wrong answer. For example: "4 workers finish in 6 days. How long for 8 workers?" Direct setup 4/6 = 8/x gives x=12 days (wrong). Inverse setup 4×6 = 8×x gives x=3 days (correct).

> **Correct model:** Direct proportion uses ratio equality (a₁/b₁ = a₂/b₂). Inverse proportion uses product equality (a₁×b₁ = a₂×b₂). Always identify the type before choosing the formula.
""",
        ],
    }
    return misconceptions.get(topic_slug, [
        """> ⚠️ **Misconception:** "The formula always works the same way regardless of the problem context."

> **Why it fails:** CSE problems often present variations where the standard formula must be adapted. Blindly applying a memorized formula without checking the context leads to systematic errors.

> **Correct model:** Always read the problem to identify what type of relationship exists (direct, inverse, part-whole, etc.), then apply the appropriate formula. Verify your answer makes sense in the problem's context before selecting it.
""",
        """> ⚠️ **Misconception:** "If my computed answer is close to one of the choices, it must be right."

> **Why it fails:** The CSE deliberately includes distractors that result from common errors — using the wrong operation, misidentifying the proportion type, or reversing the ratio. A "close" answer could be the result of a systematic mistake that the test writers anticipated.

> **Correct model:** Verify your setup before computing. Check that you've identified the correct proportion type, set up the equation properly, and solved accurately. A wrong setup with correct arithmetic still produces a wrong answer — and the CSE will include that wrong answer among the choices.
""",
    ])


def get_guided_practice(topic_slug):
    """Generate guided practice faded examples."""
    practice = {
        "types-of-ratios": """### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** A factory has 150 male workers and 100 female workers. Find the part-to-whole ratio of male workers to total.

- Step 1: Compute total: 150 + 100 = _____
- Step 2: Write male:total = _____:_____
- Step 3: Simplify by dividing by GCF: _____:_____

**Answer:** Total = 250. male:total = 150:250. GCF of 150 and 250 = 50. 150÷50=3, 250÷50=5. Result: 3:5

**2.** Determine if 14:21 and 8:12 are equivalent ratios.

- Step 1: Simplify 14:21 — GCF = 7 → _____:_____
- Step 2: Simplify 8:12 — GCF = 4 → _____:_____
- Step 3: Are the simplified forms equal? _____

**Answer:** 14:21 = 2:3. 8:12 = 2:3. Both simplify to 2:3 → equivalent.

**3.** Store X sells 6 cans for ₱210. Find the unit price.

- Step 1: Write the ratio: _____:_____
- Step 2: Divide both terms by 6: _____:_____
- Step 3: Interpret: ₱_____ per can

**Answer:** Ratio: 210:6. Divide both by 6: 35:1. Unit price: ₱35 per can.

**4.** The ratio of passed to failed is 7:3. If 420 passed, find the number who failed.

- Step 1: 7 parts = _____ examinees, so 1 part = _____
- Step 2: Failed = 3 × _____ = _____
- Step 3: Total = 420 + _____ = _____

**Answer:** 7 parts = 420, so 1 part = 60. Failed = 3×60 = 180. Total = 420+180 = 600.

**5.** A barangay budget allocates funds in the ratio education:health:infrastructure = 5:3:2. If the total is ₱800,000, how much goes to health?

- Step 1: Total parts = 5 + 3 + 2 = _____
- Step 2: 1 part = ₱800,000 ÷ _____ = ₱_____
- Step 3: Health = 3 × _____ = ₱_____

**Answer:** Total parts = 10. 1 part = ₱800,000 ÷ 10 = ₱80,000. Health = 3 × ₱80,000 = ₱240,000.
""",
        "direct-and-inverse-proportions": """### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** If 4 kg of rice costs ₱220, how much does 7 kg cost?

- Step 1: Identify proportion type: more kg → more cost → _____ proportion
- Step 2: Set up: 4/220 = 7/_____
- Step 3: Cross-multiply: 4 × _____ = 220 × 7
- Step 4: Solve: _____ = 1,540 ÷ 4 = _____

**Answer:** Direct proportion. 4/220 = 7/x. 4x = 1,540. x = 385. Cost: ₱385

**2.** A car at 60 km/h takes 5 hours. How long at 75 km/h?

- Step 1: Identify proportion type: more speed → less time → _____ proportion
- Step 2: Set up: 60 × 5 = 75 × _____
- Step 3: Solve: 300 = 75 × _____ → _____ = _____

**Answer:** Inverse proportion. 60×5 = 75×x. 300 = 75x. x = 4 hours.

**3.** A builder estimates 8 workers finish a wall in 15 days. After 5 days, 2 workers leave. How many more days needed?

- Step 1: Work done in 5 days: 8 × 5 = _____ worker-days
- Step 2: Total work: 8 × 15 = _____ worker-days
- Step 3: Remaining work: _____ - _____ = _____
- Step 4: Remaining workers: _____
- Step 5: Days needed: _____ ÷ _____ = _____

**Answer:** 40 worker-days done. Total: 120. Remaining: 80 worker-days. 6 workers left. 80÷6 ≈ 13.33 → 14 more days.

**4.** A pump fills a pool in 12 hours. How long with 3 identical pumps?

- Step 1: Identify proportion type: more pumps → less time → _____ proportion
- Step 2: Set up: 1 × 12 = 3 × _____
- Step 3: Solve: _____ = _____

**Answer:** Inverse proportion. 1×12 = 3×x. x = 4 hours.

**5.** A factory's 10 machines produce 500 units in 6 hours. How many units with 15 machines in 4 hours?

- Step 1: Rate per machine-hour: 500 ÷ (10 × 6) = _____ units per machine-hour
- Step 2: New production: 15 × 4 × _____ = _____ units

**Answer:** Rate = 500÷60 = 8.33 units/machine-hour. New: 15×4×8.33 = 500 units.
""",
    }
    return practice.get(topic_slug, """### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** [Example 1]

- Step 1: Identify the relationship: _____
- Step 2: Set up the equation: _____
- Step 3: Solve: _____

**Answer:** [Complete solution]

**2.** [Example 2]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]

**3.** [Example 3]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]

**4.** [Example 4]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]

**5.** [Example 5]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]
""")


def get_which_method(topic_slug):
    """Generate Which Method? interleaved practice."""
    methods = {
        "types-of-ratios": """### Which Method?

For each problem, identify the ratio type and solve.

**1.** A survey shows 120 agree and 80 disagree. What is agree:total?
- **Type:** Part-to-whole (agree compared to total respondents)
- **Answer:** 120:200 = 3:5
- **Why:** Total = 120+80 = 200. agree:total = 120:200, simplify by GCF 40 → 3:5.

**2.** Which of these is equivalent to 5:8? (a) 10:16 (b) 15:20 (c) 25:32
- **Type:** Equivalent ratio identification (test each option)
- **Answer:** (a) 10:16
- **Why:** 5×2=10, 8×2=16 ✓. (b) 15:20 → ×3 and ×2.5 — not same multiplier. (c) 25:32 → ×5 and ×4 — not same multiplier.

**3.** A printer produces 1,440 pages in 12 minutes. What is the printing rate per minute?
- **Type:** Unit ratio (rate per one minute)
- **Answer:** 120 pages per minute
- **Why:** 1,440:12 → divide both by 12 → 120:1. Unit ratio = 120 pages per minute.

**4.** In a barangay of 500 residents, the ratio of registered to unregistered voters is 3:2. How many are registered?
- **Type:** Part-to-part with scaling (find actual values from ratio)
- **Answer:** 300 registered voters
- **Why:** Total parts = 5. 1 part = 500÷5 = 100. Registered = 3×100 = 300.

**5.** A recipe uses 3 cups of flour for every 2 cups of sugar. If you use 12 cups of flour, how much sugar?
- **Type:** Equivalent ratio (scaling up from given ratio)
- **Answer:** 8 cups
- **Why:** 3:2 = 12:? → multiplier = 12÷3 = 4 → sugar = 2×4 = 8.

**6.** The ratio of boys to total students is 2:5. If there are 30 boys, how many are NOT boys?
- **Type:** Part-to-whole with reverse calculation
- **Answer:** 45 non-boys (girls + others)
- **Why:** 2 parts = 30, so 1 part = 15. Total = 5×15 = 75. Non-boys = 75-30 = 45.
""",
        "direct-and-inverse-proportions": """### Which Method?

For each problem, identify the proportion type and solve.

**1.** If 8 pens cost ₱120, how much do 14 pens cost?
- **Type:** Direct proportion (more pens → more cost)
- **Answer:** ₱210
- **Why:** 8/120 = 14/x → 8x = 1,680 → x = 210. Rate per pen is constant (₱15/pen).

**2.** A vehicle at 80 km/h takes 3 hours. How long at 60 km/h?
- **Type:** Inverse proportion (more speed → less time)
- **Answer:** 4 hours
- **Why:** 80×3 = 60×x → 240 = 60x → x = 4. Distance is constant (240 km).

**3.** 12 workers build a road in 20 days. How many workers needed to finish in 8 days?
- **Type:** Inverse proportion (more workers → fewer days)
- **Answer:** 30 workers
- **Why:** 12×20 = x×8 → 240 = 8x → x = 30. Total work constant (240 worker-days).

**4.** A car uses 15 liters for 180 km. How far can it go on 25 liters?
- **Type:** Direct proportion (more fuel → more distance)
- **Answer:** 300 km
- **Why:** 15/180 = 25/x → 15x = 4,500 → x = 300. Fuel efficiency constant (12 km/L).

**5.** A machine fills 200 bottles in 5 hours. How many bottles in 8 hours?
- **Type:** Direct proportion (more time → more bottles)
- **Answer:** 320 bottles
- **Why:** 5/200 = 8/x → 5x = 1,600 → x = 320. Rate constant (40 bottles/hour).

**6.** 4 taps fill a tank in 15 hours. How long for 6 taps?
- **Type:** Inverse proportion (more taps → less time)
- **Answer:** 10 hours
- **Why:** 4×15 = 6×x → 60 = 6x → x = 10. Tank volume constant.
""",
    }
    return methods.get(topic_slug, """### Which Method?

For each problem, identify the type and solve.

**1.** [Problem 1]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**2.** [Problem 2]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**3.** [Problem 3]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**4.** [Problem 4]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**5.** [Problem 5]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**6.** [Problem 6]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]
""")


def get_before_you_practice(topic_slug):
    """Generate Before You Practice confidence check."""
    checks = {
        "types-of-ratios": """### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Distinguish part-to-part from part-to-whole ratios based on wording
- [ ] Simplify ratios and verify equivalence using cross-multiplication
- [ ] Calculate unit ratios and interpret them as rates
- [ ] Convert between part-to-part and part-to-whole ratios
- [ ] Scale ratios up and down using equivalent ratios
- [ ] Identify the correct ratio type in CSE word problems
""",
        "direct-and-inverse-proportions": """### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Identify direct and inverse proportion from problem wording
- [ ] Set up proportion equations correctly (direct: a₁/b₁ = a₂/b₂; inverse: a₁×b₁ = a₂×b₂)
- [ ] Cross-multiply and solve proportion equations accurately
- [ ] Solve multi-step proportion problems (work rate, combined proportions)
- [ ] Verify answers by checking if the result makes logical sense
- [ ] Distinguish direct vs. inverse proportion under exam time pressure
""",
    }
    return checks.get(topic_slug, """### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Identify the type of problem and select the appropriate method
- [ ] Set up the correct equation or formula for the problem
- [ ] Execute calculations accurately and efficiently
- [ ] Verify answers by checking reasonableness
- [ ] Apply concepts to CSE-style word problems
- [ ] Avoid common mistakes and traps in this topic
""")


def get_connections(topic_slug):
    """Generate Connections transfer bridge."""
    connections = {
        "types-of-ratios": """### Connections

How this topic connects to other areas of the CSE:

- **Introduction to Ratios:** The fundamental ratio concepts from that lesson — writing ratios, identifying quantities — are the foundation for distinguishing between ratio types here
- **Ratio Word Problems:** Every ratio word problem requires you to first classify the ratio type before solving — misidentifying part-to-part as part-to-whole changes the entire calculation
- **Direct and Inverse Proportions:** Unit ratios are directly applied in proportion problems — the constant of proportionality is essentially a unit ratio
- **Percentages:** A percentage is a part-to-whole ratio with the whole normalized to 100 — converting 3:5 to 60% requires the concept of equivalent ratios
- **Fractions (Basic Operations):** A part-to-whole ratio like 3:8 is identical to the fraction 3/8 — ratio types bridge directly to fraction concepts
""",
        "direct-and-inverse-proportions": """### Connections

How this topic connects to other areas of the CSE:

- **Ratio Word Problems:** Proportion problems are ratio problems with an unknown — the setup and cross-multiplication skills transfer directly
- **Types of Ratios:** Understanding part-to-part, part-to-whole, and unit ratios is prerequisite for identifying which proportion type applies
- **Percentage Applications:** Percentage increase/decrease problems are direct proportion problems where the "per hundred" rate is the constant
- **Average Word Problems:** Finding a weighted average requires proportional reasoning — each group's contribution is proportional to its size
- **Fractions (Basic Operations):** Cross-multiplication in proportions is identical to finding equivalent fractions — the same mathematical operation
""",
    }
    return connections.get(topic_slug, """### Connections

How this topic connects to other areas of the CSE:

- **[Related Topic 1]:** [How this skill transfers or applies to that topic]
- **[Related Topic 2]:** [How understanding this concept helps with that topic]
- **[Related Topic 3]:** [Structural similarity between this and that topic]
- **[Related Topic 4]:** [How this skill is a prerequisite for that topic]
- **[Related Topic 5]:** [How both topics use similar reasoning or methods]
""")


def insert_content(lines, position, content):
    """Insert content at a specific line position."""
    if isinstance(content, str):
        content = content.splitlines(True)
    else:
        content = [l + "\n" if not l.endswith("\n") else l for l in content]
    # Ensure content ends with newlines if it doesn't
    if content and not content[-1].endswith("\n"):
        content[-1] += "\n"
    # Add separator before new section
    result = []
    for i, line in enumerate(lines):
        result.append(line)
        if i == position:
            result.append("\n")
            result.extend(content)
    return result


def enhance_lesson(filepath, topic_slug):
    """Enhance a single lesson file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines(True)
    boundaries = find_section_boundaries(lines)
    
    # Get content for this topic
    check_blocks = get_check_your_understanding(topic_slug)
    interrogations = get_elaborative_interrogations(topic_slug)
    misconceptions_list = get_misconceptions(topic_slug)
    guided_practice = get_guided_practice(topic_slug)
    which_method = get_which_method(topic_slug)
    before_practice = get_before_you_practice(topic_slug)
    connections = get_connections(topic_slug)

    # Already enhanced?
    has_guided = any("### Guided Practice" in l for l in lines)
    has_which = any("### Which Method?" in l for l in lines)
    has_before = any("### Before You Practice" in l for l in lines)
    has_connections = any("### Connections" in l for l in lines)
    has_check = any("### Check Your Understanding" in l for l in lines)
    has_why = any("🤔" in l for l in lines)

    if all([has_guided, has_which, has_before, has_connections, has_check, has_why]):
        print(f"  {topic_slug}: Already enhanced, skipping")
        return

    # Find content section boundaries for inserting Check Your Understanding blocks
    section_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^###\s+4\.\d+", stripped):
            section_starts.append((i, stripped))

    # Insert elaborative interrogations after the 1st, 3rd, and 5th content sections
    interrog_idx = 0
    if len(section_starts) >= 5:
        targets = [section_starts[0], section_starts[2], section_starts[4]]
    elif len(section_starts) >= 3:
        targets = [section_starts[0], section_starts[1], section_starts[2]]
    else:
        targets = section_starts[:]

    # We'll build the enhanced file by tracking insertions from bottom to top
    insertions = []  # (line_number, content_to_insert)
    
    # Insert Connections before Mastery Checklist
    mastery_idx = boundaries.get("mastery_start")
    if mastery_idx and not has_connections:
        insertions.append((mastery_idx - 1, "\n---\n\n" + connections + "\n"))

    # Find insertion point: Mini Practice Set, or fallback to before mastery/quick recap
    mini_idx = boundaries.get("mini_practice")
    fallback_idx = boundaries.get("mastery_start")
    
    # If no mini_practice, use mastery_start as insertion point
    insert_before = mini_idx if mini_idx is not None else (fallback_idx if fallback_idx else None)

    if insert_before is not None:
        if not has_guided:
            insertions.append((insert_before - 1, "\n---\n\n" + guided_practice + "\n"))
        if not has_which:
            insertions.append((insert_before - 1, "\n---\n\n" + which_method + "\n"))
        if not has_before:
            insertions.append((insert_before - 1, "\n---\n\n" + before_practice + "\n"))

    # Insert misconceptions near relevant content sections
    misconception_inserts = []
    for i, (line_num, _) in enumerate(section_starts):
        if i >= len(misconceptions_list):
            break
        # Find end of this section (next section start or next ---)
        end = line_num
        for j in range(line_num + 1, len(lines)):
            if re.match(r"^###\s+4\.\d+", lines[j].strip()) or lines[j].strip() == "---":
                end = j - 1
                break
        if end > line_num + 10:  # Section has enough content
            misconception_inserts.append((end, misconceptions_list[i]))

    # Only insert if not already there
    if not has_why:
        for line_num, mc in misconception_inserts[:2]:  # At least 2
            insertions.append((line_num, "\n" + mc + "\n"))

    # Insert elaborative interrogations after key sections
    if not has_why:
        for idx, (line_num, section_title) in enumerate(targets[:3]):
            text = interrogations[min(idx, len(interrogations)-1)]
            insertions.append((line_num, text + "\n"))

    # Insert Check Your Understanding blocks
    if not has_check:
        for block_idx, block in enumerate(check_blocks[:2]):
            # Find where to insert: after the 3rd and 6th content sections
            if block_idx == 0 and len(section_starts) >= 3:
                pos = section_starts[2][0] - 1  # before the 3rd content section
            elif block_idx == 1 and len(section_starts) >= 6:
                pos = section_starts[5][0] - 1
            elif len(section_starts) > 0:
                pos = section_starts[-1][0]  # end of last section
            else:
                continue
            
            check_text = "### Check Your Understanding\n\n"
            for j, (q, a) in enumerate(block["questions"], 1):
                check_text += f"**{j}.** {q} → **{a}**\n\n"
            check_text += "---\n"
            insertions.append((pos, "\n" + check_text + "\n"))

    # Sort insertions by line number (descending to preserve indices)
    insertions.sort(key=lambda x: x[0], reverse=True)

    # Apply insertions
    result = list(lines)
    for line_num, text in insertions:
        line_num = min(line_num, len(result) - 1)
        if isinstance(text, str):
            text_lines = text.splitlines(True)
        else:
            text_lines = text
        # Insert after line_num
        for j, tl in enumerate(reversed(text_lines)):
            result.insert(line_num + 1, tl)

    # Write back
    enhanced = "".join(result)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(enhanced)
    print(f"  {topic_slug}: Enhanced ({len(result)} lines)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        print("Usage: python _enhance_lesson.py <path/to/lesson.md>")
        sys.exit(1)

    # Determine topic slug from path
    topic_slug = os.path.basename(os.path.dirname(filepath))
    print(f"Enhancing: {topic_slug}")
    enhance_lesson(filepath, topic_slug)