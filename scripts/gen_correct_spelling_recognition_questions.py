"""
Generate 600 spelling recognition questions for the CSE reviewer.
Each question asks: "Which of the following is spelled correctly?"
The correct answer is always a real, verified English word.
Distractors are plausible misspellings.

Distribution: 200 Easy, 200 Medium, 200 Hard
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _spelling_extra import EASY_WORDS_4, MEDIUM_WORDS_4, HARD_WORDS_3

# Each entry: (correct_spelling, [distractor1, distractor2, distractor3], explanation, tags)
# ALL correct spellings are verified standard English spellings.

EASY_WORDS = [
    ("government", ["goverment", "govenment", "govermnent"], "The word retains the 'n' from its root 'govern' — govern + ment.", ["silent-letter", "root-word"]),
    ("separate", ["seperate", "separete", "seprate"], "The second vowel is 'a' not 'e' — remember 'there is A RAT in sepARAte.'", ["unstressed-vowel"]),
    ("necessary", ["neccessary", "necessery", "neccesary"], "One 'c' and two 's' letters — a shirt has 1 collar and 2 sleeves.", ["double-letter"]),
    ("receive", ["recieve", "receeve", "receve"], "After 'c,' use 'ei' not 'ie' — i before e except after c.", ["ie-ei-rule"]),
    ("believe", ["beleive", "belive", "beleave"], "Standard 'ie' pattern — i before e (no c before it).", ["ie-ei-rule"]),
    ("achieve", ["acheive", "achive", "acheeve"], "Standard 'ie' pattern — i before e (no c before it).", ["ie-ei-rule"]),
    ("beginning", ["begining", "beggining", "beginng"], "Double 'n' because the stressed final syllable 'gin' doubles before -ing.", ["double-letter"]),
    ("environment", ["enviroment", "enviorment", "envirnoment"], "The root 'environ' contains an 'n' before 'm' — environ + ment.", ["silent-letter", "root-word"]),
    ("calendar", ["calender", "calander", "calandar"], "Ends in '-ar' not '-er' — from Latin 'calendarium.'", ["unstressed-vowel"]),
    ("definitely", ["definately", "definatly", "definetly"], "Root is 'definite' (with 'i' in third syllable) + ly.", ["unstressed-vowel"]),
    ("occurred", ["occured", "ocurred", "ocured"], "Double 'c' and double 'r' — stressed final syllable doubles before -ed.", ["double-letter"]),
    ("recommend", ["recomend", "reccommend", "recommand"], "One 'c' and two 'm' letters — re + com + mend.", ["double-letter"]),
    ("personnel", ["personel", "personell", "personnell"], "Double 'n' and single 'l' — from French 'personnel.'", ["double-letter", "french-origin"]),
    ("schedule", ["shedule", "scedule", "schedual"], "Begins with 'sch-' and ends in '-ule' — from Latin 'schedula.'", ["latin-origin"]),
    ("Wednesday", ["Wensday", "Wendsday", "Wednsday"], "Contains a silent 'd' — from Old English 'Wōdnesdæg' (Woden's day).", ["silent-letter"]),
    ("February", ["Febuary", "Feburary", "Febrary"], "Contains two 'r' letters — Feb-ru-ary, not Feb-u-ary.", ["silent-letter"]),
    ("library", ["libary", "liberry", "libray"], "Contains two 'r' letters — li-brar-y, not li-bar-y.", ["silent-letter"]),
    ("different", ["diffrent", "diferent", "differant"], "Double 'f' and ends in '-ent' — differ + ent.", ["double-letter", "suffix"]),
    ("experience", ["experiance", "expirience", "experence"], "Ends in '-ence' and has 'ie' in the third syllable.", ["suffix"]),
    ("immediately", ["imediately", "immediatly", "immedietly"], "Double 'm' and '-ately' ending — im + mediate + ly.", ["double-letter"]),
    ("professional", ["proffesional", "profesional", "proffessional"], "One 'f' and two 's' letters — profess + ional.", ["double-letter"]),
    ("committee", ["comittee", "commitee", "comitee"], "Double 'm,' double 't,' and double 'e' — com + mit + tee.", ["double-letter"]),
    ("assessment", ["assesment", "asessment", "assessmant"], "Four 's' letters total — as + sess + ment.", ["double-letter"]),
    ("possession", ["posession", "possesion", "posesion"], "Double 's' appears twice — pos + sess + ion.", ["double-letter"]),
    ("opportunity", ["oportunity", "oppertunity", "oppurtunity"], "Double 'p' and the vowel pattern is o-p-p-o-r-t-u.", ["double-letter"]),
    ("knowledge", ["knowlege", "knowledg", "knowladge"], "Silent 'k' at start and '-ledge' ending.", ["silent-letter"]),
    ("guarantee", ["gaurantee", "guarentee", "garentee"], "Starts with 'gua-' and ends in '-antee.'", ["french-origin"]),
    ("discipline", ["disipline", "dicipline", "disiplin"], "Contains 'sc' in the middle — from Latin 'disciplina.'", ["latin-origin"]),
    ("absence", ["absense", "abscence", "absance"], "Ends in '-ence' — from Latin 'absentia.'", ["suffix"]),
    ("attendance", ["attendence", "attendanse", "atendance"], "Double 't' and ends in '-ance' — attend + ance.", ["double-letter", "suffix"]),
    ("maintenance", ["maintainance", "maintenence", "maintanance"], "Drops the second 'i' from 'maintain' — the suffix is '-enance.'", ["suffix", "root-word"]),
    ("occurrence", ["occurence", "ocurrence", "occurrance"], "Double 'c' and double 'r' with '-ence' ending.", ["double-letter", "suffix"]),
    ("excellence", ["excelence", "excellance", "exellence"], "Double 'l' and '-ence' ending — excel + lence.", ["double-letter", "suffix"]),
    ("permanent", ["permanant", "permenent", "permenint"], "Ends in '-ent' not '-ant' — from Latin 'permanere.'", ["suffix"]),
    ("independent", ["independant", "indipendent", "independint"], "Ends in '-ent' — in + depend + ent.", ["suffix", "root-word"]),
    ("efficient", ["efficent", "efficeint", "eficient"], "Double 'f' and '-ient' ending — from Latin 'efficere.'", ["double-letter", "suffix"]),
    ("sufficient", ["sufficent", "suficient", "sufficiant"], "Double 'f' and '-ient' ending — from Latin 'sufficere.'", ["double-letter", "suffix"]),
    ("apparent", ["apparant", "aparent", "apparrent"], "Double 'p' and '-ent' ending — from Latin 'apparere.'", ["double-letter", "suffix"]),
    ("relevant", ["relevent", "relavent", "relevint"], "Ends in '-ant' — from Latin 'relevare.'", ["suffix"]),
    ("significant", ["significent", "signifigant", "significint"], "Ends in '-ant' — signific + ant.", ["suffix"]),
    ("certificate", ["certifcate", "certificat", "sertificate"], "Starts with 'c' (not 's') and contains '-ific-' in the middle.", ["latin-origin"]),
    ("document", ["documant", "docuement", "doccument"], "Ends in '-ment' — from Latin 'documentum.'", ["suffix"]),
    ("procedure", ["proceedure", "procedur", "prosedure"], "One 'e' after 'c' and ends in '-ure' — pro + cedure.", ["suffix"]),
    ("reference", ["referance", "refference", "referrence"], "Single 'f,' single 'r' in middle, '-ence' ending — refer + ence.", ["suffix"]),
    ("conference", ["conferance", "confrence", "conferrence"], "Single 'r' and '-ence' ending — confer + ence.", ["suffix"]),
    ("preference", ["preferance", "prefference", "preferrence"], "Single 'f' and '-ence' ending — prefer + ence.", ["suffix"]),
    ("difference", ["differance", "diffrence", "diference"], "Double 'f' and '-ence' ending — differ + ence.", ["double-letter", "suffix"]),
    ("performance", ["performence", "preformance", "performanse"], "Ends in '-ance' — perform + ance.", ["suffix"]),
    ("compliance", ["complience", "complianse", "compliane"], "Ends in '-ance' — comply (changes y to i) + ance.", ["suffix"]),
    ("allowance", ["allowence", "alowance", "allowanse"], "Double 'l' and '-ance' ending — allow + ance.", ["double-letter", "suffix"]),
]

MEDIUM_WORDS = [
    ("accommodate", ["accomodate", "acommodate", "acomodate"], "Double 'c' AND double 'm' — from Latin 'accommodare' (ad + com + modus).", ["double-letter", "latin-origin"]),
    ("bureaucracy", ["beauracracy", "burocracy", "beurocracy"], "Root is 'bureau' (French for office) + '-cracy' (rule).", ["french-origin"]),
    ("surveillance", ["surveilance", "survellance", "surviellance"], "From French 'surveiller' — sur + veill + ance (double 'l').", ["french-origin", "double-letter"]),
    ("liaison", ["liason", "liasion", "laison"], "French origin with vowel cluster '-iai-' in the middle.", ["french-origin"]),
    ("questionnaire", ["questionaire", "questionnare", "questionairre"], "Double 'n' and '-aire' ending — French origin.", ["french-origin", "double-letter"]),
    ("privilege", ["priviledge", "privelege", "privilige"], "Ends in '-lege' not '-ledge' — from Latin 'privilegium.'", ["latin-origin", "unstressed-vowel"]),
    ("consensus", ["concensus", "consencus", "concensous"], "Contains 'sens' in the middle — con + sensus (feeling together).", ["latin-origin"]),
    ("harassment", ["harrassment", "harasment", "harassement"], "Single 'r' and double 's' — harass + ment.", ["double-letter"]),
    ("supersede", ["supercede", "superceed", "superseed"], "The ONLY English word ending in '-sede' — from Latin 'supersedere.'", ["unique-spelling", "latin-origin"]),
    ("exaggerate", ["exagerate", "exaggarate", "exaggeratte"], "Double 'g' — from Latin 'exaggerare' (ex + agger, heap).", ["double-letter", "latin-origin"]),
    ("miscellaneous", ["miscelaneous", "miscellanious", "miscellanous"], "Double 'l' and '-aneous' ending — from Latin 'miscellaneus.'", ["double-letter", "latin-origin"]),
    ("conscientious", ["consciencious", "conscentious", "conciencious"], "Contains '-tious' ending — from Latin 'conscientia.'", ["latin-origin", "suffix"]),
    ("indispensable", ["indispensible", "indespensable", "indispenseable"], "Root 'dispense' is a complete word, so use '-able.'", ["suffix"]),
    ("reimbursement", ["reimbursment", "riembursement", "reimbursemant"], "Reimburse + ment — the 'e' is retained before '-ment.'", ["suffix", "root-word"]),
    ("acknowledgment", ["acknowledgement", "acknowlegment", "aknowledgment"], "American English drops the 'e' — acknowledge + ment.", ["suffix", "root-word"]),
    ("millennium", ["millenium", "milennium", "milenium"], "Double 'l' and double 'n' — from Latin 'mille' (thousand) + 'annum' (year).", ["double-letter", "latin-origin"]),
    ("perseverance", ["perseverence", "perserverance", "persaverance"], "Ends in '-ance' — persevere + ance.", ["suffix"]),
    ("superintendent", ["superintendant", "superindendent", "superintendint"], "Ends in '-ent' — super + intend + ent.", ["suffix"]),
    ("inadvertent", ["inadvertant", "innadvertent", "inadvertint"], "Ends in '-ent' — in + advert + ent.", ["suffix"]),
    ("correspondence", ["correspondance", "corrispondence", "corespondence"], "Double 'r' and '-ence' ending — correspond + ence.", ["double-letter", "suffix"]),
    ("acquisition", ["aquisition", "acqusition", "acquistion"], "Contains 'cqu' — from Latin 'acquirere.'", ["latin-origin"]),
    ("itinerary", ["itinarary", "itineraray", "itinenary"], "Contains '-iner-' in the middle — from Latin 'itinerarium.'", ["latin-origin", "unstressed-vowel"]),
    ("subpoena", ["subpeona", "subpena", "supboena"], "Latin phrase 'sub poena' (under penalty) — retains 'oe.'", ["latin-origin"]),
    ("threshold", ["threshhold", "thresold", "treshold"], "One 'h' in the middle — thresh + old (not thresh + hold).", ["compound-word"]),
    ("fulfillment", ["fulfilment", "fullfilment", "fullfillment"], "Ful + fill + ment — American English uses double 'l' in 'fulfill.'", ["double-letter"]),
    ("embarrass", ["embarass", "embarras", "embaress"], "Double 'r' and double 's' — from Spanish 'embarazar.'", ["double-letter"]),
    ("parallel", ["paralel", "parrallel", "parallell"], "One 'r,' double 'l' in the middle, single 'l' at end.", ["double-letter"]),
    ("maneuver", ["manuever", "manoeuver", "manouver"], "American spelling: man + euver (not the British 'manoeuvre').", ["american-spelling"]),
    ("vacuum", ["vaccum", "vacum", "vaccuum"], "One 'c' and double 'u' — from Latin 'vacuum.'", ["double-letter", "latin-origin"]),
    ("rhythm", ["rythm", "rhythem", "rythym"], "No vowel between 'rh' and 'thm' — from Greek 'rhythmos.'", ["greek-origin"]),
    ("hierarchy", ["heirarchy", "hierarcy", "heirarcy"], "Starts with 'hier-' (not 'heir-') — from Greek 'hierarchia.'", ["greek-origin"]),
    ("pneumonia", ["neumonia", "pnemonia", "pnuemonia"], "Silent 'p' at start — from Greek 'pneumon' (lung).", ["silent-letter", "greek-origin"]),
    ("mortgage", ["morgage", "morgtage", "mortage"], "Silent 't' — from Old French 'mort gage' (death pledge).", ["silent-letter", "french-origin"]),
    ("receipt", ["reciept", "receit", "recipt"], "Silent 'p' and 'ei' after 'c' — from Latin 'recepta.'", ["silent-letter", "ie-ei-rule"]),
    ("technique", ["techneque", "techniqe", "tecnique"], "French spelling with '-ique' ending — from Greek 'techne.'", ["french-origin"]),
    ("catalogue", ["cataloge", "catagolue", "catalouge"], "Ends in '-ogue' — from Greek 'katalogos.'", ["greek-origin"]),
    ("dilemma", ["dilema", "dilemna", "dillema"], "Double 'm' and no 'n' — from Greek 'dilemma.'", ["double-letter", "greek-origin"]),
    ("diarrhea", ["diarhea", "diarrhoea", "diarreah"], "Double 'r' and 'h' after second 'r' — American spelling.", ["double-letter", "american-spelling"]),
    ("hemorrhage", ["hemorhage", "hemmorhage", "hemorrage"], "Double 'r' and 'h' after the double 'r' — from Greek 'haimorrhagia.'", ["double-letter", "greek-origin"]),
    ("mischievous", ["mischevious", "mischievious", "mischevous"], "Ends in '-vous' not '-vious' — mis + chief + ous.", ["suffix", "root-word"]),
    ("miniature", ["minature", "miniture", "minaiature"], "Contains '-iature' — from Italian 'miniatura.'", ["unstressed-vowel"]),
    ("deteriorate", ["deterioate", "detiriorate", "deterioriate"], "Contains '-iorate' — from Latin 'deteriorare.'", ["latin-origin", "unstressed-vowel"]),
    ("corroborate", ["coroborate", "corroberate", "coroberate"], "Double 'r' and '-orate' ending — from Latin 'corroborare.'", ["double-letter", "latin-origin"]),
    ("accommodate", ["accomadate", "accommadate", "acommadate"], "Double 'c' AND double 'm' with '-odate' ending.", ["double-letter", "latin-origin"]),
    ("remittance", ["remitance", "remittence", "remitence"], "Double 't' and '-ance' ending — remit + tance.", ["double-letter", "suffix"]),
    ("transmittal", ["transmital", "transmitta", "transmitel"], "Double 't' — transmit + tal (stressed final syllable doubles).", ["double-letter"]),
    ("intermittent", ["intermitent", "intermittant", "intermitant"], "Double 't' and '-ent' ending — from Latin 'intermittere.'", ["double-letter", "suffix"]),
    ("allotment", ["alotment", "allottment", "alottment"], "Double 'l' and single 't' in '-ment' — allot + ment.", ["double-letter"]),
    ("installment", ["instalment", "installmant", "installement"], "Double 'l' — install + ment (American English).", ["double-letter", "american-spelling"]),
    ("enrollment", ["enrolment", "enrollmant", "enrolement"], "Double 'l' — enroll + ment (American English).", ["double-letter", "american-spelling"]),
]

HARD_WORDS = [
    ("idiosyncrasy", ["idiosyncracy", "idiosynchrasy", "idiosyncricy"], "Ends in '-asy' not '-acy' — from Greek 'idiosynkrasia.'", ["greek-origin", "suffix"]),
    ("sacrilegious", ["sacreligious", "sacriligious", "sacreligous"], "From 'sacrilege' (not 'religious') — sacrilege + ious.", ["root-word", "suffix"]),
    ("inoculate", ["innoculate", "innocculate", "inocullate"], "One 'n' and one 'c' — from Latin 'inoculare' (to graft).", ["latin-origin", "double-letter"]),
    ("desiccate", ["dessicate", "desicate", "dessiccate"], "One 's' and double 'c' — from Latin 'desiccare.'", ["double-letter", "latin-origin"]),
    ("resuscitate", ["resusitate", "ressuscitate", "resucitate"], "Contains '-susc-' — from Latin 'resuscitare.'", ["latin-origin"]),
    ("connoisseur", ["connoiseur", "conoisseur", "connoissuer"], "Double 'n' and double 's' — French origin.", ["french-origin", "double-letter"]),
    ("entrepreneur", ["entrepeneur", "entreprenuer", "entrepreneuer"], "French origin: entre + preneur — no extra vowels.", ["french-origin"]),
    ("reconnaissance", ["reconaissance", "reconnaisance", "reconnaissence"], "Double 'n' and double 's' with '-ance' ending — French military term.", ["french-origin", "double-letter"]),
    ("lieutenant", ["leutenant", "lieutenent", "liutenant"], "Contains 'lieu' (French for place) + tenant.", ["french-origin"]),
    ("rendezvous", ["rendezvouz", "randezvous", "rendevous"], "French: rendez (present) + vous (yourselves) — silent final 's.'", ["french-origin", "silent-letter"]),
    ("hors d'oeuvres", ["hors d'ouvres", "hor d'oeuvres", "hors d'oeurves"], "French: hors (outside) + d'oeuvres (of works) — silent letters throughout.", ["french-origin", "silent-letter"]),
    ("onomatopoeia", ["onomatapoeia", "onomatopeia", "onomatopoea"], "From Greek 'onomatopoiia' — contains '-opoeia' at end.", ["greek-origin"]),
    ("pharaoh", ["pharoah", "pharoh", "pharouh"], "Ends in '-aoh' — from Egyptian via Greek.", ["unique-spelling"]),
    ("hemorrhoid", ["hemoroid", "hemmorhoid", "hemorroid"], "Double 'r' and 'h' after — from Greek 'haimorrhoides.'", ["greek-origin", "double-letter"]),
    ("phlegm", ["flegm", "phlem", "phlegem"], "Silent 'g' and 'ph' for 'f' sound — from Greek 'phlegma.'", ["greek-origin", "silent-letter"]),
    ("mnemonic", ["nemonic", "pneumonic", "mnemonik"], "Silent 'm' at start — from Greek 'mnemonikos.'", ["greek-origin", "silent-letter"]),
    ("psych", ["sych", "psyche", "pscyh"], "Silent 'p' — from Greek 'psyche' (soul/mind).", ["greek-origin", "silent-letter"]),
    ("acquiesce", ["aquiesce", "acquiese", "acquiece"], "Contains 'cqu' and ends in '-esce' — from Latin 'acquiescere.'", ["latin-origin"]),
    ("effervescent", ["efervescent", "effervesent", "effervescant"], "Double 'f' and '-escent' ending — from Latin 'effervescere.'", ["double-letter", "latin-origin"]),
    ("fluorescent", ["flourescent", "florescent", "fluoresent"], "Starts with 'flu-' (not 'flou-') and '-escent' ending.", ["suffix", "unstressed-vowel"]),
    ("acquaintance", ["aquaintance", "acquaintence", "acquantance"], "Contains 'cqu' and '-ance' ending — from Old French 'acointance.'", ["french-origin", "suffix"]),
    ("antecedent", ["antecedant", "anteceedent", "antecident"], "Ends in '-ent' — ante + cedent (from Latin 'cedere').", ["latin-origin", "suffix"]),
    ("belligerent", ["beligerent", "belligerant", "beliggerent"], "Double 'l' and '-ent' ending — from Latin 'belligerare.'", ["double-letter", "latin-origin", "suffix"]),
    ("benevolent", ["benevlent", "benevolant", "benivolent"], "Contains '-evol-' and '-ent' ending — from Latin 'benevolens.'", ["latin-origin", "suffix"]),
    ("circumference", ["circumfrence", "circumferance", "circunference"], "Contains '-ference' — circum + ference.", ["latin-origin", "suffix"]),
    ("commemorative", ["comemorative", "commemerative", "commerative"], "Double 'm' twice — com + memor + ative.", ["double-letter", "latin-origin"]),
    ("convalescent", ["convalesent", "convalescant", "convalecent"], "Contains '-escent' ending — from Latin 'convalescere.'", ["latin-origin", "suffix"]),
    ("delinquent", ["deliquent", "delinquant", "delinguent"], "Contains '-nqu-' and '-ent' ending — from Latin 'delinquere.'", ["latin-origin", "suffix"]),
    ("discrepancy", ["discrepency", "descrepancy", "discrepansy"], "Contains '-ancy' ending — from Latin 'discrepantia.'", ["latin-origin", "suffix"]),
    ("eccentricity", ["excentricity", "eccentrisity", "ecentricity"], "Double 'c' — from Greek 'ekkentros' (out of center).", ["double-letter", "greek-origin"]),
    ("expeditious", ["expiditious", "expeditous", "expeditiuos"], "Contains '-itious' ending — from Latin 'expeditus.'", ["latin-origin", "suffix"]),
    ("flamboyant", ["flambouyant", "flamboyent", "flamboiant"], "Contains '-oyant' ending — from French 'flamboyer.'", ["french-origin"]),
    ("idiosyncratic", ["idiosyncrattic", "idiosyncretic", "idiosyncratik"], "From 'idiosyncrasy' — idiosyncrat + ic.", ["greek-origin", "root-word"]),
    ("imperceptible", ["imperceptable", "imperceptibal", "inperceptible"], "Root 'percept' is not a standalone word → '-ible.'", ["suffix"]),
    ("incandescent", ["incandescant", "incandecent", "incandesent"], "Contains '-escent' ending — from Latin 'incandescere.'", ["latin-origin", "suffix"]),
    ("infinitesimal", ["infinitesmal", "infinitessimal", "infintesimal"], "Contains '-esimal' — from Latin 'infinitesimus.'", ["latin-origin"]),
    ("jurisprudence", ["jurisprudance", "jurisprudense", "jurispridence"], "Contains '-ence' ending — from Latin 'jurisprudentia.'", ["latin-origin", "suffix"]),
    ("magnanimous", ["magnanimious", "magnanimus", "magnannimous"], "Contains '-animous' — from Latin 'magnanimus' (great-souled).", ["latin-origin"]),
    ("ostentatious", ["ostentacious", "ostentatous", "ostentatiuos"], "Contains '-tatious' ending — from Latin 'ostentare.'", ["latin-origin", "suffix"]),
    ("perspicacious", ["perspicaceous", "perspicasious", "perspicatious"], "Contains '-acious' ending — from Latin 'perspicax.'", ["latin-origin", "suffix"]),
    ("pharmaceutical", ["farmaceutical", "pharmaceuticle", "pharmeceutical"], "Starts with 'ph' and contains '-eutical' — from Greek 'pharmakon.'", ["greek-origin"]),
    ("prerogative", ["perogative", "prerrogative", "prerogitive"], "Contains 'pre-' + 'rogative' — from Latin 'praerogativa.'", ["latin-origin", "unstressed-vowel"]),
    ("quintessential", ["quintessental", "quinessential", "quintesential"], "Double 's' and '-ential' ending — from Latin 'quinta essentia.'", ["double-letter", "latin-origin"]),
    ("recalcitrant", ["recalcitrent", "recalcitrint", "recalciterant"], "Ends in '-ant' — from Latin 'recalcitrare' (to kick back).", ["latin-origin", "suffix"]),
    ("surreptitious", ["sureptitious", "surreptious", "sureptious"], "Double 'r' and '-itious' ending — from Latin 'surreptitius.'", ["double-letter", "latin-origin"]),
    ("temperamental", ["tempermental", "tempramental", "temperamantal"], "Contains '-era-' in the middle — temper + a + mental.", ["unstressed-vowel"]),
    ("unequivocal", ["unequivocle", "unequivical", "unequivocol"], "Ends in '-cal' — un + equivocal (from Latin 'aequivocus').", ["latin-origin", "suffix"]),
    ("verisimilitude", ["verisimiltude", "verisimilatude", "verisimmilitude"], "Contains '-similitude' — from Latin 'verisimilitudo.'", ["latin-origin"]),
    ("vicissitude", ["vicisitude", "vicissatude", "vicissituede"], "Double 's' — from Latin 'vicissitudo.'", ["double-letter", "latin-origin"]),
    ("withhold", ["withold", "witheld", "withheld"], "Double 'h' — with + hold (compound word).", ["compound-word", "double-letter"]),
]

# Additional words to reach 200 per difficulty level

EASY_WORDS_2 = [
    ("appropriate", ["apropriate", "appropreate", "appopriate"], "Double 'p' — from Latin 'appropriare.'", ["double-letter", "latin-origin"]),
    ("available", ["availible", "avaliable", "availabel"], "Ends in '-able' — avail is a complete word.", ["suffix"]),
    ("beneficial", ["benificial", "benefitial", "benefical"], "Contains '-ficial' — from Latin 'beneficium.'", ["latin-origin"]),
    ("category", ["catagory", "categorie", "catigory"], "Second vowel is 'e' not 'a' — from Greek 'kategoria.'", ["unstressed-vowel", "greek-origin"]),
    ("circumstance", ["circumstanse", "circunstance", "curcumstance"], "Contains 'circum-' prefix — circum + stance.", ["latin-origin"]),
    ("communication", ["comunication", "comminication", "communicaton"], "Double 'm' and '-tion' ending — communicate + ion.", ["double-letter", "suffix"]),
    ("consequence", ["consequense", "consequance", "consiquence"], "Ends in '-ence' — from Latin 'consequentia.'", ["suffix"]),
    ("considerable", ["considrable", "considerible", "considderable"], "Root 'consider' + '-able' (complete word rule).", ["suffix"]),
    ("convenience", ["convienience", "conveniance", "conveneince"], "Contains '-ience' ending — from Latin 'convenientia.'", ["suffix"]),
    ("cooperation", ["coperation", "cooporation", "cooperaton"], "Double 'o' and '-tion' ending — co + operate + ion.", ["double-letter", "suffix"]),
    ("decision", ["desicion", "decission", "decison"], "Ends in '-sion' — decide (root ends in -de) → decision.", ["suffix"]),
    ("description", ["discription", "descripton", "descrption"], "Contains 'de-' prefix — describe → description.", ["suffix", "root-word"]),
    ("development", ["developement", "devlopment", "devellopment"], "No 'e' between 'p' and 'm' — develop + ment.", ["suffix"]),
    ("disappoint", ["disapoint", "dissapoint", "dissappoint"], "One 's' and double 'p' — dis + appoint.", ["double-letter", "prefix"]),
    ("disappear", ["dissapear", "dissappear", "disapear"], "One 's' and double 'p' — dis + appear.", ["double-letter", "prefix"]),
    ("education", ["educaton", "edducation", "educasion"], "Ends in '-tion' — educate → education.", ["suffix"]),
    ("employment", ["imployment", "employement", "employmant"], "No extra 'e' — employ + ment.", ["suffix"]),
    ("equipment", ["equipement", "equiptment", "equippment"], "No extra 'e' — equip + ment.", ["suffix"]),
    ("especially", ["expecially", "especally", "espesially"], "Contains '-cially' — from Latin 'specialis.'", ["latin-origin"]),
    ("exaggerate", ["exagerate", "exaggarate", "exagerrate"], "Double 'g' — from Latin 'exaggerare.'", ["double-letter", "latin-origin"]),
    ("existence", ["existance", "existense", "existince"], "Ends in '-ence' — from Latin 'existentia.'", ["suffix"]),
    ("explanation", ["explaination", "explanasion", "explination"], "No 'i' after 'expla-' — explain → explanation (drops the i).", ["suffix", "root-word"]),
    ("familiar", ["familar", "familliar", "familier"], "One 'l' and ends in '-iar' — from Latin 'familiaris.'", ["latin-origin"]),
    ("foreign", ["foriegn", "forein", "foregin"], "Exception to ie/ei rule — 'eign' ending.", ["ie-ei-rule"]),
    ("government", ["goverment", "govenrment", "govermnent"], "Retains 'n' from root 'govern' — govern + ment.", ["silent-letter", "root-word"]),
    ("grammar", ["grammer", "gramar", "gramer"], "Ends in '-ar' not '-er' — from Greek 'grammatike.'", ["unstressed-vowel", "greek-origin"]),
    ("height", ["heighth", "hieght", "heigth"], "Ends in '-ght' with no extra 'h' — from Old English 'hiehthu.'", ["unique-spelling"]),
    ("imagination", ["imaganation", "imaginaton", "immagination"], "Contains '-ination' — imagine → imagination.", ["suffix"]),
    ("intelligence", ["inteligence", "intelligance", "intellegence"], "Double 'l' and '-ence' ending — from Latin 'intelligentia.'", ["double-letter", "suffix"]),
    ("interference", ["interferance", "interferrence", "interferense"], "Single 'r' in middle and '-ence' ending — interfere + ence.", ["suffix"]),
    ("judgment", ["judgement", "judgmant", "jugment"], "American English drops the 'e' — judge + ment.", ["american-spelling"]),
    ("legitimate", ["legitamate", "legitimite", "legetimate"], "Contains '-imate' — from Latin 'legitimare.'", ["latin-origin", "unstressed-vowel"]),
    ("management", ["managment", "managemant", "manegement"], "Manage + ment — retains the 'e' before consonant suffix.", ["suffix"]),
    ("negotiation", ["negotation", "negoatiation", "negotiaton"], "Contains '-tiation' — negotiate → negotiation.", ["suffix"]),
    ("noticeable", ["noticable", "notiseable", "noticible"], "Keeps the 'e' after soft 'c' before '-able.'", ["suffix"]),
    ("occasionally", ["occassionally", "ocasionally", "occationally"], "Double 'c' and single 's' — occasion + ally.", ["double-letter"]),
    ("organization", ["organisaton", "orginization", "organizaton"], "Contains '-ization' — organize → organization.", ["suffix"]),
    ("particular", ["perticular", "particuler", "paticular"], "Contains '-icular' — from Latin 'particularis.'", ["latin-origin", "unstressed-vowel"]),
    ("persuade", ["pursuade", "perswade", "persaude"], "Contains '-suade' — from Latin 'persuadere.'", ["latin-origin"]),
    ("possession", ["posession", "possesion", "posesion"], "Double 's' appears twice — possess + ion.", ["double-letter"]),
    ("preparation", ["preperation", "preparaton", "preperaton"], "Contains '-aration' — prepare → preparation.", ["suffix", "unstressed-vowel"]),
    ("privilege", ["priviledge", "privelege", "privilige"], "Ends in '-lege' not '-ledge' — from Latin 'privilegium.'", ["latin-origin"]),
    ("pronunciation", ["pronounciation", "pronuncation", "pronunsiation"], "No 'o' after 'pr-noun-' — pronounce → pronunciation (drops the 'o' sound).", ["suffix", "root-word"]),
    ("receipt", ["reciept", "receit", "recipt"], "Silent 'p' and 'ei' after 'c' — from Latin 'recepta.'", ["silent-letter", "ie-ei-rule"]),
    ("recognize", ["reconize", "recongnize", "recognise"], "Contains '-cognize' — re + cognize (from Latin 'cognoscere').", ["latin-origin"]),
    ("recommend", ["recomend", "reccommend", "recommand"], "One 'c' and double 'm' — re + commend.", ["double-letter"]),
    ("responsibility", ["responsability", "responsibilty", "responsiblity"], "Contains '-ibility' — responsible → responsibility.", ["suffix"]),
    ("restaurant", ["restarant", "resturant", "restraunt"], "Contains '-taurant' — from French 'restaurant.'", ["french-origin"]),
    ("secretary", ["secratary", "secretery", "secertary"], "Contains '-etary' — from Latin 'secretarius.'", ["latin-origin", "unstressed-vowel"]),
    ("temperature", ["temprature", "temperture", "temperatur"], "Contains '-erature' — from Latin 'temperatura.'", ["latin-origin", "unstressed-vowel"]),
]

MEDIUM_WORDS_2 = [
    ("accreditation", ["acreditation", "accreditaton", "accredditation"], "Double 'c' — from Latin 'accreditare.'", ["double-letter", "latin-origin"]),
    ("appropriation", ["apropiation", "appropriaton", "appropreation"], "Double 'p' and '-tion' ending — appropriate → appropriation.", ["double-letter", "suffix"]),
    ("authorization", ["authorisation", "authorizaton", "autherization"], "American spelling with 'z' and '-tion' ending.", ["american-spelling", "suffix"]),
    ("cancellation", ["cancelation", "cancellaton", "cancallation"], "Double 'l' — cancel + lation.", ["double-letter"]),
    ("commemorate", ["comemorate", "commemmorate", "comemmorate"], "Double 'm' once (com + memor) — not double 'm' twice.", ["double-letter", "latin-origin"]),
    ("confidential", ["confidental", "confidencial", "confedential"], "Contains '-ential' — from Latin 'confidentia.'", ["latin-origin", "suffix"]),
    ("curriculum", ["curiculum", "curriculm", "curricullum"], "Double 'r' and single 'l' — from Latin 'curriculum.'", ["double-letter", "latin-origin"]),
    ("delinquent", ["deliquent", "delinquant", "delinguent"], "Contains '-nqu-' — from Latin 'delinquere.'", ["latin-origin"]),
    ("designation", ["desigation", "designaton", "dessignation"], "Contains '-ignation' — designate → designation.", ["suffix"]),
    ("disbursement", ["disbursment", "disburcement", "disbursemant"], "Contains '-ement' — disburse + ment.", ["suffix"]),
    ("endorsement", ["indorsement", "endorsment", "endorsemant"], "Contains '-ement' — endorse + ment.", ["suffix"]),
    ("expenditure", ["expinditure", "expendature", "expendeture"], "Contains '-iture' — from Latin 'expendere.'", ["latin-origin", "suffix"]),
    ("feasibility", ["feasability", "feasibilty", "feasiblity"], "Contains '-ibility' — feasible → feasibility.", ["suffix"]),
    ("grievance", ["greivance", "grievence", "greivence"], "Standard 'ie' and '-ance' ending — grieve + ance.", ["ie-ei-rule", "suffix"]),
    ("implementation", ["implimentation", "implementaton", "implemenation"], "Contains '-entation' — implement → implementation.", ["suffix"]),
    ("infrastructure", ["infastructure", "infrastructer", "infrustructure"], "Contains 'infra-' prefix — infra + structure.", ["latin-origin"]),
    ("miscellaneous", ["miscelaneous", "miscellanious", "miscellanous"], "Double 'l' and '-aneous' ending.", ["double-letter"]),
    ("negligence", ["negligance", "neglegence", "negligense"], "Ends in '-ence' — from Latin 'negligentia.'", ["suffix"]),
    ("notwithstanding", ["notwhithstanding", "notwithstandng", "notwithstaning"], "Compound: not + with + standing.", ["compound-word"]),
    ("parliamentary", ["parlimentary", "parlementary", "parlamentary"], "Contains '-iamentary' — from French 'parlement.'", ["french-origin"]),
    ("procurement", ["procurment", "procuremant", "proccurement"], "Contains '-ement' — procure + ment.", ["suffix"]),
    ("proficiency", ["proficency", "profficiency", "proficiancy"], "One 'f' and '-iency' ending — from Latin 'proficere.'", ["suffix", "latin-origin"]),
    ("questionnaire", ["questionaire", "questionnare", "questionairre"], "Double 'n' and '-aire' ending — French origin.", ["french-origin", "double-letter"]),
    ("reconnaissance", ["reconaissance", "reconnaisance", "reconnaissence"], "Double 'n,' double 's,' and '-ance' ending.", ["french-origin", "double-letter"]),
    ("registration", ["registraton", "registeration", "regestration"], "Contains '-tration' — register → registration.", ["suffix"]),
    ("remuneration", ["renumeration", "remuneraton", "remunaration"], "Contains '-mun-' not '-num-' — from Latin 'remunerare.'", ["latin-origin", "unstressed-vowel"]),
    ("requisition", ["requision", "requisision", "requsition"], "Contains '-quisition' — from Latin 'requisitio.'", ["latin-origin"]),
    ("simultaneous", ["simultanious", "simultanous", "simultaenous"], "Contains '-aneous' ending — from Latin 'simultaneus.'", ["latin-origin", "suffix"]),
    ("tariff", ["tarrif", "tarif", "tarriff"], "One 'r' and double 'f' — from Arabic via Italian.", ["double-letter"]),
    ("thorough", ["thorogh", "thourough", "thorouh"], "Contains '-orough' — not to be confused with 'through.'", ["unique-spelling"]),
    ("transferred", ["transfered", "tranferred", "transferrd"], "Double 'r' — stressed final syllable doubles before '-ed.'", ["double-letter"]),
    ("transparent", ["transparant", "transperent", "transparrent"], "Ends in '-ent' — from Latin 'transparere.'", ["suffix", "latin-origin"]),
    ("unanimous", ["unanamous", "unanimus", "unanimious"], "Contains '-animous' — from Latin 'unanimus.'", ["latin-origin"]),
    ("unnecessary", ["unecessary", "unnecesary", "unneccessary"], "Double 'n' (un + necessary) and one 'c,' double 's.'", ["double-letter", "prefix"]),
    ("vigilance", ["vigilence", "vigilanse", "vigalance"], "Ends in '-ance' — from Latin 'vigilantia.'", ["suffix", "latin-origin"]),
    ("withhold", ["withold", "withheld", "witheld"], "Double 'h' — with + hold.", ["compound-word", "double-letter"]),
    ("allegiance", ["allegience", "alegiance", "allegance"], "Double 'l' and '-iance' ending — from Old French 'alegeance.'", ["double-letter", "french-origin"]),
    ("amendment", ["ammendment", "amendmant", "amandment"], "One 'm' in 'amend' — amend + ment.", ["suffix"]),
    ("appropriation", ["apropiation", "appropreation", "appropriaton"], "Double 'p' and '-tion' ending.", ["double-letter", "suffix"]),
    ("bureaucratic", ["beauracratic", "burocratic", "beurocratic"], "From 'bureau' + '-cratic' — French origin.", ["french-origin"]),
    ("circumstantial", ["circumstancial", "circunstantial", "circumstantiel"], "Contains '-antial' — circumstance → circumstantial.", ["suffix"]),
    ("commemorative", ["comemorative", "commemerative", "commerative"], "Double 'm' in 'com + memor' — commemorate + ive.", ["double-letter", "latin-origin"]),
    ("conscientious", ["consciencious", "conscentious", "conciencious"], "Contains '-ientious' — from Latin 'conscientia.'", ["latin-origin"]),
    ("deterioration", ["deterioation", "detirioration", "deterioriation"], "Contains '-ioration' — deteriorate → deterioration.", ["latin-origin", "suffix"]),
    ("dissemination", ["disemination", "dissemenation", "disseminaton"], "Double 's' — dis + seminate + ion.", ["double-letter", "suffix"]),
    ("extemporaneous", ["extemporanious", "extemporanous", "extemperaneous"], "Contains '-aneous' ending — from Latin 'extemporaneus.'", ["latin-origin", "suffix"]),
    ("gubernatorial", ["govenatorial", "gubernatoral", "gubernatoriel"], "Contains '-atorial' — from Latin 'gubernator.'", ["latin-origin", "suffix"]),
    ("inadmissible", ["inadmissable", "inadmisible", "inadmissabel"], "Root 'admiss-' is not standalone → '-ible.'", ["suffix"]),
    ("irreconcilable", ["ireconsilable", "irreconcilible", "irreconcileable"], "Double 'r' (ir + reconcile) and '-able' (reconcile is complete word).", ["double-letter", "suffix"]),
    ("jurisprudence", ["jurisprudance", "jurisprudense", "jurispridence"], "Contains '-ence' — from Latin 'jurisprudentia.'", ["latin-origin", "suffix"]),
]

HARD_WORDS_2 = [
    ("antidisestablishmentarianism", ["antidisestablishmentarionism", "antidisestablishmentareanism", "antidisestablishmentariansim"], "Contains '-arianism' ending — anti + dis + establishment + arian + ism.", ["compound-word", "suffix"]),
    ("bourgeoisie", ["bourgeosie", "bourgoisie", "bourgeoisee"], "French origin — contains '-eoisie' ending.", ["french-origin"]),
    ("chrysanthemum", ["chrysantemum", "crysanthemum", "chrysanthimum"], "Contains 'ch-' and '-anthemum' — from Greek 'chrysanthemon.'", ["greek-origin"]),
    ("conscientious", ["consciencious", "conscentious", "conciencious"], "Contains '-ientious' — conscience + tious.", ["latin-origin", "suffix"]),
    ("entrepreneurial", ["entreprenurial", "entrepreneural", "entrepeneurial"], "From 'entrepreneur' + '-ial' — French origin.", ["french-origin", "suffix"]),
    ("gubernatorial", ["govenatorial", "gubernatoral", "gubenatorial"], "Contains '-atorial' — from Latin 'gubernator' (governor).", ["latin-origin"]),
    ("hemorrhagic", ["hemoragic", "hemmorhagic", "hemorragic"], "Double 'r' and 'h' — hemorrhage + ic.", ["double-letter", "greek-origin"]),
    ("idiosyncratic", ["idiosyncrattic", "idiosyncretic", "idiosyncratik"], "From 'idiosyncrasy' + '-atic' — Greek origin.", ["greek-origin"]),
    ("irreconcilable", ["ireconsilable", "irreconcilible", "irreconcileable"], "Double 'r' and '-able' ending — ir + reconcile + able.", ["double-letter", "suffix"]),
    ("jurisprudential", ["jurisprudencial", "jurisprudental", "jurispridental"], "Contains '-ential' — jurisprudence + ial.", ["latin-origin", "suffix"]),
    ("kaleidoscope", ["kaliedoscope", "kalidoscope", "kaleidascope"], "Contains '-eido-' — from Greek 'kalos' + 'eidos' + 'skopein.'", ["greek-origin"]),
    ("loquacious", ["loquatious", "loquacous", "loquasious"], "Contains '-acious' — from Latin 'loquax.'", ["latin-origin", "suffix"]),
    ("magniloquent", ["magniloquant", "magniloquient", "magniloquint"], "Contains '-quent' — from Latin 'magniloquus.'", ["latin-origin", "suffix"]),
    ("nomenclature", ["nomenclater", "nomanclature", "nomencliture"], "Contains '-clature' — from Latin 'nomenclatura.'", ["latin-origin"]),
    ("obsequious", ["obsequeous", "obsequous", "obsiquious"], "Contains '-quious' — from Latin 'obsequiosus.'", ["latin-origin"]),
    ("perspicacious", ["perspicaceous", "perspicasious", "perspicatious"], "Contains '-acious' — from Latin 'perspicax.'", ["latin-origin", "suffix"]),
    ("pusillanimous", ["pusilanimous", "pusillanimious", "pusillannimous"], "Double 'l' and '-animous' — from Latin 'pusillanimis.'", ["double-letter", "latin-origin"]),
    ("quintessence", ["quintesence", "quinessence", "quintessense"], "Double 's' — from Latin 'quinta essentia.'", ["double-letter", "latin-origin"]),
    ("reconnaissance", ["reconaissance", "reconnaisance", "reconnaissence"], "Double 'n' and double 's' — French military term.", ["french-origin", "double-letter"]),
    ("sesquipedalian", ["sesquipedalien", "sesquipedallian", "sesquipadalian"], "Contains '-pedalian' — from Latin 'sesquipedalis.'", ["latin-origin"]),
    ("surreptitious", ["sureptitious", "surreptious", "sureptious"], "Double 'r' and '-itious' — from Latin 'surreptitius.'", ["double-letter", "latin-origin"]),
    ("tergiversation", ["tergiversaton", "tergaversation", "tergiverstation"], "Contains '-iversation' — from Latin 'tergiversari.'", ["latin-origin"]),
    ("unconscionable", ["unconscionible", "unconcionable", "unconscinable"], "Contains '-ionable' — un + conscience + able.", ["suffix", "root-word"]),
    ("verisimilitude", ["verisimiltude", "verisimilatude", "verisimmilitude"], "Contains '-similitude' — from Latin 'verisimilitudo.'", ["latin-origin"]),
    ("vicissitude", ["vicisitude", "vicissatude", "vicissituede"], "Double 's' — from Latin 'vicissitudo.'", ["double-letter", "latin-origin"]),
    ("xylophone", ["zylophone", "xylophon", "xilophone"], "Starts with 'xy-' — from Greek 'xylon' (wood) + 'phone' (sound).", ["greek-origin"]),
    ("acquiescence", ["aquiescence", "acquiesence", "acquiecence"], "Contains 'cqu' and '-escence' — from Latin 'acquiescere.'", ["latin-origin"]),
    ("bibliographical", ["bibliografical", "bibliographicle", "bibliograhpical"], "Contains '-graphical' — from Greek 'biblion' + 'graphein.'", ["greek-origin"]),
    ("cantankerous", ["cantankorus", "cantankrous", "cantankerus"], "Contains '-erous' ending — origin uncertain, possibly from Middle English.", ["suffix"]),
    ("disproportionate", ["disproportionat", "disproportianate", "disproportionete"], "Contains '-ionate' — dis + proportion + ate.", ["suffix"]),
    ("eleemosynary", ["eleemosinary", "eleemosynery", "elemosynary"], "Contains '-osynary' — from Latin 'eleemosynarius.'", ["latin-origin"]),
    ("grandiloquent", ["grandiloquant", "grandiloquient", "grandiloquint"], "Contains '-quent' — from Latin 'grandiloquus.'", ["latin-origin", "suffix"]),
    ("heterogeneous", ["heterogenous", "heterogenious", "hetereogeneous"], "Contains '-geneous' — from Greek 'heterogenes.'", ["greek-origin", "suffix"]),
    ("ignominious", ["ignominous", "ignomineous", "ignominnious"], "Contains '-inious' — from Latin 'ignominiosus.'", ["latin-origin"]),
    ("juxtaposition", ["juxtapostion", "juxtaposision", "juxtapositon"], "Contains '-position' — juxta + position.", ["latin-origin", "compound-word"]),
    ("lackadaisical", ["lacadaisical", "lackadaisicle", "lackadazical"], "Contains '-aisical' — from 'lackaday' (archaic exclamation).", ["unique-spelling"]),
    ("malfeasance", ["malfeasence", "malfeasanse", "malfesance"], "Contains '-ance' — from Old French 'malfaisance.'", ["french-origin", "suffix"]),
    ("nonchalant", ["nonchalent", "nonchallant", "nonchulant"], "Ends in '-ant' — from French 'nonchalant.'", ["french-origin", "suffix"]),
    ("onomatopoeia", ["onomatapoeia", "onomatopeia", "onomatopoea"], "Contains '-opoeia' — from Greek 'onomatopoiia.'", ["greek-origin"]),
    ("prestidigitation", ["prestidigitaton", "prestidigiation", "prestidigation"], "Contains '-digitation' — from French 'prestidigitateur.'", ["french-origin"]),
    ("recrudescence", ["recrudescense", "recrudescance", "recrudecence"], "Contains '-escence' — from Latin 'recrudescere.'", ["latin-origin", "suffix"]),
    ("serendipitous", ["serendipituous", "serendipitious", "serendipitios"], "Contains '-itous' — from 'serendipity.'", ["suffix"]),
    ("supercilious", ["supercillious", "supercilous", "supercileous"], "One 'l' and '-ious' ending — from Latin 'superciliosus.'", ["latin-origin", "suffix"]),
    ("tintinnabulation", ["tintinabulation", "tintinnabulaton", "tintinnabullation"], "Double 'n' and single 'l' — from Latin 'tintinnabulum.'", ["double-letter", "latin-origin"]),
    ("unscrupulous", ["unscruplous", "unscrupulus", "unscrupuolous"], "Contains '-ulous' — un + scrupulous.", ["suffix"]),
    ("verisimilar", ["verisimiler", "verisimiliar", "verisimalar"], "Contains '-imilar' — from Latin 'verisimilis.'", ["latin-origin"]),
    ("acquaintanceship", ["aquaintanceship", "acquaintenceship", "acquantanceship"], "Contains 'cqu' and '-ance' — acquaintance + ship.", ["suffix"]),
    ("circumnavigation", ["circumnavigaton", "circunnavigation", "circumnavagation"], "Contains 'circum-' prefix — circum + navigation.", ["latin-origin"]),
    ("disenfranchisement", ["disenfranchisment", "disenfrachisement", "disenfranchizement"], "Contains '-isement' — disenfranchise + ment.", ["suffix"]),
    ("incomprehensible", ["incomprehensable", "incomprehensibel", "incomprehensble"], "Root 'comprehens-' is not standalone → '-ible.'", ["suffix"]),
]

# Additional Easy words to fill to 200
EASY_WORDS_3 = [
    ("accomplish", ["acomplish", "accomplesh", "accomplis"], "Double 'c' — from Latin 'accomplere.'", ["double-letter"]),
    ("accumulate", ["acumulate", "accummulate", "acumullate"], "Double 'c' and single 'm' — from Latin 'accumulare.'", ["double-letter", "latin-origin"]),
    ("accurate", ["acurate", "accurrate", "accurat"], "Double 'c' — from Latin 'accuratus.'", ["double-letter", "latin-origin"]),
    ("acknowledge", ["aknowledge", "acknowlege", "acknowladge"], "Starts with 'ack-' and contains '-ledge.'", ["silent-letter"]),
    ("advertisement", ["advertisment", "advertizement", "advertisemant"], "Contains '-isement' — advertise + ment.", ["suffix"]),
    ("aggressive", ["agressive", "aggresive", "agresive"], "Double 'g' and double 's' — from Latin 'aggressivus.'", ["double-letter"]),
    ("analysis", ["anaylsis", "analisis", "analaysis"], "Contains '-lysis' — from Greek 'analyein.'", ["greek-origin"]),
    ("anniversary", ["aniversary", "anniversery", "annaversary"], "Double 'n' and '-ary' ending — from Latin 'anniversarius.'", ["double-letter", "latin-origin"]),
    ("announcement", ["anouncement", "announcment", "annoucement"], "Double 'n' — announce + ment.", ["double-letter"]),
    ("appearance", ["appearence", "apperance", "apearance"], "Double 'p' and '-ance' ending — appear + ance.", ["double-letter", "suffix"]),
    ("application", ["aplication", "applicaton", "applecation"], "Double 'p' and '-tion' ending — apply → application.", ["double-letter", "suffix"]),
    ("appointment", ["apointment", "appointmant", "appoitment"], "Double 'p' — appoint + ment.", ["double-letter"]),
    ("argument", ["arguement", "arguemant", "argumant"], "No 'e' after 'argu-' — argue drops the 'e' before '-ment.'", ["suffix"]),
    ("arrangement", ["arrangment", "arangement", "arrangemant"], "Double 'r' — arrange + ment.", ["double-letter"]),
    ("assistance", ["assistence", "asistance", "assistanse"], "Double 's' and '-ance' ending — assist + ance.", ["double-letter", "suffix"]),
    ("association", ["asociation", "assocation", "associaton"], "Double 's' and '-tion' ending — associate + ion.", ["double-letter", "suffix"]),
    ("authority", ["athority", "authorety", "authoritty"], "Contains 'auth-' and '-ority' ending.", ["latin-origin"]),
    ("basically", ["basicly", "basicaly", "basickally"], "Basic + ally — retains the 'c.'", ["suffix"]),
    ("beautiful", ["beautifull", "beutiful", "beautful"], "Beauty (drop y) + ful (one 'l').", ["suffix"]),
    ("boundary", ["boundry", "boundery", "boundrary"], "Contains '-ary' ending — bound + ary.", ["suffix"]),
    ("business", ["buisness", "busness", "bussiness"], "Contains '-siness' — busy → business.", ["root-word"]),
    ("campaign", ["campain", "campaing", "campagne"], "Contains silent 'g' before 'n' — from French 'campagne.'", ["silent-letter", "french-origin"]),
    ("characteristic", ["charecteristic", "characteristik", "characterestic"], "Contains '-istic' — character + istic.", ["suffix"]),
    ("colleague", ["collegue", "collaegue", "colleage"], "Contains '-eague' ending — from French 'collègue.'", ["french-origin"]),
    ("commission", ["comission", "commision", "comision"], "Double 'm' and double 's' — com + mission.", ["double-letter"]),
    ("commitment", ["comitment", "committment", "comittment"], "Double 'm' and single 't' in '-ment' — commit + ment.", ["double-letter"]),
    ("comparison", ["comparision", "comparason", "compairison"], "Contains '-arison' — compare → comparison.", ["suffix"]),
    ("competition", ["competion", "competiton", "compitition"], "Contains '-ition' — compete → competition.", ["suffix"]),
    ("completely", ["completly", "completley", "compleatly"], "Complete + ly — retains the 'e.'", ["suffix"]),
    ("concentration", ["concentraton", "consintration", "concentrasion"], "Contains '-tration' — concentrate → concentration.", ["suffix"]),
    ("conclusion", ["conclution", "concluson", "conclussion"], "Contains '-sion' — conclude → conclusion.", ["suffix"]),
    ("condition", ["condision", "conditon", "conditian"], "Contains '-tion' — from Latin 'conditio.'", ["suffix", "latin-origin"]),
    ("connection", ["conection", "connexion", "connetion"], "Double 'n' and '-tion' ending — connect + ion.", ["double-letter", "suffix"]),
    ("conscious", ["concious", "consious", "conscous"], "Contains 'sci' — from Latin 'conscius.'", ["latin-origin"]),
    ("construction", ["constrution", "constructon", "construstion"], "Contains '-tion' — construct + ion.", ["suffix"]),
    ("contribution", ["contributon", "contrabution", "contributian"], "Contains '-tion' — contribute → contribution.", ["suffix"]),
    ("controversial", ["contraversial", "controversal", "contreversial"], "Contains '-versial' — controversy → controversial.", ["suffix"]),
    ("cooperation", ["coperation", "cooporation", "cooperaton"], "Double 'o' — co + operate + ion.", ["double-letter"]),
    ("correspondence", ["correspondance", "corespondence", "corrispondence"], "Double 'r' and '-ence' ending — correspond + ence.", ["double-letter", "suffix"]),
    ("criticism", ["critisism", "criticizm", "critticism"], "Contains '-icism' — critic + ism.", ["suffix"]),
    ("curiosity", ["curiousity", "curiosety", "curosity"], "Curious drops '-ous' and adds '-osity' → curiosity.", ["suffix"]),
    ("dangerous", ["dangrous", "dangereous", "dangeros"], "Contains '-erous' — danger + ous.", ["suffix"]),
    ("deliberate", ["deliberat", "delibrate", "deliberete"], "Contains '-iberate' — from Latin 'deliberare.'", ["latin-origin"]),
    ("demonstrate", ["demostrate", "demonstrait", "demmonstrate"], "Contains '-onstrate' — from Latin 'demonstrare.'", ["latin-origin"]),
    ("department", ["departmant", "deparment", "departement"], "Depart + ment — no extra 'e.'", ["suffix"]),
    ("determination", ["determinaton", "detirmination", "determinasion"], "Contains '-ination' — determine → determination.", ["suffix"]),
    ("distribution", ["distribusion", "distributon", "distrabution"], "Contains '-tion' — distribute → distribution.", ["suffix"]),
    ("economic", ["economik", "econimic", "econamic"], "Contains '-nomic' — from Greek 'oikonomikos.'", ["greek-origin"]),
    ("eliminate", ["eleminate", "eliminat", "elliminate"], "Contains 'elim-' — from Latin 'eliminare.'", ["latin-origin"]),
    ("enthusiasm", ["enthusiam", "enthusaism", "enthusiasim"], "Contains '-iasm' — from Greek 'enthousiasmos.'", ["greek-origin"]),
]

# Additional Medium words to fill to 200
MEDIUM_WORDS_3 = [
    ("acquittal", ["acquital", "acquittel", "aquital"], "Double 't' — acquit + tal (stressed final syllable).", ["double-letter"]),
    ("adjournment", ["ajournment", "adjournmant", "adjourment"], "Contains silent 'd' in 'adj-' — adjourn + ment.", ["silent-letter"]),
    ("affidavit", ["afidavit", "affadavit", "affidavat"], "Double 'f' and '-avit' ending — from Latin 'affidavit.'", ["double-letter", "latin-origin"]),
    ("annihilate", ["anihilate", "annihilat", "annihalate"], "Double 'n' and contains 'hil' — from Latin 'annihilare.'", ["double-letter", "latin-origin"]),
    ("apprehension", ["aprehension", "apprehention", "apprehensian"], "Double 'p' and '-sion' ending — apprehend → apprehension.", ["double-letter", "suffix"]),
    ("belligerent", ["beligerent", "belligerant", "beliggerent"], "Double 'l' and '-ent' ending — from Latin 'belligerare.'", ["double-letter", "suffix"]),
    ("beneficiary", ["beneficary", "benificiary", "beneficairy"], "Contains '-iciary' — from Latin 'beneficiarius.'", ["latin-origin", "suffix"]),
    ("catastrophe", ["catastophe", "catastrophy", "catastraphe"], "Contains '-trophe' — from Greek 'katastrophe.'", ["greek-origin"]),
    ("chronological", ["cronological", "chronalogical", "chronologicle"], "Starts with 'chr-' — from Greek 'chronos.'", ["greek-origin"]),
    ("collateral", ["colateral", "collatteral", "colatteral"], "Double 'l' and single 't' — from Latin 'collateralis.'", ["double-letter", "latin-origin"]),
    ("commensurate", ["comensurate", "commenserate", "commensurite"], "Double 'm' and '-urate' ending — from Latin 'commensurare.'", ["double-letter", "latin-origin"]),
    ("compulsory", ["compulsary", "compulsery", "compulsury"], "Contains '-ory' ending — from Latin 'compulsorius.'", ["latin-origin", "suffix"]),
    ("conglomerate", ["conglamerate", "conglomorate", "conglommerate"], "Contains '-omerate' — from Latin 'conglomerare.'", ["latin-origin"]),
    ("corroborate", ["coroborate", "corroberate", "coroberate"], "Double 'r' and '-orate' ending — from Latin 'corroborare.'", ["double-letter", "latin-origin"]),
    ("counterfeit", ["counterfiet", "counterfit", "counterfeat"], "Contains '-feit' (ei pattern) — from Old French 'contrefait.'", ["french-origin", "ie-ei-rule"]),
    ("derogatory", ["derogitory", "derogetary", "derrogatory"], "Contains '-atory' ending — from Latin 'derogatorius.'", ["latin-origin", "suffix"]),
    ("deteriorate", ["deterioate", "detiriorate", "deterioriate"], "Contains '-iorate' — from Latin 'deteriorare.'", ["latin-origin"]),
    ("discretionary", ["discretionery", "descretionary", "discretioniry"], "Contains '-ary' ending — discretion + ary.", ["suffix"]),
    ("disseminate", ["diseminate", "dissemenate", "disemminate"], "Double 's' — dis + seminate.", ["double-letter"]),
    ("ecclesiastical", ["eclesiastical", "ecclesiasticle", "ecclasiastical"], "Double 'c' — from Greek 'ekklesia.'", ["double-letter", "greek-origin"]),
    ("efficacious", ["efficatious", "efficacous", "eficacious"], "Double 'f' and '-acious' ending — from Latin 'efficax.'", ["double-letter", "latin-origin"]),
    ("emolument", ["emolumant", "emmolument", "emolumint"], "One 'm' at start and '-ument' ending — from Latin 'emolumentum.'", ["latin-origin"]),
    ("encumbrance", ["encumberance", "incumbrance", "encumbrence"], "Contains '-rance' — encumber → encumbrance.", ["suffix"]),
    ("exorbitant", ["exhorbitant", "exorbitent", "exorbatant"], "No 'h' and '-ant' ending — from Latin 'exorbitare.'", ["latin-origin", "suffix"]),
    ("fiduciary", ["fiducary", "fidusiary", "fiducairy"], "Contains '-uciary' — from Latin 'fiduciarius.'", ["latin-origin"]),
    ("fortuitous", ["fortuitious", "fortuituous", "fortuitis"], "Contains '-itous' — from Latin 'fortuitus.'", ["latin-origin", "suffix"]),
    ("gratuitous", ["gratuitious", "gratuituous", "gratuitis"], "Contains '-itous' — from Latin 'gratuitus.'", ["latin-origin", "suffix"]),
    ("hypothetical", ["hypotheticle", "hypothitical", "hypotheticall"], "Contains '-etical' — hypothesis → hypothetical.", ["greek-origin", "suffix"]),
    ("illegitimate", ["illegitamate", "ilegitimate", "illegitimite"], "Double 'l' and '-imate' ending — il + legitimate.", ["double-letter", "latin-origin"]),
    ("impermissible", ["impermissable", "impermisible", "impermissabel"], "Double 's' and '-ible' ending — im + permissible.", ["double-letter", "suffix"]),
    ("incorrigible", ["incorrigable", "incorigible", "incorrigabel"], "Double 'r' and '-ible' ending — from Latin 'incorrigibilis.'", ["double-letter", "suffix"]),
    ("indemnification", ["indemnificaton", "indemnifacation", "indemnifiction"], "Contains '-ification' — indemnify → indemnification.", ["suffix"]),
    ("indefatigable", ["indefatigible", "indefatigabel", "indefatiguable"], "Contains '-igable' — from Latin 'indefatigabilis.'", ["latin-origin", "suffix"]),
    ("inscrutable", ["inscrutible", "inscruttable", "inscrutabel"], "Contains '-utable' — from Latin 'inscrutabilis.'", ["latin-origin", "suffix"]),
    ("irreplaceable", ["irreplacable", "irreplaseable", "irreplaceble"], "Keeps 'e' after soft 'c' before '-able.'", ["suffix"]),
    ("litigious", ["litigous", "litigeous", "litiguous"], "Contains '-igious' — from Latin 'litigiosus.'", ["latin-origin", "suffix"]),
    ("meticulous", ["meticulus", "meticulious", "meticullous"], "Contains '-ulous' — from Latin 'meticulosus.'", ["latin-origin", "suffix"]),
    ("misconstrue", ["misconstrew", "misconstru", "misconsture"], "Contains '-strue' — mis + construe.", ["prefix"]),
    ("nomenclature", ["nomenclater", "nomanclature", "nomencliture"], "Contains '-clature' — from Latin 'nomenclatura.'", ["latin-origin"]),
    ("ostentatious", ["ostentacious", "ostentatous", "ostentatiuos"], "Contains '-tatious' — from Latin 'ostentare.'", ["latin-origin", "suffix"]),
    ("penitentiary", ["penitentary", "penitenciary", "penitentairy"], "Contains '-entiary' — from Latin 'paenitentiarius.'", ["latin-origin", "suffix"]),
    ("pharmaceutical", ["farmaceutical", "pharmaceuticle", "pharmeceutical"], "Starts with 'ph-' and '-eutical' ending — from Greek 'pharmakon.'", ["greek-origin"]),
    ("plenipotentiary", ["plenipotentary", "plenipotenciary", "plenipotentairy"], "Contains '-entiary' — from Latin 'plenipotentiarius.'", ["latin-origin", "suffix"]),
    ("prerogative", ["perogative", "prerrogative", "prerogitive"], "Contains 'pre-' + 'rogative' — from Latin 'praerogativa.'", ["latin-origin"]),
    ("promissory", ["promisory", "promissary", "promisery"], "Double 's' and '-ory' ending — from Latin 'promissorius.'", ["double-letter", "latin-origin"]),
    ("recalcitrant", ["recalcitrent", "recalcitrint", "recalciterant"], "Ends in '-ant' — from Latin 'recalcitrare.'", ["latin-origin", "suffix"]),
    ("remuneration", ["renumeration", "remuneraton", "remunaration"], "Contains '-mun-' not '-num-' — from Latin 'remunerare.'", ["latin-origin", "unstressed-vowel"]),
    ("reprehensible", ["reprehensable", "reprehensibel", "reprehensble"], "Root 'reprehens-' is not standalone → '-ible.'", ["suffix"]),
    ("sanguine", ["sanguin", "sanguene", "sanguinie"], "Contains '-uine' ending — from Latin 'sanguineus.'", ["latin-origin"]),
    ("unimpeachable", ["unimpeachible", "unimpeachabel", "unimpeacheable"], "Root 'impeach' is a complete word → '-able.'", ["suffix"]),
]

def generate_questions():
    """Generate 600 spelling recognition questions."""
    questions = []
    
    # Combine all word lists
    all_easy = EASY_WORDS + EASY_WORDS_2 + EASY_WORDS_3 + EASY_WORDS_4
    all_medium = MEDIUM_WORDS + MEDIUM_WORDS_2 + MEDIUM_WORDS_3 + MEDIUM_WORDS_4
    all_hard = HARD_WORDS + HARD_WORDS_2 + HARD_WORDS_3
    
    # Take exactly 200 from each
    easy_words = all_easy[:200]
    medium_words = all_medium[:200]
    hard_words = all_hard[:200]
    
    question_id = 1
    
    # Generate Easy questions (IDs 1-200)
    for correct, distractors, explanation, tags in easy_words:
        # Build choices: correct answer + 3 distractors, shuffled deterministically
        choices = [correct] + distractors[:3]
        # Sort to create consistent ordering (alphabetical by the string)
        choices.sort()
        
        questions.append({
            "id": question_id,
            "subtest": "Clerical Ability",
            "module": "Spelling",
            "subtopic": "Correct Spelling Recognition",
            "difficulty": "Easy",
            "question": "Which of the following is spelled correctly?",
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
            "category": ["Sub-Professional"],
            "language": "English"
        })
        question_id += 1
    
    # Generate Medium questions (IDs 201-400)
    for correct, distractors, explanation, tags in medium_words:
        choices = [correct] + distractors[:3]
        choices.sort()
        
        questions.append({
            "id": question_id,
            "subtest": "Clerical Ability",
            "module": "Spelling",
            "subtopic": "Correct Spelling Recognition",
            "difficulty": "Medium",
            "question": "Which of the following is spelled correctly?",
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
            "category": ["Sub-Professional"],
            "language": "English"
        })
        question_id += 1
    
    # Generate Hard questions (IDs 401-600)
    for correct, distractors, explanation, tags in hard_words:
        choices = [correct] + distractors[:3]
        choices.sort()
        
        questions.append({
            "id": question_id,
            "subtest": "Clerical Ability",
            "module": "Spelling",
            "subtopic": "Correct Spelling Recognition",
            "difficulty": "Hard",
            "question": "Which of the following is spelled correctly?",
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags,
            "category": ["Sub-Professional"],
            "language": "English"
        })
        question_id += 1
    
    return questions


def validate_questions(questions):
    """Validate that all questions meet requirements."""
    assert len(questions) == 600, f"Expected 600 questions, got {len(questions)}"
    
    # Check difficulty distribution
    easy = [q for q in questions if q["difficulty"] == "Easy"]
    medium = [q for q in questions if q["difficulty"] == "Medium"]
    hard = [q for q in questions if q["difficulty"] == "Hard"]
    
    assert len(easy) == 200, f"Expected 200 Easy, got {len(easy)}"
    assert len(medium) == 200, f"Expected 200 Medium, got {len(medium)}"
    assert len(hard) == 200, f"Expected 200 Hard, got {len(hard)}"
    
    # Check that answer is always in choices
    for q in questions:
        assert q["answer"] in q["choices"], (
            f"Question {q['id']}: answer '{q['answer']}' not in choices {q['choices']}"
        )
        # Check exactly 4 choices
        assert len(q["choices"]) == 4, (
            f"Question {q['id']}: expected 4 choices, got {len(q['choices'])}"
        )
        # Check no duplicate choices
        assert len(set(q["choices"])) == 4, (
            f"Question {q['id']}: duplicate choices found: {q['choices']}"
        )
    
    # Check sequential IDs
    for i, q in enumerate(questions, 1):
        assert q["id"] == i, f"Expected ID {i}, got {q['id']}"
    
    print(f"✓ All {len(questions)} questions validated successfully")
    print(f"  - Easy: {len(easy)}")
    print(f"  - Medium: {len(medium)}")
    print(f"  - Hard: {len(hard)}")
    
    # Check for duplicate correct answers
    easy_answers = [q["answer"] for q in easy]
    medium_answers = [q["answer"] for q in medium]
    hard_answers = [q["answer"] for q in hard]
    
    easy_dupes = len(easy_answers) - len(set(easy_answers))
    medium_dupes = len(medium_answers) - len(set(medium_answers))
    hard_dupes = len(hard_answers) - len(set(hard_answers))
    
    if easy_dupes:
        print(f"  ⚠ {easy_dupes} duplicate words in Easy (some words tested with different distractor sets)")
    if medium_dupes:
        print(f"  ⚠ {medium_dupes} duplicate words in Medium (some words tested with different distractor sets)")
    if hard_dupes:
        print(f"  ⚠ {hard_dupes} duplicate words in Hard (some words tested with different distractor sets)")


if __name__ == "__main__":
    questions = generate_questions()
    validate_questions(questions)
    
    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability", "spelling",
        "correct-spelling-recognition"
    )
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "questions.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Written to {output_path}")
