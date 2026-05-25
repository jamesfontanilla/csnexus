# Requirements Document

## Introduction

This feature enhances all existing lesson files in the CSE reviewer app by adding research-backed pedagogical elements that improve learning outcomes. The enhancements are grounded in cognitive psychology research: retrieval practice (Roediger & Karpicke, 2006), worked example fading (Renkl et al., 2002), interleaving (Rohrer et al., 2015), elaborative interrogation (Dunlosky et al., 2013), dual coding (Mayer, 2021; Paivio, 1986), metacognitive calibration (Bjork & Bjork, 2020), refutation texts (Tippett, 2010), and transfer bridging (Gick & Holyoak, 1983).

The scope covers all ~60 lesson files across three modules (Numerical Ability, Verbal Ability, Analytical Ability). Each lesson will be augmented with new pedagogical sections while preserving existing content and maintaining parser compatibility.

## Glossary

- **Retrieval_Prompt**: A short "Check Your Understanding" block inserted between content sections containing 2-3 quick-answer questions that force active recall during reading
- **Faded_Example**: A worked example where early solution steps are provided but later steps are left blank for the learner to complete, bridging passive reading and independent practice
- **Interleaved_Discrimination**: A "Which Method?" exercise block that presents mixed problem types requiring the learner to first identify the correct approach before solving
- **Elaborative_Interrogation**: A "Why does this work?" callout that prompts the learner to generate or read an explanation of the underlying principle behind a rule or procedure
- **Misconception_Confrontation**: A refutation text block that explicitly states a common false belief, explains why it fails with a counterexample, and provides the correct mental model
- **Transfer_Bridge**: A "Connections" section that explicitly links the current topic to other topics in the curriculum, highlighting structural similarities
- **Confidence_Check**: A metacognitive self-assessment prompt before the practice set where learners rate their confidence on each sub-skill
- **Dual_Coding_Visual**: An SVG diagram, flowchart, or concept map that represents a key concept visually alongside its textual explanation
- **Lesson_File**: A markdown file at `data/seed/lessons/<module>/<topic>/<subtopic>/lesson.md`
- **Enhanced_Lesson_Template**: The standardized section ordering that all lessons must follow after enhancement
- **Parser**: The `parse_lesson_markdown()` function in `scripts/parse_lesson.py` that converts lesson markdown into structured JSON

## Requirements

### Requirement 1: Enhanced Lesson Section Structure

**User Story:** As a learner, I want lessons to follow a consistent structure that incorporates evidence-based learning techniques throughout the reading experience, so that I retain more and can self-assess my understanding before taking quizzes.

#### Acceptance Criteria

1. THE Enhanced_Lesson_Template SHALL define the following section ordering within `## Explanations`: Introduction → Learning Objectives → Content Sections (with embedded Retrieval_Prompts) → Exam Strategies → Memory Aids → Guided Practice → Which Method? → Confidence Check → Mini Practice Set → Connections → Mastery Checklist
2. WHEN a Lesson_File is enhanced, THE Lesson_File SHALL preserve all existing content sections (Introduction, Learning Objectives, numbered content subsections, Exam Strategies, Memory Aids, Mini Practice Set, Mastery Checklist) without removing or reducing their content
3. WHEN a Lesson_File is enhanced, THE Lesson_File SHALL add new pedagogical sections in the positions specified by the Enhanced_Lesson_Template
4. THE Enhanced_Lesson_Template SHALL remain compatible with the existing Parser — all new sections must be parseable as H3 subsections under `## Explanations` or as recognized special sections (practice set, memory aids, exam strategies, mastery checklist)
5. WHEN the Parser encounters a `### Check Your Understanding` subsection, THE Parser SHALL classify it as a retrieval practice block within the containing section
6. WHEN the Parser encounters a `### Guided Practice` subsection, THE Parser SHALL classify it as a practice section distinct from the Mini Practice Set
7. WHEN the Parser encounters a `### Which Method?` or `### Discrimination Practice` subsection, THE Parser SHALL classify it as an interleaved practice section
8. WHEN the Parser encounters a `### Connections` subsection, THE Parser SHALL classify it as a transfer bridge section
9. WHEN the Parser encounters a `### Before You Practice` subsection, THE Parser SHALL classify it as a metacognitive calibration section

### Requirement 2: Distributed Retrieval Prompts

**User Story:** As a learner, I want short recall questions embedded throughout the lesson (not just at the end), so that I actively retrieve information while reading and identify gaps early.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain a `### Check Your Understanding` block after every 2 to 3 content subsections (approximately every 150-250 lines of content)
2. WHEN a `### Check Your Understanding` block is inserted, THE block SHALL contain exactly 2 to 4 quick-answer questions
3. THE Check Your Understanding questions SHALL be answerable in under 10 seconds each — they test immediate recall of the preceding content, not complex problem-solving
4. EACH Check Your Understanding question SHALL follow the format: `**N.** Question text → **Answer** (brief rationale)`
5. THE Check Your Understanding questions SHALL cover the key concepts from the immediately preceding 2-3 subsections only — not material from earlier or later in the lesson
6. WHEN a lesson has fewer than 6 content subsections, THE Lesson_File SHALL contain at minimum 1 Check Your Understanding block placed at the midpoint

### Requirement 3: Elaborative Interrogation Prompts

**User Story:** As a learner, I want "why does this work?" prompts after key rules and procedures, so that I build deeper understanding rather than just memorizing steps.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain at least 3 Elaborative_Interrogation callouts distributed across the content sections
2. WHEN an Elaborative_Interrogation callout is inserted, THE callout SHALL use the blockquote format: `> 🤔 **Why does this work?** [explanation]`
3. THE Elaborative_Interrogation callout SHALL explain the underlying principle, not merely restate the rule
4. THE Elaborative_Interrogation callout SHALL be placed immediately after a rule, formula, or procedure is introduced — not in isolation
5. THE Elaborative_Interrogation callout SHALL be 2 to 4 sentences in length — concise enough to read in under 15 seconds
6. FOR numerical lessons, THE Elaborative_Interrogation callouts SHALL explain mathematical reasoning (e.g., why moving decimals preserves the quotient)
7. FOR verbal lessons, THE Elaborative_Interrogation callouts SHALL explain linguistic reasoning (e.g., why parallel structure aids comprehension)
8. FOR analytical lessons, THE Elaborative_Interrogation callouts SHALL explain logical reasoning (e.g., why rotation preserves chirality but reflection reverses it)

### Requirement 4: Misconception Confrontation Blocks

**User Story:** As a learner, I want common misconceptions explicitly stated and refuted with counterexamples, so that I can correct false beliefs rather than just reading the correct information.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain at least 2 Misconception_Confrontation blocks
2. WHEN a Misconception_Confrontation block is inserted, THE block SHALL use the blockquote format with warning emoji: `> ⚠️ **Misconception:** "[false belief statement]"`
3. THE Misconception_Confrontation block SHALL follow the three-part refutation structure: (a) State the misconception, (b) Provide a counterexample showing why it fails, (c) State the correct mental model
4. THE Misconception_Confrontation block SHALL be placed near the content section where the misconception is most likely to arise
5. THE Misconception_Confrontation blocks SHALL be derived from the existing "Common Mistakes Examinees Make" section — transforming the most impactful errors into full refutation texts
6. THE counterexample in each Misconception_Confrontation block SHALL use concrete numbers or specific sentences (not abstract descriptions)

### Requirement 5: Faded Worked Examples

**User Story:** As a learner, I want partially-completed worked examples that require me to fill in later steps, so that I transition gradually from reading solutions to solving independently.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain a `### Guided Practice` section positioned after the Exam Strategies section and before the Mini Practice Set
2. THE Guided Practice section SHALL contain 3 to 5 faded worked examples
3. WHEN a faded worked example is presented, THE example SHALL provide the first 1-2 solution steps completed and leave the remaining steps as blanks (using `_____` placeholder notation)
4. EACH faded worked example SHALL include the complete answer and brief solution after the blanks, separated by a blank line
5. THE fading SHALL progress within the section: the first example provides more completed steps than the last example
6. FOR numerical lessons, THE faded steps SHALL involve computation (e.g., "Step 2: Multiply: _____ × _____ = _____")
7. FOR verbal lessons, THE faded steps SHALL involve identification or classification (e.g., "Conjunction type: _____ | Relationship: _____")
8. FOR analytical lessons, THE faded steps SHALL involve pattern identification (e.g., "Rule: The shape rotates ___° ___wise each step")

### Requirement 6: Interleaved Discrimination Practice

**User Story:** As a learner, I want mixed-type problems that require me to first identify which method to use, so that I develop the discrimination skill needed on the actual exam where problem types are not grouped.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain a `### Which Method?` section positioned after the Guided Practice section and before the Confidence Check
2. THE Which Method? section SHALL contain 4 to 6 problems that mix different sub-skills taught within the same lesson
3. EACH Which Method? problem SHALL require the learner to first identify the problem type or method before solving
4. THE answer for each Which Method? problem SHALL include: (a) the identified type/method, (b) the solution, (c) a one-line rationale for why that method applies
5. THE problems SHALL be presented in random order with respect to difficulty and type — not grouped by sub-skill
6. FOR lessons that teach only one method (e.g., a single grammar rule), THE Which Method? section SHALL instead present problems that require distinguishing when the rule applies vs. when it does not

### Requirement 7: Metacognitive Confidence Check

**User Story:** As a learner, I want to rate my confidence on each sub-skill before attempting practice problems, so that I can focus my effort on weak areas and improve my self-assessment accuracy.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain a `### Before You Practice` section positioned immediately before the Mini Practice Set
2. THE Before You Practice section SHALL list 4 to 6 sub-skills covered in the lesson as checkbox items
3. EACH sub-skill item SHALL be phrased as a concrete ability statement (e.g., "Apply sign rules for integer division" not "Understand division")
4. THE section SHALL include a brief instruction: "Rate your confidence (1-5) on each skill before attempting the problems. Focus your practice on areas where you rated 3 or below."
5. THE sub-skills listed SHALL correspond to the actual content sections in the lesson — not generic or aspirational statements

### Requirement 8: Transfer Bridge Connections

**User Story:** As a learner, I want explicit connections between the current topic and other topics in the curriculum, so that I can see how skills transfer and build upon each other.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain a `### Connections` section positioned after the Mini Practice Set and before the Mastery Checklist
2. THE Connections section SHALL list 3 to 5 explicit links to other subtopics in the curriculum
3. EACH connection SHALL follow the format: `- **[Topic Name]:** [1-sentence explanation of how the current skill applies to or builds upon that topic]`
4. THE connections SHALL reference actual subtopics that exist in the `data/seed/lessons/` directory structure
5. THE connections SHALL be bidirectional where possible — if Topic A connects to Topic B, Topic B's Connections section should reference Topic A
6. FOR numerical lessons, THE connections SHALL link to other numerical topics and to word-problem applications
7. FOR verbal lessons, THE connections SHALL link to related grammar, vocabulary, and comprehension topics
8. FOR analytical lessons, THE connections SHALL link to related reasoning patterns and to numerical/verbal topics that use similar logic

### Requirement 9: Dual Coding Visual Elements

**User Story:** As a learner, I want key concepts represented visually (diagrams, flowcharts, concept maps) alongside text explanations, so that I encode information through both verbal and visual channels.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain at least 1 Dual_Coding_Visual for lessons in the Numerical Ability and Analytical Ability modules
2. THE Lesson_File SHALL contain at least 1 Dual_Coding_Visual (decision tree or flowchart) for lessons in the Verbal Ability module where a decision process exists (e.g., choosing conjunction type, identifying sentence errors)
3. WHEN a Dual_Coding_Visual is inserted, THE visual SHALL use inline SVG format compatible with the existing Parser's SVG block detection
4. THE Dual_Coding_Visual SHALL represent a concept that is also explained in text — it supplements, not replaces, the textual explanation
5. THE Dual_Coding_Visual SHALL be placed immediately after or within the text section it illustrates
6. THE SVG SHALL use a maximum width of 400px and maximum height of 300px to fit within the lesson content area
7. THE SVG SHALL use accessible colors with sufficient contrast and include text labels for all meaningful elements
8. FOR analytical lessons that already contain SVG diagrams, THE requirement is satisfied if existing diagrams adequately illustrate the key concepts

### Requirement 10: Parser Compatibility

**User Story:** As a developer, I want the enhanced lessons to remain fully compatible with the existing parse_lesson_markdown() function, so that the seed pipeline continues to work without code changes.

#### Acceptance Criteria

1. WHEN an enhanced Lesson_File is parsed by the Parser, THE Parser SHALL produce valid `LessonContent` JSON with non-empty `explanations`, `worked_examples`, `key_takeaways`, and `summary` fields
2. THE enhanced Lesson_File SHALL NOT introduce any new H2-level sections beyond those already handled by the Parser (`## Explanations`, `## Worked Examples`, `## Key Takeaways`, `## Summary`)
3. WHEN new pedagogical sections are added as H3 subsections, THE Parser SHALL include them in the `sections` array of the output JSON without errors
4. THE enhanced Lesson_File SHALL NOT break the Parser's special-section detection for: Mini Practice Set, Memory Aids, Exam Strategies, Mastery Checklist
5. WHEN the `> 🤔` or `> ⚠️` blockquote patterns are used, THE Parser SHALL classify them as `tip` or `warning` block types respectively (existing behavior)
6. THE enhanced Lesson_File SHALL maintain a minimum of 800 lines and SHALL NOT exceed 2000 lines after enhancement
7. WHEN the enhanced Lesson_File is seeded via `scripts/seed_all_content.py` or `scripts/update_lessons.py`, THE seed process SHALL complete without errors

### Requirement 11: Content Quality Standards for New Sections

**User Story:** As a learner, I want the new pedagogical sections to maintain the same quality, relevance, and Philippine CSE context as the existing content, so that the enhancements feel integrated rather than bolted on.

#### Acceptance Criteria

1. ALL new content added to Lesson_Files SHALL use Philippine government, civil service, and professional context in examples and scenarios
2. ALL new questions (in Check Your Understanding, Guided Practice, Which Method?, and Mini Practice Set) SHALL be factually correct and have unambiguous answers
3. THE Guided Practice and Which Method? sections SHALL use difficulty progression consistent with the lesson's existing Easy/Medium/Hard pattern
4. THE Misconception_Confrontation blocks SHALL address misconceptions that are genuinely common among CSE examinees — not contrived or trivial errors
5. THE Elaborative_Interrogation callouts SHALL provide accurate explanations grounded in the subject matter — not vague or hand-wavy reasoning
6. THE Transfer_Bridge connections SHALL reference real relationships between topics — not forced or superficial links
7. ALL new content SHALL be written in clear, professional English consistent with the existing lesson tone

### Requirement 12: Batch Processing and Validation

**User Story:** As a developer, I want a validation script that checks all enhanced lessons for structural compliance, so that I can verify the enhancement was applied correctly across all ~60 lessons.

#### Acceptance Criteria

1. THE validation script SHALL check each Lesson_File for the presence of all required enhanced sections: at least 1 Check Your Understanding, at least 1 Elaborative Interrogation callout, at least 2 Misconception Confrontation blocks, Guided Practice, Which Method?, Before You Practice, Connections, and Mastery Checklist
2. WHEN a Lesson_File is missing a required section, THE validation script SHALL report the missing section name and file path
3. THE validation script SHALL verify that each Lesson_File can be parsed by `parse_lesson_markdown()` without exceptions
4. THE validation script SHALL verify that the parsed output contains non-empty `explanations`, `worked_examples`, `key_takeaways`, and `summary` fields
5. THE validation script SHALL produce a summary report showing: total lessons checked, lessons passing, lessons failing, and a breakdown of failures by missing section type
6. THE validation script SHALL be located at `scripts/validate_enhanced_lessons.py` and runnable via `python scripts/validate_enhanced_lessons.py`
