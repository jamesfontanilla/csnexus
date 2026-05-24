"""Verify all 600 sentence structure questions for accuracy.

Checks:
1. JSON schema validity (all required keys present)
2. Answer is one of the choices
3. IDs are sequential 1-600
4. No duplicate questions
5. Difficulty distribution (200/200/200)
6. Answer correctness via clause analysis heuristics
"""
import json
import re
from pathlib import Path

FILE = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions" / "verbal-ability"
    / "sentence-structure" / "types-of-sentences-by-structure" / "questions.json"
)

REQUIRED_KEYS = {"id", "subtest", "module", "subtopic", "difficulty", "question",
                 "choices", "answer", "explanation", "tags", "category", "language"}

VALID_ANSWERS = {"Simple", "Compound", "Complex", "Compound-Complex"}
VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}

# Subordinating conjunctions that create dependent clauses
SUBORDINATORS = [
    "although", "though", "even though", "because", "since", "as",
    "while", "when", "whenever", "where", "wherever", "after",
    "before", "until", "unless", "if", "provided that", "as long as",
    "so that", "in order that", "even if", "whereas", "once",
    "as soon as", "inasmuch as", "now that", "lest",
]

# Coordinating conjunctions
FANBOYS = ["for", "and", "nor", "but", "or", "yet", "so"]

# Relative pronouns that create dependent clauses
RELATIVE_PRONOUNS = ["who", "whom", "whose", "which", "that", "where", "when", "why"]


def extract_sentence(question_text):
    """Extract the sentence being analyzed from the question text."""
    # Pattern: 'sentence here'
    match = re.search(r"'(.+?)'", question_text)
    if match:
        return match.group(1)
    return None


def has_subordinator(sentence):
    """Check if sentence contains a subordinating conjunction followed by a clause pattern."""
    s_lower = sentence.lower()
    for sub in SUBORDINATORS:
        # Check if subordinator appears and is likely followed by a subject-verb
        pattern = r'\b' + re.escape(sub) + r'\b'
        if re.search(pattern, s_lower):
            return True
    return False


def has_relative_clause(sentence):
    """Check if sentence contains a relative pronoun likely introducing a clause."""
    s_lower = sentence.lower()
    # Look for relative pronouns that are likely clause-starters
    for rp in ["who ", "whom ", "whose ", "which ", "that "]:
        if rp in s_lower:
            return True
    return False


def has_fanboys_between_clauses(sentence):
    """Check if sentence has comma + FANBOYS pattern suggesting compound structure."""
    # Pattern: ", and/but/or/nor/yet/so/for " between what look like clauses
    pattern = r',\s+(and|but|or|nor|yet|so|for)\s+'
    return bool(re.search(pattern, sentence, re.IGNORECASE))


def has_semicolon(sentence):
    """Check if sentence has a semicolon (compound signal)."""
    return ";" in sentence


def basic_answer_check(sentence, answer):
    """
    Perform basic heuristic check on whether the answer is plausible.
    Returns (is_plausible, reason) tuple.
    
    This is a HEURISTIC - it catches obvious errors but cannot verify
    every nuanced case (e.g., compound verbs vs compound sentences).
    """
    if sentence is None:
        return True, "Could not extract sentence"
    
    has_sub = has_subordinator(sentence)
    has_rel = has_relative_clause(sentence)
    has_compound_signal = has_fanboys_between_clauses(sentence) or has_semicolon(sentence)
    has_dependent = has_sub or has_rel
    
    if answer == "Simple":
        # Simple should NOT have subordinators creating clauses or compound signals
        # But this is tricky - "before the deadline" (phrase) vs "before he left" (clause)
        # We'll flag only obvious cases
        if has_compound_signal and has_dependent:
            return False, f"Marked Simple but has both compound signal and dependent clause markers"
        # Don't flag subordinators alone - could be prepositional use
        return True, "OK"
    
    elif answer == "Compound":
        # Compound needs compound signal (FANBOYS between clauses or semicolon)
        # and should NOT have subordinators creating dependent clauses
        if not has_compound_signal:
            return False, "Marked Compound but no comma+FANBOYS or semicolon found"
        return True, "OK"
    
    elif answer == "Complex":
        # Complex needs a dependent clause marker (subordinator or relative pronoun)
        # and should NOT have compound signals between independent clauses
        if not has_dependent:
            return False, "Marked Complex but no subordinator or relative pronoun found"
        return True, "OK"
    
    elif answer == "Compound-Complex":
        # Needs BOTH compound signal AND dependent clause marker
        if not has_compound_signal:
            return False, "Marked Compound-Complex but no compound signal found"
        if not has_dependent:
            return False, "Marked Compound-Complex but no dependent clause marker found"
        return True, "OK"
    
    return True, "Non-standard answer type"


def main():
    print(f"Loading: {FILE}")
    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Total questions: {len(data)}")
    print()
    
    errors = []
    warnings = []
    
    # Check 1: Total count
    if len(data) != 600:
        errors.append(f"Expected 600 questions, got {len(data)}")
    
    # Check 2: Schema, IDs, duplicates
    seen_ids = set()
    seen_questions = set()
    difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    answer_distribution = {}
    
    for i, q in enumerate(data):
        # Schema check
        missing = REQUIRED_KEYS - set(q.keys())
        if missing:
            errors.append(f"Q{q.get('id', '?')}: Missing keys: {missing}")
        
        # ID check
        expected_id = i + 1
        if q.get("id") != expected_id:
            errors.append(f"Q at index {i}: Expected id={expected_id}, got id={q.get('id')}")
        
        if q.get("id") in seen_ids:
            errors.append(f"Q{q['id']}: Duplicate ID")
        seen_ids.add(q.get("id"))
        
        # Duplicate question check
        q_text = q.get("question", "")
        if q_text in seen_questions:
            errors.append(f"Q{q['id']}: Duplicate question text")
        seen_questions.add(q_text)
        
        # Difficulty check
        diff = q.get("difficulty", "")
        if diff not in VALID_DIFFICULTIES:
            errors.append(f"Q{q['id']}: Invalid difficulty '{diff}'")
        else:
            difficulty_counts[diff] += 1
        
        # Answer in choices check
        answer = q.get("answer", "")
        choices = q.get("choices", [])
        if answer not in choices:
            errors.append(f"Q{q['id']}: Answer '{answer}' not in choices {choices}")
        
        # Track answer distribution
        answer_distribution[answer] = answer_distribution.get(answer, 0) + 1
        
        # Choices count check
        if len(choices) != 4:
            errors.append(f"Q{q['id']}: Expected 4 choices, got {len(choices)}")
        
        # Tags check
        if not q.get("tags") or len(q.get("tags", [])) == 0:
            warnings.append(f"Q{q['id']}: Empty tags")
        
        # Answer correctness heuristic (only for sentence-type identification questions)
        if answer in VALID_ANSWERS:
            sentence = extract_sentence(q_text)
            if sentence:
                plausible, reason = basic_answer_check(sentence, answer)
                if not plausible:
                    warnings.append(f"Q{q['id']} ({diff}): {reason} | Sentence: '{sentence[:80]}...' | Answer: {answer}")
    
    # Check 3: Difficulty distribution
    print("=== DIFFICULTY DISTRIBUTION ===")
    for d, c in difficulty_counts.items():
        status = "✓" if c == 200 else "✗"
        print(f"  {status} {d}: {c}")
    print()
    
    # Answer distribution
    print("=== ANSWER DISTRIBUTION ===")
    for a, c in sorted(answer_distribution.items()):
        print(f"  {a}: {c}")
    print()
    
    # Report errors
    print(f"=== ERRORS ({len(errors)}) ===")
    if errors:
        for e in errors[:50]:
            print(f"  ✗ {e}")
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more")
    else:
        print("  ✓ No errors found!")
    print()
    
    # Report warnings (heuristic flags - may be false positives)
    print(f"=== WARNINGS / FLAGGED FOR REVIEW ({len(warnings)}) ===")
    if warnings:
        for w in warnings[:100]:
            print(f"  ⚠ {w}")
        if len(warnings) > 100:
            print(f"  ... and {len(warnings) - 100} more")
    else:
        print("  ✓ No warnings!")
    print()
    
    # Final verdict
    if not errors:
        print("✓ ALL STRUCTURAL CHECKS PASSED")
    else:
        print(f"✗ {len(errors)} ERRORS FOUND - needs fixing")
    
    return len(errors)


if __name__ == "__main__":
    exit(main())
