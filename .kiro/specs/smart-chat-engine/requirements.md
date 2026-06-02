# Requirements Document

## Introduction

Upgrade the rule-based lesson chat engine (`lesson_chat_engine.py`) from a stateless keyword-matching system to a context-aware conversational engine. The engine remains fully rule-based (no LLM, no external API calls) but gains multi-turn conversation tracking, Socratic questioning capability, cross-lesson awareness via the existing mastery data, and adaptive response complexity based on learner proficiency. The companion `explanation_engine.py` remains separate but may be invoked by the new engine for deeper explanations.

## Glossary

- **Chat_Engine**: The rule-based module (`lesson_chat_engine.py`) that classifies user intent and generates contextual responses during lesson reading
- **Conversation_Context**: A structured representation of the current multi-turn conversation including topic thread, unresolved questions, and discourse state
- **Discourse_State**: The classification of what phase the conversation is in (e.g., initial question, follow-up, clarification, confirmation)
- **Socratic_Module**: The sub-component of the Chat_Engine that generates guiding questions instead of direct answers to promote deeper thinking
- **Cross_Lesson_Registry**: A lookup structure that maps concepts to the subtopics where they are taught, enabling the engine to reference related lessons
- **Complexity_Level**: One of three tiers (SIMPLIFIED, STANDARD, DETAILED) that controls vocabulary density, sentence length, and example depth in responses
- **Mastery_Data**: The existing `UserSubtopicMastery` records containing mastery_score, total_attempts, correct_attempts, and mastery_level per user per subtopic
- **Intent_Classifier**: The component that determines what the user is asking for based on message content, conversation history, and discourse state
- **Topic_Thread**: A sequence of related messages about the same concept within a conversation, tracked to enable coherent follow-ups
- **Anaphora_Resolver**: The sub-component that resolves pronouns and references (e.g., "it", "that", "this concept") back to their referent from conversation history

## Requirements

### Requirement 1: Multi-Turn Conversation Context Tracking

**User Story:** As a learner, I want the chatbot to remember what we've been discussing so that I can ask follow-up questions naturally without re-stating context.

#### Acceptance Criteria

1. WHEN a user sends a message, THE Chat_Engine SHALL construct a Conversation_Context from the message history that identifies the current Topic_Thread and Discourse_State
2. WHEN a user message contains a pronoun or anaphoric reference (e.g., "explain it more", "what about that"), THE Anaphora_Resolver SHALL resolve the reference to the most recent concept mentioned in the current Topic_Thread
3. WHILE a Topic_Thread is active, THE Chat_Engine SHALL use the thread's subject as implicit context for intent classification when no single intent scores above the confidence threshold from the current message alone
4. WHEN a user message shares no key terms with the current Topic_Thread subject and does not contain an anaphoric reference to the current thread, THE Chat_Engine SHALL detect a topic shift, start a new Topic_Thread, and preserve the previous thread for back-references up to a maximum of 3 preserved threads per session
5. IF the Anaphora_Resolver produces no candidate referent or all candidates score below the confidence threshold, THEN THE Chat_Engine SHALL ask a clarifying question that names the ambiguous reference and presents at most 2 candidate interpretations from the Topic_Thread history
6. THE Conversation_Context SHALL track at most 10 previous exchanges (where one exchange equals one user message paired with one assistant response) and SHALL evict the oldest exchange first when the limit is exceeded
7. WHEN the oldest exchange is evicted from the Conversation_Context, THE Chat_Engine SHALL retain the Topic_Thread subject from that exchange so that anaphora resolution and back-references remain functional for threads still within the 10-exchange window

### Requirement 2: Discourse-Aware Intent Classification

**User Story:** As a learner, I want the chatbot to understand what I mean based on the conversation flow, not just isolated keywords, so that responses feel coherent and contextual.

#### Acceptance Criteria

1. WHEN classifying intent, THE Intent_Classifier SHALL weight the Discourse_State from the Conversation_Context as a disambiguation factor, such that the same message text may yield different intents depending on the current Discourse_State
2. WHEN the previous assistant response was a quiz question and the user sends a message of 30 characters or fewer, THE Intent_Classifier SHALL classify it as a quiz answer attempt rather than a new question
3. WHEN the previous assistant response was an explanation and the user sends a single-sentence message that is a follow-up inquiry (e.g., "why?", "how come?", "why is that?", "what do you mean?"), THE Intent_Classifier SHALL classify it as a request for deeper explanation of the same topic rather than a generic question
4. WHEN the user sends a message that matches multiple intents with equal confidence, THE Intent_Classifier SHALL select the intent that continues the current Topic_Thread over an intent that would start a new thread
5. IF the Intent_Classifier confidence is below 0.4 for all candidate intents, THEN THE Chat_Engine SHALL ask a disambiguation question presenting the top two candidate intents as options for the learner to select
6. IF the Intent_Classifier confidence is below 0.4 for all candidate intents and fewer than two candidate intents exist, THEN THE Chat_Engine SHALL ask an open-ended clarifying question requesting the learner to rephrase

### Requirement 3: Socratic Questioning Mode

**User Story:** As a learner, I want the chatbot to guide me toward answers through questions rather than always giving direct answers, so that I develop deeper understanding.

#### Acceptance Criteria

1. WHEN a user asks a conceptual question (classified by the Intent_Classifier as intent type "conceptual_question" — questions seeking explanation of why, how, or the relationship between concepts, as opposed to factual recall or procedural steps) and their mastery_level for the current subtopic is FAMILIAR or higher, THE Socratic_Module SHALL respond with a guiding question instead of a direct answer
2. WHEN the Socratic_Module generates a guiding question, THE Chat_Engine SHALL store the expected concept as a structured entry containing the target concept identifier and up to 3 key terms that a correct learner response must reference
3. WHEN the learner responds to a Socratic question with an answer that contains at least 2 of the stored key terms or a synonym match for the target concept, THE Chat_Engine SHALL confirm the understanding and extend with one related insight drawn from the Cross_Lesson_Registry if a cross-reference is available for the concept
4. WHEN the learner responds to a Socratic question with an answer that contains fewer than 2 of the stored key terms and does not match the target concept, THE Chat_Engine SHALL provide a more specific guiding question that narrows the path toward the expected concept
5. IF the learner has received 3 consecutive guiding questions on the same Topic_Thread without demonstrating understanding, THEN THE Chat_Engine SHALL provide the direct explanation without further Socratic prompting
6. IF the learner explicitly requests a direct answer (detected by the Intent_Classifier as intent type "direct_answer_request") after 1 or more Socratic exchanges on the same topic, THEN THE Chat_Engine SHALL provide the direct explanation without further Socratic prompting
7. WHILE the learner's mastery_level for the current subtopic is BEGINNER, THE Socratic_Module SHALL remain inactive and the Chat_Engine SHALL provide direct explanations
8. THE Socratic_Module SHALL select guiding questions from a predefined set of question templates categorized by reasoning type (definition recall, comparison, application, cause-effect) with a minimum of 3 templates per reasoning type

### Requirement 4: Cross-Lesson Awareness

**User Story:** As a learner, I want the chatbot to reference related concepts from other lessons I've studied, so that I can build connections across topics.

#### Acceptance Criteria

1. THE Cross_Lesson_Registry SHALL maintain a mapping of key concepts to the subtopic IDs where they are taught, where key concepts are extracted from the key_takeaways field and section headings of lesson metadata, with each concept stored as a normalized term or phrase of 1 to 5 words
2. WHEN the Chat_Engine generates an explanation, THE Cross_Lesson_Registry SHALL identify related concepts from other subtopics by matching terms that appear in both the current explanation context and another subtopic's concept list, or by following prerequisite relationships declared in the lesson metadata's prerequisites field
3. WHEN a related concept is found and the user has Mastery_Data for that subtopic, THE Chat_Engine SHALL include a cross-reference of at most 1 sentence (maximum 150 characters) noting the connection between the current concept and the related subtopic by name
4. WHEN a related concept is found but the user has no Mastery_Data for that subtopic, THE Chat_Engine SHALL mention the related subtopic as a future learning opportunity using only the concept name and subtopic title without referencing any content from that subtopic's lesson material
5. IF the user explicitly asks how the current topic relates to another topic, THEN THE Chat_Engine SHALL generate a comparison response containing: at least 1 shared principle between the topics, at least 1 difference, and each point expressed in at most 2 sentences
6. THE Cross_Lesson_Registry SHALL limit cross-references to at most 2 per response
7. IF no related concepts are found for the current explanation context, THEN THE Chat_Engine SHALL generate the response without any cross-reference section and SHALL NOT indicate the absence of connections to the user
8. WHEN the Chat_Engine includes cross-references, THE Chat_Engine SHALL place them after the core explanation content and before the closing prompt in the response template structure

### Requirement 5: Adaptive Response Complexity

**User Story:** As a learner, I want the chatbot to adjust its language complexity to match my current understanding level, so that explanations are neither too simple nor too overwhelming.

#### Acceptance Criteria

1. THE Chat_Engine SHALL determine the learner's Complexity_Level based on their mastery_score for the current subtopic: SIMPLIFIED for score less than 0.3, STANDARD for score greater than or equal to 0.3 and less than or equal to 0.7, DETAILED for score greater than 0.7
2. WHILE the Complexity_Level is SIMPLIFIED, THE Chat_Engine SHALL generate responses with sentences no longer than 20 words on average, avoid domain jargon unless immediately followed by an inline definition, and include at least one concrete analogy per explanation
3. WHILE the Complexity_Level is STANDARD, THE Chat_Engine SHALL use domain terminology with parenthetical clarifications of no more than 8 words and include one example per explanation
4. WHILE the Complexity_Level is DETAILED, THE Chat_Engine SHALL use domain terminology without inline definitions, reference at least one edge case or exception, and connect the concept to exam-level application scenarios
5. WHEN the learner sends a message containing a complexity adjustment phrase (e.g., "explain more simply", "too complex", "dumb it down", "give me more detail", "go deeper"), THE Chat_Engine SHALL override the computed Complexity_Level for that response and the next 3 responses in the same Topic_Thread, shifting one tier in the requested direction
6. WHEN a complexity override expires after 3 responses, THE Chat_Engine SHALL revert to the mastery_score-computed Complexity_Level for subsequent responses in that Topic_Thread
7. IF no Mastery_Data exists for the current user and subtopic, THEN THE Chat_Engine SHALL default to STANDARD Complexity_Level

### Requirement 6: Response Template System

**User Story:** As a developer, I want response generation to use composable templates with complexity-aware variants, so that the system remains maintainable and extensible without requiring code changes for content updates.

#### Acceptance Criteria

1. THE Chat_Engine SHALL select response templates based on the combination of detected intent and current Complexity_Level
2. WHEN generating a response, THE Chat_Engine SHALL compose the final text from template parts (opener, core content, cross-reference, closing prompt) where each part is independently selectable and any part except core content may be omitted when not applicable to the current response context
3. THE Chat_Engine SHALL maintain at least 3 template variants per intent-complexity combination to avoid repetitive phrasing within a session
4. WHEN the same intent is triggered consecutively within a Topic_Thread, THE Chat_Engine SHALL select a different template variant than the one used in the previous response
5. IF all available template variants for a given intent-complexity combination have been used within the current Topic_Thread, THEN THE Chat_Engine SHALL reset the usage tracking and cycle through variants again starting from a random selection
6. THE Chat_Engine SHALL load response templates from declarative data definitions external to the engine source code, so that content updates do not require changes to application logic

### Requirement 7: Conversation State Serialization

**User Story:** As a developer, I want the conversation state to be serializable to and from a JSON-compatible dictionary, so that the frontend can persist it across page navigations without server-side session storage.

#### Acceptance Criteria

1. THE Conversation_Context SHALL be serializable to a JSON-compatible dictionary containing topic threads, discourse state, complexity overrides, Socratic state, and a schema version identifier
2. WHEN the Chat_Engine receives a serialized Conversation_Context, THE Chat_Engine SHALL reconstruct the full context and produce identical responses to subsequent messages as if the context had never been serialized
3. THE Chat_Engine SHALL guarantee that serializing and then deserializing any valid Conversation_Context produces a structurally equal Conversation_Context where all fields contain the same values
4. IF a serialized context fails validation due to missing required fields, unrecognized schema version, or fields with incorrect types, THEN THE Chat_Engine SHALL discard the payload and start a fresh Conversation_Context rather than raising an error
5. WHEN the Chat_Engine receives a serialized Conversation_Context with an older schema version, THE Chat_Engine SHALL migrate the payload to the current schema version before reconstruction, preserving all compatible state
