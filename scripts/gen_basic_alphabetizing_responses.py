"""Generate chat response variations for basic-alphabetizing lesson.

Produces data/chat_responses/clerical-ability/alphabetical-filing/basic-alphabetizing/responses.json
following the prompt template at prompts/chat-responses-clerical-ability.md.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "chat_responses" / "clerical-ability" / "alphabetical-filing" / "basic-alphabetizing"

SUBTOPIC_ID = "basic-alphabetizing"
SUBTOPIC_TITLE = "Basic Alphabetizing"

