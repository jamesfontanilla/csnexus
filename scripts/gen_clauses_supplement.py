"""
Supplement script to add remaining questions to reach 600 total.
Adds 40 Easy, 95 Medium, 105 Hard questions.
"""

import json
import os

# Load existing questions
input_path = os.path.join("data", "seed", "questions", "verbal-ability",
                          "sentence-structure", "clauses", "questions.json")
with open(input_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

base_id = len(questions)


def add(difficulty, question, choices, answer, explanation, tags):
    global base_id
    base_id += 1
    questions.append({
        "id": base_id,
        "subtest": "Verbal Ability",
        "module": "Sentence Structure",
        "subtopic": "Clauses",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    })

# ============================================================
# ADDITIONAL EASY QUESTIONS (40 more to reach 200)
# ============================================================

add("Easy",
    "Which is an independent clause? 'Since the policy changed, compliance has improved.'",
    ["Since the policy changed", "compliance has improved", "the policy changed", "Since"],
    "compliance has improved",
    "'Compliance has improved' expresses a complete thought and can stand alone.",
    ["independent clause", "identification"])

add("Easy",
    "Which is a dependent clause? 'The staff left after the meeting ended.'",
    ["The staff left", "after the meeting ended", "the meeting ended", "The staff"],
    "after the meeting ended",
    "'After the meeting ended' begins with 'after' and cannot stand alone.",
    ["dependent clause", "time", "after"])

add("Easy",
    "What type of clause is 'that she is qualified'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It begins with 'that' and functions as a noun (e.g., 'I believe that she is qualified').",
    ["noun clause", "that", "identification"])

add("Easy",
    "Which word is a subordinating conjunction? 'He stayed home because he was sick.'",
    ["He", "stayed", "because", "sick"],
    "because",
    "'Because' introduces the dependent clause explaining the reason.",
    ["subordinating conjunction", "because"])

add("Easy",
    "Is 'the recently published report' a clause or a phrase?",
    ["Clause", "Phrase", "Dependent clause", "Independent clause"],
    "Phrase",
    "It is a noun phrase — 'published' is a participle used as an adjective, not a finite verb.",
    ["clause vs phrase", "noun phrase"])

add("Easy",
    "How many clauses? 'The director approved the plan, and the team began working.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two independent clauses joined by 'and': 'The director approved the plan' and 'the team began working.'",
    ["counting clauses", "compound sentence"])

add("Easy",
    "Which is a complete sentence?",
    ["Before the ceremony began.", "While the guests were arriving.", "The ceremony was beautiful.", "Although everyone was excited."],
    "The ceremony was beautiful.",
    "Only this option is an independent clause expressing a complete thought.",
    ["complete sentence", "identification"])

add("Easy",
    "What type of sentence? 'She left because she was tired.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Complex",
    "One independent clause + one dependent clause (because she was tired).",
    ["sentence type", "complex"])

add("Easy",
    "Which relative pronoun completes: 'The student ___ won the award is my classmate.'",
    ["whom", "whose", "which", "who"],
    "who",
    "'Who' is for people as the subject of the clause (the student WON).",
    ["relative pronoun", "who", "subject"])

add("Easy",
    "Which is a fragment?",
    ["She completed the task.", "The report was filed on time.", "While the committee was deliberating.", "He received a promotion."],
    "While the committee was deliberating.",
    "It begins with 'while' and is a dependent clause — incomplete without a main clause.",
    ["fragment", "while", "identification"])

add("Easy",
    "What type of clause is 'after the training ended'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'after' (time) and modifies a verb by telling when.",
    ["adverb clause", "time", "after"])

add("Easy",
    "Which is NOT a subordinating conjunction?",
    ["while", "because", "therefore", "although"],
    "therefore",
    "'Therefore' is a conjunctive adverb, not a subordinating conjunction.",
    ["subordinating conjunction", "conjunctive adverb"])

add("Easy",
    "Is 'she completed the assignment' an independent or dependent clause?",
    ["Independent", "Dependent", "Phrase", "Fragment"],
    "Independent",
    "It has a subject, verb, and complete thought with no subordinating word.",
    ["independent clause", "identification"])

add("Easy",
    "Which is a clause?",
    ["the old building", "very quickly", "when he arrived", "on the desk"],
    "when he arrived",
    "'When he arrived' has a subject (he) and a finite verb (arrived).",
    ["clause identification", "subject-verb pair"])

add("Easy",
    "What type of clause is 'who lives next door'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "It begins with 'who' (relative pronoun) and modifies a noun.",
    ["adjective clause", "who"])

add("Easy",
    "Which sentence has correct punctuation?",
    ["Although he was late he apologized.", "Although he was late, he apologized.", "Although, he was late he apologized.", "Although he was late; he apologized."],
    "Although he was late, he apologized.",
    "A comma follows the introductory dependent clause.",
    ["punctuation", "comma", "introductory clause"])

add("Easy",
    "How many clauses? 'She smiled.'",
    ["None", "One", "Two", "Three"],
    "One",
    "One independent clause with subject (She) and verb (smiled).",
    ["counting clauses", "simple sentence"])

add("Easy",
    "Which is a dependent clause?",
    ["The sun rose early.", "Birds sang in the trees.", "Before the day began.", "The air was fresh."],
    "Before the day began.",
    "It begins with 'before' and cannot stand alone as a sentence.",
    ["dependent clause", "before", "time"])

add("Easy",
    "What type of sentence? 'The officer filed the report.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Simple",
    "One independent clause, no dependent clauses.",
    ["sentence type", "simple"])

add("Easy",
    "Which word makes this dependent? 'unless the manager approves'",
    ["the", "manager", "unless", "approves"],
    "unless",
    "'Unless' is a subordinating conjunction creating dependency.",
    ["subordinating conjunction", "unless"])

add("Easy",
    "Is 'despite the heavy workload' a clause or phrase?",
    ["Clause", "Phrase", "Independent clause", "Dependent clause"],
    "Phrase",
    "'Despite' is a preposition followed by a noun phrase — no subject-verb pair.",
    ["clause vs phrase", "preposition"])

add("Easy",
    "Which is an independent clause? 'While he waited, she prepared the documents.'",
    ["While he waited", "she prepared the documents", "he waited", "While"],
    "she prepared the documents",
    "It expresses a complete thought without a subordinating word.",
    ["independent clause", "identification"])

add("Easy",
    "What type of clause is 'whoever finishes first'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "'Whoever finishes first' functions as a noun (subject or object).",
    ["noun clause", "whoever"])

add("Easy",
    "Which is a run-on sentence?",
    ["She left early, and he stayed.", "She left early he stayed.", "Although she left early, he stayed.", "She left early; he stayed."],
    "She left early he stayed.",
    "Two independent clauses with no punctuation or conjunction is a run-on.",
    ["run-on", "error identification"])

add("Easy",
    "Which relative pronoun completes: 'The book ___ I borrowed is interesting.'",
    ["who", "whom", "that", "whose"],
    "that",
    "'That' is used for things in restrictive clauses.",
    ["relative pronoun", "that", "things"])

add("Easy",
    "What type of clause is 'where the meeting will be held'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It functions as a noun (e.g., 'I don't know where the meeting will be held').",
    ["noun clause", "where"])

add("Easy",
    "Which is a phrase?",
    ["after she left", "the morning sun", "because it rained", "when they arrived"],
    "the morning sun",
    "'The morning sun' is a noun phrase with no verb.",
    ["clause vs phrase", "noun phrase"])

add("Easy",
    "Is this a complete sentence? 'The team won the competition.'",
    ["Yes", "No, it is a fragment", "No, it is a run-on", "No, it is a comma splice"],
    "Yes",
    "It is an independent clause with subject, verb, and complete thought.",
    ["complete sentence", "identification"])

add("Easy",
    "Which is a dependent clause? 'He will succeed if he works hard.'",
    ["He will succeed", "if he works hard", "he works hard", "will succeed"],
    "if he works hard",
    "It begins with 'if' (condition) and cannot stand alone.",
    ["dependent clause", "condition", "if"])

add("Easy",
    "What type of sentence? 'He studied, but he failed.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound",
    "Two independent clauses joined by 'but.' No dependent clause.",
    ["sentence type", "compound"])

add("Easy",
    "Which word introduces the dependent clause? 'She will attend provided that she finishes her work.'",
    ["She", "attend", "provided that", "finishes"],
    "provided that",
    "'Provided that' is a subordinating conjunction of condition.",
    ["subordinating conjunction", "provided that", "condition"])

add("Easy",
    "How many clauses? 'Although it was cold, they went outside.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'Although it was cold' (dependent) and 'they went outside' (independent).",
    ["counting clauses", "complex sentence"])

add("Easy",
    "Which is a clause?",
    ["without hesitation", "the final decision", "because they agreed", "extremely important"],
    "because they agreed",
    "It has a subject (they) and a verb (agreed), introduced by 'because.'",
    ["clause identification", "because"])

add("Easy",
    "What type of clause is 'that was built last year'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "It begins with 'that' (relative pronoun) and modifies a noun.",
    ["adjective clause", "that"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["If you need help ask the supervisor.", "If you need help, ask the supervisor.", "If, you need help ask the supervisor.", "If you need help; ask the supervisor."],
    "If you need help, ask the supervisor.",
    "A comma follows the introductory conditional clause.",
    ["punctuation", "comma", "condition"])

add("Easy",
    "Is 'although challenging' a clause or a phrase?",
    ["Clause", "Phrase", "Dependent clause", "Independent clause"],
    "Phrase",
    "It lacks a subject and finite verb. It is an elliptical/reduced phrase.",
    ["clause vs phrase", "reduced"])

add("Easy",
    "Which is an independent clause?",
    ["Whenever she visits", "The project was completed successfully", "Although the budget was tight", "Before the semester ends"],
    "The project was completed successfully",
    "It has a subject, verb, and complete thought with no subordinating word.",
    ["independent clause", "identification"])

add("Easy",
    "What type of clause is 'until the results are announced'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'until' (time) and modifies a verb.",
    ["adverb clause", "time", "until"])

add("Easy",
    "Which is a comma splice?",
    ["She was happy, for she passed.", "She was happy, she passed.", "She was happy because she passed.", "She was happy; she passed."],
    "She was happy, she passed.",
    "Two independent clauses joined by only a comma is a comma splice.",
    ["comma splice", "error identification"])

add("Easy",
    "Which relative pronoun completes: 'The city ___ I was born is beautiful.'",
    ["who", "which", "where", "whom"],
    "where",
    "'Where' is used for places as a relative adverb.",
    ["relative adverb", "where", "place"])

add("Easy",
    "How many clauses? 'The teacher who taught us retired last year.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'The teacher retired last year' (independent) and 'who taught us' (adjective).",
    ["counting clauses", "adjective clause"])

# ============================================================
# ADDITIONAL MEDIUM QUESTIONS (95 more to reach 200)
# ============================================================

add("Medium",
    "What is the function of 'that the deadline has been extended' in: 'The announcement that the deadline has been extended relieved the applicants.'?",
    ["Direct object", "Subject", "Appositive noun clause", "Adjective clause"],
    "Appositive noun clause",
    "The clause renames/explains 'announcement' — it tells what the announcement IS.",
    ["noun clause", "appositive", "function"])

add("Medium",
    "Identify the adverb clause: 'The staff will be notified as soon as the decision is finalized.'",
    ["The staff will be notified", "as soon as the decision is finalized", "the decision is finalized", "will be notified"],
    "as soon as the decision is finalized",
    "'As soon as' introduces a time clause modifying 'will be notified.'",
    ["adverb clause", "time", "as soon as"])

add("Medium",
    "Which sentence correctly uses 'who' vs 'whom'? 'The candidate ___ the panel interviewed impressed everyone.'",
    ["who the panel interviewed", "whom the panel interviewed", "whose the panel interviewed", "which the panel interviewed"],
    "whom the panel interviewed",
    "'Whom' is correct because it is the object of 'interviewed' (the panel interviewed HIM/HER).",
    ["who vs whom", "object", "relative pronoun"])

add("Medium",
    "What type of clause is 'wherever the director assigns them' in: 'The employees must report wherever the director assigns them.'?",
    ["Noun clause (direct object)", "Adjective clause", "Adverb clause of place", "Noun clause (subject)"],
    "Adverb clause of place",
    "'Wherever' introduces an adverb clause telling WHERE the employees must report.",
    ["adverb clause", "place", "wherever"])

add("Medium",
    "Identify the noun clause: 'How the error occurred remains a mystery.'",
    ["remains a mystery", "How the error occurred", "the error occurred", "a mystery"],
    "How the error occurred",
    "'How the error occurred' is a noun clause functioning as the subject of 'remains.'",
    ["noun clause", "subject", "how"])

add("Medium",
    "Which sentence has a misplaced adjective clause?",
    ["The woman who called left a message.", "The message was urgent that she left.", "The report that was filed contained errors.", "The employee who resigned was experienced."],
    "The message was urgent that she left.",
    "'That she left' should follow 'message': 'The message that she left was urgent.'",
    ["misplaced clause", "adjective clause", "error"])

add("Medium",
    "What relationship does the dependent clause express? 'Now that the training is complete, employees may return to their duties.'",
    ["Time", "Cause/Reason", "Condition", "Contrast"],
    "Cause/Reason",
    "'Now that' means 'because at this point' — it gives the reason employees may return.",
    ["clause relationship", "reason", "now that"])

add("Medium",
    "Identify the sentence type: 'The report was filed, and the supervisor reviewed it after the deadline passed.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound-Complex",
    "Two independent clauses ('The report was filed' and 'the supervisor reviewed it') plus one dependent clause ('after the deadline passed').",
    ["sentence type", "compound-complex"])

add("Medium",
    "Which subordinating conjunction best completes: '___ the evidence was overwhelming, the committee could not ignore the findings.'",
    ["Although", "Unless", "Since", "Before"],
    "Since",
    "'Since' (meaning 'because') correctly shows that the overwhelming evidence is the reason.",
    ["subordinating conjunction", "since", "reason"])

add("Medium",
    "What is the function of 'what the investigation uncovered' in: 'What the investigation uncovered shocked the public.'?",
    ["Direct object", "Subject", "Subject complement", "Object of preposition"],
    "Subject",
    "The noun clause 'What the investigation uncovered' is the subject of 'shocked.'",
    ["noun clause", "subject", "what"])

add("Medium",
    "Identify the adjective clause: 'The regulation, which has been in effect since 2020, requires annual compliance reviews.'",
    ["The regulation requires annual compliance reviews", "which has been in effect since 2020", "requires annual compliance reviews", "since 2020"],
    "which has been in effect since 2020",
    "Non-restrictive adjective clause (set off by commas) modifying 'regulation.'",
    ["adjective clause", "non-restrictive", "which"])

add("Medium",
    "How many clauses? 'She confirmed that the employee who was absent had submitted the report before the deadline.'",
    ["Two", "Three", "Four", "Five"],
    "Four",
    "Four: (1) 'She confirmed' (independent), (2) 'that the employee had submitted the report' (noun), (3) 'who was absent' (adjective), (4) 'before the deadline' — no, 'before the deadline' is a phrase. Actually three clauses.",
    ["counting clauses", "complex"])

# Fix above
questions[-1]["answer"] = "Three"
questions[-1]["choices"] = ["Two", "Three", "Four", "Five"]
questions[-1]["explanation"] = "Three clauses: (1) 'She confirmed' (independent), (2) 'that the employee who was absent had submitted the report before the deadline' (noun clause containing adjective clause), (3) 'who was absent' (adjective clause). 'Before the deadline' is a prepositional phrase, not a clause."

add("Medium",
    "Which sentence correctly combines: 'The budget was approved. The project could finally begin.'?",
    ["The budget was approved, the project could finally begin.", "Because the budget was approved, the project could finally begin.", "The budget was approved the project could finally begin.", "Although the budget was approved, the project could finally begin."],
    "Because the budget was approved, the project could finally begin.",
    "'Because' correctly shows cause-effect: approval caused the project to begin.",
    ["sentence combining", "because", "cause"])

add("Medium",
    "What type of clause is 'in case the system fails' in: 'Back up your files in case the system fails.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of condition", "Adverb clause of purpose"],
    "Adverb clause of condition",
    "'In case' introduces a conditional clause — a precautionary condition.",
    ["adverb clause", "condition", "in case"])

add("Medium",
    "Identify the noun clause: 'The question is whether we should proceed.'",
    ["The question is", "whether we should proceed", "we should proceed", "The question"],
    "whether we should proceed",
    "'Whether we should proceed' is a noun clause functioning as the subject complement after 'is.'",
    ["noun clause", "subject complement", "whether"])

add("Medium",
    "Which sentence has correct clause structure?",
    ["The employee that, was hired last month, resigned.", "The employee, that was hired last month, resigned.", "The employee that was hired last month resigned.", "The employee that was hired last month, resigned."],
    "The employee that was hired last month resigned.",
    "'That' introduces restrictive clauses — no commas needed.",
    ["restrictive clause", "that", "punctuation"])

add("Medium",
    "What relationship does 'whereas' express? 'The first team exceeded targets, whereas the second team fell short.'",
    ["Time", "Cause", "Contrast", "Condition"],
    "Contrast",
    "'Whereas' introduces a direct contrast between two situations.",
    ["clause relationship", "contrast", "whereas"])

add("Medium",
    "Identify the dependent clause type: 'The manager asked when the report would be ready.'",
    ["Adverb clause of time", "Adjective clause", "Noun clause (direct object)", "Noun clause (subject)"],
    "Noun clause (direct object)",
    "'When the report would be ready' is an indirect question functioning as the direct object of 'asked.'",
    ["noun clause", "indirect question", "when"])

add("Medium",
    "Which sentence correctly uses a non-restrictive clause?",
    ["The director who has served twenty years announced retirement.", "The director, who has served twenty years, announced retirement.", "The director, that has served twenty years, announced retirement.", "The director who has served twenty years, announced retirement."],
    "The director, who has served twenty years, announced retirement.",
    "Non-restrictive clauses use 'who' (not 'that') with commas on both sides.",
    ["non-restrictive", "who", "punctuation"])

add("Medium",
    "What is the function of 'that all employees must attend' in: 'The directive states that all employees must attend.'?",
    ["Subject", "Direct object of 'states'", "Subject complement", "Adjective modifier"],
    "Direct object of 'states'",
    "The noun clause is what was stated — the direct object.",
    ["noun clause", "direct object", "that"])

add("Medium",
    "Identify the adverb clause type: 'She spoke softly lest she disturb the sleeping child.'",
    ["Time", "Reason", "Negative purpose", "Condition"],
    "Negative purpose",
    "'Lest' means 'for fear that' — it introduces a negative purpose clause.",
    ["adverb clause", "purpose", "lest"])

add("Medium",
    "How many dependent clauses? 'The officer who was promoted confirmed that the training which he completed was rigorous.'",
    ["One", "Two", "Three", "Four"],
    "Three",
    "Three: (1) 'who was promoted' (adjective), (2) 'that the training was rigorous' (noun), (3) 'which he completed' (adjective).",
    ["counting clauses", "dependent", "three"])

add("Medium",
    "Which subordinating conjunction best completes: 'The project will succeed ___ everyone contributes.'",
    ["unless", "although", "provided that", "because"],
    "provided that",
    "'Provided that' means 'on the condition that' — success depends on everyone contributing.",
    ["subordinating conjunction", "provided that", "condition"])

add("Medium",
    "What type of clause is 'than the previous one did' in: 'The new system performs better than the previous one did.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of comparison", "Independent clause"],
    "Adverb clause of comparison",
    "'Than the previous one did' is an adverb clause of comparison modifying 'better.'",
    ["adverb clause", "comparison", "than"])

add("Medium",
    "Identify the error: 'The employee which was promoted had excellent reviews.'",
    ["'which' should be 'who'", "'was' should be 'were'", "'had' should be 'has'", "No error"],
    "'which' should be 'who'",
    "'Which' is for things; 'who' is for people. The employee is a person.",
    ["who vs which", "error", "people"])

add("Medium",
    "What is the function of 'whoever arrives first' in: 'Give the package to whoever arrives first.'?",
    ["Subject of sentence", "Direct object", "Object of preposition 'to'", "Subject complement"],
    "Object of preposition 'to'",
    "The noun clause is the object of 'to.' Note: 'whoever' (not 'whomever') because it is the subject of 'arrives.'",
    ["noun clause", "object of preposition", "whoever"])

add("Medium",
    "Which sentence correctly fixes: 'Although she was qualified. She was not hired.'?",
    ["Although she was qualified; she was not hired.", "Although she was qualified, she was not hired.", "Although she was qualified she was not hired.", "She was qualified although. She was not hired."],
    "Although she was qualified, she was not hired.",
    "Join the dependent and independent clauses in one sentence with a comma.",
    ["fragment correction", "although", "comma"])

add("Medium",
    "Identify the clause type: 'The exam was such that many students failed.'",
    ["Noun clause", "Adjective clause", "Adverb clause of result", "Adverb clause of manner"],
    "Adverb clause of result",
    "'Such...that' introduces a result clause — the nature of the exam caused failure.",
    ["adverb clause", "result", "such that"])

add("Medium",
    "What type of clause is 'as the director instructed' in: 'Complete the form as the director instructed.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of manner", "Adverb clause of time"],
    "Adverb clause of manner",
    "'As the director instructed' tells HOW to complete the form.",
    ["adverb clause", "manner", "as"])

add("Medium",
    "Which sentence uses a noun clause as a subject complement?",
    ["She knows that he is honest.", "The issue is whether we can afford it.", "I asked what time it was.", "That he lied is obvious."],
    "The issue is whether we can afford it.",
    "'Whether we can afford it' follows the linking verb 'is' and describes the subject 'issue.'",
    ["noun clause", "subject complement", "whether"])

add("Medium",
    "Identify the adjective clause: 'The time when we must decide is approaching.'",
    ["The time is approaching", "when we must decide", "we must decide", "is approaching"],
    "when we must decide",
    "'When we must decide' modifies 'time' (tells which time).",
    ["adjective clause", "when", "time"])

add("Medium",
    "Which sentence has a subject-verb agreement issue with a noun clause?",
    ["What he wants is unclear.", "What they need are more resources.", "Whether she attends is her choice.", "That the reports are late is concerning."],
    "What they need are more resources.",
    "The noun clause subject is singular; the verb should be 'is': 'What they need is more resources.'",
    ["subject-verb agreement", "noun clause", "error"])

add("Medium",
    "What relationship does 'even though' express?",
    ["Time", "Cause", "Concession", "Condition"],
    "Concession",
    "'Even though' introduces an unexpected contrast — the result is surprising given the circumstance.",
    ["clause relationship", "concession", "even though"])

add("Medium",
    "Identify the sentence type: 'What she said surprised me, but I did not show it.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound-Complex",
    "Two independent clauses ('What she said surprised me' and 'I did not show it') plus one dependent noun clause ('What she said').",
    ["sentence type", "compound-complex"])

add("Medium",
    "Which subordinating conjunction best completes: 'She reviewed the manual ___ she could answer questions correctly.'",
    ["because", "although", "so that", "unless"],
    "so that",
    "'So that' introduces purpose — the reason for reviewing.",
    ["subordinating conjunction", "so that", "purpose"])

add("Medium",
    "What is the function of 'that the funds are available' in: 'The certification that the funds are available must be submitted.'?",
    ["Direct object", "Subject", "Appositive noun clause", "Adjective clause"],
    "Appositive noun clause",
    "The clause explains what the certification IS — it is in apposition to 'certification.'",
    ["noun clause", "appositive", "that"])

add("Medium",
    "Identify the error: 'The reason is because he was absent.'",
    ["'is' should be 'was'", "'because' should be 'that'", "'absent' should be 'absence'", "No error"],
    "'because' should be 'that'",
    "'The reason is that...' is correct. 'The reason is because...' is redundant.",
    ["redundancy", "reason is that", "error"])

add("Medium",
    "Which sentence correctly uses an indirect question?",
    ["I wonder where is the office.", "I wonder where the office is.", "I wonder is the office where.", "Where I wonder the office is."],
    "I wonder where the office is.",
    "Indirect questions use statement word order: 'where the office is' (not 'where is the office').",
    ["indirect question", "word order", "noun clause"])

add("Medium",
    "What type of clause is 'once the approval is granted' in: 'The project will begin once the approval is granted.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of time", "Adverb clause of condition"],
    "Adverb clause of time",
    "'Once' means 'as soon as' — it introduces a time clause.",
    ["adverb clause", "time", "once"])

add("Medium",
    "Identify the adjective clause: 'The reason why she resigned remains unclear.'",
    ["The reason remains unclear", "why she resigned", "she resigned", "remains unclear"],
    "why she resigned",
    "'Why she resigned' modifies 'reason' (tells which reason/what kind of reason).",
    ["adjective clause", "why", "reason"])

add("Medium",
    "Which sentence correctly combines: 'He is experienced. He was not selected.'?",
    ["He is experienced, he was not selected.", "Although he is experienced, he was not selected.", "He is experienced because he was not selected.", "He is experienced, and he was not selected."],
    "Although he is experienced, he was not selected.",
    "'Although' correctly shows concession — not selected despite experience.",
    ["sentence combining", "concession", "although"])

add("Medium",
    "What is the function of 'how the budget should be allocated' in: 'The committee will decide how the budget should be allocated.'?",
    ["Subject", "Direct object of 'decide'", "Subject complement", "Adverb clause"],
    "Direct object of 'decide'",
    "The noun clause is what will be decided — the direct object.",
    ["noun clause", "direct object", "how"])

add("Medium",
    "Identify the adverb clause: 'Wherever you go, follow the safety protocols.'",
    ["follow the safety protocols", "Wherever you go", "you go", "the safety protocols"],
    "Wherever you go",
    "'Wherever you go' is an adverb clause of place.",
    ["adverb clause", "place", "wherever"])

add("Medium",
    "Which sentence has correct punctuation?",
    ["The policy which was revised, is effective.", "The policy, which was revised is effective.", "The policy, which was revised, is effective.", "The policy which was revised is effective."],
    "The policy, which was revised, is effective.",
    "'Which' introduces a non-restrictive clause requiring commas on both sides.",
    ["punctuation", "non-restrictive", "which"])

add("Medium",
    "What type of dependent clause is 'that requires annual renewal' in: 'The license that requires annual renewal must be updated.'?",
    ["Noun clause", "Adjective clause (restrictive)", "Adjective clause (non-restrictive)", "Adverb clause"],
    "Adjective clause (restrictive)",
    "'That requires annual renewal' identifies WHICH license — restrictive, no commas.",
    ["adjective clause", "restrictive", "that"])

add("Medium",
    "Identify the noun clause: 'Whether the amendment passes depends on the vote count.'",
    ["depends on the vote count", "Whether the amendment passes", "the amendment passes", "the vote count"],
    "Whether the amendment passes",
    "The noun clause functions as the subject of 'depends.'",
    ["noun clause", "subject", "whether"])

add("Medium",
    "Which subordinating conjunction best completes: 'The meeting was productive ___ it lasted only thirty minutes.'",
    ["because", "although", "unless", "after"],
    "although",
    "'Although' shows concession — productive despite being short.",
    ["subordinating conjunction", "although", "concession"])

add("Medium",
    "What is the function of 'whom the director appointed' in: 'The officer whom the director appointed will lead the task force.'?",
    ["Subject", "Direct object", "Modifier of 'officer'", "Subject complement"],
    "Modifier of 'officer'",
    "The adjective clause modifies 'officer' (tells which officer).",
    ["adjective clause", "whom", "modifier"])

add("Medium",
    "Identify the sentence type: 'I know that she is qualified, and I will recommend her.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound-Complex",
    "Two independent clauses ('I know' and 'I will recommend her') plus one dependent noun clause ('that she is qualified').",
    ["sentence type", "compound-complex"])

add("Medium",
    "Which sentence correctly uses 'that' vs 'which'?",
    ["The car, that she drives, is new.", "The car that she drives is new.", "The car, which she drives is new.", "The car that she drives, is new."],
    "The car that she drives is new.",
    "'That' for restrictive clauses (no commas). Identifies which car.",
    ["that vs which", "restrictive", "punctuation"])

add("Medium",
    "What type of clause is 'inasmuch as the evidence supports it' in: 'The conclusion is valid inasmuch as the evidence supports it.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of reason", "Adverb clause of condition"],
    "Adverb clause of reason",
    "'Inasmuch as' means 'because/to the extent that' — it gives the reason.",
    ["adverb clause", "reason", "inasmuch as"])

add("Medium",
    "Identify the error: 'I wonder that she will come.'",
    ["'wonder' should be 'know'", "'that' should be 'whether/if'", "'will' should be 'would'", "No error"],
    "'that' should be 'whether/if'",
    "After 'wonder,' use 'whether' or 'if' (not 'that') for indirect yes/no questions.",
    ["noun clause", "whether vs that", "error"])

add("Medium",
    "How many clauses? 'The director said that the policy would change and that the staff would be notified.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three: (1) 'The director said' (independent), (2) 'that the policy would change' (noun), (3) 'that the staff would be notified' (noun).",
    ["counting clauses", "parallel noun clauses"])

add("Medium",
    "Which sentence correctly places the adverb clause?",
    ["The staff, because the office closed early, went home.", "Because the office closed early, the staff went home.", "The staff went because the office closed early home.", "Because the office closed early the staff, went home."],
    "Because the office closed early, the staff went home.",
    "Introductory adverb clause + comma + independent clause is the standard pattern.",
    ["adverb clause", "placement", "punctuation"])

add("Medium",
    "What is the function of 'when the new policy takes effect' in: 'Everyone wants to know when the new policy takes effect.'?",
    ["Adverb clause of time", "Adjective clause", "Noun clause (direct object)", "Noun clause (subject)"],
    "Noun clause (direct object)",
    "'When the new policy takes effect' is an indirect question — the direct object of 'know.'",
    ["noun clause", "indirect question", "when"])

add("Medium",
    "Which sentence has a fragment?",
    ["Although the task was difficult, she completed it.", "She completed the task. Although it was difficult.", "The task was difficult, but she completed it.", "She completed the difficult task on time."],
    "She completed the task. Although it was difficult.",
    "'Although it was difficult' is a dependent clause punctuated as a separate sentence — a fragment.",
    ["fragment", "identification", "although"])

add("Medium",
    "Identify the clause type: 'The harder she works, the more she achieves.'",
    ["Two independent clauses", "Two adverb clauses of comparison", "Correlative comparative structure", "Compound sentence"],
    "Correlative comparative structure",
    "'The...the...' is a correlative comparative structure where both clauses are interdependent.",
    ["comparative", "correlative", "the...the"])

add("Medium",
    "Which subordinating conjunction best completes: 'She will not be promoted ___ she completes the required training.'",
    ["because", "although", "until", "while"],
    "until",
    "'Until' means the promotion won't happen before the training is complete.",
    ["subordinating conjunction", "until", "time"])

add("Medium",
    "What type of clause is 'as if he had seen a ghost' in: 'He looked as if he had seen a ghost.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of manner", "Adverb clause of reason"],
    "Adverb clause of manner",
    "'As if he had seen a ghost' describes HOW he looked.",
    ["adverb clause", "manner", "as if"])

add("Medium",
    "Identify the adjective clause: 'The year when the regulation was enacted saw many changes.'",
    ["The year saw many changes", "when the regulation was enacted", "the regulation was enacted", "saw many changes"],
    "when the regulation was enacted",
    "'When the regulation was enacted' modifies 'year' (tells which year).",
    ["adjective clause", "when", "time"])

add("Medium",
    "Which sentence correctly uses a noun clause after 'suggest'?",
    ["I suggest that he attends the meeting.", "I suggest that he attend the meeting.", "I suggest that he will attend the meeting.", "I suggest him to attend the meeting."],
    "I suggest that he attend the meeting.",
    "After 'suggest' (mandative verb), use the subjunctive: base form 'attend.'",
    ["subjunctive", "suggest", "noun clause"])

add("Medium",
    "What is the function of 'that the project was completed on time' in: 'The fact that the project was completed on time impressed the client.'?",
    ["Direct object", "Subject", "Appositive to 'fact'", "Adjective clause"],
    "Appositive to 'fact'",
    "The noun clause explains what the fact IS — it is in apposition.",
    ["noun clause", "appositive", "fact"])

add("Medium",
    "Identify the error: 'The employee, that was hired last month, resigned.'",
    ["'that' should be 'who' or 'which' (non-restrictive needs who/which, not that)", "'was' should be 'were'", "'resigned' should be 'has resigned'", "No error"],
    "'that' should be 'who' or 'which' (non-restrictive needs who/which, not that)",
    "'That' cannot introduce non-restrictive clauses (with commas). Use 'who' for people.",
    ["that vs who", "non-restrictive", "error"])

add("Medium",
    "How many clauses? 'Although the weather was bad, the event proceeded as planned, and everyone enjoyed it.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three: (1) 'Although the weather was bad' (dependent), (2) 'the event proceeded as planned' (independent), (3) 'everyone enjoyed it' (independent).",
    ["counting clauses", "compound-complex"])

add("Medium",
    "Which sentence correctly transforms: 'Where is the office?' into an indirect question?",
    ["She asked where is the office.", "She asked where the office is.", "She asked where the office was.", "She asked that where the office is."],
    "She asked where the office was.",
    "Indirect questions use statement word order and backshift tense: 'where the office was.'",
    ["indirect question", "word order", "tense"])

add("Medium",
    "What type of clause is 'while effective' in: 'The policy, while effective, has some drawbacks.'?",
    ["Adverb clause (reduced)", "Adjective clause", "Noun clause", "Independent clause"],
    "Adverb clause (reduced)",
    "'While effective' is a reduced adverb clause (from 'while it is effective').",
    ["reduced clause", "adverb clause", "while"])

add("Medium",
    "Identify the noun clause: 'It is important that everyone participates.'",
    ["It is important", "that everyone participates", "everyone participates", "is important"],
    "that everyone participates",
    "'That everyone participates' is a noun clause — the true subject (extraposed). 'It' is a dummy subject.",
    ["noun clause", "extraposed subject", "that"])

add("Medium",
    "Which sentence correctly uses 'unless'?",
    ["Unless you don't submit the form, you will be disqualified.", "Unless you submit the form, you will be disqualified.", "Unless you will submit the form, you will be disqualified.", "Unless submitting the form, you will be disqualified."],
    "Unless you submit the form, you will be disqualified.",
    "'Unless' means 'if not' — don't add another negative. Use present tense in the condition.",
    ["unless", "condition", "correct usage"])

add("Medium",
    "What is the function of 'why the system failed' in: 'The report explains why the system failed.'?",
    ["Subject", "Direct object of 'explains'", "Subject complement", "Adverb clause"],
    "Direct object of 'explains'",
    "The noun clause is what the report explains — the direct object.",
    ["noun clause", "direct object", "why"])
