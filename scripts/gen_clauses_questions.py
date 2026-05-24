"""
Generate 600 multiple-choice questions for the Clauses subtopic.
Verbal Ability > Sentence Structure > Clauses
200 Easy / 200 Medium / 200 Hard
"""

import json
import os

questions = []
qid = 0


def add(difficulty, question, choices, answer, explanation, tags):
    global qid
    qid += 1
    questions.append({
        "id": qid,
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
# EASY QUESTIONS (200)
# ============================================================

# --- Independent vs Dependent Identification (1-40) ---
add("Easy",
    "Which of the following is an independent clause?",
    ["Because she was late", "The manager approved the request", "Although the report was ready", "When the bell rang"],
    "The manager approved the request",
    "An independent clause expresses a complete thought and can stand alone as a sentence. 'The manager approved the request' is grammatically complete.",
    ["independent clause", "identification", "complete thought"])

add("Easy",
    "Which of the following is a dependent clause?",
    ["The employees submitted their reports", "She passed the examination", "Because the office was closed", "The director signed the memorandum"],
    "Because the office was closed",
    "'Because the office was closed' begins with the subordinating conjunction 'because' and does not express a complete thought by itself.",
    ["dependent clause", "identification", "subordinating conjunction"])

add("Easy",
    "Which group of words is an independent clause?",
    ["After the meeting ended", "Although he studied hard", "The staff returned to work", "Unless you submit the form"],
    "The staff returned to work",
    "'The staff returned to work' has a subject (staff), a verb (returned), and expresses a complete thought.",
    ["independent clause", "identification", "complete thought"])

add("Easy",
    "Identify the dependent clause: 'When the results were announced, everyone cheered.'",
    ["everyone cheered", "When the results were announced", "the results were announced", "everyone"],
    "When the results were announced",
    "The clause begins with the subordinating conjunction 'when' and cannot stand alone as a complete sentence.",
    ["dependent clause", "adverb clause", "time"])

add("Easy",
    "Which is a dependent clause?",
    ["The teacher explained the lesson", "He finished the project on time", "If you study consistently", "They celebrated their success"],
    "If you study consistently",
    "'If you study consistently' begins with the subordinating conjunction 'if' and expresses an incomplete thought.",
    ["dependent clause", "condition", "if"])

add("Easy",
    "Which is an independent clause in this sentence? 'Although it rained, the event continued.'",
    ["Although it rained", "the event continued", "it rained", "Although"],
    "the event continued",
    "'The event continued' expresses a complete thought and can stand alone. 'Although it rained' is dependent because of 'although.'",
    ["independent clause", "identification", "concession"])

add("Easy",
    "Identify the independent clause: 'Because the budget was cut, the project was delayed.'",
    ["Because the budget was cut", "the project was delayed", "the budget was cut", "was delayed"],
    "the project was delayed",
    "'The project was delayed' is a complete thought that can stand alone as a sentence.",
    ["independent clause", "identification", "cause"])

add("Easy",
    "Which of the following can stand alone as a complete sentence?",
    ["While she was working", "Before the deadline passed", "The committee made a decision", "Although the plan was approved"],
    "The committee made a decision",
    "Only 'The committee made a decision' expresses a complete thought without depending on another clause.",
    ["independent clause", "complete thought", "sentence"])

add("Easy",
    "Which is a dependent clause?",
    ["The officer filed the report", "She received a promotion", "Until the investigation is complete", "The agency issued new guidelines"],
    "Until the investigation is complete",
    "'Until the investigation is complete' begins with 'until' and cannot stand alone as a sentence.",
    ["dependent clause", "time", "until"])

add("Easy",
    "Identify the independent clause: 'After she graduated, she applied for a government position.'",
    ["After she graduated", "she applied for a government position", "she graduated", "for a government position"],
    "she applied for a government position",
    "This clause expresses a complete thought and does not begin with a subordinating conjunction.",
    ["independent clause", "identification", "time"])

add("Easy",
    "Which of the following is NOT a clause?",
    ["She works hard", "Because he left early", "In the morning", "The report was submitted"],
    "In the morning",
    "'In the morning' is a prepositional phrase — it has no subject-verb pair, so it is not a clause.",
    ["clause vs phrase", "identification", "prepositional phrase"])

add("Easy",
    "Which is a clause?",
    ["running in the park", "after the meeting", "because she was absent", "with great enthusiasm"],
    "because she was absent",
    "'Because she was absent' has a subject (she) and a finite verb (was), making it a clause. The others are phrases.",
    ["clause vs phrase", "identification", "dependent clause"])

add("Easy",
    "Which group of words is a phrase, NOT a clause?",
    ["when the bell rings", "the students left", "during the examination", "she answered correctly"],
    "during the examination",
    "'During the examination' is a prepositional phrase with no subject-verb pair.",
    ["clause vs phrase", "phrase identification"])

add("Easy",
    "Which is a dependent clause?",
    ["The applicant was nervous", "She answered all questions", "Although the test was difficult", "The results were posted online"],
    "Although the test was difficult",
    "'Although the test was difficult' begins with 'although' and cannot express a complete thought alone.",
    ["dependent clause", "concession", "although"])

add("Easy",
    "Which is an independent clause?",
    ["Since the policy changed", "While the director was away", "The employees followed the new procedure", "Before the audit began"],
    "The employees followed the new procedure",
    "This clause has a subject, verb, and complete thought with no subordinating conjunction.",
    ["independent clause", "identification", "complete thought"])

add("Easy",
    "Identify the dependent clause: 'The officer who investigated the case filed a report.'",
    ["The officer filed a report", "who investigated the case", "filed a report", "the case"],
    "who investigated the case",
    "'Who investigated the case' is an adjective clause introduced by the relative pronoun 'who.' It modifies 'officer.'",
    ["dependent clause", "adjective clause", "relative pronoun"])

add("Easy",
    "Which of the following contains a subject and a verb?",
    ["in the office", "running quickly", "before she arrived", "with great care"],
    "before she arrived",
    "'Before she arrived' has a subject (she) and a verb (arrived). The others are phrases without subject-verb pairs.",
    ["clause identification", "subject-verb pair"])

add("Easy",
    "Which is a dependent clause?",
    ["The memo was distributed", "He completed the training", "Unless you have permission", "The deadline is tomorrow"],
    "Unless you have permission",
    "'Unless you have permission' begins with the subordinating conjunction 'unless' and is an incomplete thought.",
    ["dependent clause", "condition", "unless"])

add("Easy",
    "Which is an independent clause in this sentence? 'If you pass the exam, you will be promoted.'",
    ["If you pass the exam", "you will be promoted", "you pass the exam", "If you pass"],
    "you will be promoted",
    "'You will be promoted' is a complete thought that can stand alone as a sentence.",
    ["independent clause", "condition", "if"])

add("Easy",
    "Which of the following is a clause?",
    ["the tall building", "quickly and efficiently", "after he submitted the form", "in front of the office"],
    "after he submitted the form",
    "'After he submitted the form' contains a subject (he) and a verb (submitted), making it a clause.",
    ["clause identification", "subject-verb pair", "dependent clause"])

# --- Subordinating Conjunction Identification (21-40) ---
add("Easy",
    "Which word is a subordinating conjunction in this sentence? 'She left early because she felt ill.'",
    ["She", "early", "because", "ill"],
    "because",
    "'Because' is a subordinating conjunction that introduces the dependent clause 'because she felt ill.'",
    ["subordinating conjunction", "because", "identification"])

add("Easy",
    "Which word makes the clause dependent? 'Although the report was complete'",
    ["the", "report", "Although", "complete"],
    "Although",
    "'Although' is a subordinating conjunction that makes the clause dependent — it cannot stand alone.",
    ["subordinating conjunction", "although", "dependent clause"])

add("Easy",
    "Which word introduces the dependent clause? 'The meeting was postponed because the director was absent.'",
    ["The", "was", "because", "absent"],
    "because",
    "'Because' introduces the dependent clause 'because the director was absent' and shows a cause relationship.",
    ["subordinating conjunction", "because", "cause"])

add("Easy",
    "Identify the subordinating conjunction: 'If you complete the training, you will receive a certificate.'",
    ["you", "complete", "If", "will"],
    "If",
    "'If' is a subordinating conjunction that introduces a condition.",
    ["subordinating conjunction", "if", "condition"])

add("Easy",
    "Which word signals a dependent clause? 'When the alarm sounded, everyone evacuated.'",
    ["the", "sounded", "When", "everyone"],
    "When",
    "'When' is a subordinating conjunction that introduces the time clause 'When the alarm sounded.'",
    ["subordinating conjunction", "when", "time"])

add("Easy",
    "Which is a subordinating conjunction?",
    ["and", "but", "because", "or"],
    "because",
    "'Because' is a subordinating conjunction. 'And,' 'but,' and 'or' are coordinating conjunctions (FANBOYS).",
    ["subordinating conjunction", "identification", "coordinating vs subordinating"])

add("Easy",
    "Which word introduces a dependent clause?",
    ["however", "therefore", "although", "moreover"],
    "although",
    "'Although' is a subordinating conjunction that introduces dependent clauses. The others are conjunctive adverbs.",
    ["subordinating conjunction", "although", "conjunctive adverb"])

add("Easy",
    "Identify the subordinating conjunction: 'Unless you apply, you will not be considered.'",
    ["you", "apply", "Unless", "not"],
    "Unless",
    "'Unless' means 'if not' and introduces a conditional dependent clause.",
    ["subordinating conjunction", "unless", "condition"])

add("Easy",
    "Which word makes this a dependent clause? 'while the supervisor was on leave'",
    ["the", "supervisor", "while", "leave"],
    "while",
    "'While' is a subordinating conjunction indicating time, making the clause dependent.",
    ["subordinating conjunction", "while", "time"])

add("Easy",
    "Which is a subordinating conjunction?",
    ["so (coordinating)", "yet", "since", "nor"],
    "since",
    "'Since' can function as a subordinating conjunction (meaning 'because' or 'from the time that'). The others listed are coordinating conjunctions.",
    ["subordinating conjunction", "since", "identification"])

add("Easy",
    "Which word introduces the dependent clause? 'Before the deadline arrives, submit your documents.'",
    ["submit", "your", "Before", "documents"],
    "Before",
    "'Before' is a subordinating conjunction introducing the time clause 'Before the deadline arrives.'",
    ["subordinating conjunction", "before", "time"])

add("Easy",
    "Identify the subordinating conjunction: 'She will be promoted after she passes the exam.'",
    ["She", "promoted", "after", "passes"],
    "after",
    "'After' introduces the dependent clause 'after she passes the exam' and indicates time.",
    ["subordinating conjunction", "after", "time"])

add("Easy",
    "Which word creates a dependent clause?",
    ["the", "quickly", "until", "very"],
    "until",
    "'Until' is a subordinating conjunction that introduces dependent clauses of time.",
    ["subordinating conjunction", "until", "time"])

add("Easy",
    "Which is NOT a subordinating conjunction?",
    ["because", "although", "and", "unless"],
    "and",
    "'And' is a coordinating conjunction (FANBOYS), not a subordinating conjunction.",
    ["subordinating conjunction", "coordinating conjunction", "FANBOYS"])

add("Easy",
    "Which word introduces the dependent clause? 'The project failed because the team lacked resources.'",
    ["project", "failed", "because", "resources"],
    "because",
    "'Because' is the subordinating conjunction introducing the reason clause.",
    ["subordinating conjunction", "because", "reason"])

add("Easy",
    "Identify the subordinating conjunction: 'Even though he was tired, he continued working.'",
    ["he", "tired", "Even though", "continued"],
    "Even though",
    "'Even though' is a subordinating conjunction expressing concession.",
    ["subordinating conjunction", "even though", "concession"])

add("Easy",
    "Which word signals that a clause is dependent? 'She stayed late so that she could finish the report.'",
    ["stayed", "late", "so that", "finish"],
    "so that",
    "'So that' is a subordinating conjunction introducing a purpose clause.",
    ["subordinating conjunction", "so that", "purpose"])

add("Easy",
    "Which is a subordinating conjunction?",
    ["furthermore", "however", "whereas", "nevertheless"],
    "whereas",
    "'Whereas' is a subordinating conjunction showing contrast. The others are conjunctive adverbs.",
    ["subordinating conjunction", "whereas", "contrast"])

add("Easy",
    "Which word introduces the dependent clause? 'Once the forms are signed, the process can begin.'",
    ["the", "forms", "Once", "process"],
    "Once",
    "'Once' is a subordinating conjunction meaning 'as soon as' or 'after,' introducing a time clause.",
    ["subordinating conjunction", "once", "time"])

add("Easy",
    "Identify the subordinating conjunction: 'Provided that you meet the requirements, your application will be processed.'",
    ["you", "meet", "Provided that", "processed"],
    "Provided that",
    "'Provided that' is a subordinating conjunction introducing a conditional clause.",
    ["subordinating conjunction", "provided that", "condition"])

# --- Clause vs Phrase (41-60) ---
add("Easy",
    "Is 'in the government office' a clause or a phrase?",
    ["Clause", "Phrase", "Independent clause", "Dependent clause"],
    "Phrase",
    "'In the government office' is a prepositional phrase — it has no subject-verb pair.",
    ["clause vs phrase", "prepositional phrase"])

add("Easy",
    "Is 'the committee decided' a clause or a phrase?",
    ["Phrase", "Clause", "Neither", "Fragment"],
    "Clause",
    "'The committee decided' has a subject (committee) and a verb (decided), making it a clause.",
    ["clause vs phrase", "clause identification"])

add("Easy",
    "Which is a phrase?",
    ["she was promoted", "because he resigned", "with great difficulty", "the policy changed"],
    "with great difficulty",
    "'With great difficulty' is a prepositional phrase with no subject-verb pair.",
    ["clause vs phrase", "phrase identification"])

add("Easy",
    "Which is a clause?",
    ["under the table", "the bright morning sun", "while they waited", "running very fast"],
    "while they waited",
    "'While they waited' has a subject (they) and a finite verb (waited), introduced by 'while.'",
    ["clause vs phrase", "clause identification"])

add("Easy",
    "Is 'running through the corridor' a clause or a phrase?",
    ["Clause", "Phrase", "Independent clause", "Dependent clause"],
    "Phrase",
    "'Running' is a participle (non-finite verb), and there is no subject. This is a participial phrase.",
    ["clause vs phrase", "participial phrase"])

add("Easy",
    "Which is a clause?",
    ["before the deadline", "to finish the project", "after she submitted the report", "the new employee"],
    "after she submitted the report",
    "It has a subject (she), a finite verb (submitted), and is introduced by 'after.'",
    ["clause vs phrase", "clause identification", "time"])

add("Easy",
    "Is 'to complete the assignment' a clause or a phrase?",
    ["Clause", "Phrase", "Dependent clause", "Independent clause"],
    "Phrase",
    "'To complete' is an infinitive (non-finite verb form). This is an infinitive phrase, not a clause.",
    ["clause vs phrase", "infinitive phrase"])

add("Easy",
    "Which is NOT a clause?",
    ["because he was late", "the manager approved it", "during the conference", "if she agrees"],
    "during the conference",
    "'During the conference' is a prepositional phrase — no subject-verb pair.",
    ["clause vs phrase", "prepositional phrase"])

add("Easy",
    "Is 'that the policy was effective' a clause or a phrase?",
    ["Phrase", "Clause", "Neither", "Sentence"],
    "Clause",
    "It has a subject (policy), a verb (was), and is introduced by 'that.' It is a noun clause.",
    ["clause vs phrase", "noun clause"])

add("Easy",
    "Which is a phrase?",
    ["when the alarm rang", "the extremely detailed report", "she completed the task", "although it was raining"],
    "the extremely detailed report",
    "'The extremely detailed report' is a noun phrase — it has no verb.",
    ["clause vs phrase", "noun phrase"])

add("Easy",
    "Is 'having completed the training' a clause or a phrase?",
    ["Clause", "Phrase", "Independent clause", "Dependent clause"],
    "Phrase",
    "'Having completed' is a perfect participle (non-finite). This is a participial phrase, not a clause.",
    ["clause vs phrase", "participial phrase"])

add("Easy",
    "Which contains a subject-verb pair?",
    ["the new policy", "in the morning", "before she left", "with careful planning"],
    "before she left",
    "'Before she left' has a subject (she) and a finite verb (left).",
    ["clause identification", "subject-verb pair"])

add("Easy",
    "Is 'because of the heavy rain' a clause or a phrase?",
    ["Clause", "Phrase", "Dependent clause", "Adverb clause"],
    "Phrase",
    "'Because of' is a compound preposition followed by a noun phrase. There is no subject-verb pair. Compare with 'because it rained heavily' (clause).",
    ["clause vs phrase", "preposition vs conjunction"])

add("Easy",
    "Which is a clause?",
    ["the recently hired employee", "working overtime", "since the office opened", "near the entrance"],
    "since the office opened",
    "'Since the office opened' has a subject (office) and a verb (opened), introduced by 'since.'",
    ["clause vs phrase", "clause identification"])

add("Easy",
    "Is 'who was assigned to the project' a clause or a phrase?",
    ["Phrase", "Clause", "Neither", "Simple sentence"],
    "Clause",
    "It has a subject (who) and a verb (was assigned). It is an adjective clause.",
    ["clause vs phrase", "adjective clause", "relative pronoun"])

add("Easy",
    "Which is a phrase?",
    ["if the budget allows", "the carefully prepared document", "she was promoted", "because they agreed"],
    "the carefully prepared document",
    "'The carefully prepared document' is a noun phrase — no finite verb.",
    ["clause vs phrase", "noun phrase"])

add("Easy",
    "Is 'the employees who were hired last month' a clause or a phrase?",
    ["Clause", "Phrase", "Both", "Neither"],
    "Both",
    "The full expression is a noun phrase ('the employees...'), but it contains an embedded adjective clause ('who were hired last month').",
    ["clause vs phrase", "embedded clause"])

add("Easy",
    "Which group of words is a clause?",
    ["despite the challenges", "the well-organized event", "although the task was difficult", "for the entire department"],
    "although the task was difficult",
    "It has a subject (task), a verb (was), and begins with the subordinating conjunction 'although.'",
    ["clause vs phrase", "dependent clause", "although"])

add("Easy",
    "Is 'what the director said' a clause or a phrase?",
    ["Phrase", "Clause", "Sentence", "Fragment"],
    "Clause",
    "It has a subject (director) and a verb (said), introduced by 'what.' It is a noun clause.",
    ["clause vs phrase", "noun clause", "what"])

add("Easy",
    "Which is NOT a clause?",
    ["while she waited", "he submitted the form", "the recently approved budget", "because it was urgent"],
    "the recently approved budget",
    "'The recently approved budget' is a noun phrase with no finite verb.",
    ["clause vs phrase", "noun phrase"])

# --- Simple Clause Type Identification (61-100) ---
add("Easy",
    "What type of clause is 'because she was absent'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'because' (subordinating conjunction of reason) and modifies a verb by explaining why.",
    ["adverb clause", "reason", "because"])

add("Easy",
    "What type of clause is 'who submitted the report'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "It begins with the relative pronoun 'who' and modifies a noun (describes which person).",
    ["adjective clause", "relative pronoun", "who"])

add("Easy",
    "What type of clause is 'that the meeting was canceled'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It begins with 'that' and functions as a noun (can be subject or object of a verb).",
    ["noun clause", "that", "identification"])

add("Easy",
    "What type of clause is 'when the bell rings'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'when' (subordinating conjunction of time) and tells when something happens.",
    ["adverb clause", "time", "when"])

add("Easy",
    "What type of clause is 'which was approved last week'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "It begins with the relative pronoun 'which' and describes a noun.",
    ["adjective clause", "relative pronoun", "which"])

add("Easy",
    "What type of clause is 'what the committee decided'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It begins with 'what' and functions as a noun (subject or object in a sentence).",
    ["noun clause", "what", "identification"])

add("Easy",
    "What type of clause is 'although the weather was bad'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'although' (subordinating conjunction of concession) and modifies a verb.",
    ["adverb clause", "concession", "although"])

add("Easy",
    "What type of clause is 'whose performance improved'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "It begins with the relative pronoun 'whose' and modifies a noun (describes possession).",
    ["adjective clause", "relative pronoun", "whose"])

add("Easy",
    "What type of clause is 'whether the policy is effective'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It begins with 'whether' and functions as a noun (subject, object, or complement).",
    ["noun clause", "whether", "identification"])

add("Easy",
    "What type of clause is 'if the documents are complete'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'if' (subordinating conjunction of condition) and tells under what condition.",
    ["adverb clause", "condition", "if"])

add("Easy",
    "What type of clause is 'that you submitted yesterday'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "'That you submitted yesterday' modifies a noun (e.g., 'the report that you submitted yesterday'). The relative pronoun 'that' refers back to a noun.",
    ["adjective clause", "relative pronoun", "that"])

add("Easy",
    "What type of clause is 'before the deadline expires'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'before' (subordinating conjunction of time) and tells when.",
    ["adverb clause", "time", "before"])

add("Easy",
    "What type of clause is 'how the system works'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It begins with 'how' and functions as a noun (e.g., 'I understand how the system works').",
    ["noun clause", "how", "identification"])

add("Easy",
    "What type of clause is 'where the office is located'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It begins with 'where' and functions as a noun (e.g., 'I know where the office is located').",
    ["noun clause", "where", "identification"])

add("Easy",
    "What type of clause is 'unless you have authorization'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'unless' (subordinating conjunction of condition) and tells under what condition.",
    ["adverb clause", "condition", "unless"])

add("Easy",
    "What type of clause is 'whom the panel selected'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "It begins with the relative pronoun 'whom' and modifies a noun (describes which person).",
    ["adjective clause", "relative pronoun", "whom"])

add("Easy",
    "What type of clause is 'since the regulation took effect'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'since' (subordinating conjunction of time/reason) and modifies a verb.",
    ["adverb clause", "time", "since"])

add("Easy",
    "What type of clause is 'why the project was delayed'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Noun clause",
    "It begins with 'why' and functions as a noun (e.g., 'No one knows why the project was delayed').",
    ["noun clause", "why", "identification"])

add("Easy",
    "What type of clause is 'while the director was speaking'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adverb clause",
    "It begins with 'while' (subordinating conjunction of time) and tells when.",
    ["adverb clause", "time", "while"])

add("Easy",
    "What type of clause is 'that was issued last month'?",
    ["Independent clause", "Noun clause", "Adjective clause", "Adverb clause"],
    "Adjective clause",
    "It begins with the relative pronoun 'that' and modifies a noun (describes which one).",
    ["adjective clause", "relative pronoun", "that"])

# --- Sentence Completeness (101-120) ---
add("Easy",
    "Is this a complete sentence? 'Because the office was closed.'",
    ["Yes, it is complete", "No, it is a fragment", "Yes, it is a compound sentence", "No, it is a run-on"],
    "No, it is a fragment",
    "This is a dependent clause (begins with 'because') written as a sentence. It needs an independent clause to be complete.",
    ["fragment", "sentence completeness", "dependent clause"])

add("Easy",
    "Is this a complete sentence? 'The employees submitted their reports on time.'",
    ["Yes, it is complete", "No, it is a fragment", "No, it is a run-on", "Yes, it is complex"],
    "Yes, it is complete",
    "This is an independent clause with a subject (employees), verb (submitted), and complete thought.",
    ["complete sentence", "independent clause"])

add("Easy",
    "Is this a complete sentence? 'Although the training was mandatory.'",
    ["Yes, it is complete", "No, it is a fragment", "Yes, it is a simple sentence", "No, it is a run-on"],
    "No, it is a fragment",
    "This dependent clause begins with 'although' and does not express a complete thought alone.",
    ["fragment", "sentence completeness", "although"])

add("Easy",
    "Is this a complete sentence? 'When the director arrives.'",
    ["Yes, it is complete", "No, it is a fragment", "Yes, it is complex", "No, it is a comma splice"],
    "No, it is a fragment",
    "This is a dependent clause beginning with 'when.' It leaves the reader expecting more information.",
    ["fragment", "sentence completeness", "when"])

add("Easy",
    "Is this a complete sentence? 'She passed the civil service examination.'",
    ["No, it is a fragment", "Yes, it is complete", "No, it is a run-on", "Yes, it is compound"],
    "Yes, it is complete",
    "This is an independent clause — subject (She), verb (passed), complete thought.",
    ["complete sentence", "independent clause"])

add("Easy",
    "Which is a sentence fragment?",
    ["The report was filed yesterday.", "Although the budget was approved.", "She received a commendation.", "The office opened at eight."],
    "Although the budget was approved.",
    "It begins with 'although' (subordinating conjunction), making it a dependent clause that cannot stand alone.",
    ["fragment", "identification", "although"])

add("Easy",
    "Which is a complete sentence?",
    ["While the committee deliberated.", "Because the funds were insufficient.", "The agency released the results.", "If the applicant qualifies."],
    "The agency released the results.",
    "Only this option is an independent clause expressing a complete thought.",
    ["complete sentence", "identification"])

add("Easy",
    "Which is a sentence fragment?",
    ["The supervisor approved the leave.", "Unless the employee submits a medical certificate.", "The deadline was extended.", "They completed the project."],
    "Unless the employee submits a medical certificate.",
    "It begins with 'unless' and is a dependent clause — incomplete without a main clause.",
    ["fragment", "identification", "unless"])

add("Easy",
    "Is this a complete sentence? 'The budget was approved, and the project started.'",
    ["Yes, it is complete", "No, it is a fragment", "No, it is a run-on", "Yes, but it has an error"],
    "Yes, it is complete",
    "This is a compound sentence: two independent clauses joined by a comma and 'and.'",
    ["complete sentence", "compound sentence"])

add("Easy",
    "Is this a complete sentence? 'Who was assigned to the project.'",
    ["Yes, it is complete", "No, it is a fragment", "Yes, it is a question", "No, it is a run-on"],
    "No, it is a fragment",
    "This is an adjective clause (begins with 'who') that needs a noun to modify and a main clause.",
    ["fragment", "adjective clause", "relative pronoun"])

# --- Simple Relative Pronoun Identification (121-140) ---
add("Easy",
    "Which relative pronoun correctly completes the sentence? 'The employee ___ was promoted had excellent reviews.'",
    ["which", "whom", "who", "whose"],
    "who",
    "'Who' is used for people as the subject of the clause. The employee performed the action of being promoted.",
    ["relative pronoun", "who", "subject"])

add("Easy",
    "Which relative pronoun correctly completes the sentence? 'The report ___ was submitted contained errors.'",
    ["who", "whom", "that", "whose"],
    "that",
    "'That' is used for things in restrictive clauses. It refers to 'report.'",
    ["relative pronoun", "that", "things"])

add("Easy",
    "Which relative pronoun correctly completes the sentence? 'The officer ___ report was late received a warning.'",
    ["who", "whom", "which", "whose"],
    "whose",
    "'Whose' shows possession — the report belongs to the officer.",
    ["relative pronoun", "whose", "possession"])

add("Easy",
    "Which relative pronoun correctly completes the sentence? 'The applicant ___ we interviewed was qualified.'",
    ["who", "whom", "whose", "which"],
    "whom",
    "'Whom' is used for people as the object of the clause. 'We interviewed' the applicant (object).",
    ["relative pronoun", "whom", "object"])

add("Easy",
    "Which relative pronoun correctly completes the sentence? 'The policy, ___ was revised last year, is now effective.'",
    ["who", "that", "which", "whom"],
    "which",
    "'Which' is used for things in non-restrictive clauses (note the commas).",
    ["relative pronoun", "which", "non-restrictive"])

add("Easy",
    "Which relative pronoun refers to people?",
    ["which", "that (only)", "who", "where"],
    "who",
    "'Who' specifically refers to people. 'Which' refers to things. 'That' can refer to both.",
    ["relative pronoun", "who", "people"])

add("Easy",
    "Which relative pronoun shows possession?",
    ["who", "whom", "whose", "which"],
    "whose",
    "'Whose' indicates possession (e.g., 'the employee whose file was lost').",
    ["relative pronoun", "whose", "possession"])

add("Easy",
    "Which relative pronoun is used for things in non-restrictive clauses?",
    ["that", "who", "which", "whom"],
    "which",
    "'Which' introduces non-restrictive (non-essential) clauses about things, set off by commas.",
    ["relative pronoun", "which", "non-restrictive"])

add("Easy",
    "Which relative pronoun correctly completes: 'The building ___ houses the agency is on Main Street.'",
    ["who", "whom", "that", "whose"],
    "that",
    "'That' is used for things in restrictive clauses. It refers to 'building.'",
    ["relative pronoun", "that", "restrictive"])

add("Easy",
    "Which relative pronoun correctly completes: 'The supervisor ___ I reported to has retired.'",
    ["who", "whom", "whose", "which"],
    "whom",
    "'Whom' is the object form — 'I reported to whom.' The supervisor received the action.",
    ["relative pronoun", "whom", "object of preposition"])

add("Easy",
    "Which relative pronoun correctly completes: 'The students ___ passed the exam celebrated.'",
    ["whom", "whose", "which", "who"],
    "who",
    "'Who' is used for people as the subject of the clause — the students performed the action of passing.",
    ["relative pronoun", "who", "subject"])

add("Easy",
    "Which relative pronoun correctly completes: 'The document ___ you need is on the desk.'",
    ["who", "whom", "that", "whose"],
    "that",
    "'That' refers to things in restrictive clauses. 'You need' the document (object).",
    ["relative pronoun", "that", "object"])

add("Easy",
    "Which relative pronoun correctly completes: 'The manager ___ team won the award gave a speech.'",
    ["who", "whom", "whose", "which"],
    "whose",
    "'Whose' shows possession — the team belongs to the manager.",
    ["relative pronoun", "whose", "possession"])

add("Easy",
    "Which relative pronoun correctly completes: 'The regulation, ___ took effect last month, affects all employees.'",
    ["that", "who", "which", "whom"],
    "which",
    "'Which' is used for things in non-restrictive clauses (commas present).",
    ["relative pronoun", "which", "non-restrictive"])

add("Easy",
    "Which relative pronoun correctly completes: 'The candidate ___ the committee chose starts Monday.'",
    ["who", "whom", "whose", "which"],
    "whom",
    "'Whom' is the object — 'the committee chose whom.'",
    ["relative pronoun", "whom", "object"])

add("Easy",
    "Which relative pronoun correctly completes: 'The office ___ she works is on the third floor.'",
    ["who", "which", "where", "whom"],
    "where",
    "'Where' is a relative adverb used for places.",
    ["relative adverb", "where", "place"])

add("Easy",
    "Which relative pronoun correctly completes: 'The day ___ results are released is always stressful.'",
    ["who", "which", "when", "whom"],
    "when",
    "'When' is a relative adverb used for times.",
    ["relative adverb", "when", "time"])

add("Easy",
    "Which relative pronoun correctly completes: 'The employee ___ filed the complaint was transferred.'",
    ["whom", "whose", "which", "who"],
    "who",
    "'Who' is used for people as the subject — the employee performed the action of filing.",
    ["relative pronoun", "who", "subject"])

add("Easy",
    "Which relative pronoun correctly completes: 'The memo ___ the director signed is now effective.'",
    ["who", "whom", "that", "whose"],
    "that",
    "'That' refers to things in restrictive clauses. The director signed the memo (object).",
    ["relative pronoun", "that", "restrictive"])

add("Easy",
    "Which relative pronoun correctly completes: 'The teacher ___ class I attended was excellent.'",
    ["who", "whom", "whose", "which"],
    "whose",
    "'Whose' shows possession — the class belongs to the teacher.",
    ["relative pronoun", "whose", "possession"])

# --- Counting Clauses (141-160) ---
add("Easy",
    "How many clauses are in this sentence? 'The officer submitted the report.'",
    ["One", "Two", "Three", "None"],
    "One",
    "There is one subject-verb pair (officer submitted), so there is one clause (independent).",
    ["counting clauses", "simple sentence"])

add("Easy",
    "How many clauses are in this sentence? 'She studied hard, and she passed the exam.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two independent clauses joined by 'and': 'She studied hard' and 'she passed the exam.'",
    ["counting clauses", "compound sentence"])

add("Easy",
    "How many clauses are in this sentence? 'Because it rained, the event was canceled.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'Because it rained' (dependent) and 'the event was canceled' (independent).",
    ["counting clauses", "complex sentence"])

add("Easy",
    "How many clauses are in this sentence? 'The employee who was late apologized.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'The employee apologized' (independent) and 'who was late' (adjective clause).",
    ["counting clauses", "adjective clause"])

add("Easy",
    "How many clauses are in this sentence? 'She knows that the deadline is tomorrow.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'She knows' (independent) and 'that the deadline is tomorrow' (noun clause).",
    ["counting clauses", "noun clause"])

add("Easy",
    "How many clauses are in this sentence? 'The director approved the budget.'",
    ["One", "Two", "Three", "None"],
    "One",
    "One independent clause with one subject-verb pair (director approved).",
    ["counting clauses", "simple sentence"])

add("Easy",
    "How many clauses are in this sentence? 'If you apply, you will be considered.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'If you apply' (dependent/condition) and 'you will be considered' (independent).",
    ["counting clauses", "complex sentence", "condition"])

add("Easy",
    "How many clauses are in this sentence? 'The report was submitted, but it contained errors.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two independent clauses joined by 'but': 'The report was submitted' and 'it contained errors.'",
    ["counting clauses", "compound sentence"])

add("Easy",
    "How many clauses are in this sentence? 'I believe that she is honest.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'I believe' (independent) and 'that she is honest' (noun clause).",
    ["counting clauses", "noun clause"])

add("Easy",
    "How many clauses are in this sentence? 'The policy that was revised takes effect today.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'The policy takes effect today' (independent) and 'that was revised' (adjective clause).",
    ["counting clauses", "adjective clause"])

add("Easy",
    "How many clauses are in this sentence? 'When the alarm sounded, everyone evacuated immediately.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'When the alarm sounded' (dependent/time) and 'everyone evacuated immediately' (independent).",
    ["counting clauses", "complex sentence", "time"])

add("Easy",
    "How many clauses are in this sentence? 'She left early because she was ill.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'She left early' (independent) and 'because she was ill' (dependent/reason).",
    ["counting clauses", "complex sentence", "reason"])

add("Easy",
    "How many clauses are in this sentence? 'The manager signed the document and submitted it.'",
    ["One", "Two", "Three", "Four"],
    "One",
    "One clause with a compound predicate (signed AND submitted). The subject 'manager' is shared — there is only one subject-verb unit.",
    ["counting clauses", "compound predicate"])

add("Easy",
    "How many clauses are in this sentence? 'Although he was tired, he finished the work.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'Although he was tired' (dependent/concession) and 'he finished the work' (independent).",
    ["counting clauses", "complex sentence", "concession"])

add("Easy",
    "How many clauses are in this sentence? 'The team celebrated after they won.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'The team celebrated' (independent) and 'after they won' (dependent/time).",
    ["counting clauses", "complex sentence", "time"])

add("Easy",
    "How many clauses are in this sentence? 'She is the officer who handles complaints.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'She is the officer' (independent) and 'who handles complaints' (adjective clause).",
    ["counting clauses", "adjective clause"])

add("Easy",
    "How many clauses are in this sentence? 'What he said was surprising.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'What he said' (noun clause/subject) and the main clause 'What he said was surprising.'",
    ["counting clauses", "noun clause"])

add("Easy",
    "How many clauses are in this sentence? 'The students reviewed their notes before the exam started.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'The students reviewed their notes' (independent) and 'before the exam started' (dependent/time).",
    ["counting clauses", "complex sentence", "time"])

add("Easy",
    "How many clauses are in this sentence? 'He works hard and earns well.'",
    ["One", "Two", "Three", "Four"],
    "One",
    "One clause with a compound predicate (works AND earns). 'He' is the shared subject.",
    ["counting clauses", "compound predicate"])

add("Easy",
    "How many clauses are in this sentence? 'Unless you register, you cannot take the exam.'",
    ["One", "Two", "Three", "Four"],
    "Two",
    "Two clauses: 'Unless you register' (dependent/condition) and 'you cannot take the exam' (independent).",
    ["counting clauses", "complex sentence", "condition"])

# --- Basic Sentence Type Identification (161-180) ---
add("Easy",
    "What type of sentence is this? 'The committee approved the proposal.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Simple",
    "It has one independent clause and no dependent clauses.",
    ["sentence type", "simple sentence"])

add("Easy",
    "What type of sentence is this? 'She studied hard, and she passed the exam.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound",
    "It has two independent clauses joined by a coordinating conjunction ('and').",
    ["sentence type", "compound sentence"])

add("Easy",
    "What type of sentence is this? 'Because the budget was approved, the project started.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Complex",
    "It has one independent clause and one dependent clause (begins with 'because').",
    ["sentence type", "complex sentence"])

add("Easy",
    "What type of sentence is this? 'The report was filed, but the director had not reviewed it.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound",
    "Two independent clauses joined by 'but.' No dependent clause.",
    ["sentence type", "compound sentence"])

add("Easy",
    "What type of sentence is this? 'When the alarm rang, the employees evacuated.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Complex",
    "One dependent clause ('When the alarm rang') + one independent clause ('the employees evacuated').",
    ["sentence type", "complex sentence"])

add("Easy",
    "What type of sentence is this? 'The officer filed the report and submitted the evidence.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Simple",
    "One independent clause with a compound predicate (filed AND submitted). One subject, two verbs.",
    ["sentence type", "simple sentence", "compound predicate"])

add("Easy",
    "What type of sentence is this? 'Although it was late, she finished the task, and she submitted it.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound-Complex",
    "It has two independent clauses ('she finished the task' and 'she submitted it') and one dependent clause ('Although it was late').",
    ["sentence type", "compound-complex sentence"])

add("Easy",
    "What type of sentence is this? 'The employee who arrived early received praise.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Complex",
    "One independent clause with an embedded dependent clause ('who arrived early').",
    ["sentence type", "complex sentence", "adjective clause"])

add("Easy",
    "What type of sentence is this? 'She left early; he stayed late.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound",
    "Two independent clauses joined by a semicolon.",
    ["sentence type", "compound sentence", "semicolon"])

add("Easy",
    "What type of sentence is this? 'I know that she is qualified.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Complex",
    "One independent clause ('I know') + one dependent noun clause ('that she is qualified').",
    ["sentence type", "complex sentence", "noun clause"])

# --- Basic Punctuation with Clauses (181-200) ---
add("Easy",
    "Which sentence is punctuated correctly?",
    ["Because she was late she missed the meeting.", "Because she was late, she missed the meeting.", "Because, she was late she missed the meeting.", "Because she was late; she missed the meeting."],
    "Because she was late, she missed the meeting.",
    "When a dependent clause comes before an independent clause, a comma separates them.",
    ["punctuation", "comma", "introductory clause"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["The report was submitted, and the director approved it.", "The report was submitted and, the director approved it.", "The report was submitted, and, the director approved it.", "The report, was submitted and the director approved it."],
    "The report was submitted, and the director approved it.",
    "A comma before the coordinating conjunction 'and' correctly joins two independent clauses.",
    ["punctuation", "compound sentence", "comma"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["She passed the exam because she studied hard.", "She passed the exam, because she studied hard.", "She passed the exam; because she studied hard.", "She passed the exam. Because she studied hard."],
    "She passed the exam because she studied hard.",
    "When the dependent clause follows the independent clause, no comma is typically needed.",
    ["punctuation", "no comma", "dependent after independent"])

add("Easy",
    "Which sentence has a comma splice error?",
    ["She was tired, so she went home.", "She was tired, she went home.", "Although she was tired, she continued.", "She was tired; she went home."],
    "She was tired, she went home.",
    "Two independent clauses joined by only a comma is a comma splice. A conjunction or semicolon is needed.",
    ["comma splice", "error identification", "punctuation"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["Although the task was difficult she completed it.", "Although the task was difficult, she completed it.", "Although, the task was difficult she completed it.", "Although the task was difficult. She completed it."],
    "Although the task was difficult, she completed it.",
    "A comma follows the introductory dependent clause before the independent clause.",
    ["punctuation", "comma", "introductory clause"])

add("Easy",
    "Where should the comma be placed? 'If you need assistance please ask the receptionist.'",
    ["After 'If'", "After 'assistance'", "After 'please'", "No comma needed"],
    "After 'assistance'",
    "The introductory dependent clause 'If you need assistance' should be followed by a comma.",
    ["punctuation", "comma placement", "condition"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["The director, who has served for twenty years announced her retirement.", "The director who has served for twenty years, announced her retirement.", "The director, who has served for twenty years, announced her retirement.", "The director who has served for twenty years announced her retirement."],
    "The director, who has served for twenty years, announced her retirement.",
    "Non-restrictive adjective clauses are set off by commas on both sides.",
    ["punctuation", "non-restrictive clause", "commas"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["The employees who passed the exam, will be promoted.", "The employees, who passed the exam will be promoted.", "The employees who passed the exam will be promoted.", "The employees who passed the exam; will be promoted."],
    "The employees who passed the exam will be promoted.",
    "Restrictive adjective clauses (essential to meaning) do NOT use commas.",
    ["punctuation", "restrictive clause", "no commas"])

add("Easy",
    "Where should the comma be placed? 'After the audit was completed the findings were presented.'",
    ["After 'After'", "After 'completed'", "After 'findings'", "No comma needed"],
    "After 'completed'",
    "The introductory adverb clause 'After the audit was completed' should be followed by a comma.",
    ["punctuation", "comma placement", "introductory clause"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["When the bell rings the students leave.", "When the bell rings, the students leave.", "When, the bell rings the students leave.", "When the bell rings; the students leave."],
    "When the bell rings, the students leave.",
    "A comma separates the introductory dependent clause from the independent clause.",
    ["punctuation", "comma", "time clause"])

add("Easy",
    "Which sentence has correct punctuation?",
    ["He left early, because he was sick.", "He left early because he was sick.", "He left early; because he was sick.", "He left early. Because he was sick."],
    "He left early because he was sick.",
    "When the dependent clause follows the independent clause, no comma is needed (for 'because' clauses).",
    ["punctuation", "no comma", "because"])

add("Easy",
    "Which sentence is a run-on?",
    ["She finished the report, and she submitted it.", "She finished the report she submitted it.", "After she finished the report, she submitted it.", "She finished the report; then she submitted it."],
    "She finished the report she submitted it.",
    "Two independent clauses with no punctuation or conjunction between them create a run-on sentence.",
    ["run-on", "error identification", "punctuation"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["The policy which was revised last year is now effective.", "The policy, which was revised last year, is now effective.", "The policy, which was revised last year is now effective.", "The policy which was revised last year, is now effective."],
    "The policy, which was revised last year, is now effective.",
    "'Which' introduces a non-restrictive clause requiring commas on both sides.",
    ["punctuation", "non-restrictive", "which"])

add("Easy",
    "Which sentence has a fragment error?",
    ["Because the meeting was canceled, we left early.", "We left early because the meeting was canceled.", "Because the meeting was canceled.", "The meeting was canceled, so we left early."],
    "Because the meeting was canceled.",
    "A dependent clause punctuated as a complete sentence is a fragment.",
    ["fragment", "error identification", "because"])

add("Easy",
    "Where should the comma be placed? 'Unless you have permission you cannot enter the restricted area.'",
    ["After 'Unless'", "After 'permission'", "After 'cannot'", "No comma needed"],
    "After 'permission'",
    "The introductory conditional clause 'Unless you have permission' needs a comma after it.",
    ["punctuation", "comma placement", "condition"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["She will be promoted, after she completes the training.", "She will be promoted after she completes the training.", "She will be promoted; after she completes the training.", "She will be promoted. After she completes the training."],
    "She will be promoted after she completes the training.",
    "When the dependent clause follows the independent clause, no comma is typically needed.",
    ["punctuation", "no comma", "after"])

add("Easy",
    "Which sentence has correct punctuation?",
    ["The officer who filed the report, is here.", "The officer, who filed the report is here.", "The officer who filed the report is here.", "The officer; who filed the report is here."],
    "The officer who filed the report is here.",
    "This is a restrictive clause (identifies which officer), so no commas are used.",
    ["punctuation", "restrictive clause", "no commas"])

add("Easy",
    "Which sentence is a comma splice?",
    ["The budget was approved, so the project began.", "The budget was approved, the project began.", "Although the budget was approved, the project was delayed.", "The budget was approved; the project began."],
    "The budget was approved, the project began.",
    "Two independent clauses joined by only a comma (no conjunction) is a comma splice.",
    ["comma splice", "error identification"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["While the director was speaking, the staff took notes.", "While the director was speaking the staff took notes.", "While, the director was speaking the staff took notes.", "While the director was speaking; the staff took notes."],
    "While the director was speaking, the staff took notes.",
    "An introductory adverb clause ('While the director was speaking') is followed by a comma.",
    ["punctuation", "comma", "while"])

add("Easy",
    "Which sentence is punctuated correctly?",
    ["I don't know, whether she will attend.", "I don't know whether she will attend.", "I don't know; whether she will attend.", "I don't know. Whether she will attend."],
    "I don't know whether she will attend.",
    "A noun clause ('whether she will attend') acting as a direct object is not separated from the verb by a comma.",
    ["punctuation", "noun clause", "no comma"])

# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Clause Function Analysis (201-240) ---
add("Medium",
    "What is the function of the underlined clause? 'The committee announced THAT ALL EMPLOYEES MUST ATTEND THE SEMINAR.'",
    ["Subject", "Direct object", "Subject complement", "Adjective modifier"],
    "Direct object",
    "The noun clause 'that all employees must attend the seminar' is the direct object of 'announced' (announced WHAT?).",
    ["noun clause", "direct object", "function"])

add("Medium",
    "What is the function of the underlined clause? 'WHAT THE DIRECTOR SAID surprised everyone.'",
    ["Direct object", "Subject", "Subject complement", "Object of preposition"],
    "Subject",
    "The noun clause 'What the director said' is the subject of the verb 'surprised.'",
    ["noun clause", "subject", "function"])

add("Medium",
    "What is the function of the underlined clause? 'The problem is THAT NO ONE FOLLOWED THE PROCEDURE.'",
    ["Subject", "Direct object", "Subject complement", "Adverb modifier"],
    "Subject complement",
    "The noun clause follows the linking verb 'is' and renames/describes the subject 'problem.'",
    ["noun clause", "subject complement", "linking verb"])

add("Medium",
    "What is the function of the underlined clause? 'She gave the award to WHOEVER SCORED HIGHEST.'",
    ["Subject", "Direct object", "Object of preposition", "Subject complement"],
    "Object of preposition",
    "The noun clause 'whoever scored highest' is the object of the preposition 'to.'",
    ["noun clause", "object of preposition", "function"])

add("Medium",
    "What is the function of the clause 'who was assigned to the project' in: 'The officer who was assigned to the project filed a report.'?",
    ["Subject of the sentence", "Direct object", "Modifier of 'officer'", "Adverb of reason"],
    "Modifier of 'officer'",
    "The adjective clause 'who was assigned to the project' modifies the noun 'officer' (tells which officer).",
    ["adjective clause", "modifier", "function"])

add("Medium",
    "What is the function of the clause 'because the funds were insufficient' in: 'The project was canceled because the funds were insufficient.'?",
    ["Subject", "Direct object", "Modifier of 'project'", "Modifier of 'was canceled' (reason)"],
    "Modifier of 'was canceled' (reason)",
    "The adverb clause modifies the verb 'was canceled' by explaining why.",
    ["adverb clause", "reason", "function"])

add("Medium",
    "What is the function of the clause 'that the budget was approved' in: 'The fact that the budget was approved pleased the team.'?",
    ["Subject", "Direct object", "Modifier of 'fact'", "Subject complement"],
    "Modifier of 'fact'",
    "This is an appositive noun clause that renames/explains the noun 'fact.' It functions as a modifier.",
    ["noun clause", "appositive", "function"])

add("Medium",
    "What is the function of the clause 'whether the policy should be revised' in: 'The question is whether the policy should be revised.'?",
    ["Subject", "Direct object", "Subject complement", "Object of preposition"],
    "Subject complement",
    "The noun clause follows the linking verb 'is' and describes the subject 'question.'",
    ["noun clause", "subject complement", "function"])

add("Medium",
    "What is the function of the clause 'whose report was outstanding' in: 'The employee whose report was outstanding received recognition.'?",
    ["Subject", "Direct object", "Modifier of 'employee'", "Adverb of manner"],
    "Modifier of 'employee'",
    "The adjective clause 'whose report was outstanding' modifies 'employee' (tells which employee).",
    ["adjective clause", "modifier", "whose"])

add("Medium",
    "What is the function of the clause 'after the investigation is completed' in: 'The findings will be released after the investigation is completed.'?",
    ["Subject", "Direct object", "Modifier of 'findings'", "Modifier of 'will be released' (time)"],
    "Modifier of 'will be released' (time)",
    "The adverb clause modifies the verb 'will be released' by telling when.",
    ["adverb clause", "time", "function"])

add("Medium",
    "Identify the noun clause and its function: 'I don't understand why the application was rejected.'",
    ["'why the application was rejected' — subject", "'why the application was rejected' — direct object", "'the application was rejected' — direct object", "'I don't understand' — independent clause"],
    "'why the application was rejected' — direct object",
    "The noun clause 'why the application was rejected' is the direct object of 'understand' (understand WHAT?).",
    ["noun clause", "direct object", "why"])

add("Medium",
    "Identify the noun clause and its function: 'Whether he will accept the position remains uncertain.'",
    ["'Whether he will accept the position' — subject", "'he will accept the position' — subject", "'remains uncertain' — predicate", "'Whether he will accept' — direct object"],
    "'Whether he will accept the position' — subject",
    "The noun clause 'Whether he will accept the position' is the subject of 'remains.'",
    ["noun clause", "subject", "whether"])

add("Medium",
    "What type of dependent clause is 'that the committee approved' in: 'The policy that the committee approved is now in effect.'?",
    ["Noun clause (direct object)", "Adjective clause (modifies 'policy')", "Adverb clause (reason)", "Noun clause (subject)"],
    "Adjective clause (modifies 'policy')",
    "'That the committee approved' modifies the noun 'policy' — it tells which policy. 'That' is a relative pronoun here.",
    ["adjective clause", "that", "restrictive"])

add("Medium",
    "What type of dependent clause is 'that the deadline was extended' in: 'She confirmed that the deadline was extended.'?",
    ["Adjective clause", "Adverb clause", "Noun clause (direct object)", "Noun clause (subject)"],
    "Noun clause (direct object)",
    "'That the deadline was extended' is the direct object of 'confirmed' (confirmed WHAT?). Here 'that' is a conjunction, not a relative pronoun.",
    ["noun clause", "that", "direct object"])

add("Medium",
    "What is the function of 'where the documents are stored' in: 'No one knows where the documents are stored.'?",
    ["Subject", "Direct object", "Subject complement", "Adjective modifier"],
    "Direct object",
    "The noun clause is the direct object of 'knows' (knows WHAT?).",
    ["noun clause", "direct object", "where"])

add("Medium",
    "What type of clause is 'provided that the requirements are met' in: 'The application will be processed provided that the requirements are met.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of condition", "Adverb clause of reason"],
    "Adverb clause of condition",
    "'Provided that' is a subordinating conjunction of condition. The clause tells under what condition.",
    ["adverb clause", "condition", "provided that"])

add("Medium",
    "What is the function of 'whoever submits first' in: 'Whoever submits first will be prioritized.'?",
    ["Direct object", "Subject", "Object of preposition", "Adjective modifier"],
    "Subject",
    "The noun clause 'Whoever submits first' is the subject of 'will be prioritized.'",
    ["noun clause", "subject", "whoever"])

add("Medium",
    "What type of clause is 'where new employees are assigned' in: 'The office where new employees are assigned is on the second floor.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of place", "Independent clause"],
    "Adjective clause",
    "'Where new employees are assigned' modifies the noun 'office' (tells which office). It is an adjective clause.",
    ["adjective clause", "where", "place"])

add("Medium",
    "What is the function of 'how the error occurred' in: 'The investigation revealed how the error occurred.'?",
    ["Subject", "Direct object", "Subject complement", "Adverb modifier"],
    "Direct object",
    "The noun clause 'how the error occurred' is the direct object of 'revealed' (revealed WHAT?).",
    ["noun clause", "direct object", "how"])

add("Medium",
    "What type of clause is 'so that employees can access the system remotely' in: 'The IT department upgraded the network so that employees can access the system remotely.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of purpose", "Adverb clause of result"],
    "Adverb clause of purpose",
    "'So that' introduces a purpose clause — it explains why the network was upgraded.",
    ["adverb clause", "purpose", "so that"])

# --- Complex Clause Identification in Sentences (241-280) ---
add("Medium",
    "Identify the adjective clause: 'The regulation that was implemented last year has reduced violations significantly.'",
    ["The regulation has reduced violations significantly", "that was implemented last year", "has reduced violations significantly", "last year"],
    "that was implemented last year",
    "The clause 'that was implemented last year' modifies 'regulation' (tells which regulation).",
    ["adjective clause", "identification", "that"])

add("Medium",
    "Identify the adverb clause: 'The employees remained calm even though the situation was critical.'",
    ["The employees remained calm", "even though the situation was critical", "the situation was critical", "remained calm"],
    "even though the situation was critical",
    "'Even though the situation was critical' is an adverb clause of concession modifying 'remained.'",
    ["adverb clause", "concession", "even though"])

add("Medium",
    "Identify the noun clause: 'The supervisor asked whether the report had been submitted.'",
    ["The supervisor asked", "whether the report had been submitted", "the report had been submitted", "had been submitted"],
    "whether the report had been submitted",
    "'Whether the report had been submitted' is a noun clause functioning as the direct object of 'asked.'",
    ["noun clause", "whether", "direct object"])

add("Medium",
    "Identify the independent clause: 'Although the training was optional, most employees attended because they wanted to improve their skills.'",
    ["Although the training was optional", "most employees attended", "because they wanted to improve their skills", "they wanted to improve their skills"],
    "most employees attended",
    "'Most employees attended' is the main independent clause. The other clauses are dependent (although... and because...).",
    ["independent clause", "complex sentence", "identification"])

add("Medium",
    "Identify the adjective clause: 'The candidate whom the panel recommended has accepted the position.'",
    ["The candidate has accepted the position", "whom the panel recommended", "has accepted the position", "the panel recommended"],
    "whom the panel recommended",
    "'Whom the panel recommended' modifies 'candidate' (tells which candidate). 'Whom' is the object.",
    ["adjective clause", "whom", "object"])

add("Medium",
    "Identify the adverb clause: 'Before the fiscal year ends, all departments must submit their budget proposals.'",
    ["all departments must submit their budget proposals", "Before the fiscal year ends", "the fiscal year ends", "must submit their budget proposals"],
    "Before the fiscal year ends",
    "'Before the fiscal year ends' is an adverb clause of time modifying 'must submit.'",
    ["adverb clause", "time", "before"])

add("Medium",
    "Identify the noun clause: 'That the project was completed on time impressed the stakeholders.'",
    ["That the project was completed on time", "impressed the stakeholders", "the project was completed on time", "the stakeholders"],
    "That the project was completed on time",
    "The noun clause 'That the project was completed on time' functions as the subject of 'impressed.'",
    ["noun clause", "subject", "that"])

add("Medium",
    "Identify the dependent clause: 'The manager will approve the request as soon as the documents are verified.'",
    ["The manager will approve the request", "as soon as the documents are verified", "the documents are verified", "will approve the request"],
    "as soon as the documents are verified",
    "'As soon as the documents are verified' is a dependent adverb clause of time.",
    ["dependent clause", "time", "as soon as"])

add("Medium",
    "Identify the adjective clause: 'The office where the incident occurred has been temporarily closed.'",
    ["The office has been temporarily closed", "where the incident occurred", "has been temporarily closed", "the incident occurred"],
    "where the incident occurred",
    "'Where the incident occurred' modifies 'office' (tells which office). 'Where' functions as a relative adverb.",
    ["adjective clause", "where", "relative adverb"])

add("Medium",
    "Identify the adverb clause: 'Unless the committee approves the amendment, the original policy will remain in effect.'",
    ["the original policy will remain in effect", "Unless the committee approves the amendment", "the committee approves the amendment", "will remain in effect"],
    "Unless the committee approves the amendment",
    "'Unless the committee approves the amendment' is an adverb clause of condition.",
    ["adverb clause", "condition", "unless"])

add("Medium",
    "Identify the noun clause: 'The director explained how the new system would improve efficiency.'",
    ["The director explained", "how the new system would improve efficiency", "the new system would improve efficiency", "would improve efficiency"],
    "how the new system would improve efficiency",
    "'How the new system would improve efficiency' is a noun clause functioning as the direct object of 'explained.'",
    ["noun clause", "how", "direct object"])

add("Medium",
    "Identify the adjective clause: 'The employees whose evaluations were outstanding received bonuses.'",
    ["The employees received bonuses", "whose evaluations were outstanding", "received bonuses", "evaluations were outstanding"],
    "whose evaluations were outstanding",
    "'Whose evaluations were outstanding' modifies 'employees' (tells which employees).",
    ["adjective clause", "whose", "possession"])

add("Medium",
    "Identify the adverb clause: 'She completed the project ahead of schedule so that she could take her leave.'",
    ["She completed the project ahead of schedule", "so that she could take her leave", "she could take her leave", "ahead of schedule"],
    "so that she could take her leave",
    "'So that she could take her leave' is an adverb clause of purpose.",
    ["adverb clause", "purpose", "so that"])

add("Medium",
    "Identify the independent clause: 'While the audit was being conducted, the department continued its operations, and the staff cooperated fully.'",
    ["While the audit was being conducted", "the department continued its operations", "the staff cooperated fully", "Both 'the department continued its operations' and 'the staff cooperated fully'"],
    "Both 'the department continued its operations' and 'the staff cooperated fully'",
    "There are two independent clauses joined by 'and.' 'While the audit was being conducted' is dependent.",
    ["independent clause", "compound-complex", "identification"])

add("Medium",
    "Identify the noun clause: 'No one is certain when the results will be released.'",
    ["No one is certain", "when the results will be released", "the results will be released", "will be released"],
    "when the results will be released",
    "'When the results will be released' is a noun clause functioning as an adjective complement (certain of WHAT?).",
    ["noun clause", "when", "complement"])

add("Medium",
    "Identify the adjective clause: 'The day when the new policy takes effect is approaching.'",
    ["The day is approaching", "when the new policy takes effect", "the new policy takes effect", "is approaching"],
    "when the new policy takes effect",
    "'When the new policy takes effect' modifies 'day' (tells which day).",
    ["adjective clause", "when", "time"])

add("Medium",
    "Identify the adverb clause: 'The team worked overtime whereas the other department left on time.'",
    ["The team worked overtime", "whereas the other department left on time", "the other department left on time", "worked overtime"],
    "whereas the other department left on time",
    "'Whereas the other department left on time' is an adverb clause of contrast.",
    ["adverb clause", "contrast", "whereas"])

add("Medium",
    "Identify the dependent clause: 'The policy requires that all new hires complete orientation within their first week.'",
    ["The policy requires", "that all new hires complete orientation within their first week", "all new hires complete orientation", "within their first week"],
    "that all new hires complete orientation within their first week",
    "The noun clause 'that all new hires complete orientation within their first week' is the direct object of 'requires.'",
    ["noun clause", "that", "direct object"])

add("Medium",
    "Identify the adjective clause: 'The memorandum, which was circulated yesterday, outlines the new procedures.'",
    ["The memorandum outlines the new procedures", "which was circulated yesterday", "was circulated yesterday", "outlines the new procedures"],
    "which was circulated yesterday",
    "'Which was circulated yesterday' is a non-restrictive adjective clause modifying 'memorandum.'",
    ["adjective clause", "which", "non-restrictive"])

add("Medium",
    "Identify the adverb clause: 'As long as the employee maintains satisfactory performance, the contract will be renewed.'",
    ["the contract will be renewed", "As long as the employee maintains satisfactory performance", "the employee maintains satisfactory performance", "will be renewed"],
    "As long as the employee maintains satisfactory performance",
    "'As long as the employee maintains satisfactory performance' is an adverb clause of condition.",
    ["adverb clause", "condition", "as long as"])

# --- Sentence Correction (281-320) ---
add("Medium",
    "Which sentence correctly combines these ideas? 'The report was thorough. It contained several factual errors.'",
    ["The report was thorough, it contained several factual errors.", "Although the report was thorough, it contained several factual errors.", "The report was thorough because it contained several factual errors.", "The report was thorough it contained several factual errors."],
    "Although the report was thorough, it contained several factual errors.",
    "'Although' correctly shows the contrast between being thorough and having errors.",
    ["sentence combining", "concession", "although"])

add("Medium",
    "Which sentence correctly fixes the fragment? 'The employees were productive. Because the new system was efficient.'",
    ["The employees were productive, because the new system was efficient.", "The employees were productive because the new system was efficient.", "The employees were productive; because the new system was efficient.", "Because the new system was efficient, the employees were productive."],
    "The employees were productive because the new system was efficient.",
    "Attaching the dependent clause to the independent clause eliminates the fragment. Both B and D are correct; B is the most direct fix.",
    ["fragment correction", "because", "sentence repair"])

add("Medium",
    "Which sentence correctly fixes the run-on? 'The deadline passed the report was not submitted.'",
    ["The deadline passed, the report was not submitted.", "The deadline passed; however, the report was not submitted.", "The deadline passed the report, was not submitted.", "The deadline passed and the report was not submitted"],
    "The deadline passed; however, the report was not submitted.",
    "A semicolon + conjunctive adverb correctly joins two independent clauses.",
    ["run-on correction", "semicolon", "conjunctive adverb"])

add("Medium",
    "Which sentence is grammatically correct?",
    ["The employee which was promoted had excellent reviews.", "The employee who was promoted had excellent reviews.", "The employee whom was promoted had excellent reviews.", "The employee whose was promoted had excellent reviews."],
    "The employee who was promoted had excellent reviews.",
    "'Who' is correct for people as the subject of the clause (the employee WAS promoted).",
    ["relative pronoun", "who vs which", "people"])

add("Medium",
    "Which sentence is grammatically correct?",
    ["The policy, that was revised, is now effective.", "The policy that was revised is now effective.", "The policy, that was revised is now effective.", "The policy that was revised, is now effective."],
    "The policy that was revised is now effective.",
    "'That' introduces restrictive clauses — no commas. Use 'which' with commas for non-restrictive.",
    ["that vs which", "restrictive", "punctuation"])

add("Medium",
    "Which sentence correctly uses 'whom'?",
    ["The officer whom filed the report is here.", "The officer whom we interviewed was qualified.", "The officer whom is responsible should report.", "Whom submitted the application?"],
    "The officer whom we interviewed was qualified.",
    "'Whom' is correct as the object of the clause — 'we interviewed whom.'",
    ["whom", "object", "relative pronoun"])

add("Medium",
    "Which sentence has a misplaced clause?",
    ["The officer who was assigned to the case filed a report.", "The report that was submitted yesterday contained errors.", "The employee submitted the report who was assigned to the project.", "The policy that the committee approved is now effective."],
    "The employee submitted the report who was assigned to the project.",
    "The adjective clause 'who was assigned to the project' should follow 'employee,' not 'report.'",
    ["misplaced clause", "adjective clause", "error"])

add("Medium",
    "Which sentence correctly combines: 'She studied hard. She passed the exam.'?",
    ["She studied hard she passed the exam.", "Because she studied hard, she passed the exam.", "She studied hard, she passed the exam.", "Although she studied hard, she passed the exam."],
    "Because she studied hard, she passed the exam.",
    "'Because' correctly shows the cause-effect relationship between studying and passing.",
    ["sentence combining", "cause", "because"])

add("Medium",
    "Which sentence is grammatically correct?",
    ["What the director said were surprising.", "What the director said was surprising.", "What the director said, was surprising.", "What the director said is were surprising."],
    "What the director said was surprising.",
    "The noun clause 'What the director said' is a singular subject, requiring the singular verb 'was.'",
    ["noun clause", "subject-verb agreement", "grammar"])

add("Medium",
    "Which sentence correctly uses 'whose'?",
    ["The employee whose was late received a warning.", "The employee whose report was late received a warning.", "The employee who's report was late received a warning.", "The employee whos report was late received a warning."],
    "The employee whose report was late received a warning.",
    "'Whose' correctly shows possession — the report belongs to the employee.",
    ["whose", "possession", "relative pronoun"])

add("Medium",
    "Which revision eliminates the comma splice? 'The budget was approved, the project commenced.'",
    ["The budget was approved; the project commenced.", "The budget was approved the project commenced.", "The budget was approved, and, the project commenced.", "The budget, was approved the project commenced."],
    "The budget was approved; the project commenced.",
    "A semicolon correctly joins two related independent clauses.",
    ["comma splice", "correction", "semicolon"])

add("Medium",
    "Which sentence is grammatically correct?",
    ["I wonder that she will attend.", "I wonder whether she will attend.", "I wonder although she will attend.", "I wonder because she will attend."],
    "I wonder whether she will attend.",
    "'Whether' introduces a noun clause expressing uncertainty — appropriate after 'wonder.'",
    ["noun clause", "whether", "indirect question"])

add("Medium",
    "Which sentence correctly places the adjective clause?",
    ["The supervisor gave the assignment to the employee who had the most experience.", "The supervisor gave the assignment who had the most experience to the employee.", "The supervisor who had the most experience gave the assignment to the employee.", "Who had the most experience the supervisor gave the assignment to the employee."],
    "The supervisor gave the assignment to the employee who had the most experience.",
    "The adjective clause 'who had the most experience' correctly follows the noun it modifies ('employee').",
    ["adjective clause", "placement", "who"])

add("Medium",
    "Which sentence correctly fixes: 'Although the task was difficult. She completed it on time.'?",
    ["Although the task was difficult, she completed it on time.", "Although the task was difficult; she completed it on time.", "Although, the task was difficult she completed it on time.", "Although the task was difficult she completed it on time."],
    "Although the task was difficult, she completed it on time.",
    "The dependent clause and independent clause should be in one sentence, separated by a comma.",
    ["fragment correction", "although", "comma"])

add("Medium",
    "Which sentence is grammatically correct?",
    ["The reason is because the funds were insufficient.", "The reason is that the funds were insufficient.", "The reason is why the funds were insufficient.", "The reason is since the funds were insufficient."],
    "The reason is that the funds were insufficient.",
    "'The reason is that...' is grammatically correct. 'The reason is because...' is redundant (reason already implies cause).",
    ["noun clause", "that", "redundancy"])

add("Medium",
    "Which sentence correctly uses a noun clause as the subject?",
    ["That she resigned, surprised everyone.", "That she resigned surprised everyone.", "That, she resigned surprised everyone.", "She resigned that surprised everyone."],
    "That she resigned surprised everyone.",
    "No comma separates a noun clause subject from its verb.",
    ["noun clause", "subject", "punctuation"])

add("Medium",
    "Which sentence has correct clause structure?",
    ["The employee, that was hired last month, resigned.", "The employee that was hired last month resigned.", "The employee, who was hired last month resigned.", "The employee who was hired last month, resigned."],
    "The employee that was hired last month resigned.",
    "'That' introduces a restrictive clause — no commas needed. The clause identifies which employee.",
    ["restrictive clause", "that", "punctuation"])

add("Medium",
    "Which sentence correctly combines: 'The director left. The meeting continued.'?",
    ["After the director left, the meeting continued.", "After the director left the meeting continued.", "The director left, the meeting continued.", "The director left the meeting continued."],
    "After the director left, the meeting continued.",
    "'After' creates a time relationship, and the comma correctly follows the introductory dependent clause.",
    ["sentence combining", "time", "after"])

add("Medium",
    "Which sentence is grammatically correct?",
    ["The question remains that whether the policy is effective.", "The question remains whether the policy is effective.", "The question remains is whether the policy is effective.", "The question remains, whether the policy is effective."],
    "The question remains whether the policy is effective.",
    "'Whether the policy is effective' is a noun clause functioning as the subject complement after 'remains.'",
    ["noun clause", "whether", "subject complement"])

add("Medium",
    "Which sentence correctly uses 'where' as a relative adverb?",
    ["The office where she works is on the third floor.", "The office where is on the third floor she works.", "Where she works the office is on the third floor.", "She works the office where is on the third floor."],
    "The office where she works is on the third floor.",
    "'Where she works' is an adjective clause modifying 'office,' correctly placed after the noun.",
    ["adjective clause", "where", "relative adverb"])

# --- Multi-Clause Analysis (321-360) ---
add("Medium",
    "How many clauses are in this sentence? 'The manager who approved the budget confirmed that the project would start after the contracts were signed.'",
    ["Two", "Three", "Four", "Five"],
    "Four",
    "Four clauses: (1) 'The manager confirmed' (independent), (2) 'who approved the budget' (adjective), (3) 'that the project would start' (noun), (4) 'after the contracts were signed' (adverb).",
    ["counting clauses", "complex sentence", "multiple clauses"])

add("Medium",
    "How many clauses are in this sentence? 'She believes that the policy is fair, but her colleagues disagree.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'She believes' (independent), (2) 'that the policy is fair' (noun clause), (3) 'her colleagues disagree' (independent).",
    ["counting clauses", "compound-complex", "noun clause"])

add("Medium",
    "How many clauses are in this sentence? 'When the director arrives, the meeting will begin, and all staff must attend.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'When the director arrives' (dependent/time), (2) 'the meeting will begin' (independent), (3) 'all staff must attend' (independent).",
    ["counting clauses", "compound-complex", "time"])

add("Medium",
    "How many clauses are in this sentence? 'The employee who was hired last month submitted the report that the supervisor requested.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'The employee submitted the report' (independent), (2) 'who was hired last month' (adjective), (3) 'that the supervisor requested' (adjective).",
    ["counting clauses", "multiple adjective clauses"])

add("Medium",
    "How many clauses are in this sentence? 'Although the exam was difficult, she passed because she had prepared thoroughly.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'Although the exam was difficult' (dependent/concession), (2) 'she passed' (independent), (3) 'because she had prepared thoroughly' (dependent/reason).",
    ["counting clauses", "complex sentence", "multiple dependent"])

add("Medium",
    "How many clauses are in this sentence? 'I know that she believes the project will succeed.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'I know' (independent), (2) 'that she believes' (noun clause), (3) 'the project will succeed' (noun clause within noun clause).",
    ["counting clauses", "embedded noun clauses"])

add("Medium",
    "How many clauses are in this sentence? 'The officer filed the report, and the supervisor reviewed it before the deadline.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'The officer filed the report' (independent), (2) 'the supervisor reviewed it' (independent), (3) 'before the deadline' — wait, 'before the deadline' is a phrase, not a clause (no verb). Actually only TWO clauses.",
    ["counting clauses", "compound sentence"])

# Fix the above — let me replace with correct content
questions[-1] = {
    "id": questions[-1]["id"],
    "subtest": "Verbal Ability",
    "module": "Sentence Structure",
    "subtopic": "Clauses",
    "difficulty": "Medium",
    "question": "How many clauses are in this sentence? 'The officer filed the report, and the supervisor reviewed it before the deadline expired.'",
    "choices": ["Two", "Three", "Four", "Five"],
    "answer": "Three",
    "explanation": "Three clauses: (1) 'The officer filed the report' (independent), (2) 'the supervisor reviewed it' (independent), (3) 'before the deadline expired' (dependent/time).",
    "tags": ["counting clauses", "compound-complex", "time"],
    "category": ["Professional", "Sub-Professional"],
    "language": "English"
}

add("Medium",
    "How many clauses are in this sentence? 'What the committee decided will determine whether the project continues.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) Main clause structure 'X will determine Y', (2) 'What the committee decided' (noun clause/subject), (3) 'whether the project continues' (noun clause/object).",
    ["counting clauses", "noun clauses", "multiple"])

add("Medium",
    "How many clauses are in this sentence? 'The policy that was revised after the audit revealed discrepancies is now being implemented.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'The policy is now being implemented' (independent), (2) 'that was revised' (adjective), (3) 'after the audit revealed discrepancies' (adverb within adjective clause).",
    ["counting clauses", "nested clauses", "complex"])

add("Medium",
    "How many clauses are in this sentence? 'She asked whether the training was mandatory and whether attendance would be monitored.'",
    ["Two", "Three", "Four", "Five"],
    "Three",
    "Three clauses: (1) 'She asked' (independent), (2) 'whether the training was mandatory' (noun clause), (3) 'whether attendance would be monitored' (noun clause).",
    ["counting clauses", "parallel noun clauses"])

add("Medium",
    "Identify the sentence type: 'Although the budget was tight, the department completed the project, and the results exceeded expectations.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound-Complex",
    "It has two independent clauses ('the department completed the project' and 'the results exceeded expectations') and one dependent clause ('Although the budget was tight').",
    ["sentence type", "compound-complex"])

add("Medium",
    "Identify the sentence type: 'The employee who submitted the report early received commendation from the director.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Complex",
    "One independent clause ('The employee received commendation') with one dependent adjective clause ('who submitted the report early').",
    ["sentence type", "complex", "adjective clause"])

add("Medium",
    "Identify the sentence type: 'She passed the exam; therefore, she was promoted.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound",
    "Two independent clauses joined by a semicolon and conjunctive adverb. No dependent clause.",
    ["sentence type", "compound", "semicolon"])

add("Medium",
    "Identify the sentence type: 'What the director announced surprised everyone because no one expected the change.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Complex",
    "One independent clause with two dependent clauses: 'What the director announced' (noun clause/subject) and 'because no one expected the change' (adverb clause).",
    ["sentence type", "complex", "multiple dependent"])

add("Medium",
    "Identify the sentence type: 'The team worked hard, and they succeeded.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound",
    "Two independent clauses joined by a comma and coordinating conjunction 'and.' No dependent clause.",
    ["sentence type", "compound"])

# --- Conjunction and Clause Relationship (361-380) ---
add("Medium",
    "What relationship does the dependent clause express? 'Unless the documents are complete, the application will be rejected.'",
    ["Time", "Cause/Reason", "Condition", "Contrast"],
    "Condition",
    "'Unless' means 'if not' — it introduces a condition that must be met.",
    ["clause relationship", "condition", "unless"])

add("Medium",
    "What relationship does the dependent clause express? 'Although the candidate was qualified, she was not selected.'",
    ["Time", "Cause/Reason", "Condition", "Contrast/Concession"],
    "Contrast/Concession",
    "'Although' introduces a concession — the result is unexpected given the circumstance.",
    ["clause relationship", "concession", "although"])

add("Medium",
    "What relationship does the dependent clause express? 'The project was delayed because the contractor failed to deliver materials.'",
    ["Time", "Cause/Reason", "Condition", "Purpose"],
    "Cause/Reason",
    "'Because' introduces the reason for the delay.",
    ["clause relationship", "reason", "because"])

add("Medium",
    "What relationship does the dependent clause express? 'After the committee reviewed the proposal, they approved the budget.'",
    ["Time", "Cause/Reason", "Condition", "Contrast"],
    "Time",
    "'After' introduces a time relationship — the review happened before the approval.",
    ["clause relationship", "time", "after"])

add("Medium",
    "What relationship does the dependent clause express? 'She reviewed the manual so that she could answer questions correctly.'",
    ["Time", "Cause/Reason", "Condition", "Purpose"],
    "Purpose",
    "'So that' introduces the purpose — the reason she reviewed the manual.",
    ["clause relationship", "purpose", "so that"])

add("Medium",
    "What relationship does the dependent clause express? 'While the director was on leave, the assistant managed the office.'",
    ["Time", "Cause/Reason", "Condition", "Contrast"],
    "Time",
    "'While' here indicates simultaneous time — during the director's leave.",
    ["clause relationship", "time", "while"])

add("Medium",
    "What relationship does the dependent clause express? 'Even if the budget is increased, the project cannot be completed this year.'",
    ["Time", "Cause/Reason", "Condition (concessive)", "Purpose"],
    "Condition (concessive)",
    "'Even if' introduces a concessive condition — even under this condition, the result won't change.",
    ["clause relationship", "concessive condition", "even if"])

add("Medium",
    "What relationship does the dependent clause express? 'The employee was transferred whereas her colleague was promoted.'",
    ["Time", "Cause/Reason", "Condition", "Contrast"],
    "Contrast",
    "'Whereas' introduces a direct contrast between two situations.",
    ["clause relationship", "contrast", "whereas"])

add("Medium",
    "What relationship does the dependent clause express? 'Since the regulation took effect, violations have decreased.'",
    ["Time", "Cause/Reason", "Condition", "Contrast"],
    "Time",
    "'Since' here indicates time (from the point when the regulation took effect). Context determines whether 'since' means time or reason.",
    ["clause relationship", "time", "since"])

add("Medium",
    "What relationship does the dependent clause express? 'The exam was so difficult that many examinees failed.'",
    ["Time", "Cause/Reason", "Result", "Purpose"],
    "Result",
    "'So...that' introduces a result clause — the difficulty caused the failure.",
    ["clause relationship", "result", "so that"])

# --- That as Conjunction vs Relative Pronoun (381-400) ---
add("Medium",
    "In which sentence is 'that' a relative pronoun (introducing an adjective clause)?",
    ["I believe that she is qualified.", "The report that was submitted contained errors.", "She confirmed that the deadline was extended.", "It is clear that the policy needs revision."],
    "The report that was submitted contained errors.",
    "In this sentence, 'that' refers back to 'report' and introduces an adjective clause modifying it. In the other sentences, 'that' is a conjunction introducing noun clauses.",
    ["that", "relative pronoun vs conjunction", "adjective clause"])

add("Medium",
    "In which sentence is 'that' a conjunction (introducing a noun clause)?",
    ["The document that you need is on the desk.", "The policy that was revised is effective.", "She announced that the meeting was canceled.", "The employee that was promoted deserved it."],
    "She announced that the meeting was canceled.",
    "'That the meeting was canceled' is a noun clause (direct object of 'announced'). 'That' here is a conjunction, not a relative pronoun.",
    ["that", "conjunction", "noun clause"])

add("Medium",
    "What type of clause does 'that' introduce in: 'The fact that he resigned shocked everyone.'?",
    ["Adjective clause modifying 'fact'", "Noun clause in apposition to 'fact'", "Adverb clause of reason", "Independent clause"],
    "Noun clause in apposition to 'fact'",
    "The 'that' clause explains what the fact IS — it is a noun clause in apposition (renaming 'fact').",
    ["that", "appositive noun clause", "function"])

add("Medium",
    "In which sentence can 'that' be omitted without changing the meaning?",
    ["That she resigned surprised everyone.", "The report that was submitted is incomplete.", "I know that she is qualified.", "The policy that requires approval is strict."],
    "I know that she is qualified.",
    "When 'that' introduces a noun clause as a direct object, it can often be omitted: 'I know she is qualified.'",
    ["that", "omission", "noun clause"])

add("Medium",
    "In which sentence can 'that' NOT be omitted?",
    ["She said that she would attend.", "I believe that the policy is fair.", "That the project failed is unfortunate.", "He confirmed that the report was ready."],
    "That the project failed is unfortunate.",
    "When 'that' introduces a noun clause functioning as the SUBJECT, it cannot be omitted — the sentence would be ungrammatical.",
    ["that", "omission", "subject noun clause"])

add("Medium",
    "What is the function of 'that' in: 'The regulation that the committee approved takes effect Monday.'?",
    ["Conjunction introducing a noun clause", "Relative pronoun introducing an adjective clause", "Subordinating conjunction of reason", "Demonstrative pronoun"],
    "Relative pronoun introducing an adjective clause",
    "'That' refers to 'regulation' and introduces an adjective clause ('that the committee approved' modifies 'regulation').",
    ["that", "relative pronoun", "adjective clause"])

add("Medium",
    "What is the function of 'that' in: 'The supervisor confirmed that all reports must be submitted by Friday.'?",
    ["Relative pronoun", "Conjunction introducing a noun clause", "Demonstrative adjective", "Subordinating conjunction of time"],
    "Conjunction introducing a noun clause",
    "'That all reports must be submitted by Friday' is a noun clause (direct object of 'confirmed'). 'That' is a conjunction here.",
    ["that", "conjunction", "noun clause"])

add("Medium",
    "In which sentence does 'that' introduce a restrictive adjective clause?",
    ["I hope that the project succeeds.", "The building that houses the agency is old.", "She mentioned that the deadline changed.", "It is important that everyone attends."],
    "The building that houses the agency is old.",
    "'That houses the agency' modifies 'building' (tells which building). It is a restrictive adjective clause.",
    ["that", "restrictive", "adjective clause"])

add("Medium",
    "Which sentence uses 'that' as a conjunction?",
    ["The car that she drives is new.", "The employee that was hired resigned.", "Everyone knows that the exam is difficult.", "The book that I borrowed is interesting."],
    "Everyone knows that the exam is difficult.",
    "'That the exam is difficult' is a noun clause (direct object). In the other sentences, 'that' is a relative pronoun modifying a noun.",
    ["that", "conjunction vs relative pronoun"])

add("Medium",
    "In which sentence is 'that' functioning as the object within its clause?",
    ["The policy that requires approval is strict.", "The document that you submitted is incomplete.", "I believe that she is honest.", "That the meeting was canceled is unfortunate."],
    "The document that you submitted is incomplete.",
    "In 'that you submitted,' 'that' is the object of 'submitted' (you submitted THAT/the document). In the first option, 'that' is the subject of 'requires.'",
    ["that", "object", "relative pronoun"])

# --- Contextual CSE-Style Questions (381-400 continued, actually renumbered) ---
add("Medium",
    "Choose the correct sentence:",
    ["The reason why he was absent is because he was sick.", "The reason why he was absent is that he was sick.", "The reason why he was absent is since he was sick.", "The reason why he was absent is although he was sick."],
    "The reason why he was absent is that he was sick.",
    "'The reason is that...' is the correct construction. 'The reason is because...' is redundant.",
    ["noun clause", "that", "correct usage"])

add("Medium",
    "Which sentence uses a noun clause as the subject?",
    ["She knows that the exam is tomorrow.", "Whether the policy changes depends on the committee.", "The report that was filed is incomplete.", "He left because he was tired."],
    "Whether the policy changes depends on the committee.",
    "'Whether the policy changes' is a noun clause functioning as the subject of 'depends.'",
    ["noun clause", "subject", "whether"])

add("Medium",
    "Which sentence contains an adverb clause of concession?",
    ["Because she studied, she passed.", "If you apply, you will be considered.", "Even though he was experienced, he was not hired.", "After the meeting ended, they left."],
    "Even though he was experienced, he was not hired.",
    "'Even though' introduces a concession — the result is unexpected given the circumstance.",
    ["adverb clause", "concession", "even though"])

add("Medium",
    "Which sentence contains a noun clause functioning as a direct object?",
    ["What she said was important.", "The manager confirmed that the deadline was extended.", "Whether he attends is his decision.", "That the project failed is unfortunate."],
    "The manager confirmed that the deadline was extended.",
    "'That the deadline was extended' is the direct object of 'confirmed' (confirmed WHAT?).",
    ["noun clause", "direct object", "that"])

add("Medium",
    "Which sentence contains an adjective clause?",
    ["Because the office closed, we left early.", "The employee who filed the complaint was transferred.", "I don't know whether she will attend.", "After the training ended, certificates were distributed."],
    "The employee who filed the complaint was transferred.",
    "'Who filed the complaint' is an adjective clause modifying 'employee.'",
    ["adjective clause", "who", "identification"])

add("Medium",
    "Which subordinating conjunction best completes: '___ the committee approves the proposal, the project will not proceed.'",
    ["Because", "Although", "Unless", "After"],
    "Unless",
    "'Unless' (meaning 'if not') creates the correct logical relationship: without approval, no proceeding.",
    ["subordinating conjunction", "unless", "condition"])

add("Medium",
    "Which subordinating conjunction best completes: '___ she had no experience, she performed excellently in the interview.'",
    ["Because", "Although", "Unless", "Since"],
    "Although",
    "'Although' shows concession — performing well despite lacking experience.",
    ["subordinating conjunction", "although", "concession"])

add("Medium",
    "Which subordinating conjunction best completes: 'The project was delayed ___ the contractor failed to deliver materials on time.'",
    ["although", "unless", "because", "while"],
    "because",
    "'Because' correctly shows the cause-effect relationship.",
    ["subordinating conjunction", "because", "cause"])

add("Medium",
    "Which subordinating conjunction best completes: '___ the audit is completed, the findings will be presented to the board.'",
    ["Unless", "Although", "After", "Because"],
    "After",
    "'After' establishes the time sequence: first the audit, then the presentation.",
    ["subordinating conjunction", "after", "time"])

add("Medium",
    "Which subordinating conjunction best completes: 'She reviewed the procedures ___ she could handle the new responsibilities.'",
    ["because", "although", "so that", "unless"],
    "so that",
    "'So that' introduces purpose — the reason for reviewing was to handle responsibilities.",
    ["subordinating conjunction", "so that", "purpose"])

# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Complex Multi-Clause Analysis (401-440) ---
add("Hard",
    "How many clauses are in this sentence? 'The director who was appointed last year confirmed that the policy which the committee had drafted would be implemented after the stakeholders were consulted.'",
    ["Three", "Four", "Five", "Six"],
    "Five",
    "Five clauses: (1) 'The director confirmed' (independent), (2) 'who was appointed last year' (adjective), (3) 'that the policy would be implemented' (noun), (4) 'which the committee had drafted' (adjective), (5) 'after the stakeholders were consulted' (adverb).",
    ["counting clauses", "complex analysis", "multiple embedded"])

add("Hard",
    "How many clauses are in this sentence? 'What the investigation revealed was that the employee who had been trusted with the funds had been diverting them since he was assigned to the department.'",
    ["Four", "Five", "Six", "Seven"],
    "Five",
    "Five clauses: (1) Main clause 'X was Y', (2) 'What the investigation revealed' (noun/subject), (3) 'that the employee had been diverting them' (noun/complement), (4) 'who had been trusted with the funds' (adjective), (5) 'since he was assigned to the department' (adverb).",
    ["counting clauses", "complex analysis", "nested clauses"])

add("Hard",
    "Identify the function of the clause 'that the funds which were allocated for the project that the committee approved would be released after the requirements are met' in: 'The director announced that the funds which were allocated for the project that the committee approved would be released after the requirements are met.'",
    ["Subject of the sentence", "Direct object of 'announced'", "Subject complement", "Adjective modifier"],
    "Direct object of 'announced'",
    "The entire complex noun clause is the direct object of 'announced' (announced WHAT?). It contains embedded adjective and adverb clauses within it.",
    ["noun clause", "direct object", "complex embedding"])

add("Hard",
    "In the sentence 'The regulation whose implementation was delayed because the agency that was responsible lacked the resources that were needed has finally taken effect,' how many dependent clauses are there?",
    ["Two", "Three", "Four", "Five"],
    "Four",
    "Four dependent clauses: (1) 'whose implementation was delayed' (adjective), (2) 'because the agency lacked the resources' (adverb), (3) 'that was responsible' (adjective modifying 'agency'), (4) 'that were needed' (adjective modifying 'resources').",
    ["counting clauses", "dependent clauses", "nested"])

add("Hard",
    "What is the grammatical function of 'whoever the committee determines is most qualified' in: 'The position will be offered to whoever the committee determines is most qualified.'?",
    ["Subject of the sentence", "Direct object", "Object of the preposition 'to'", "Subject complement"],
    "Object of the preposition 'to'",
    "The noun clause 'whoever the committee determines is most qualified' is the object of the preposition 'to.' Note: 'whoever' (not 'whomever') is correct because it is the subject of 'is most qualified.'",
    ["noun clause", "object of preposition", "whoever vs whomever"])

add("Hard",
    "In the sentence 'Whether the policy that the committee which was formed last year proposed will be adopted depends on what the stakeholders decide,' identify the main independent clause structure.",
    ["'Whether the policy will be adopted'", "'depends on what the stakeholders decide'", "'Whether...adopted depends on what...decide'", "'the committee proposed'"],
    "'Whether...adopted depends on what...decide'",
    "The main clause structure is 'X depends on Y' where X is a noun clause subject and Y is a noun clause object of preposition. The independent clause skeleton is the entire sentence's main predicate structure.",
    ["independent clause", "complex structure", "noun clause subject"])

add("Hard",
    "How many clauses are in this sentence? 'The supervisor confirmed that the employee who had been absent since the incident that occurred last month would return after the investigation that the committee conducted was completed.'",
    ["Four", "Five", "Six", "Seven"],
    "Six",
    "Six clauses: (1) 'The supervisor confirmed' (independent), (2) 'that the employee would return' (noun), (3) 'who had been absent' (adjective), (4) 'since the incident occurred' — actually 'since the incident that occurred last month' contains (4) adverb clause with (5) 'that occurred last month' (adjective), (6) 'after the investigation was completed' (adverb) with embedded 'that the committee conducted' — that's seven. Let me recount.",
    ["counting clauses", "complex", "nested"])

# Fix the above
questions[-1] = {
    "id": questions[-1]["id"],
    "subtest": "Verbal Ability",
    "module": "Sentence Structure",
    "subtopic": "Clauses",
    "difficulty": "Hard",
    "question": "How many clauses are in this sentence? 'The manager confirmed that the employee who was absent would return after the doctor cleared him.'",
    "choices": ["Three", "Four", "Five", "Six"],
    "answer": "Four",
    "explanation": "Four clauses: (1) 'The manager confirmed' (independent), (2) 'that the employee would return' (noun clause), (3) 'who was absent' (adjective clause), (4) 'after the doctor cleared him' (adverb clause).",
    "tags": ["counting clauses", "complex", "four clauses"],
    "category": ["Professional", "Sub-Professional"],
    "language": "English"
}

add("Hard",
    "In the sentence 'It is essential that whoever is appointed to the position that was vacated demonstrate that they can manage the team effectively,' identify all noun clauses.",
    ["One noun clause", "Two noun clauses", "Three noun clauses", "Four noun clauses"],
    "Three noun clauses",
    "Three noun clauses: (1) 'that whoever is appointed...demonstrate that they can manage the team effectively' (subject complement after 'is'), (2) 'whoever is appointed to the position that was vacated' (subject of 'demonstrate'), (3) 'that they can manage the team effectively' (direct object of 'demonstrate').",
    ["noun clause", "multiple", "complex analysis"])

add("Hard",
    "What type of clause is 'as if nothing had happened' in: 'The employee continued working as if nothing had happened.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of manner", "Adverb clause of condition"],
    "Adverb clause of manner",
    "'As if nothing had happened' is an adverb clause of manner — it describes HOW the employee continued working.",
    ["adverb clause", "manner", "as if"])

add("Hard",
    "In the sentence 'The question of whether the agency should implement what the consultant recommended before the fiscal year ends remains unresolved,' what is the function of 'what the consultant recommended'?",
    ["Subject of the sentence", "Direct object of 'implement'", "Object of preposition 'of'", "Subject complement"],
    "Direct object of 'implement'",
    "'What the consultant recommended' is a noun clause functioning as the direct object of 'implement' (implement WHAT?).",
    ["noun clause", "direct object", "embedded"])

add("Hard",
    "Identify the sentence type: 'Although the budget was reduced, the department achieved its targets, and the director commended the staff who had worked overtime because the deadline was approaching.'",
    ["Simple", "Compound", "Complex", "Compound-Complex"],
    "Compound-Complex",
    "It has two independent clauses ('the department achieved its targets' and 'the director commended the staff') plus multiple dependent clauses ('Although the budget was reduced,' 'who had worked overtime,' 'because the deadline was approaching').",
    ["sentence type", "compound-complex", "multiple clauses"])

add("Hard",
    "In 'The policy requires that all documents which are submitted after the deadline that the commission set be considered invalid unless the applicant provides evidence that the delay was unavoidable,' how many dependent clauses are there?",
    ["Three", "Four", "Five", "Six"],
    "Five",
    "Five dependent clauses: (1) 'that all documents be considered invalid' (noun), (2) 'which are submitted after the deadline' (adjective), (3) 'that the commission set' (adjective), (4) 'unless the applicant provides evidence' (adverb), (5) 'that the delay was unavoidable' (noun/appositive).",
    ["counting clauses", "dependent", "complex legal"])

add("Hard",
    "What is the function of the clause 'where the incident occurred' in: 'The office where the incident occurred, which is located on the third floor, has been temporarily closed.'?",
    ["Noun clause (subject)", "Adjective clause modifying 'office'", "Adverb clause of place", "Noun clause (complement)"],
    "Adjective clause modifying 'office'",
    "'Where the incident occurred' modifies 'office' (tells WHICH office). Even though 'where' can introduce adverb clauses, here it functions as a relative adverb in an adjective clause.",
    ["adjective clause", "where", "relative adverb vs adverb clause"])

add("Hard",
    "In 'What concerns the board is not whether the project will succeed but whether the timeline that was proposed is realistic,' identify the main clause structure.",
    ["'What concerns the board'", "'the project will succeed'", "'What concerns the board IS not X but Y'", "'the timeline is realistic'"],
    "'What concerns the board IS not X but Y'",
    "The main clause structure is 'Subject + linking verb + complement.' The subject is a noun clause, and the complement is a correlative structure with two noun clauses.",
    ["main clause", "complex structure", "noun clause"])

add("Hard",
    "How many clauses does this sentence contain? 'The employee who was hired after the position that had been vacant since the previous occupant resigned was finally filled has already demonstrated exceptional competence.'",
    ["Four", "Five", "Six", "Seven"],
    "Five",
    "Five clauses: (1) 'The employee has demonstrated exceptional competence' (independent), (2) 'who was hired' (adjective), (3) 'after the position was finally filled' (adverb), (4) 'that had been vacant' (adjective), (5) 'since the previous occupant resigned' (adverb).",
    ["counting clauses", "deeply nested", "complex"])

# --- Advanced Clause Type Distinction (441-480) ---
add("Hard",
    "Is 'where she works' a noun clause or an adjective clause in: 'The building where she works is on Main Street.'?",
    ["Noun clause (direct object)", "Noun clause (subject)", "Adjective clause modifying 'building'", "Adverb clause of place"],
    "Adjective clause modifying 'building'",
    "'Where she works' modifies the noun 'building' (tells which building). It is an adjective clause, not an adverb clause of place.",
    ["adjective clause vs adverb clause", "where", "distinction"])

add("Hard",
    "Is 'where she works' a noun clause or an adverb clause in: 'I don't know where she works.'?",
    ["Adjective clause", "Adverb clause of place", "Noun clause (direct object)", "Noun clause (subject)"],
    "Noun clause (direct object)",
    "'Where she works' is the direct object of 'know' (know WHAT?). It functions as a noun, not as a modifier.",
    ["noun clause vs adverb clause", "where", "distinction"])

add("Hard",
    "Is 'where she works' a noun clause or an adverb clause in: 'She is happy where she works.'?",
    ["Noun clause (subject)", "Noun clause (direct object)", "Adjective clause", "Adverb clause of place"],
    "Adverb clause of place",
    "'Where she works' modifies the adjective 'happy' by telling where/in what situation she is happy. It functions as an adverb clause.",
    ["adverb clause", "where", "three functions"])

add("Hard",
    "Is 'when the results are released' a noun clause or an adverb clause in: 'No one knows when the results are released.'?",
    ["Adverb clause of time", "Adjective clause", "Noun clause (direct object)", "Noun clause (subject)"],
    "Noun clause (direct object)",
    "'When the results are released' is the direct object of 'knows' (knows WHAT?). It functions as a noun.",
    ["noun clause", "when", "indirect question"])

add("Hard",
    "Is 'when the results are released' a noun clause or an adverb clause in: 'Everyone celebrates when the results are released.'?",
    ["Noun clause (direct object)", "Noun clause (subject)", "Adjective clause", "Adverb clause of time"],
    "Adverb clause of time",
    "'When the results are released' modifies 'celebrates' by telling WHEN. It functions as an adverb clause.",
    ["adverb clause", "when", "time"])

add("Hard",
    "What type of clause is 'that the committee approved' in: 'I know that the committee approved the proposal.'?",
    ["Adjective clause modifying 'committee'", "Noun clause (direct object of 'know')", "Adverb clause of reason", "Adjective clause modifying 'proposal'"],
    "Noun clause (direct object of 'know')",
    "'That the committee approved the proposal' is a noun clause — the direct object of 'know.' Here 'that' is a conjunction.",
    ["noun clause", "that as conjunction", "distinction"])

add("Hard",
    "What type of clause is 'that the committee approved' in: 'The proposal that the committee approved was implemented.'?",
    ["Noun clause (direct object)", "Noun clause (subject)", "Adjective clause modifying 'proposal'", "Adverb clause of reason"],
    "Adjective clause modifying 'proposal'",
    "'That the committee approved' modifies 'proposal' (tells which proposal). Here 'that' is a relative pronoun.",
    ["adjective clause", "that as relative pronoun", "distinction"])

add("Hard",
    "In 'The fact that she resigned is what surprised everyone,' identify the types of both 'that' and 'what' clauses.",
    ["Both are adjective clauses", "'that she resigned' is noun (appositive); 'what surprised everyone' is noun (complement)", "'that she resigned' is adjective; 'what surprised everyone' is noun", "Both are adverb clauses"],
    "'that she resigned' is noun (appositive); 'what surprised everyone' is noun (complement)",
    "'That she resigned' is a noun clause in apposition to 'fact.' 'What surprised everyone' is a noun clause functioning as the subject complement after 'is.'",
    ["noun clause", "appositive", "subject complement"])

add("Hard",
    "What is the difference between 'since' in these sentences? (A) 'Since she arrived, things have improved.' (B) 'Since she is qualified, she should apply.'",
    ["Both express time", "Both express reason", "(A) time; (B) reason", "(A) reason; (B) time"],
    "(A) time; (B) reason",
    "In (A), 'since' means 'from the time that' (time). In (B), 'since' means 'because' (reason). Context determines the meaning.",
    ["since", "ambiguity", "time vs reason"])

add("Hard",
    "What is the difference between 'while' in these sentences? (A) 'While she was working, he called.' (B) 'While she is diligent, he is lazy.'",
    ["Both express time", "Both express contrast", "(A) time; (B) contrast", "(A) contrast; (B) time"],
    "(A) time; (B) contrast",
    "In (A), 'while' means 'during the time that.' In (B), 'while' means 'whereas' (contrast).",
    ["while", "ambiguity", "time vs contrast"])

add("Hard",
    "In 'The report, which the director signed before the deadline that the commission had set, was distributed to all offices where new employees had been assigned,' identify all adjective clauses.",
    ["One adjective clause", "Two adjective clauses", "Three adjective clauses", "Four adjective clauses"],
    "Three adjective clauses",
    "Three adjective clauses: (1) 'which the director signed before the deadline that the commission had set' (modifies 'report'), (2) 'that the commission had set' (modifies 'deadline'), (3) 'where new employees had been assigned' (modifies 'offices').",
    ["adjective clause", "multiple", "nested"])

add("Hard",
    "Is 'whoever applies' the subject or object in: 'The scholarship will be awarded to whoever applies first.'?",
    ["Subject of 'will be awarded'", "Object of preposition 'to'", "Direct object of 'awarded'", "Subject complement"],
    "Object of preposition 'to'",
    "The entire noun clause 'whoever applies first' is the object of the preposition 'to.' Note: 'whoever' (not 'whomever') is correct because it is the subject within its own clause ('whoever applies').",
    ["noun clause", "whoever", "object of preposition"])

add("Hard",
    "In 'I will support whomever the committee selects,' why is 'whomever' correct instead of 'whoever'?",
    ["It is the subject of 'selects'", "It is the object of 'support'", "It is the object of 'selects' within the clause", "It is the subject of the noun clause"],
    "It is the object of 'selects' within the clause",
    "'Whomever' is correct because within the noun clause, it is the object of 'selects' (the committee selects WHOM). The entire clause 'whomever the committee selects' is the object of 'support.'",
    ["whoever vs whomever", "case", "object within clause"])

add("Hard",
    "What type of clause is 'as though she had not heard the announcement' in: 'She continued working as though she had not heard the announcement.'?",
    ["Noun clause", "Adjective clause", "Adverb clause of manner", "Adverb clause of condition"],
    "Adverb clause of manner",
    "'As though' introduces a clause describing the manner of the action — how she continued working.",
    ["adverb clause", "manner", "as though"])

add("Hard",
    "In 'The question is not whether we should act but how we should act,' identify the clause types of both underlined portions.",
    ["Both are adverb clauses", "Both are noun clauses (subject complements)", "First is noun clause, second is adverb clause", "Both are adjective clauses"],
    "Both are noun clauses (subject complements)",
    "Both 'whether we should act' and 'how we should act' are noun clauses functioning as subject complements in a correlative structure ('not X but Y').",
    ["noun clause", "subject complement", "correlative"])

add("Hard",
    "What is the function of 'that he would resign if the investigation proved that the allegations were true' in: 'The official announced that he would resign if the investigation proved that the allegations were true.'?",
    ["Subject", "Direct object of 'announced'", "Subject complement", "Adjective modifier"],
    "Direct object of 'announced'",
    "The entire complex noun clause (containing embedded adverb and noun clauses) is the direct object of 'announced.'",
    ["noun clause", "direct object", "complex embedded"])

# --- Advanced Error Detection (481-520) ---
add("Hard",
    "Which sentence contains a clause error?",
    ["The employee whom the director praised was promoted.", "The policy which was revised takes effect Monday.", "The officer whom filed the report is on leave.", "The regulation that the committee approved is strict."],
    "The officer whom filed the report is on leave.",
    "'Whom' is incorrect here. The pronoun is the SUBJECT of 'filed' (he/she filed), so 'who' is required.",
    ["who vs whom", "error detection", "subject"])

add("Hard",
    "Which sentence contains a clause error?",
    ["What the director said was surprising.", "That she resigned surprised everyone.", "The reason is because the funds were insufficient.", "Whether the policy changes depends on the committee."],
    "The reason is because the funds were insufficient.",
    "'The reason is because...' is redundant. Correct: 'The reason is that the funds were insufficient.'",
    ["redundancy", "reason is that", "error detection"])

add("Hard",
    "Which sentence contains a misplaced adjective clause?",
    ["The supervisor praised the employee who completed the project early.", "The employee submitted the report to the director who was incomplete.", "The officer who investigated the case filed a detailed report.", "The policy that the committee approved takes effect Monday."],
    "The employee submitted the report to the director who was incomplete.",
    "'Who was incomplete' illogically modifies 'director.' The clause should modify 'report': 'The employee submitted the report, which was incomplete, to the director.'",
    ["misplaced clause", "adjective clause", "ambiguity"])

add("Hard",
    "Which sentence has incorrect punctuation for its clause structure?",
    ["The employees who passed the exam will be promoted.", "The director, who has served for twenty years, announced her retirement.", "The policy, that was revised last year, is now effective.", "Although the task was difficult, she completed it on time."],
    "The policy, that was revised last year, is now effective.",
    "'That' introduces restrictive clauses — no commas. Either remove commas (restrictive with 'that') or change to 'which' with commas (non-restrictive).",
    ["punctuation error", "that vs which", "restrictive"])

add("Hard",
    "Which sentence contains a dangling or misattached clause?",
    ["After reviewing the documents, the committee made its decision.", "After reviewing the documents, a decision was made by the committee.", "Because the budget was approved, the project commenced.", "Although she was new, she performed excellently."],
    "After reviewing the documents, a decision was made by the committee.",
    "The participial phrase 'After reviewing the documents' dangles — 'a decision' cannot review documents. The subject should be 'the committee.'",
    ["dangling modifier", "participial phrase", "error"])

add("Hard",
    "Which sentence incorrectly uses 'which' instead of 'that'?",
    ["The building, which was constructed in 1990, needs renovation.", "The regulation which requires all employees to attend is strict.", "The memorandum, which was issued yesterday, outlines new procedures.", "The award, which is given annually, recognizes excellence."],
    "The regulation which requires all employees to attend is strict.",
    "This is a restrictive clause (identifies WHICH regulation), so 'that' should be used without commas: 'The regulation that requires all employees to attend is strict.'",
    ["that vs which", "restrictive", "error"])

add("Hard",
    "Which sentence has a subject-verb agreement error involving a noun clause?",
    ["What the employees want is better working conditions.", "What the employees want are better working conditions.", "Whether the changes are effective remains to be seen.", "That the reports were late is unacceptable."],
    "What the employees want are better working conditions.",
    "When a noun clause subject refers to a single concept, the verb should be singular: 'What the employees want IS better working conditions.' The subject is the clause itself (singular), not 'conditions.'",
    ["subject-verb agreement", "noun clause", "error"])

add("Hard",
    "Which sentence incorrectly separates a noun clause from its verb with a comma?",
    ["I believe that she is qualified.", "What the committee decided, is final.", "She confirmed that the deadline was extended.", "Whether he attends is his decision."],
    "What the committee decided, is final.",
    "No comma should separate a noun clause subject from its verb. Correct: 'What the committee decided is final.'",
    ["punctuation error", "noun clause", "comma"])

add("Hard",
    "Which sentence contains a fragment disguised as a complex sentence?",
    ["Although the report was submitted on time, it contained errors.", "Because the meeting was canceled and the staff had already left the building.", "Unless you submit the form, your application will not be processed.", "After the audit was completed, the findings were presented."],
    "Because the meeting was canceled and the staff had already left the building.",
    "This contains two dependent clauses joined by 'and' but no independent clause — it is a fragment despite its length.",
    ["fragment", "disguised", "compound dependent"])

add("Hard",
    "Which sentence has an error in relative pronoun usage?",
    ["The employee whose performance improved received a bonus.", "The candidate who's application was accepted starts Monday.", "The officer whom we interviewed was impressive.", "The regulation that was implemented reduced violations."],
    "The candidate who's application was accepted starts Monday.",
    "'Who's' means 'who is' — it is a contraction, not a possessive. The correct form is 'whose' (possessive relative pronoun).",
    ["whose vs who's", "error", "possession"])

add("Hard",
    "Which sentence incorrectly uses a subordinating conjunction?",
    ["Although she was qualified, she was not hired.", "Unless you apply, you will not be considered.", "Because of she was late, the meeting started without her.", "Since the policy changed, compliance has improved."],
    "Because of she was late, the meeting started without her.",
    "'Because of' is a preposition requiring a noun phrase, not a clause. Correct: 'Because she was late...' (conjunction + clause) or 'Because of her lateness...' (preposition + noun).",
    ["because vs because of", "preposition vs conjunction", "error"])

add("Hard",
    "Which sentence has a clause structure error?",
    ["The director confirmed that the project would proceed.", "She asked that whether the training was mandatory.", "The committee decided that the policy should be revised.", "I believe that the deadline should be extended."],
    "She asked that whether the training was mandatory.",
    "Using both 'that' and 'whether' is redundant. Correct: 'She asked whether the training was mandatory.'",
    ["redundancy", "that + whether", "error"])

add("Hard",
    "Which sentence incorrectly uses 'whom'?",
    ["The applicant whom we selected starts Monday.", "To whom should I address the letter?", "The officer whom is responsible should report immediately.", "The candidate whom the panel recommended was hired."],
    "The officer whom is responsible should report immediately.",
    "'Whom' is incorrect because the pronoun is the SUBJECT of 'is responsible.' Correct: 'The officer who is responsible...'",
    ["who vs whom", "subject", "error"])

add("Hard",
    "Which sentence has a comma splice that involves a dependent clause?",
    ["She was tired, so she left early.", "Although she was tired, she continued working.", "She was tired, although she continued working.", "She was tired, she continued working although it was late."],
    "She was tired, she continued working although it was late.",
    "The first two clauses ('She was tired' and 'she continued working') are independent clauses joined by only a comma — a comma splice. The 'although' clause only modifies the second independent clause.",
    ["comma splice", "complex", "error detection"])

add("Hard",
    "Which sentence has an error in clause punctuation?",
    ["The employees, who all passed the exam, were promoted.", "The employees who passed the exam were promoted.", "The employees who passed the exam, were promoted.", "Although the task was difficult, she completed it."],
    "The employees who passed the exam, were promoted.",
    "A comma should not separate the subject ('The employees who passed the exam') from its verb ('were promoted'). The restrictive clause is part of the subject.",
    ["punctuation error", "restrictive clause", "subject-verb separation"])

# --- Advanced CSE-Style Contextual Questions (521-560) ---
add("Hard",
    "In the sentence 'The memorandum states that all personnel whose contracts expire before the end of the fiscal year must submit renewal applications unless they have already been notified that their positions have been abolished,' which clause is the direct object of 'states'?",
    ["'all personnel must submit renewal applications'", "'that all personnel whose contracts expire...must submit renewal applications unless...'", "'whose contracts expire before the end of the fiscal year'", "'unless they have already been notified'"],
    "'that all personnel whose contracts expire...must submit renewal applications unless...'",
    "The entire complex noun clause beginning with 'that' is the direct object of 'states.' It contains multiple embedded dependent clauses within it.",
    ["noun clause", "direct object", "complex government language"])

add("Hard",
    "Which analysis is correct for the sentence 'What the audit revealed was that the department had been operating without the authorization that the law requires'?",
    ["Two noun clauses and one adjective clause", "One noun clause and two adjective clauses", "Three noun clauses", "Two adjective clauses and one adverb clause"],
    "Two noun clauses and one adjective clause",
    "'What the audit revealed' (noun clause/subject), 'that the department had been operating without the authorization' (noun clause/complement), 'that the law requires' (adjective clause modifying 'authorization').",
    ["clause analysis", "multiple types", "complex"])

add("Hard",
    "In 'Provided that the applicant demonstrates that she possesses the qualifications that the position requires, the committee will recommend that she be appointed,' how many 'that' clauses are there and what are their types?",
    ["Two noun clauses, one adjective clause", "Three noun clauses", "One adverb clause, two noun clauses, one adjective clause", "Two adjective clauses, two noun clauses"],
    "One adverb clause, two noun clauses, one adjective clause",
    "'Provided that the applicant demonstrates...' (adverb/condition), 'that she possesses the qualifications' (noun/object of 'demonstrates'), 'that the position requires' (adjective modifying 'qualifications'), 'that she be appointed' (noun/object of 'recommend').",
    ["that clauses", "multiple types", "complex analysis"])

add("Hard",
    "Which sentence correctly uses the subjunctive mood in a noun clause?",
    ["The committee recommended that he is promoted.", "The committee recommended that he be promoted.", "The committee recommended that he was promoted.", "The committee recommended that he will be promoted."],
    "The committee recommended that he be promoted.",
    "After verbs of recommendation/demand (recommend, suggest, insist, require), the noun clause uses the subjunctive: base form of the verb ('be,' not 'is/was/will be').",
    ["subjunctive", "noun clause", "recommend"])

add("Hard",
    "Which sentence correctly uses the subjunctive in a noun clause?",
    ["It is essential that every employee attends the training.", "It is essential that every employee attend the training.", "It is essential that every employee will attend the training.", "It is essential that every employee is attending the training."],
    "It is essential that every employee attend the training.",
    "After 'it is essential/important/necessary that...,' the subjunctive (base form) is used: 'attend' (not 'attends').",
    ["subjunctive", "noun clause", "essential"])

add("Hard",
    "In 'The director, whose tenure has been marked by reforms that have transformed the agency since she assumed office, announced that she would step down after the transition that the board had planned was completed,' identify the main clause.",
    ["'whose tenure has been marked by reforms'", "'that have transformed the agency'", "'The director announced that she would step down'", "'after the transition was completed'"],
    "'The director announced that she would step down'",
    "The main independent clause skeleton is 'The director announced [noun clause].' Everything else is embedded dependent clauses.",
    ["main clause", "complex sentence", "identification"])

add("Hard",
    "Which sentence demonstrates correct parallel structure in noun clauses?",
    ["The report shows that revenue increased and expenses have been reduced.", "The report shows that revenue increased and that expenses decreased.", "The report shows that revenue increased and decreasing expenses.", "The report shows that revenue increased, expenses decreased."],
    "The report shows that revenue increased and that expenses decreased.",
    "Parallel noun clauses should both begin with 'that' for clarity and grammatical parallelism.",
    ["parallelism", "noun clauses", "that"])

add("Hard",
    "In 'Whether the regulation that was proposed by the committee which oversees compliance will be adopted before the legislative session that begins next month ends depends on factors that no one can predict,' what is the subject of the main verb 'depends'?",
    ["'the regulation'", "'the committee'", "'Whether the regulation...will be adopted before...ends'", "'factors that no one can predict'"],
    "'Whether the regulation...will be adopted before...ends'",
    "The entire complex noun clause beginning with 'Whether' is the subject of 'depends.' It contains multiple embedded clauses.",
    ["noun clause", "subject", "complex embedding"])

add("Hard",
    "Which sentence correctly handles a noun clause after a preposition?",
    ["She is concerned about that the project might fail.", "She is concerned about whether the project might fail.", "She is concerned about the project might fail.", "She is concerned that about the project might fail."],
    "She is concerned about whether the project might fail.",
    "'Whether' can follow a preposition. 'That' clauses generally cannot directly follow prepositions in standard English (use 'the fact that' instead).",
    ["noun clause", "preposition", "whether vs that"])

add("Hard",
    "Which analysis is correct for 'It remains to be seen whether what the new administration proposes will address the concerns that stakeholders have raised since the policy was first implemented'?",
    ["Three dependent clauses", "Four dependent clauses", "Five dependent clauses", "Six dependent clauses"],
    "Four dependent clauses",
    "Four dependent clauses: (1) 'whether what...will address the concerns' (noun clause), (2) 'what the new administration proposes' (noun clause/subject within #1), (3) 'that stakeholders have raised' (adjective modifying 'concerns'), (4) 'since the policy was first implemented' (adverb of time).",
    ["counting clauses", "complex", "nested noun clauses"])

add("Hard",
    "Which sentence correctly uses an adverb clause of condition with the subjunctive?",
    ["If I was the director, I would change the policy.", "If I were the director, I would change the policy.", "If I am the director, I would change the policy.", "If I would be the director, I would change the policy."],
    "If I were the director, I would change the policy.",
    "The subjunctive 'were' is used in hypothetical/contrary-to-fact conditions ('If I were...' not 'If I was...').",
    ["subjunctive", "adverb clause", "condition", "hypothetical"])

add("Hard",
    "In 'The investigation determined that the official who had been entrusted with the funds that were allocated for the program that serves underprivileged communities had been misappropriating them since he assumed the position,' what does the adjective clause 'that serves underprivileged communities' modify?",
    ["'the official'", "'the funds'", "'the program'", "'the investigation'"],
    "'the program'",
    "The clause 'that serves underprivileged communities' immediately follows and modifies 'the program.'",
    ["adjective clause", "modification", "nested"])

add("Hard",
    "Which sentence uses a reduced adjective clause correctly?",
    ["The documents submitted yesterday contained errors.", "The documents were submitted yesterday contained errors.", "The documents submitting yesterday contained errors.", "The documents submit yesterday contained errors."],
    "The documents submitted yesterday contained errors.",
    "'Submitted yesterday' is a reduced adjective clause (from 'that were submitted yesterday'). The past participle correctly modifies 'documents.'",
    ["reduced clause", "past participle", "adjective clause"])

add("Hard",
    "Which sentence uses a reduced adverb clause correctly?",
    ["While reviewing the documents, the committee found discrepancies.", "While reviewing the documents, discrepancies were found.", "While reviewed the documents, the committee found discrepancies.", "While the reviewing documents, the committee found discrepancies."],
    "While reviewing the documents, the committee found discrepancies.",
    "The reduced adverb clause 'While reviewing the documents' correctly shares its subject with the main clause ('the committee').",
    ["reduced clause", "adverb clause", "dangling modifier"])

add("Hard",
    "In 'Lest the committee forget that the deadline that was set by the regulation which governs procurement is non-negotiable, the director issued a reminder,' what type of clause is 'Lest the committee forget...'?",
    ["Noun clause", "Adjective clause", "Adverb clause of purpose (negative)", "Adverb clause of condition"],
    "Adverb clause of purpose (negative)",
    "'Lest' means 'for fear that' or 'so that...not.' It introduces an adverb clause of negative purpose.",
    ["adverb clause", "purpose", "lest"])

add("Hard",
    "Which sentence correctly embeds a noun clause within an adjective clause?",
    ["The employee who believes that the policy is unfair filed a complaint.", "The employee who believes the policy is unfair that filed a complaint.", "The employee that who believes the policy is unfair filed a complaint.", "The employee believes who that the policy is unfair filed a complaint."],
    "The employee who believes that the policy is unfair filed a complaint.",
    "The adjective clause 'who believes that the policy is unfair' contains an embedded noun clause 'that the policy is unfair' (object of 'believes').",
    ["embedded clauses", "noun within adjective", "complex"])

add("Hard",
    "What is the error in: 'The reason why the project failed is because the team lacked resources.'?",
    ["'why' should be 'that'", "'is because' should be 'is that'", "'lacked' should be 'was lacking'", "No error"],
    "'is because' should be 'is that'",
    "'The reason is because...' is redundant (reason already implies cause). Correct: 'The reason is that the team lacked resources.'",
    ["redundancy", "reason is that", "error correction"])

add("Hard",
    "Which sentence correctly uses a cleft construction with a noun clause?",
    ["It was the director who approved the budget.", "It was that the director approved the budget.", "What approved the budget was the director it.", "The director it was who approved the budget."],
    "It was the director who approved the budget.",
    "The cleft construction 'It was X who/that...' correctly emphasizes 'the director.' The adjective clause 'who approved the budget' modifies the focused element.",
    ["cleft sentence", "emphasis", "adjective clause"])

add("Hard",
    "In 'Not until the committee certifies that the requirements have been met will the funds be released,' identify the clause type of 'that the requirements have been met.'",
    ["Adverb clause of time", "Adjective clause", "Noun clause (direct object of 'certifies')", "Noun clause (subject)"],
    "Noun clause (direct object of 'certifies')",
    "'That the requirements have been met' is the direct object of 'certifies' (certifies WHAT?). The inverted word order doesn't change clause functions.",
    ["noun clause", "inverted sentence", "direct object"])

add("Hard",
    "Which sentence correctly uses 'whether or not' in a noun clause?",
    ["Whether or not she attends the meeting is her decision.", "Whether or not, she attends the meeting is her decision.", "She attends the meeting whether or not is her decision.", "Whether she attends or not the meeting is her decision."],
    "Whether or not she attends the meeting is her decision.",
    "'Whether or not she attends the meeting' is a noun clause functioning as the subject. 'Whether or not' correctly precedes the subject of the embedded clause.",
    ["noun clause", "whether or not", "subject"])

# --- Advanced Sentence Combining and Transformation (561-600) ---
add("Hard",
    "Which sentence best combines these ideas using appropriate clause structure? 'The policy was implemented. The committee had concerns. The concerns were about its feasibility.'",
    ["The policy was implemented although the committee had concerns about its feasibility.", "The policy was implemented, the committee had concerns about its feasibility.", "Although the committee had concerns about its feasibility, the policy was implemented.", "The policy was implemented and the committee had concerns about its feasibility."],
    "Although the committee had concerns about its feasibility, the policy was implemented.",
    "'Although' correctly shows concession (implemented despite concerns), and placing the dependent clause first emphasizes the contrast.",
    ["sentence combining", "concession", "although"])

add("Hard",
    "Which revision best corrects this sentence? 'The employee submitted the report. Who was assigned to the project.'",
    ["The employee submitted the report, who was assigned to the project.", "The employee who was assigned to the project submitted the report.", "The employee submitted the report who was assigned to the project.", "Who was assigned to the project, the employee submitted the report."],
    "The employee who was assigned to the project submitted the report.",
    "The adjective clause 'who was assigned to the project' must immediately follow the noun it modifies ('employee').",
    ["sentence combining", "adjective clause placement", "fragment correction"])

add("Hard",
    "Which sentence correctly transforms the direct question into an embedded noun clause? Direct: 'When will the results be released?'",
    ["I want to know when will the results be released.", "I want to know when the results will be released.", "I want to know when are the results released.", "I want to know when the results are will be released."],
    "I want to know when the results will be released.",
    "In embedded (indirect) questions, use statement word order (subject before verb): 'when the results will be released' (not 'when will the results').",
    ["indirect question", "noun clause", "word order"])

add("Hard",
    "Which sentence correctly transforms the direct question into an embedded noun clause? Direct: 'Has the committee made a decision?'",
    ["I wonder has the committee made a decision.", "I wonder whether the committee has made a decision.", "I wonder that the committee has made a decision.", "I wonder if has the committee made a decision."],
    "I wonder whether the committee has made a decision.",
    "Yes/no questions become 'whether/if' clauses with statement word order in indirect speech.",
    ["indirect question", "whether", "word order"])

add("Hard",
    "Which sentence correctly uses a noun clause as the subject with appropriate verb agreement?",
    ["That the reports were submitted late are unacceptable.", "That the reports were submitted late is unacceptable.", "That the reports were submitted late were unacceptable.", "That the reports were submitted late have been unacceptable."],
    "That the reports were submitted late is unacceptable.",
    "A noun clause subject takes a singular verb ('is'), regardless of plural nouns within the clause.",
    ["noun clause", "subject-verb agreement", "singular verb"])

add("Hard",
    "Which sentence correctly reduces 'The employees who were hired last month' to a participial phrase?",
    ["The employees hiring last month attended the orientation.", "The employees hired last month attended the orientation.", "The employees who hiring last month attended the orientation.", "The employees were hired last month attended the orientation."],
    "The employees hired last month attended the orientation.",
    "'Hired last month' is a reduced adjective clause (past participle phrase) from 'who were hired last month.'",
    ["reduced clause", "participial phrase", "past participle"])

add("Hard",
    "Which sentence correctly uses a noun clause after 'the fact that' to follow a preposition?",
    ["She was upset about that the project was canceled.", "She was upset about the fact that the project was canceled.", "She was upset about the project was canceled.", "She was upset the fact about that the project was canceled."],
    "She was upset about the fact that the project was canceled.",
    "'That' clauses cannot directly follow prepositions. Use 'the fact that' as a bridge: 'about the fact that...'",
    ["noun clause", "preposition", "the fact that"])

add("Hard",
    "In 'Had the committee known that the contractor whom they had selected lacked the certification that the regulation requires, they would not have awarded the contract,' identify the conditional clause.",
    ["'that the contractor lacked the certification'", "'Had the committee known'", "'whom they had selected'", "'that the regulation requires'"],
    "'Had the committee known'",
    "'Had the committee known' is an inverted conditional clause (formal equivalent of 'If the committee had known'). It is an adverb clause of condition.",
    ["inverted conditional", "adverb clause", "condition"])

add("Hard",
    "Which sentence correctly uses parallel noun clauses?",
    ["The report shows that revenue increased, expenses decreased, and the workforce expanded.", "The report shows that revenue increased, that expenses decreased, and that the workforce expanded.", "The report shows that revenue increased, expenses have decreased, and expanding the workforce.", "The report shows revenue increased, that expenses decreased, and that the workforce expanded."],
    "The report shows that revenue increased, that expenses decreased, and that the workforce expanded.",
    "For clarity and parallelism, each noun clause in a series should begin with 'that.'",
    ["parallelism", "noun clauses", "series"])

add("Hard",
    "Which sentence correctly handles the ambiguity of 'since'?",
    ["Since the director left, the department has improved. (time)", "Since the director is qualified, she should be promoted. (reason)", "Both A and B are correct uses of 'since'", "Neither A nor B is correct"],
    "Both A and B are correct uses of 'since'",
    "'Since' can mean 'from the time that' (time) or 'because' (reason). Both uses are grammatically correct; context determines meaning.",
    ["since", "ambiguity", "time vs reason"])

add("Hard",
    "Which sentence correctly uses a concessive clause with inversion?",
    ["Though she is experienced, she was not hired.", "Experienced though she is, she was not hired.", "Though experienced she is, she was not hired.", "She is experienced though, she was not hired."],
    "Experienced though she is, she was not hired.",
    "'Adjective + though + subject + verb' is a formal inverted concessive structure. It emphasizes the concession.",
    ["concessive clause", "inversion", "formal"])

add("Hard",
    "In 'So complex was the regulation that even the lawyers who specialize in administrative law found that they could not determine what the provision that was added at the last minute actually required,' identify the result clause.",
    ["'So complex was the regulation'", "'that even the lawyers found'", "'that even the lawyers who specialize in administrative law found that they could not determine what...'", "'who specialize in administrative law'"],
    "'that even the lawyers who specialize in administrative law found that they could not determine what...'",
    "In the 'so...that' construction, the 'that' clause expresses the result of the extreme degree ('so complex').",
    ["result clause", "so...that", "complex"])

add("Hard",
    "Which sentence correctly uses a noun clause in apposition?",
    ["The idea, that we should postpone the project, was rejected.", "The idea that we should postpone the project was rejected.", "The idea we should postpone the project that was rejected.", "That we should postpone the project the idea was rejected."],
    "The idea that we should postpone the project was rejected.",
    "A noun clause in apposition to 'idea' uses 'that' without commas (it defines what the idea IS). This is different from a non-restrictive adjective clause.",
    ["noun clause", "apposition", "no commas"])

add("Hard",
    "Which analysis is correct for 'It is not clear whether the amendment that the opposition proposed, which would have required that all agencies submit quarterly reports, will be included in the final version that the president signs.'?",
    ["Three dependent clauses", "Four dependent clauses", "Five dependent clauses", "Six dependent clauses"],
    "Five dependent clauses",
    "Five: (1) 'whether the amendment will be included' (noun clause), (2) 'that the opposition proposed' (adjective), (3) 'which would have required that all agencies submit quarterly reports' (adjective, non-restrictive), (4) 'that all agencies submit quarterly reports' (noun, object of 'required'), (5) 'that the president signs' (adjective modifying 'version').",
    ["counting clauses", "complex analysis", "five clauses"])

add("Hard",
    "Which sentence demonstrates correct use of a free relative clause (nominal relative clause)?",
    ["Whatever the committee decides will be final.", "Whatever the committee decides, will be final.", "The committee decides whatever will be final.", "Will be final whatever the committee decides."],
    "Whatever the committee decides will be final.",
    "'Whatever the committee decides' is a free relative clause (noun clause without an antecedent) functioning as the subject. No comma separates it from the verb.",
    ["free relative clause", "whatever", "subject"])

add("Hard",
    "In 'The official denied that he had known that the funds which had been earmarked for the project that the legislature approved were being diverted to accounts that he controlled,' how many clauses beginning with 'that' are there?",
    ["Two", "Three", "Four", "Five"],
    "Four",
    "Four 'that' clauses: (1) 'that he had known...' (noun/object of 'denied'), (2) 'that the funds were being diverted' (noun/object of 'known'), (3) 'that the legislature approved' (adjective modifying 'project'), (4) 'that he controlled' (adjective modifying 'accounts'). Plus 'which had been earmarked' uses 'which.'",
    ["that clauses", "counting", "complex"])

add("Hard",
    "Which sentence correctly uses an adverb clause with 'no sooner...than'?",
    ["No sooner had she arrived when the meeting started.", "No sooner had she arrived than the meeting started.", "No sooner she had arrived than the meeting started.", "No sooner had she arrived that the meeting started."],
    "No sooner had she arrived than the meeting started.",
    "'No sooner...than' is the correct correlative structure with inverted word order ('had she arrived').",
    ["correlative", "no sooner than", "inversion"])

add("Hard",
    "Which sentence correctly handles a noun clause after 'insist'?",
    ["She insists that he attends the meeting.", "She insists that he attend the meeting.", "She insists that he will attend the meeting.", "She insists that he is attending the meeting."],
    "She insists that he attend the meeting.",
    "After 'insist' (a mandative verb), the noun clause uses the subjunctive: base form 'attend' (not 'attends').",
    ["subjunctive", "insist", "mandative"])

add("Hard",
    "In 'Not only did the investigation reveal that the official had been negligent, but it also showed that the system which was supposed to prevent such failures had itself been compromised by those who were tasked with maintaining it,' identify the total number of dependent clauses.",
    ["Four", "Five", "Six", "Seven"],
    "Five",
    "Five dependent clauses: (1) 'that the official had been negligent' (noun), (2) 'that the system had itself been compromised' (noun), (3) 'which was supposed to prevent such failures' (adjective), (4) 'by those' — actually 'who were tasked with maintaining it' (adjective modifying 'those'). That's four. Let me recount: (1) that...negligent, (2) that...compromised, (3) which...failures, (4) who...maintaining it. Four dependent clauses plus the correlative structure.",
    ["counting clauses", "correlative", "complex"])

# Fix the above
questions[-1] = {
    "id": questions[-1]["id"],
    "subtest": "Verbal Ability",
    "module": "Sentence Structure",
    "subtopic": "Clauses",
    "difficulty": "Hard",
    "question": "In 'Not only did the investigation reveal that the official had been negligent, but it also showed that the system which was supposed to prevent such failures had been compromised by those who were tasked with maintaining it,' how many dependent clauses are there?",
    "choices": ["Three", "Four", "Five", "Six"],
    "answer": "Four",
    "explanation": "Four dependent clauses: (1) 'that the official had been negligent' (noun clause), (2) 'that the system...had been compromised by those who were tasked with maintaining it' (noun clause), (3) 'which was supposed to prevent such failures' (adjective clause), (4) 'who were tasked with maintaining it' (adjective clause).",
    "tags": ["counting clauses", "complex", "four dependent"],
    "category": ["Professional", "Sub-Professional"],
    "language": "English"
}

add("Hard",
    "Which sentence correctly uses a conditional clause with mixed time reference?",
    ["If she studied harder yesterday, she will pass tomorrow.", "If she had studied harder yesterday, she would pass tomorrow.", "If she would have studied harder yesterday, she will pass tomorrow.", "If she studies harder yesterday, she would pass tomorrow."],
    "If she had studied harder yesterday, she would pass tomorrow.",
    "Mixed conditional: past condition ('had studied' — past perfect for unreal past) + present/future result ('would pass' — would + base form).",
    ["mixed conditional", "adverb clause", "time reference"])

add("Hard",
    "Which sentence correctly uses 'whether' vs 'if' in a noun clause?",
    ["Whether or not she attends is her decision.", "If or not she attends is her decision.", "Whether she attends is her decision, or not.", "If she attends or not is her decision."],
    "Whether or not she attends is her decision.",
    "'Whether' (not 'if') is used when the noun clause is the subject. 'If' cannot introduce subject noun clauses.",
    ["whether vs if", "noun clause", "subject position"])

add("Hard",
    "In 'The committee recommended that the regulation be revised so that it would address the concerns that stakeholders had raised before the policy was implemented,' what is the function of 'that the regulation be revised'?",
    ["Subject", "Direct object of 'recommended'", "Subject complement", "Adverb clause of purpose"],
    "Direct object of 'recommended'",
    "'That the regulation be revised' is a noun clause (direct object of 'recommended'). Note the subjunctive 'be revised.'",
    ["noun clause", "direct object", "subjunctive"])

add("Hard",
    "Which sentence correctly uses a cleft sentence to emphasize time?",
    ["It was yesterday when the director announced the changes.", "It was yesterday that the director announced the changes.", "Yesterday it was that the director announced the changes.", "It was that yesterday the director announced the changes."],
    "It was yesterday that the director announced the changes.",
    "In cleft sentences emphasizing adverbs of time, 'that' (not 'when') is used: 'It was [focused element] that [rest of sentence].'",
    ["cleft sentence", "emphasis", "time"])

add("Hard",
    "Which sentence correctly uses a pseudo-cleft (wh-cleft) construction?",
    ["What the department needs is additional funding.", "What the department needs are additional funding.", "The department needs is what additional funding.", "Additional funding is what the department needs it."],
    "What the department needs is additional funding.",
    "The wh-cleft 'What X is Y' uses a noun clause as subject. The linking verb 'is' agrees with the clause (singular).",
    ["pseudo-cleft", "noun clause", "emphasis"])

add("Hard",
    "In 'Inasmuch as the evidence that was presented during the hearing which lasted three days demonstrated that the accused had violated the regulation that prohibits conflicts of interest, the committee had no choice but to recommend dismissal,' identify the main clause.",
    ["'the evidence demonstrated'", "'the committee had no choice but to recommend dismissal'", "'the accused had violated the regulation'", "'Inasmuch as the evidence was presented'"],
    "'the committee had no choice but to recommend dismissal'",
    "The main independent clause is 'the committee had no choice but to recommend dismissal.' Everything before the comma is a complex adverb clause of reason ('Inasmuch as...').",
    ["main clause", "complex", "inasmuch as"])

add("Hard",
    "Which sentence correctly uses 'however' as a free relative (not a conjunctive adverb)?",
    ["However difficult the task may be, she will complete it.", "The task is difficult; however, she will complete it.", "However, the task is difficult, she will complete it.", "She will complete it however the task is difficult."],
    "However difficult the task may be, she will complete it.",
    "'However difficult the task may be' is a concessive free relative clause (= 'no matter how difficult'). It functions as an adverb clause.",
    ["free relative", "however", "concessive"])

add("Hard",
    "Which analysis is correct for the sentence 'The fact that what the whistleblower alleged turned out to be true vindicated those who had believed that the system was corrupt'?",
    ["Three dependent clauses", "Four dependent clauses", "Five dependent clauses", "Six dependent clauses"],
    "Four dependent clauses",
    "Four: (1) 'that what the whistleblower alleged turned out to be true' (noun clause in apposition to 'fact'), (2) 'what the whistleblower alleged' (noun clause/subject within #1), (3) 'who had believed that the system was corrupt' (adjective clause), (4) 'that the system was corrupt' (noun clause/object of 'believed').",
    ["counting clauses", "complex", "nested"])

add("Hard",
    "Which sentence correctly uses a conditional clause with 'were to'?",
    ["If the director were to resign, the department would be restructured.", "If the director was to resign, the department would be restructured.", "If the director would resign, the department were to be restructured.", "Were the director to resign, the department will be restructured."],
    "If the director were to resign, the department would be restructured.",
    "'Were to + infinitive' expresses a hypothetical future condition. It is more formal than simple past subjunctive.",
    ["conditional", "were to", "hypothetical"])

add("Hard",
    "In 'So thoroughly had the auditors examined the records that they discovered discrepancies that no one who had previously reviewed the documents that were filed before the new system was implemented had noticed,' identify the result clause.",
    ["'So thoroughly had the auditors examined the records'", "'that they discovered discrepancies'", "'that they discovered discrepancies that no one...had noticed'", "'that no one had noticed'"],
    "'that they discovered discrepancies that no one...had noticed'",
    "In the 'so...that' construction, the entire 'that' clause (including its embedded clauses) expresses the result.",
    ["result clause", "so...that", "inversion"])


# ============================================================
# OUTPUT
# ============================================================

# Verify counts
easy = [q for q in questions if q["difficulty"] == "Easy"]
medium = [q for q in questions if q["difficulty"] == "Medium"]
hard = [q for q in questions if q["difficulty"] == "Hard"]

print(f"Total questions: {len(questions)}")
print(f"Easy: {len(easy)}")
print(f"Medium: {len(medium)}")
print(f"Hard: {len(hard)}")

# Reassign IDs sequentially
for i, q in enumerate(questions, 1):
    q["id"] = i

# Write output
output_dir = os.path.join("data", "seed", "questions", "verbal-ability", "sentence-structure", "clauses")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "questions.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written to: {output_path}")
