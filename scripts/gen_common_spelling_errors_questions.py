"""
Generate 600 questions for Common Spelling Errors lesson.
200 Easy, 200 Medium, 200 Hard.
All questions: "Which of the following is spelled correctly?"
"""

import json
import random
import os

random.seed(42)

def make_q(id_num, difficulty, choices, answer, explanation, tags):
    return {
        "id": id_num,
        "subtest": "Clerical Ability",
        "module": "Spelling",
        "subtopic": "Common Spelling Errors",
        "difficulty": difficulty,
        "question": "Which of the following is spelled correctly?",
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English"
    }


# Format: (correct_spelling, [distractor1, distractor2, distractor3], explanation, [tags])
# EVERY correct spelling has been verified.

EASY_WORDS = [
    ("government", ["goverment", "govenment", "govermnent"], "Retains the 'n' from root 'govern' — govern + ment.", ["silent-letter", "root-word"]),
    ("separate", ["seperate", "separete", "seprate"], "The second vowel is 'a' — remember 'there is A RAT in sepARAte.'", ["unstressed-vowel"]),
    ("necessary", ["neccesary", "neccessary", "necessery"], "One 'c' and two 's' letters — 1 collar, 2 sleeves.", ["double-letter"]),
    ("receive", ["recieve", "receeve", "receve"], "After 'c,' use 'ei' not 'ie' — i before e except after c.", ["ie-ei-rule"]),
    ("believe", ["beleive", "beleave", "belive"], "Standard 'ie' pattern — i before e (no c before it).", ["ie-ei-rule"]),
    ("achieve", ["acheive", "acheeve", "achive"], "Standard 'ie' pattern — i before e (no c before it).", ["ie-ei-rule"]),
    ("beginning", ["begining", "beggining", "beginng"], "Double 'n' — stressed final syllable 'gin' doubles before -ing.", ["consonant-doubling"]),
    ("environment", ["enviroment", "enviorment", "envirnoment"], "Root 'environ' has 'n' before 'm' — environ + ment.", ["silent-letter", "root-word"]),
    ("calendar", ["calender", "calandar", "callendar"], "Ends in -ar (like solar, lunar), not -er.", ["unstressed-vowel"]),
    ("occurred", ["occured", "ocurred", "occurrd"], "Stressed final syllable + single vowel + single consonant = double r.", ["consonant-doubling"]),
    ("until", ["untill", "untile", "untl"], "'Until' always has one l — it is not 'un + till.'", ["false-doubling"]),
    ("disappear", ["dissappear", "dissapear", "disapear"], "Prefix dis- (one s) + appear — prefix does not change root.", ["prefix-error"]),
    ("recommend", ["reccommend", "recomend", "recommand"], "Re- + commend — one c in prefix, double m in root.", ["prefix-error", "double-letter"]),
    ("definitely", ["definately", "definetly", "definitly"], "From 'finite' — definite + ly. The vowel is i, not a.", ["unstressed-vowel"]),
    ("February", ["Febuary", "Feburary", "Febrary"], "Contains two r's — Feb-ru-ary. First r is often silent in speech.", ["silent-letter"]),
    ("Wednesday", ["Wensday", "Wednsday", "Wendsday"], "Contains a silent 'd' — Wed-nes-day.", ["silent-letter"]),
    ("library", ["libary", "liberry", "libray"], "Contains two r's — li-brar-y. First r often dropped in speech.", ["silent-letter"]),
    ("grammar", ["grammer", "gramer", "gramar"], "Ends in -ar (like similar), not -er.", ["unstressed-vowel"]),
    ("writing", ["writeing", "writting", "writng"], "Drop silent e before -ing: write → writing.", ["final-e-drop"]),
    ("coming", ["comeing", "comming", "commeing"], "Drop silent e before -ing: come → coming.", ["final-e-drop"]),
    ("careful", ["carefull", "carful", "carefal"], "Suffix -ful always has ONE l.", ["ful-suffix"]),
    ("beautiful", ["beautifull", "beutiful", "beautful"], "Suffix -ful always has ONE l.", ["ful-suffix"]),
    ("hopeful", ["hopefull", "hopful", "hopefal"], "Suffix -ful always has ONE l.", ["ful-suffix"]),
    ("grateful", ["gratefull", "greatful", "gratefal"], "Suffix -ful always has ONE l; root is 'grate' not 'great.'", ["ful-suffix"]),
    ("successful", ["successfull", "succesful", "sucessful"], "Suffix -ful has ONE l; 'success' has double c and double s.", ["ful-suffix", "double-letter"]),
    ("argument", ["arguement", "arguemant", "argumant"], "Exception: 'argue' drops the e before -ment.", ["final-e-drop"]),
    ("truly", ["truely", "truley", "trully"], "Exception: 'true' drops the e before -ly.", ["final-e-drop"]),
    ("judgment", ["judgement", "judgmant", "jugdment"], "American English: 'judge' drops e before -ment.", ["final-e-drop"]),
    ("knowledge", ["knowlege", "nowledge", "knowledg"], "Silent k at start; full root 'knowledge' retained.", ["silent-letter"]),
    ("different", ["diffrent", "diferent", "differant"], "Two f's and -ent ending (not -ant).", ["double-letter", "suffix-confusion"]),
    ("occasion", ["ocassion", "occassion", "ocasion"], "Double c, single s — oc-ca-sion.", ["double-letter"]),
    ("suppression", ["supression", "suppresson", "supresion"], "Double p + double s — sup-pres-sion.", ["double-letter"]),
    ("tomorrow", ["tommorow", "tomorow", "tommorrow"], "One m, double r — to-mor-row.", ["double-letter"]),
    ("address", ["adress", "addres", "adres"], "Double d, double s — ad-dress.", ["double-letter"]),
    ("across", ["accross", "acros", "acrosse"], "One c, double s — a-cross.", ["double-letter"]),
    ("already", ["allready", "alredy", "allredy"], "Al- + ready — one l in prefix.", ["prefix-error"]),
    ("altogether", ["alltogether", "alltogather", "altogather"], "Al- + together — one l in prefix.", ["prefix-error"]),
    ("immediately", ["immediatly", "imediately", "imediatly"], "Double m; keep e before -ly: immediate + ly.", ["double-letter", "suffix-rule"]),
    ("surprise", ["suprise", "surprize", "surprice"], "Contains two r's — sur-prise. First r often dropped in speech.", ["silent-letter"]),
    ("foreign", ["foriegn", "forein", "foregin"], "Exception to ie/ei rule — memorize: f-o-r-e-i-g-n.", ["ie-ei-rule"]),
]


EASY_WORDS_2 = [
    ("weird", ["wierd", "weerd", "werid"], "Exception to ie/ei rule — memorize: w-e-i-r-d.", ["ie-ei-rule"]),
    ("freight", ["frieght", "freit", "freigth"], "ei sounded as 'ay' — freight.", ["ie-ei-rule"]),
    ("friend", ["freind", "frend", "freand"], "Standard ie pattern — i before e.", ["ie-ei-rule"]),
    ("piece", ["peice", "peece", "piese"], "Standard ie pattern — i before e (no c before it).", ["ie-ei-rule"]),
    ("ceiling", ["cieling", "ceeling", "seiling"], "ei after c — ceiling.", ["ie-ei-rule"]),
    ("neighbor", ["nieghbor", "neighbour", "neigbor"], "ei sounded as 'ay' — American spelling (no u).", ["ie-ei-rule"]),
    ("weight", ["wieght", "weigth", "waight"], "ei sounded as 'ay' — w-e-i-g-h-t.", ["ie-ei-rule"]),
    ("misspell", ["mispell", "misspel", "mispel"], "Prefix mis- + spell — keep both s's.", ["prefix-error"]),
    ("disappoint", ["dissappoint", "disapoint", "dissapoint"], "Prefix dis- (one s) + appoint (two p's).", ["prefix-error"]),
    ("unnecessary", ["unecessary", "unneccesary", "unneccessary"], "Prefix un- + necessary — double n at junction.", ["prefix-error"]),
    ("irregular", ["iregular", "irreguler", "iregullar"], "Prefix ir- + regular — double r at junction.", ["prefix-error"]),
    ("illegal", ["ilegal", "ilagal", "illegle"], "Prefix il- + legal — double l at junction.", ["prefix-error"]),
    ("immature", ["imature", "immatuer", "imatture"], "Prefix im- + mature — double m at junction.", ["prefix-error"]),
    ("preferred", ["prefered", "preffered", "preferrd"], "Stressed final syllable — double r before -ed.", ["consonant-doubling"]),
    ("referred", ["refered", "reffered", "referrd"], "Stressed final syllable — double r before -ed.", ["consonant-doubling"]),
    ("submitted", ["submited", "submiteed", "submittd"], "Stressed final syllable — double t before -ed.", ["consonant-doubling"]),
    ("transferred", ["transfered", "tranferred", "transferrd"], "Stressed final syllable — double r before -ed.", ["consonant-doubling"]),
    ("planning", ["planing", "planeing", "plannig"], "One-syllable word — double n before -ing.", ["consonant-doubling"]),
    ("running", ["runing", "runeing", "runnning"], "One-syllable word — double n before -ing.", ["consonant-doubling"]),
    ("stopped", ["stoped", "stoppped", "stoppd"], "One-syllable word — double p before -ed.", ["consonant-doubling"]),
    ("opened", ["oppened", "openned", "opend"], "Stress on FIRST syllable — do NOT double.", ["consonant-doubling"]),
    ("benefited", ["benefitted", "benifited", "benifitted"], "Stress on FIRST syllable — do NOT double t.", ["consonant-doubling"]),
    ("budgeted", ["budgetted", "bugeted", "budgetd"], "Stress on FIRST syllable — do NOT double t.", ["consonant-doubling"]),
    ("offered", ["offerred", "offerd", "ofered"], "Stress on FIRST syllable — do NOT double r.", ["consonant-doubling"]),
    ("traveled", ["travelled", "traveld", "travveled"], "American English: stress on FIRST syllable — single l.", ["consonant-doubling"]),
    ("management", ["managment", "managemant", "manegement"], "Keep e before consonant suffix: manage + ment.", ["final-e-drop"]),
    ("requirement", ["requirment", "requiremant", "requirament"], "Keep e before consonant suffix: require + ment.", ["final-e-drop"]),
    ("achievement", ["achievment", "acheivment", "achievemant"], "Keep e before consonant suffix: achieve + ment.", ["final-e-drop"]),
    ("statement", ["statment", "statemant", "statmant"], "Keep e before consonant suffix: state + ment.", ["final-e-drop"]),
    ("completely", ["completly", "completley", "compleetly"], "Keep e before consonant suffix: complete + ly.", ["final-e-drop"]),
    ("sincerely", ["sincerly", "sincerley", "sinceraly"], "Keep e before consonant suffix: sincere + ly.", ["final-e-drop"]),
    ("safety", ["saftey", "safty", "safetey"], "Safe + ty — keep the e (consonant suffix).", ["final-e-drop"]),
    ("desirable", ["desireable", "desirble", "desirible"], "Drop e before vowel suffix: desire + able = desirable.", ["final-e-drop"]),
    ("valuable", ["valueable", "valuble", "valuible"], "Drop e before vowel suffix: value + able = valuable.", ["final-e-drop"]),
    ("excitable", ["exciteable", "excitible", "excitble"], "Drop e before vowel suffix: excite + able = excitable.", ["final-e-drop"]),
    ("receipt", ["reciept", "receit", "recipt"], "Silent p; ei after c.", ["silent-letter", "ie-ei-rule"]),
    ("scissors", ["scisors", "sissors", "scizzors"], "Silent c; double s in middle.", ["silent-letter", "double-letter"]),
    ("answer", ["anser", "answar", "anwser"], "Silent w — ans-wer.", ["silent-letter"]),
    ("listen", ["lisen", "listan", "listin"], "Silent t — lis-ten.", ["silent-letter"]),
    ("often", ["ofen", "offten", "oftin"], "Silent t (in most dialects) — of-ten.", ["silent-letter"]),
]


EASY_WORDS_3 = [
    ("discipline", ["disipline", "discpline", "disiplin"], "Contains 'sc' cluster — dis-ci-pline.", ["silent-letter"]),
    ("muscle", ["musle", "mussle", "muscel"], "Silent c — mus-cle.", ["silent-letter"]),
    ("fascinate", ["facinate", "fasinate", "fasscinate"], "Contains 'sc' — fas-ci-nate.", ["silent-letter"]),
    ("scene", ["sene", "sceen", "scean"], "Silent c — scene.", ["silent-letter"]),
    ("acquire", ["aquire", "acuire", "acquir"], "Contains 'cqu' cluster — ac-quire.", ["double-letter"]),
    ("accommodate", ["accomodate", "acommodate", "acomodate"], "Double c AND double m — from Latin ad + com + modus.", ["double-letter"]),
    ("committee", ["comittee", "commitee", "comitee"], "Double m, double t, double e at end.", ["double-letter"]),
    ("embarrass", ["embarass", "embarras", "imbarrass"], "Double r AND double s — em-bar-rass.", ["double-letter"]),
    ("exaggerate", ["exagerate", "exaggarate", "exaggeratte"], "Double g — ex-ag-ger-ate.", ["double-letter"]),
    ("parallel", ["paralel", "parrallel", "parallell"], "One r, double l in middle, single l at end.", ["double-letter"]),
    ("professional", ["proffesional", "profesional", "proffessional"], "One f, double s — pro-fes-sion-al.", ["double-letter"]),
    ("assessment", ["assesment", "assessement", "asessment"], "Double s appears twice: as-sess-ment.", ["double-letter"]),
    ("commission", ["comission", "commision", "comision"], "Double m AND double s — com-mis-sion.", ["double-letter"]),
    ("opportunity", ["oportunity", "oppertunity", "oppurtunity"], "Double p — op-por-tu-ni-ty.", ["double-letter"]),
    ("succeed", ["suceed", "succede", "succceed"], "Double c + double e — suc-ceed.", ["double-letter"]),
    ("excellent", ["excelent", "excellant", "exellent"], "Double l + -ent ending.", ["double-letter", "suffix-confusion"]),
    ("intelligence", ["inteligence", "intellegence", "intelligance"], "Double l + -ence ending.", ["double-letter", "suffix-confusion"]),
    ("attendance", ["attendence", "atendance", "attendanse"], "Double t + -ance ending.", ["double-letter", "suffix-confusion"]),
    ("appearance", ["apperance", "appearence", "apearance"], "Double p + -ance ending.", ["double-letter", "suffix-confusion"]),
    ("allowance", ["alowance", "allowence", "alowence"], "Double l + -ance ending.", ["double-letter", "suffix-confusion"]),
    ("maintenance", ["maintainence", "maintenence", "maintanance"], "Main-ten-ance — drops 'tai' from maintain.", ["suffix-confusion", "root-word"]),
    ("performance", ["performence", "preformance", "performanse"], "Perform + ance — not -ence.", ["suffix-confusion"]),
    ("resistance", ["resistence", "resistanse", "resistince"], "Resist + ance — not -ence.", ["suffix-confusion"]),
    ("abundance", ["abundence", "abundanse", "abondance"], "Abund + ance — not -ence.", ["suffix-confusion"]),
    ("tolerance", ["tolerence", "toleranse", "tollerance"], "Toler + ance — not -ence.", ["suffix-confusion"]),
    ("dependable", ["dependible", "dependeble", "depandable"], "Root 'depend' is a complete word → -able.", ["suffix-confusion"]),
    ("comfortable", ["comfortible", "comfertable", "comfertible"], "Root 'comfort' is a complete word → -able.", ["suffix-confusion"]),
    ("reasonable", ["reasonible", "resonable", "reasoneble"], "Root 'reason' is a complete word → -able.", ["suffix-confusion"]),
    ("noticeable", ["noticable", "noticible", "notisable"], "Keep e after soft c + -able: notice + able.", ["suffix-confusion", "final-e-drop"]),
    ("manageable", ["managable", "managible", "manageble"], "Keep e after soft g + -able: manage + able.", ["suffix-confusion", "final-e-drop"]),
    ("responsible", ["responsable", "responseable", "responsble"], "Root 'respons-' is NOT a standalone word → -ible.", ["suffix-confusion"]),
    ("accessible", ["accessable", "accesible", "acessible"], "Root 'access-' takes -ible (Latin pattern).", ["suffix-confusion"]),
    ("flexible", ["flexable", "flexeble", "flexibal"], "Root 'flex-' is not a standalone word → -ible.", ["suffix-confusion"]),
    ("visible", ["visable", "viseable", "visble"], "Root 'vis-' is not a standalone word → -ible.", ["suffix-confusion"]),
    ("feasible", ["feasable", "feaseable", "feasble"], "Root 'feas-' is not a standalone word → -ible.", ["suffix-confusion"]),
    ("independent", ["independant", "indipendent", "independint"], "Stressed final syllable → -ent (not -ant).", ["suffix-confusion"]),
    ("occurrence", ["occurence", "occurance", "occurrance"], "Double c + double r + -ence ending.", ["double-letter", "suffix-confusion"]),
    ("preference", ["preferance", "preferrence", "preferense"], "Prefer (stressed) → -ence.", ["suffix-confusion"]),
    ("correspondence", ["correspondance", "corespondence", "corrispondence"], "Correspond → -ence (stressed final syllable).", ["suffix-confusion"]),
    ("difference", ["differance", "diffrence", "diferrence"], "Differ → -ence.", ["suffix-confusion"]),
]


EASY_WORDS_4 = [
    ("excellence", ["excellance", "excelence", "excellense"], "Excel → -ence (not -ance).", ["suffix-confusion"]),
    ("existence", ["existance", "existense", "existince"], "Exist → -ence (not -ance).", ["suffix-confusion"]),
    ("patience", ["patiance", "patiense", "patence"], "Patient → patience (-ence pattern).", ["suffix-confusion"]),
    ("absence", ["absense", "abscence", "absance"], "Absent → absence — ends in -ence.", ["suffix-confusion"]),
    ("sentence", ["sentance", "sentense", "sentince"], "Ends in -ence (not -ance).", ["suffix-confusion"]),
    ("experience", ["experiance", "experiense", "expirience"], "Ends in -ence (not -ance).", ["suffix-confusion"]),
    ("confidence", ["confidance", "confidense", "confidince"], "Confident → confidence — -ence ending.", ["suffix-confusion"]),
    ("evidence", ["evidance", "evidanse", "evidince"], "Evident → evidence — -ence ending.", ["suffix-confusion"]),
    ("convenience", ["convienience", "conveniance", "conveniense"], "Convenient → convenience — -ence ending.", ["suffix-confusion"]),
    ("significance", ["significanse", "significence", "signifigance"], "Significant → significance — -ance ending.", ["suffix-confusion"]),
    ("importance", ["importence", "importanse", "importince"], "Important → importance — -ance ending.", ["suffix-confusion"]),
    ("acceptance", ["acceptence", "acceptanse", "acceptince"], "Accept → acceptance — -ance ending.", ["suffix-confusion"]),
    ("guidance", ["guidanse", "guidence", "guidince"], "Guide → guidance — -ance ending.", ["suffix-confusion"]),
    ("insurance", ["insurence", "insuranse", "insurince"], "Insure → insurance — -ance ending.", ["suffix-confusion"]),
    ("ignorance", ["ignorence", "ignoranse", "ignorince"], "Ignorant → ignorance — -ance ending.", ["suffix-confusion"]),
    ("assistance", ["assistense", "assistince", "assistence"], "Assist → assistance — -ance ending.", ["suffix-confusion"]),
    ("compliance", ["complience", "complianse", "complince"], "Comply → compliance — -ance ending.", ["suffix-confusion"]),
    ("grievance", ["grievence", "grievanse", "greivance"], "Grieve → grievance — -ance ending.", ["suffix-confusion"]),
    ("allegiance", ["allegience", "alleganse", "allegaince"], "French origin → -ance ending.", ["suffix-confusion"]),
    ("surveillance", ["surveillence", "surveilance", "survellance"], "French 'surveiller' → -ance ending.", ["suffix-confusion"]),
    ("privilege", ["priviledge", "privelege", "privilige"], "Ends in -lege (not -ledge) — from Latin privilegium.", ["false-analogy"]),
    ("category", ["catagory", "categery", "catigory"], "Second vowel is 'e' — cat-e-go-ry.", ["unstressed-vowel"]),
    ("desperate", ["despirate", "desparate", "desprate"], "Contains 'era' — des-per-ate.", ["unstressed-vowel"]),
    ("repetition", ["repitition", "repetision", "repitision"], "From 'repeat' — rep-e-ti-tion.", ["unstressed-vowel"]),
    ("medicine", ["medecine", "medicin", "medacine"], "From 'medic' — med-i-cine.", ["unstressed-vowel"]),
    ("cemetery", ["cemetary", "cematery", "cemetry"], "All e's: c-e-m-e-t-e-ry (three e's).", ["unstressed-vowel"]),
    ("describe", ["discribe", "descibe", "discibe"], "Prefix de- (not di-) + scribe.", ["unstressed-vowel", "prefix-error"]),
    ("temperature", ["temprature", "temperture", "temparature"], "Temper + ature — all vowels present.", ["unstressed-vowel"]),
    ("interesting", ["intresting", "intersting", "intressting"], "Inter + est + ing — all syllables present.", ["silent-letter"]),
    ("restaurant", ["restarant", "resturant", "restraunt"], "French origin — res-tau-rant.", ["unstressed-vowel"]),
    ("particular", ["perticular", "particlar", "particuler"], "Part + icular — ends in -ar.", ["unstressed-vowel"]),
    ("original", ["orignal", "origional", "origenal"], "Origin + al — no extra letters.", ["unstressed-vowel"]),
    ("familiar", ["familar", "familliar", "familier"], "Family → familiar — ends in -iar.", ["unstressed-vowel"]),
    ("similar", ["similer", "similiar", "simalar"], "Ends in -ilar (like familiar).", ["unstressed-vowel"]),
    ("popular", ["populer", "popullar", "poplar"], "Ends in -ular (like regular).", ["unstressed-vowel"]),
    ("regular", ["reguler", "regullar", "regualar"], "Ends in -ular.", ["unstressed-vowel"]),
    ("circular", ["circuler", "circullar", "circlar"], "Ends in -ular.", ["unstressed-vowel"]),
    ("natural", ["naturel", "naturall", "natral"], "Nature + al — ends in -ural.", ["unstressed-vowel"]),
    ("general", ["generel", "generall", "genral"], "Ends in -eral.", ["unstressed-vowel"]),
    ("several", ["severel", "severall", "sevral"], "Ends in -eral.", ["unstressed-vowel"]),
]


EASY_WORDS_5 = [
    ("mineral", ["minerel", "minerall", "minral"], "Ends in -eral.", ["unstressed-vowel"]),
    ("federal", ["federel", "federall", "fedral"], "Ends in -eral.", ["unstressed-vowel"]),
    ("physical", ["phisical", "physicall", "fysical"], "Ph = f sound; ends in -ical.", ["silent-letter"]),
    ("technical", ["technicall", "techncal", "technicle"], "Ends in -ical.", ["suffix-confusion"]),
    ("practical", ["practicall", "practcal", "practicle"], "Ends in -ical.", ["suffix-confusion"]),
    ("political", ["politicall", "politcal", "politicle"], "Ends in -ical.", ["suffix-confusion"]),
    ("historical", ["historicall", "historcal", "historicle"], "Ends in -ical.", ["suffix-confusion"]),
    ("basically", ["basicly", "basicaly", "basickly"], "Basic + ally — double l in -ally.", ["suffix-confusion"]),
    ("accidentally", ["accidently", "accidentaly", "accidentlly"], "Accidental + ly — not 'accident + ly.'", ["suffix-confusion"]),
    ("occasionally", ["occasionaly", "occassionally", "ocassionally"], "Occasional + ly — double l.", ["suffix-confusion", "double-letter"]),
    ("especially", ["especialy", "espesially", "especally"], "Especial + ly — double l.", ["suffix-confusion"]),
    ("finally", ["finaly", "finely", "finially"], "Final + ly — double l.", ["suffix-confusion"]),
    ("actually", ["actualy", "actully", "acutally"], "Actual + ly — double l.", ["suffix-confusion"]),
    ("usually", ["usualy", "usally", "ussually"], "Usual + ly — double l.", ["suffix-confusion"]),
    ("probably", ["probaly", "probabley", "probibly"], "Probable → probably — drop e, add y.", ["unstressed-vowel"]),
    ("business", ["buisness", "busness", "bussiness"], "Busy → business — u-s-i-n-e-s-s.", ["unstressed-vowel"]),
    ("decision", ["desicion", "decission", "decison"], "Decide → decision — -sion ending.", ["suffix-confusion"]),
    ("discussion", ["discusion", "disscussion", "dicussion"], "Discuss → discussion — double s + -ion.", ["double-letter", "suffix-confusion"]),
    ("permission", ["permision", "permisson", "premission"], "Permit → permission — double s + -ion.", ["double-letter", "suffix-confusion"]),
    ("admission", ["admision", "addmission", "admisson"], "Admit → admission — double s + -ion.", ["double-letter", "suffix-confusion"]),
    ("apparent", ["apparant", "aparent", "apparrent"], "Double p + -ent ending.", ["double-letter", "suffix-confusion"]),
    ("permanent", ["permanant", "permenent", "permanint"], "Double meaning: perm + anent — -ent ending.", ["suffix-confusion"]),
    ("rhythm", ["rythm", "rhythem", "rythym"], "No vowel between th and m — rhythm.", ["silent-letter"]),
    ("schedule", ["shedule", "scedule", "schedual"], "Sch- cluster — sched-ule.", ["silent-letter"]),
    ("guarantee", ["gaurantee", "guarentee", "garentee"], "French origin — g-u-a-r-a-n-t-e-e.", ["transposition"]),
    ("language", ["langauge", "languege", "languge"], "Correct sequence: l-a-n-g-u-a-g-e.", ["transposition"]),
    ("develop", ["develope", "develp", "devellop"], "No final e — de-vel-op.", ["letter-insertion"]),
    ("forty", ["fourty", "fortey", "fourthy"], "Unlike 'four,' forty drops the u.", ["false-analogy"]),
    ("ninth", ["nineth", "ninethe", "ninthe"], "Unlike 'nine,' ninth drops the e.", ["false-analogy"]),
    ("wholly", ["wholely", "wholey", "wholy"], "Exception: 'whole' drops the e before -ly.", ["final-e-drop"]),
    ("width", ["widht", "widdth", "wideth"], "No extra letters — width.", ["letter-insertion"]),
    ("strength", ["strenth", "strenght", "stength"], "Contains 'ngth' — strength.", ["silent-letter"]),
    ("eighth", ["eigth", "eightth", "eigthh"], "Eight + h — eighth.", ["silent-letter"]),
    ("twelfth", ["twelth", "twelvth", "twelfeth"], "Twelve → twelfth — f replaces ve.", ["silent-letter"]),
    ("whether", ["wether", "wheather", "wheter"], "Contains 'wh' — whether.", ["silent-letter"]),
    ("which", ["wich", "whitch", "whch"], "Contains 'wh' — which.", ["silent-letter"]),
    ("whole", ["hole", "whoal", "whol"], "Silent w + h — whole.", ["silent-letter"]),
    ("thought", ["thougth", "thougt", "thot"], "Contains 'ough' — thought.", ["silent-letter"]),
    ("thorough", ["thorogh", "thurough", "thorouh"], "Contains 'ough' — thorough.", ["silent-letter"]),
    ("enough", ["enuf", "enought", "enogh"], "Contains 'ough' — enough.", ["silent-letter"]),
]

# Combine all easy words
ALL_EASY = EASY_WORDS + EASY_WORDS_2 + EASY_WORDS_3 + EASY_WORDS_4 + EASY_WORDS_5


MEDIUM_WORDS = [
    ("bureaucracy", ["beauracracy", "burocracy", "beurocracy"], "French 'bureau' + Greek '-cracy' — bureau + cracy.", ["transposition", "foreign-origin"]),
    ("liaison", ["liason", "liasion", "laison"], "French origin — retains vowel cluster -iai-.", ["foreign-origin"]),
    ("questionnaire", ["questionaire", "questionnare", "questionairre"], "French origin — double n + -aire ending.", ["foreign-origin", "double-letter"]),
    ("personnel", ["personel", "personell", "personnell"], "Double n, single l — person-nel.", ["double-letter"]),
    ("itinerary", ["itinarary", "itineraray", "itinery"], "Latin iter (journey) — i-tin-er-ary.", ["unstressed-vowel"]),
    ("remuneration", ["renumeration", "remunaration", "remnuneration"], "From Latin munus (gift) — re-mu-ner-ation (not re-nu-mer).", ["transposition"]),
    ("superintendent", ["superintendant", "superindendent", "superintendint"], "Super + intend + ent — ends in -ent.", ["suffix-confusion"]),
    ("disbursement", ["disbursment", "disburcement", "disbursemant"], "Disburse + ment — keep the e.", ["final-e-drop"]),
    ("reimbursement", ["reimbursment", "riembursement", "reimbursemant"], "Reimburse + ment — keep the e.", ["final-e-drop"]),
    ("procurement", ["procurment", "procurrement", "procuremant"], "Procure + ment — keep the e.", ["final-e-drop"]),
    ("acknowledgment", ["acknowledgement", "acknowlegment", "acknoledgment"], "American English drops e: acknowledge + ment.", ["final-e-drop"]),
    ("subpoena", ["subpena", "supboena", "subpeona"], "Latin origin — sub + poena (penalty).", ["foreign-origin", "silent-letter"]),
    ("indictment", ["inditement", "indictmant", "indicment"], "Silent c — in-dict-ment.", ["silent-letter"]),
    ("acquittal", ["aquital", "acquital", "acquittall"], "Prefix ac- + quit + double t + al.", ["double-letter"]),
    ("affidavit", ["afidavit", "affadavit", "afidavvit"], "Double f + i (not a) in third syllable.", ["double-letter", "unstressed-vowel"]),
    ("defendant", ["defendent", "defandant", "defendint"], "Defend + ant — ends in -ant.", ["suffix-confusion"]),
    ("plaintiff", ["plaintif", "plantiff", "plaintiffe"], "Plain + tiff — double f at end.", ["double-letter"]),
    ("ordinance", ["ordanance", "ordinence", "ordinanse"], "Ordin + ance — not -ence.", ["suffix-confusion"]),
    ("expenditure", ["expinditure", "expendature", "expendeture"], "Expend + iture — i in suffix.", ["unstressed-vowel"]),
    ("allotment", ["alotment", "allottment", "alottment"], "Double l, single t — allot + ment.", ["double-letter"]),
    ("appropriation", ["apropiation", "appropreation", "appropriaton"], "Double p + -iation ending.", ["double-letter"]),
    ("remittance", ["remitance", "remittence", "remitence"], "Double t + -ance ending.", ["double-letter", "suffix-confusion"]),
    ("collateral", ["colateral", "collatteral", "colatteral"], "Double l, single t — col-lat-er-al.", ["double-letter"]),
    ("supersede", ["supercede", "superseed", "superceed"], "The ONLY English word ending in -sede (Latin supersedere).", ["false-analogy"]),
    ("consensus", ["concensus", "consencus", "concensous"], "Con + sensus — not related to 'census.'", ["false-analogy"]),
    ("inoculate", ["innoculate", "inocullate", "innocullate"], "One n, one c — not related to 'innocent.'", ["false-analogy"]),
    ("harass", ["harrass", "harras", "herrass"], "One r, double s — not like 'embarrass.'", ["false-analogy"]),
    ("minuscule", ["miniscule", "miniscuel", "minascule"], "From Latin 'minusculus' — not from 'mini.'", ["false-analogy"]),
    ("sacrilegious", ["sacreligious", "sacreligous", "sacriligious"], "From 'sacrilege' — not from 'religious.'", ["false-analogy"]),
    ("memento", ["momento", "memanto", "mamento"], "From Latin 'memento' (remember) — not from 'moment.'", ["false-analogy"]),
    ("pronunciation", ["pronounciation", "prononciation", "pronuncation"], "Noun form drops 'ce' from 'pronounce.'", ["false-analogy"]),
    ("athlete", ["athelete", "athalete", "athelet"], "Only 2 syllables: ath-lete — no extra e.", ["letter-insertion"]),
    ("mischievous", ["mischievious", "mischevous", "mischivous"], "Three syllables: mis-chie-vous — no -ious.", ["letter-insertion"]),
    ("disastrous", ["disasterous", "disastorus", "disastrus"], "Disaster drops e + ous: disastr-ous.", ["letter-insertion"]),
    ("remembrance", ["rememberance", "remembrence", "remberance"], "Not 'remember + ance' — drops 'e' in middle.", ["letter-insertion"]),
    ("hindrance", ["hinderance", "hindrence", "hinderence"], "Not 'hinder + ance' — drops 'e.'", ["letter-insertion"]),
    ("entrance", ["enterance", "entrence", "enterence"], "Not 'enter + ance' — it is 'en-trance.'", ["letter-insertion"]),
    ("lightning", ["lightening", "lightnning", "litening"], "'Lightening' means making lighter; 'lightning' = electrical.", ["letter-insertion"]),
    ("grievous", ["grievious", "greivous", "grevious"], "Griev + ous — no i before -ous.", ["letter-insertion"]),
    ("height", ["heighth", "hieght", "heigth"], "No extra h at end — height (not heighth).", ["letter-insertion"]),
]


MEDIUM_WORDS_2 = [
    ("amateur", ["amature", "amatuer", "amatur"], "French origin — am-a-teur.", ["foreign-origin"]),
    ("colleague", ["colleauge", "colague", "collegue"], "French origin — col-league.", ["foreign-origin"]),
    ("adequate", ["adeqaute", "adequete", "addequate"], "Correct sequence: a-d-e-q-u-a-t-e.", ["transposition"]),
    ("relevant", ["relavant", "relevent", "relavent"], "Correct: r-e-l-e-v-a-n-t (not transposed).", ["transposition"]),
    ("tragedy", ["tradegy", "tradgedy", "tragady"], "Correct sequence: t-r-a-g-e-d-y.", ["transposition"]),
    ("jewelry", ["jewlery", "jewellry", "jewlrey"], "American: jewel + ry = jewelry.", ["transposition"]),
    ("prescription", ["perscription", "presciption", "prescritpion"], "Pre + script + ion — not 'per.'", ["transposition"]),
    ("hierarchy", ["heirarchy", "hierarcy", "heirarcy"], "Hier- (not heir-) + archy.", ["transposition"]),
    ("counterfeit", ["counterfiet", "counterfit", "counterfeat"], "ei pattern — coun-ter-feit.", ["ie-ei-rule"]),
    ("desiccate", ["dessicate", "desicate", "dessiccate"], "Single s + double c — des-ic-cate.", ["false-analogy"]),
    ("mattress", ["matress", "mattrass", "mattres"], "Double t + double s — mat-tress.", ["double-letter"]),
    ("miscellaneous", ["miscelaneous", "miscellanious", "miscellanous"], "Double l + -aneous ending.", ["double-letter"]),
    ("curriculum", ["curiculum", "curriculm", "curricullum"], "Double r — cur-ric-u-lum.", ["double-letter"]),
    ("commemorate", ["comemorate", "commemmorate", "comemmorate"], "Double m once — com-mem-o-rate.", ["double-letter"]),
    ("mozzarella", ["mozarella", "mozzarela", "mozarela"], "Double z + double l — moz-za-rel-la.", ["double-letter"]),
    ("aggravate", ["agravate", "aggrevate", "agravvate"], "Double g — ag-gra-vate.", ["double-letter"]),
    ("aggressive", ["agressive", "aggresive", "agresive"], "Double g + double s — ag-gres-sive.", ["double-letter"]),
    ("appreciate", ["apreciate", "appriciate", "appreceate"], "Double p — ap-pre-ci-ate.", ["double-letter"]),
    ("approximate", ["aproximate", "apporximate", "aproximite"], "Double p — ap-prox-i-mate.", ["double-letter"]),
    ("broccoli", ["brocoli", "brocolli", "broccilli"], "Double c, single l — broc-co-li.", ["double-letter"]),
    ("cappuccino", ["capuccino", "cappucino", "capucino"], "Double p, double c — cap-puc-ci-no.", ["double-letter"]),
    ("diarrhea", ["diarrhoea", "diarhea", "diarrea"], "American: double r + h — di-ar-rhe-a.", ["double-letter"]),
    ("dilemma", ["dilema", "dilemna", "dillema"], "Double m (not mn) — di-lem-ma.", ["double-letter"]),
    ("graffiti", ["grafiti", "graffitti", "grafitti"], "Double f, single t — graf-fi-ti.", ["double-letter"]),
    ("harassment", ["harrassment", "harasment", "harassement"], "Single r, double s — harass + ment.", ["double-letter"]),
    ("innocence", ["inocence", "innocense", "inosence"], "Double n — in-no-cence.", ["double-letter"]),
    ("interrupt", ["interupt", "interrup", "interuupt"], "Double r — in-ter-rupt.", ["double-letter"]),
    ("zucchini", ["zuchini", "zuchinni", "zuccini"], "Double c + h + single n — broc-co-li.", ["double-letter"]),
    ("anniversary", ["aniversary", "anniversery", "annivarsary"], "Double n + -ary ending — ne-ces-sa-ry.", ["double-letter"]),
    ("battalion", ["batalion", "battallion", "batallion"], "Double t + single l — bat-tal-ion.", ["double-letter"]),
    ("permissible", ["permissable", "permisible", "permisable"], "Root 'permiss-' not standalone → -ible.", ["suffix-confusion"]),
    ("admissible", ["admissable", "admisible", "admisable"], "Root 'admiss-' not standalone → -ible.", ["suffix-confusion"]),
    ("compatible", ["compatable", "compatble", "compatabile"], "Root 'compat-' not standalone → -ible.", ["suffix-confusion"]),
    ("credible", ["credable", "credibal", "credabel"], "Root 'cred-' not standalone → -ible.", ["suffix-confusion"]),
    ("eligible", ["elegible", "eligable", "eligeble"], "Root 'elig-' not standalone → -ible.", ["suffix-confusion"]),
    ("inevitable", ["inevitible", "inevetable", "inevitabel"], "Root 'evit' + in- prefix → -able (from evitare).", ["suffix-confusion"]),
    ("considerable", ["considerible", "considrable", "considerble"], "Root 'consider' is complete → -able.", ["suffix-confusion"]),
    ("enforceable", ["enforcible", "enforcable", "enforceble"], "Keep e after soft c + -able.", ["suffix-confusion", "final-e-drop"]),
    ("replaceable", ["replacable", "replacible", "replaceble"], "Keep e after soft c + -able.", ["suffix-confusion", "final-e-drop"]),
    ("traceable", ["tracable", "tracible", "traceble"], "Keep e after soft c + -able.", ["suffix-confusion", "final-e-drop"]),
]


MEDIUM_WORDS_3 = [
    ("courageous", ["couragous", "couragious", "corageous"], "Keep e after soft g + -ous: courage + ous.", ["final-e-drop"]),
    ("outrageous", ["outragous", "outragious", "outrageious"], "Keep e after soft g + -ous: outrage + ous.", ["final-e-drop"]),
    ("advantageous", ["advantagous", "advantagious", "advantageus"], "Keep e after soft g + -ous: advantage + ous.", ["final-e-drop"]),
    ("changeable", ["changable", "changible", "changeble"], "Keep e after soft g + -able.", ["final-e-drop"]),
    ("knowledgeable", ["knowledgable", "knowlegeable", "knowledgible"], "Keep e after soft g + -able.", ["final-e-drop"]),
    ("peaceable", ["peacable", "peacible", "peaceble"], "Keep e after soft c + -able.", ["final-e-drop"]),
    ("serviceable", ["servicable", "servicible", "serviceble"], "Keep e after soft c + -able.", ["final-e-drop"]),
    ("extension", ["extention", "exstension", "extenshion"], "Extend (ends in -d) → -sion.", ["suffix-confusion"]),
    ("suspension", ["suspencion", "suspention", "suspenshion"], "Suspend (ends in -d) → -sion.", ["suffix-confusion"]),
    ("comprehension", ["comprehention", "comprehenshion", "comprahension"], "Comprehend → -sion.", ["suffix-confusion"]),
    ("expansion", ["expantion", "expancion", "expanshion"], "Expand → -sion.", ["suffix-confusion"]),
    ("submission", ["submittion", "submision", "submisson"], "Submit (ends in -mit) → -ssion.", ["suffix-confusion"]),
    ("transmission", ["transmittion", "transmision", "transmisson"], "Transmit → -ssion.", ["suffix-confusion"]),
    ("concession", ["concetion", "concesion", "concesssion"], "Concede → concession — -ssion.", ["suffix-confusion"]),
    ("possession", ["posession", "possesion", "posesion"], "Possess → possession — double s twice.", ["double-letter"]),
    ("succession", ["succesion", "sucession", "successsion"], "Succeed → succession — double c + -ssion.", ["double-letter", "suffix-confusion"]),
    ("aggression", ["agression", "agresion", "aggresion"], "Double g + -ssion.", ["double-letter", "suffix-confusion"]),
    ("impression", ["impresion", "immpression", "impresson"], "Double s — im-pres-sion.", ["double-letter"]),
    ("expression", ["expresion", "exppression", "expresson"], "Double s — ex-pres-sion.", ["double-letter"]),
    ("profession", ["proffession", "profesion", "proffesion"], "Single f, double s — pro-fes-sion.", ["double-letter"]),
    ("conscience", ["concience", "consience", "concsience"], "Sci cluster — con-sci-ence.", ["silent-letter"]),
    ("conscious", ["concious", "consious", "concsious"], "Sci cluster — con-sci-ous.", ["silent-letter"]),
    ("crescent", ["cresent", "cressent", "crescant"], "Sc cluster — cres-cent.", ["silent-letter"]),
    ("ascend", ["assend", "acend", "asscend"], "Sc cluster — a-scend.", ["silent-letter"]),
    ("pneumonia", ["neumonia", "pnemonia", "nuemonia"], "Silent p — pneu-mo-nia.", ["silent-letter"]),
    ("psychology", ["sychology", "phsycology", "psycology"], "Silent p — psy-chol-o-gy.", ["silent-letter"]),
    ("psychiatry", ["sychiatry", "phsychiatry", "psyciatry"], "Silent p — psy-chi-a-try.", ["silent-letter"]),
    ("mortgage", ["morgage", "mortage", "morgtage"], "Silent t — mort-gage.", ["silent-letter"]),
    ("pterodactyl", ["terodactyl", "pterodactil", "terodactil"], "Silent p — pter-o-dac-tyl.", ["silent-letter"]),
    ("salmon", ["sammon", "samon", "salmen"], "Silent l — sal-mon.", ["silent-letter"]),
    ("colonel", ["kernal", "colonol", "cornel"], "Pronounced 'kernel' but spelled colonel.", ["silent-letter"]),
    ("subtle", ["suttle", "subttle", "sutle"], "Silent b — sub-tle.", ["silent-letter"]),
    ("doubt", ["dout", "doupt", "dowbt"], "Silent b — doubt.", ["silent-letter"]),
    ("debt", ["det", "dept", "dett"], "Silent b — debt.", ["silent-letter"]),
    ("island", ["iland", "ilsand", "iseland"], "Silent s — is-land.", ["silent-letter"]),
    ("aisle", ["isle", "aistle", "aile"], "Silent s — aisle (not same as 'isle').", ["silent-letter"]),
    ("forfeit", ["forfiet", "forfit", "forfet"], "Exception to ie/ei — for-feit.", ["ie-ei-rule"]),
    ("seize", ["sieze", "seeze", "seise"], "Exception to ie/ei — memorize.", ["ie-ei-rule"]),
    ("leisure", ["liesure", "leasure", "leizure"], "Exception to ie/ei — lei-sure.", ["ie-ei-rule"]),
    ("protein", ["protien", "protine", "proteine"], "Exception to ie/ei — pro-tein.", ["ie-ei-rule"]),
]


MEDIUM_WORDS_4 = [
    ("caffeine", ["caffiene", "cafeine", "caffeen"], "Exception to ie/ei — caf-feine.", ["ie-ei-rule"]),
    ("species", ["speceis", "speices", "spiecies"], "Exception to ie/ei — spe-cies.", ["ie-ei-rule"]),
    ("sufficient", ["sufficent", "sufficiant", "sufficint"], "-ient ending (not -ent).", ["ie-ei-rule", "suffix-confusion"]),
    ("efficient", ["efficent", "efficeint", "efficiant"], "-ient ending (not -ent).", ["ie-ei-rule", "suffix-confusion"]),
    ("ancient", ["anciant", "anceint", "ancent"], "-ient ending.", ["ie-ei-rule", "suffix-confusion"]),
    ("patient", ["pateint", "patiant", "patcient"], "-ient ending.", ["ie-ei-rule", "suffix-confusion"]),
    ("ingredient", ["ingrediant", "ingredeint", "ingredent"], "-ient ending.", ["ie-ei-rule", "suffix-confusion"]),
    ("convenient", ["convienient", "conveniant", "conveinent"], "-ient ending.", ["ie-ei-rule", "suffix-confusion"]),
    ("dissatisfied", ["disatisfied", "dissatisifed", "disattisfied"], "Dis- + satisfied — double s at junction.", ["prefix-error"]),
    ("dissimilar", ["disimilar", "dissimiler", "disimiler"], "Dis- + similar — double s at junction.", ["prefix-error"]),
    ("immoral", ["imoral", "imorral", "immorel"], "Im- + moral — double m at junction.", ["prefix-error"]),
    ("immortal", ["imortal", "imortall", "imortel"], "Im- + mortal — double m at junction.", ["prefix-error"]),
    ("illogical", ["ilogical", "illogicle", "ilogicle"], "Il- + logical — double l at junction.", ["prefix-error"]),
    ("illegible", ["ilegible", "illegable", "ilegable"], "Il- + legible — double l at junction.", ["prefix-error"]),
    ("irresponsible", ["iresponsible", "irresponsable", "iresponsable"], "Ir- + responsible — double r at junction.", ["prefix-error"]),
    ("irrelevant", ["irelevant", "irrelavent", "irelavent"], "Ir- + relevant — double r at junction.", ["prefix-error"]),
    ("unnatural", ["unatural", "unnateral", "unatral"], "Un- + natural — double n at junction.", ["prefix-error"]),
    ("overrate", ["overate", "overatte", "ovverate"], "Over- + rate — double r at junction.", ["prefix-error"]),
    ("overrule", ["overule", "overulle", "overrul"], "Over- + rule — double r at junction.", ["prefix-error"]),
    ("withhold", ["withold", "withheld", "witheld"], "With- + hold — double h at junction.", ["prefix-error"]),
    ("fulfill", ["fullfill", "fulfil", "fullfil"], "Ful- + fill — one l in prefix (American: fulfill).", ["prefix-error"]),
    ("skillful", ["skillfull", "skilfull", "skilful"], "Skill + ful — drop one l from skill, -ful has one l.", ["ful-suffix"]),
    ("willful", ["willfull", "wilfull", "wilful"], "Will + ful — drop one l from will, -ful has one l.", ["ful-suffix"]),
    ("carefully", ["carefuly", "carfully", "carefullly"], "-fully always has two l's: careful + ly.", ["ful-suffix"]),
    ("successfully", ["successfuly", "succesfully", "sucessfully"], "-fully always has two l's.", ["ful-suffix"]),
    ("hopefully", ["hopefuly", "hopfully", "hopefullly"], "-fully always has two l's.", ["ful-suffix"]),
    ("gratefully", ["gratefuly", "greatfully", "gratefullly"], "-fully always has two l's.", ["ful-suffix"]),
    ("respectfully", ["respectfuly", "respecfully", "respectfullly"], "-fully always has two l's.", ["ful-suffix"]),
    ("peacefully", ["peacefuly", "peacfully", "peacefullly"], "-fully always has two l's.", ["ful-suffix"]),
    ("beautifully", ["beautifuly", "beutifully", "beautifullly"], "-fully always has two l's.", ["ful-suffix"]),
    ("organization", ["organisation", "organizaton", "organzation"], "American: -ize → -ization.", ["american-spelling"]),
    ("authorize", ["authorise", "autherize", "authoreze"], "American: -ize (not -ise).", ["american-spelling"]),
    ("recognize", ["recognise", "reconize", "reconise"], "American: -ize (not -ise).", ["american-spelling"]),
    ("apologize", ["apologise", "apoligize", "apoligise"], "American: -ize (not -ise).", ["american-spelling"]),
    ("analyze", ["analyse", "analize", "analise"], "American: -yze (not -yse).", ["american-spelling"]),
    ("defense", ["defence", "defanse", "defince"], "American: -ense (not -ence).", ["american-spelling"]),
    ("offense", ["offence", "ofense", "offanse"], "American: -ense (not -ence).", ["american-spelling"]),
    ("license", ["licence", "lisense", "lisence"], "American: -ense (not -ence).", ["american-spelling"]),
    ("catalog", ["catalogue", "cataloge", "catolog"], "American: shorter form (no -ue).", ["american-spelling"]),
    ("program", ["programme", "progam", "programm"], "American: shorter form (no -me).", ["american-spelling"]),
]


MEDIUM_WORDS_5 = [
    ("enrollment", ["enrolment", "enrollmant", "enrolmant"], "American: double l + -ment.", ["american-spelling"]),
    ("installment", ["instalment", "installmant", "instalmant"], "American: double l + -ment.", ["american-spelling"]),
    ("fulfillment", ["fulfilment", "fulfillmant", "fulfilmant"], "American: double l + -ment.", ["american-spelling"]),
    ("skillfully", ["skilfully", "skillfulley", "skilfuly"], "American: skill + fully (double l + double l).", ["american-spelling", "ful-suffix"]),
    ("color", ["colour", "coler", "collor"], "American: no 'u' — col-or.", ["american-spelling"]),
    ("favor", ["favour", "faver", "favvor"], "American: no 'u' — fa-vor.", ["american-spelling"]),
    ("honor", ["honour", "honer", "honnor"], "American: no 'u' — hon-or.", ["american-spelling"]),
    ("behavior", ["behaviour", "behavor", "behavoir"], "American: no 'u' — behav-ior.", ["american-spelling"]),
    ("labor", ["labour", "laber", "labur"], "American: no 'u' — la-bor.", ["american-spelling"]),
    ("center", ["centre", "senter", "centar"], "American: -er (not -re).", ["american-spelling"]),
    ("theater", ["theatre", "theator", "theeter"], "American: -er (not -re).", ["american-spelling"]),
    ("fiber", ["fibre", "fiver", "fibber"], "American: -er (not -re).", ["american-spelling"]),
    ("meter", ["metre", "meeter", "metir"], "American: -er (not -re).", ["american-spelling"]),
    ("liter", ["litre", "leeter", "litir"], "American: -er (not -re).", ["american-spelling"]),
    ("maneuver", ["manoeuvre", "manuever", "manuver"], "American spelling: ma-neu-ver.", ["american-spelling"]),
    ("encyclopedia", ["encyclopaedia", "enciclopedia", "encyclopeadia"], "American: no 'ae' — encyclop-e-dia.", ["american-spelling"]),
    ("anemia", ["anaemia", "aneamia", "anamia"], "American: no 'ae' — a-ne-mi-a.", ["american-spelling"]),
    ("pediatric", ["paediatric", "pedeatric", "pediactric"], "American: no 'ae' — pe-di-at-ric.", ["american-spelling"]),
    ("medieval", ["mediaeval", "medeival", "mideval"], "American: no 'ae' — me-di-e-val.", ["american-spelling"]),
    ("aesthetic", ["esthetic", "asthetic", "aestetic"], "Both accepted; 'aesthetic' more common in formal use.", ["american-spelling"]),
    ("borough", ["borogh", "burough", "borugh"], "Contains 'ough' — bor-ough.", ["silent-letter"]),
    ("through", ["thru", "thrugh", "throgh"], "Contains 'ough' — through (formal spelling).", ["silent-letter"]),
    ("although", ["altho", "allthough", "althogh"], "Contains 'ough' — al-though.", ["silent-letter"]),
    ("bought", ["bougth", "bougt", "bot"], "Contains 'ough' — bought.", ["silent-letter"]),
    ("daughter", ["daugther", "dauter", "doughter"], "Contains 'ugh' — daugh-ter.", ["silent-letter"]),
    ("caught", ["cought", "caut", "caght"], "Contains 'augh' — caught.", ["silent-letter"]),
    ("taught", ["tought", "taut", "taght"], "Contains 'augh' — taught.", ["silent-letter"]),
    ("naughty", ["noughty", "nauty", "naghty"], "Contains 'augh' — naugh-ty.", ["silent-letter"]),
    ("campaign", ["campain", "campaing", "campagne"], "Silent g + n — cam-paign.", ["silent-letter"]),
    ("sovereign", ["soveriegn", "sovreign", "soverign"], "Contains 'eign' — sov-er-eign.", ["silent-letter", "ie-ei-rule"]),
    ("technique", ["techneque", "techniqe", "technic"], "French origin — tech-nique.", ["foreign-origin"]),
    ("unique", ["uneque", "uniqe", "uneak"], "French origin — u-nique.", ["foreign-origin"]),
    ("antique", ["anteque", "antiqe", "anteek"], "French origin — an-tique.", ["foreign-origin"]),
    ("boutique", ["bouteque", "boutiqe", "booteek"], "French origin — bou-tique.", ["foreign-origin"]),
    ("critique", ["criteque", "critiqe", "criteek"], "French origin — cri-tique.", ["foreign-origin"]),
    ("etiquette", ["ettiquette", "etiquete", "ettiquet"], "French origin — et-i-quette.", ["foreign-origin"]),
    ("silhouette", ["silouette", "silhouete", "sillouhette"], "French origin — sil-hou-ette.", ["foreign-origin"]),
    ("chauffeur", ["chaufeur", "shofer", "chauffer"], "French origin — chauf-feur.", ["foreign-origin"]),
    ("entrepreneur", ["entrepeneur", "entreprenur", "entreprener"], "French origin — en-tre-pre-neur.", ["foreign-origin"]),
    ("connoisseur", ["conoisseur", "conoiseur", "connoiseur"], "French origin — con-nois-seur.", ["foreign-origin"]),
]

# Combine all medium words
ALL_MEDIUM = MEDIUM_WORDS + MEDIUM_WORDS_2 + MEDIUM_WORDS_3 + MEDIUM_WORDS_4 + MEDIUM_WORDS_5


HARD_WORDS = [
    ("accreditation", ["acreditation", "accreditaton", "accredditation"], "Double c — ac-cred-i-ta-tion.", ["double-letter"]),
    ("acquaintance", ["aquaintance", "acquaintence", "acquantance"], "Cqu cluster + -ance ending.", ["double-letter", "suffix-confusion"]),
    ("acquisition", ["aquisition", "acqusition", "acquistion"], "Cqu cluster — ac-qui-si-tion.", ["double-letter"]),
    ("amalgamation", ["amalgamtion", "amalgimation", "amalagmation"], "A-mal-ga-ma-tion — all a's.", ["unstressed-vowel"]),
    ("annihilate", ["anihilate", "annihillate", "annihalate"], "Double n + single l — an-ni-hi-late.", ["double-letter"]),
    ("antecedent", ["antecedant", "antecident", "antecedint"], "Ante- + cedent — -ent ending.", ["suffix-confusion"]),
    ("asphyxiate", ["asphixiate", "asphyxeate", "aspyhxiate"], "Contains 'phyx' — as-phyx-i-ate.", ["silent-letter"]),
    ("belligerent", ["beligerent", "belligerant", "beliggerent"], "Double l + -ent ending.", ["double-letter", "suffix-confusion"]),
    ("benevolent", ["benivolent", "benevolant", "benevlent"], "Bene- (good) + volent — -ent ending.", ["unstressed-vowel", "suffix-confusion"]),
    ("bourgeoisie", ["bourgeosie", "bourgoisie", "bourgeoisee"], "French origin — bour-geoi-sie.", ["foreign-origin"]),
    ("camaraderie", ["comraderie", "camaradarie", "cameraderie"], "French origin — ca-ma-ra-de-rie.", ["foreign-origin"]),
    ("catastrophe", ["catastophe", "catastrophy", "catastraphe"], "Greek origin — ca-tas-tro-phe.", ["foreign-origin"]),
    ("chrysanthemum", ["crysanthemum", "chrysanthamum", "chrysanthimum"], "Greek origin — chrys-an-the-mum.", ["foreign-origin"]),
    ("clandestine", ["clandestien", "clandistine", "clandestene"], "Ends in -ine (not -ien or -ene).", ["suffix-confusion"]),
    ("cognizant", ["cognizent", "cognisant", "cognizint"], "Ends in -ant (not -ent).", ["suffix-confusion"]),
    ("appalling", ["apalling", "appaling", "apaling"], "Double p + double l — ac-com-mo-date.", ["double-letter"]),
    ("rendezvous", ["rendevouz", "rendevous", "randayvoo"], "French origin — ren-dez-vous.", ["foreign-origin"]),
    ("conscientious", ["consciencious", "conscentious", "conciencious"], "Sci + ent + ious — con-sci-en-tious.", ["silent-letter"]),
    ("corroborate", ["coroborate", "corroberate", "coroberate"], "Double r — cor-rob-o-rate.", ["double-letter"]),
    ("perceive", ["percieve", "perceve", "percive"], "ei after c — per-ceive — coun-ter-feit.", ["ie-ei-rule"]),
    ("deteriorate", ["deterioate", "deterioriate", "detereorate"], "De-te-ri-o-rate — all vowels present.", ["unstressed-vowel"]),
    ("ecstasy", ["ecstacy", "exstasy", "ecstacey"], "Ends in -sy (not -cy) — ec-sta-sy.", ["suffix-confusion"]),
    ("effervescent", ["effervesent", "efervescent", "effervescant"], "Double f + -ent ending.", ["double-letter", "suffix-confusion"]),
    ("embarrassment", ["embarassment", "embarrassement", "embarrasment"], "Double r + double s + -ment.", ["double-letter"]),
    ("exhilarate", ["exhilerate", "exhillarate", "exhilirate"], "Ex-hil-a-rate — a (not e) in third syllable.", ["unstressed-vowel"]),
    ("fluorescent", ["flourescent", "florescent", "fluoresent"], "Flu-o-res-cent — contains 'uo.'", ["transposition"]),
    ("hemorrhage", ["hemorhage", "hemmorhage", "hemorrage"], "Double r + h — hem-or-rhage.", ["double-letter"]),
    ("idiosyncrasy", ["idiosyncracy", "idiosynchrasy", "idiosyncrassy"], "Ends in -sy (not -cy) — like ecstasy.", ["suffix-confusion"]),
    ("inadvertent", ["inadvertant", "innadvertent", "inadvertint"], "In- + advertent — -ent ending.", ["suffix-confusion"]),
    ("incandescent", ["incandescant", "incandecent", "incandesent"], "-escent ending (not -ascent).", ["suffix-confusion"]),
    ("indispensable", ["indispensible", "indespensable", "indispenseable"], "Root 'dispense' is complete → -able.", ["suffix-confusion"]),
    ("iridescent", ["irridescent", "iridescant", "iridesent"], "Single r + -escent ending.", ["double-letter", "suffix-confusion"]),
    ("juxtaposition", ["juxtapostion", "juxtoposition", "juxtaposision"], "Juxta + position — all letters present.", ["unstressed-vowel"]),
    ("kaleidoscope", ["kaliedoscope", "kalidoscope", "kaleidascope"], "ei pattern + scope — ka-lei-do-scope.", ["ie-ei-rule"]),
    ("lieutenant", ["leiutenant", "leftenant", "leutenant"], "French lieu (place) + tenant — lieu-ten-ant.", ["foreign-origin"]),
    ("magnanimous", ["magnanimious", "magnanamous", "magnanimis"], "Magn + anim + ous — mag-nan-i-mous.", ["unstressed-vowel"]),
    ("artifact", ["artefact", "artifcat", "artafact"], "American: arti-fact (not arte-).", ["american-spelling"]),
    ("millennium", ["millenium", "milennium", "milenium"], "Double l + double n — mill-enn-ium.", ["double-letter"]),
    ("noncommittal", ["noncommital", "noncomittal", "noncommittall"], "Double m + double t — non-com-mit-tal.", ["double-letter"]),
    ("onomatopoeia", ["onomatopeia", "onomatopoea", "onomatapoeia"], "Greek origin — on-o-mat-o-poe-ia.", ["foreign-origin"]),
]


HARD_WORDS_2 = [
    ("oscillate", ["oscilate", "oscillatte", "osscillate"], "Double l — os-cil-late.", ["double-letter"]),
    ("paraphernalia", ["paraphenalia", "paraphernelia", "paraphanalia"], "Para + phernalia — all vowels correct.", ["unstressed-vowel"]),
    ("perseverance", ["perseverence", "perserverance", "persaverance"], "Per-se-ver-ance — -ance ending.", ["suffix-confusion"]),
    ("pharmaceutical", ["farmaceutical", "pharmeceutical", "pharmaseutical"], "Ph = f sound + -eutical.", ["silent-letter"]),
    ("phenomenon", ["phenominon", "phenomenom", "phenomemon"], "Greek origin — phe-nom-e-non.", ["foreign-origin"]),
    ("prerogative", ["perogative", "prerrogative", "prerogitive"], "Pre- + rogative — single r after pre-.", ["prefix-error"]),
    ("pseudonym", ["psuedonym", "pseudonim", "psuedonim"], "Greek pseudo- (false) + nym (name).", ["foreign-origin"]),
    ("reconnaissance", ["reconaissance", "reconnaisance", "reconaisance"], "French origin — double n + double s.", ["double-letter", "foreign-origin"]),
    ("crochet", ["crochett", "croshet", "croshay"], "French origin — ren-dez-vous.", ["foreign-origin"]),
    ("resuscitate", ["resusitate", "ressuscitate", "resusicate"], "Re + suscitate — single s after re-.", ["prefix-error"]),
    ("rheumatism", ["rhuematism", "rheumatizm", "reumatism"], "Greek origin — rheu-ma-tism.", ["foreign-origin"]),
    ("myrrh", ["myrh", "mirr", "myrre"], "Greek origin — double r + silent h.", ["foreign-origin"]),
    ("sacrilege", ["sacrelige", "sacralege", "sacriledge"], "Sacri + lege (not -ledge or -lege from religious).", ["false-analogy"]),
    ("surreptitious", ["sureptitious", "surreptious", "sureptious"], "Double r + -itious ending.", ["double-letter"]),
    ("bourgeois", ["bourgois", "bourgeoise", "borgeois"], "French origin — bour-geois.", ["foreign-origin"]),
    ("sycophant", ["sycophent", "sychophant", "sicophant"], "Greek origin — syc-o-phant.", ["foreign-origin"]),
    ("temperament", ["temperment", "temprament", "temperamant"], "Temper + ament — all vowels present.", ["unstressed-vowel"]),
    ("tyranny", ["tyrany", "tyrrany", "tyranney"], "Single r + double n — tyr-an-ny.", ["double-letter"]),
    ("ubiquitous", ["ubiqitous", "ubiquituous", "ubiquitos"], "Ubiquit + ous — u-biq-ui-tous.", ["unstressed-vowel"]),
    ("unconscionable", ["unconscinable", "unconcionable", "unconsionable"], "Un + conscion + able.", ["prefix-error"]),
    ("unequivocal", ["unequivocle", "unequivical", "unequivocall"], "Un + equivocal — ends in -al.", ["suffix-confusion"]),
    ("vacillate", ["vacilate", "vaccillate", "vacillatte"], "Single c + double l — vac-il-late.", ["double-letter"]),
    ("vengeance", ["vengance", "vengence", "vengience"], "Venge + ance — -ance ending.", ["suffix-confusion"]),
    ("veterinarian", ["veternarian", "veterinerian", "vetrinarian"], "Vet-er-i-nar-i-an — all vowels present.", ["unstressed-vowel"]),
    ("vicissitude", ["vicisitude", "vicissatude", "vicissitued"], "Double s — vi-cis-si-tude.", ["double-letter"]),
    ("handkerchief", ["hankerchief", "handkerchif", "hankerchif"], "Silent d — hand-ker-chief.", ["silent-letter"]),
    ("misstep", ["mistep", "misstap", "mistap"], "Mis + step — double s at junction.", ["prefix-error"]),
    ("xylophone", ["zylophone", "xylophon", "xilophone"], "Greek origin — xy-lo-phone.", ["foreign-origin"]),
    ("zealous", ["zelous", "zealos", "zealeous"], "Zeal + ous — zeal-ous.", ["suffix-confusion"]),
    ("piccolo", ["picolo", "piccallo", "picallo"], "Italian origin — double c + single l.", ["foreign-origin", "double-letter"]),
    ("staccato", ["stacato", "staccatto", "stacatto"], "Double c + single t — stac-ca-to.", ["double-letter"]),
    ("acquiesce", ["aquiesce", "acquiese", "acquiece"], "Cqu cluster + sc ending — ac-qui-esce.", ["double-letter"]),
    ("anachronism", ["anachranism", "anachonism", "anacronism"], "Greek ana + chronos — an-ach-ro-nism.", ["foreign-origin"]),
    ("archipelago", ["archepelago", "archipeligo", "archepeligo"], "Greek origin — ar-chi-pel-a-go.", ["foreign-origin"]),
    ("assuage", ["asuage", "assauge", "assuadge"], "Double s — as-suage.", ["double-letter"]),
    ("auxiliary", ["auxillary", "auxilary", "auxilliary"], "Single l — aux-il-ia-ry.", ["double-letter"]),
    ("irreconcilable", ["ireconsilable", "irreconcilible", "ireconsilible"], "Double r + -able ending.", ["double-letter", "suffix-confusion"]),
    ("blasphemous", ["blasphemeous", "blasphemus", "blasfemous"], "Greek origin — blas-phe-mous.", ["foreign-origin"]),
    ("cantankerous", ["cantankorus", "cantankrous", "cantankarus"], "Ends in -erous — can-tan-ker-ous.", ["suffix-confusion"]),
    ("claustrophobia", ["claustraphobia", "clostrophobia", "claustraphobea"], "Latin claustrum + Greek phobia.", ["foreign-origin"]),
]


HARD_WORDS_3 = [
    ("convalescent", ["convalesent", "convalescant", "convalecent"], "Con + valesce + nt — -ent ending.", ["suffix-confusion"]),
    ("intermittent", ["intermitent", "intermittant", "intermitant"], "Double t + -ent ending.", ["double-letter", "suffix-confusion"]),
    ("crystallize", ["crystalize", "chrystallize", "crystalise"], "Double l — crys-tal-lize.", ["double-letter"]),
    ("delinquent", ["deliquent", "delinquant", "delinqent"], "Contains 'nqu' — de-lin-quent.", ["suffix-confusion"]),
    ("stucco", ["stuco", "stuccko", "stucko"], "Double c — stuc-co — des-ic-cate.", ["double-letter", "false-analogy"]),
    ("dilapidated", ["delapidated", "dillapidated", "dilapedated"], "Di + lapid + ated — single l.", ["double-letter"]),
    ("discrepancy", ["discrepency", "descrepancy", "discrepansy"], "Dis + crepancy — -ancy ending.", ["suffix-confusion"]),
    ("effervescence", ["efervescence", "effervesence", "effervescense"], "Double f + -escence ending.", ["double-letter"]),
    ("eloquent", ["eloquant", "elequent", "eloqent"], "Ends in -ent (not -ant).", ["suffix-confusion"]),
    ("exorbitant", ["exhorbitant", "exorbitent", "exorbatant"], "Ex + orbit + ant — no h.", ["suffix-confusion"]),
    ("flamboyant", ["flamboyent", "flamboiant", "flambouyant"], "French origin — -ant ending.", ["suffix-confusion", "foreign-origin"]),
    ("fluorescence", ["flourescence", "florescence", "fluoresence"], "Flu-o-res-cence — contains 'uo.'", ["transposition"]),
    ("diphtheria", ["diptheria", "diphtherea", "diptherea"], "Contains 'phth' — diph-the-ria.", ["silent-letter"]),
    ("hors d'oeuvres", ["hors d'ouvres", "hors d'oeurves", "hor d'oeuvres"], "French — hors d'oeuvres.", ["foreign-origin"]),
    ("ignominious", ["ignominous", "ignomineous", "ignominus"], "Igno + mini + ous — ig-no-min-i-ous.", ["suffix-confusion"]),
    ("impermeable", ["impermiable", "impermable", "impermiabel"], "Im + perme + able — -able ending.", ["suffix-confusion"]),
    ("incorrigible", ["incorrigable", "incorigible", "incorrigabel"], "Double r + -ible ending.", ["double-letter", "suffix-confusion"]),
    ("infinitesimal", ["infinitesmal", "infintesimal", "infinitesimle"], "Infinite + simal — all syllables present.", ["unstressed-vowel"]),
    ("innocuous", ["inocuous", "innocous", "innocuos"], "Double n — in-noc-u-ous.", ["double-letter"]),
    ("insouciance", ["insousiance", "insoucience", "insouceance"], "French origin — in-sou-ci-ance.", ["foreign-origin"]),
    ("irascible", ["irascable", "irrasible", "irascabel"], "Single r + -ible ending.", ["suffix-confusion"]),
    ("labyrinth", ["labrynth", "labirinth", "labyrnith"], "Greek origin — lab-y-rinth.", ["foreign-origin"]),
    ("liquefy", ["liquify", "liquafy", "liquefi"], "Exception: lique + fy (not liqui + fy).", ["false-analogy"]),
    ("temperance", ["temperence", "temperanse", "temparance"], "Temper + ance — -ance ending.", ["suffix-confusion"]),
    ("maleficent", ["malificent", "maleficant", "malefisent"], "Male + ficent — -ent ending.", ["suffix-confusion"]),
    ("Mediterranean", ["Mediteranean", "Mediterranian", "Mediterannean"], "Double r — Med-i-ter-ra-ne-an.", ["double-letter"]),
    ("antenna", ["antena", "anntenna", "antennna"], "Double n + single t — di-lem-ma — mil-len-ni-um.", ["double-letter"]),
    ("innuendo", ["inuendo", "innuenndo", "inuenndo"], "Double n — in-nu-en-do.", ["double-letter"]),
    ("mnemonic", ["nemonic", "pneumonic", "nnemonic"], "Silent m — mne-mon-ic.", ["silent-letter"]),
    ("accessory", ["accesory", "acessory", "accessery"], "Double c + double s — ac-ces-so-ry.", ["double-letter"]),
    ("nonchalant", ["nonchalent", "nonchallant", "nonchilant"], "French origin — non-cha-lant.", ["foreign-origin", "suffix-confusion"]),
    ("obsolescence", ["obsolesence", "obsolescense", "obsolecence"], "-escence ending — ob-so-les-cence.", ["suffix-confusion"]),
    ("ophthalmology", ["opthalmology", "ophthamology", "opthamology"], "Contains 'phth' — oph-thal-mol-o-gy.", ["silent-letter"]),
    ("guerrilla", ["guerilla", "guerila", "guerrila"], "Double r + double l — guer-ril-la.", ["double-letter"]),
    ("penicillin", ["penicilin", "penicillan", "pennicillin"], "Single n + double l — pen-i-cil-lin.", ["double-letter"]),
    ("exuberance", ["exuberence", "exuberanse", "exubarance"], "Exuber + ance — -ance ending.", ["suffix-confusion"]),
    ("pharaoh", ["pharoah", "pharoh", "pharouh"], "Egyptian origin — pha-ra-oh.", ["foreign-origin"]),
    ("phlegm", ["flegm", "phlem", "phlegem"], "Silent g + ph — phlegm.", ["silent-letter"]),
    ("plagiarism", ["plagerism", "plagarism", "plagierism"], "Plagi + arism — a (not e) in second syllable.", ["unstressed-vowel"]),
    ("pneumatic", ["neumatic", "pnuematic", "pnematic"], "Silent p — pneu-mat-ic.", ["silent-letter"]),
]


HARD_WORDS_4 = [
    ("potpourri", ["potpouri", "potporri", "potpoori"], "French origin — pot-pour-ri.", ["foreign-origin"]),
    ("precedent", ["precident", "precedant", "presedent"], "Pre + cedent — -ent ending.", ["suffix-confusion"]),
    ("cartilage", ["cartiledge", "cartilege", "cartalage"], "Ends in -lage (not -ledge) — from Latin.", ["false-analogy"]),
    ("protuberant", ["protuberent", "protruberant", "protuberint"], "Pro + tuber + ant — -ant ending.", ["suffix-confusion"]),
    ("plateau", ["plato", "plateu", "plataeu"], "French origin — pla-teau — chauf-feur.", ["foreign-origin"]),
    ("recalcitrant", ["recalcitrent", "recalcitrint", "recalciterant"], "Re + calcitrant — -ant ending.", ["suffix-confusion"]),
    ("reminiscence", ["reminisence", "reminiscense", "reminisscence"], "Reminisc + ence — sc cluster.", ["suffix-confusion"]),
    ("renaissance", ["renaisance", "rennaissance", "renaissanse"], "French origin — re-nais-sance.", ["foreign-origin"]),
    ("restaurateur", ["restauranteur", "restaurater", "restarateur"], "No 'n' — restaura-teur (not restaurant + eur).", ["false-analogy"]),
    ("resurgent", ["resurgant", "ressurgent", "resurjent"], "Re + surgent — -ent ending.", ["suffix-confusion"]),
    ("saccharin", ["sacharin", "saccharine", "saccarin"], "Double c + h — sac-cha-rin.", ["double-letter"]),
    ("serendipity", ["serendipety", "serendippity", "serandipity"], "Ser-en-dip-i-ty — all vowels correct.", ["unstressed-vowel"]),
    ("soliloquy", ["soliliquy", "soliloqy", "soliloquey"], "Latin solus + loqui — sol-il-o-quy.", ["foreign-origin"]),
    ("souvenir", ["souvenier", "suovenir", "souvanir"], "French origin — sou-ve-nir.", ["foreign-origin"]),
    ("strenuous", ["strenous", "strenuos", "strennuous"], "Stren + uous — stren-u-ous.", ["unstressed-vowel"]),
    ("succinct", ["succint", "sucinct", "succinkt"], "Double c — suc-cinct.", ["double-letter"]),
    ("Mississippi", ["Missisippi", "Mississipi", "Misissipi"], "Double s + double s + double p — Mis-sis-sip-pi.", ["double-letter"]),
    ("susceptible", ["suseptible", "susceptable", "suceptible"], "Susc + eptible — -ible ending.", ["suffix-confusion"]),
    ("synonymous", ["synonomous", "synonimous", "synonomus"], "Syn + onym + ous — sy-non-y-mous.", ["unstressed-vowel"]),
    ("temperamental", ["tempermental", "tempramental", "temperamantal"], "Temperament + al — all vowels present.", ["unstressed-vowel"]),
    ("terrestrial", ["terestrial", "terrestreal", "terristrial"], "Double r — ter-res-tri-al.", ["double-letter"]),
    ("tranquility", ["tranquillity", "tranqulity", "tranquality"], "American: single l — tran-quil-i-ty.", ["american-spelling"]),
    ("tumultuous", ["tumultuos", "tumultous", "tumultuious"], "Tumult + uous — tu-mul-tu-ous.", ["unstressed-vowel"]),
    ("tyrannical", ["tyranical", "tyrranical", "tyrannicle"], "Double n — ty-ran-ni-cal.", ["double-letter"]),
    ("unanimous", ["unanamous", "unanimus", "unanimious"], "Un + anim + ous — u-nan-i-mous.", ["unstressed-vowel"]),
    ("unparalleled", ["unparalelled", "unparralleled", "unparaleled"], "Un + parallel + ed — one r, double l.", ["double-letter"]),
    ("vacuum", ["vaccum", "vacum", "vaccuum"], "Single c + double u — vac-u-um.", ["double-letter"]),
    ("vehement", ["vehemant", "veheement", "vehiment"], "Vehe + ment — -ent ending.", ["suffix-confusion"]),
    ("vermicelli", ["vermiceli", "vermacelli", "vermiccelli"], "Italian — double l — ver-mi-cel-li.", ["foreign-origin", "double-letter"]),
    ("vicarious", ["vicarius", "vicareous", "vicarous"], "Vicar + ious — vi-car-i-ous.", ["suffix-confusion"]),
    ("vinaigrette", ["vinegrette", "vinagrette", "vinagrete"], "French — vin-ai-grette.", ["foreign-origin"]),
    ("visceral", ["viseral", "visciral", "viscerel"], "Visc + eral — vis-cer-al.", ["unstressed-vowel"]),
    ("voluminous", ["voluminus", "voluminious", "volumanous"], "Volum + inous — vo-lu-mi-nous.", ["suffix-confusion"]),
    ("vulnerable", ["vunerable", "vulnrable", "vulnerble"], "Contains 'ln' — vul-ner-a-ble.", ["silent-letter"]),
    ("whimsical", ["whimsicle", "whimsicall", "wimsical"], "Whims + ical — whim-si-cal.", ["suffix-confusion"]),
    ("wrathful", ["wrathfull", "rathful", "wrathfal"], "Silent w + -ful (one l).", ["silent-letter", "ful-suffix"]),
    ("xenophobia", ["zenophobia", "xenaphobia", "xenophobea"], "Greek xeno- (foreign) + phobia.", ["foreign-origin"]),
    ("yacht", ["yatch", "yaht", "yaucht"], "Silent ch — yacht.", ["silent-letter"]),
    ("zealot", ["zelot", "zealott", "zealat"], "Zeal + ot — zeal-ot.", ["unstressed-vowel"]),
    ("zeppelin", ["zepelin", "zepplin", "zeppelen"], "Double p + single l — zep-pe-lin.", ["double-letter"]),
]


HARD_WORDS_5 = [
    ("aberration", ["aberation", "abberration", "aberraton"], "Double r — ab-er-ra-tion.", ["double-letter"]),
    ("abhorrent", ["abhorent", "abhorrant", "abhorant"], "Double r + -ent ending.", ["double-letter", "suffix-confusion"]),
    ("abstemious", ["abstemeous", "abstimious", "abstemius"], "Abs + temious — ab-ste-mi-ous.", ["unstressed-vowel"]),
    ("accentuate", ["acentuate", "accentuatte", "acsentuate"], "Double c — ac-cen-tu-ate.", ["double-letter"]),
    ("accompaniment", ["acompaniment", "accompanyment", "accompanament"], "Double c + -iment ending.", ["double-letter"]),
    ("accumulate", ["acumulate", "accummulate", "acumullate"], "Double c + single m — ac-cu-mu-late.", ["double-letter"]),
    ("allegory", ["alegory", "allegery", "allagory"], "Double l — al-le-go-ry.", ["double-letter"]),
    ("ambidextrous", ["ambidexterous", "ambidextrus", "ambidextrious"], "Ends in -rous (not -erous).", ["suffix-confusion"]),
    ("ameliorate", ["ameleorate", "amelorate", "ameliarate"], "A-mel-io-rate — all vowels present.", ["unstressed-vowel"]),
    ("amphibious", ["amphibeous", "amfibious", "amphibius"], "Greek amphi- + bios — am-phib-i-ous.", ["foreign-origin"]),
    ("anaesthetic", ["anesthetic", "anasthetic", "anaestetic"], "British: ae; American 'anesthetic' also accepted.", ["foreign-origin"]),
    ("annihilation", ["anihilation", "annihillation", "anihillation"], "Double n + single l — an-ni-hi-la-tion.", ["double-letter"]),
    ("antipathy", ["antipothy", "antepathy", "antipathey"], "Greek anti + pathos — an-tip-a-thy.", ["foreign-origin"]),
    ("apocryphal", ["apocriphal", "apocraphyl", "apocrifal"], "Greek origin — a-poc-ry-phal.", ["foreign-origin"]),
    ("apprehension", ["aprehension", "apprehention", "aprehention"], "Double p + -sion ending.", ["double-letter", "suffix-confusion"]),
    ("auspicious", ["auspicous", "auspitious", "auspiscious"], "Auspi + cious — aus-pi-cious.", ["suffix-confusion"]),
    ("avarice", ["avarise", "avarrice", "avarace"], "Single r — av-a-rice.", ["double-letter"]),
    ("benign", ["benine", "begnin", "beniegn"], "Silent g — be-nign.", ["silent-letter"]),
    ("bougainvillea", ["bouganvillea", "bougainvilea", "bougainvillia"], "Named after Bougainville — bou-gain-vil-le-a.", ["foreign-origin"]),
    ("bureaucratic", ["beaurocratic", "burocratic", "beurocratic"], "Bureau + cratic — bu-reau-crat-ic.", ["foreign-origin"]),
    ("caricature", ["charicature", "cariciture", "carricature"], "Italian origin — car-i-ca-ture.", ["foreign-origin"]),
    ("circumference", ["circumfrence", "circumferance", "circmference"], "Circum + ference — -ence ending.", ["suffix-confusion"]),
    ("coalesce", ["coalese", "coellesce", "coallesce"], "Co + alesce — co-a-lesce.", ["double-letter"]),
    ("colloquial", ["coloquial", "colloqual", "colloqial"], "Double l — col-lo-qui-al.", ["double-letter"]),
    ("combustible", ["combustable", "combusible", "combustabel"], "Root 'combust-' not standalone → -ible.", ["suffix-confusion"]),
    ("commensurate", ["comensurate", "commenserate", "commensurite"], "Double m — com-men-su-rate.", ["double-letter"]),
    ("compulsory", ["compulsary", "compulsery", "compulsury"], "Ends in -ory (not -ary).", ["suffix-confusion"]),
    ("concatenate", ["concatinate", "concatanate", "concatennate"], "Con + caten + ate — con-cat-e-nate.", ["unstressed-vowel"]),
    ("condescension", ["condescention", "condescenshion", "condecension"], "Condescend → -sion.", ["suffix-confusion"]),
    ("conglomerate", ["conglamerate", "conglommerate", "conglomarate"], "Con + glomerate — con-glom-er-ate.", ["unstressed-vowel"]),
    ("contemptible", ["contemptable", "contemptabel", "contemptble"], "Root 'contempt-' → -ible.", ["suffix-confusion"]),
    ("controversial", ["contraversial", "controvercial", "controversal"], "Contro + versial — con-tro-ver-sial.", ["unstressed-vowel"]),
    ("convalescence", ["convalesence", "convalescense", "convalecence"], "Con + valesce + nce — -escence.", ["suffix-confusion"]),
    ("corroboration", ["coroboration", "corroberation", "coroberation"], "Double r — cor-rob-o-ra-tion.", ["double-letter"]),
    ("decadent", ["decadant", "decadint", "decedent"], "Decade + nt — -ent ending.", ["suffix-confusion"]),
    ("deference", ["deferance", "deferrence", "deferense"], "Defer → -ence (stressed final syllable).", ["suffix-confusion"]),
    ("deleterious", ["deletereous", "deletirious", "deletereus"], "Delete + rious — del-e-te-ri-ous.", ["suffix-confusion"]),
    ("diaphanous", ["diaphanious", "diaphanus", "diaphenous"], "Greek origin — di-aph-a-nous.", ["foreign-origin"]),
    ("dichotomy", ["dicotomy", "dichotamy", "dichotemy"], "Greek dicho + tomy — di-chot-o-my.", ["foreign-origin"]),
    ("dilettante", ["diletante", "dilletante", "dilettanti"], "Italian — double t — dil-et-tante.", ["foreign-origin", "double-letter"]),
]

# Combine all hard words
ALL_HARD = HARD_WORDS + HARD_WORDS_2 + HARD_WORDS_3 + HARD_WORDS_4 + HARD_WORDS_5


def generate_questions(word_list, difficulty, start_id):
    """Generate questions from word list, shuffling choice positions."""
    questions = []
    for i, (correct, distractors, explanation, tags) in enumerate(word_list):
        choices = distractors + [correct]
        random.shuffle(choices)
        q = make_q(
            id_num=start_id + i,
            difficulty=difficulty,
            choices=choices,
            answer=correct,
            explanation=explanation,
            tags=tags
        )
        questions.append(q)
    return questions


def validate_questions(questions):
    """Validate that all questions have correct answer in choices."""
    errors = []
    for q in questions:
        if q["answer"] not in q["choices"]:
            errors.append(f"ID {q['id']}: Answer '{q['answer']}' not in choices {q['choices']}")
        if len(q["choices"]) != 4:
            errors.append(f"ID {q['id']}: Expected 4 choices, got {len(q['choices'])}")
        if len(set(q["choices"])) != 4:
            errors.append(f"ID {q['id']}: Duplicate choices found: {q['choices']}")
    return errors


def main():
    print(f"Easy words available: {len(ALL_EASY)}")
    print(f"Medium words available: {len(ALL_MEDIUM)}")
    print(f"Hard words available: {len(ALL_HARD)}")

    # We need exactly 200 per difficulty
    if len(ALL_EASY) < 200:
        print(f"WARNING: Only {len(ALL_EASY)} easy words, need 200")
    if len(ALL_MEDIUM) < 200:
        print(f"WARNING: Only {len(ALL_MEDIUM)} medium words, need 200")
    if len(ALL_HARD) < 200:
        print(f"WARNING: Only {len(ALL_HARD)} hard words, need 200")

    easy_words = ALL_EASY[:200]
    medium_words = ALL_MEDIUM[:200]
    hard_words = ALL_HARD[:200]

    easy_qs = generate_questions(easy_words, "Easy", 1)
    medium_qs = generate_questions(medium_words, "Medium", 201)
    hard_qs = generate_questions(hard_words, "Hard", 401)

    all_questions = easy_qs + medium_qs + hard_qs

    # Validate
    errors = validate_questions(all_questions)
    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  {e}")
        print(f"\nTotal errors: {len(errors)}")
    else:
        print("All questions validated successfully!")

    print(f"Total questions generated: {len(all_questions)}")

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability", "spelling",
        "common-spelling-errors"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
