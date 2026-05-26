import os

paths = [
    "data/seed/lessons/numerical-ability/percentages/profit-loss-and-tax/lesson.md",
    "data/seed/lessons/numerical-ability/percentages/percentage-applications/lesson.md",
    "data/seed/lessons/numerical-ability/percentages/percentage-word-problems/lesson.md",
    "data/seed/lessons/numerical-ability/percentages/percentage-mental-math-and-shortcuts/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/introduction-to-ratios/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/types-of-ratios/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/ratio-word-problems/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/direct-and-inverse-proportions/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/proportion-word-problems/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/scale-and-map-problems/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/introduction-to-average/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/weighted-average/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/finding-missing-values-in-averages/lesson.md",
    "data/seed/lessons/numerical-ability/ratio-proportion-and-average/average-word-problems/lesson.md",
]

required = [
    "Check Your Understanding",
    "Why does this work",
    "Misconception",
    "Guided Practice",
    "Which Method?",
    "Before You Practice",
    "Connections",
    "Mastery Checklist",
]

for path in paths:
    if not os.path.exists(path):
        print(f"\n=== {path} === NOT FOUND")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = len(content.splitlines())
    name = os.path.basename(os.path.dirname(path))
    print(f"\n=== {name} ({lines} lines) ===")
    all_ok = True
    for r in required:
        count = content.count(r)
        if count == 0:
            print(f"  MISSING: \"{r}\"")
            all_ok = False
        else:
            print(f"  OK: \"{r}\" ({count})")
    if all_ok:
        print("  >>> ALL SECTIONS PRESENT")