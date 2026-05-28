# Numerical Filing

## Explanations

### Introduction

Numerical filing is the system of arranging records, documents, and entries by their assigned numbers — whether those numbers are pure digits, alphanumeric codes, or hyphenated sequences. In government offices, nearly every document carries a numerical identifier: employee numbers, account codes, document tracking numbers, budget line items, and agency reference codes. A clerk who cannot file these correctly will misplace records that may take hours to locate.

In the Philippine Civil Service Examination (CSE) Sub-Professional level, numerical filing questions test whether an examinee can correctly arrange entries by account number, code number, or mixed alphanumeric identifiers. These questions require precision because a single transposed digit or misread prefix changes the filing position entirely. Unlike alphabetical filing — where context clues help you guess approximate positions — numerical filing demands exact, mechanical comparison.

Numerical filing is the backbone of government records management. The Commission on Audit (COA) tracks thousands of transactions by voucher number. The Civil Service Commission (CSC) assigns employee numbers to every government worker. The Department of Budget and Management (DBM) organizes expenditures by budget codes. Mastering numerical filing means mastering the language that government paperwork actually speaks.

### Why Numerical Filing Is Tested in the CSE

- Government employees retrieve records by document tracking numbers daily.
- Budget codes (PS, MOOE, CO) organize all government expenditures and must be filed accurately.
- Employee numbers are the primary identifier in personnel records across all agencies.
- Account codes link transactions to specific budget line items — misfiling delays audits.
- Clerks must distinguish between ascending and descending filing systems used by different offices.
- Mixed alphanumeric codes (like DTN-2024-0001) require segment-by-segment comparison skills.
- Numerical filing errors are harder to detect than alphabetical errors because numbers lack contextual meaning.
- The skill demonstrates the precision and systematic thinking required for clerical positions.

### Common Mistakes Examinees Make

1. Comparing numbers as strings (digit by digit) when they should be compared as whole numeric values.
2. Ignoring leading zeros — treating "007" and "7" as different values when they represent the same number.
3. Filing alphanumeric codes by the numeric portion first instead of the alphabetic prefix first.
4. Confusing ascending order (smallest first) with descending order (largest first).
5. Treating hyphenated codes as single numbers instead of comparing each segment separately.
6. Mishandling codes of different lengths — assuming longer codes always come after shorter ones.
7. Comparing the year segment numerically when it should be compared as a unit within a hyphenated code.
8. Forgetting that in mixed alphanumeric filing, the alphabetic prefix determines primary position.

### Learning Objectives

By the end of this lesson, you should be able to:

- File pure account numbers in correct ascending and descending order.
- Compare digit sequences from left to right applying the shorter-number-first rule.
- File alphanumeric code numbers by treating the prefix as the primary sort key.
- Compare numeric portions as whole numbers (not digit-by-digit strings).
- Distinguish between ascending and descending filing systems and apply each correctly.
- Break hyphenated codes into segments and compare each segment in sequence.
- Handle mixed alphanumeric entries where letters and numbers coexist.
- Apply these rules quickly and accurately under exam time pressure.

### 4.1 Filing by Account Number

Account numbers are pure numeric identifiers assigned to records, personnel, or transactions. In Philippine government offices, these appear as employee numbers (2024-001), voucher numbers (0001234), and transaction codes (100045).

**Core Rule:** Compare account numbers digit by digit from left to right. The first position where digits differ determines the filing order. If all compared digits are identical but one number is shorter, the shorter number comes first.

#### Basic Digit-by-Digit Comparison

When two account numbers have the same length, compare them position by position:

| Position | Number A: 1023 | Number B: 1045 | Result |
|----------|---------------|---------------|--------|
| 1st digit | 1 | 1 | Same — continue |
| 2nd digit | 0 | 0 | Same — continue |
| 3rd digit | 2 | 4 | 2 < 4 → A comes first |

**Filing order:** 1023, 1045

Another example:

| Position | Number A: 3056 | Number B: 3012 | Result |
|----------|---------------|---------------|--------|
| 1st digit | 3 | 3 | Same — continue |
| 2nd digit | 0 | 0 | Same — continue |
| 3rd digit | 5 | 1 | 1 < 5 → B comes first |

**Filing order:** 3012, 3056

> 🤔 **Why does this work?** Digit-by-digit comparison from left to right works because our number system is positional — the leftmost digit carries the greatest value. A difference in the first digit (thousands place in a 4-digit number) represents a much larger gap than a difference in the last digit (ones place). By comparing left to right, you identify the most significant difference first, which is exactly what determines which number is smaller or larger. This mirrors how we naturally read numbers and ensures consistent ordering without needing to calculate actual values.

#### The Shorter-Number Rule

When one number is shorter than another but all its digits match the leading digits of the longer number, the shorter number files first.

| Number A | Number B | Comparison | Order |
|----------|----------|------------|-------|
| 103 | 1034 | 1-0-3 matches 1-0-3 in 1034; A is shorter | 103 first |
| 25 | 251 | 2-5 matches 2-5 in 251; A is shorter | 25 first |
| 7 | 72 | 7 matches 7 in 72; A is shorter | 7 first |

**Why?** A shorter number with identical leading digits is numerically smaller. 103 < 1034 because 103 has no digit in the fourth position — effectively, it is "103_" where the blank is less than any digit.

**Important exception:** If the digits do NOT match before the shorter number ends, normal comparison applies:

| Number A | Number B | Comparison | Order |
|----------|----------|------------|-------|
| 15 | 142 | 1st digits match (1=1); 2nd digits: 5 vs. 4 → 4 < 5 | 142 first |
| 39 | 381 | 1st digits match (3=3); 2nd digits: 9 vs. 8 → 8 < 9 | 381 first |

#### Leading Zeros

In government filing systems, leading zeros are significant for maintaining uniform code lengths but do NOT change the numeric value for comparison purposes.

| Code | Numeric Value | Filed Position |
|------|--------------|----------------|
| 007 | 7 | Same as 7 |
| 012 | 12 | Same as 12 |
| 0234 | 234 | Same as 234 |

**Rule:** When all numbers in a set have the same number of digits (padded with leading zeros), compare digit by digit as normal. When numbers have different lengths, compare their numeric values — leading zeros do not give a number higher priority.

**Example with uniform-length codes (employee numbers):**

Arrange: 2024-003, 2024-001, 2024-012, 2024-002

All have the same format (YYYY-NNN), so compare the sequence portion digit by digit:
- 001, 002, 003, 012

**Filing order:** 2024-001, 2024-002, 2024-003, 2024-012

> ⚠️ **Misconception:** "Leading zeros make a number come first because 0 is the smallest digit."
>
> **Why it fails:** If you compare "007" and "12" digit by digit as strings, you would get 0 < 1, placing 007 before 12. But numerically, 7 < 12, so 007 should still come before 12. The issue arises when comparing "099" and "12" — string comparison gives 0 < 1 (099 first), but numerically 12 < 99 (12 first). The correct approach depends on context: if all codes have the same length (like 001, 002, 099), digit-by-digit works perfectly. If codes have different lengths, compare numeric values.
>
> **Correct model:** For uniform-length codes (all padded to the same number of digits), digit-by-digit comparison is safe and correct. For mixed-length codes, strip leading zeros and compare as whole numbers.

#### Practice Arrangement: Employee Numbers

Arrange these CSC employee numbers in ascending filing order:

2024-015, 2024-003, 2024-100, 2024-009, 2024-042

**Step 1:** All share the prefix "2024-" — compare only the sequence numbers.
**Step 2:** Sequence numbers: 015, 003, 100, 009, 042
**Step 3:** As 3-digit uniform codes, compare digit by digit:
- 003 (smallest — starts with 00)
- 009 (next — starts with 00, third digit 9 > 3)
- 015 (starts with 01)
- 042 (starts with 04)
- 100 (starts with 10)

**Filing order:**
1. 2024-003
2. 2024-009
3. 2024-015
4. 2024-042
5. 2024-100

### 4.2 Filing by Code Number

Code numbers combine an alphabetic prefix with a numeric portion. In Philippine government offices, these appear as budget codes (PS-101, MOOE-205, CO-301), account codes (ACCT-1001, ACCT-2045), and agency reference codes (CSC-NCR-001, COA-R3-045).

**Core Rule:** Treat the alphabetic prefix as the PRIMARY filing unit. Compare prefixes alphabetically first. Only when prefixes are identical do you compare the numeric portion — and compare it as a whole number (numerically), not digit by digit as a string.

#### Why Numeric Portions Are Compared as Numbers, Not Strings

This is the critical distinction between filing by account number and filing by code number:

| Method | Comparing "PS-9" vs "PS-85" | Result |
|--------|----------------------------|--------|
| String comparison (digit by digit) | 9 vs. 8 → 9 > 8 → PS-85 first | ❌ WRONG |
| Numeric comparison (as whole numbers) | 9 vs. 85 → 9 < 85 → PS-9 first | ✅ CORRECT |

**Why the difference?** Account numbers (like employee IDs) are typically uniform-length codes designed for digit-by-digit comparison. Code numbers use the numeric portion as a meaningful quantity — PS-9 is the 9th item, PS-85 is the 85th item. Filing them numerically preserves their sequential meaning.

> 🤔 **Why does this work?** Code numbers use their numeric portion as a sequential counter — MOOE-9 is the 9th MOOE item, MOOE-85 is the 85th. If you compared digit-by-digit, MOOE-9 would file AFTER MOOE-85 (because 9 > 8 in the first digit position), destroying the natural sequence. Numeric comparison preserves the intended order: item 9 comes before item 85, just as it would in a numbered list. The alphabetic prefix groups related items together, and the number orders them within that group.

#### Budget Code Filing Example

Philippine government budgets use three main categories:
- **PS** (Personal Services) — salaries and benefits
- **MOOE** (Maintenance and Other Operating Expenses) — supplies, utilities, travel
- **CO** (Capital Outlay) — equipment, buildings, vehicles

Arrange these budget codes: PS-101, CO-301, MOOE-205, PS-15, CO-42, MOOE-1003

**Step 1:** Group by alphabetic prefix.
- CO: CO-301, CO-42
- MOOE: MOOE-205, MOOE-1003
- PS: PS-101, PS-15

**Step 2:** Within each prefix group, arrange by numeric value.
- CO: 42 < 301 → CO-42, CO-301
- MOOE: 205 < 1003 → MOOE-205, MOOE-1003
- PS: 15 < 101 → PS-15, PS-101

**Step 3:** Combine groups in alphabetical prefix order.

**Filing order:**
1. CO-42
2. CO-301
3. MOOE-205
4. MOOE-1003
5. PS-15
6. PS-101

#### Account Code Filing Example

Arrange these account codes: ACCT-2045, ACCT-1001, ACCT-999, ACCT-10050, ACCT-88

**Step 1:** All share the prefix "ACCT" — compare numeric portions as whole numbers.
**Step 2:** Numeric values: 2045, 1001, 999, 10050, 88
**Step 3:** Order numerically: 88 < 999 < 1001 < 2045 < 10050

**Filing order:**
1. ACCT-88
2. ACCT-999
3. ACCT-1001
4. ACCT-2045
5. ACCT-10050

Notice that ACCT-88 comes before ACCT-999 even though "88" starts with 8 and "999" starts with 9. String comparison would incorrectly place ACCT-999 first (because 9 > 8 in the first position). Numeric comparison correctly identifies 88 < 999.

> ⚠️ **Misconception:** "When codes have the same prefix, compare the numbers digit by digit from left to right, just like account numbers."
>
> **Why it fails:** Consider ACCT-9 vs. ACCT-85. Digit-by-digit comparison says 9 > 8, so ACCT-85 would come first. But ACCT-9 represents a smaller quantity (the 9th account) and should file before ACCT-85 (the 85th account). Digit-by-digit comparison only works when all numeric portions have the same number of digits.
>
> **Correct model:** For code numbers with alphabetic prefixes, always compare the numeric portion as a whole number. ACCT-9 (value: 9) comes before ACCT-85 (value: 85) comes before ACCT-100 (value: 100). If all numeric portions happen to have the same length, digit-by-digit and numeric comparison produce the same result — but numeric comparison is always safe.

#### Mixed Prefix Comparison

When entries have different prefixes, alphabetical comparison of the prefix takes absolute priority:

| Entry A | Entry B | Prefix Comparison | Filing Order |
|---------|---------|-------------------|--------------|
| PS-1 | CO-9999 | CO before PS | CO-9999 first |
| MOOE-5 | CO-5000 | CO before MOOE | CO-5000 first |
| PS-100 | MOOE-1 | MOOE before PS | MOOE-1 first |

The numeric portion is ONLY compared when prefixes are identical.

### 4.3 Ascending and Descending Order

Filing systems use two directions: ascending (smallest to largest) and descending (largest to smallest). Most government filing systems default to ascending order, but some chronological systems use descending order to keep the most recent records at the front.

#### Ascending Order (Default)

Ascending order arranges entries from the smallest value to the largest. This is the standard in most filing systems and the default assumption on the CSE unless stated otherwise.

**Pure numbers — ascending:**

| Unsorted | Ascending Order |
|----------|----------------|
| 450, 123, 789, 234, 567 | 123, 234, 450, 567, 789 |
| 1005, 998, 1100, 1002, 999 | 998, 999, 1002, 1005, 1100 |

**Code numbers — ascending:**

| Unsorted | Ascending Order |
|----------|----------------|
| PS-50, PS-8, PS-120, PS-33 | PS-8, PS-33, PS-50, PS-120 |

#### Descending Order

Descending order arranges entries from the largest value to the smallest. Government offices use this when:
- Filing documents by date (most recent first) so the latest record is always on top.
- Organizing transaction logs where the newest entry needs immediate access.
- Maintaining priority queues where higher numbers indicate higher priority.

**Pure numbers — descending:**

| Unsorted | Descending Order |
|----------|-----------------|
| 450, 123, 789, 234, 567 | 789, 567, 450, 234, 123 |
| 1005, 998, 1100, 1002, 999 | 1100, 1005, 1002, 999, 998 |

**Code numbers — descending (within same prefix):**

| Unsorted | Descending Order |
|----------|-----------------|
| PS-50, PS-8, PS-120, PS-33 | PS-120, PS-50, PS-33, PS-8 |

**Important:** When a question asks for descending order with mixed prefixes, the alphabetic prefixes still sort alphabetically (A before B before C), but the numeric portions within each prefix group sort from largest to smallest.

**Example:** Arrange in descending numeric order: CO-50, PS-10, CO-200, PS-75, MOOE-30

**Step 1:** Group by prefix (alphabetical): CO, MOOE, PS
**Step 2:** Within each group, arrange numbers descending:
- CO: 200, 50
- MOOE: 30
- PS: 75, 10

**Filing order (descending within groups):**
1. CO-200
2. CO-50
3. MOOE-30
4. PS-75
5. PS-10

> 🤔 **Why does this work?** Descending order within alphabetical prefix groups works because the prefix identifies the *category* (which type of expense, which department) while the number identifies the *sequence* within that category. Reversing only the numeric order keeps related items grouped together while placing the most recent or highest-priority items first within each group. If you reversed both prefix and number order, related items would scatter across the file, defeating the purpose of categorical organization.

#### Recognizing Which Order the Question Wants

CSE questions signal the required order through specific phrases:

| Phrase in Question | Order Required |
|-------------------|----------------|
| "Arrange from smallest to largest" | Ascending |
| "Arrange in ascending order" | Ascending |
| "Arrange in filing order" (no other specification) | Ascending (default) |
| "Arrange from largest to smallest" | Descending |
| "Arrange in descending order" | Descending |
| "Arrange with the most recent first" | Descending (by date/number) |
| "Arrange in reverse order" | Descending |

**Default assumption:** If a question simply says "arrange in correct filing order" without specifying direction, use ascending order.

### 4.4 Hyphenated Codes: Segment-by-Segment Filing

Many government codes use hyphens to separate meaningful segments. Each segment carries distinct information and must be compared independently, in sequence.

**Common Philippine government hyphenated code formats:**

| Code Type | Format | Example | Segments |
|-----------|--------|---------|----------|
| Document Tracking Number | PREFIX-YEAR-SEQUENCE | DTN-2024-0001 | DTN / 2024 / 0001 |
| Employee Number | YEAR-SEQUENCE | 2024-001 | 2024 / 001 |
| Agency Regional Code | AGENCY-REGION-SEQUENCE | CSC-NCR-001 | CSC / NCR / 001 |
| Budget Item Code | CATEGORY-NUMBER | MOOE-205 | MOOE / 205 |

**Core Rule:** Treat each hyphen-separated segment as an independent comparison unit. Compare Segment 1 first; if equal, compare Segment 2; if equal, compare Segment 3; and so on. Alphabetic segments are compared alphabetically. Numeric segments are compared numerically (as whole numbers).

#### Document Tracking Numbers (DTN)

Arrange: DTN-2024-0015, DTN-2023-0100, DTN-2024-0003, DTN-2023-0045

**Step 1:** Compare Segment 1 (prefix): All are "DTN" — equal, move to Segment 2.

**Step 2:** Compare Segment 2 (year):
- DTN-2023-0100: year = 2023
- DTN-2023-0045: year = 2023
- DTN-2024-0015: year = 2024
- DTN-2024-0003: year = 2024

Group by year: 2023 entries first (smaller year), then 2024 entries.

**Step 3:** Compare Segment 3 (sequence) within each year group:
- 2023 group: 0045 vs. 0100 → 45 < 100 → 0045 first
- 2024 group: 0003 vs. 0015 → 3 < 15 → 0003 first

**Filing order:**
1. DTN-2023-0045
2. DTN-2023-0100
3. DTN-2024-0003
4. DTN-2024-0015

#### Agency Regional Codes

Arrange: CSC-NCR-001, COA-R3-045, CSC-R4-012, COA-NCR-003, CSC-NCR-015

**Step 1:** Compare Segment 1 (agency prefix) alphabetically:
- COA entries: COA-R3-045, COA-NCR-003
- CSC entries: CSC-NCR-001, CSC-R4-012, CSC-NCR-015

COA comes before CSC alphabetically.

**Step 2:** Within COA group, compare Segment 2 (region):
- COA-NCR-003: region = NCR
- COA-R3-045: region = R3

Compare alphabetically: NCR vs. R3 → N comes before R → NCR first.

**Step 3:** Within CSC group, compare Segment 2 (region):
- CSC-NCR-001: region = NCR
- CSC-NCR-015: region = NCR
- CSC-R4-012: region = R4

NCR comes before R4 (N before R). Within NCR subgroup, compare Segment 3:
- 001 vs. 015 → 1 < 15 → 001 first

**Filing order:**
1. COA-NCR-003
2. COA-R3-045
3. CSC-NCR-001
4. CSC-NCR-015
5. CSC-R4-012

> 🤔 **Why does this work?** Segment-by-segment comparison works because each segment in a hyphenated code encodes a different dimension of information — agency, region, and sequence number are three independent categories. Comparing them in order (left to right) creates a hierarchical sort: first by agency (the broadest category), then by region (a subdivision within the agency), then by sequence (the specific document within that region). This mirrors how physical filing cabinets are organized — you go to the right cabinet (agency), then the right drawer (region), then the right folder (sequence number).

#### Mixed Segment Types

When a segment contains both letters and numbers (like "R3" or "R12"), compare the alphabetic portion first, then the numeric portion:

| Segment A | Segment B | Comparison | Order |
|-----------|-----------|------------|-------|
| R3 | R12 | R = R; then 3 vs. 12 → 3 < 12 | R3 first |
| NCR | R1 | N vs. R → N < R | NCR first |
| R4A | R4B | R4 = R4; then A vs. B → A < B | R4A first |
| R10 | R9 | R = R; then 10 vs. 9 → 9 < 10 | R9 first |

### 4.5 Mixed Alphanumeric Filing

Mixed alphanumeric filing handles entries where letters and numbers coexist without a clear prefix-number structure. This occurs when filing codes from different systems together, or when entries have varying formats.

**Core Rule:** In mixed alphanumeric filing, letters come before numbers in the same position. Compare alphabetic portions first, then numeric portions.

#### The Letters-Before-Numbers Principle

When two entries begin differently — one with a letter and one with a number — the letter-starting entry files first:

| Entry A | Entry B | Rule Applied | Order |
|---------|---------|--------------|-------|
| A-101 | 1-101 | Letter A before digit 1 | A-101 first |
| B-500 | 200 | Letter B before digit 2 | B-500 first |
| Z-001 | 9999 | Letter Z before digit 9 | Z-001 first |

**Why?** This convention exists because most filing systems place alphabetic sections before numeric sections — just as a phone book places named entries before numbered listings.

#### Comparing Entries with the Same Starting Type

When entries all start with letters, compare alphabetically:

| Entry A | Entry B | Comparison | Order |
|---------|---------|------------|-------|
| ACCT-100 | BUD-50 | A before B | ACCT-100 first |
| PS-101 | MOOE-205 | M before P | MOOE-205 first |

When entries all start with numbers, compare numerically:

| Entry A | Entry B | Comparison | Order |
|---------|---------|------------|-------|
| 2024-001 | 2023-100 | 2023 < 2024 | 2023-100 first |
| 100-A | 95-B | 95 < 100 | 95-B first |

#### Complete Mixed Filing Example

Arrange: 2024-005, ACCT-1001, PS-101, 2023-100, MOOE-205, 100-A, CO-301

**Step 1:** Separate letter-starting entries from number-starting entries.
- Letter-starting: ACCT-1001, PS-101, MOOE-205, CO-301
- Number-starting: 2024-005, 2023-100, 100-A

**Step 2:** Arrange letter-starting entries (prefix alphabetically, then number numerically):
- ACCT-1001 (A)
- CO-301 (C)
- MOOE-205 (M)
- PS-101 (P)

**Step 3:** Arrange number-starting entries (first segment numerically):
- 100-A (first segment: 100)
- 2023-100 (first segment: 2023)
- 2024-005 (first segment: 2024)

**Step 4:** Letters before numbers — combine:

**Filing order:**
1. ACCT-1001
2. CO-301
3. MOOE-205
4. PS-101
5. 100-A
6. 2023-100
7. 2024-005

> ⚠️ **Misconception:** "Numbers always come before letters because 0-9 comes before A-Z on a keyboard or in ASCII."
>
> **Why it fails:** While computers may sort digits before letters by default (ASCII order), standard filing systems used in government offices place alphabetic entries before numeric entries. The CSE follows filing conventions, not computer sorting conventions. A clerk looking for "ACCT-1001" would check the alphabetic section first, then the numeric section — this matches how physical filing cabinets are organized.
>
> **Correct model:** In standard filing systems (and on the CSE), letters come before numbers. Entries starting with A-Z file before entries starting with 0-9. Within the alphabetic section, sort alphabetically. Within the numeric section, sort numerically.

#### Handling Entries with Embedded Numbers

Some codes have numbers embedded within alphabetic text (like "R3" or "FORM12"). Compare the alphabetic portion first, then the numeric portion:

| Entry | Alpha Portion | Numeric Portion | Filing Position |
|-------|--------------|-----------------|-----------------|
| FORM1 | FORM | 1 | First (FORM, then 1) |
| FORM2 | FORM | 2 | Second (FORM, then 2) |
| FORM10 | FORM | 10 | Third (FORM, then 10) |
| FORMA | FORM | A | Compare as FORMA — pure alpha |

**Rule for embedded numbers:** When the same alphabetic prefix is followed by a number, compare the numbers numerically. FORM1 < FORM2 < FORM10 (not FORM1 < FORM10 < FORM2, which would be string order).

### Check Your Understanding

**1.** Which comes first in ascending order: 2024-015 or 2024-003? → **2024-003** (003 = 3, which is less than 015 = 15)

**2.** Which comes first: PS-9 or PS-85? → **PS-9** (same prefix; compare numbers: 9 < 85)

**3.** Which comes first: ACCT-100 or 200-B? → **ACCT-100** (letters before numbers in mixed filing)

**4.** In descending order, which comes first: CO-50 or CO-200? → **CO-200** (descending = largest first; 200 > 50)

**5.** Which comes first: DTN-2023-0100 or DTN-2024-0003? → **DTN-2023-0100** (same prefix; compare years: 2023 < 2024)

### Exam Strategies

- Read the question carefully for direction words: "ascending," "descending," "smallest to largest," or "largest to smallest."
- If no direction is specified, default to ascending order (smallest first).
- For code numbers with prefixes, sort by prefix FIRST — do not jump to comparing numbers across different prefixes.
- When comparing numeric portions of code numbers, always compare as whole numbers, not digit by digit.
- For hyphenated codes, mentally separate at each hyphen and compare segment by segment, left to right.
- Use elimination: identify the entry that clearly comes first or last, then narrow down the middle positions.
- Watch for the letters-before-numbers rule in mixed filing — it is a common trap when entries mix formats.
- Double-check your work on the first and last positions — these are where most errors occur.
- If two entries share a long prefix (like DTN-2024-), skip to the first segment that differs to save time.
- For uniform-length codes (like 001, 002, 099), digit-by-digit comparison is safe and fast.

### Memory Aids

#### The SNAP Method for Numerical Filing

**S** — Segment the code at each hyphen
**N** — Note whether each segment is alphabetic or numeric
**A** — Alphabetic segments compare alphabetically; numeric segments compare as whole numbers
**P** — Proceed left to right, segment by segment

#### Ascending vs. Descending Quick Check

Think of a staircase:
- **Ascending** = climbing UP the stairs: 1, 2, 3, 4, 5 (small → large)
- **Descending** = going DOWN the stairs: 5, 4, 3, 2, 1 (large → small)

#### The "Phone Book" Rule for Mixed Filing

Imagine a phone book: named entries (alphabetic) come in the main section; numbered entries come in a separate section at the back. **Letters first, numbers second.**

#### Prefix Priority Reminder

"**Category before Count**" — The prefix (category) always determines position first. Only compare counts (numbers) when categories match.

- CO before MOOE before PS (alphabetical categories)
- Within CO: CO-1 before CO-2 before CO-100 (numerical count)

### Guided Practice

#### Problem 1 (Full scaffolding)

Arrange in ascending filing order:
- PS-205
- CO-42
- MOOE-1003
- PS-15
- CO-301

**Step 1:** Identify the type of code.
These are budget codes with alphabetic prefixes and numeric portions. Rule: compare prefix alphabetically first, then numeric portion as a whole number.

**Step 2:** Group by prefix.
- CO: CO-42, CO-301
- MOOE: MOOE-1003
- PS: PS-205, PS-15

**Step 3:** Within each prefix group, arrange numeric portions in ascending order.
- CO group: 42 < 301 → CO-42, CO-301
- MOOE group: only one entry → MOOE-1003
- PS group: 15 < 205 → PS-15, PS-205

**Step 4:** Combine groups in alphabetical prefix order (C before M before P).

**Answer:**
1. CO-42
2. CO-301
3. MOOE-1003
4. PS-15
5. PS-205

#### Problem 2 (Moderate scaffolding)

Arrange in ascending filing order:
- DTN-2024-0012
- DTN-2023-0050
- DTN-2024-0003
- DTN-2023-0008
- DTN-2024-0100

**Step 1:** All share prefix "DTN" — move to Segment 2 (year).
- 2023 entries: DTN-2023-0050, DTN-2023-0008
- 2024 entries: DTN-2024-0012, DTN-2024-0003, DTN-2024-0100

**Step 2:** Within each year group, compare Segment 3 (sequence) _____.
- 2023 group: _____ < _____ → order: _____
- 2024 group: _____ < _____ < _____ → order: _____

**Step 3:** Combine (2023 before 2024).

**Answer:**
1. DTN-2023-0008
2. DTN-2023-0050
3. DTN-2024-0003
4. DTN-2024-0012
5. DTN-2024-0100

#### Problem 3 (Reduced scaffolding)

Arrange in ascending filing order:
- CSC-NCR-015
- COA-R3-045
- CSC-R4-012
- COA-NCR-003
- CSC-NCR-001

**Step 1:** Compare Segment 1 (agency): _____ comes before _____

**Step 2:** Within each agency group, compare Segment 2 (region): _____

**Step 3:** Within matching regions, compare Segment 3: _____

**Answer:**
1. COA-NCR-003
2. COA-R3-045
3. CSC-NCR-001
4. CSC-NCR-015
5. CSC-R4-012

#### Problem 4 (Minimal scaffolding)

Arrange in descending numeric order (prefixes still alphabetical):
- MOOE-50
- PS-200
- CO-175
- MOOE-300
- PS-10
- CO-80

Group by prefix, then arrange numbers from _____ to _____.

**Answer:**
1. CO-175
2. CO-80
3. MOOE-300
4. MOOE-50
5. PS-200
6. PS-10

#### Problem 5 (No scaffolding)

Arrange in ascending filing order:
- 2024-100
- ACCT-505
- PS-33
- 2023-200
- MOOE-12
- 150-B

**Answer:**
1. ACCT-505
2. MOOE-12
3. PS-33
4. 150-B
5. 2023-200
6. 2024-100

### Which Method?

Determine which filing rule applies to each entry or set.

#### 1.

Entries: PS-101, PS-8, PS-55

Rule: **Same prefix — compare numeric portions as whole numbers** → PS-8, PS-55, PS-101

#### 2.

Entries: 2024-003, 2024-015, 2024-001

Rule: **Same-length uniform codes — compare digit by digit (or numerically, same result)** → 2024-001, 2024-003, 2024-015

#### 3.

Entries: ACCT-100, 500-C, BUD-25

Rule: **Mixed alphanumeric — letters before numbers; then alphabetical prefixes, then numeric** → ACCT-100, BUD-25, 500-C

#### 4.

Entries: DTN-2023-0100, DTN-2024-0005, DTN-2023-0050

Rule: **Hyphenated codes — segment by segment (prefix, then year, then sequence)** → DTN-2023-0050, DTN-2023-0100, DTN-2024-0005

#### 5.

Question says: "Arrange from largest to smallest"
Entries: CO-50, CO-200, CO-15

Rule: **Descending order — largest numeric value first within same prefix** → CO-200, CO-50, CO-15

#### 6.

Entries: CSC-NCR-001, CSC-R4-012, COA-R3-045

Rule: **Multi-segment agency codes — compare segment by segment left to right** → COA-R3-045, CSC-NCR-001, CSC-R4-012

### Before You Practice

- [ ] I can compare pure account numbers digit by digit from left to right.
- [ ] I understand the shorter-number-first rule for numbers with identical leading digits.
- [ ] I can file code numbers by comparing the alphabetic prefix first, then the numeric portion as a whole number.
- [ ] I know the difference between ascending order (smallest first) and descending order (largest first).
- [ ] I can break hyphenated codes into segments and compare each segment independently.
- [ ] I can apply the letters-before-numbers rule in mixed alphanumeric filing.

### Mini Practice Set

Arrange each group in correct ascending filing order unless otherwise specified.

#### 1.

- 2024-005
- 2024-001
- 2024-012

Answer:
1. 2024-001
2. 2024-005
3. 2024-012

#### 2.

- PS-120
- PS-15
- PS-8

Answer:
1. PS-8
2. PS-15
3. PS-120

#### 3.

- ACCT-2045
- ACCT-999
- ACCT-1001

Answer:
1. ACCT-999
2. ACCT-1001
3. ACCT-2045

#### 4.

- CO-301
- MOOE-205
- PS-101

Answer:
1. CO-301
2. MOOE-205
3. PS-101

#### 5.

Arrange in DESCENDING order:
- 2024-050
- 2024-003
- 2024-100

Answer:
1. 2024-100
2. 2024-050
3. 2024-003

#### 6.

- DTN-2023-0100
- DTN-2023-0008
- DTN-2024-0001

Answer:
1. DTN-2023-0008
2. DTN-2023-0100
3. DTN-2024-0001

#### 7.

- CSC-NCR-015
- CSC-NCR-001
- CSC-R4-012

Answer:
1. CSC-NCR-001
2. CSC-NCR-015
3. CSC-R4-012

#### 8.

- COA-R3-045
- COA-NCR-003
- COA-R1-100

Answer:
1. COA-NCR-003
2. COA-R1-100
3. COA-R3-045

#### 9.

- MOOE-50
- CO-999
- PS-1

Answer:
1. CO-999
2. MOOE-50
3. PS-1

#### 10.

- ACCT-88
- 500-C
- PS-101

Answer:
1. ACCT-88
2. PS-101
3. 500-C

#### 11.

Arrange in DESCENDING order:
- PS-200
- PS-33
- PS-1005

Answer:
1. PS-1005
2. PS-200
3. PS-33

#### 12.

- DTN-2024-0003
- DTN-2024-0100
- DTN-2023-0500
- DTN-2024-0015

Answer:
1. DTN-2023-0500
2. DTN-2024-0003
3. DTN-2024-0015
4. DTN-2024-0100

#### 13.

- 2024-001
- ACCT-1001
- 2023-100
- CO-301

Answer:
1. ACCT-1001
2. CO-301
3. 2023-100
4. 2024-001

#### 14.

- CSC-NCR-100
- COA-NCR-001
- CSC-NCR-005
- COA-R3-050

Answer:
1. COA-NCR-001
2. COA-R3-050
3. CSC-NCR-005
4. CSC-NCR-100

#### 15.

Arrange in DESCENDING order:
- CO-80
- CO-175
- MOOE-300
- MOOE-50
- PS-10
- PS-200

Answer:
1. CO-175
2. CO-80
3. MOOE-300
4. MOOE-50
5. PS-200
6. PS-10

#### 16.

- ACCT-5
- ACCT-50
- ACCT-500
- ACCT-5000

Answer:
1. ACCT-5
2. ACCT-50
3. ACCT-500
4. ACCT-5000

#### 17.

- DTN-2024-0001
- CSC-NCR-001
- 2024-001
- PS-101
- MOOE-205

Answer:
1. CSC-NCR-001
2. DTN-2024-0001
3. MOOE-205
4. PS-101
5. 2024-001

#### 18.

- COA-R3-001
- COA-R1-050
- COA-R10-003
- COA-R2-100

Answer:
1. COA-R1-050
2. COA-R10-003
3. COA-R2-100
4. COA-R3-001

### Connections

- Numerical filing builds on the digit-by-digit comparison skill used in alphabetical filing — the same left-to-right scanning applies, but with digits instead of letters.
- The prefix-first rule for code numbers mirrors the distinctive-word-first rule in government office filing — both identify the primary category before comparing secondary details.
- Ascending and descending order concepts transfer directly to data arrangement questions in the Numerical Ability section of the CSE.
- Segment-by-segment comparison of hyphenated codes uses the same hierarchical logic as filing personal names with particles (Dela Cruz → compare "Dela" first, then "Cruz").
- The letters-before-numbers convention in mixed filing connects to how government forms organize sections — alphabetic codes (Form A, Form B) precede numbered appendices.

### Mastery Checklist

- ✅ I can file pure account numbers by comparing digits left to right.
- ✅ I apply the shorter-number-first rule when leading digits match.
- ✅ I understand that leading zeros do not change a number's filing position.
- ✅ I can file code numbers by prefix first, then numeric portion as a whole number.
- ✅ I know the difference between digit-by-digit comparison and numeric comparison.
- ✅ I can arrange entries in both ascending and descending order.
- ✅ I default to ascending order when no direction is specified.
- ✅ I can break hyphenated codes into segments and compare each independently.
- ✅ I apply the letters-before-numbers rule in mixed alphanumeric filing.
- ✅ I can use the SNAP method to systematically file any numerical code.
- ✅ I can solve numerical filing problems accurately under time pressure.

## Worked Examples

### Worked Example 1

**Question:** Arrange in correct ascending filing order:
- PS-101
- CO-42
- MOOE-205
- PS-15
- CO-301

**Step 1:** Identify the code type.
These are budget codes with alphabetic prefixes (CO, MOOE, PS) and numeric portions. Rule: compare prefix alphabetically first, then numeric portion as a whole number.

**Step 2:** Group by prefix.
- CO: CO-42, CO-301
- MOOE: MOOE-205
- PS: PS-101, PS-15

**Step 3:** Arrange numeric portions within each group (ascending).
- CO: 42 < 301 → CO-42, CO-301
- MOOE: only one entry
- PS: 15 < 101 → PS-15, PS-101

**Step 4:** Combine in alphabetical prefix order (C → M → P).

**Final answer:**
1. CO-42
2. CO-301
3. MOOE-205
4. PS-15
5. PS-101

### Worked Example 2

**Question:** Which comes first in ascending order: ACCT-9 or ACCT-85?

**Step 1:** Identify the code type.
Both have the prefix "ACCT" — prefixes are identical, so compare numeric portions.

**Step 2:** Compare numeric portions as whole numbers.
- ACCT-9: numeric value = 9
- ACCT-85: numeric value = 85

**Step 3:** Determine order.
9 < 85, so ACCT-9 comes first.

**Answer:** ACCT-9 comes first.

**Common error:** Comparing digit-by-digit would give 9 vs. 8 → 9 > 8 → ACCT-85 first. This is WRONG because code numbers compare their numeric portions as whole numbers, not as strings.

### Worked Example 3

**Question:** Arrange in ascending filing order:
- DTN-2024-0015
- DTN-2023-0100
- DTN-2024-0003
- DTN-2023-0045

**Step 1:** All share prefix "DTN" — compare Segment 2 (year).
- 2023 entries: DTN-2023-0100, DTN-2023-0045
- 2024 entries: DTN-2024-0015, DTN-2024-0003

2023 < 2024, so all 2023 entries come before all 2024 entries.

**Step 2:** Within 2023 group, compare Segment 3 (sequence number).
- 0045 = 45, 0100 = 100
- 45 < 100 → DTN-2023-0045 first

**Step 3:** Within 2024 group, compare Segment 3.
- 0003 = 3, 0015 = 15
- 3 < 15 → DTN-2024-0003 first

**Final answer:**
1. DTN-2023-0045
2. DTN-2023-0100
3. DTN-2024-0003
4. DTN-2024-0015

### Worked Example 4

**Question:** Arrange in ascending filing order:
- 2024-050
- ACCT-300
- PS-12
- 2023-100
- MOOE-75

**Step 1:** Identify entry types — this is a mixed alphanumeric filing problem.
- Letter-starting: ACCT-300, PS-12, MOOE-75
- Number-starting: 2024-050, 2023-100

**Step 2:** Apply letters-before-numbers rule. All letter-starting entries come first.

**Step 3:** Arrange letter-starting entries by prefix alphabetically:
- ACCT-300 (A)
- MOOE-75 (M)
- PS-12 (P)

**Step 4:** Arrange number-starting entries by first numeric segment:
- 2023-100 (2023)
- 2024-050 (2024)

**Step 5:** Combine: letters first, then numbers.

**Final answer:**
1. ACCT-300
2. MOOE-75
3. PS-12
4. 2023-100
5. 2024-050

### Worked Example 5

**Question:** Arrange in DESCENDING order within each prefix group:
- CO-80
- PS-200
- CO-175
- PS-10
- MOOE-50
- MOOE-300

**Step 1:** Group by prefix (alphabetical order for prefixes remains ascending).
- CO: CO-80, CO-175
- MOOE: MOOE-50, MOOE-300
- PS: PS-200, PS-10

**Step 2:** Within each group, arrange numeric portions in DESCENDING order (largest first).
- CO: 175 > 80 → CO-175, CO-80
- MOOE: 300 > 50 → MOOE-300, MOOE-50
- PS: 200 > 10 → PS-200, PS-10

**Step 3:** Combine groups (prefixes in alphabetical order).

**Final answer:**
1. CO-175
2. CO-80
3. MOOE-300
4. MOOE-50
5. PS-200
6. PS-10

**Key insight:** "Descending order" reverses only the numeric comparison within each prefix group. The prefix groups themselves remain in standard alphabetical order (CO before MOOE before PS) because the question asks for descending *numeric* order, not descending alphabetical order.

## Key Takeaways

- Account numbers are compared digit by digit from left to right; the first differing digit determines order.
- When leading digits match and one number is shorter, the shorter number files first (it is numerically smaller).
- Leading zeros do not change filing position — 007 and 7 occupy the same position.
- Code numbers with alphabetic prefixes sort by prefix first (alphabetically), then by numeric portion (as a whole number).
- The critical distinction: code number numeric portions compare as whole numbers (9 < 85), NOT digit by digit (where 9 > 8 would give wrong results).
- Ascending order (smallest to largest) is the default in government filing systems and on the CSE.
- Descending order (largest to smallest) reverses only the numeric comparison; prefix order stays alphabetical.
- Hyphenated codes are compared segment by segment, left to right — each segment is an independent comparison unit.
- In mixed alphanumeric filing, letters come before numbers: all letter-starting entries file before all number-starting entries.
- Use the SNAP method: Segment, Note type, Alphabetic/numeric comparison, Proceed left to right.

## Summary

Numerical filing covers the rules for arranging records by account numbers, code numbers, and mixed alphanumeric identifiers — the primary systems used in Philippine government offices. Pure account numbers are compared digit by digit from left to right, with shorter numbers filing first when their leading digits match a longer number. This method works because our positional number system gives the leftmost digit the greatest significance, making left-to-right comparison the natural and efficient approach.

Code numbers with alphabetic prefixes (like PS-101, MOOE-205, CO-301) require a two-level sort: the prefix determines the primary filing position alphabetically, and the numeric portion determines position within the prefix group. The critical rule is that numeric portions are compared as whole numbers — not digit by digit — because the number represents a sequential quantity. This means PS-9 correctly files before PS-85, even though a digit-by-digit comparison would incorrectly reverse them.

Hyphenated codes like DTN-2024-0001 are broken into segments at each hyphen, with each segment compared independently in left-to-right order. This creates a hierarchical sort that mirrors how physical filing systems organize records — by category, then subcategory, then specific item. In mixed alphanumeric filing, the convention is letters before numbers: entries starting with alphabetic characters file before entries starting with digits. Mastering these rules requires understanding not just the procedures but the principles behind them — positional value, hierarchical categorization, and the distinction between string comparison and numeric comparison.
