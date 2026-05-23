"""
Generate 600 multiple-choice questions for Scale and Map Problems subtopic.
200 Easy / 200 Medium / 200 Hard
"""

import json
import random
import math

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
        "subtopic": "Scale and Map Problems",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })


def shuffle_choices(correct, distractors):
    """Return shuffled choices list and the correct answer string."""
    all_choices = [correct] + distractors
    random.shuffle(all_choices)
    return all_choices, correct


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Type 1: Map to Actual (simple scales, whole numbers) ---
easy_scales_100k = [
    (1, 100000), (2, 100000), (3, 100000), (4, 100000), (5, 100000),
    (6, 100000), (7, 100000), (8, 100000), (9, 100000), (10, 100000),
]

for map_cm, scale in easy_scales_100k:
    actual_cm = map_cm * scale
    actual_km = actual_cm / 100000
    correct = f"{int(actual_km)} km"
    d1 = f"{int(actual_km * 10)} km"
    d2 = f"{int(actual_km) * 100} km" if actual_km >= 1 else f"{actual_km * 0.1:.1f} km"
    d3 = f"{max(1, int(actual_km) - 1)} km" if actual_km > 1 else "0.5 km"
    # Ensure unique distractors
    distractors = []
    for d in [d1, d2, d3]:
        if d != correct and d not in distractors:
            distractors.append(d)
    while len(distractors) < 3:
        distractors.append(f"{int(actual_km) + len(distractors) + 2} km")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"A map has a scale of 1:100,000. If two points are {map_cm} cm apart on the map, what is the actual distance?",
          choices, ans,
          f"At scale 1:100,000, 1 cm = 1 km. So {map_cm} cm = {int(actual_km)} km.",
          ["scale", "map-to-actual", "unit conversion"])

# --- Type 2: Map to Actual (1:50,000) ---
for i in range(10):
    map_cm = random.choice([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
    scale = 50000
    actual_km = (map_cm * scale) / 100000
    correct = f"{actual_km:.0f} km" if actual_km == int(actual_km) else f"{actual_km} km"
    d1 = f"{actual_km * 2:.0f} km"
    d2 = f"{actual_km / 2:.1f} km" if actual_km / 2 != int(actual_km / 2) else f"{int(actual_km / 2)} km"
    d3 = f"{actual_km + 3:.0f} km"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{actual_km + len(distractors) + 5:.0f} km")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"On a map with scale 1:50,000, two locations are {map_cm} cm apart. What is the actual distance in kilometers?",
          choices, ans,
          f"Actual = {map_cm} × 50,000 = {map_cm * 50000:,} cm = {actual_km} km.",
          ["scale", "map-to-actual", "1:50,000"])

# --- Type 3: What does 1 cm represent? ---
easy_scales_interpret = [
    (25000, "250 m"), (50000, "500 m"), (100000, "1 km"),
    (200000, "2 km"), (500000, "5 km"), (1000000, "10 km"),
    (10000, "100 m"), (20000, "200 m"), (75000, "750 m"), (150000, "1.5 km"),
]

for scale, correct in easy_scales_interpret:
    if "km" in correct:
        val = float(correct.replace(" km", ""))
        d1 = f"{val * 10} km"
        d2 = f"{val / 10} km" if val / 10 >= 0.1 else "50 m"
        d3 = f"{val * 2} km"
    else:
        val = float(correct.replace(" m", ""))
        d1 = f"{int(val * 10)} m"
        d2 = f"{int(val / 10)} m" if val >= 10 else "5 m"
        d3 = f"{int(val + 100)} m"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(val) + 50} m")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"On a map with scale 1:{scale:,}, what actual distance does 1 cm represent?",
          choices, ans,
          f"1 cm = {scale:,} cm. Converting: {scale:,} cm = {correct}.",
          ["scale", "interpretation", "unit conversion"])

# --- Type 4: Actual to Map (simple) ---
for i in range(15):
    actual_km = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    scale = 100000
    map_cm = (actual_km * 100000) / scale
    correct = f"{int(map_cm)} cm"
    d1 = f"{int(map_cm * 2)} cm"
    d2 = f"{int(map_cm / 2)} cm" if map_cm >= 2 else "0.5 cm"
    d3 = f"{int(map_cm) + 3} cm"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(map_cm) + len(distractors) + 4} cm")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"A map has a scale of 1:100,000. If the actual distance between two towns is {actual_km} km, how far apart are they on the map?",
          choices, ans,
          f"At 1:100,000, 1 km = 1 cm on the map. So {actual_km} km = {int(map_cm)} cm.",
          ["scale", "actual-to-map", "1:100,000"])

# --- Type 5: Written scale, map to actual ---
written_scales = [
    ("1 cm represents 2 km", 2), ("1 cm represents 3 km", 3),
    ("1 cm represents 5 km", 5), ("1 cm represents 4 km", 4),
    ("1 cm represents 10 km", 10), ("1 cm represents 0.5 km", 0.5),
    ("1 cm represents 1 km", 1), ("1 cm represents 8 km", 8),
    ("1 cm represents 6 km", 6), ("1 cm represents 7 km", 7),
]

for i in range(15):
    desc, km_per_cm = random.choice(written_scales)
    map_cm = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    actual_km = map_cm * km_per_cm
    correct = f"{actual_km:.0f} km" if actual_km == int(actual_km) else f"{actual_km} km"
    d1 = f"{actual_km + km_per_cm:.0f} km" if (actual_km + km_per_cm) == int(actual_km + km_per_cm) else f"{actual_km + km_per_cm} km"
    d2 = f"{actual_km * 2:.0f} km" if actual_km * 2 == int(actual_km * 2) else f"{actual_km * 2} km"
    d3 = f"{max(1, actual_km - km_per_cm):.0f} km" if (actual_km - km_per_cm) == int(actual_km - km_per_cm) else f"{max(0.5, actual_km - km_per_cm)} km"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{actual_km + 10 + len(distractors)} km")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f'A map uses the scale "{desc}." If two cities are {map_cm} cm apart on the map, what is the actual distance?',
          choices, ans,
          f"Each cm = {km_per_cm} km. So {map_cm} cm = {map_cm} × {km_per_cm} = {actual_km} km.",
          ["scale", "written scale", "map-to-actual"])

# --- Type 6: Identify scale type ---
scale_type_qs = [
    ("1:50,000", "Ratio scale", ["Written scale", "Graphic scale", "Verbal scale"]),
    ("1 cm represents 5 km", "Written scale", ["Ratio scale", "Graphic scale", "Bar scale"]),
    ("A labeled bar printed on the map showing distances", "Graphic scale", ["Ratio scale", "Written scale", "Fractional scale"]),
    ("1:1,000,000", "Ratio scale", ["Statement scale", "Bar scale", "Linear scale"]),
    ("2 cm represents 10 km", "Written scale", ["Ratio scale", "Graphic scale", "Representative fraction"]),
]

for q_text, correct, dists in scale_type_qs:
    choices, ans = shuffle_choices(correct, dists)
    add_q("Easy",
          f'What type of scale representation is this: "{q_text}"?',
          choices, ans,
          f'This is a {correct.lower()} because it {"uses a pure numerical ratio" if "Ratio" in correct else "states the relationship in words" if "Written" in correct else "uses a visual bar with markings"}.',
          ["scale", "scale types", "definition"])

# --- Type 7: Conceptual questions ---
conceptual_easy = [
    ("On a map with scale 1:100,000, which statement is correct?",
     "1 cm on the map equals 1 km in reality",
     ["1 km on the map equals 1 cm in reality", "1 cm on the map equals 100 m in reality", "1 cm on the map equals 10 km in reality"],
     "1:100,000 means 1 cm = 100,000 cm = 1 km."),
    ("If a map scale is 1:50,000, what does the number 50,000 represent?",
     "The actual distance is 50,000 times the map distance",
     ["The map distance is 50,000 times the actual distance", "The map covers 50,000 square km", "There are 50,000 landmarks on the map"],
     "In scale 1:n, n is the factor by which reality exceeds the map measurement."),
    ("Which map shows MORE detail of a small area?",
     "1:10,000",
     ["1:100,000", "1:1,000,000", "1:500,000"],
     "A smaller scale number (1:10,000) means less reduction, so more detail for a given paper size."),
    ("Which map covers a LARGER geographic area on the same paper size?",
     "1:1,000,000",
     ["1:10,000", "1:50,000", "1:100,000"],
     "A larger scale number means more reduction, so a larger area fits on the same paper."),
    ("What is the first step when solving a scale problem?",
     "Identify the scale and what is being asked",
     ["Multiply all numbers together", "Convert to inches", "Draw a diagram"],
     "Always start by identifying the scale ratio and determining whether you need map→actual or actual→map."),
    ("In the scale 1:25,000, which number represents the map distance?",
     "1",
     ["25,000", "Both numbers", "Neither number"],
     "In scale notation map:actual, the first number (1) represents the map distance."),
    ("If you need to find the actual distance from a map measurement, you should:",
     "Multiply the map distance by the scale factor",
     ["Divide the map distance by the scale factor", "Add the scale factor to the map distance", "Subtract the map distance from the scale factor"],
     "Map to actual = multiply. The scale factor enlarges the small map measurement to real size."),
    ("If you need to find the map distance from an actual distance, you should:",
     "Divide the actual distance by the scale factor",
     ["Multiply the actual distance by the scale factor", "Add the scale factor", "Subtract the scale factor"],
     "Actual to map = divide. You shrink the real distance down to map size."),
    ("How many centimeters are in 1 kilometer?",
     "100,000",
     ["1,000", "10,000", "1,000,000"],
     "1 km = 1,000 m = 100,000 cm (multiply by 1,000 then by 100)."),
    ("A scale of 1:1 means:",
     "The drawing is the same size as the real object",
     ["The drawing is half the real size", "The drawing is double the real size", "The scale is invalid"],
     "1:1 means no enlargement or reduction — full size."),
]

for q, correct, dists, expl in conceptual_easy:
    choices, ans = shuffle_choices(correct, dists)
    add_q("Easy", q, choices, ans, expl, ["scale", "conceptual", "definition"])

# --- Type 8: Simple unit conversion in context ---
for i in range(15):
    km_val = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    cm_val = km_val * 100000
    correct = f"{cm_val:,} cm"
    d1 = f"{km_val * 1000:,} cm"
    d2 = f"{km_val * 10000:,} cm"
    d3 = f"{km_val * 1000000:,} cm"
    distractors = [d1, d2, d3]
    distractors = [d for d in distractors if d != correct][:3]
    while len(distractors) < 3:
        distractors.append(f"{cm_val + 50000:,} cm")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"How many centimeters are in {km_val} km?",
          choices, ans,
          f"{km_val} km × 100,000 = {cm_val:,} cm.",
          ["unit conversion", "km to cm"])

# --- Type 9: Blueprint scale (1:100, 1:200) ---
for i in range(15):
    scale = random.choice([100, 200, 500, 50])
    map_cm = random.choice([2, 3, 4, 5, 6, 7, 8, 10, 12, 15])
    actual_cm = map_cm * scale
    actual_m = actual_cm / 100
    correct = f"{int(actual_m)} m" if actual_m == int(actual_m) else f"{actual_m} m"
    d1 = f"{int(actual_m * 2)} m"
    d2 = f"{int(actual_m / 2)} m" if actual_m >= 2 else "0.5 m"
    d3 = f"{int(actual_m) + 5} m"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(actual_m) + 10 + len(distractors)} m")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"A building blueprint has a scale of 1:{scale}. A room measures {map_cm} cm on the blueprint. What is the actual length of the room?",
          choices, ans,
          f"Actual = {map_cm} × {scale} = {actual_cm:,} cm = {actual_m} m.",
          ["scale", "blueprint", "map-to-actual"])

# --- Type 10: Simple scale identification ---
for i in range(15):
    map_cm = random.choice([1, 2, 3, 4, 5])
    actual_km = random.choice([2, 3, 4, 5, 6, 8, 10])
    actual_cm = actual_km * 100000
    scale_val = actual_cm // map_cm
    correct = f"1:{scale_val:,}"
    d1 = f"1:{scale_val * 2:,}"
    d2 = f"1:{scale_val // 2:,}"
    d3 = f"1:{scale_val + 50000:,}"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"1:{scale_val + 100000 * (len(distractors) + 1):,}")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"Two points are {map_cm} cm apart on a map and {actual_km} km apart in reality. What is the map scale?",
          choices, ans,
          f"{actual_km} km = {actual_cm:,} cm. Scale = {map_cm}:{actual_cm:,} = 1:{scale_val:,}.",
          ["scale", "finding scale", "ratio"])

# --- Fill remaining easy to reach 200 ---
# Type 11: More map-to-actual with varied scales
additional_easy_scales = [
    (250000, 4), (250000, 8), (250000, 2), (250000, 6),
    (500000, 2), (500000, 4), (500000, 6), (500000, 10),
    (200000, 3), (200000, 5), (200000, 7), (200000, 9),
    (150000, 2), (150000, 4), (150000, 6), (150000, 10),
    (300000, 3), (300000, 5), (300000, 10), (400000, 2),
    (400000, 5), (400000, 8), (75000, 4), (75000, 8),
    (75000, 12), (125000, 4), (125000, 8), (125000, 16),
    (1000000, 2), (1000000, 3), (1000000, 5), (1000000, 7),
    (1000000, 10), (2000000, 1), (2000000, 3), (2000000, 5),
]

for scale, map_cm in additional_easy_scales:
    actual_cm = map_cm * scale
    actual_km = actual_cm / 100000
    if actual_km == int(actual_km):
        correct = f"{int(actual_km)} km"
    else:
        correct = f"{actual_km} km"
    d1_val = actual_km * 10
    d2_val = actual_km / 10
    d3_val = actual_km + 5
    d1 = f"{int(d1_val)} km" if d1_val == int(d1_val) else f"{d1_val} km"
    d2 = f"{d2_val} km" if d2_val >= 0.1 else "0.1 km"
    d3 = f"{int(d3_val)} km" if d3_val == int(d3_val) else f"{d3_val} km"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{actual_km + 2 + len(distractors)} km")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"On a map with scale 1:{scale:,}, a distance measures {map_cm} cm. What is the actual distance in kilometers?",
          choices, ans,
          f"Actual = {map_cm} × {scale:,} = {actual_cm:,} cm. Convert: {actual_cm:,} ÷ 100,000 = {actual_km} km.",
          ["scale", "map-to-actual", "unit conversion"])
    if len([q for q in questions if q["difficulty"] == "Easy"]) >= 200:
        break

# Pad if needed
while len([q for q in questions if q["difficulty"] == "Easy"]) < 200:
    map_cm = random.randint(1, 20)
    scale = random.choice([50000, 100000, 200000, 250000, 500000])
    actual_km = (map_cm * scale) / 100000
    correct = f"{actual_km:.1f} km" if actual_km != int(actual_km) else f"{int(actual_km)} km"
    d1 = f"{actual_km * 2:.1f} km"
    d2 = f"{actual_km / 2:.1f} km"
    d3 = f"{actual_km + 3:.1f} km"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{actual_km + 7 + len(distractors):.1f} km")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Easy",
          f"Scale: 1:{scale:,}. Map distance: {map_cm} cm. What is the actual distance?",
          choices, ans,
          f"{map_cm} × {scale:,} = {map_cm * scale:,} cm = {actual_km} km.",
          ["scale", "map-to-actual", "computation"])


print(f"Easy questions generated: {len([q for q in questions if q['difficulty'] == 'Easy'])}")

# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Type 1: Written scale, actual to map ---
for i in range(20):
    km_per_cm = random.choice([2, 2.5, 3, 4, 5, 6, 7.5, 8, 10, 12])
    actual_km = random.choice([12, 15, 18, 20, 24, 25, 28, 30, 35, 36, 40, 42, 45, 48, 50, 56, 60])
    map_cm = actual_km / km_per_cm
    if map_cm != int(map_cm):
        continue  # skip non-integer results for cleaner questions
    map_cm = int(map_cm)
    correct = f"{map_cm} cm"
    d1 = f"{map_cm + 2} cm"
    d2 = f"{map_cm * 2} cm"
    d3 = f"{max(1, map_cm - 2)} cm"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{map_cm + 4 + len(distractors)} cm")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Medium",
          f'A map uses the scale "1 cm represents {km_per_cm} km." If the actual distance between two cities is {actual_km} km, how far apart are they on the map?',
          choices, ans,
          f"Map distance = {actual_km} ÷ {km_per_cm} = {map_cm} cm.",
          ["scale", "actual-to-map", "written scale"])

# --- Type 2: Finding the scale ---
for i in range(20):
    map_cm = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15])
    actual_km = random.choice([4, 6, 8, 10, 12, 15, 16, 18, 20, 24, 25, 30, 40, 50])
    actual_cm_val = actual_km * 100000
    if actual_cm_val % map_cm != 0:
        continue
    scale_val = actual_cm_val // map_cm
    correct = f"1:{scale_val:,}"
    d1 = f"1:{scale_val * 2:,}"
    d2 = f"1:{scale_val // 2:,}"
    d3 = f"1:{scale_val + 100000:,}"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"1:{scale_val + 200000 * (len(distractors) + 1):,}")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Medium",
          f"On a map, two towns are {map_cm} cm apart. The actual distance between them is {actual_km} km. What is the scale of the map?",
          choices, ans,
          f"{actual_km} km = {actual_cm_val:,} cm. Scale = {map_cm}:{actual_cm_val:,} = 1:{scale_val:,}.",
          ["scale", "finding scale", "proportion"])

# --- Type 3: Convert written scale to ratio ---
written_to_ratio = [
    ("1 cm represents 2 km", "1:200,000", ["1:2,000", "1:20,000", "1:2,000,000"]),
    ("1 cm represents 5 km", "1:500,000", ["1:5,000", "1:50,000", "1:5,000,000"]),
    ("1 cm represents 0.5 km", "1:50,000", ["1:500", "1:5,000", "1:500,000"]),
    ("2 cm represents 1 km", "1:50,000", ["1:500", "1:5,000", "1:100,000"]),
    ("1 cm represents 10 km", "1:1,000,000", ["1:10,000", "1:100,000", "1:10,000,000"]),
    ("1 cm represents 250 m", "1:25,000", ["1:250", "1:2,500", "1:250,000"]),
    ("1 cm represents 500 m", "1:50,000", ["1:500", "1:5,000", "1:500,000"]),
    ("4 cm represents 1 km", "1:25,000", ["1:250", "1:4,000", "1:100,000"]),
    ("5 cm represents 1 km", "1:20,000", ["1:200", "1:5,000", "1:200,000"]),
    ("1 cm represents 3 km", "1:300,000", ["1:3,000", "1:30,000", "1:3,000,000"]),
    ("2 cm represents 5 km", "1:250,000", ["1:2,500", "1:25,000", "1:2,500,000"]),
    ("1 cm represents 4 km", "1:400,000", ["1:4,000", "1:40,000", "1:4,000,000"]),
    ("1 cm represents 7.5 km", "1:750,000", ["1:7,500", "1:75,000", "1:7,500,000"]),
    ("3 cm represents 6 km", "1:200,000", ["1:2,000", "1:60,000", "1:600,000"]),
    ("1 cm represents 1.5 km", "1:150,000", ["1:1,500", "1:15,000", "1:1,500,000"]),
]

for desc, correct, dists in written_to_ratio:
    choices, ans = shuffle_choices(correct, dists)
    add_q("Medium",
          f'Convert this written scale to a ratio scale: "{desc}"',
          choices, ans,
          f'Convert the actual distance to cm, then simplify. {desc} → ratio = {correct}.',
          ["scale", "conversion", "written to ratio"])

# --- Type 4: Decimal map distances ---
for i in range(20):
    scale = random.choice([50000, 100000, 200000, 250000, 500000])
    map_cm = random.choice([2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 1.5, 0.5])
    actual_km = (map_cm * scale) / 100000
    correct = f"{actual_km} km"
    d1 = f"{actual_km * 2} km"
    d2 = f"{actual_km + 1} km"
    d3 = f"{actual_km - 0.5} km" if actual_km > 0.5 else "0.1 km"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{actual_km + 3 + len(distractors)} km")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Medium",
          f"A map has a scale of 1:{scale:,}. Two points are {map_cm} cm apart on the map. What is the actual distance?",
          choices, ans,
          f"Actual = {map_cm} × {scale:,} = {int(map_cm * scale):,} cm = {actual_km} km.",
          ["scale", "map-to-actual", "decimal"])

# --- Type 5: Speed and time problems ---
for i in range(20):
    scale = random.choice([100000, 200000, 250000, 500000])
    map_cm = random.choice([3, 4, 5, 6, 8, 9, 10, 12, 15])
    actual_km = (map_cm * scale) / 100000
    speed = random.choice([40, 50, 60, 80, 90, 100])
    time_hr = actual_km / speed
    time_min = time_hr * 60
    if time_min == int(time_min):
        correct = f"{int(time_min)} minutes"
    else:
        correct = f"{time_min:.1f} minutes"
    d1 = f"{int(time_min * 2)} minutes"
    d2 = f"{int(time_min / 2)} minutes" if time_min >= 2 else "1 minute"
    d3 = f"{int(time_min) + 10} minutes"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(time_min) + 15 + len(distractors) * 5} minutes")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Medium",
          f"On a map with scale 1:{scale:,}, two towns are {map_cm} cm apart. If a vehicle travels at {speed} km/h, how long will the trip take?",
          choices, ans,
          f"Actual distance = {map_cm} × {scale:,} = {int(map_cm * scale):,} cm = {actual_km} km. Time = {actual_km} ÷ {speed} = {time_hr} hours = {correct}.",
          ["scale", "distance-speed-time", "multi-step"])

# --- Type 6: Comparing distances on different maps ---
for i in range(15):
    scale_a = random.choice([50000, 100000, 200000])
    scale_b = random.choice([s for s in [100000, 200000, 500000, 250000] if s != scale_a])
    map_a = random.choice([4, 5, 6, 8, 10, 12])
    map_b = random.choice([2, 3, 4, 5, 6, 8])
    actual_a = (map_a * scale_a) / 100000
    actual_b = (map_b * scale_b) / 100000
    if actual_a > actual_b:
        correct = "Route A is longer"
        diff = actual_a - actual_b
    elif actual_b > actual_a:
        correct = "Route B is longer"
        diff = actual_b - actual_a
    else:
        correct = "Both routes are equal"
        diff = 0
    distractors = ["Route A is longer", "Route B is longer", "Both routes are equal", "Cannot be determined"]
    distractors = [d for d in distractors if d != correct][:3]
    choices, ans = shuffle_choices(correct, distractors)
    add_q("Medium",
          f"Route A measures {map_a} cm on a 1:{scale_a:,} map. Route B measures {map_b} cm on a 1:{scale_b:,} map. Which route is longer in reality?",
          choices, ans,
          f"Route A actual = {actual_a} km. Route B actual = {actual_b} km. {correct}.",
          ["scale", "comparison", "multi-step"])

# --- Type 7: Actual to map with non-standard scales ---
for i in range(20):
    scale = random.choice([25000, 40000, 75000, 125000, 150000, 300000, 400000, 600000])
    actual_km = random.choice([3, 4.5, 6, 7.5, 9, 10, 12, 15, 18, 20, 24, 30])
    actual_cm_val = actual_km * 100000
    map_cm = actual_cm_val / scale
    if map_cm != int(map_cm) and map_cm * 10 != int(map_cm * 10):
        continue
    if map_cm == int(map_cm):
        correct = f"{int(map_cm)} cm"
    else:
        correct = f"{map_cm} cm"
    d1_val = map_cm * 2
    d2_val = map_cm / 2
    d3_val = map_cm + 3
    d1 = f"{int(d1_val)} cm" if d1_val == int(d1_val) else f"{d1_val} cm"
    d2 = f"{d2_val} cm" if d2_val >= 0.5 else "0.5 cm"
    d3 = f"{int(d3_val)} cm" if d3_val == int(d3_val) else f"{d3_val} cm"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{map_cm + 5 + len(distractors)} cm")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Medium",
          f"A map has a scale of 1:{scale:,}. What is the map distance for an actual distance of {actual_km} km?",
          choices, ans,
          f"Actual = {actual_km} km = {int(actual_cm_val):,} cm. Map distance = {int(actual_cm_val):,} ÷ {scale:,} = {correct}.",
          ["scale", "actual-to-map", "computation"])

# --- Type 8: Proportion setup ---
for i in range(15):
    scale = random.choice([50000, 100000, 200000, 250000])
    map_cm = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    actual_km = (map_cm * scale) / 100000
    # Ask in meters
    actual_m = actual_km * 1000
    correct = f"{int(actual_m):,} m"
    d1 = f"{int(actual_m * 10):,} m"
    d2 = f"{int(actual_m / 10):,} m"
    d3 = f"{int(actual_m + 500):,} m"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(actual_m) + 1000 * (len(distractors) + 1):,} m")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Medium",
          f"On a 1:{scale:,} map, two landmarks are {map_cm} cm apart. What is the actual distance in meters?",
          choices, ans,
          f"Actual = {map_cm} × {scale:,} = {map_cm * scale:,} cm = {int(actual_m):,} m.",
          ["scale", "map-to-actual", "meters"])

# --- Fill remaining medium ---
while len([q for q in questions if q["difficulty"] == "Medium"]) < 200:
    qtype = random.choice(["map_to_actual", "actual_to_map", "find_scale", "time"])
    scale = random.choice([25000, 50000, 75000, 100000, 150000, 200000, 250000, 300000, 400000, 500000])

    if qtype == "map_to_actual":
        map_cm = round(random.uniform(1, 20), 1)
        if map_cm == int(map_cm):
            map_cm = int(map_cm)
        actual_km = (map_cm * scale) / 100000
        if actual_km == int(actual_km):
            correct = f"{int(actual_km)} km"
        else:
            correct = f"{actual_km:.1f} km"
        d1 = f"{actual_km * 2:.1f} km"
        d2 = f"{actual_km / 2:.1f} km"
        d3 = f"{actual_km + 2:.1f} km"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"{actual_km + 5 + len(distractors):.1f} km")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Medium",
              f"Scale: 1:{scale:,}. A road measures {map_cm} cm on the map. Find the actual distance in km.",
              choices, ans,
              f"{map_cm} × {scale:,} = {map_cm * scale:,.0f} cm = {correct}.",
              ["scale", "map-to-actual", "computation"])

    elif qtype == "actual_to_map":
        actual_km = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30])
        map_cm = (actual_km * 100000) / scale
        if map_cm == int(map_cm):
            correct = f"{int(map_cm)} cm"
        else:
            correct = f"{map_cm:.1f} cm"
        d1 = f"{map_cm * 2:.1f} cm"
        d2 = f"{map_cm / 2:.1f} cm"
        d3 = f"{map_cm + 3:.1f} cm"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"{map_cm + 5 + len(distractors):.1f} cm")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Medium",
              f"Scale: 1:{scale:,}. Actual distance: {actual_km} km. What is the map distance?",
              choices, ans,
              f"{actual_km} km = {actual_km * 100000:,} cm. Map = {actual_km * 100000:,} ÷ {scale:,} = {correct}.",
              ["scale", "actual-to-map", "computation"])

    elif qtype == "find_scale":
        map_cm = random.choice([2, 3, 4, 5, 6, 8, 10])
        actual_km = random.choice([4, 6, 8, 10, 12, 15, 20, 24, 30, 40, 50])
        actual_cm_val = actual_km * 100000
        scale_val = actual_cm_val // map_cm
        correct = f"1:{scale_val:,}"
        d1 = f"1:{scale_val * 2:,}"
        d2 = f"1:{scale_val // 2:,}"
        d3 = f"1:{scale_val + 50000:,}"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"1:{scale_val + 100000 * (len(distractors) + 1):,}")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Medium",
              f"A road is {map_cm} cm long on a map and {actual_km} km in reality. Determine the map scale.",
              choices, ans,
              f"{actual_km} km = {actual_cm_val:,} cm. Scale = {map_cm}:{actual_cm_val:,} = 1:{scale_val:,}.",
              ["scale", "finding scale", "ratio"])

    else:  # time
        map_cm = random.choice([4, 5, 6, 8, 10, 12])
        actual_km = (map_cm * scale) / 100000
        speed = random.choice([40, 50, 60, 80, 100, 120])
        time_min = (actual_km / speed) * 60
        if time_min == int(time_min):
            correct = f"{int(time_min)} minutes"
        else:
            correct = f"{time_min:.1f} minutes"
        d1 = f"{int(time_min * 2)} minutes"
        d2 = f"{max(1, int(time_min / 2))} minutes"
        d3 = f"{int(time_min) + 15} minutes"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"{int(time_min) + 20 + len(distractors) * 10} minutes")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Medium",
              f"On a 1:{scale:,} map, two points are {map_cm} cm apart. A bus travels at {speed} km/h. How long is the journey?",
              choices, ans,
              f"Actual = {actual_km} km. Time = {actual_km}/{speed} hr = {correct}.",
              ["scale", "distance-speed-time", "multi-step"])

print(f"Medium questions generated: {len([q for q in questions if q['difficulty'] == 'Medium'])}")

# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Type 1: Area problems ---
for i in range(25):
    scale = random.choice([1000, 2000, 5000, 10000, 20000, 25000, 50000])
    length_cm = random.choice([2, 3, 4, 5, 6, 7, 8, 10])
    width_cm = random.choice([2, 3, 4, 5, 6, 7, 8])
    if width_cm >= length_cm:
        width_cm = length_cm - 1 if length_cm > 2 else 1
    actual_l = (length_cm * scale) / 100  # in meters
    actual_w = (width_cm * scale) / 100
    area = actual_l * actual_w
    if area >= 10000:
        correct = f"{int(area):,} m²"
    else:
        correct = f"{int(area):,} m²"
    d1 = f"{int(area * 2):,} m²"
    d2 = f"{int(area / 2):,} m²"
    d3 = f"{int(area + 1000):,} m²"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(area) + 5000 * (len(distractors) + 1):,} m²")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"A rectangular lot measures {length_cm} cm × {width_cm} cm on a 1:{scale:,} map. What is the actual area in square meters?",
          choices, ans,
          f"Length = {length_cm} × {scale:,} = {int(length_cm * scale):,} cm = {int(actual_l):,} m. Width = {width_cm} × {scale:,} = {int(width_cm * scale):,} cm = {int(actual_w):,} m. Area = {int(actual_l):,} × {int(actual_w):,} = {int(area):,} m².",
          ["scale", "area", "multi-step"])

# --- Type 2: Cross-map conversion ---
for i in range(20):
    scale_a = random.choice([50000, 100000, 200000, 250000])
    scale_b = random.choice([s for s in [100000, 200000, 400000, 500000, 250000] if s != scale_a])
    map_a_cm = random.choice([4, 5, 6, 8, 10, 12, 15, 16, 20])
    actual_cm = map_a_cm * scale_a
    map_b_cm = actual_cm / scale_b
    if map_b_cm != int(map_b_cm) and map_b_cm * 2 != int(map_b_cm * 2):
        continue
    if map_b_cm == int(map_b_cm):
        correct = f"{int(map_b_cm)} cm"
    else:
        correct = f"{map_b_cm} cm"
    d1_v = map_b_cm * 2
    d2_v = map_b_cm / 2
    d3_v = map_b_cm + 3
    d1 = f"{int(d1_v)} cm" if d1_v == int(d1_v) else f"{d1_v} cm"
    d2 = f"{d2_v} cm" if d2_v >= 0.5 else "0.5 cm"
    d3 = f"{int(d3_v)} cm" if d3_v == int(d3_v) else f"{d3_v} cm"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{map_b_cm + 4 + len(distractors)} cm")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"A river measures {map_a_cm} cm on Map A (scale 1:{scale_a:,}). How long would the same river appear on Map B (scale 1:{scale_b:,})?",
          choices, ans,
          f"Actual = {map_a_cm} × {scale_a:,} = {actual_cm:,} cm. On Map B: {actual_cm:,} ÷ {scale_b:,} = {correct}.",
          ["scale", "cross-map", "multi-step"])

# --- Type 3: Land value problems ---
for i in range(20):
    scale = random.choice([1000, 2000, 5000, 10000])
    length_cm = random.choice([3, 4, 5, 6, 8, 10])
    width_cm = random.choice([2, 3, 4, 5, 6])
    if width_cm >= length_cm:
        width_cm = max(1, length_cm - 1)
    price_per_sqm = random.choice([2000, 3000, 5000, 8000, 10000, 15000])
    actual_l_m = (length_cm * scale) / 100
    actual_w_m = (width_cm * scale) / 100
    area_sqm = actual_l_m * actual_w_m
    total_value = area_sqm * price_per_sqm
    correct = f"₱{int(total_value):,}"
    d1 = f"₱{int(total_value * 2):,}"
    d2 = f"₱{int(total_value / 2):,}"
    d3 = f"₱{int(total_value + 1000000):,}"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"₱{int(total_value) + 500000 * (len(distractors) + 1):,}")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"A lot measures {length_cm} cm × {width_cm} cm on a 1:{scale:,} cadastral map. If land costs ₱{price_per_sqm:,} per square meter, what is the total land value?",
          choices, ans,
          f"Length = {int(actual_l_m)} m, Width = {int(actual_w_m)} m. Area = {int(area_sqm):,} m². Value = {int(area_sqm):,} × ₱{price_per_sqm:,} = {correct}.",
          ["scale", "area", "land value", "multi-step"])

# --- Type 4: Multi-leg journey ---
for i in range(20):
    scale = random.choice([100000, 200000, 250000, 500000])
    leg1_cm = random.choice([3, 4, 5, 6, 7, 8])
    leg2_cm = random.choice([2, 3, 4, 5, 6, 7])
    leg3_cm = random.choice([1, 2, 3, 4, 5])
    total_cm = leg1_cm + leg2_cm + leg3_cm
    actual_km = (total_cm * scale) / 100000
    if actual_km == int(actual_km):
        correct = f"{int(actual_km)} km"
    else:
        correct = f"{actual_km} km"
    d1 = f"{actual_km + 5:.0f} km"
    d2 = f"{actual_km - 3:.0f} km" if actual_km > 3 else "1 km"
    d3 = f"{actual_km * 2:.0f} km"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{actual_km + 8 + len(distractors) * 3:.0f} km")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"On a 1:{scale:,} map, a delivery route has three legs measuring {leg1_cm} cm, {leg2_cm} cm, and {leg3_cm} cm. What is the total actual distance?",
          choices, ans,
          f"Total map distance = {leg1_cm} + {leg2_cm} + {leg3_cm} = {total_cm} cm. Actual = {total_cm} × {scale:,} = {total_cm * scale:,} cm = {actual_km} km.",
          ["scale", "multi-leg", "addition", "multi-step"])

# --- Type 5: Fuel consumption problems ---
for i in range(15):
    scale = random.choice([200000, 250000, 500000, 1000000])
    map_cm = random.choice([5, 6, 8, 10, 12, 15, 20])
    actual_km = (map_cm * scale) / 100000
    fuel_rate = random.choice([8, 10, 12, 15])  # km per liter
    fuel_needed = actual_km / fuel_rate
    if fuel_needed == int(fuel_needed):
        correct = f"{int(fuel_needed)} liters"
    else:
        correct = f"{fuel_needed:.1f} liters"
    d1 = f"{fuel_needed * 2:.1f} liters"
    d2 = f"{fuel_needed / 2:.1f} liters"
    d3 = f"{fuel_needed + 3:.1f} liters"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{fuel_needed + 5 + len(distractors) * 2:.1f} liters")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"On a 1:{scale:,} map, the distance between two cities is {map_cm} cm. If a car consumes 1 liter per {fuel_rate} km, how much fuel is needed for the trip?",
          choices, ans,
          f"Actual = {map_cm} × {scale:,} = {map_cm * scale:,} cm = {actual_km:.0f} km. Fuel = {actual_km:.0f} ÷ {fuel_rate} = {correct}.",
          ["scale", "fuel consumption", "multi-step"])

# --- Type 6: Perimeter problems ---
for i in range(15):
    scale = random.choice([2000, 5000, 10000, 20000])
    length_cm = random.choice([4, 5, 6, 7, 8, 10])
    width_cm = random.choice([2, 3, 4, 5, 6])
    if width_cm >= length_cm:
        width_cm = max(1, length_cm - 1)
    actual_l_m = (length_cm * scale) / 100
    actual_w_m = (width_cm * scale) / 100
    perimeter = 2 * (actual_l_m + actual_w_m)
    correct = f"{int(perimeter):,} m"
    d1 = f"{int(perimeter * 2):,} m"
    d2 = f"{int(perimeter / 2):,} m"
    d3 = f"{int(actual_l_m * actual_w_m):,} m"  # area trap
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(perimeter) + 100 * (len(distractors) + 1):,} m")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"A rectangular field measures {length_cm} cm × {width_cm} cm on a 1:{scale:,} map. What is the actual perimeter of the field?",
          choices, ans,
          f"Length = {int(actual_l_m)} m, Width = {int(actual_w_m)} m. Perimeter = 2({int(actual_l_m)} + {int(actual_w_m)}) = {int(perimeter):,} m.",
          ["scale", "perimeter", "multi-step"])

# --- Type 7: Cost of fencing/road construction ---
for i in range(15):
    scale = random.choice([5000, 10000, 20000, 25000, 50000])
    map_cm = random.choice([4, 5, 6, 8, 10, 12, 15, 20])
    actual_m = (map_cm * scale) / 100
    cost_per_m = random.choice([500, 800, 1000, 1500, 2000, 2500])
    total_cost = actual_m * cost_per_m
    correct = f"₱{int(total_cost):,}"
    d1 = f"₱{int(total_cost * 2):,}"
    d2 = f"₱{int(total_cost / 2):,}"
    d3 = f"₱{int(total_cost + 50000):,}"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"₱{int(total_cost) + 100000 * (len(distractors) + 1):,}")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"A road measures {map_cm} cm on a 1:{scale:,} map. If construction costs ₱{cost_per_m:,} per meter, what is the total construction cost?",
          choices, ans,
          f"Actual = {map_cm} × {scale:,} = {map_cm * scale:,} cm = {int(actual_m):,} m. Cost = {int(actual_m):,} × ₱{cost_per_m:,} = {correct}.",
          ["scale", "cost", "construction", "multi-step"])

# --- Type 8: Two-part journey with different speeds ---
for i in range(15):
    scale = random.choice([100000, 200000, 250000])
    leg1_cm = random.choice([4, 5, 6, 8])
    leg2_cm = random.choice([3, 4, 5, 6])
    speed1 = random.choice([40, 50, 60])
    speed2 = random.choice([80, 90, 100])
    actual1 = (leg1_cm * scale) / 100000
    actual2 = (leg2_cm * scale) / 100000
    time1_min = (actual1 / speed1) * 60
    time2_min = (actual2 / speed2) * 60
    total_min = time1_min + time2_min
    if total_min == int(total_min):
        correct = f"{int(total_min)} minutes"
    else:
        correct = f"{total_min:.1f} minutes"
    d1 = f"{int(total_min + 10)} minutes"
    d2 = f"{int(total_min * 2)} minutes"
    d3 = f"{max(1, int(total_min - 10))} minutes"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{int(total_min) + 15 + len(distractors) * 5} minutes")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"On a 1:{scale:,} map, a trip has two legs: {leg1_cm} cm at {speed1} km/h and {leg2_cm} cm at {speed2} km/h. What is the total travel time?",
          choices, ans,
          f"Leg 1: {actual1} km at {speed1} km/h = {time1_min:.1f} min. Leg 2: {actual2} km at {speed2} km/h = {time2_min:.1f} min. Total = {correct}.",
          ["scale", "speed-time", "multi-leg", "multi-step"])

# --- Type 9: Scale change (enlargement/reduction) ---
for i in range(15):
    old_scale = random.choice([50000, 100000, 200000, 250000])
    new_scale = random.choice([s for s in [25000, 50000, 100000, 500000, 1000000] if s != old_scale])
    map_old_cm = random.choice([4, 5, 6, 8, 10, 12])
    # actual stays same, find new map distance
    actual_cm = map_old_cm * old_scale
    map_new_cm = actual_cm / new_scale
    if map_new_cm == int(map_new_cm):
        correct = f"{int(map_new_cm)} cm"
    else:
        correct = f"{map_new_cm:.1f} cm"
    d1_v = map_new_cm * 2
    d2_v = map_new_cm / 2
    d3_v = map_new_cm + 4
    d1 = f"{d1_v:.1f} cm" if d1_v != int(d1_v) else f"{int(d1_v)} cm"
    d2 = f"{d2_v:.1f} cm" if d2_v != int(d2_v) else f"{int(d2_v)} cm"
    d3 = f"{d3_v:.1f} cm" if d3_v != int(d3_v) else f"{int(d3_v)} cm"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{map_new_cm + 6 + len(distractors) * 2:.1f} cm")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"A feature measures {map_old_cm} cm on a 1:{old_scale:,} map. If the same feature is drawn on a 1:{new_scale:,} map, what will its length be?",
          choices, ans,
          f"Actual = {map_old_cm} × {old_scale:,} = {actual_cm:,} cm. New map = {actual_cm:,} ÷ {new_scale:,} = {correct}.",
          ["scale", "scale change", "cross-map"])

# --- Type 10: Backward from travel time ---
for i in range(15):
    speed = random.choice([40, 50, 60, 80, 100])
    time_hr = random.choice([0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3])
    actual_km = speed * time_hr
    scale = random.choice([100000, 200000, 250000, 500000])
    map_cm = (actual_km * 100000) / scale
    if map_cm == int(map_cm):
        correct = f"{int(map_cm)} cm"
    else:
        correct = f"{map_cm:.1f} cm"
    d1 = f"{map_cm * 2:.1f} cm" if map_cm * 2 != int(map_cm * 2) else f"{int(map_cm * 2)} cm"
    d2 = f"{map_cm / 2:.1f} cm" if map_cm / 2 != int(map_cm / 2) else f"{int(map_cm / 2)} cm"
    d3 = f"{map_cm + 5:.1f} cm" if (map_cm + 5) != int(map_cm + 5) else f"{int(map_cm + 5)} cm"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{map_cm + 8 + len(distractors) * 3:.1f} cm")
    choices, ans = shuffle_choices(correct, distractors[:3])
    time_desc = f"{int(time_hr * 60)} minutes" if time_hr < 1 else f"{time_hr} hours"
    add_q("Hard",
          f"A car travels at {speed} km/h for {time_desc}. On a 1:{scale:,} map, how far apart are the start and end points?",
          choices, ans,
          f"Distance = {speed} × {time_hr} = {actual_km} km = {int(actual_km * 100000):,} cm. Map = {int(actual_km * 100000):,} ÷ {scale:,} = {correct}.",
          ["scale", "backward", "speed-time", "multi-step"])

# --- Type 11: Hectare conversion ---
for i in range(10):
    scale = random.choice([5000, 10000, 20000, 25000])
    length_cm = random.choice([5, 6, 8, 10, 12, 15, 20])
    width_cm = random.choice([4, 5, 6, 8, 10])
    if width_cm >= length_cm:
        width_cm = max(2, length_cm - 2)
    actual_l_m = (length_cm * scale) / 100
    actual_w_m = (width_cm * scale) / 100
    area_sqm = actual_l_m * actual_w_m
    area_ha = area_sqm / 10000
    if area_ha == int(area_ha):
        correct = f"{int(area_ha)} hectares"
    else:
        correct = f"{area_ha:.1f} hectares"
    d1 = f"{area_ha * 2:.1f} hectares"
    d2 = f"{area_ha / 2:.1f} hectares"
    d3 = f"{area_ha + 5:.1f} hectares"
    distractors = list(set([d1, d2, d3]) - {correct})[:3]
    while len(distractors) < 3:
        distractors.append(f"{area_ha + 10 + len(distractors) * 3:.1f} hectares")
    choices, ans = shuffle_choices(correct, distractors[:3])
    add_q("Hard",
          f"A farm measures {length_cm} cm × {width_cm} cm on a 1:{scale:,} map. What is the actual area in hectares?",
          choices, ans,
          f"Length = {int(actual_l_m)} m, Width = {int(actual_w_m)} m. Area = {int(area_sqm):,} m² = {area_ha} hectares (÷ 10,000).",
          ["scale", "area", "hectares", "multi-step"])

# --- Fill remaining hard to reach 200 ---
while len([q for q in questions if q["difficulty"] == "Hard"]) < 200:
    qtype = random.choice(["area", "cost_road", "fuel", "cross_map", "time_multi", "perimeter_fence"])
    scale = random.choice([2000, 5000, 10000, 20000, 25000, 50000, 100000, 200000, 250000, 500000])

    if qtype == "area":
        l = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])
        w = random.choice([2, 3, 4, 5, 6, 7, 8])
        if w >= l:
            w = max(1, l - 1)
        al = (l * scale) / 100
        aw = (w * scale) / 100
        area = al * aw
        correct = f"{int(area):,} m²"
        d1 = f"{int(area * 4):,} m²"
        d2 = f"{int(area / 4):,} m²"
        d3 = f"{int(area + 2000):,} m²"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"{int(area) + 3000 * (len(distractors) + 1):,} m²")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Hard",
              f"A plot is {l} cm × {w} cm on a 1:{scale:,} plan. Find the actual area in m².",
              choices, ans,
              f"L={int(al)} m, W={int(aw)} m. Area = {int(area):,} m².",
              ["scale", "area", "computation"])

    elif qtype == "cost_road":
        map_cm = random.choice([3, 4, 5, 6, 8, 10, 12, 15])
        actual_m = (map_cm * scale) / 100
        cost = random.choice([500, 750, 1000, 1200, 1500, 2000, 3000])
        total = actual_m * cost
        correct = f"₱{int(total):,}"
        d1 = f"₱{int(total * 2):,}"
        d2 = f"₱{int(total / 2):,}"
        d3 = f"₱{int(total + 100000):,}"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"₱{int(total) + 200000 * (len(distractors) + 1):,}")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Hard",
              f"A fence line is {map_cm} cm on a 1:{scale:,} map. Fencing costs ₱{cost:,}/m. Total cost?",
              choices, ans,
              f"Actual = {int(actual_m):,} m. Cost = {int(actual_m):,} × ₱{cost:,} = {correct}.",
              ["scale", "cost", "fencing", "multi-step"])

    elif qtype == "fuel":
        map_cm = random.choice([6, 8, 10, 12, 15, 20])
        actual_km = (map_cm * scale) / 100000
        if actual_km < 1:
            continue
        rate = random.choice([8, 10, 12, 14, 15])
        fuel = actual_km / rate
        correct = f"{fuel:.1f} liters"
        d1 = f"{fuel * 2:.1f} liters"
        d2 = f"{fuel / 2:.1f} liters"
        d3 = f"{fuel + 2:.1f} liters"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"{fuel + 4 + len(distractors):.1f} liters")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Hard",
              f"Scale 1:{scale:,}. Distance on map: {map_cm} cm. Car uses 1 L per {rate} km. Fuel needed?",
              choices, ans,
              f"Actual = {actual_km} km. Fuel = {actual_km}/{rate} = {correct}.",
              ["scale", "fuel", "multi-step"])

    elif qtype == "cross_map":
        sa = random.choice([50000, 100000, 200000])
        sb = random.choice([s for s in [100000, 250000, 500000] if s != sa])
        ma = random.choice([4, 6, 8, 10, 12, 15, 20])
        actual = ma * sa
        mb = actual / sb
        if mb != int(mb) and mb * 10 != int(mb * 10):
            continue
        correct = f"{mb:.1f} cm" if mb != int(mb) else f"{int(mb)} cm"
        d1 = f"{mb * 2:.1f} cm"
        d2 = f"{mb / 2:.1f} cm"
        d3 = f"{mb + 3:.1f} cm"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"{mb + 5 + len(distractors) * 2:.1f} cm")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Hard",
              f"A road is {ma} cm on a 1:{sa:,} map. What length on a 1:{sb:,} map?",
              choices, ans,
              f"Actual = {ma} × {sa:,} = {actual:,.0f} cm. New map = {actual:,.0f} ÷ {sb:,} = {correct}.",
              ["scale", "cross-map", "multi-step"])

    elif qtype == "time_multi":
        map_cm = random.choice([5, 6, 8, 10, 12, 15])
        actual_km = (map_cm * scale) / 100000
        if actual_km < 1:
            continue
        speed = random.choice([40, 50, 60, 80, 100])
        time_min = (actual_km / speed) * 60
        correct = f"{time_min:.1f} minutes" if time_min != int(time_min) else f"{int(time_min)} minutes"
        d1 = f"{time_min * 2:.0f} minutes"
        d2 = f"{max(1, time_min / 2):.0f} minutes"
        d3 = f"{time_min + 15:.0f} minutes"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"{int(time_min) + 20 + len(distractors) * 10} minutes")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Hard",
              f"Scale 1:{scale:,}. Map distance: {map_cm} cm. Speed: {speed} km/h. Travel time?",
              choices, ans,
              f"Actual = {actual_km} km. Time = {actual_km}/{speed} × 60 = {correct}.",
              ["scale", "time", "speed", "multi-step"])

    else:  # perimeter_fence
        l = random.choice([4, 5, 6, 8, 10])
        w = random.choice([2, 3, 4, 5, 6])
        if w >= l:
            w = max(1, l - 1)
        al = (l * scale) / 100
        aw = (w * scale) / 100
        perim = 2 * (al + aw)
        cost = random.choice([200, 300, 500, 800, 1000])
        total = perim * cost
        correct = f"₱{int(total):,}"
        d1 = f"₱{int(total * 2):,}"
        d2 = f"₱{int(total / 2):,}"
        d3 = f"₱{int(total + 50000):,}"
        distractors = list(set([d1, d2, d3]) - {correct})[:3]
        while len(distractors) < 3:
            distractors.append(f"₱{int(total) + 100000 * (len(distractors) + 1):,}")
        choices, ans = shuffle_choices(correct, distractors[:3])
        add_q("Hard",
              f"A lot is {l} cm × {w} cm on a 1:{scale:,} map. Fencing costs ₱{cost:,}/m. Total fencing cost?",
              choices, ans,
              f"L={int(al)} m, W={int(aw)} m. Perimeter = {int(perim):,} m. Cost = {int(perim):,} × ₱{cost:,} = {correct}.",
              ["scale", "perimeter", "cost", "multi-step"])

print(f"Hard questions generated: {len([q for q in questions if q['difficulty'] == 'Hard'])}")

# ============================================================
# TRIM TO EXACTLY 200 PER DIFFICULTY
# ============================================================

easy_qs = [q for q in questions if q["difficulty"] == "Easy"][:200]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"][:200]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"][:200]

final_questions = easy_qs + medium_qs + hard_qs

# Re-number IDs sequentially
for i, q in enumerate(final_questions, 1):
    q["id"] = i

print(f"\nFinal counts:")
print(f"  Easy: {len(easy_qs)}")
print(f"  Medium: {len(medium_qs)}")
print(f"  Hard: {len(hard_qs)}")
print(f"  Total: {len(final_questions)}")

# Write to JSON
output_path = r"c:\Users\Jaime\Documents\GitHub\csnexus\data\seed\questions\numerical-ability\ratio-proportion-and-average\scale-and-map-problems\questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_questions, f, indent=2, ensure_ascii=False)

print(f"\nJSON written to: {output_path}")
