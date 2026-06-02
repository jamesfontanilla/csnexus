"""
Generate 600 word recognition questions for the CSE reviewer.
Question types:
  - "Which of the following is a REAL English word?"
  - "Which of the following is NOT a real English word?"
  - "Which word is a legitimate term used in government/professional contexts?"
  - "Identify the fabricated (non-existent) word."

Distribution: 200 Easy, 200 Medium, 200 Hard
Each question has 4 choices, all unique per question.
No two questions share the same sorted choice set.
"""

import json
import os
import random
import sys

# =============================================================================
# WORD BANKS — each entry: (real_word, definition, [3 non-words], tags)
# =============================================================================

EASY_WORDS = [
    ("government", "the governing body of a nation", ["goverment", "governmant", "govenment"], ["common", "root-word"]),
    ("environment", "surroundings or conditions", ["enviroment", "environmant", "enviranment"], ["common", "root-word"]),
    ("committee", "a group for a specific function", ["comittee", "commitee", "comitee"], ["common", "double-letter"]),
    ("assessment", "evaluation of something", ["assesment", "asessment", "assessmant"], ["common", "double-letter"]),
    ("professional", "relating to a profession", ["proffesional", "profesional", "proffessional"], ["common", "double-letter"]),
    ("immediately", "at once; without delay", ["imediately", "immediatly", "immedietly"], ["common", "double-letter"]),
    ("acknowledge", "to accept or recognize", ["acknowlege", "acknowladge", "aknowledge"], ["common", "silent-letter"]),
    ("certificate", "an official document", ["certifcate", "sertificate", "certificat"], ["common", "latin-origin"]),
    ("independent", "free from outside control", ["independant", "indipendent", "independint"], ["common", "suffix"]),
    ("maintenance", "preserving a condition", ["maintainance", "maintenence", "maintanance"], ["common", "suffix"]),
    ("occurrence", "an incident or event", ["occurence", "ocurrence", "occurrance"], ["common", "double-letter"]),
    ("recommend", "to suggest as suitable", ["recomend", "reccommend", "recommand"], ["common", "double-letter"]),
    ("permanent", "lasting indefinitely", ["permanant", "permenent", "permenint"], ["common", "suffix"]),
    ("procedure", "an established method", ["proceedure", "procedur", "prosedure"], ["common", "suffix"]),
    ("reference", "a source of information", ["referance", "refference", "referrence"], ["common", "suffix"]),
    ("experience", "practical contact with events", ["experiance", "expirience", "experence"], ["common", "suffix"]),
    ("attendance", "being present", ["attendence", "attendanse", "atendance"], ["common", "suffix"]),
    ("conference", "a formal meeting", ["conferance", "confrence", "conferrence"], ["common", "suffix"]),
    ("performance", "execution of an action", ["performence", "preformance", "performanse"], ["common", "suffix"]),
    ("compliance", "acting per rules", ["complience", "complianse", "compliane"], ["common", "suffix"]),
    ("significant", "important; of consequence", ["significent", "signifigant", "significint"], ["common", "suffix"]),
    ("responsibility", "being accountable", ["responsibilty", "responsability", "responsibilety"], ["common", "suffix"]),
    ("communication", "exchange of information", ["comunication", "communicaton", "commmunication"], ["common", "double-letter"]),
    ("opportunity", "favorable circumstances", ["oportunity", "oppertunity", "oppurtunity"], ["common", "double-letter"]),
    ("administration", "management of affairs", ["administracion", "administrasion", "administraton"], ["common", "suffix"]),
    ("organization", "a structured group", ["organizacion", "organisaton", "organizasion"], ["common", "suffix"]),
    ("requirement", "something needed", ["requirment", "requiremant", "requierment"], ["common", "suffix"]),
    ("development", "growth or advancement", ["developement", "devlopment", "develpoment"], ["common", "root-word"]),
    ("management", "controlling things", ["managment", "managemant", "manegement"], ["common", "suffix"]),
    ("achievement", "something accomplished", ["acheivement", "achievment", "acheivment"], ["common", "ie-ei"]),
    ("enrollment", "the act of registering", ["enrolement", "enrollmant", "enroalment"], ["common", "double-letter"]),
    ("department", "a division of an organization", ["departmant", "deparment", "departement"], ["common", "suffix"]),
    ("employment", "having paid work", ["employement", "employmant", "imployment"], ["common", "suffix"]),
    ("regulation", "a rule by authority", ["regulacion", "regulasion", "regulaton"], ["common", "suffix"]),
    ("information", "facts provided", ["informacion", "informasion", "informaton"], ["common", "suffix"]),
    ("application", "a formal request", ["aplicacion", "applicaton", "applicasion"], ["common", "suffix"]),
    ("examination", "detailed inspection", ["examinacion", "examinasion", "examinaton"], ["common", "suffix"]),
    ("supervision", "overseeing work", ["supervicion", "supervisin", "supervison"], ["common", "suffix"]),
    ("preparation", "making ready", ["preparacion", "preparasion", "preparaton"], ["common", "suffix"]),
    ("distribution", "sharing out", ["distribusion", "distribucion", "distributoin"], ["common", "suffix"]),
    ("qualification", "a quality or accomplishment", ["qualificacion", "qualificasion", "qualificaton"], ["common", "suffix"]),
    ("investigation", "a formal inquiry", ["investigacion", "investigasion", "investigaton"], ["common", "suffix"]),
    ("appreciation", "recognition of quality", ["apreciacion", "appreciasion", "appreciaton"], ["common", "suffix"]),
    ("authorization", "official permission", ["authorizacion", "authorizasion", "authorizaton"], ["common", "suffix"]),
    ("determination", "firmness of purpose", ["determinacion", "determinasion", "determinaton"], ["common", "suffix"]),
    ("implementation", "putting into effect", ["implementacion", "implementasion", "implementaton"], ["common", "suffix"]),
    ("consideration", "careful thought", ["consideracion", "considerasion", "consideraton"], ["common", "suffix"]),
    ("accommodation", "lodging or adjustment", ["accomodacion", "accommodasion", "accommodaton"], ["common", "double-letter"]),
    ("transportation", "movement of goods", ["transportacion", "transportasion", "transportaton"], ["common", "suffix"]),
    ("documentation", "official materials", ["documentacion", "documentasion", "documentaton"], ["common", "suffix"]),
    ("curriculum", "subjects in a course", ["curiculum", "curriculam", "curricullum"], ["common", "latin-origin"]),
    ("hierarchy", "a ranking system", ["heirarchy", "hierachy", "heiarchy"], ["common", "greek-origin"]),
    ("guarantee", "a formal assurance", ["gaurantee", "guarentee", "garentee"], ["common", "french-origin"]),
    ("discipline", "training to obey rules", ["disipline", "dicipline", "disiplin"], ["common", "latin-origin"]),
    ("privilege", "a special right", ["priviledge", "privelege", "privilige"], ["common", "latin-origin"]),
    ("possession", "having something", ["posession", "possesion", "posesion"], ["common", "double-letter"]),
    ("knowledge", "awareness through experience", ["knowlege", "knowledg", "knowladge"], ["common", "silent-letter"]),
    ("correspondence", "communication by letters", ["correspondance", "corrispondence", "corespondence"], ["common", "suffix"]),
    ("surveillance", "close observation", ["surveilance", "survellance", "surviellance"], ["common", "french-origin"]),
    ("questionnaire", "a set of questions", ["questionaire", "questionnare", "questionairre"], ["common", "french-origin"]),
    ("bureaucracy", "government by officials", ["beauracracy", "burocracy", "beurocracy"], ["common", "french-origin"]),
    ("accommodate", "provide lodging or adjust", ["accomodate", "acommodate", "acomodate"], ["common", "double-letter"]),
    ("conscience", "sense of right and wrong", ["concience", "consience", "consciance"], ["common", "latin-origin"]),
    ("embarrass", "to cause awkwardness", ["embarass", "embarras", "embaress"], ["common", "double-letter"]),
    ("exaggerate", "to overstate", ["exagerate", "exaggarate", "exaggeratte"], ["common", "double-letter"]),
    ("miscellaneous", "various types mixed", ["miscelaneous", "miscellanious", "miscellanous"], ["common", "latin-origin"]),
    ("consensus", "general agreement", ["concensus", "consencus", "concensous"], ["common", "latin-origin"]),
    ("harassment", "aggressive pressure", ["harrassment", "harasment", "harassement"], ["common", "suffix"]),
    ("personnel", "employees of an organization", ["personel", "personell", "personnell"], ["common", "french-origin"]),
    ("acquisition", "acquiring something", ["aquisition", "acqusition", "acquistion"], ["common", "latin-origin"]),
    ("reimbursement", "repayment of money", ["reimbursment", "reimbursemant", "riembursement"], ["common", "suffix"]),
    ("millennium", "a thousand years", ["millenium", "milennium", "milenium"], ["common", "latin-origin"]),
    ("itinerary", "a planned route", ["itinarary", "itineraray", "itinenary"], ["common", "latin-origin"]),
    ("perseverance", "persistence", ["perseverence", "perserverance", "persaverance"], ["common", "suffix"]),
    ("conscientious", "wishing to do right", ["consciencious", "conscentious", "conciencious"], ["common", "suffix"]),
    ("simultaneous", "occurring at same time", ["simultanious", "simultanous", "simultaenous"], ["common", "suffix"]),
    ("transparent", "allowing light through", ["transparant", "transperent", "transparrent"], ["common", "suffix"]),
    ("unnecessary", "not needed", ["unecessary", "unnecesary", "unneccessary"], ["common", "double-letter"]),
    ("vigilance", "keeping careful watch", ["vigilence", "vigilanse", "vigalance"], ["common", "suffix"]),
    ("allegiance", "loyalty or commitment", ["allegience", "alegiance", "allegance"], ["common", "suffix"]),
    ("cancellation", "deciding something won't happen", ["cancellaton", "cancelation", "cancallation"], ["common", "double-letter"]),
    ("commemorate", "to recall and show respect", ["comemorate", "commemmorate", "comemmorate"], ["common", "double-letter"]),
    ("infrastructure", "basic physical systems", ["infastructure", "infrastructer", "infrustructure"], ["common", "latin-origin"]),
    ("superintendent", "person who manages", ["superintendant", "superindendent", "superintendint"], ["common", "suffix"]),
    ("remittance", "money sent as payment", ["remitance", "remittence", "remittanse"], ["common", "suffix"]),
    ("beneficiary", "person who receives benefit", ["beneficary", "benificiary", "beneficiarey"], ["common", "suffix"]),
    ("comprehensive", "including all elements", ["comprehansive", "comprehensiv", "comprahensive"], ["common", "suffix"]),
    ("characteristic", "a distinguishing feature", ["characteristc", "charecteristic", "characterestic"], ["common", "suffix"]),
    ("accomplishment", "something achieved", ["acomplishment", "accomplishmant", "accompplishment"], ["common", "double-letter"]),
    ("acknowledgment", "recognition of existence", ["acknowledgmant", "acknowlegment", "aknowledgment"], ["common", "suffix"]),
    ("approximately", "close to exact amount", ["approximatly", "aproximately", "approximatley"], ["common", "suffix"]),
    ("consequently", "as a result", ["consequantly", "consequentley", "consequintly"], ["common", "suffix"]),
    ("deterioration", "becoming worse", ["deterioracion", "deteriorasion", "deterioraton"], ["common", "suffix"]),
    ("discrimination", "unjust treatment", ["discriminacion", "discriminasion", "discriminaton"], ["common", "suffix"]),
    ("encouragement", "support or confidence", ["encouragment", "encouragemant", "incouragement"], ["common", "suffix"]),
    ("establishment", "action of establishing", ["establisment", "establishmant", "estableshment"], ["common", "suffix"]),
    ("interpretation", "explanation of meaning", ["interpretacion", "interpretasion", "interpretaton"], ["common", "suffix"]),
    ("recommendation", "suggestion for action", ["recomendation", "recommendacion", "recomendacion"], ["common", "double-letter"]),
    ("rehabilitation", "restoration to normal life", ["rehabilitacion", "rehabilitasion", "rehabilitaton"], ["common", "suffix"]),
    ("congratulations", "expression of joy for someone", ["congradulations", "congratulasions", "congratulatons"], ["common", "suffix"]),
    ("differentiation", "distinguishing between things", ["differentiacion", "differentiasion", "differentiaton"], ["common", "suffix"]),
    ("participation", "taking part in something", ["participacion", "participasion", "participaton"], ["common", "suffix"]),
    ("pronunciation", "how a word is spoken", ["pronounciation", "pronunciacion", "pronuncation"], ["common", "suffix"]),
    ("communication", "exchange of information", ["communicacion", "comunicasion", "communicaton"], ["common", "suffix"]),
    ("collaboration", "working together", ["colaboration", "collaboracion", "collaborasion"], ["common", "double-letter"]),
    ("representation", "acting on behalf of someone", ["representacion", "representasion", "representaton"], ["common", "suffix"]),
    ("classification", "arranging into categories", ["classificacion", "classificasion", "classificaton"], ["common", "suffix"]),
    ("specification", "detailed description", ["specificacion", "specificasion", "specificaton"], ["common", "suffix"]),
    ("identification", "establishing identity", ["identificacion", "identificasion", "identificaton"], ["common", "suffix"]),
    ("recommendation", "a suggestion or endorsement", ["recomendacion", "recommendasion", "recomandation"], ["common", "suffix"]),
    ("demonstration", "a showing or proof", ["demonstracion", "demonstrasion", "demonstraton"], ["common", "suffix"]),
    ("accommodation", "housing or adjustment", ["acommodation", "accomodacion", "accommodasion"], ["common", "double-letter"]),
    ("concentration", "focus or density", ["concentracion", "concentrasion", "concentraton"], ["common", "suffix"]),
    ("congratulation", "praise for achievement", ["congradulation", "congratulacion", "congratulasion"], ["common", "suffix"]),
    ("consolidation", "combining into one", ["consolidacion", "consolidasion", "consolidaton"], ["common", "suffix"]),
    ("configuration", "arrangement of parts", ["configuracion", "configurasion", "configuraton"], ["common", "suffix"]),
    ("appropriation", "money set aside", ["apropriacion", "appropriasion", "apropriation"], ["common", "suffix"]),
    ("justification", "showing something is right", ["justificacion", "justificasion", "justificaton"], ["common", "suffix"]),
    ("notification", "the act of notifying", ["notificacion", "notificasion", "notificaton"], ["common", "suffix"]),
    ("verification", "confirming truth or accuracy", ["verificacion", "verificasion", "verificaton"], ["common", "suffix"]),
]

MEDIUM_WORDS = [
    ("adjudicate", "to make a formal judgment", ["adjudicant", "adjudikate", "adjudicament"], ["legal", "latin-origin"]),
    ("promulgate", "to make widely known", ["promulgant", "promulkate", "promulgament"], ["legal", "latin-origin"]),
    ("expropriation", "taking property for public use", ["expropriament", "expropriacion", "expropriant"], ["legal", "latin-origin"]),
    ("disbursement", "payment from a fund", ["disbursation", "disbursament", "disbursiment"], ["financial", "suffix"]),
    ("remuneration", "payment for services", ["remunerant", "remunerament", "remunerasion"], ["financial", "latin-origin"]),
    ("requisition", "a formal demand", ["requisitament", "requisitionary", "requisitant"], ["procurement", "latin-origin"]),
    ("encumbrance", "a burden or claim", ["encumbrement", "encumbrant", "encumbrament"], ["financial", "suffix"]),
    ("appropriation", "money for a purpose", ["appropriament", "appropriant", "appropriacion"], ["financial", "suffix"]),
    ("jurisprudence", "the theory of law", ["jurisprudention", "jurisprudentious", "jurisprudentiary"], ["legal", "latin-origin"]),
    ("indemnification", "compensation for loss", ["indemnificant", "indemnificament", "indemnificatious"], ["legal", "latin-origin"]),
    ("corroborate", "to confirm or support", ["corroborant", "corroborize", "corroborament"], ["legal", "latin-origin"]),
    ("ameliorate", "to make better", ["ameliorant", "ameliorize", "ameliorament"], ["formal", "latin-origin"]),
    ("exacerbate", "to make worse", ["exacerbant", "exacerbize", "exacerbament"], ["formal", "latin-origin"]),
    ("perseverate", "to repeat insistently", ["perseverant", "perseverize", "perseverament"], ["psychology", "latin-origin"]),
    ("concatenate", "to link in a chain", ["concatenant", "concatenize", "concatenament"], ["technical", "latin-origin"]),
    ("prevaricate", "to speak evasively", ["prevaricant", "prevaricize", "prevaricament"], ["formal", "latin-origin"]),
    ("confabulate", "to chat or fabricate memories", ["confabulant", "confabulize", "confabulament"], ["psychology", "latin-origin"]),
    ("tergiversate", "to change loyalties", ["tergiversant", "tergiversize", "tergiversament"], ["formal", "latin-origin"]),
    ("capitulate", "to surrender", ["capitulant", "capitulize", "capitulament"], ["formal", "latin-origin"]),
    ("extrapolate", "to extend known data", ["extrapolant", "extrapolize", "extrapolament"], ["technical", "latin-origin"]),
    ("superannuation", "retirement pension", ["superannuament", "superannuant", "superannuatious"], ["hr", "latin-origin"]),
    ("retrenchment", "reduction of costs", ["retrenchation", "retrenchant", "retrenchamous"], ["hr", "suffix"]),
    ("emolument", "salary or compensation", ["emolumant", "emolumentary", "emolumention"], ["hr", "latin-origin"]),
    ("probationary", "relating to trial period", ["probationant", "probationate", "probationous"], ["hr", "suffix"]),
    ("commendation", "formal praise", ["commendament", "commendatious", "commendantial"], ["hr", "suffix"]),
    ("amortization", "spreading cost over time", ["amortizament", "amortizant", "amortizatious"], ["financial", "suffix"]),
    ("liquidation", "settling debts", ["liquidament", "liquidatious", "liquidantial"], ["financial", "suffix"]),
    ("expenditure", "the act of spending", ["expendament", "expenditant", "expendituous"], ["financial", "suffix"]),
    ("procurement", "obtaining something", ["procurament", "procuratious", "procurementary"], ["government", "suffix"]),
    ("accreditation", "official recognition", ["accreditament", "accreditatious", "accreditantial"], ["government", "suffix"]),
    ("adjudication", "formal judgment", ["adjudicament", "adjudicatious", "adjudicantial"], ["legal", "suffix"]),
    ("promulgation", "making law known", ["promulgament", "promulgatious", "promulgantial"], ["legal", "suffix"]),
    ("exonerate", "to free from blame", ["exonerant", "exonerize", "exonerament"], ["legal", "latin-origin"]),
    ("abrogate", "to abolish formally", ["abrogant", "abrogize", "abrogament"], ["legal", "latin-origin"]),
    ("subpoena", "a legal summons", ["subpeona", "subpena", "supboena"], ["legal", "latin-origin"]),
    ("supersede", "to replace", ["supercede", "superseed", "superceed"], ["formal", "latin-origin"]),
    ("acquiescence", "acceptance without protest", ["acquiescance", "acquiescment", "acquiescious"], ["legal", "suffix"]),
    ("malfeasance", "wrongdoing by official", ["malfeasence", "malfeasant", "malfeasious"], ["legal", "suffix"]),
    ("nonfeasance", "failure to act", ["nonfeasence", "nonfeasant", "nonfeasious"], ["legal", "suffix"]),
    ("misfeasance", "improper performance", ["misfeasence", "misfeasant", "misfeasious"], ["legal", "suffix"]),
    ("fiduciary", "involving trust in finances", ["fiduciant", "fiduciarious", "fiduciament"], ["financial", "latin-origin"]),
    ("arbitration", "dispute settlement", ["arbitrament", "arbitratious", "arbitrantial"], ["legal", "suffix"]),
    ("delineation", "description in detail", ["delineament", "delineatious", "delineantial"], ["formal", "suffix"]),
    ("proliferation", "rapid increase", ["proliferant", "proliferatious", "proliferantial"], ["formal", "suffix"]),
    ("interpolation", "insertion between parts", ["interpolament", "interpolatious", "interpolantial"], ["technical", "suffix"]),
    ("confiscation", "seizure by authority", ["confiscament", "confiscatious", "confiscantial"], ["legal", "suffix"]),
    ("deliberation", "careful consideration", ["deliberament", "deliberatious", "deliberantial"], ["formal", "suffix"]),
    ("remonstrance", "a forceful protest", ["remonstrament", "remonstratious", "remonstrantial"], ["formal", "suffix"]),
    ("acquittal", "verdict of not guilty", ["acquittament", "acquittatious", "acquittantial"], ["legal", "suffix"]),
    ("insubordination", "defiance of authority", ["insubordinament", "insubordinatious", "insubordinantial"], ["hr", "suffix"]),
    ("ratification", "formal consent", ["ratificament", "ratificatious", "ratificantial"], ["legal", "suffix"]),
    ("jurisdiction", "official power to decide", ["jurisdicament", "jurisdictious", "jurisdicantial"], ["legal", "suffix"]),
    ("nomenclature", "a naming system", ["nomenclaturant", "nomenclatize", "nomenclatament"], ["formal", "latin-origin"]),
    ("recapitulate", "to summarize points", ["recapitulant", "recapitulize", "recapitulament"], ["formal", "latin-origin"]),
    ("dissemination", "spreading info widely", ["disseminament", "disseminatious", "disseminantial"], ["formal", "suffix"]),
    ("circumscribe", "to restrict or define", ["circumscribant", "circumscribize", "circumscribament"], ["formal", "latin-origin"]),
    ("remonstrate", "to protest forcefully", ["remonstrant", "remonstratize", "remonstratament"], ["formal", "latin-origin"]),
    ("extemporaneous", "without preparation", ["extemporaniant", "extemporanize", "extemporanament"], ["formal", "latin-origin"]),
    ("concatenation", "a linked series", ["concatenament", "concatenatious", "concatenantial"], ["technical", "suffix"]),
    ("authentication", "proof of identity", ["authenticament", "authenticatious", "authenticantial"], ["technical", "suffix"]),
    ("disenfranchise", "to deprive of voting rights", ["disenfranchisant", "disenfranchizement", "disenfranchisament"], ["legal", "suffix"]),
    ("conglomeration", "things grouped together", ["conglomerament", "conglomeratious", "conglomerantial"], ["formal", "suffix"]),
    ("accountability", "being responsible", ["accountabilament", "accountabilitant", "accountabilitous"], ["government", "suffix"]),
    ("memorandum", "a business message", ["memorandament", "memorandatious", "memorandantial"], ["government", "latin-origin"]),
    ("corrigendum", "a correction to text", ["corrigendament", "corrigendatious", "corrigendantial"], ["legal", "latin-origin"]),
    ("addendum", "addition to a document", ["addendament", "addendatious", "addendantial"], ["legal", "latin-origin"]),
    ("referendum", "a direct vote", ["referendament", "referendatious", "referendantial"], ["governance", "latin-origin"]),
    ("ultimatum", "final demand", ["ultimatament", "ultimatatious", "ultimatantial"], ["diplomatic", "latin-origin"]),
    ("compendium", "concise information collection", ["compendament", "compendatious", "compendantial"], ["formal", "latin-origin"]),
    ("standardization", "making things uniform", ["standardizament", "standardizatious", "standardizantial"], ["technical", "suffix"]),
    ("decentralization", "transfer of authority", ["decentralizament", "decentralizatious", "decentralizantial"], ["government", "suffix"]),
    ("unsubstantiated", "not supported by evidence", ["unsubstantiament", "unsubstantiatious", "unsubstantiantial"], ["legal", "suffix"]),
    ("disproportionate", "too large in comparison", ["disproportionant", "disproportionatize", "disproportionament"], ["formal", "suffix"]),
    ("predetermination", "determining in advance", ["predeterminament", "predeterminatious", "predeterminantial"], ["formal", "suffix"]),
    ("miscommunication", "failure to communicate", ["miscommunicament", "miscommunicatious", "miscommunicantial"], ["common", "suffix"]),
]

HARD_WORDS = [
    ("defenestrate", "to throw out of a window", ["defenestrant", "defenestrize", "defenestrament"], ["rare", "latin-origin"]),
    ("sesquipedalian", "characterized by long words", ["sesquipedantic", "sesquipedalious", "sesquipedalment"], ["rare", "latin-origin"]),
    ("absquatulate", "to leave abruptly", ["absquatulant", "absquatulize", "absquatulament"], ["rare", "informal"]),
    ("pusillanimous", "lacking courage", ["pusillanimant", "pusillanimize", "pusillaniment"], ["rare", "latin-origin"]),
    ("perspicacious", "having keen perception", ["perspicaciant", "perspicacize", "perspicaciment"], ["rare", "latin-origin"]),
    ("magnanimous", "generous or forgiving", ["magnanimant", "magnanimize", "magnanimious"], ["formal", "latin-origin"]),
    ("obstreperous", "noisy and difficult", ["obstreperant", "obstreperate", "obstreperious"], ["formal", "latin-origin"]),
    ("loquacious", "very talkative", ["loquaciant", "loquaciate", "loquaciment"], ["formal", "latin-origin"]),
    ("perspicuous", "clearly expressed", ["perspicuant", "perspicuate", "perspicument"], ["formal", "latin-origin"]),
    ("contumacious", "stubbornly resistant", ["contumaciant", "contumaciate", "contumaciment"], ["legal", "latin-origin"]),
    ("desuetude", "state of disuse", ["desuetudent", "desuetudize", "desuetudement"], ["legal", "latin-origin"]),
    ("plenipotentiary", "having full power", ["plenipotentiant", "plenipotentiament", "plenipotentiarous"], ["diplomatic", "latin-origin"]),
    ("usufruct", "right to use another's property", ["usufructant", "usufructize", "usufructament"], ["legal", "latin-origin"]),
    ("demurrer", "a legal objection", ["demurrant", "demurrize", "demurrament"], ["legal", "suffix"]),
    ("mandamus", "court order to act", ["mandamant", "mandamize", "mandameous"], ["legal", "latin-origin"]),
    ("certiorari", "order to review lower court", ["certiorant", "certiorize", "certiorament"], ["legal", "latin-origin"]),
    ("quorum", "minimum members needed", ["quorument", "quorumize", "quorumant"], ["governance", "latin-origin"]),
    ("moratorium", "temporary prohibition", ["moratoriant", "moratoriment", "moratorious"], ["legal", "latin-origin"]),
    ("prorogation", "discontinuing legislature", ["prorogament", "prorogatious", "prorogantial"], ["governance", "latin-origin"]),
    ("pecuniary", "relating to money", ["pecuniant", "pecuniarate", "pecuniament"], ["financial", "latin-origin"]),
    ("impecunious", "having little money", ["impecuniant", "impecuniate", "impecuniament"], ["formal", "latin-origin"]),
    ("eleemosynary", "relating to charity", ["eleemosynant", "eleemosynate", "eleemosynament"], ["rare", "greek-origin"]),
    ("terpsichorean", "relating to dancing", ["terpsichorant", "terpsichorate", "terpsichorement"], ["rare", "greek-origin"]),
    ("penultimate", "second to last", ["penultimant", "penultimatize", "penultimament"], ["formal", "latin-origin"]),
    ("antepenultimate", "third from the end", ["antepenultimant", "antepenultimatize", "antepenultimament"], ["rare", "latin-origin"]),
    ("verisimilitude", "appearance of being true", ["verisimilitudent", "verisimilitudize", "verisimilitudement"], ["formal", "latin-origin"]),
    ("circumlocution", "using many words", ["circumlocutant", "circumlocutize", "circumlocutament"], ["formal", "latin-origin"]),
    ("obfuscation", "making unclear", ["obfuscament", "obfuscatious", "obfuscantial"], ["formal", "latin-origin"]),
    ("conflagration", "an extensive fire", ["conflagrant", "conflagulate", "conflagrament"], ["formal", "latin-origin"]),
    ("perturbation", "disturbance or anxiety", ["perturbament", "perturbatious", "perturbantial"], ["formal", "latin-origin"]),
    ("expostulation", "expressing disagreement", ["expostulament", "expostulatious", "expostulantial"], ["formal", "latin-origin"]),
    ("perambulation", "walking around", ["perambulament", "perambulatious", "perambulantial"], ["formal", "latin-origin"]),
    ("equivocation", "ambiguous language", ["equivocament", "equivocatious", "equivocantial"], ["formal", "latin-origin"]),
    ("tintinnabulation", "ringing sound", ["tintinnabulament", "tintinnabulatious", "tintinnabulantial"], ["rare", "latin-origin"]),
    ("sesquicentennial", "150th anniversary", ["sesquicentenniant", "sesquicentenniate", "sesquicentenniament"], ["formal", "latin-origin"]),
    ("pococurante", "indifferent person", ["pococurantize", "pococurantic", "pococurament"], ["rare", "italian-origin"]),
    ("supererogation", "beyond what is required", ["supererogament", "supererogatious", "supererogantial"], ["formal", "latin-origin"]),
    ("antediluvian", "extremely old-fashioned", ["antediluviant", "antediluviate", "antediluviament"], ["formal", "latin-origin"]),
    ("propinquity", "nearness", ["propinquant", "propinquitate", "propinquiment"], ["formal", "latin-origin"]),
    ("concomitant", "accompanying", ["concomitaneous", "concomitantize", "concomitament"], ["formal", "latin-origin"]),
    ("recalcitrant", "stubbornly resistant", ["recalcitranous", "recalcitrantize", "recalcitrament"], ["formal", "latin-origin"]),
    ("intransigent", "unwilling to compromise", ["intransigentious", "intransigentize", "intransigement"], ["formal", "latin-origin"]),
    ("indefatigable", "persisting tirelessly", ["indefatigant", "indefatigize", "indefatigament"], ["formal", "latin-origin"]),
    ("insouciant", "casual lack of concern", ["insouciantize", "insouciament", "insouciatious"], ["formal", "french-origin"]),
    ("rapprochement", "harmonious relations", ["rapprochant", "rapprochize", "rapprochament"], ["diplomatic", "french-origin"]),
    ("sangfroid", "composure under strain", ["sangfroidant", "sangfroidize", "sangfroidament"], ["formal", "french-origin"]),
    ("nonchalance", "casual indifference", ["nonchalament", "nonchalatious", "nonchalantial"], ["formal", "french-origin"]),
    ("reconnaissance", "military observation", ["reconnaissament", "reconnaissatious", "reconnaissantial"], ["military", "french-origin"]),
    ("pulchritudinous", "beautiful", ["pulchritudinant", "pulchritudinize", "pulchritudinament"], ["rare", "latin-origin"]),
    ("grandiloquent", "pompous language", ["grandiloquant", "grandiloquize", "grandiloquament"], ["formal", "latin-origin"]),
    ("magniloquent", "high-flown language", ["magniloquant", "magniloquize", "magniloquament"], ["formal", "latin-origin"]),
    ("somnambulism", "sleepwalking", ["somnambulant", "somnambulize", "somnambulament"], ["rare", "latin-origin"]),
    ("pusillanimity", "lack of courage", ["pusillanimament", "pusillanimitize", "pusillanimitement"], ["rare", "latin-origin"]),
    ("perspicacity", "keen perception quality", ["perspicacitement", "perspicacitize", "perspicacitament"], ["formal", "latin-origin"]),
    ("magnanimity", "generosity of spirit", ["magnanimitement", "magnanimitize", "magnanimitament"], ["formal", "latin-origin"]),
    ("contumacy", "stubborn resistance", ["contumaciment", "contumacize", "contumacament"], ["legal", "latin-origin"]),
    ("abnegation", "renouncing", ["abnegament", "abnegatious", "abnegantial"], ["formal", "latin-origin"]),
    ("abstemious", "moderate in eating/drinking", ["abstemiousant", "abstemiate", "abstemiament"], ["formal", "latin-origin"]),
    ("apotheosis", "highest point", ["apotheosiant", "apotheosiate", "apotheosiament"], ["formal", "greek-origin"]),
    ("calumny", "false damaging statements", ["calumniant", "calumnize", "calumniament"], ["legal", "latin-origin"]),
    ("capricious", "sudden mood changes", ["capriciousant", "capriciate", "capriciament"], ["formal", "latin-origin"]),
    ("ebullient", "enthusiastic and energetic", ["ebulliament", "ebullientize", "ebullientious"], ["formal", "latin-origin"]),
    ("ephemeral", "lasting briefly", ["ephemerament", "ephemeralize", "ephemerious"], ["formal", "greek-origin"]),
    ("iconoclast", "person who challenges beliefs", ["iconoclastant", "iconoclastize", "iconoclastament"], ["formal", "greek-origin"]),
    ("idiosyncratic", "peculiar to individual", ["idiosyncratant", "idiosyncratize", "idiosyncratament"], ["formal", "greek-origin"]),
    ("incorrigible", "not able to be corrected", ["incorrigibant", "incorrigibize", "incorrigibament"], ["formal", "latin-origin"]),
    ("ineffable", "too great to express", ["ineffabant", "ineffabize", "ineffabament"], ["formal", "latin-origin"]),
    ("obsequious", "excessively eager to please", ["obsequiousant", "obsequiate", "obsequiament"], ["formal", "latin-origin"]),
    ("sycophant", "person who flatters", ["sycophantize", "sycophantious", "sycophantament"], ["formal", "greek-origin"]),
    ("truculent", "eager to fight", ["truculentize", "truculentious", "truculentament"], ["formal", "latin-origin"]),
    ("vituperative", "bitter and abusive", ["vituperatant", "vituperatize", "vituperatament"], ["formal", "latin-origin"]),
    ("sesquicentenary", "150th celebration", ["sesquicentenant", "sesquicentenize", "sesquicentenament"], ["rare", "latin-origin"]),
    ("verisimilar", "appearing true", ["verisimilant", "verisimilize", "verisimilament"], ["formal", "latin-origin"]),
    ("loquaciousness", "quality of being talkative", ["loquaciousament", "loquaciousize", "loquaciousiant"], ["formal", "latin-origin"]),
    ("obstreperousness", "being noisy and difficult", ["obstreperousament", "obstreperousize", "obstreperousiant"], ["formal", "latin-origin"]),
    ("antidisestablishmentarianism", "opposing disestablishment", ["antidisestablishant", "antidisestablishize", "antidisestablishament"], ["rare", "political"]),
]

# Real words used as distractors in "which is NOT real" questions
REAL_WORDS_POOL = [
    "government", "environment", "committee", "assessment", "professional",
    "immediately", "acknowledge", "certificate", "independent", "maintenance",
    "occurrence", "recommend", "permanent", "procedure", "reference",
    "experience", "attendance", "conference", "performance", "compliance",
    "significant", "responsibility", "communication", "opportunity", "administration",
    "organization", "requirement", "development", "management", "achievement",
    "enrollment", "department", "employment", "regulation", "information",
    "application", "examination", "supervision", "preparation", "distribution",
    "adjudicate", "promulgate", "expropriation", "disbursement", "remuneration",
    "requisition", "encumbrance", "appropriation", "jurisprudence", "indemnification",
    "corroborate", "ameliorate", "exacerbate", "concatenate", "prevaricate",
    "confabulate", "tergiversate", "capitulate", "extrapolate", "superannuation",
    "retrenchment", "emolument", "probationary", "commendation", "amortization",
    "liquidation", "expenditure", "procurement", "accreditation", "adjudication",
    "promulgation", "exonerate", "abrogate", "subpoena", "supersede",
    "acquiescence", "malfeasance", "fiduciary", "arbitration", "proliferation",
    "confiscation", "deliberation", "acquittal", "insubordination", "ratification",
    "defenestrate", "sesquipedalian", "pusillanimous", "perspicacious", "magnanimous",
    "obstreperous", "loquacious", "contumacious", "desuetude", "plenipotentiary",
    "usufruct", "demurrer", "mandamus", "certiorari", "quorum", "moratorium",
    "prorogation", "pecuniary", "impecunious", "penultimate", "verisimilitude",
    "circumlocution", "obfuscation", "conflagration", "perturbation", "equivocation",
    "antediluvian", "propinquity", "concomitant", "recalcitrant", "intransigent",
    "indefatigable", "insouciant", "rapprochement", "nonchalance", "reconnaissance",
    "ebullient", "ephemeral", "iconoclast", "obsequious", "sycophant", "truculent",
]

# Non-words for "which is NOT real" and "identify fabricated" questions
NONWORDS = [
    ("administrament", "fabricated — correct form is 'administration'", ["wrong-suffix"]),
    ("consolidature", "fabricated — correct form is 'consolidation'", ["wrong-suffix"]),
    ("remunerant", "fabricated — correct form is 'remunerative'", ["wrong-suffix"]),
    ("promulgant", "fabricated — no such adjective exists", ["wrong-suffix"]),
    ("corroborant", "fabricated — correct form is 'corroborative'", ["wrong-suffix"]),
    ("ameliorant", "fabricated — correct form is 'ameliorative'", ["wrong-suffix"]),
    ("exacerbant", "fabricated — no such adjective exists", ["wrong-suffix"]),
    ("conflagulate", "fabricated — 'conflagration' is the real noun", ["wrong-suffix"]),
    ("gratificent", "fabricated — correct forms are 'gratifying' or 'gratification'", ["wrong-suffix"]),
    ("procrastinous", "fabricated — correct form is 'procrastinating'", ["wrong-suffix"]),
    ("capitulant", "fabricated — correct form is 'capitulation'", ["wrong-suffix"]),
    ("extrapolant", "fabricated — correct form is 'extrapolation'", ["wrong-suffix"]),
    ("insinuant", "fabricated — correct form is 'insinuation'", ["wrong-suffix"]),
    ("expatriant", "fabricated — correct form is 'expatriate'", ["wrong-suffix"]),
    ("concatenant", "fabricated — correct form is 'concatenation'", ["wrong-suffix"]),
    ("prevaricant", "fabricated — correct form is 'prevarication'", ["wrong-suffix"]),
    ("confabulant", "fabricated — correct form is 'confabulation'", ["wrong-suffix"]),
    ("tergiversant", "fabricated — correct form is 'tergiversation'", ["wrong-suffix"]),
    ("obfuscament", "fabricated — correct form is 'obfuscation'", ["wrong-suffix"]),
    ("delinquament", "fabricated — correct form is 'delinquency'", ["wrong-suffix"]),
    ("proliferant", "fabricated — correct form is 'proliferative'", ["wrong-suffix"]),
    ("adjudicament", "fabricated — correct form is 'adjudication'", ["wrong-suffix"]),
    ("expropriament", "fabricated — correct form is 'expropriation'", ["wrong-suffix"]),
    ("disbursation", "fabricated — correct form is 'disbursement'", ["wrong-suffix"]),
    ("requisitament", "fabricated — correct form is 'requisition'", ["wrong-suffix"]),
    ("encumbrement", "fabricated — correct form is 'encumbrance'", ["wrong-suffix"]),
    ("appropriament", "fabricated — correct form is 'appropriation'", ["wrong-suffix"]),
    ("indemnificant", "fabricated — correct form is 'indemnification'", ["wrong-suffix"]),
    ("accreditament", "fabricated — correct form is 'accreditation'", ["wrong-suffix"]),
    ("superannuament", "fabricated — correct form is 'superannuation'", ["wrong-suffix"]),
    ("emolumention", "fabricated — correct form is 'emolument'", ["wrong-suffix"]),
    ("acquiescament", "fabricated — correct form is 'acquiescence'", ["wrong-suffix"]),
    ("malfeasament", "fabricated — correct form is 'malfeasance'", ["wrong-suffix"]),
    ("fiduciant", "fabricated — correct form is 'fiduciary'", ["wrong-suffix"]),
    ("plenipotentiant", "fabricated — correct form is 'plenipotentiary'", ["wrong-suffix"]),
    ("usufructant", "fabricated — correct form is 'usufructuary'", ["wrong-suffix"]),
    ("moratoriant", "fabricated — correct form is 'moratorium'", ["wrong-suffix"]),
    ("prorogament", "fabricated — correct form is 'prorogation'", ["wrong-suffix"]),
    ("pecuniant", "fabricated — correct form is 'pecuniary'", ["wrong-suffix"]),
    ("circumlocutant", "fabricated — correct form is 'circumlocution'", ["wrong-suffix"]),
    ("perturbament", "fabricated — correct form is 'perturbation'", ["wrong-suffix"]),
    ("equivocament", "fabricated — correct form is 'equivocation'", ["wrong-suffix"]),
    ("verisimilitudent", "fabricated — correct form is 'verisimilitude'", ["wrong-suffix"]),
    ("propinquant", "fabricated — correct form is 'propinquity'", ["wrong-suffix"]),
    ("magnanimant", "fabricated — correct form is 'magnanimous'", ["wrong-suffix"]),
    ("perspicaciant", "fabricated — correct form is 'perspicacious'", ["wrong-suffix"]),
    ("pusillanimant", "fabricated — correct form is 'pusillanimous'", ["wrong-suffix"]),
    ("loquaciant", "fabricated — correct form is 'loquacious'", ["wrong-suffix"]),
    ("contumaciant", "fabricated — correct form is 'contumacious'", ["wrong-suffix"]),
    ("recalcitranous", "fabricated — correct form is 'recalcitrant'", ["wrong-suffix"]),
]


def generate_which_is_real(word_entry, qid, difficulty):
    """Generate a 'Which is a real word?' question."""
    real_word, definition, nonwords, tags = word_entry
    choices = nonwords[:3] + [real_word]
    random.shuffle(choices)
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Spelling",
        "subtopic": "Word Recognition",
        "difficulty": difficulty,
        "question": "Which of the following is a REAL English word?",
        "choices": choices,
        "answer": real_word,
        "explanation": f"'{real_word}' means {definition}. The other options are fabricated non-words.",
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English"
    }


def generate_which_is_not_real(real_words_pool, nonword_entry, qid, difficulty, seed_val=0):
    """Generate a 'Which is NOT a real word?' question."""
    nonword, explanation, tags = nonword_entry
    rng = random.Random(hash((nonword, difficulty, seed_val)))
    reals = rng.sample(real_words_pool, 3)
    choices = reals + [nonword]
    rng.shuffle(choices)
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Spelling",
        "subtopic": "Word Recognition",
        "difficulty": difficulty,
        "question": "Which of the following is NOT a real English word?",
        "choices": choices,
        "answer": nonword,
        "explanation": f"'{nonword}' is {explanation}. The other options are all legitimate English words.",
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English"
    }


def generate_identify_legitimate(word_entry, qid, difficulty):
    """Generate a 'Which is a legitimate government/professional term?' question."""
    real_word, definition, nonwords, tags = word_entry
    choices = nonwords[:3] + [real_word]
    random.shuffle(choices)
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Spelling",
        "subtopic": "Word Recognition",
        "difficulty": difficulty,
        "question": "Which of the following is a legitimate term used in government or professional contexts?",
        "choices": choices,
        "answer": real_word,
        "explanation": f"'{real_word}' means {definition}. It is commonly used in official documents. The other options are fabricated.",
        "tags": tags + ["government-context"],
        "category": ["Sub-Professional"],
        "language": "English"
    }


def generate_identify_fabricated(real_words_pool, nonword_entry, qid, difficulty, seed_val=0):
    """Generate an 'Identify the fabricated word' question."""
    nonword, explanation, tags = nonword_entry
    rng = random.Random(hash((nonword, difficulty, "fab", seed_val)))
    reals = rng.sample(real_words_pool, 3)
    choices = reals + [nonword]
    rng.shuffle(choices)
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Spelling",
        "subtopic": "Word Recognition",
        "difficulty": difficulty,
        "question": "Identify the FABRICATED (non-existent) word among the following:",
        "choices": choices,
        "answer": nonword,
        "explanation": f"'{nonword}' is {explanation}. The other options are all real English words.",
        "tags": tags + ["fabricated-detection"],
        "category": ["Sub-Professional"],
        "language": "English"
    }


def main():
    random.seed(42)
    questions = []
    seen_choice_sets = set()

    def add_unique(q):
        # Include full question text in key so same choices with different question types are allowed
        key = (q["question"], tuple(sorted(q["choices"])))
        if key in seen_choice_sets:
            return False
        # Check for duplicate values within choices
        if len(set(q["choices"])) != 4:
            return False
        seen_choice_sets.add(key)
        questions.append(q)
        return True

    # =========================================================================
    # EASY (200 questions)
    # =========================================================================
    easy_shuffled = list(EASY_WORDS)
    random.shuffle(easy_shuffled)
    
    # Use full bank for both question types (different question text = different question)
    # 100x "Which is a REAL English word?"
    for entry in easy_shuffled[:100]:
        q = generate_which_is_real(entry, 0, "Easy")
        add_unique(q)

    # 50x "Which is NOT a real English word?"
    count = 0
    for i in range(200):
        nw = NONWORDS[i % len(NONWORDS)]
        q = generate_which_is_not_real(REAL_WORDS_POOL[:50], nw, 0, "Easy", seed_val=i)
        if add_unique(q):
            count += 1
            if count >= 50:
                break

    # 50x "Which is a legitimate term?" — reuses same words but different question text
    for entry in easy_shuffled[:50]:
        q = generate_identify_legitimate(entry, 0, "Easy")
        add_unique(q)

    easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
    print(f"  Easy: {easy_count}")

    # =========================================================================
    # MEDIUM (200 questions)
    # =========================================================================
    medium_shuffled = list(MEDIUM_WORDS)
    random.shuffle(medium_shuffled)
    
    medium_real = medium_shuffled[:80]

    # 80x "Which is a REAL English word?"
    for entry in medium_real:
        q = generate_which_is_real(entry, 0, "Medium")
        add_unique(q)

    # 50x "Which is NOT a real English word?"
    count = 0
    for i in range(500):
        nw = NONWORDS[i % len(NONWORDS)]
        q = generate_which_is_not_real(REAL_WORDS_POOL, nw, 0, "Medium", seed_val=i + 1000)
        if add_unique(q):
            count += 1
            if count >= 50:
                break

    # 40x "Identify the FABRICATED word"
    count = 0
    for i in range(500):
        nw = NONWORDS[i % len(NONWORDS)]
        q = generate_identify_fabricated(REAL_WORDS_POOL, nw, 0, "Medium", seed_val=i + 2000)
        if add_unique(q):
            count += 1
            if count >= 40:
                break

    # 35x "Which is a legitimate term?"
    legit_count = 0
    legit_rejected = 0
    for entry in medium_shuffled[40:75]:
        q = generate_identify_legitimate(entry, 0, "Medium")
        if add_unique(q):
            legit_count += 1
        else:
            legit_rejected += 1
            if len(set(q["choices"])) != 4:
                print(f"    REJECTED (dup choices): {q['choices']}")
    print(f"    Medium legit: added={legit_count}, rejected={legit_rejected}")

    medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
    print(f"  Medium: {medium_count}")

    # =========================================================================
    # HARD (200 questions)
    # =========================================================================
    hard_shuffled = list(HARD_WORDS)
    random.shuffle(hard_shuffled)
    
    hard_real = hard_shuffled[:80]

    # 80x "Which is a REAL English word?"
    for entry in hard_real:
        q = generate_which_is_real(entry, 0, "Hard")
        add_unique(q)

    # 50x "Which is NOT a real English word?"
    count = 0
    for i in range(500):
        nw = NONWORDS[i % len(NONWORDS)]
        q = generate_which_is_not_real(REAL_WORDS_POOL, nw, 0, "Hard", seed_val=i + 3000)
        if add_unique(q):
            count += 1
            if count >= 50:
                break

    # 40x "Identify the FABRICATED word"
    count = 0
    for i in range(500):
        nw = NONWORDS[i % len(NONWORDS)]
        q = generate_identify_fabricated(REAL_WORDS_POOL, nw, 0, "Hard", seed_val=i + 4000)
        if add_unique(q):
            count += 1
            if count >= 40:
                break

    # 34x "Which is a legitimate term?"
    legit_count_h = 0
    legit_rejected_h = 0
    for entry in hard_shuffled[40:74]:
        q = generate_identify_legitimate(entry, 0, "Hard")
        if add_unique(q):
            legit_count_h += 1
        else:
            legit_rejected_h += 1
            if len(set(q["choices"])) != 4:
                print(f"    REJECTED (dup choices): {q['choices']}")
    print(f"    Hard legit: added={legit_count_h}, rejected={legit_rejected_h}")

    hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
    print(f"  Hard: {hard_count}")

    # =========================================================================
    # Final assignment of sequential IDs
    # =========================================================================
    for i, q in enumerate(questions):
        q["id"] = i + 1

    total = len(questions)
    easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
    medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
    
    print(f"\n  Total: {total} (Easy={easy_count}, Medium={medium_count}, Hard={hard_count})")

    assert total == 600, f"Expected 600 questions, got {total}"
    assert easy_count == 200, f"Expected 200 Easy, got {easy_count}"
    assert medium_count == 200, f"Expected 200 Medium, got {medium_count}"
    assert hard_count == 200, f"Expected 200 Hard, got {hard_count}"

    # Verify all answers in choices and no intra-question duplicates
    for q in questions:
        assert q["answer"] in q["choices"], f"Q{q['id']}: answer not in choices"
        assert len(q["choices"]) == 4, f"Q{q['id']}: not 4 choices"
        assert len(set(q["choices"])) == 4, f"Q{q['id']}: duplicate choices"

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability", "spelling", "word-recognition"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Generated {total} unique questions")
    print(f"   Output: {output_path}")


if __name__ == "__main__":
    main()
