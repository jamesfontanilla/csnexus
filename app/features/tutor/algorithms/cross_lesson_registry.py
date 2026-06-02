"""Cross-Lesson Registry for concept-based cross-referencing.

Builds a lookup structure that maps key concepts to the subtopics where
they are taught, enabling the engine to reference related lessons in
responses. The registry is built once at application startup from all
lesson content_json records.

Concepts are extracted from:
- key_takeaways field → normalized to 1–5 word phrases
- sections[*].title → each section heading as a concept
- metadata.prerequisites → prerequisite subtopic IDs as relationships

Cross-reference text generation:
- When mastery data exists for a related subtopic → note the connection
- When no mastery data exists → mention as a future learning opportunity
- At most 2 cross-references per response, each ≤ 150 characters and single sentence
- Supports comparison responses when user asks how topics relate

Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.features.tutor.algorithms.chat_models import ConceptEntry


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MAX_CROSS_REFS = 2
_MAX_CROSS_REF_CHARS = 150


class CrossLessonRegistry:
    """Maps key concepts to their source subtopics for cross-referencing.

    Built once at startup by iterating all lesson content_json records.
    Provides lookup by term matching and by subtopic ID.
    """

    def __init__(self) -> None:
        self._concepts: dict[str, list[ConceptEntry]] = {}

    @classmethod
    def build_from_lessons(cls, lessons: list[dict]) -> CrossLessonRegistry:
        """Build a registry from a list of lesson content_json dicts.

        Each lesson dict is expected to have:
        - subtopic_id: int
        - subtopic_title: str
        - key_takeaways: list[str] (optional)
        - sections: list[dict] with 'title' key (optional)
        - metadata: dict with 'prerequisites' list (optional)
        """
        registry = cls()

        for lesson in lessons:
            subtopic_id = lesson.get("subtopic_id")
            subtopic_title = lesson.get("subtopic_title", "")

            if subtopic_id is None:
                continue

            # Extract from key_takeaways
            key_takeaways = lesson.get("key_takeaways", [])
            if isinstance(key_takeaways, list):
                for takeaway in key_takeaways:
                    if not isinstance(takeaway, str):
                        continue
                    normalized = _normalize_phrase(takeaway)
                    if normalized and 1 <= len(normalized.split()) <= 5:
                        entry = ConceptEntry(
                            term=normalized,
                            subtopic_id=subtopic_id,
                            subtopic_title=subtopic_title,
                            source="key_takeaway",
                        )
                        registry._add_entry(normalized, entry)

            # Extract from section headings
            sections = lesson.get("sections", [])
            if isinstance(sections, list):
                for section in sections:
                    if not isinstance(section, dict):
                        continue
                    title = section.get("title", "")
                    if not isinstance(title, str):
                        continue
                    normalized = _normalize_phrase(title)
                    if normalized and 1 <= len(normalized.split()) <= 5:
                        entry = ConceptEntry(
                            term=normalized,
                            subtopic_id=subtopic_id,
                            subtopic_title=subtopic_title,
                            source="section_heading",
                        )
                        registry._add_entry(normalized, entry)

            # Extract from prerequisites
            metadata = lesson.get("metadata", {})
            if isinstance(metadata, dict):
                prerequisites = metadata.get("prerequisites", [])
                if isinstance(prerequisites, list):
                    for prereq in prerequisites:
                        if isinstance(prereq, dict):
                            prereq_id = prereq.get("subtopic_id")
                            prereq_title = prereq.get("subtopic_title", "")
                            prereq_term = _normalize_phrase(prereq_title)
                            if prereq_term and prereq_id is not None:
                                entry = ConceptEntry(
                                    term=prereq_term,
                                    subtopic_id=subtopic_id,
                                    subtopic_title=subtopic_title,
                                    source="prerequisite",
                                )
                                registry._add_entry(prereq_term, entry)

        return registry

    def _add_entry(self, term: str, entry: ConceptEntry) -> None:
        """Add a concept entry to the registry under the given term."""
        if term not in self._concepts:
            self._concepts[term] = []
        self._concepts[term].append(entry)

    def find_related(
        self, terms: list[str], current_subtopic_id: int
    ) -> list[ConceptEntry]:
        """Find concepts from other subtopics that match provided terms.

        Returns at most 2 entries from subtopics different from the current one.
        Also performs partial matching: if a search term appears as a substring
        of a registered term (or vice versa), it counts as a match. This enables
        matching "prerequisite relationships" against registered terms like
        "prerequisites" or "relationships".
        """
        results: list[ConceptEntry] = []
        seen_subtopics: set[int] = set()

        for term in terms:
            normalized = _normalize_phrase(term)
            if not normalized:
                continue

            # Exact match first
            entries = self._concepts.get(normalized, [])
            for entry in entries:
                if entry.subtopic_id == current_subtopic_id:
                    continue
                if entry.subtopic_id in seen_subtopics:
                    continue
                results.append(entry)
                seen_subtopics.add(entry.subtopic_id)
                if len(results) >= _MAX_CROSS_REFS:
                    return results

            # Partial match: check if normalized term is a substring of any
            # registered term, or any registered term is a substring of the
            # normalized search term.
            if len(results) < _MAX_CROSS_REFS:
                for reg_term, reg_entries in self._concepts.items():
                    if reg_term == normalized:
                        continue  # Already handled above
                    if normalized in reg_term or reg_term in normalized:
                        for entry in reg_entries:
                            if entry.subtopic_id == current_subtopic_id:
                                continue
                            if entry.subtopic_id in seen_subtopics:
                                continue
                            results.append(entry)
                            seen_subtopics.add(entry.subtopic_id)
                            if len(results) >= _MAX_CROSS_REFS:
                                return results

        return results

    def find_by_subtopic(self, subtopic_id: int) -> list[ConceptEntry]:
        """Return all concept entries for a given subtopic ID."""
        results: list[ConceptEntry] = []
        for entries in self._concepts.values():
            for entry in entries:
                if entry.subtopic_id == subtopic_id:
                    results.append(entry)
        return results

    def lookup(self, term: str) -> list[ConceptEntry]:
        """Look up all entries for a normalized term."""
        normalized = _normalize_phrase(term)
        return self._concepts.get(normalized, [])

    @property
    def all_terms(self) -> list[str]:
        """Return all registered terms."""
        return list(self._concepts.keys())

    def __len__(self) -> int:
        """Return total number of unique terms in the registry."""
        return len(self._concepts)

    # ------------------------------------------------------------------
    # Cross-reference text generation (Req 4.3, 4.4, 4.5, 4.6)
    # ------------------------------------------------------------------

    def format_cross_reference(
        self,
        entry: ConceptEntry,
        has_mastery: bool,
    ) -> str:
        """Generate a single cross-reference sentence for a related concept.

        Behavior differs based on mastery data availability:
        - has_mastery=True → notes the connection to the studied topic
        - has_mastery=False → mentions as a future learning opportunity

        The returned text is always a single sentence and at most 150 characters.
        """
        if has_mastery:
            text = (
                f"This connects to {entry.term} in {entry.subtopic_title} "
                f"which you've studied."
            )
        else:
            text = (
                f"You'll explore {entry.term} further in "
                f"{entry.subtopic_title}."
            )

        # Enforce the 150-character constraint
        if len(text) > _MAX_CROSS_REF_CHARS:
            # Truncate and close with a period to maintain single-sentence form
            text = text[: _MAX_CROSS_REF_CHARS - 1].rstrip() + "."

        return text

    def format_cross_references(
        self,
        entries: list[ConceptEntry],
        mastery_subtopic_ids: set[int] | None = None,
    ) -> str:
        """Format up to 2 cross-reference entries into response text.

        Each reference is a single sentence of at most 150 characters.
        Mastery-aware: uses mastery_subtopic_ids to differentiate messaging.

        Args:
            entries: ConceptEntry items from find_related().
            mastery_subtopic_ids: Set of subtopic IDs where the user has
                mastery data. If None, all are treated as having mastery.

        Returns:
            Combined cross-reference text, or empty string if no entries.
        """
        if not entries:
            return ""

        if mastery_subtopic_ids is None:
            mastery_subtopic_ids = set()

        parts: list[str] = []
        for entry in entries[:_MAX_CROSS_REFS]:
            has_mastery = entry.subtopic_id in mastery_subtopic_ids
            ref_text = self.format_cross_reference(entry, has_mastery)
            parts.append(ref_text)

        return " ".join(parts)

    def generate_comparison(
        self,
        current_subtopic_id: int,
        other_subtopic_id: int,
    ) -> ComparisonResult:
        """Generate a comparison between two subtopics.

        Produces at least 1 shared principle and at least 1 difference,
        each expressed in at most 2 sentences.

        Used when the user explicitly asks how topics relate (Req 4.5).

        Returns a ComparisonResult with shared principles and differences.
        """
        current_entries = self.find_by_subtopic(current_subtopic_id)
        other_entries = self.find_by_subtopic(other_subtopic_id)

        current_terms = {e.term for e in current_entries}
        other_terms = {e.term for e in other_entries}

        # Shared principles: terms that appear in both subtopics
        shared_terms = current_terms & other_terms

        # Differences: terms unique to each subtopic
        current_only = current_terms - other_terms
        other_only = other_terms - current_terms

        # Build the current and other titles for readable output
        current_title = (
            current_entries[0].subtopic_title if current_entries else "this topic"
        )
        other_title = (
            other_entries[0].subtopic_title if other_entries else "that topic"
        )

        # Generate shared principles (at least 1)
        shared: list[str] = []
        for term in list(shared_terms)[:2]:
            shared.append(
                f"Both {current_title} and {other_title} involve {term}."
            )
        if not shared:
            # Fallback: they're in the same knowledge domain
            shared.append(
                f"Both {current_title} and {other_title} build foundational skills."
            )

        # Generate differences (at least 1)
        differences: list[str] = []
        if current_only:
            unique_term = next(iter(current_only))
            differences.append(
                f"{current_title} focuses on {unique_term}, "
                f"while {other_title} does not cover this directly."
            )
        if other_only and len(differences) < 2:
            unique_term = next(iter(other_only))
            differences.append(
                f"{other_title} emphasizes {unique_term}, "
                f"which is not a primary focus of {current_title}."
            )
        if not differences:
            differences.append(
                f"{current_title} and {other_title} approach the subject "
                f"from different angles."
            )

        return ComparisonResult(
            current_title=current_title,
            other_title=other_title,
            shared_principles=shared,
            differences=differences,
        )


@dataclass
class ComparisonResult:
    """Result of comparing two subtopics for cross-reference responses.

    Contains at least 1 shared principle and at least 1 difference,
    each expressed in at most 2 sentences (Req 4.5).
    """

    current_title: str
    other_title: str
    shared_principles: list[str] = field(default_factory=list)
    differences: list[str] = field(default_factory=list)

    def format_response(self) -> str:
        """Format the comparison into a response string.

        Each point is at most 2 sentences.
        """
        parts: list[str] = []

        for principle in self.shared_principles:
            parts.append(principle)

        for difference in self.differences:
            parts.append(difference)

        return " ".join(parts)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_phrase(phrase: str) -> str:
    """Normalize a phrase to lowercase, stripped, with single spaces."""
    if not phrase:
        return ""
    # Lowercase and strip
    result = phrase.lower().strip()
    # Replace non-alphanumeric (except spaces) with spaces
    result = re.sub(r"[^a-z0-9 ]", " ", result)
    # Collapse multiple spaces
    result = re.sub(r"\s+", " ", result).strip()
    return result
