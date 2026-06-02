"""Fix the last remaining duplicate: verisimilitude x2 in CSR."""
import json, pathlib, random
from collections import Counter

random.seed(55)

BASE = pathlib.Path(r"c:\Users\Jaime\Documents\GitHub\csnexus\data\seed\questions\clerical-ability\spelling")
csr_path = BASE / "correct-spelling-recognition/questions.json"
cse_path = BASE / "common-spelling-errors/questions.json"

csr = json.loads(csr_path.read_text(encoding="utf-8"))
cse = json.loads(cse_path.read_text(encoding="utf-8"))

csr_by_id = {q["id"]: q for q in csr}
all_answers = set(q["answer"].lower() for q in csr)

# verisimilitude x2: IDs 448 (keep) and 474 (replace)
# Replace ID 474 with 'verisimilar' — a real English adjective
q474 = csr_by_id[474]
new_answer = "verisimilar"
if new_answer.lower() not in all_answers:
    q474["answer"] = new_answer
    q474["choices"] = ["verisimlar", "verisimiler", "verisimiller", new_answer]
    random.shuffle(q474["choices"])
    q474["explanation"] = "Verisimilitude → verisimilar — resembling truth or reality."
    q474["tags"] = ["latin-origin"]
    all_answers.add(new_answer.lower())
    print(f"Fixed ID 474: 'verisimilitude' -> '{new_answer}'")
else:
    print(f"'{new_answer}' already in bank — need different word")
    # Use 'verisimilarly' instead
    new_answer = "verisimilarly"
    q474["answer"] = new_answer
    q474["choices"] = ["verisimarly", "verisimillarly", "verisimillary", new_answer]
    random.shuffle(q474["choices"])
    q474["explanation"] = "Verisimilar → verisimilarly — in a verisimilar manner."
    q474["tags"] = ["latin-origin"]
    print(f"Fixed ID 474: -> '{new_answer}'")

# Validate both
def validate(bank, name):
    errors = []
    for q in bank:
        if q["answer"] not in q["choices"]:
            errors.append(f"{name} ID {q['id']}: answer not in choices")
        if len(set(q["choices"])) != 4:
            errors.append(f"{name} ID {q['id']}: duplicate choices")
    dupes = {k: v for k, v in Counter(q["answer"] for q in bank).items() if v > 1}
    return errors, dupes

csr_errors, csr_dupes = validate(csr, "CSR")
cse_errors, cse_dupes = validate(cse, "CSE")

print(f"CSR errors: {len(csr_errors)}, dupes: {len(csr_dupes)}")
print(f"CSE errors: {len(cse_errors)}, dupes: {len(cse_dupes)}")

if not csr_errors and not cse_errors and not csr_dupes and not cse_dupes:
    csr_path.write_text(json.dumps(csr, indent=2, ensure_ascii=False), encoding="utf-8")
    cse_path.write_text(json.dumps(cse, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Both files saved!")
