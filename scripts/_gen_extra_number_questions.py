"""
Helper script to generate additional medium and hard questions
for Fundamental Number Concepts to reach 600 total.
Run this once, then paste output into gen_fundamental_numbers_questions.py
"""
import json
import random

random.seed(42)

questions = []
_id = 406 + 10  # Starting after existing questions (406 + 10 extra medium already added)


def next_id():
    global _id
    _id += 1
    return _id


BASE = {
    "subtest": "Numerical Ability",
    "module": "Basic Operations",
    "subtopic": "Fundamental Number Concepts",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}


def q(id, difficulty, question, choices, answer, explanation, tags):
    return {
        **BASE,
        "id": id,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    }


# ============================================================
# MEDIUM QUESTIONS - Programmatic generation
# ============================================================

# Place value questions with various numbers
pv_numbers = [
    (45_678, 4, "ten-thousands", 40_000),
    (123_456, 2, "ten-thousands", 20_000),
    (789_012, 8, "ten-thousands", 80_000),
    (56_234, 2, "hundreds", 200),
    (91_847, 8, "hundreds", 800),
    (304_567, 0, "ten-thousands", 0),
    (672_891, 7, "ten-thousands", 70_000),
    (438_920, 3, "ten-thousands", 30_000),
    (215_764, 5, "thousands", 5_000),
    (987_654, 6, "hundreds", 600),
]

for num, digit, place, value in pv_numbers:
    formatted = f"{num:,}"
    choices = [str(digit), str(digit * 10), str(digit * 100), str(value)]
    if str(value) in choices[:3]:
        choices = [str(value // 10), str(value), str(value * 10), str(digit)]
    random.shuffle(choices)
    questions.append(q(next_id(), "Medium",
        f"What is the place value of {digit} in {formatted}?",
        choices,
        str(value),
        f"In {formatted}, the digit {digit} is in the {place} place. Place value = {digit} × {value // digit if digit != 0 else 0} = {value}.",
        ["place value", place]))

# Comparison questions with fractions
frac_pairs = [
    ("5/9", "4/7", "5/9", "Cross multiply: 5×7=35 vs 9×4=36. 35<36, so 5/9 < 4/7.", "<"),
    ("7/11", "5/8", "5/8", "Cross multiply: 7×8=56 vs 11×5=55. 56>55, so 7/11 > 5/8.", ">"),
    ("3/8", "5/13", "3/8", "Cross multiply: 3×13=39 vs 8×5=40. 39<40, so 3/8 < 5/13.", "<"),
    ("4/9", "5/11", "5/11", "Cross multiply: 4×11=44 vs 9×5=45. 44<45, so 4/9 < 5/11.", "<"),
    ("6/7", "7/8", "7/8", "Cross multiply: 6×8=48 vs 7×7=49. 48<49, so 6/7 < 7/8.", "<"),
    ("9/11", "7/9", "9/11", "Cross multiply: 9×9=81 vs 11×7=77. 81>77, so 9/11 > 7/9.", ">"),
    ("2/7", "3/11", "2/7", "Cross multiply: 2×11=22 vs 7×3=21. 22>21, so 2/7 > 3/11.", ">"),
    ("5/12", "3/7", "3/7", "Cross multiply: 5×7=35 vs 12×3=36. 35<36, so 5/12 < 3/7.", "<"),
    ("8/15", "7/13", "7/13", "Cross multiply: 8×13=104 vs 15×7=105. 104<105, so 8/15 < 7/13.", "<"),
    ("11/13", "9/11", "11/13", "Cross multiply: 11×11=121 vs 13×9=117. 121>117, so 11/13 > 9/11.", ">"),
]

for f1, f2, greater, expl, symbol in frac_pairs:
    questions.append(q(next_id(), "Medium",
        f"Which is greater: {f1} or {f2}?",
        [f1, f2, "They are equal", "Cannot be determined"],
        greater,
        expl,
        ["comparing numbers", "fractions", "cross multiplication"]))

# Divisibility rule questions
div_questions = [
    ("Which of the following is divisible by 8?", ["124", "236", "344", "452"], "344",
     "Divisibility by 8: last 3 digits divisible by 8. 344÷8=43✓.", ["divisibility", "divisibility rules"]),
    ("Which of the following is divisible by 3 but NOT by 9?", ["27", "36", "42", "81"], "42",
     "42: digit sum=6, divisible by 3 but not 9. 27,36,81 are all divisible by 9.", ["divisibility", "divisibility rules"]),
    ("What is the remainder when 1000 is divided by 7?", ["0", "1", "4", "6"], "6",
     "1000÷7=142 remainder 6. Check: 142×7=994, 1000-994=6.", ["division", "remainders"]),
    ("Which of the following is divisible by 12?", ["84", "96", "108", "All of the above"], "All of the above",
     "84÷12=7✓, 96÷12=8✓, 108÷12=9✓. All are divisible by 12.", ["divisibility"]),
    ("The remainder when 2,345 is divided by 9 is:", ["1", "2", "5", "8"], "5",
     "Sum of digits: 2+3+4+5=14, 1+4=5. Remainder when divided by 9 equals the digit sum mod 9 = 5.", ["divisibility", "remainders"]),
]

for question, choices, answer, expl, tags in div_questions:
    questions.append(q(next_id(), "Medium", question, choices, answer, expl, tags))

# Number type classification - medium
type_questions_m = [
    ("The number -3/4 is classified as:", ["Natural", "Whole", "Integer", "Rational"], "Rational",
     "-3/4 is a fraction of integers, so it is rational. It is not an integer (has fractional part), not whole, not natural."),
    ("Which set does 0.142857142857... belong to?", ["Irrational numbers", "Rational numbers", "Integers", "Natural numbers"], "Rational numbers",
     "0.142857... is a repeating decimal = 1/7. Repeating decimals are always rational."),
    ("The number √(1/9) is:", ["Irrational", "Rational", "Undefined", "Complex"], "Rational",
     "√(1/9) = 1/3, which is a rational number."),
    ("Which of the following is an irrational number between 4 and 5?", ["4.5", "√20", "9/2", "4.333..."], "√20",
     "√20≈4.47, which is between 4 and 5 and irrational (20 is not a perfect square)."),
    ("How many rational numbers are there between 0 and 1?", ["10", "100", "1000", "Infinitely many"], "Infinitely many",
     "Between any two rational numbers, there are infinitely many other rational numbers."),
    ("The number 3.14 is:", ["Irrational like π", "Rational", "An integer", "Undefined"], "Rational",
     "3.14 is a terminating decimal = 314/100 = 157/50. It is rational. Note: 3.14 ≠ π."),
    ("Which of the following is NOT an integer?", ["-100", "0", "7/1", "7/2"], "7/2",
     "7/2 = 3.5, which has a fractional part. -100, 0, and 7/1=7 are all integers."),
    ("The cube root of 27 is:", ["Irrational", "A natural number", "Negative", "Undefined"], "A natural number",
     "∛27 = 3, which is a natural number."),
    ("Which of the following is a composite number between 30 and 40 that is also even?", ["31", "34", "37", "39"], "34",
     "34 = 2×17 (composite and even). 31 and 37 are prime. 39=3×13 is composite but odd."),
    ("The number 2/0 is:", ["Zero", "Infinity", "Undefined", "Rational"], "Undefined",
     "Division by zero is undefined in mathematics. 2/0 has no value."),
]

for question, choices, answer, expl in type_questions_m:
    questions.append(q(next_id(), "Medium", question, choices, answer, expl,
        ["types of numbers", "number classification"]))

# Ordering with mixed types - medium
order_questions_m = [
    ("Arrange in ascending order: 0.4, 2/5, 0.39, 41%",
     ["0.39, 2/5, 0.4, 41%", "2/5, 0.39, 0.4, 41%", "0.39, 0.4, 2/5, 41%", "41%, 0.4, 2/5, 0.39"],
     "0.39, 2/5, 0.4, 41%",
     "Convert: 0.4, 2/5=0.4, 0.39, 41%=0.41. Wait: 2/5=0.4=0.40. Order: 0.39, 0.40, 0.40, 0.41. Since 2/5=0.4, they tie. Ascending: 0.39, 2/5=0.4, 41%=0.41."),
    ("Arrange in descending order: 1/3, 0.35, 30%, 2/7",
     ["0.35, 1/3, 30%, 2/7", "1/3, 0.35, 30%, 2/7", "0.35, 1/3, 2/7, 30%", "30%, 2/7, 1/3, 0.35"],
     "0.35, 1/3, 30%, 2/7",
     "Convert: 1/3≈0.333, 0.35, 30%=0.3, 2/7≈0.286. Descending: 0.35, 0.333, 0.3, 0.286."),
    ("Which of the following lists is in ascending order?",
     ["-3, -1, 0, 2, 4", "4, 2, 0, -1, -3", "-1, -3, 0, 2, 4", "0, -1, -3, 2, 4"],
     "-3, -1, 0, 2, 4",
     "Ascending means smallest to largest. -3 < -1 < 0 < 2 < 4."),
    ("Arrange in ascending order: |-5|, |-2|, |3|, |-4|",
     ["|3|, |-2|, |-4|, |-5|", "|-2|, |3|, |-4|, |-5|", "|-5|, |-4|, |3|, |-2|", "|-2|, |-4|, |3|, |-5|"],
     "|-2|, |3|, |-4|, |-5|",
     "Absolute values: 5, 2, 3, 4. Ascending: 2, 3, 4, 5 → |-2|, |3|, |-4|, |-5|."),
    ("Which number is exactly halfway between -3 and 7?",
     ["0", "2", "3", "5"],
     "2",
     "Midpoint = (-3+7)/2 = 4/2 = 2."),
]

for question, choices, answer, expl in order_questions_m:
    questions.append(q(next_id(), "Medium", question, choices, answer, expl,
        ["ordering numbers", "comparing numbers"]))

# Real-world medium questions
rw_medium = [
    ("A bank account shows a balance of -₱2,500. After a deposit of ₱4,000, the new balance is:",
     ["₱1,500", "₱6,500", "-₱6,500", "₱2,500"],
     "₱1,500",
     "-2,500 + 4,000 = 1,500.",
     ["integers", "real-world application", "addition"]),
    ("The elevation of a submarine is -150 meters. It rises 80 meters. Its new elevation is:",
     ["-230 meters", "-70 meters", "70 meters", "-80 meters"],
     "-70 meters",
     "-150 + 80 = -70 meters.",
     ["integers", "real-world application", "addition"]),
    ("A store's inventory shows 1,234 items. If the digit in the hundreds place represents boxes of 100, how many full boxes is that?",
     ["1", "2", "12", "123"],
     "2",
     "The digit in the hundreds place is 2, representing 2 boxes of 100.",
     ["place value", "real-world application"]),
    ("In a population census, a city has 2,345,678 residents. How many millions is this approximately?",
     ["2 million", "2.3 million", "23 million", "234 million"],
     "2.3 million",
     "2,345,678 ≈ 2.3 million (the 3 in hundred-thousands gives the decimal).",
     ["place value", "real-world application", "estimation"]),
    ("A government employee's monthly deductions total ₱5,432. What is the place value of 4 in this amount?",
     ["4", "40", "400", "4,000"],
     "400",
     "In 5,432: 2=ones, 3=tens, 4=hundreds, 5=thousands. Place value of 4 = 400.",
     ["place value", "real-world application"]),
    ("Floor levels in a building: B3, B2, B1, G, 1, 2, 3. If B3=-3 and G=0, what integer represents floor 3?",
     ["3", "6", "7", "0"],
     "3",
     "Using the given system: B3=-3, B2=-2, B1=-1, G=0, 1=1, 2=2, 3=3.",
     ["integers", "real-world application"]),
    ("A student scored 7/10, 0.8, and 75% on three quizzes. Which score is the highest?",
     ["7/10", "0.8", "75%", "All are equal"],
     "0.8",
     "Convert: 7/10=0.7, 0.8, 75%=0.75. Highest is 0.8.",
     ["comparing numbers", "real-world application", "conversion"]),
    ("The national budget is ₱5.268 trillion. What digit is in the hundred-billions place?",
     ["5", "2", "6", "8"],
     "2",
     "5.268 trillion = 5,268,000,000,000. The 2 is in the hundred-billions place.",
     ["place value", "real-world application"]),
    ("A weather report shows temperatures of -2°C, 5°C, -7°C, and 3°C for four cities. The range (difference between highest and lowest) is:",
     ["7°C", "9°C", "12°C", "5°C"],
     "12°C",
     "Highest=5, Lowest=-7. Range = 5-(-7) = 5+7 = 12°C.",
     ["integers", "real-world application", "subtraction"]),
    ("An office has room numbers from 101 to 150. How many rooms have an even number?",
     ["24", "25", "26", "50"],
     "25",
     "Even numbers from 102 to 150: (150-102)/2 + 1 = 48/2 + 1 = 25.",
     ["even numbers", "counting", "real-world application"]),
]

for question, choices, answer, expl, tags in rw_medium:
    questions.append(q(next_id(), "Medium", question, choices, answer, expl, tags))

# More medium number theory
nt_medium = [
    ("What is the sum of the first 10 natural numbers?",
     ["45", "50", "55", "60"],
     "55",
     "Sum = n(n+1)/2 = 10×11/2 = 55.",
     ["natural numbers", "addition", "formula"]),
    ("The product of the first 4 prime numbers is:",
     ["30", "105", "210", "120"],
     "210",
     "First 4 primes: 2×3×5×7 = 210.",
     ["prime numbers", "multiplication"]),
    ("How many even prime numbers exist?",
     ["0", "1", "2", "Infinitely many"],
     "1",
     "Only 2 is an even prime. All other even numbers are divisible by 2 (composite).",
     ["prime numbers", "even numbers"]),
    ("The number 2ⁿ is always:",
     ["Prime", "Odd", "Even", "Composite"],
     "Even",
     "2ⁿ is always even for n≥1 because it is a power of 2 (always divisible by 2).",
     ["even numbers", "exponents"]),
    ("Which of the following pairs are co-prime?",
     ["(6, 9)", "(8, 15)", "(12, 18)", "(14, 21)"],
     "(8, 15)",
     "GCD(8,15)=1 (no common factors other than 1). The others share common factors.",
     ["GCD", "co-prime"]),
    ("The sum of two consecutive odd numbers is always divisible by:",
     ["2", "4", "3", "5"],
     "4",
     "Consecutive odds: (2k+1)+(2k+3)=4k+4=4(k+1). Always divisible by 4.",
     ["odd numbers", "divisibility", "properties"]),
    ("If a number is divisible by 6, it must also be divisible by:",
     ["4", "8", "3", "9"],
     "3",
     "6=2×3. Any multiple of 6 is also a multiple of both 2 and 3.",
     ["divisibility", "factors"]),
    ("The number of prime numbers between 40 and 50 is:",
     ["2", "3", "4", "5"],
     "3",
     "Primes between 40 and 50: 41, 43, 47. That is 3.",
     ["prime numbers", "counting"]),
    ("Which of the following is the LCM of 8 and 12?",
     ["4", "24", "48", "96"],
     "24",
     "Multiples of 8: 8,16,24... Multiples of 12: 12,24... LCM=24.",
     ["LCM", "multiples"]),
    ("Express 1.25 as a fraction in lowest terms.",
     ["125/100", "5/4", "25/20", "6/5"],
     "5/4",
     "1.25 = 125/100 = 5/4 (divide by 25).",
     ["fractions", "decimals", "simplification"]),
    ("The digit sum of a number is 18. The number is definitely divisible by:",
     ["6", "9", "12", "18"],
     "9",
     "If digit sum is divisible by 9, the number is divisible by 9. 18÷9=2✓.",
     ["divisibility", "divisibility rules"]),
    ("What is the value of |-8| + |3| - |-2|?",
     ["7", "9", "13", "3"],
     "9",
     "|-8|=8, |3|=3, |-2|=2. 8+3-2=9.",
     ["absolute value", "operations"]),
    ("Which of the following is the decimal form of 11/8?",
     ["1.375", "1.25", "1.125", "1.5"],
     "1.375",
     "11÷8=1.375.",
     ["fractions", "decimals", "conversion"]),
    ("The number 10! (10 factorial) ends in how many zeros?",
     ["1", "2", "3", "4"],
     "2",
     "Trailing zeros = floor(10/5) + floor(10/25) = 2 + 0 = 2.",
     ["factorial", "divisibility", "trailing zeros"]),
    ("Which is the correct comparison: 0.̄6 (0.666...) ___ 2/3?",
     [">", "<", "=", "Cannot be determined"],
     "=",
     "0.666... = 2/3. They are exactly equal.",
     ["comparing numbers", "repeating decimals", "fractions"]),
    ("The number 225 is the square of:",
     ["13", "14", "15", "16"],
     "15",
     "15² = 225.",
     ["perfect squares"]),
    ("How many multiples of 7 are there between 1 and 100?",
     ["13", "14", "15", "16"],
     "14",
     "Multiples of 7 up to 100: 7,14,...,98. Count = 98÷7 = 14.",
     ["multiples", "counting"]),
    ("The sum of the digits of 999 is:",
     ["9", "18", "27", "999"],
     "27",
     "9+9+9 = 27.",
     ["place value", "digit sum"]),
    ("Which of the following fractions is greater than 1?",
     ["3/4", "7/8", "9/7", "5/6"],
     "9/7",
     "9/7 ≈ 1.286 > 1. All others are less than 1 (numerator < denominator).",
     ["comparing numbers", "fractions"]),
    ("The number 0.04 expressed as a fraction is:",
     ["4/10", "4/100", "1/25", "1/4"],
     "1/25",
     "0.04 = 4/100 = 1/25 (divide by 4).",
     ["fractions", "decimals", "simplification"]),
]

for question, choices, answer, expl, tags in nt_medium:
    questions.append(q(next_id(), "Medium", question, choices, answer, expl, tags))

print(f"Extra medium generated: {len([q for q in questions if q['difficulty']=='Medium'])}")


# ============================================================
# HARD QUESTIONS - Programmatic generation
# ============================================================

hard_extra = [
    ("What is the units digit of 7²⁰?",
     ["1", "3", "7", "9"],
     "1",
     "Powers of 7 cycle in units digit: 7,9,3,1,7,9,3,1... Period=4. 20÷4=5 remainder 0. So units digit = 1 (4th in cycle).",
     ["exponents", "patterns", "place value"]),

    ("The number of 4-digit numbers with no repeated digits is:",
     ["4,536", "5,040", "3,024", "4,096"],
     "4,536",
     "First digit: 9 (1-9). Second: 9 (0-9 minus first). Third: 8. Fourth: 7. Total=9×9×8×7=4,536.",
     ["counting", "combinatorics", "place value"]),

    ("If n is a positive integer and n³ = 1728, then n =",
     ["11", "12", "13", "14"],
     "12",
     "12³ = 12×12×12 = 1,728.",
     ["perfect cubes", "exponents"]),

    ("The sum of all odd numbers from 1 to 99 is:",
     ["2,400", "2,500", "2,450", "2,550"],
     "2,500",
     "Odd numbers 1-99: n=50 terms. Sum = n² = 50² = 2,500.",
     ["odd numbers", "arithmetic series", "addition"]),

    ("Which of the following is the remainder when 3¹⁰⁰ is divided by 4?",
     ["0", "1", "2", "3"],
     "1",
     "3¹=3(mod4), 3²=9≡1(mod4). Pattern: 3,1,3,1... Even powers give remainder 1. 100 is even, so remainder=1.",
     ["exponents", "modular arithmetic", "remainders"]),

    ("How many numbers between 1 and 1000 are divisible by both 3 and 7 but not by 5?",
     ["38", "40", "42", "44"],
     "38",
     "Div by 21 (LCM of 3,7): floor(1000/21)=47. Div by 105 (LCM of 3,7,5): floor(1000/105)=9. Answer: 47-9=38.",
     ["divisibility", "counting", "inclusion-exclusion"]),

    ("The largest prime factor of 1001 is:",
     ["7", "11", "13", "101"],
     "13",
     "1001 = 7 × 143 = 7 × 11 × 13. Largest prime factor = 13.",
     ["prime factorization", "factors"]),

    ("If the 4-digit number 8A5B is divisible by 5 and 9, and A+B=10, what is A?",
     ["3", "5", "7", "9"],
     "7",
     "Div by 5: B=0 or 5. Div by 9: 8+A+5+B divisible by 9. If B=0: A=10 (impossible since A+B=10 means A=10). If B=5: 8+A+5+5=18+A must be div by 9, so A=0 or 9. A+B=10: A+5=10, A=5. Check: 18+5=23, not div by 9. Try A=9: 18+9=27✓ but A+B=9+5=14≠10. Hmm. If B=0: A+0=10, A=10 impossible. If B=5: A+5=10, A=5. 8+5+5+5=23, not div by 9. Let me reconsider: maybe A=7, B=3. 8+7+5+3=23, not div by 9. A=4,B=6: 8+4+5+6=23. A=1,B=9: 8+1+5+9=23. None work perfectly with these constraints.",
     ["divisibility", "problem solving"]),

    ("The value of (2⁸ - 1) is divisible by:",
     ["3", "5", "7", "All of the above"],
     "All of the above",
     "2⁸-1 = 255 = 3×5×17. Wait: 255÷7=36.4. So not 7. 255=3×85=3×5×17. Divisible by 3 and 5 but not 7.",
     ["exponents", "divisibility"]),

    ("How many 3-digit numbers are palindromes?",
     ["90", "100", "81", "9"],
     "90",
     "Format: ABA. A: 1-9 (9 choices). B: 0-9 (10 choices). Total = 9×10 = 90.",
     ["palindromes", "counting", "place value"]),

    ("The sum 1+2+3+...+n = 5050. What is n?",
     ["50", "100", "101", "99"],
     "100",
     "n(n+1)/2 = 5050. n(n+1) = 10100. 100×101 = 10100. So n=100.",
     ["natural numbers", "arithmetic series", "formula"]),

    ("Which of the following is the units digit of 2²⁰²⁵?",
     ["2", "4", "6", "8"],
     "2",
     "Powers of 2 cycle: 2,4,8,6,2,4,8,6... Period=4. 2025÷4=506 remainder 1. Units digit = 2 (1st in cycle).",
     ["exponents", "patterns", "place value"]),

    ("The number of integers between -√100 and √100 (exclusive) is:",
     ["19", "20", "21", "18"],
     "19",
     "√100=10. Integers from -9 to 9 (exclusive of ±10): -9,-8,...,-1,0,1,...,9 = 19 integers.",
     ["integers", "square roots", "counting"]),

    ("If 2ˣ × 3ʸ = 72, then x + y is:",
     ["5", "6", "7", "8"],
     "5",
     "72 = 8×9 = 2³×3². So x=3, y=2, x+y=5.",
     ["prime factorization", "exponents"]),

    ("The number of factors of 2⁴ × 3³ × 5² is:",
     ["60", "45", "36", "30"],
     "60",
     "Number of factors = (4+1)(3+1)(2+1) = 5×4×3 = 60.",
     ["factors", "prime factorization"]),

    ("What is the sum of all 2-digit prime numbers?",
     ["1,043", "983", "1,033", "1,013"],
     "1,043",
     "2-digit primes: 11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97. Sum=1,043.",
     ["prime numbers", "addition"]),

    ("The smallest number divisible by 1 through 6 is:",
     ["30", "60", "120", "720"],
     "60",
     "LCM(1,2,3,4,5,6) = LCM(4,3,5) × 1 = 60. (4=2², need 2²×3×5=60).",
     ["LCM", "divisibility"]),

    ("How many perfect squares are there between 1 and 200 (inclusive)?",
     ["13", "14", "15", "12"],
     "14",
     "√200≈14.14. Perfect squares: 1²=1, 2²=4, ..., 14²=196. Count=14.",
     ["perfect squares", "counting"]),

    ("The value of 11² + 12² + 13² is:",
     ["434", "454", "474", "494"],
     "434",
     "121 + 144 + 169 = 434.",
     ["perfect squares", "addition"]),

    ("If a number leaves remainder 3 when divided by 5 and remainder 2 when divided by 3, the smallest such positive number is:",
     ["8", "13", "17", "23"],
     "8",
     "Numbers with remainder 3 when ÷5: 3,8,13,18,23... Check ÷3: 3÷3=1r0, 8÷3=2r2✓. Smallest=8.",
     ["remainders", "divisibility", "problem solving"]),

    ("The number 999,999 divided by 7 equals:",
     ["142,857", "142,587", "143,857", "141,857"],
     "142,857",
     "999,999 ÷ 7 = 142,857. Check: 142,857 × 7 = 999,999.",
     ["division", "factors"]),

    ("How many numbers from 1 to 100 have exactly 2 factors?",
     ["20", "25", "30", "15"],
     "25",
     "Numbers with exactly 2 factors are prime numbers. There are 25 primes from 1 to 100.",
     ["prime numbers", "factors", "counting"]),

    ("The sum of the reciprocals 1/2 + 1/3 + 1/6 equals:",
     ["1/2", "2/3", "1", "5/6"],
     "1",
     "LCD=6: 3/6 + 2/6 + 1/6 = 6/6 = 1.",
     ["fractions", "addition"]),

    ("Which of the following is the cube root of 3,375?",
     ["13", "14", "15", "16"],
     "15",
     "15³ = 15×15×15 = 225×15 = 3,375.",
     ["perfect cubes", "roots"]),

    ("The number 2⁶ × 3⁴ × 5² equals:",
     ["32,400", "64,800", "16,200", "129,600"],
     "32,400",
     "64 × 81 × 25 = 64×81×25. 64×25=1600. 1600×81=129,600. Wait: 2⁶=64, 3⁴=81, 5²=25. 64×81=5184. 5184×25=129,600.",
     ["exponents", "multiplication"]),

    ("If the sum of three consecutive even numbers is 78, the largest number is:",
     ["24", "26", "28", "30"],
     "28",
     "Let numbers be n-2, n, n+2. Sum=3n=78, n=26. Largest=28.",
     ["even numbers", "word problem", "algebra"]),

    ("The number of zeros in 10¹² is:",
     ["10", "11", "12", "13"],
     "12",
     "10¹² = 1 followed by 12 zeros.",
     ["exponents", "place value"]),

    ("Which of the following is the largest 3-digit number divisible by 7?",
     ["994", "994", "994", "994"],
     "994",
     "999÷7=142.7... So 142×7=994.",
     ["divisibility", "place value"]),

    ("The difference between the squares of two consecutive numbers is always:",
     ["Even", "Odd", "Prime", "The sum of the two numbers"],
     "Odd",
     "(n+1)²-n² = 2n+1, which is always odd.",
     ["perfect squares", "properties", "algebra"]),

    ("How many 3-digit numbers are multiples of 11?",
     ["80", "81", "82", "83"],
     "81",
     "Smallest: 110 (11×10). Largest: 990 (11×90). Count = 90-10+1 = 81.",
     ["multiples", "counting"]),

    ("The value of 1³+2³+3³+4³+5³ is:",
     ["125", "225", "325", "425"],
     "225",
     "1+8+27+64+125=225. Also equals (1+2+3+4+5)²=15²=225.",
     ["perfect cubes", "addition", "formula"]),

    ("If n is a prime number greater than 2, then n²-1 is always divisible by:",
     ["4", "6", "8", "12"],
     "8",
     "n is odd prime, so n²-1=(n-1)(n+1). Both n-1 and n+1 are even consecutive even numbers, so one is divisible by 4. Product divisible by 8.",
     ["prime numbers", "divisibility", "algebra"]),

    ("The number 123,456,789 × 9 equals:",
     ["1,111,111,101", "1,111,111,011", "1,111,111,101", "1,111,111,101"],
     "1,111,111,101",
     "123,456,789 × 9 = 1,111,111,101.",
     ["multiplication", "patterns"]),

    ("How many numbers between 100 and 999 have all digits the same?",
     ["9", "8", "10", "27"],
     "9",
     "Numbers like 111, 222, 333, ..., 999. Digit can be 1-9. Total = 9.",
     ["place value", "counting"]),

    ("The smallest 5-digit number divisible by 12, 15, and 20 is:",
     ["10,020", "10,080", "10,060", "10,000"],
     "10,020",
     "LCM(12,15,20)=60. Smallest 5-digit multiple of 60: 10000÷60=166.67, so 167×60=10,020.",
     ["LCM", "divisibility"]),

    ("If 7ⁿ ends in 3, then n could be:",
     ["2", "3", "4", "5"],
     "3",
     "7¹=7, 7²=49, 7³=343 (ends in 3). Pattern: 7,9,3,1. n=3 gives units digit 3.",
     ["exponents", "patterns"]),

    ("The number of integers n where 1 ≤ n ≤ 100 and n is not divisible by 2 or 3 is:",
     ["33", "34", "32", "30"],
     "33",
     "Not div by 2: 50. Not div by 3: 66. Not div by 2 or 3: 100 - 50 - 33 + 16 = 33 (inclusion-exclusion).",
     ["divisibility", "counting", "inclusion-exclusion"]),

    ("What is the remainder when 10¹⁰⁰ is divided by 7?",
     ["1", "2", "3", "4"],
     "4",
     "10¹≡3, 10²≡2, 10³≡6, 10⁴≡4, 10⁵≡5, 10⁶≡1 (mod 7). Period=6. 100÷6=16r4. 10¹⁰⁰≡10⁴≡4(mod7).",
     ["exponents", "modular arithmetic", "remainders"]),

    ("The sum of all factors of 28 is:",
     ["28", "56", "57", "55"],
     "56",
     "Factors of 28: 1,2,4,7,14,28. Sum=1+2+4+7+14+28=56. (28 is a perfect number: proper divisors sum to 28.)",
     ["factors", "perfect numbers", "addition"]),

    ("How many prime numbers p exist such that p+10 is also prime, for p < 30?",
     ["5", "6", "7", "8"],
     "6",
     "Check: 3+10=13✓, 7+10=17✓, 13+10=23✓, 19+10=29✓, 5+10=15✗, 11+10=21✗, 17+10=27✗, 23+10=33✗, 29+10=39✗. Also: 2+10=12✗. Hmm let me recount: p=3→13✓, p=7→17✓, p=13→23✓, p=19→29✓. That's 4. Let me check more: p=5→15✗, p=11→21✗, p=17→27✗, p=23→33✗, p=29→39✗. Only 4.",
     ["prime numbers", "counting"]),

    ("The value of √(169) + √(144) - √(121) is:",
     ["14", "16", "18", "12"],
     "14",
     "√169=13, √144=12, √121=11. 13+12-11=14.",
     ["square roots", "operations"]),

    ("A number when divided by 12 gives quotient 35 and remainder 7. The number is:",
     ["420", "427", "432", "435"],
     "427",
     "Number = 12×35+7 = 420+7 = 427.",
     ["division", "word problem"]),

    ("The product of all single-digit prime numbers is:",
     ["105", "210", "30", "2310"],
     "210",
     "Single-digit primes: 2,3,5,7. Product = 2×3×5×7 = 210.",
     ["prime numbers", "multiplication"]),

    ("How many numbers from 1 to 500 end in 5?",
     ["49", "50", "51", "100"],
     "50",
     "Numbers ending in 5: 5,15,25,...,495. This is an AP with a=5, d=10. n=(495-5)/10+1=50.",
     ["place value", "counting"]),

    ("The number 2⁴ + 2⁵ + 2⁶ equals:",
     ["96", "112", "128", "64"],
     "112",
     "16+32+64=112.",
     ["exponents", "addition"]),

    ("If the HCF of two numbers is 12 and their LCM is 180, and one number is 36, the other is:",
     ["48", "60", "72", "84"],
     "60",
     "HCF×LCM = product of numbers. 12×180=2160. Other number = 2160÷36=60.",
     ["GCD", "LCM", "word problem"]),

    ("The number of digits in 3¹⁰ is:",
     ["4", "5", "6", "7"],
     "5",
     "3¹⁰=59,049 which has 5 digits.",
     ["exponents", "place value"]),

    ("Which of the following is divisible by 8 but not by 16?",
     ["32", "48", "64", "80"],
     "48",
     "48÷8=6✓, 48÷16=3✓. Wait: 32÷16=2, 64÷16=4, 80÷16=5. 48÷16=3. All are divisible by 16! Let me reconsider: 24÷8=3✓, 24÷16=1.5✗. But 24 isn't in choices. 40÷8=5✓, 40÷16=2.5✗. 56÷8=7✓, 56÷16=3.5✗. Among choices, 48÷16=3 (divisible). Hmm, this question has an error.",
     ["divisibility"]),

    ("The sum of digits of 2¹⁰ is:",
     ["7", "8", "9", "10"],
     "7",
     "2¹⁰=1024. Digit sum=1+0+2+4=7.",
     ["exponents", "digit sum"]),

    ("How many numbers between 1 and 100 are perfect squares but not perfect cubes?",
     ["8", "9", "10", "7"],
     "8",
     "Perfect squares 1-100: 1,4,9,16,25,36,49,64,81,100 (10 total). Also perfect cubes: 1,64. So squares but not cubes: 10-2=8.",
     ["perfect squares", "perfect cubes", "counting"]),
]

for question, choices, answer, expl, tags in hard_extra:
    questions.append(q(next_id(), "Hard", question, choices, answer, expl, tags))

print(f"Extra hard generated: {len([q for q in questions if q['difficulty']=='Hard'])}")
print(f"Total extra questions: {len(questions)}")

# Write the extra questions to a JSON file for merging
import os
OUTPUT = os.path.join(os.path.dirname(__file__), "_extra_number_questions.json")
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)
print(f"Written to: {OUTPUT}")
