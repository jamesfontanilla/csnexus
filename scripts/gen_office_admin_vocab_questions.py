"""
Generate 600 questions for Office and Administrative Vocabulary lesson.
200 Easy, 200 Medium, 200 Hard.

Question types:
- "Which of the following is spelled correctly?" (correct answer among misspellings)
- "Which of the following is spelled incorrectly?" (misspelling among correct words)
- "Choose the correctly spelled word to complete the sentence." (Medium/Hard)
- "Identify the misspelled word in the sentence." (Hard)

All words are office/administrative vocabulary used in Philippine government context.
"""

import json
import random
import os

random.seed(42)

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "seed", "questions", "clerical-ability", "spelling",
    "office-and-administrative-vocabulary"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


def make_q(id_num, difficulty, question, choices, answer, explanation, tags):
    return {
        "id": id_num,
        "subtest": "Clerical Ability",
        "module": "Spelling",
        "subtopic": "Office and Administrative Vocabulary",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English"
    }


# ============================================================================
# WORD BANKS — Format: (correct, [misspelling1, misspelling2, misspelling3], explanation, [tags])
# ============================================================================

# --- EASY: Common office words, single error type, obvious differences ---
EASY_WORDS = [
    ("memorandum", ["memorandom", "memorandem", "memorandm"], "Latin ending -andum (like referendum).", ["correspondence", "latin-origin"]),
    ("endorsement", ["endorcement", "indorsment", "endorsment"], "En + dorse + ment — keep the e before -ment.", ["correspondence", "suffix-rule"]),
    ("correspondence", ["correspondance", "correspondense", "corespondence"], "Correspond + ence — stressed final syllable takes -ence.", ["correspondence", "suffix-confusion"]),
    ("communication", ["comunication", "commuication", "communicaton"], "Double m, single n — com-mu-ni-ca-tion.", ["correspondence", "double-letter"]),
    ("recommendation", ["recomendation", "reccommendation", "recommandation"], "One c in re-, double m in commend.", ["correspondence", "double-letter"]),
    ("circular", ["circuler", "circlar", "circullar"], "Circul + ar ending (like regular).", ["correspondence", "unstressed-vowel"]),
    ("transmittal", ["transmital", "transmittall", "tranmittal"], "Transmit + tal — double t from doubling rule.", ["correspondence", "consonant-doubling"]),
    ("disbursement", ["disbursment", "disburcement", "disbursemant"], "Disburse + ment — keep the e before consonant suffix.", ["finance", "final-e-rule"]),
    ("expenditure", ["expinditure", "expendature", "expendeture"], "Expend + iture (like furniture).", ["finance", "unstressed-vowel"]),
    ("allotment", ["alotment", "allottment", "alottment"], "Double l, single t — allot + ment.", ["finance", "double-letter"]),
    ("appropriation", ["apropiation", "appropreation", "appropriaton"], "Double p + -iation ending.", ["finance", "double-letter"]),
    ("remittance", ["remitance", "remittence", "remitence"], "Double t + -ance ending (remit → remittance).", ["finance", "consonant-doubling"]),
    ("assessment", ["assesment", "assessement", "asessment"], "Assess has double s twice: as-sess-ment.", ["finance", "double-letter"]),
    ("personnel", ["personel", "personell", "personnell"], "Double n, single l — French origin.", ["human-resources", "double-letter"]),
    ("appointment", ["apointment", "appointtment", "appoitment"], "Double p — ap + point + ment.", ["human-resources", "double-letter"]),
    ("resignation", ["resignition", "resignasion", "resigation"], "Resign + ation — silent g stays.", ["human-resources", "silent-letter"]),
    ("eligibility", ["elegibility", "eligiblity", "eligibilty"], "Elig + ibility — all i vowels.", ["human-resources", "unstressed-vowel"]),
    ("grievance", ["greivance", "grievence", "grievanse"], "Grieve + ance — ie not ei; -ance not -ence.", ["human-resources", "suffix-confusion"]),
    ("suspension", ["suspencion", "suspention", "suspenson"], "Suspend → suspension — d becomes -sion.", ["human-resources", "suffix-confusion"]),
    ("negligence", ["negligance", "neglegence", "negligense"], "Neglig + ence — not -ance.", ["human-resources", "suffix-confusion"]),
    ("resolution", ["resolusion", "resolucion", "resoluton"], "Resolut + ion — standard -tion ending.", ["legal", "suffix-confusion"]),
    ("compliance", ["complience", "compiance", "complianse"], "Comply → compli + ance.", ["legal", "suffix-confusion"]),
    ("implementation", ["implementasion", "implimentation", "implementaton"], "Implement + ation — not -asion.", ["legal", "suffix-confusion"]),
    ("accreditation", ["acreditation", "acreditasion", "accreditasion"], "Double c — ac + credit + ation.", ["legal", "double-letter"]),
    ("certification", ["certificasion", "certifcation", "certificaton"], "Certif + ication — not -asion.", ["legal", "suffix-confusion"]),
    ("authorization", ["authorisation", "authorizasion", "authorazation"], "Authorize + ation — American English uses -ize.", ["legal", "suffix-confusion"]),
    ("documentation", ["documentasion", "documention", "documentaton"], "Document + ation — full root + -ation.", ["records", "suffix-confusion"]),
    ("classification", ["classifcation", "classificasion", "clasification"], "Classif + ication — double s in class.", ["records", "double-letter"]),
    ("maintenance", ["maintainence", "maintanance", "maintenence"], "Irregular: maintain → mainten + ance.", ["records", "suffix-confusion"]),
    ("preliminary", ["preliminery", "prelimnary", "prelimminary"], "Prelimin + ary — not -ery.", ["records", "unstressed-vowel"]),
    ("equipment", ["equippment", "equipement", "equiptment"], "Equip + ment — single p before -ment.", ["office-supplies", "consonant-doubling"]),
    ("stationery", ["stationary", "stationairy", "stationerry"], "StationERy = papER (office supplies, not 'not moving').", ["office-supplies", "confused-pair"]),
    ("envelope", ["envalope", "envelop", "envellope"], "Envel + ope (noun); 'envelop' is the verb.", ["office-supplies", "confused-pair"]),
    ("fluorescent", ["florescent", "flourescent", "fluoresent"], "Fluor + escent — like fluoride.", ["office-supplies", "silent-letter"]),
    ("calculator", ["calculater", "calcualtor", "calcultor"], "Calcul + ator (not -ater).", ["office-supplies", "unstressed-vowel"]),
    ("itinerary", ["itinarary", "itineraray", "itinery"], "Latin iter (journey) — i-tin-er-ar-y.", ["meetings", "unstressed-vowel"]),
    ("conference", ["conferance", "confrence", "conferense"], "Confer + ence — stressed final syllable.", ["meetings", "suffix-confusion"]),
    ("liaison", ["liason", "liasion", "laison"], "French origin — vowel cluster l-i-a-i-s-o-n.", ["meetings", "foreign-origin"]),
    ("agenda", ["aganda", "aggenda", "agender"], "Latin 'things to do' — one g.", ["meetings", "latin-origin"]),
    ("superintendent", ["superintendant", "superindendent", "superintendint"], "Super + intend + ent — stressed → -ent.", ["positions", "suffix-confusion"]),
    ("commissioner", ["commisioner", "comissioner", "commisionner"], "Double m + double s — com-mis-sion-er.", ["positions", "double-letter"]),
    ("administrator", ["administator", "adminstrator", "administrater"], "Administer → administr + ator.", ["positions", "unstressed-vowel"]),
    ("secretary", ["secretery", "secratary", "secretrary"], "Secret + ary — not -ery.", ["positions", "unstressed-vowel"]),
    ("treasurer", ["treasuerer", "tresurer", "treasuer"], "Treasure + r — keep the e.", ["positions", "final-e-rule"]),
    ("bureaucracy", ["beauracracy", "burocracy", "beurocracy"], "Bureau (French) + cracy (Greek).", ["policy", "foreign-origin"]),
    ("hierarchy", ["heirarchy", "hierarcy", "hierachy"], "Hier + archy — Greek hieros (sacred).", ["policy", "foreign-origin"]),
    ("infrastructure", ["infrastracture", "infrustructure", "infastructure"], "Infra + structure — Latin 'below.'", ["policy", "prefix-error"]),
    ("requisition", ["requisiton", "requsition", "requisision"], "Requis + ition — like acquisition.", ["procurement", "unstressed-vowel"]),
    ("acquisition", ["aquisition", "acqusition", "aquisision"], "Ac + quis + ition — cqu cluster.", ["procurement", "silent-letter"]),
    ("specification", ["specificaton", "specfication", "specifcation"], "Specific + ation — full root kept.", ["procurement", "suffix-confusion"]),
    # Additional Easy words
    ("memoranda", ["memorandas", "memorandums", "memorandae"], "Latin plural of memorandum: -um → -a.", ["correspondence", "latin-origin"]),
    ("addendum", ["adendum", "addenddum", "addendem"], "Add + endum — double d.", ["correspondence", "double-letter"]),
    ("verbatim", ["verbatum", "verbetim", "verbatam"], "Latin 'word for word' — verb + atim.", ["correspondence", "latin-origin"]),
    ("quorum", ["quarum", "quorom", "quoram"], "Latin 'of whom' — quo + rum.", ["meetings", "latin-origin"]),
    ("curriculum", ["curiculum", "curriculm", "curricullum"], "Double r, single l — Latin origin.", ["correspondence", "double-letter"]),
    ("reimbursement", ["reimbursment", "riembursement", "reimbursemant"], "Reimburse + ment — keep the e.", ["finance", "final-e-rule"]),
    ("procurement", ["procurment", "proccurement", "procuremant"], "Procure + ment — keep the e.", ["procurement", "final-e-rule"]),
    ("collateral", ["colateral", "collatteral", "colatteral"], "Double l, single t — col-lat-er-al.", ["finance", "double-letter"]),
    ("reconciliation", ["reconcilliation", "reconceliation", "reconcilition"], "Reconcili + ation — single l.", ["finance", "double-letter"]),
    ("voucher", ["vaucher", "vouchar", "vouchur"], "Vouch + er — ou, not au.", ["finance", "unstressed-vowel"]),
    ("inventory", ["invetory", "inventroy", "inventry"], "Invent + ory — all syllables present.", ["procurement", "silent-letter"]),
    ("solicitation", ["solisitation", "solicitasion", "solicatation"], "Solicit + ation — not -asion.", ["procurement", "suffix-confusion"]),
    ("quotation", ["qoutation", "quotasion", "qutation"], "Quot + ation — qu not qou.", ["procurement", "suffix-confusion"]),
    ("appraisal", ["apprasial", "appraisel", "apprasal"], "Apprais + al — like approval.", ["human-resources", "transposition"]),
    ("commendation", ["comendation", "commendacion", "comendacion"], "Com + mend + ation — double m.", ["human-resources", "double-letter"]),
    ("proficiency", ["proficency", "profficiency", "proficeincy"], "Profici + ency — one f.", ["human-resources", "double-letter"]),
    ("supervisor", ["superviser", "supperviser", "supervizar"], "Supervis + or — not -er.", ["positions", "unstressed-vowel"]),
    ("ordinance", ["ordanance", "ordinence", "ordinanse"], "Ordin + ance — not -ence.", ["legal", "suffix-confusion"]),
    ("jurisdiction", ["jurisdicton", "jursidiction", "jurisdicion"], "Juris + diction — Latin 'law + speaking.'", ["legal", "latin-origin"]),
    ("promulgation", ["promulgasion", "promulguation", "promulgaton"], "Promulg + ation — not -asion.", ["legal", "suffix-confusion"]),
    ("ratification", ["ratificasion", "rattification", "ratifcation"], "Ratif + ication — single t.", ["legal", "suffix-confusion"]),
    ("alphabetical", ["alphabetcal", "alphbetical", "alphabeticall"], "Alphabet + ical — full root.", ["records", "suffix-confusion"]),
    ("chronological", ["cronological", "chronologcal", "chronoligical"], "Chrono + logical — Greek chronos (time).", ["records", "silent-letter"]),
    ("miscellaneous", ["miscelaneous", "miscellanious", "miscelleanous"], "Miscell + aneous — double l, -eous.", ["records", "double-letter"]),
    ("sequential", ["sequensial", "sequental", "sequencial"], "Sequent + ial — not -sial.", ["records", "suffix-confusion"]),
    ("supplementary", ["supplementry", "supplimentary", "supplimentery"], "Supplement + ary — not -ery.", ["records", "unstressed-vowel"]),
    ("temporary", ["temprary", "temporery", "temporrary"], "Tempor + ary — not -ery.", ["records", "unstressed-vowel"]),
    ("auxiliary", ["auxillary", "auxilary", "auxilliary"], "Auxili + ary — single l.", ["records", "double-letter"]),
    ("apparatus", ["apperatus", "aparatus", "apparattus"], "Ap + parat + us — double p, single t.", ["office-supplies", "double-letter"]),
    ("facsimile", ["facimile", "facsimilie", "faximile"], "Fac + simile — Latin 'make similar.'", ["office-supplies", "latin-origin"]),
    ("paraphernalia", ["paraphenalia", "paraphranalia", "paraphanalia"], "Para + phern + alia — Greek origin.", ["office-supplies", "foreign-origin"]),
    ("adhesive", ["adhessive", "adheesive", "adheseve"], "Ad + hesive — single s.", ["office-supplies", "double-letter"]),
    ("cartridge", ["catridge", "cartrige", "cardridge"], "Cart + ridge — not 'card.'", ["office-supplies", "silent-letter"]),
    ("scissors", ["scisors", "sissors", "scizzors"], "Sc + issors — silent c, double s.", ["office-supplies", "silent-letter"]),
    ("seminar", ["semminar", "semnar", "seminnar"], "Semin + ar — single m.", ["meetings", "double-letter"]),
    ("symposium", ["simposium", "symopsium", "symposeum"], "Sym + posium — Greek 'drinking together.'", ["meetings", "foreign-origin"]),
    ("plenary", ["plennary", "plenery", "pleanary"], "Plen + ary — Latin plenus (full).", ["meetings", "latin-origin"]),
    ("registrar", ["registrer", "registar", "registrrar"], "Registr + ar — not -er.", ["positions", "unstressed-vowel"]),
    ("comptroller", ["comptroler", "comptoller", "comptrollor"], "Variant of controller — silent p retained.", ["positions", "silent-letter"]),
    ("constituency", ["constituancy", "constiuency", "constitutency"], "Constitu + ency — not -ancy.", ["policy", "suffix-confusion"]),
    ("prerogative", ["perogative", "prerrogative", "prerogitive"], "Pre + rogative — Latin rogare (to ask).", ["policy", "prefix-error"]),
    ("prerequisite", ["prerequiste", "prerequsite", "prerequiset"], "Pre + requisite — one word.", ["policy", "prefix-error"]),
    ("entrepreneur", ["entrepeneur", "entrepraneur", "entreprenuer"], "French: entre + preneur (between + taker).", ["policy", "foreign-origin"]),
    ("confidential", ["confidensial", "confidentail", "confidencial"], "Confident + ial — not -sial.", ["legal", "suffix-confusion"]),
    ("surveillance", ["surveilance", "surveillence", "survellance"], "French surveiller → -ance; double l.", ["legal", "foreign-origin"]),
    ("verification", ["verificasion", "verifcation", "verificaton"], "Verif + ication — not -asion.", ["legal", "suffix-confusion"]),
    ("notarization", ["notarizasion", "notoriztion", "notarisation"], "Notarize + ation — American -ize.", ["legal", "suffix-confusion"]),
    ("receivable", ["recievable", "receiveable", "recieveable"], "ei after c; drop e before -able.", ["finance", "ie-ei-rule"]),
    ("delinquent", ["deliquent", "delinqent", "deliquint"], "De + linqu + ent — u always after q.", ["finance", "silent-letter"]),
    ("deficiency", ["deficency", "defficiency", "deficiancy"], "Defici + ency — one f, -ency.", ["finance", "suffix-confusion"]),
    ("liquidation", ["liqudation", "liquidasion", "liquedation"], "Liquid + ation — qu cluster preserved.", ["finance", "suffix-confusion"]),
    ("amortization", ["amortiztion", "amortisation", "amortazation"], "Amortize + ation — American -ize.", ["finance", "suffix-confusion"]),
]

# --- MEDIUM: Two comparison steps, sentence context, government terms ---
MEDIUM_WORDS = [
    ("remuneration", ["renumeration", "remunaration", "remnuneration"], "From Latin munus (gift) — re-mu-ner-ation, not re-nu-mer.", ["human-resources", "transposition"]),
    ("insubordination", ["insubordiantion", "insubbordination", "insubordnation"], "In + subordin + ation — correct vowel sequence.", ["human-resources", "transposition"]),
    ("probationary", ["probationery", "probationnary", "probatinary"], "Probation + ary — not -ery.", ["human-resources", "suffix-confusion"]),
    ("absenteeism", ["absentism", "absenteism", "absenteeizm"], "Absentee + ism — keep double e.", ["human-resources", "suffix-confusion"]),
    ("disciplinary", ["discplinary", "disciplinery", "disiplinary"], "Disciplin + ary — sc cluster.", ["human-resources", "silent-letter"]),
    ("satisfactory", ["satisfactry", "satisfaktory", "sattisfactory"], "Satisfact + ory — one t in sat.", ["human-resources", "unstressed-vowel"]),
    ("tardiness", ["terrdiness", "tradiness", "tardinness"], "Tardy → tard + iness — single d.", ["human-resources", "consonant-doubling"]),
    ("meritorious", ["meritourous", "meritorius", "meritoreous"], "Merit + orious — standard -ious.", ["human-resources", "suffix-confusion"]),
    ("competency", ["competancy", "compentency", "competensy"], "Compet + ency — not -ancy.", ["human-resources", "suffix-confusion"]),
    ("subpoena", ["subpena", "supboena", "subpeona"], "Latin sub + poena (penalty) — silent b retained.", ["legal", "latin-origin"]),
    ("indictment", ["inditement", "indictmant", "indicment"], "Silent c — in-dict-ment.", ["legal", "silent-letter"]),
    ("acquittal", ["aquital", "acquital", "acquittall"], "Ac + quit + double t + al.", ["legal", "consonant-doubling"]),
    ("affidavit", ["afidavit", "affadavit", "afidavvit"], "Double f + i in third syllable (not a).", ["legal", "double-letter"]),
    ("adjudication", ["ajudication", "adjudikation", "adjudicasion"], "Ad + judic + ation — Latin 'to judge.'", ["legal", "latin-origin"]),
    ("stipulation", ["stipullation", "stipulasion", "stippulation"], "Stipul + ation — single l, single p.", ["legal", "double-letter"]),
    ("promulgation", ["promulgasion", "promullgation", "promulguation"], "Promulg + ation — standard -tion.", ["legal", "suffix-confusion"]),
    ("defendant", ["defendent", "defandant", "defendint"], "Defend + ant — ends in -ant.", ["legal", "suffix-confusion"]),
    ("plaintiff", ["plaintif", "plantiff", "plaintiffe"], "Plain + tiff — double f at end.", ["legal", "double-letter"]),
    ("surcharge", ["surchage", "surcharrge", "surrcharge"], "Sur + charge — single r.", ["finance", "double-letter"]),
    ("depreciation", ["depriciation", "depreciasion", "depreshiation"], "Depreci + ation — different from 'deprecation.'", ["finance", "unstressed-vowel"]),
    ("fiduciary", ["fiducary", "fiduceary", "fidusiary"], "Fiduci + ary — Latin fides (trust).", ["finance", "latin-origin"]),
    ("ledger", ["legder", "ledgr", "letger"], "Ledg + er — dg cluster.", ["finance", "transposition"]),
    ("revenue", ["revnue", "reveue", "revanue"], "Reven + ue — French ending.", ["finance", "unstressed-vowel"]),
    ("consignment", ["consigment", "consignement", "consignmant"], "Consign + ment — silent g stays.", ["procurement", "silent-letter"]),
    ("canvass", ["canvas", "canvus", "canvase"], "Canvass = to survey (double s); canvas = cloth.", ["procurement", "confused-pair"]),
    ("bidder", ["bider", "biddr", "biddor"], "Bid + der — double d from doubling rule.", ["procurement", "consonant-doubling"]),
    ("tabulation", ["tabulasion", "tabullation", "tabualtion"], "Tabul + ation — single l.", ["records", "double-letter"]),
    ("disposition", ["disposision", "dispostion", "desposition"], "Dispos + ition — standard -ition.", ["records", "suffix-confusion"]),
    ("retrieval", ["retreival", "retrival", "retreval"], "Retrieve → retriev + al — ie not ei.", ["records", "ie-ei-rule"]),
    ("systematic", ["systimatic", "systematik", "systammatic"], "System + atic — e in second syllable.", ["records", "unstressed-vowel"]),
    ("subsidiary", ["subsidary", "subsiduary", "subsideary"], "Subsidi + ary — all i's.", ["records", "unstressed-vowel"]),
    ("colloquium", ["coloquium", "colloquim", "colloqium"], "Col + loqui + um — double l, qu.", ["meetings", "double-letter"]),
    ("convene", ["convein", "conviene", "conveen"], "Con + vene — Latin venire (to come).", ["meetings", "latin-origin"]),
    ("cellophane", ["celophane", "cellofane", "cellophain"], "Cello + phane — double l, ph.", ["office-supplies", "double-letter"]),
    ("laminate", ["lamenate", "laminnate", "laminait"], "Lamin + ate — single n.", ["office-supplies", "double-letter"]),
    ("manila", ["manilla", "manela", "mannila"], "From Manila, Philippines — single l.", ["office-supplies", "double-letter"]),
    ("tarpaulin", ["tarpauline", "terpollin", "tarpolin"], "Tar + paul + in — au vowel cluster.", ["office-supplies", "unstressed-vowel"]),
    ("peripheral", ["periferal", "periphrial", "perepheral"], "Peripher + al — ph = f sound.", ["office-supplies", "silent-letter"]),
    ("photocopier", ["photocoppier", "photocopyer", "photocpier"], "Photo + copi + er — single p.", ["office-supplies", "consonant-doubling"]),
    ("bureaucrat", ["beaurocrat", "burocrat", "beurocrat"], "Bureau + crat — French bureau.", ["positions", "foreign-origin"]),
    ("ombudsman", ["ombusman", "ombudsmen", "ombudzman"], "Swedish origin — -ds- cluster.", ["positions", "foreign-origin"]),
    ("undersecretary", ["under-secretary", "undersecratary", "undersecretry"], "One word; under + secretary.", ["positions", "compound-word"]),
    ("memorandum circular", ["memorandom circular", "memorandum circuler", "memorandem circular"], "Memorandum (Latin -um) + circular.", ["correspondence", "latin-origin"]),
    ("prerequisite", ["pre-requisite", "prerequiste", "prerequsite"], "One word: pre + requisite.", ["policy", "compound-word"]),
    ("entrepreneur", ["entrepeneur", "entrepraneur", "entreprenure"], "French entre + preneur (taker).", ["policy", "foreign-origin"]),
    # Sentence-based medium questions (stored differently, processed later)
    ("questionnaire", ["questionaire", "questionnare", "questionairre"], "French origin — double n + -aire ending.", ["correspondence", "foreign-origin"]),
    ("per diem", ["perdiem", "per deim", "per deum"], "Two words; Latin 'per day.'", ["finance", "latin-origin"]),
    ("pro rata", ["prorata", "pro-rata", "pro ratta"], "Two words; Latin 'proportionally.'", ["finance", "latin-origin"]),
    ("ad hoc", ["adhoc", "ad-hoc", "ad hock"], "Two words; Latin 'for this purpose.'", ["policy", "latin-origin"]),
    ("bona fide", ["bonafide", "bona-fide", "bonified"], "Two words; Latin 'in good faith.'", ["legal", "latin-origin"]),
    ("de facto", ["defacto", "de-facto", "de fakto"], "Two words; Latin 'in practice.'", ["legal", "latin-origin"]),
    ("ex officio", ["ex-officio", "exofficio", "ex oficio"], "Two words; Latin 'by virtue of office.'", ["positions", "latin-origin"]),
    ("status quo", ["statusquo", "status-quo", "statis quo"], "Two words; Latin 'existing state.'", ["policy", "latin-origin"]),
    ("vice versa", ["visa versa", "vice-versa", "vise versa"], "Two words; Latin 'the other way around.'", ["correspondence", "latin-origin"]),
    ("modus operandi", ["modus operande", "modus operandee", "modis operandi"], "Latin 'method of operating' — -andi ending.", ["legal", "latin-origin"]),
    ("in lieu", ["in liew", "inlieu", "in leiu"], "Two words; French/Latin 'in place of.'", ["correspondence", "foreign-origin"]),
    ("per annum", ["perannum", "per-annum", "per anum"], "Two words; Latin 'per year' — double n.", ["finance", "latin-origin"]),
    ("esprit de corps", ["esprit de core", "esprit de corpse", "esprit de corp"], "French 'group spirit' — corps (silent ps).", ["policy", "foreign-origin"]),
    ("fait accompli", ["fate accompli", "fait acompli", "fait accomplie"], "French 'accomplished fact' — silent t in fait.", ["policy", "foreign-origin"]),
    ("carte blanche", ["cart blanche", "carte blance", "carte blanch"], "French 'blank card' — complete freedom.", ["policy", "foreign-origin"]),
    ("rapport", ["raport", "rappor", "rapore"], "French — double p, silent t.", ["meetings", "foreign-origin"]),
    ("attaché", ["attache", "atache", "attachee"], "French — double t, accent on é.", ["positions", "foreign-origin"]),
    ("laissez-faire", ["laisez faire", "laissez-fair", "lassez-faire"], "French 'let do' — double s, hyphenated.", ["policy", "foreign-origin"]),
    # More government-specific terms
    ("appropriation", ["apropiation", "appropreation", "appropriaton"], "Double p + -iation ending.", ["finance", "double-letter"]),
    ("disbursement", ["disbursment", "disbersement", "disburcement"], "Disburse + ment — keep the e.", ["finance", "final-e-rule"]),
    ("personnel", ["personel", "personnell", "personell"], "Double n, single l — French origin.", ["human-resources", "double-letter"]),
    ("accommodation", ["accomodation", "accommadation", "acomodation"], "Double c AND double m — Latin ad + com.", ["office-supplies", "double-letter"]),
    ("correspondence", ["correspondance", "corespondence", "corrispondence"], "Correspond + ence — stressed syllable → -ence.", ["correspondence", "suffix-confusion"]),
    ("superintendent", ["superintendant", "superindendent", "superintendint"], "Super + intend + ent — stressed → -ent.", ["positions", "suffix-confusion"]),
    ("liaison", ["liason", "liasion", "laision"], "French — vowel cluster i-a-i.", ["meetings", "foreign-origin"]),
    ("bureaucracy", ["beauracracy", "burocracy", "beaurocracy"], "Bureau + cracy — French + Greek.", ["policy", "foreign-origin"]),
    ("maintenance", ["maintainence", "maintenence", "maintanance"], "Irregular: maintain → mainten + ance.", ["records", "suffix-confusion"]),
    ("requisition", ["requisiton", "requsition", "requisision"], "Requis + ition — like acquisition.", ["procurement", "unstressed-vowel"]),
    # More medium
    ("acknowledgment", ["acknowledgement", "acknowlegment", "acknowledgmant"], "American English drops e: acknowledge + ment.", ["correspondence", "final-e-rule"]),
    ("enclosure", ["encloseure", "inclosure", "enclosire"], "En + clos(e) + ure — standard formation.", ["correspondence", "prefix-error"]),
    ("errata", ["erata", "eratta", "errada"], "Double r, single t — Latin 'errors.'", ["correspondence", "double-letter"]),
    ("pro forma", ["proforma", "pro-forma", "pro fourma"], "Two words; Latin 'for form's sake.'", ["finance", "latin-origin"]),
    ("competency", ["competancy", "compitency", "compentency"], "Compet + ency — not -ancy.", ["human-resources", "suffix-confusion"]),
    ("insubordination", ["insubordiantion", "insubbordination", "insubordinasion"], "In + subordin + ation — standard formation.", ["human-resources", "suffix-confusion"]),
    ("promulgation", ["promulgasion", "promullgation", "promulgution"], "Promulg + ation — not -asion.", ["legal", "suffix-confusion"]),
    ("adjudication", ["ajudication", "adjudicasion", "adjuddication"], "Ad + judic + ation — Latin origin.", ["legal", "latin-origin"]),
    ("ratification", ["ratificasion", "rattification", "ratifacation"], "Ratif + ication — single t.", ["legal", "suffix-confusion"]),
    ("reconciliation", ["reconcilliation", "reconceliation", "reconciliasion"], "Reconcili + ation — single l.", ["finance", "double-letter"]),
    ("depreciation", ["depriciation", "depreciasion", "depreshiation"], "Depreci + ation — e not i.", ["finance", "unstressed-vowel"]),
    ("amortization", ["amortiztion", "amortazation", "amortisasion"], "Amortize + ation — American -ize.", ["finance", "suffix-confusion"]),
    ("specification", ["specificaton", "specifcation", "specificasion"], "Specific + ation — not -asion.", ["procurement", "suffix-confusion"]),
    ("solicitation", ["solisitation", "solicitasion", "solicatation"], "Solicit + ation — not -asion.", ["procurement", "suffix-confusion"]),
    ("chronological", ["cronological", "chronologcal", "chronoligical"], "Chrono + logical — ch = k sound.", ["records", "silent-letter"]),
    ("miscellaneous", ["miscelaneous", "miscellainous", "miscellanious"], "Miscell + aneous — double l, -eous.", ["records", "double-letter"]),
    ("supplementary", ["supplementry", "supplimentary", "supplimentery"], "Supplement + ary — not -ery.", ["records", "unstressed-vowel"]),
    ("paraphernalia", ["paraphenalia", "paraphranalia", "paraphanalia"], "Para + phern + alia — Greek origin.", ["office-supplies", "foreign-origin"]),
    ("fluorescent", ["florescent", "flourescent", "fluoresent"], "Fluor + escent — like fluoride.", ["office-supplies", "silent-letter"]),
    ("symposium", ["simposium", "symopsium", "symposeum"], "Sym + posium — Greek origin.", ["meetings", "foreign-origin"]),
]

# --- HARD: Multiple rules, subtle differences, sentence context, traps ---
HARD_WORDS = [
    ("remuneration", ["renumeration", "remunaration", "remnuneration"], "Latin munus (gift) — mu-ner, NOT nu-mer. Commonly swapped.", ["human-resources", "transposition"]),
    ("questionnaire", ["questionaire", "questionnare", "questionairre"], "French double n + -aire. Most commonly misspelled admin word.", ["correspondence", "foreign-origin"]),
    ("accommodation", ["accomodation", "accommadation", "acomodation"], "Latin ad + com → acc + comm. Double c AND double m.", ["office-supplies", "double-letter"]),
    ("indemnification", ["indemnificasion", "indemnifcation", "indemnifikation"], "Indemnif + ication — Latin indemnitas.", ["legal", "suffix-confusion"]),
    ("unencumbered", ["unincumbered", "unencumbured", "unencumberd"], "Un + en + cumber + ed — all prefixes intact.", ["legal", "prefix-error"]),
    ("supersede", ["supercede", "superseed", "superceed"], "The ONLY English -sede word. Latin supersedere (to sit above).", ["legal", "false-analogy"]),
    ("unconscionable", ["unconscinable", "unconsionable", "unconscionabl"], "Un + con + scion + able — 'science' root.", ["legal", "silent-letter"]),
    ("notwithstanding", ["notwithstandig", "notwhithstanding", "notwithstading"], "Not + with + standing — compound word.", ["legal", "compound-word"]),
    ("jurisprudence", ["jurisprudance", "jurispurdence", "jurisprodence"], "Juris + prudence — Latin 'law wisdom.'", ["legal", "latin-origin"]),
    ("malfeasance", ["malfeasence", "malfeasanse", "malfeesance"], "Mal + feas + ance — 'doing wrong.'", ["legal", "suffix-confusion"]),
    ("nonfeasance", ["nonfeasence", "non-feasance", "nonfeasanse"], "Non + feas + ance — 'failure to act.'", ["legal", "suffix-confusion"]),
    ("embezzlement", ["embezlement", "embezzlment", "embezzalment"], "Em + bezzle + ment — double z.", ["legal", "double-letter"]),
    ("expropriation", ["expropiation", "expropreation", "expropriasion"], "Ex + propri + ation — like appropriation.", ["legal", "double-letter"]),
    ("fiduciary", ["fiducary", "fiduceary", "fidushiary"], "Fiduci + ary — Latin fides (trust).", ["finance", "latin-origin"]),
    ("disbursement", ["disbursment", "disburcement", "disbursemant"], "Disburse + ment — e STAYS before consonant suffix.", ["finance", "final-e-rule"]),
    ("reimbursement", ["reimbursment", "riembursement", "reimbersement"], "Reimburse + ment — e STAYS before consonant suffix.", ["finance", "final-e-rule"]),
    ("indebtedness", ["indeptedness", "indebtness", "indebttedness"], "In + debt + edness — silent b retained.", ["finance", "silent-letter"]),
    ("amortization", ["amortiztion", "amortasation", "amortazation"], "Amortize + ation — full -ization suffix.", ["finance", "suffix-confusion"]),
    ("receivable", ["recievable", "receiveable", "recieveable"], "ei after c + drop e before -able.", ["finance", "ie-ei-rule"]),
    ("delinquency", ["deliquency", "delinqency", "delinquancy"], "De + linqu + ency — u after q always.", ["finance", "silent-letter"]),
    ("appropriation", ["apropiation", "appropreation", "appropriasion"], "Double p + standard -tion (not -sion).", ["finance", "double-letter"]),
    ("entrepreneurship", ["entrepeneurship", "entrepraneurship", "entrepreneurhsip"], "Entrepreneur + ship — French compound.", ["policy", "foreign-origin"]),
    ("bureaucratization", ["beaurocratization", "burocratization", "bureaucratisation"], "Bureaucrat + ization — bureau preserved.", ["policy", "foreign-origin"]),
    ("decentralization", ["decentralisation", "decentralizasion", "decentrilization"], "De + central + ization — American -ize.", ["policy", "suffix-confusion"]),
    ("interdepartmental", ["inter-departmental", "interdeparmental", "interdepartmentall"], "One word; inter + department + al.", ["policy", "compound-word"]),
    ("intergovernmental", ["inter-governmental", "intergovernmentall", "intergovermental"], "One word; inter + government + al.", ["policy", "compound-word"]),
    ("nongovernmental", ["non-governmental", "nongovernmentall", "nongovermental"], "One word per style guide; non + governmental.", ["policy", "compound-word"]),
    ("underrepresented", ["under-represented", "underepresented", "underrepresentted"], "One word; under + represented.", ["policy", "compound-word"]),
    ("liaison", ["liason", "liasion", "liaision"], "French — exact vowel cluster i-a-i-s-o-n.", ["meetings", "foreign-origin"]),
    ("reconnaissance", ["reconaissance", "reconnaisance", "reconaisance"], "French — double n, double s, -ance.", ["legal", "foreign-origin"]),
    ("connoisseur", ["connoiseur", "conoisseur", "conoiseur"], "French — double n, double s, -eur.", ["meetings", "foreign-origin"]),
    ("hors d'oeuvre", ["hors doeuvre", "hors d'ouvre", "horse doeuvre"], "French — apostrophe, silent letters.", ["meetings", "foreign-origin"]),
    ("vis-à-vis", ["vis-a-vis", "viz-a-viz", "vise-a-vise"], "French — hyphenated with accent.", ["correspondence", "foreign-origin"]),
    ("laissez-faire", ["laisez-faire", "laissez-fair", "lassez-faire"], "French — double s, hyphenated.", ["policy", "foreign-origin"]),
    ("résumé", ["resume", "resumé", "resumè"], "French — accent on both e's (or at least final é).", ["human-resources", "foreign-origin"]),
    ("par excellence", ["par excellance", "par excelence", "par excellense"], "French — double l, -ence.", ["correspondence", "foreign-origin"]),
    ("coup de grâce", ["coup de gras", "coup de grace", "cou de grace"], "French — grâce (not gras which means 'fat').", ["correspondence", "foreign-origin"]),
    ("accoutrement", ["accouterment", "acoutrement", "accoutermet"], "French — ou vowel, double c.", ["office-supplies", "foreign-origin"]),
    ("personnel", ["personel", "personnell", "personell"], "Double n, single l — the most tested admin word.", ["human-resources", "double-letter"]),
    ("superintendent", ["superintendant", "superindendent", "superintendint"], "Super + intend + ent. Trap: -ant sounds the same.", ["positions", "suffix-confusion"]),
    ("accommodation", ["accomodation", "accommadation", "acomodation"], "Requires BOTH double c and double m.", ["office-supplies", "double-letter"]),
    ("surveillance", ["surveilance", "surveillence", "survellance"], "Double l + -ance (not -ence). French origin.", ["legal", "foreign-origin"]),
    ("maintenance", ["maintainence", "maintenence", "maintanance"], "Irregular formation: maintain drops -tain for -ten.", ["records", "suffix-confusion"]),
    ("bureaucracy", ["beauracracy", "burocracy", "beaurocracy"], "Bureau (French desk) + -cracy. NOT 'beau.'", ["policy", "foreign-origin"]),
    ("remuneration", ["renumeration", "remunaration", "remunarasion"], "mu-ner not nu-mer — transposition trap.", ["human-resources", "transposition"]),
    ("itinerary", ["itinarary", "itineraray", "itinery"], "Latin iter — five syllables: i-tin-er-ar-y.", ["meetings", "unstressed-vowel"]),
    ("miscellaneous", ["miscelaneous", "miscellainous", "miscellanious"], "Double l + -aneous ending. Not -ious.", ["records", "double-letter"]),
    ("auxiliary", ["auxillary", "auxilary", "auxilliary"], "Single l — auxili + ary.", ["records", "double-letter"]),
    ("acquittal", ["aquital", "acquital", "acquittall"], "Ac + quit + double t + al. Silent c in acq-.", ["legal", "consonant-doubling"]),
    ("subpoena", ["subpena", "supboena", "subpeona"], "Latin sub + poena — oe vowel cluster.", ["legal", "latin-origin"]),
    # Additional hard — sentence identification type
    ("dissemination", ["disemination", "dissemenation", "disseminasion"], "Dis + semin + ation — double s.", ["correspondence", "double-letter"]),
    ("commensurate", ["comensurate", "commenserait", "commensurait"], "Com + mensur + ate — double m.", ["finance", "double-letter"]),
    ("circumnavigation", ["circumnavagation", "circumnavaigation", "circumnavigasion"], "Circum + navig + ation — Latin.", ["correspondence", "latin-origin"]),
    ("disproportionate", ["disproportianate", "disproportionet", "disproprtionate"], "Dis + proportion + ate — all syllables.", ["finance", "unstressed-vowel"]),
    ("unimpeachable", ["unimpeachible", "unimpeacheable", "unimpeachble"], "Un + impeach + able — complete root → -able.", ["legal", "suffix-confusion"]),
    ("incontrovertible", ["incontrovertable", "incontravertible", "incontrovertble"], "In + controvert + ible — not a standalone word → -ible.", ["legal", "suffix-confusion"]),
    ("irreconcilable", ["irreconcileable", "ireconcilable", "irreconcilible"], "Ir + reconcile + able — double r, drop e.", ["legal", "prefix-error"]),
    ("notwithstanding", ["notwithstandig", "notwhithstanding", "notwithstaning"], "Not + with + standing — full compound.", ["legal", "compound-word"]),
    ("misappropriation", ["missappropriation", "misapropriation", "misappropriasion"], "Mis + appropriation — one s in mis-.", ["finance", "prefix-error"]),
    ("overrepresentation", ["over-representation", "overepresentation", "overrepresentasion"], "Over + representation — one word, double r.", ["policy", "compound-word"]),
    ("interdepartmental", ["inter-departmental", "interdeparmental", "interdepartmentall"], "One word: inter + departmental.", ["policy", "compound-word"]),
    ("disenfranchisement", ["disenfranchisment", "disenfrachisement", "disenfranchizement"], "Dis + en + franchise + ment — keep e.", ["legal", "final-e-rule"]),
    ("counterintelligence", ["counter-intelligence", "counterinteligence", "counterintelligense"], "One word; counter + intelligence — double l.", ["policy", "compound-word"]),
    ("intergovernmental", ["inter-governmental", "intergovermental", "intergovenmental"], "One word: inter + government + al.", ["policy", "compound-word"]),
    ("acknowledgment", ["acknowledgement", "acknowlegment", "acknowledgmant"], "American drops e: acknowledge + ment.", ["correspondence", "final-e-rule"]),
    ("nongovernmental", ["non-governmental", "nongovermental", "nongovernmantal"], "One word: non + governmental.", ["policy", "compound-word"]),
    ("reappropriation", ["re-appropriation", "reapropiation", "reappropriasion"], "Re + appropriation — double p maintained.", ["finance", "prefix-error"]),
    ("anticonstitutional", ["anti-constitutional", "anticonstituional", "anticonstitusional"], "One word: anti + constitutional.", ["legal", "compound-word"]),
    ("plenipotentiary", ["plenipotentary", "plenopotentiary", "plenipotensiary"], "Pleni + potenti + ary — Latin 'full power.'", ["positions", "latin-origin"]),
    ("ombudsman", ["ombusman", "ombbudsman", "ombutzman"], "Swedish origin — bud + s + man.", ["positions", "foreign-origin"]),
    ("comptroller", ["comptroler", "comtroller", "comptrollor"], "Silent p — variant of controller.", ["positions", "silent-letter"]),
    ("unencumbered", ["unincumbered", "unencumbured", "unencumberred"], "Un + en + cumber + ed — no doubling.", ["legal", "prefix-error"]),
    ("embezzlement", ["embezlement", "embezzlment", "imbezzlement"], "Em + bezzle + ment — double z, keep e.", ["legal", "double-letter"]),
    ("jurisprudence", ["jurisprudance", "jurispurdence", "jurisprodence"], "Juris + prudence — -ence not -ance.", ["legal", "suffix-confusion"]),
    ("reconnaissance", ["reconaissance", "reconnaisance", "reconaisance"], "French — double n, double s, -ance.", ["legal", "foreign-origin"]),
    ("connoisseur", ["connoiseur", "conoisseur", "conoiseur"], "French — double n, double s, -eur.", ["meetings", "foreign-origin"]),
    ("entrepreneurship", ["entrepeneurship", "entrepraneurship", "entrepreneurhsip"], "Entrepreneur + ship — maintain full root.", ["policy", "foreign-origin"]),
    ("bureaucratization", ["beaurocratization", "burocratization", "bureaucratisation"], "Bureaucrat + ization — bureau + -ize.", ["policy", "foreign-origin"]),
    ("decentralization", ["decentralisation", "decentralizasion", "decentrilization"], "De + central + ization — American -ize.", ["policy", "suffix-confusion"]),
    ("incontrovertible", ["incontrovertable", "incontravertible", "incontrovertble"], "Not a complete root → -ible.", ["legal", "suffix-confusion"]),
    ("unconscionable", ["unconscinable", "unconsionable", "unconscionible"], "Un + con + scion + able — 'science' root.", ["legal", "suffix-confusion"]),
    ("disproportionate", ["disproportianate", "disproportionet", "disproprtionate"], "Dis + proportion + ate — all syllables.", ["finance", "unstressed-vowel"]),
    ("irreconcilable", ["irreconcileable", "ireconcilable", "irreconcilible"], "Ir + reconcile + able — double r prefix.", ["legal", "prefix-error"]),
    ("misappropriation", ["missappropriation", "misapropriation", "misappropriasion"], "Mis + appropriation — single s in mis-.", ["finance", "prefix-error"]),
    ("disenfranchisement", ["disenfranchisment", "disenfrachisement", "disenfranchizement"], "Dis + en + franchise + ment.", ["legal", "final-e-rule"]),
    ("plenipotentiary", ["plenipotentary", "plenopotentiary", "plenipotensiary"], "Latin pleni + potenti + ary.", ["positions", "latin-origin"]),
    ("fiduciary", ["fiducary", "fiduceary", "fidushiary"], "Fiduci + ary — trust-related Latin root.", ["finance", "latin-origin"]),
    ("reconnaissance", ["reconaissance", "reconnaisance", "reconaisanse"], "French double n + double s + -ance.", ["legal", "foreign-origin"]),
    ("unimpeachable", ["unimpeachible", "unimpeacheable", "unimpeachble"], "Un + impeach + able — full root → -able.", ["legal", "suffix-confusion"]),
    ("commensurate", ["comensurate", "commenserait", "commensurait"], "Double m — com + mensur + ate.", ["finance", "double-letter"]),
]


# ============================================================================
# QUESTION GENERATION FUNCTIONS
# ============================================================================

def gen_correctly_spelled(id_num, difficulty, word_data, variation_seed=0):
    """Type: Which is spelled correctly? (correct among 3 misspellings)"""
    correct, misspellings, explanation, tags = word_data
    # Use variation_seed to pick different subsets when same word cycles
    rng = random.Random(id_num + variation_seed)
    distractors = rng.sample(misspellings, min(3, len(misspellings)))
    choices = distractors + [correct]
    rng.shuffle(choices)
    # Safety: ensure no duplicates
    if len(set(choices)) != 4:
        # Regenerate with different approach
        choices = list(set(distractors + [correct]))
        while len(choices) < 4:
            # Add a modified distractor
            base = misspellings[0]
            mod = base + "e" if not base.endswith("e") else base[:-1]
            if mod not in choices:
                choices.append(mod)
            else:
                choices.append(base + "s")
        choices = choices[:4]
        rng.shuffle(choices)
    return make_q(
        id_num, difficulty,
        "Which of the following is spelled correctly?",
        choices, correct,
        f"'{correct}' is the correct spelling. {explanation}",
        tags
    )


def gen_incorrectly_spelled(id_num, difficulty, word_data, other_correct_words):
    """Type: Which is spelled incorrectly? (misspelling among 3 correct words)"""
    correct, misspellings, explanation, tags = word_data
    misspelling = random.choice(misspellings)
    # Pick 3 other correctly spelled words — ensure all unique and different from misspelling
    available = [w for w in other_correct_words if w != correct and w.lower() != misspelling.lower()]
    others = random.sample(available, min(3, len(available)))
    # Ensure no duplicates with misspelling
    choices = others + [misspelling]
    # Deduplicate (safety)
    if len(set(choices)) != 4:
        # Replace duplicates
        extras = [w for w in available if w not in others]
        while len(set(choices)) < 4 and extras:
            choices = list(set(choices))
            choices.append(extras.pop(0))
    random.shuffle(choices)
    return make_q(
        id_num, difficulty,
        "Which of the following is spelled incorrectly?",
        choices, misspelling,
        f"'{misspelling}' is the misspelling. The correct spelling is '{correct}' — {explanation}",
        tags
    )


# Sentence templates for contextual questions (Medium/Hard)
SENTENCE_TEMPLATES = [
    ("The {word} was submitted to the regional office.", "correspondence"),
    ("Please prepare the {word} for the director's signature.", "correspondence"),
    ("The {word} of funds requires three signatories.", "finance"),
    ("The agency's {word} report is due next month.", "finance"),
    ("Submit the {word} to the HR division.", "human-resources"),
    ("The {word} officer reviewed all applications.", "human-resources"),
    ("The court issued a {word} against the respondent.", "legal"),
    ("All employees must comply with the {word} guidelines.", "legal"),
    ("The {word} system was updated last quarter.", "records"),
    ("Complete the {word} form before the deadline.", "records"),
    ("Order new {word} for the satellite office.", "office-supplies"),
    ("The {word} was scheduled for next Friday.", "meetings"),
    ("The {word} must approve the resolution.", "positions"),
    ("Government {word} requires transparency.", "policy"),
    ("The {word} process follows standard guidelines.", "procurement"),
]


def gen_sentence_correct(id_num, difficulty, word_data):
    """Type: Choose the correctly spelled word to complete the sentence."""
    correct, misspellings, explanation, tags = word_data
    template = random.choice(SENTENCE_TEMPLATES)
    sentence = template[0].format(word="______")
    distractors = random.sample(misspellings, min(3, len(misspellings)))
    choices = distractors + [correct]
    random.shuffle(choices)
    return make_q(
        id_num, difficulty,
        f"Choose the correctly spelled word to complete the sentence: \"{sentence}\"",
        choices, correct,
        f"'{correct}' is the correct spelling. {explanation}",
        tags
    )


def gen_sentence_identify_error(id_num, difficulty, word_data, other_words):
    """Type: Which word in the sentence is misspelled? (Hard only)"""
    correct, misspellings, explanation, tags = word_data
    misspelling = random.choice(misspellings)
    # Build choices with 3 correct words + 1 misspelling, all unique
    available = [w for w in other_words if w != correct and w.lower() != misspelling.lower()]
    others = random.sample(available, min(3, len(available)))
    choices = others + [misspelling]
    # Deduplicate
    if len(set(choices)) != 4:
        extras = [w for w in available if w not in others]
        while len(set(choices)) < 4 and extras:
            choices = list(set(choices))
            choices.append(extras.pop(0))
    random.shuffle(choices)
    return make_q(
        id_num, difficulty,
        "Which of the following words is misspelled?",
        choices, misspelling,
        f"'{misspelling}' is incorrect. The correct spelling is '{correct}' — {explanation}",
        tags
    )


# ============================================================================
# GENERATE ALL 600 QUESTIONS
# ============================================================================

questions = []
id_counter = 1
used_choice_sets = set()  # Track used choice combinations to avoid duplicates


def choices_key(choices):
    return tuple(sorted(c.lower() for c in choices))


def add_question(q):
    """Add question, checking for duplicate choice sets."""
    global id_counter
    key = choices_key(q["choices"])
    if key in used_choice_sets:
        return False  # Skip duplicate
    used_choice_sets.add(key)
    questions.append(q)
    return True


# --- EASY (200 questions) ---
easy_pool = EASY_WORDS.copy()
random.shuffle(easy_pool)
all_easy_correct = [w[0] for w in EASY_WORDS]

easy_idx = 0
attempts = 0
while len([q for q in questions if q["difficulty"] == "Easy"]) < 200 and attempts < 1000:
    word_data = easy_pool[easy_idx % len(easy_pool)]
    easy_idx += 1
    attempts += 1
    
    # Alternate question types
    roll = random.randint(0, 4)
    if roll in (0, 1, 2):
        q = gen_correctly_spelled(id_counter, "Easy", word_data, variation_seed=attempts)
    elif roll == 3:
        others = [w for w in all_easy_correct if w != word_data[0]]
        q = gen_incorrectly_spelled(id_counter, "Easy", word_data, others)
    else:
        q = gen_sentence_correct(id_counter, "Easy", word_data)
    
    if add_question(q):
        id_counter += 1

# --- MEDIUM (200 questions) ---
medium_pool = MEDIUM_WORDS.copy()
random.shuffle(medium_pool)
all_medium_correct = [w[0] for w in MEDIUM_WORDS]

med_idx = 0
attempts = 0
while len([q for q in questions if q["difficulty"] == "Medium"]) < 200 and attempts < 1000:
    word_data = medium_pool[med_idx % len(medium_pool)]
    med_idx += 1
    attempts += 1
    
    roll = random.randint(0, 9)
    if roll in (0, 1, 2, 3):
        q = gen_correctly_spelled(id_counter, "Medium", word_data, variation_seed=attempts)
    elif roll in (4, 5, 6):
        others = [w for w in all_medium_correct if w != word_data[0]]
        q = gen_incorrectly_spelled(id_counter, "Medium", word_data, others)
    else:
        q = gen_sentence_correct(id_counter, "Medium", word_data)
    
    if add_question(q):
        id_counter += 1

# --- HARD (200 questions) ---
hard_pool = HARD_WORDS.copy()
random.shuffle(hard_pool)
all_hard_correct = [w[0] for w in HARD_WORDS]

hard_idx = 0
attempts = 0
while len([q for q in questions if q["difficulty"] == "Hard"]) < 200 and attempts < 1000:
    word_data = hard_pool[hard_idx % len(hard_pool)]
    hard_idx += 1
    attempts += 1
    
    roll = random.randint(0, 19)
    if roll in range(0, 6):
        q = gen_correctly_spelled(id_counter, "Hard", word_data, variation_seed=attempts)
    elif roll in range(6, 11):
        others = [w for w in all_hard_correct if w != word_data[0]]
        q = gen_sentence_identify_error(id_counter, "Hard", word_data, others)
    elif roll in range(11, 16):
        q = gen_sentence_correct(id_counter, "Hard", word_data)
    else:
        others = [w for w in all_hard_correct if w != word_data[0]]
        q = gen_incorrectly_spelled(id_counter, "Hard", word_data, others)
    
    if add_question(q):
        id_counter += 1

# ============================================================================
# VALIDATION & OUTPUT
# ============================================================================

# Validate
assert len(questions) == 600, f"Expected 600, got {len(questions)}"
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
assert easy_count == 200, f"Easy: {easy_count}"
assert medium_count == 200, f"Medium: {medium_count}"
assert hard_count == 200, f"Hard: {hard_count}"

# Verify all answers are in choices
for q in questions:
    assert q["answer"] in q["choices"], f"ID {q['id']}: answer '{q['answer']}' not in choices {q['choices']}"

# Verify IDs are sequential
for i, q in enumerate(questions):
    assert q["id"] == i + 1, f"Expected id {i+1}, got {q['id']}"

# Write output
output_path = os.path.join(OUTPUT_DIR, "questions.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {len(questions)} questions")
print(f"   Easy: {easy_count} | Medium: {medium_count} | Hard: {hard_count}")
print(f"   Output: {output_path}")

# Print tag distribution
all_tags = {}
for q in questions:
    for tag in q["tags"]:
        all_tags[tag] = all_tags.get(tag, 0) + 1
print("\n📊 Tag distribution:")
for tag, count in sorted(all_tags.items(), key=lambda x: -x[1]):
    print(f"   {tag}: {count}")
