# Master Prompt - Lesson Parser and Lesson Proper Generation

You are a senior software architect and frontend engineer.

Your task is to redesign the lesson parsing system into a modern, block-based rendering engine.

The current parser is heading-driven. That architecture should be replaced with a semantic document model where content, structure, and presentation are separated.

---

# Overall Philosophy

Markdown is the source of truth.

It should never contain styling instructions or presentation logic.

The parser should convert Markdown into an internal Abstract Syntax Tree (AST).

The renderer should consume the AST and build the UI using reusable components.

Authors should only write lessons.

Developers should only build components.

The renderer decides how content is displayed.

---

# High-Level Architecture

Markdown -> Lexer -> Parser -> Semantic AST -> Validation -> Lesson Model -> Renderer -> Interactive Lesson

The renderer must never inspect raw Markdown.

It only receives structured nodes.

---

# Lesson Structure

Every lesson follows this hierarchy.

Lesson
- Title
- Explanations
  - Introduction
  - Why Topic Is Tested
  - Common Mistakes
  - Learning Objectives
- MicroConcepts
- Worked Examples
- Key Takeaways
- Summary
- Final Challenge

This hierarchy is semantic.

It must not depend on heading numbers such as 4.1 or 4.2.

Do not add separate Exam Strategies, Memory Aids, or Practice & Review sections.

If a lesson needs practice, put it in Final Challenge or the quiz proper.

---

# Supported Sections

The parser should recognize these major sections.

## Explanations

Contains:

- Introduction
- Why Topic Is Tested
- Common Mistakes
- Learning Objectives

---

## Micro Concept

Every repeated `## Some Concept` after Explanations is considered one MicroConcept.

Each MicroConcept contains:

- Overview
- Core Principle
- Visualization
- Common Mistakes
- Worked Mini Example
- Key Insight
- Quick Check

The parser should automatically recognize these subsections.

Quick Check is the final MicroConcept subsection and must become its own screen.
It is not a static reveal card.

Write Quick Check as exactly 3 interactive multiple-choice questions.
Each question must have exactly 3 choices, with one unambiguous correct answer.

Use this format:

Question: What is the best answer?
Choices:
- First choice
- Second choice
- Third choice
Answer: Second choice
Rationale: Short explanation of why the answer is correct.

Keep the questions short, concrete, and directly tied to the concept.
Prefer one idea per question.

Do not require numbering.

The renderer can display Concept 1, Concept 2, Concept 3, or nothing.

Presentation is separate.

---

## Worked Examples

Contains:

- Example 1
- Example 2
- Example 3
- Unlimited examples

---

## Key Takeaways

Simple bullet list.

---

## Summary

Normal rich text.

---

## Final Challenge

Contains the quiz proper and wrap-up material:

- Mixed Practice Set
- Self Assessment
- What's Next?

---

# Parsing Rules

The parser should identify sections semantically.

Example:

`## Worked Examples`

creates a `WorkedExamplesNode`, not just a generic heading node.

Likewise:

`### Overview`

inside a MicroConcept becomes an `OverviewNode`, not merely a heading.

Unknown headings should become GenericSection nodes instead of causing failures.

The parser should fail gracefully.

---

# Block System

Every paragraph becomes a block.

Supported block types include:

- Paragraph
- Bullet List
- Ordered List
- Checklist
- Table
- Quote
- Warning
- Tip
- Note
- Code
- Inline Code
- Formula
- SVG
- Mermaid
- Image
- Video
- Divider
- Callout
- Definition
- Question
- Answer
- Diagram
- Interactive Exercise
- Embedded Quiz

Each block has:

- type
- children
- metadata
- content

---

# Automatic Numbering

Markdown must never require numbering like 4.1, 4.2, 4.3.

Instead, use semantic headings such as:

## Rotation
## Reflection
## Grid Reasoning

The renderer automatically determines concept numbering if desired.

---

# Renderer Responsibilities

The renderer decides:

- numbering
- spacing
- colors
- typography
- animations
- transitions
- responsiveness
- collapsible sections
- progress indicators
- cards
- tabs
- swipe navigation

Markdown should contain none of these.

---

# Screen-Based Rendering

The app should render one learning unit at a time.

A screen should represent one learning objective or one compact semantic chunk.

For example:

Overview -> Screen
Core Principle -> Screen
Visualization -> Screen
Worked Mini Example -> Screen
Key Insight -> Screen
Quick Check -> Dedicated screen

Final Challenge is the practice and wrap-up stage, so do not add a separate Practice & Review block.

Large paragraphs should automatically paginate when necessary.

---

# Progress Engine

Every screen reports:

- lesson progress
- current concept
- current screen
- completion
- estimated time
- mastery
- quiz score

---

# Interactive Components

The parser should recognize:

- SVG
- Mermaid
- Markdown Tables
- Code Blocks
- Math
- Callouts
- Images
- Videos
- Quizzes

without requiring custom HTML.

---

# Validation Rules

Ensure:

- Lesson contains exactly one title.
- Explanations appear first.
- MicroConcepts appear before Worked Examples.
- Worked Examples appear before Key Takeaways, Summary, and Final Challenge.
- Required subsections exist.
- Warn about missing sections.
- Never crash because one section is absent.

---

# Extensibility

New section types should be registerable.

Example:

- Flashcards
- Timeline
- Simulation
- Lab
- Coding Exercise
- Interactive Canvas

These should require only adding a registry entry.

No parser rewrite.

---

# Clean Architecture

Never hardcode `if heading == "Overview"` throughout the parser.

Use a registry.

Example:

- SectionRegistry
- MicroConceptRegistry
- BlockRegistry
- RendererRegistry

Everything should be data-driven.

---

# Performance

The parser should:

- parse incrementally
- cache ASTs
- support lazy rendering
- render only the visible screen
- support virtual scrolling for long lessons
- avoid reparsing unchanged content

---

# Future Features

Design the architecture so future features require minimal changes.

Examples:

- AI-generated hints
- AI explanations
- AI summaries
- Flashcards
- Spaced repetition
- Achievement badges
- Adaptive quizzes
- Gamification
- Progress synchronization
- Collaborative annotations
- Instructor comments
- Version history
- Offline lessons

These should plug into the AST rather than modifying Markdown.

---

# Code Quality Requirements

The implementation should be:

- modular
- strongly typed
- fully documented
- testable
- extensible
- maintainable
- framework-agnostic where possible

Avoid giant switch statements.

Prefer registries, factories, visitors, and component composition.

The parser should be easy to extend without touching existing code.

---

# Final Goal

The finished system should behave less like a Markdown renderer and more like a lesson engine.

Markdown becomes structured lesson data.

The parser transforms that data into a semantic AST.

The renderer transforms the AST into interactive learning experiences.

The architecture should be scalable enough to power thousands of lessons across multiple subjects while remaining easy for content authors to write using plain Markdown.
