"""
Generate 600 language, meaning, and context relationship analogy questions.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/analytical-ability/word-analogy/language-meaning-and-context-relationships/questions.json
"""
import json
import random
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "seed" / "questions" / "analytical-ability" / "word-analogy" / "language-meaning-and-context-relationships" / "questions.json"

B = {
    "subtest": "Analytical Ability",
    "module": "Word Analogy",
    "subtopic": "Language, Meaning, and Context Relationships",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}

# ---------------------------------------------------------------------------
# QUESTION BANKS BY TYPE AND DIFFICULTY
# Each entry: (question, choices, answer, explanation, tags)
# ---------------------------------------------------------------------------

EASY_QUESTIONS = [
    # --- Word-and-Definition (formal : common) ---
    ("PHYSICIAN : DOCTOR :: ATTORNEY : ?", ["Judge","Lawyer","Court","Legal"], "Lawyer",
     "Physician is the formal term for doctor. Attorney is the formal term for lawyer.",
     ["word analogy","definition","formal-common"]),
    ("COMMENCE : BEGIN :: TERMINATE : ?", ["Start","End","Continue","Pause"], "End",
     "Commence means begin. Terminate means end. Both are formal-to-common pairs.",
     ["word analogy","definition","formal-common"]),
    ("ENORMOUS : VERY LARGE :: TINY : ?", ["Big","Very small","Medium","Narrow"], "Very small",
     "Enormous is defined as very large. Tiny is defined as very small.",
     ["word analogy","definition","vocabulary"]),
    ("FRAGILE : EASILY BROKEN :: DURABLE : ?", ["Soft","Long-lasting","Heavy","Expensive"], "Long-lasting",
     "Fragile means easily broken. Durable means long-lasting.",
     ["word analogy","definition","vocabulary"]),
    ("NOVICE : BEGINNER :: EXPERT : ?", ["Teacher","Master","Worker","Student"], "Master",
     "A novice is a beginner. An expert is a master.",
     ["word analogy","definition","vocabulary"]),
    ("DILIGENT : HARDWORKING :: LAZY : ?", ["Idle","Slow","Tired","Weak"], "Idle",
     "Diligent means hardworking. Lazy means idle.",
     ["word analogy","definition","vocabulary"]),
    ("ABUNDANT : PLENTIFUL :: SCARCE : ?", ["Rare","Small","Empty","Lost"], "Rare",
     "Abundant means plentiful. Scarce means rare.",
     ["word analogy","definition","vocabulary"]),
    ("BRIEF : SHORT :: LENGTHY : ?", ["Tall","Long","Big","Wide"], "Long",
     "Brief means short (in duration). Lengthy means long (in duration).",
     ["word analogy","definition","vocabulary"]),
    ("RAPID : VERY FAST :: SLUGGISH : ?", ["Tired","Very slow","Weak","Heavy"], "Very slow",
     "Rapid is defined as very fast. Sluggish is defined as very slow.",
     ["word analogy","definition","vocabulary"]),
    ("ASSIST : HELP :: PROHIBIT : ?", ["Allow","Forbid","Stop","Block"], "Forbid",
     "Assist means help. Prohibit means forbid.",
     ["word analogy","definition","formal-common"]),
    ("PURCHASE : BUY :: SELL : ?", ["Trade","Vend","Give","Offer"], "Vend",
     "Purchase is the formal term for buy. Vend is the formal term for sell.",
     ["word analogy","definition","formal-common"]),
    ("RESIDENCE : HOME :: VEHICLE : ?", ["Car","Road","Travel","Drive"], "Car",
     "Residence is the formal term for home. Vehicle is the formal term for car.",
     ["word analogy","definition","formal-common"]),
    ("INFANT : BABY :: ADOLESCENT : ?", ["Child","Teenager","Adult","Youth"], "Teenager",
     "Infant is the formal term for baby. Adolescent is the formal term for teenager.",
     ["word analogy","definition","formal-common"]),
    ("BEVERAGE : DRINK :: CUISINE : ?", ["Food","Cook","Kitchen","Taste"], "Food",
     "Beverage is the formal term for drink. Cuisine is the formal term for food.",
     ["word analogy","definition","formal-common"]),
    ("ANNUAL : YEARLY :: DAILY : ?", ["Monthly","Every day","Weekly","Hourly"], "Every day",
     "Annual means yearly. Daily means every day.",
     ["word analogy","definition","vocabulary"]),
    # --- Context-Based Meaning (physical to abstract) ---
    ("COLD : UNFRIENDLY :: WARM : ?", ["Hot","Friendly","Cozy","Heated"], "Friendly",
     "Cold in personality context means unfriendly. Warm in personality context means friendly.",
     ["word analogy","context","meaning-shift"]),
    ("BRIGHT : INTELLIGENT :: DULL : ?", ["Dark","Stupid","Boring","Dim"], "Stupid",
     "Bright in cognitive context means intelligent. Dull in cognitive context means stupid/slow-witted.",
     ["word analogy","context","meaning-shift"]),
    ("SHARP : CLEVER :: BLUNT : ?", ["Dull","Direct","Rude","Flat"], "Direct",
     "Sharp in communication means clever/witty. Blunt in communication means direct/straightforward.",
     ["word analogy","context","meaning-shift"]),
    ("HARD : DIFFICULT :: EASY : ?", ["Soft","Simple","Light","Smooth"], "Simple",
     "Hard in task context means difficult. Easy in task context means simple.",
     ["word analogy","context","meaning-shift"]),
    ("DEEP : PROFOUND :: SHALLOW : ?", ["Thin","Superficial","Empty","Low"], "Superficial",
     "Deep in intellectual context means profound. Shallow in intellectual context means superficial.",
     ["word analogy","context","meaning-shift"]),
    ("LIGHT : NOT HEAVY :: DARK : ?", ["Heavy","Not light","Sad","Black"], "Heavy",
     "Light means not heavy (weight context). Dark here parallels as heavy (the opposite in weight).",
     ["word analogy","context","meaning-shift"]),
    ("SWEET : KIND :: BITTER : ?", ["Sour","Resentful","Angry","Sad"], "Resentful",
     "Sweet in personality context means kind. Bitter in personality context means resentful.",
     ["word analogy","context","meaning-shift"]),
    ("SMOOTH : EASY :: ROUGH : ?", ["Hard","Difficult","Bumpy","Tough"], "Difficult",
     "Smooth in experience context means easy/without problems. Rough in experience context means difficult.",
     ["word analogy","context","meaning-shift"]),
    ("COOL : CALM :: HOT : ?", ["Warm","Angry","Fast","Loud"], "Angry",
     "Cool in temperament context means calm. Hot in temperament context means angry.",
     ["word analogy","context","meaning-shift"]),
    ("SOFT : GENTLE :: HARD : ?", ["Strong","Harsh","Loud","Firm"], "Harsh",
     "Soft in manner context means gentle. Hard in manner context means harsh.",
     ["word analogy","context","meaning-shift"]),
    # --- Vocabulary Association (word : domain) ---
    ("DOCTOR : HOSPITAL :: TEACHER : ?", ["School","Book","Student","Chalk"], "School",
     "A doctor works in a hospital. A teacher works in a school.",
     ["word analogy","association","professional-workplace"]),
    ("CHEF : KITCHEN :: PILOT : ?", ["Cockpit","Sky","Plane","Airport"], "Cockpit",
     "A chef works in a kitchen. A pilot works in a cockpit.",
     ["word analogy","association","professional-workplace"]),
    ("JUDGE : COURTROOM :: SURGEON : ?", ["Hospital","Operating room","Clinic","Ward"], "Operating room",
     "A judge works in a courtroom. A surgeon works in an operating room.",
     ["word analogy","association","professional-workplace"]),
    ("PEN : WRITING :: HAMMER : ?", ["Nail","Building","Carpentry","Tool"], "Carpentry",
     "A pen is a tool used in writing. A hammer is a tool used in carpentry.",
     ["word analogy","association","tool-field"]),
    ("STETHOSCOPE : MEDICINE :: TELESCOPE : ?", ["Stars","Astronomy","Space","Sky"], "Astronomy",
     "A stethoscope is an instrument used in medicine. A telescope is an instrument used in astronomy.",
     ["word analogy","association","tool-field"]),
    ("BUDGET : FINANCE :: RECIPE : ?", ["Food","Cooking","Kitchen","Chef"], "Cooking",
     "A budget is a plan used in finance. A recipe is a plan used in cooking.",
     ["word analogy","association","concept-field"]),
    ("THERMOMETER : TEMPERATURE :: SCALE : ?", ["Fish","Weight","Balance","Heavy"], "Weight",
     "A thermometer measures temperature. A scale measures weight.",
     ["word analogy","association","tool-measurement"]),
    ("NURSE : HOSPITAL :: LIBRARIAN : ?", ["Library","Books","Reading","Shelf"], "Library",
     "A nurse works in a hospital. A librarian works in a library.",
     ["word analogy","association","professional-workplace"]),
    ("FARMER : FIELD :: MINER : ?", ["Mine","Rock","Gold","Mountain"], "Mine",
     "A farmer works in a field. A miner works in a mine.",
     ["word analogy","association","professional-workplace"]),
    ("PAINTBRUSH : ART :: CALCULATOR : ?", ["Numbers","Mathematics","Office","Computer"], "Mathematics",
     "A paintbrush is a tool used in art. A calculator is a tool used in mathematics.",
     ["word analogy","association","tool-field"]),
    # --- Multiple-Meaning Words ---
    ("BARK : TREE COVERING :: BAT : ?", ["Ball","Flying mammal","Hit","Sport"], "Flying mammal",
     "Bark's secondary meaning is tree covering (not dog sound). Bat's secondary meaning is flying mammal (not sports equipment).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("PEN : ANIMAL ENCLOSURE :: RING : ?", ["Jewelry","Boxing arena","Circle","Gold"], "Boxing arena",
     "Pen's secondary meaning is animal enclosure. Ring's secondary meaning is boxing arena.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("LIGHT : NOT HEAVY :: FAIR : ?", ["Beautiful","Just","Blonde","Carnival"], "Just",
     "Light can mean not heavy (not illumination). Fair can mean just/equitable (not carnival or blonde).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("BANK : RIVER EDGE :: TRUNK : ?", ["Elephant nose","Car storage","Tree","Suitcase"], "Tree",
     "Bank's secondary meaning is river edge. Trunk's secondary meaning is tree trunk (main stem).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("SPRING : WATER SOURCE :: FALL : ?", ["Autumn","Drop","Trip","Decline"], "Autumn",
     "Spring can mean a water source (not season). Fall can mean autumn (not dropping).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("WAVE : HAND GESTURE :: NOD : ?", ["Head movement","Sleep","Agreement","Bow"], "Head movement",
     "Wave as a gesture means hand movement. Nod as a gesture means head movement.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("MATCH : CONTEST :: SUIT : ?", ["Clothing","Legal case","Cards","Fit"], "Legal case",
     "Match can mean a contest/game. Suit can mean a legal case.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("SEAL : OCEAN ANIMAL :: CRANE : ?", ["Bird","Machine","Lift","Neck"], "Bird",
     "Seal's secondary meaning is an ocean animal (not a closure). Crane's secondary meaning is a bird (not construction equipment).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("NAIL : FINGER COVERING :: PUPIL : ?", ["Student","Eye part","School","Teacher"], "Eye part",
     "Nail's secondary meaning is finger/toe covering. Pupil's secondary meaning is the eye part.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("PITCHER : CONTAINER :: SPEAKER : ?", ["Audio device","Person talking","Microphone","Sound"], "Audio device",
     "Pitcher can mean a container for liquid (not baseball player). Speaker can mean an audio device (not a person talking).",
     ["word analogy","multiple-meaning","polysemy"]),
    # --- More Definition pairs ---
    ("COURAGEOUS : BRAVE :: TIMID : ?", ["Shy","Weak","Small","Quiet"], "Shy",
     "Courageous means brave. Timid means shy.",
     ["word analogy","definition","vocabulary"]),
    ("WEALTHY : RICH :: IMPOVERISHED : ?", ["Sad","Poor","Sick","Alone"], "Poor",
     "Wealthy means rich. Impoverished means poor.",
     ["word analogy","definition","vocabulary"]),
    ("ANCIENT : VERY OLD :: MODERN : ?", ["New","Very new","Current","Fast"], "Very new",
     "Ancient is defined as very old. Modern is defined as very new/current.",
     ["word analogy","definition","vocabulary"]),
    ("TRANSPARENT : SEE-THROUGH :: OPAQUE : ?", ["Dark","Not see-through","Thick","Heavy"], "Not see-through",
     "Transparent means see-through. Opaque means not see-through.",
     ["word analogy","definition","vocabulary"]),
    ("MANDATORY : REQUIRED :: OPTIONAL : ?", ["Free","Not required","Easy","Extra"], "Not required",
     "Mandatory means required. Optional means not required.",
     ["word analogy","definition","vocabulary"]),
    # --- More Context pairs ---
    ("FLAT : MONOTONE :: SHARP : ?", ["Pointed","High-pitched","Clever","Painful"], "High-pitched",
     "Flat in music context means monotone/below pitch. Sharp in music context means high-pitched/above pitch.",
     ["word analogy","context","meaning-shift"]),
    ("GREEN : INEXPERIENCED :: SEASONED : ?", ["Salty","Experienced","Old","Cooked"], "Experienced",
     "Green in skill context means inexperienced. Seasoned in skill context means experienced.",
     ["word analogy","context","meaning-shift"]),
    ("BLUE : SAD :: ROSY : ?", ["Pink","Optimistic","Healthy","Red"], "Optimistic",
     "Blue in mood context means sad. Rosy in mood context means optimistic.",
     ["word analogy","context","meaning-shift"]),
    ("HEAVY : SERIOUS :: LIGHT : ?", ["Not serious","Bright","Thin","Easy"], "Not serious",
     "Heavy in topic context means serious. Light in topic context means not serious/casual.",
     ["word analogy","context","meaning-shift"]),
    ("DARK : GLOOMY :: SUNNY : ?", ["Hot","Cheerful","Bright","Yellow"], "Cheerful",
     "Dark in mood context means gloomy. Sunny in mood context means cheerful.",
     ["word analogy","context","meaning-shift"]),
    # --- More Association pairs ---
    ("MICROSCOPE : LABORATORY :: COMPASS : ?", ["Direction","Navigation","Ship","Map"], "Navigation",
     "A microscope is used in a laboratory. A compass is used in navigation.",
     ["word analogy","association","tool-field"]),
    ("REFEREE : SPORTS :: UMPIRE : ?", ["Baseball","Cricket","Game","Field"], "Baseball",
     "A referee officiates in sports generally. An umpire officiates in baseball specifically.",
     ["word analogy","association","professional-field"]),
    ("BALLOT : ELECTION :: TICKET : ?", ["Travel","Movie","Bus","Entry"], "Travel",
     "A ballot is used in an election. A ticket is used in travel.",
     ["word analogy","association","document-activity"]),
    ("PRESCRIPTION : PHARMACY :: RECIPE : ?", ["Kitchen","Restaurant","Chef","Cooking"], "Kitchen",
     "A prescription is fulfilled at a pharmacy. A recipe is followed in a kitchen.",
     ["word analogy","association","document-setting"]),
    ("DIPLOMA : GRADUATION :: CERTIFICATE : ?", ["Training","Paper","School","Frame"], "Training",
     "A diploma is awarded at graduation. A certificate is awarded after training.",
     ["word analogy","association","document-event"]),
    # --- More Multiple-Meaning ---
    ("CURRENT : PRESENT TIME :: VOLUME : ?", ["Book","Loudness","Space","Amount"], "Loudness",
     "Current can mean present time (not water/electrical flow). Volume can mean loudness (not book or space).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("SENTENCE : GRAMMAR UNIT :: CASE : ?", ["Container","Legal matter","Example","Situation"], "Container",
     "Sentence's primary meaning is a grammar unit. Case's primary meaning is a container.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("DEGREE : TEMPERATURE UNIT :: YARD : ?", ["Garden","Measurement unit","Grass","Fence"], "Measurement unit",
     "Degree can mean a temperature unit. Yard can mean a measurement unit (3 feet).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("ORGAN : BODY PART :: CELL : ?", ["Prison room","Phone","Biology unit","Battery"], "Prison room",
     "Organ's primary meaning is a body part. Cell's secondary meaning is a prison room.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("PLOT : STORY PLAN :: DRAFT : ?", ["Air current","Sketch","Beer","Military selection"], "Air current",
     "Plot can mean a story plan (not land). Draft can mean an air current (not document version).",
     ["word analogy","multiple-meaning","polysemy"]),
    # --- Additional Easy Definition ---
    ("VACANT : EMPTY :: OCCUPIED : ?", ["Busy","Full","Taken","Working"], "Full",
     "Vacant means empty. Occupied means full/in use.",
     ["word analogy","definition","vocabulary"]),
    ("CONCEAL : HIDE :: REVEAL : ?", ["Show","Find","Open","See"], "Show",
     "Conceal means hide. Reveal means show.",
     ["word analogy","definition","vocabulary"]),
    ("PERMIT : ALLOW :: FORBID : ?", ["Stop","Prevent","Deny","Prohibit"], "Prohibit",
     "Permit means allow. Forbid means prohibit.",
     ["word analogy","definition","vocabulary"]),
    ("GENUINE : REAL :: COUNTERFEIT : ?", ["Fake","Cheap","Bad","Wrong"], "Fake",
     "Genuine means real. Counterfeit means fake.",
     ["word analogy","definition","vocabulary"]),
    ("SUMMIT : TOP :: BASE : ?", ["Bottom","Foundation","Ground","Floor"], "Bottom",
     "Summit means top. Base means bottom.",
     ["word analogy","definition","vocabulary"]),
    ("EXTERIOR : OUTSIDE :: INTERIOR : ?", ["Inside","Middle","Center","Core"], "Inside",
     "Exterior means outside. Interior means inside.",
     ["word analogy","definition","vocabulary"]),
    ("INITIAL : FIRST :: FINAL : ?", ["End","Last","Finish","Done"], "Last",
     "Initial means first. Final means last.",
     ["word analogy","definition","vocabulary"]),
    ("MAXIMUM : MOST :: MINIMUM : ?", ["Least","Smallest","Lowest","None"], "Least",
     "Maximum means the most. Minimum means the least.",
     ["word analogy","definition","vocabulary"]),
    ("FREQUENT : OFTEN :: RARE : ?", ["Never","Seldom","Once","Few"], "Seldom",
     "Frequent means often. Rare means seldom.",
     ["word analogy","definition","vocabulary"]),
    ("DOMESTIC : LOCAL :: FOREIGN : ?", ["Far","International","Outside","Away"], "International",
     "Domestic means local/within the country. Foreign means international/from another country.",
     ["word analogy","definition","vocabulary"]),
    # --- Additional Easy Context ---
    ("BRIGHT : VIVID :: PALE : ?", ["Faint","White","Sick","Light"], "Faint",
     "Bright in color context means vivid. Pale in color context means faint.",
     ["word analogy","context","meaning-shift"]),
    ("FIRM : DETERMINED :: SOFT : ?", ["Weak","Yielding","Quiet","Gentle"], "Yielding",
     "Firm in character context means determined. Soft in character context means yielding/easily persuaded.",
     ["word analogy","context","meaning-shift"]),
    ("RICH : FULL OF FLAVOR :: PLAIN : ?", ["Simple","Boring","Ugly","Empty"], "Simple",
     "Rich in food context means full of flavor. Plain in food context means simple/unflavored.",
     ["word analogy","context","meaning-shift"]),
    ("SHARP : SUDDEN :: GRADUAL : ?", ["Slow","Gentle","Smooth","Soft"], "Slow",
     "Sharp in change context means sudden. Gradual in change context means slow.",
     ["word analogy","context","meaning-shift"]),
    ("TIGHT : STRICT :: LOOSE : ?", ["Free","Relaxed","Open","Wide"], "Relaxed",
     "Tight in rules context means strict. Loose in rules context means relaxed/lenient.",
     ["word analogy","context","meaning-shift"]),
    # --- Additional Easy Association ---
    ("ERASER : CORRECTION :: RULER : ?", ["King","Measurement","Line","Straight"], "Measurement",
     "An eraser is a tool for correction. A ruler is a tool for measurement.",
     ["word analogy","association","tool-function"]),
    ("ANCHOR : SHIP :: BRAKE : ?", ["Car","Stop","Wheel","Speed"], "Car",
     "An anchor stops a ship. A brake stops a car.",
     ["word analogy","association","tool-vehicle"]),
    ("MAP : GEOGRAPHY :: CHART : ?", ["Music","Data","Statistics","Graph"], "Statistics",
     "A map is a visual tool in geography. A chart is a visual tool in statistics.",
     ["word analogy","association","tool-field"]),
    ("UNIFORM : SOLDIER :: ROBE : ?", ["Judge","Bed","Cloth","Dress"], "Judge",
     "A uniform is worn by a soldier. A robe is worn by a judge.",
     ["word analogy","association","clothing-profession"]),
    ("WHISTLE : REFEREE :: BATON : ?", ["Conductor","Police","Runner","Stick"], "Conductor",
     "A whistle is used by a referee. A baton is used by a conductor.",
     ["word analogy","association","tool-profession"]),
    # --- Additional Easy Multiple-Meaning ---
    ("ROCK : MUSIC GENRE :: COUNTRY : ?", ["Nation","Music genre","Rural","Land"], "Music genre",
     "Rock can mean a music genre (not a stone). Country can mean a music genre (not a nation).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("MOUSE : COMPUTER DEVICE :: MONITOR : ?", ["Screen","Watch","Guard","Display"], "Screen",
     "Mouse can mean a computer device (not animal). Monitor can mean a screen (not a person who watches).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("JAM : TRAFFIC CONGESTION :: BLOCK : ?", ["Toy","Mental obstacle","Square","Building"], "Mental obstacle",
     "Jam can mean traffic congestion. Block can mean a mental obstacle (writer's block).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("STAR : CELEBRITY :: FAN : ?", ["Admirer","Cool air","Blade","Wind"], "Admirer",
     "Star can mean a celebrity (not celestial body). Fan can mean an admirer (not cooling device).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("PLANT : FACTORY :: YARD : ?", ["Garden","Measurement","Grass","Fence"], "Garden",
     "Plant can mean a factory (not vegetation). Yard can mean a garden area (not measurement).",
     ["word analogy","multiple-meaning","polysemy"]),
]

MEDIUM_QUESTIONS = [
    # --- Word-and-Definition (formal/technical : meaning) ---
    ("REMUNERATION : PAYMENT :: DOMICILE : ?", ["Building","Residence","Address","Location"], "Residence",
     "Remuneration is the formal term for payment. Domicile is the formal term for residence/home.",
     ["word analogy","definition","formal-common"]),
    ("PEDAGOGUE : TEACHER :: PHILANTHROPIST : ?", ["Rich person","Charitable giver","Volunteer","Helper"], "Charitable giver",
     "A pedagogue is defined as a teacher. A philanthropist is defined as a charitable giver.",
     ["word analogy","definition","vocabulary"]),
    ("JURISPRUDENCE : STUDY OF LAW :: PEDAGOGY : ?", ["Teaching method","School","Children","Learning"], "Teaching method",
     "Jurisprudence is the study of law. Pedagogy is the study/method of teaching.",
     ["word analogy","definition","academic"]),
    ("MANDATE : OFFICIAL ORDER :: MORATORIUM : ?", ["Ban","Temporary suspension","Delay","Cancellation"], "Temporary suspension",
     "A mandate is an official order. A moratorium is a temporary suspension of activity.",
     ["word analogy","definition","government"]),
    ("ALLOCATE : DISTRIBUTE :: STIPULATE : ?", ["Agree","Specify as a condition","Request","Demand"], "Specify as a condition",
     "Allocate means to distribute resources. Stipulate means to specify as a condition.",
     ["word analogy","definition","formal-common"]),
    ("RATIFY : FORMALLY APPROVE :: RESCIND : ?", ["Reject","Formally cancel","Delay","Review"], "Formally cancel",
     "Ratify means to formally approve. Rescind means to formally cancel/revoke.",
     ["word analogy","definition","government"]),
    ("DISSEMINATE : SPREAD WIDELY :: CONSOLIDATE : ?", ["Strengthen","Combine into one","Reduce","Organize"], "Combine into one",
     "Disseminate means to spread widely. Consolidate means to combine into one.",
     ["word analogy","definition","formal-common"]),
    ("EXPEDITE : SPEED UP :: IMPEDE : ?", ["Slow down","Block","Stop","Prevent"], "Slow down",
     "Expedite means to speed up a process. Impede means to slow down/hinder.",
     ["word analogy","definition","formal-common"]),
    ("MITIGATE : LESSEN SEVERITY :: EXACERBATE : ?", ["Improve","Worsen","Change","Complicate"], "Worsen",
     "Mitigate means to lessen severity. Exacerbate means to worsen/intensify.",
     ["word analogy","definition","formal-common"]),
    ("SCRUTINIZE : EXAMINE CLOSELY :: PERUSE : ?", ["Skim","Read thoroughly","Glance","Browse"], "Read thoroughly",
     "Scrutinize means to examine closely. Peruse means to read thoroughly.",
     ["word analogy","definition","formal-common"]),
    ("CORROBORATE : CONFIRM WITH EVIDENCE :: REFUTE : ?", ["Deny","Disprove with evidence","Reject","Argue"], "Disprove with evidence",
     "Corroborate means to confirm with evidence. Refute means to disprove with evidence.",
     ["word analogy","definition","formal-common"]),
    ("AMELIORATE : MAKE BETTER :: DETERIORATE : ?", ["Improve","Become worse","Change","Decay"], "Become worse",
     "Ameliorate means to make better. Deteriorate means to become worse.",
     ["word analogy","definition","vocabulary"]),
    ("ACQUIESCE : ACCEPT WITHOUT PROTEST :: DISSENT : ?", ["Agree","Disagree openly","Leave","Refuse"], "Disagree openly",
     "Acquiesce means to accept without protest. Dissent means to disagree openly.",
     ["word analogy","definition","vocabulary"]),
    ("ABRIDGE : SHORTEN :: ELABORATE : ?", ["Decorate","Expand in detail","Improve","Complicate"], "Expand in detail",
     "Abridge means to shorten a text. Elaborate means to expand in detail.",
     ["word analogy","definition","vocabulary"]),
    ("PROCRASTINATE : DELAY ACTION :: EXPEDITE : ?", ["Rush","Hasten action","Force","Push"], "Hasten action",
     "Procrastinate means to delay action. Expedite means to hasten action.",
     ["word analogy","definition","vocabulary"]),
    # --- Context-Based Meaning (professional/abstract shifts) ---
    ("RUN : MANAGE :: TABLE : ?", ["Furniture","Postpone discussion","Flat surface","List"], "Postpone discussion",
     "Run in business context means manage. Table in meeting context means postpone discussion.",
     ["word analogy","context","meaning-shift"]),
    ("FILE : SUBMIT FORMALLY :: ADDRESS : ?", ["Location","Deal with a problem","Speech","House number"], "Deal with a problem",
     "File in legal/admin context means submit formally. Address in problem-solving context means deal with.",
     ["word analogy","context","meaning-shift"]),
    ("DRAFT : PRELIMINARY VERSION :: MINUTE : ?", ["Time unit","Official meeting record","Small","Tiny"], "Official meeting record",
     "Draft in writing context means preliminary version. Minute in government context means official meeting record.",
     ["word analogy","context","meaning-shift"]),
    ("EXECUTE : CARRY OUT A PLAN :: DISCHARGE : ?", ["Fire","Fulfill a duty","Release","Shoot"], "Fulfill a duty",
     "Execute in project context means carry out. Discharge in responsibility context means fulfill a duty.",
     ["word analogy","context","meaning-shift"]),
    ("TENDER : FORMAL BID :: BRIEF : ?", ["Short","Legal summary document","Quick","Concise"], "Legal summary document",
     "Tender in procurement context means formal bid. Brief in legal context means summary document.",
     ["word analogy","context","meaning-shift"]),
    ("INTEREST : FINANCIAL RETURN :: PRINCIPAL : ?", ["Main","Original loan amount","Leader","First"], "Original loan amount",
     "Interest in finance means financial return. Principal in finance means original loan amount.",
     ["word analogy","context","meaning-shift"]),
    ("APPRECIATION : INCREASE IN VALUE :: DEPRECIATION : ?", ["Criticism","Decrease in value","Sadness","Loss"], "Decrease in value",
     "Appreciation in finance means increase in value. Depreciation in finance means decrease in value.",
     ["word analogy","context","meaning-shift"]),
    ("GROSS : TOTAL BEFORE DEDUCTIONS :: NET : ?", ["Mesh","Total after deductions","Profit","Catch"], "Total after deductions",
     "Gross in accounting means total before deductions. Net in accounting means total after deductions.",
     ["word analogy","context","meaning-shift"]),
    ("YIELD : RETURN ON INVESTMENT :: BOND : ?", ["Connection","Debt security","Glue","Promise"], "Debt security",
     "Yield in finance means return on investment. Bond in finance means debt security instrument.",
     ["word analogy","context","meaning-shift"]),
    ("CULTURE : GROWING ORGANISMS :: MEDIUM : ?", ["Average","Growth substance","Middle","Size"], "Growth substance",
     "Culture in biology means growing organisms. Medium in biology means growth substance for organisms.",
     ["word analogy","context","meaning-shift"]),
    ("SENTENCE : JUDICIAL PUNISHMENT :: CHARGE : ?", ["Electricity","Formal accusation","Fee","Attack"], "Formal accusation",
     "Sentence in legal context means judicial punishment. Charge in legal context means formal accusation.",
     ["word analogy","context","meaning-shift"]),
    ("RESOLUTION : FORMAL DECISION :: MOTION : ?", ["Movement","Formal proposal","Exercise","Speed"], "Formal proposal",
     "Resolution in legislative context means formal decision. Motion in parliamentary context means formal proposal.",
     ["word analogy","context","meaning-shift"]),
    ("CAPITAL : FINANCIAL ASSETS :: EQUITY : ?", ["Fairness","Ownership value","Balance","Justice"], "Ownership value",
     "Capital in economics means financial assets. Equity in finance means ownership value.",
     ["word analogy","context","meaning-shift"]),
    ("PARTY : PERSON IN LEGAL CASE :: SUIT : ?", ["Clothing","Legal action","Match","Set"], "Legal action",
     "Party in legal context means person in a case. Suit in legal context means legal action/lawsuit.",
     ["word analogy","context","meaning-shift"]),
    ("BILL : PROPOSED LAW :: ACT : ?", ["Performance","Enacted law","Deed","Behavior"], "Enacted law",
     "Bill in legislative context means proposed law. Act in legislative context means enacted law.",
     ["word analogy","context","meaning-shift"]),
    # --- Vocabulary Association (concept : field, professional) ---
    ("VERDICT : COURTROOM :: DIAGNOSIS : ?", ["Doctor","Clinic","Medicine","Patient"], "Clinic",
     "A verdict is reached in a courtroom. A diagnosis is reached in a clinic.",
     ["word analogy","association","conclusion-setting"]),
    ("AUDIT : ACCOUNTING :: LITIGATION : ?", ["Court","Law","Dispute","Judge"], "Law",
     "An audit is a process in accounting. Litigation is a process in law.",
     ["word analogy","association","process-field"]),
    ("SCALPEL : SURGERY :: GAVEL : ?", ["Judge","Courtroom","Law","Justice"], "Courtroom",
     "A scalpel is a tool used in surgery. A gavel is a tool used in a courtroom.",
     ["word analogy","association","tool-setting"]),
    ("LEDGER : ACCOUNTING :: BLUEPRINT : ?", ["Architecture","Building","Design","Plan"], "Architecture",
     "A ledger is a document used in accounting. A blueprint is a document used in architecture.",
     ["word analogy","association","document-field"]),
    ("HYPOTHESIS : RESEARCH :: PRECEDENT : ?", ["Past","Case law","History","Example"], "Case law",
     "A hypothesis guides research. A precedent guides case law decisions.",
     ["word analogy","association","concept-field"]),
    ("PROCUREMENT : SUPPLY CHAIN :: TRIAGE : ?", ["Hospital","Emergency medicine","Sorting","Priority"], "Emergency medicine",
     "Procurement is a process in supply chain management. Triage is a process in emergency medicine.",
     ["word analogy","association","process-field"]),
    ("MEMORANDUM : OFFICIAL COMMUNICATION :: AFFIDAVIT : ?", ["Legal evidence","Court","Oath","Document"], "Legal evidence",
     "A memorandum is a document for official communication. An affidavit is a document for legal evidence.",
     ["word analogy","association","document-purpose"]),
    ("CURRICULUM : EDUCATION :: PROTOCOL : ?", ["Diplomacy","Rules","Manners","Government"], "Diplomacy",
     "A curriculum is a framework in education. A protocol is a framework in diplomacy.",
     ["word analogy","association","framework-field"]),
    ("APPROPRIATION : BUDGET :: RATIFICATION : ?", ["Treaty","Agreement","Law","Approval"], "Treaty",
     "Appropriation is a formal action in budgeting. Ratification is a formal action for treaties.",
     ["word analogy","association","action-domain"]),
    ("DISBURSEMENT : TREASURY :: ENROLLMENT : ?", ["School","Registration","Student","Education"], "Registration",
     "Disbursement is a process handled by treasury. Enrollment is a process handled by registration.",
     ["word analogy","association","process-office"]),
    ("ORDINANCE : LOCAL GOVERNMENT :: STATUTE : ?", ["National legislature","Court","Judge","Police"], "National legislature",
     "An ordinance is a law from local government. A statute is a law from national legislature.",
     ["word analogy","association","law-source"]),
    ("COMPLIANCE : REGULATION :: ADHERENCE : ?", ["Glue","Policy","Sticking","Rules"], "Policy",
     "Compliance means following regulations. Adherence means following policy.",
     ["word analogy","association","action-domain"]),
    ("ACCREDITATION : STANDARDS :: CERTIFICATION : ?", ["Competency","Paper","Training","Test"], "Competency",
     "Accreditation verifies standards. Certification verifies competency.",
     ["word analogy","association","verification-target"]),
    ("ADJUDICATION : JUDICIARY :: ARBITRATION : ?", ["Dispute resolution","Court","Judge","Mediation"], "Dispute resolution",
     "Adjudication is a process in the judiciary. Arbitration is a process in dispute resolution.",
     ["word analogy","association","process-field"]),
    ("SUBPOENA : LEGAL PROCESS :: SUMMONS : ?", ["Court appearance","Letter","Call","Invitation"], "Court appearance",
     "A subpoena is a document in legal process. A summons is a document requiring court appearance.",
     ["word analogy","association","document-purpose"]),
    # --- Multiple-Meaning (medium complexity) ---
    ("CURRENT : ELECTRICAL FLOW :: CHARGE : ?", ["Cost","Stored energy","Attack","Accusation"], "Stored energy",
     "Current in physics means electrical flow. Charge in physics means stored energy.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("INTEREST : CURIOSITY :: RESERVATION : ?", ["Booking","Doubt or hesitation","Restaurant","Hotel"], "Doubt or hesitation",
     "Interest's common meaning is curiosity. Reservation's common meaning is doubt/hesitation (not hotel booking).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("CABINET : GROUP OF MINISTERS :: CHAMBER : ?", ["Room","Legislative body","Heart","Box"], "Legislative body",
     "Cabinet in government means group of ministers. Chamber in government means legislative body.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("ORDER : COMMAND :: SENTENCE : ?", ["Grammar unit","Judicial punishment","Words","Paragraph"], "Judicial punishment",
     "Order in authority context means command. Sentence in legal context means judicial punishment.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("TERM : TIME PERIOD :: SESSION : ?", ["Meeting period","Sitting","Class","Activity"], "Meeting period",
     "Term can mean a defined time period. Session can mean a meeting period.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("RECORD : BEST ACHIEVEMENT :: MARK : ?", ["Stain","Target or standard","Sign","Grade"], "Target or standard",
     "Record can mean best achievement. Mark can mean a target or standard to meet.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("DEGREE : ACADEMIC QUALIFICATION :: DIPLOMA : ?", ["Certificate of completion","Paper","School","Frame"], "Certificate of completion",
     "Degree can mean academic qualification. Diploma means certificate of completion.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("VOLUME : SINGLE BOOK :: ISSUE : ?", ["Problem","Single edition of periodical","Topic","Concern"], "Single edition of periodical",
     "Volume can mean a single book in a series. Issue can mean a single edition of a periodical.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("DRAFT : MILITARY SELECTION :: LEVY : ?", ["Tax collection","Fee","Fine","Payment"], "Tax collection",
     "Draft can mean military selection/conscription. Levy can mean tax collection/imposition.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("CASE : INSTANCE :: POINT : ?", ["Dot","Argument or reason","Sharp end","Score"], "Argument or reason",
     "Case can mean an instance/example. Point can mean an argument or reason.",
     ["word analogy","multiple-meaning","polysemy"]),
    # --- Additional Medium Definition ---
    ("UBIQUITOUS : PRESENT EVERYWHERE :: EPHEMERAL : ?", ["Lasting briefly","Beautiful","Fragile","Rare"], "Lasting briefly",
     "Ubiquitous means present everywhere. Ephemeral means lasting briefly.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("PRAGMATIC : FOCUSED ON PRACTICAL RESULTS :: IDEALISTIC : ?", ["Smart","Focused on principles over practicality","Happy","Creative"], "Focused on principles over practicality",
     "Pragmatic means focused on practical results. Idealistic means focused on principles over practicality.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("METICULOUS : EXTREMELY CAREFUL :: NEGLIGENT : ?", ["Lazy","Extremely careless","Slow","Forgetful"], "Extremely careless",
     "Meticulous means extremely careful. Negligent means extremely careless.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("TENACIOUS : HOLDING FIRMLY TO PURPOSE :: FICKLE : ?", ["Weak","Changing purpose frequently","Confused","Lost"], "Changing purpose frequently",
     "Tenacious means holding firmly to purpose. Fickle means changing purpose frequently.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("PROLIFIC : PRODUCING ABUNDANTLY :: BARREN : ?", ["Empty","Producing nothing","Dry","Dead"], "Producing nothing",
     "Prolific means producing abundantly. Barren means producing nothing.",
     ["word analogy","definition","advanced-vocabulary"]),
    # --- Additional Medium Context ---
    ("PLANT : MANUFACTURING FACILITY :: OPERATION : ?", ["Surgery","Business activity","Machine","Work"], "Business activity",
     "Plant in industry means manufacturing facility. Operation in business means business activity/venture.",
     ["word analogy","context","meaning-shift"]),
    ("SECURITY : FINANCIAL INSTRUMENT :: COMMODITY : ?", ["Product","Tradeable raw material","Good","Item"], "Tradeable raw material",
     "Security in finance means financial instrument. Commodity in finance means tradeable raw material.",
     ["word analogy","context","meaning-shift"]),
    ("FLOOR : MINIMUM LIMIT :: CEILING : ?", ["Roof","Maximum limit","Top","Cover"], "Maximum limit",
     "Floor in economics means minimum limit. Ceiling in economics means maximum limit.",
     ["word analogy","context","meaning-shift"]),
    ("HEDGE : RISK PROTECTION :: LEVERAGE : ?", ["Power","Borrowed capital for investment","Lift","Force"], "Borrowed capital for investment",
     "Hedge in finance means risk protection strategy. Leverage in finance means using borrowed capital.",
     ["word analogy","context","meaning-shift"]),
    ("BENCH : JUDGES COLLECTIVELY :: BAR : ?", ["Drink","Legal profession collectively","Rod","Counter"], "Legal profession collectively",
     "Bench in legal context means judges collectively. Bar in legal context means the legal profession collectively.",
     ["word analogy","context","meaning-shift"]),
    # --- Additional Medium Association ---
    ("STETHOSCOPE : PHYSICIAN :: THEODOLITE : ?", ["Surveyor","Engineer","Builder","Architect"], "Surveyor",
     "A stethoscope is the primary tool of a physician. A theodolite is the primary tool of a surveyor.",
     ["word analogy","association","tool-profession"]),
    ("INJUNCTION : JUDICIAL REMEDY :: SANCTION : ?", ["Approval","Punitive measure","Permission","Rule"], "Punitive measure",
     "An injunction is a type of judicial remedy. A sanction is a type of punitive measure.",
     ["word analogy","association","action-category"]),
    ("QUORUM : MEETING :: MAJORITY : ?", ["Most","Vote","Election","Decision"], "Vote",
     "A quorum is the minimum needed for a valid meeting. A majority is the minimum needed for a valid vote.",
     ["word analogy","association","threshold-process"]),
    ("INDICTMENT : CRIMINAL CASE :: COMPLAINT : ?", ["Problem","Civil case","Grievance","Issue"], "Civil case",
     "An indictment initiates a criminal case. A complaint initiates a civil case.",
     ["word analogy","association","document-process"]),
    ("PROSPECTUS : INVESTMENT :: SYLLABUS : ?", ["Course","School","Teacher","Study"], "Course",
     "A prospectus is an informational document for an investment. A syllabus is an informational document for a course.",
     ["word analogy","association","document-subject"]),
    # --- Additional Medium Multiple-Meaning ---
    ("TENDER : LEGAL CURRENCY :: BILL : ?", ["Law","Paper money","Invoice","Statement"], "Paper money",
     "Tender in finance means legal currency. Bill can mean paper money.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("BRIEF : CONCISE :: MINUTE : ?", ["Time","Extremely small","Record","Meeting"], "Extremely small",
     "Brief as adjective means concise/short. Minute as adjective means extremely small.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("CONDUCT : BEHAVIOR :: BEARING : ?", ["Direction","Manner of carrying oneself","Weight","Support"], "Manner of carrying oneself",
     "Conduct as noun means behavior. Bearing as noun means manner of carrying oneself.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("CONTRACT : LEGAL AGREEMENT :: COMPACT : ?", ["Small","Formal agreement","Tight","Cosmetic case"], "Formal agreement",
     "Contract means a legal agreement. Compact can also mean a formal agreement.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("ARTICLE : WRITTEN PIECE :: CLAUSE : ?", ["Santa","Section of a legal document","Grammar","Sentence"], "Section of a legal document",
     "Article can mean a written piece. Clause can mean a section of a legal document.",
     ["word analogy","multiple-meaning","polysemy"]),
]

HARD_QUESTIONS = [
    # --- Advanced Definition (rare/academic vocabulary) ---
    ("RECALCITRANT : STUBBORNLY UNCOOPERATIVE :: OBSEQUIOUS : ?", ["Rude","Excessively eager to please","Quiet","Shy"], "Excessively eager to please",
     "Recalcitrant means stubbornly uncooperative. Obsequious means excessively eager to please authority.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("PERSPICACIOUS : HAVING KEEN PERCEPTION :: OBTUSE : ?", ["Sharp","Lacking sharpness of mind","Angled","Blunt"], "Lacking sharpness of mind",
     "Perspicacious means having keen mental perception. Obtuse means lacking sharpness of mind.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("MAGNANIMOUS : GENEROUS IN FORGIVING :: VINDICTIVE : ?", ["Kind","Seeking revenge","Angry","Cruel"], "Seeking revenge",
     "Magnanimous means generous in forgiving. Vindictive means seeking revenge.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("SYCOPHANT : ONE WHO FLATTERS FOR ADVANTAGE :: ICONOCLAST : ?", ["Artist","One who attacks established beliefs","Rebel","Destroyer"], "One who attacks established beliefs",
     "A sycophant flatters for advantage. An iconoclast attacks established beliefs.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("PERFUNCTORY : DONE WITHOUT CARE :: ASSIDUOUS : ?", ["Quick","Done with great care and persistence","Lazy","Routine"], "Done with great care and persistence",
     "Perfunctory means done without care. Assiduous means done with great care and persistence.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("EQUIVOCATE : USE AMBIGUOUS LANGUAGE :: PREVARICATE : ?", ["Lie","Speak evasively to mislead","Delay","Avoid"], "Speak evasively to mislead",
     "Equivocate means to use ambiguous language. Prevaricate means to speak evasively to mislead.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("CAPITULATE : SURRENDER UNDER AGREED CONDITIONS :: ABDICATE : ?", ["Leave","Formally renounce power","Lose","Quit"], "Formally renounce power",
     "Capitulate means to surrender under agreed conditions. Abdicate means to formally renounce power.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("ENERVATE : DRAIN OF ENERGY :: INVIGORATE : ?", ["Tire","Fill with energy and vitality","Excite","Motivate"], "Fill with energy and vitality",
     "Enervate means to drain of energy. Invigorate means to fill with energy and vitality.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("LACONIC : USING VERY FEW WORDS :: VERBOSE : ?", ["Quiet","Using too many words","Loud","Talkative"], "Using too many words",
     "Laconic means using very few words. Verbose means using too many words.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("PARSIMONIOUS : EXTREMELY UNWILLING TO SPEND :: PROFLIGATE : ?", ["Rich","Recklessly wasteful with money","Generous","Careless"], "Recklessly wasteful with money",
     "Parsimonious means extremely unwilling to spend. Profligate means recklessly wasteful with money.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("SANGUINE : OPTIMISTICALLY CHEERFUL :: MOROSE : ?", ["Angry","Sullenly gloomy","Quiet","Tired"], "Sullenly gloomy",
     "Sanguine means optimistically cheerful. Morose means sullenly gloomy.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("LOQUACIOUS : EXCESSIVELY TALKATIVE :: TACITURN : ?", ["Shy","Habitually silent","Rude","Boring"], "Habitually silent",
     "Loquacious means excessively talkative. Taciturn means habitually silent.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("GREGARIOUS : FOND OF COMPANY :: RECLUSIVE : ?", ["Lonely","Preferring solitude","Shy","Quiet"], "Preferring solitude",
     "Gregarious means fond of company. Reclusive means preferring solitude.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("EPHEMERAL : LASTING A VERY SHORT TIME :: PERENNIAL : ?", ["Yearly","Lasting indefinitely","Seasonal","Recurring"], "Lasting indefinitely",
     "Ephemeral means lasting a very short time. Perennial means lasting indefinitely.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("INSCRUTABLE : IMPOSSIBLE TO UNDERSTAND :: PELLUCID : ?", ["Clear","Transparently clear in meaning","Bright","Simple"], "Transparently clear in meaning",
     "Inscrutable means impossible to understand. Pellucid means transparently clear in meaning.",
     ["word analogy","definition","advanced-vocabulary"]),
    # --- Advanced Context (contronyms, technical shifts) ---
    ("SANCTION : AUTHORIZE :: CLEAVE : ?", ["Split","Cling to","Cut","Separate"], "Cling to",
     "Sanction can mean authorize (positive sense). Cleave can mean cling to (positive sense). Both are contronyms with opposite meanings.",
     ["word analogy","context","contronym"]),
    ("OVERSIGHT : SUPERVISION :: DUST : ?", ["Clean","To add fine particles","Remove","Wipe"], "To add fine particles",
     "Oversight can mean supervision (active watching). Dust can mean to add fine particles (as in dusting a cake). Both contronyms used in their less obvious sense.",
     ["word analogy","context","contronym"]),
    ("QUALIFY : ADD LIMITING CONDITIONS :: TEMPER : ?", ["Heat","Moderate or restrain","Anger","Metal"], "Moderate or restrain",
     "Qualify in legal context means to add limiting conditions. Temper in discourse means to moderate or restrain.",
     ["word analogy","context","meaning-shift"]),
    ("DISPOSITION : TEMPERAMENT :: CONSTITUTION : ?", ["Document","Physical makeup of a person","Law","Government"], "Physical makeup of a person",
     "Disposition in personality context means temperament. Constitution in health context means physical makeup.",
     ["word analogy","context","meaning-shift"]),
    ("INSTRUMENT : LEGAL DOCUMENT :: VEHICLE : ?", ["Car","Means of achieving something","Transport","Machine"], "Means of achieving something",
     "Instrument in legal context means a formal document. Vehicle in abstract context means a means of achieving something.",
     ["word analogy","context","meaning-shift"]),
    ("CONSIDERATION : PAYMENT IN CONTRACT :: TENDER : ?", ["Soft","Formal offer to fulfill obligation","Gentle","Young"], "Formal offer to fulfill obligation",
     "Consideration in contract law means payment/exchange. Tender in contract law means formal offer to fulfill obligation.",
     ["word analogy","context","meaning-shift"]),
    ("RELIEF : LEGAL REMEDY :: DISCOVERY : ?", ["Finding","Pre-trial evidence gathering","Science","Exploration"], "Pre-trial evidence gathering",
     "Relief in legal context means remedy/redress. Discovery in legal context means pre-trial evidence gathering.",
     ["word analogy","context","meaning-shift"]),
    ("MATERIAL : LEGALLY SIGNIFICANT :: CONSTRUCTIVE : ?", ["Building","Legally implied though not actual","Helpful","Positive"], "Legally implied though not actual",
     "Material in legal context means legally significant. Constructive in legal context means legally implied though not actual.",
     ["word analogy","context","meaning-shift"]),
    ("PREJUDICE : LEGAL HARM TO RIGHTS :: PRIVILEGE : ?", ["Advantage","Legal right to withhold information","Wealth","Power"], "Legal right to withhold information",
     "Prejudice in legal context means harm to legal rights. Privilege in legal context means right to withhold information.",
     ["word analogy","context","meaning-shift"]),
    ("INTEREST : LEGAL STAKE IN PROPERTY :: TITLE : ?", ["Name","Legal ownership right","Book","Position"], "Legal ownership right",
     "Interest in property law means legal stake. Title in property law means legal ownership right.",
     ["word analogy","context","meaning-shift"]),
    ("ACTION : LAWSUIT :: COMPLAINT : ?", ["Grievance","Initial pleading in civil case","Problem","Criticism"], "Initial pleading in civil case",
     "Action in legal context means lawsuit. Complaint in legal context means initial pleading in civil case.",
     ["word analogy","context","meaning-shift"]),
    ("APPRECIATION : VALUE INCREASE :: AMORTIZATION : ?", ["Payment","Gradual debt reduction","Depreciation","Loss"], "Gradual debt reduction",
     "Appreciation in finance means value increase. Amortization in finance means gradual debt reduction.",
     ["word analogy","context","meaning-shift"]),
    ("FLOAT : SHARES AVAILABLE FOR TRADING :: LIQUIDITY : ?", ["Water","Ease of converting to cash","Flow","Fluid"], "Ease of converting to cash",
     "Float in finance means shares available for trading. Liquidity in finance means ease of converting to cash.",
     ["word analogy","context","meaning-shift"]),
    ("EXPOSURE : AMOUNT AT RISK :: POSITION : ?", ["Place","Holdings in a financial instrument","Job","Stance"], "Holdings in a financial instrument",
     "Exposure in finance means amount at risk. Position in finance means holdings in a financial instrument.",
     ["word analogy","context","meaning-shift"]),
    ("MARGIN : BORROWED FUNDS FOR TRADING :: SPREAD : ?", ["Butter","Difference between bid and ask price","Wide","Range"], "Difference between bid and ask price",
     "Margin in trading means borrowed funds. Spread in trading means difference between bid and ask price.",
     ["word analogy","context","meaning-shift"]),
    # --- Advanced Vocabulary Association ---
    ("EPISTEMOLOGY : THEORY OF KNOWLEDGE :: ONTOLOGY : ?", ["Being","Study of existence","Logic","Reality"], "Study of existence",
     "Epistemology is the philosophical study of knowledge. Ontology is the philosophical study of existence.",
     ["word analogy","association","philosophy"]),
    ("HERMENEUTICS : INTERPRETATION OF TEXTS :: SEMIOTICS : ?", ["Signs","Study of signs and symbols","Language","Meaning"], "Study of signs and symbols",
     "Hermeneutics is the theory of text interpretation. Semiotics is the study of signs and symbols.",
     ["word analogy","association","academic-field"]),
    ("EPIDEMIOLOGY : DISEASE PATTERNS :: DEMOGRAPHY : ?", ["People","Population characteristics","Census","Statistics"], "Population characteristics",
     "Epidemiology studies disease patterns. Demography studies population characteristics.",
     ["word analogy","association","field-subject"]),
    ("FIDUCIARY : TRUST MANAGEMENT :: EXECUTOR : ?", ["Kill","Estate administration","Manager","Leader"], "Estate administration",
     "A fiduciary's role involves trust management. An executor's role involves estate administration.",
     ["word analogy","association","role-responsibility"]),
    ("TAXONOMY : CLASSIFICATION :: ETYMOLOGY : ?", ["Insects","Word origin study","Language","History"], "Word origin study",
     "Taxonomy is the science of classification. Etymology is the study of word origins.",
     ["word analogy","association","discipline-subject"]),
    ("RHETORIC : PERSUASIVE COMMUNICATION :: DIALECTIC : ?", ["Speech","Logical argumentation","Debate","Language"], "Logical argumentation",
     "Rhetoric is the art of persuasive communication. Dialectic is the art of logical argumentation.",
     ["word analogy","association","discipline-method"]),
    ("JURISPRUDENCE : LEGAL PHILOSOPHY :: BIOETHICS : ?", ["Biology","Moral issues in medicine","Health","Science"], "Moral issues in medicine",
     "Jurisprudence examines legal philosophy. Bioethics examines moral issues in medicine.",
     ["word analogy","association","field-subject"]),
    ("PRAGMATICS : LANGUAGE IN CONTEXT :: PHONOLOGY : ?", ["Sound","Sound systems in language","Voice","Speech"], "Sound systems in language",
     "Pragmatics studies language in context. Phonology studies sound systems in language.",
     ["word analogy","association","linguistics-branch"]),
    ("FORENSICS : CRIMINAL INVESTIGATION :: ACTUARIAL SCIENCE : ?", ["Math","Risk assessment","Insurance","Statistics"], "Risk assessment",
     "Forensics applies science to criminal investigation. Actuarial science applies math to risk assessment.",
     ["word analogy","association","applied-field"]),
    ("CARTOGRAPHY : MAP MAKING :: CRYPTOGRAPHY : ?", ["Secrets","Code creation and breaking","Hidden","Mystery"], "Code creation and breaking",
     "Cartography is the science of map making. Cryptography is the science of code creation and breaking.",
     ["word analogy","association","discipline-activity"]),
    # --- Advanced Multiple-Meaning ---
    ("SANCTION : PENALTY :: OVERSIGHT : ?", ["Supervision","Failure to notice","Error","Mistake"], "Failure to notice",
     "Sanction can mean penalty (negative sense). Oversight can mean failure to notice (negative sense). Both contronyms in their negative meaning.",
     ["word analogy","multiple-meaning","contronym"]),
    ("CLEAVE : TO SPLIT APART :: RAVEL : ?", ["Knit","To tangle or complicate","Unwind","Separate"], "To tangle or complicate",
     "Cleave can mean to split apart. Ravel can mean to tangle/complicate. Both contronyms in their separating/complicating sense.",
     ["word analogy","multiple-meaning","contronym"]),
    ("FAST : FIRMLY FIXED :: BOUND : ?", ["Jump","Obligated or destined","Tied","Limit"], "Obligated or destined",
     "Fast can mean firmly fixed (hold fast). Bound can mean obligated or destined (bound to happen).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("MOOT : DEBATABLE :: ACADEMIC : ?", ["School","Having no practical relevance","Scholarly","Theoretical"], "Having no practical relevance",
     "Moot can mean debatable/open to discussion. Academic can mean having no practical relevance.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("PATENT : OBVIOUS :: LATENT : ?", ["Hidden","Present but not visible","Late","Slow"], "Present but not visible",
     "Patent can mean obvious/clearly visible. Latent means present but not visible/dormant.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("CARDINAL : OF PRIMARY IMPORTANCE :: NOMINAL : ?", ["Name","In name only, not in reality","Small","Number"], "In name only, not in reality",
     "Cardinal can mean of primary importance. Nominal can mean in name only, not in reality.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("CATHOLIC : UNIVERSAL IN SCOPE :: PROVINCIAL : ?", ["Region","Narrow-minded or limited","Local","Rural"], "Narrow-minded or limited",
     "Catholic (lowercase) means universal in scope. Provincial means narrow-minded or limited in outlook.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("ECONOMY : THRIFTY USE OF RESOURCES :: INDUSTRY : ?", ["Factory","Hard work and diligence","Business","Manufacturing"], "Hard work and diligence",
     "Economy can mean thrifty use of resources (not national economy). Industry can mean hard work/diligence (not manufacturing sector).",
     ["word analogy","multiple-meaning","polysemy"]),
    ("GRAVITY : SERIOUSNESS :: LEVITY : ?", ["Lightness","Lack of seriousness","Float","Humor"], "Lack of seriousness",
     "Gravity can mean seriousness (not physical force). Levity means lack of seriousness/inappropriate humor.",
     ["word analogy","multiple-meaning","polysemy"]),
    ("CURRENCY : RELEVANCE TO PRESENT TIME :: TENDER : ?", ["Soft","Something offered in payment","Gentle","Young"], "Something offered in payment",
     "Currency can mean relevance to present time (not money). Tender can mean something offered in payment (legal tender).",
     ["word analogy","multiple-meaning","polysemy"]),
    # --- Additional Hard Definition ---
    ("PUSILLANIMOUS : SHOWING LACK OF COURAGE :: INTREPID : ?", ["Scared","Showing fearless adventure","Strong","Bold"], "Showing fearless adventure",
     "Pusillanimous means showing lack of courage. Intrepid means showing fearless adventure.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("VERISIMILITUDE : APPEARANCE OF BEING TRUE :: MENDACITY : ?", ["Truth","Habitual dishonesty","Lying","Deception"], "Habitual dishonesty",
     "Verisimilitude means the appearance of being true. Mendacity means habitual dishonesty.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("PULCHRITUDE : PHYSICAL BEAUTY :: TURPITUDE : ?", ["Ugliness","Moral wickedness","Evil","Crime"], "Moral wickedness",
     "Pulchritude means physical beauty. Turpitude means moral wickedness/depravity.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("QUOTIDIAN : OCCURRING DAILY :: PERENNIAL : ?", ["Yearly","Occurring repeatedly over many years","Seasonal","Monthly"], "Occurring repeatedly over many years",
     "Quotidian means occurring daily. Perennial means occurring repeatedly over many years.",
     ["word analogy","definition","advanced-vocabulary"]),
    ("PENURIOUS : EXTREMELY POOR :: OPULENT : ?", ["Rich","Extremely wealthy and luxurious","Fancy","Expensive"], "Extremely wealthy and luxurious",
     "Penurious means extremely poor. Opulent means extremely wealthy and luxurious.",
     ["word analogy","definition","advanced-vocabulary"]),
    # --- Additional Hard Context ---
    ("STANDING : LEGAL RIGHT TO SUE :: JURISDICTION : ?", ["Area","Court's authority over a case","Power","Control"], "Court's authority over a case",
     "Standing in legal context means right to bring a lawsuit. Jurisdiction means court's authority over a case.",
     ["word analogy","context","legal"]),
    ("ESTOPPEL : LEGAL BAR TO CONTRADICTING :: WAIVER : ?", ["Wave","Voluntary relinquishment of right","Excuse","Pass"], "Voluntary relinquishment of right",
     "Estoppel is a legal bar to contradicting one's previous position. Waiver is voluntary relinquishment of a right.",
     ["word analogy","context","legal"]),
    ("FUNGIBLE : MUTUALLY INTERCHANGEABLE :: INALIENABLE : ?", ["Foreign","Cannot be transferred or taken away","Permanent","Fixed"], "Cannot be transferred or taken away",
     "Fungible in legal/finance means mutually interchangeable. Inalienable means cannot be transferred or taken away.",
     ["word analogy","context","legal"]),
    ("FIDUCIARY : HELD IN TRUST :: PROPRIETARY : ?", ["Proper","Owned exclusively","Private","Secret"], "Owned exclusively",
     "Fiduciary describes something held in trust. Proprietary describes something owned exclusively.",
     ["word analogy","context","legal-business"]),
    ("PRIMA FACIE : ACCEPTED UNTIL DISPROVED :: DE FACTO : ?", ["Legal","Existing in practice though not officially","Real","Actual"], "Existing in practice though not officially",
     "Prima facie means accepted as correct until disproved. De facto means existing in practice though not officially established.",
     ["word analogy","context","legal"]),
    # --- Additional Hard Association ---
    ("HABEAS CORPUS : PERSONAL LIBERTY :: DUE PROCESS : ?", ["Court","Fair legal proceedings","Law","Rights"], "Fair legal proceedings",
     "Habeas corpus protects personal liberty. Due process ensures fair legal proceedings.",
     ["word analogy","association","legal-principle"]),
    ("AMICUS CURIAE : COURT ADVISORY :: OMBUDSMAN : ?", ["Government","Citizen complaint investigation","Judge","Mediator"], "Citizen complaint investigation",
     "An amicus curiae provides court advisory opinions. An ombudsman investigates citizen complaints.",
     ["word analogy","association","role-function"]),
    ("VOIR DIRE : JURY SELECTION :: ARRAIGNMENT : ?", ["Trial","Formal charge reading","Court","Hearing"], "Formal charge reading",
     "Voir dire is the process of jury selection. Arraignment is the process of formal charge reading.",
     ["word analogy","association","legal-process"]),
    ("EMINENT DOMAIN : GOVERNMENT PROPERTY TAKING :: POLICE POWER : ?", ["Force","Government regulation for public welfare","Authority","Control"], "Government regulation for public welfare",
     "Eminent domain is government's power to take property. Police power is government's power to regulate for public welfare.",
     ["word analogy","association","government-power"]),
    ("STARE DECISIS : FOLLOWING PRECEDENT :: RES JUDICATA : ?", ["Thing","Finality of judgment","Decision","Law"], "Finality of judgment",
     "Stare decisis is the principle of following precedent. Res judicata is the principle of finality of judgment.",
     ["word analogy","association","legal-doctrine"]),
]


# ---------------------------------------------------------------------------
# Additional question banks to reach 200 per difficulty
# These use template-based generation from word pair data
# ---------------------------------------------------------------------------

# Definition pairs for template generation: (word, definition, formal_flag)
EXTRA_EASY_DEFINITIONS = [
    ("Cautious","careful to avoid danger"),("Generous","willing to give freely"),
    ("Hostile","unfriendly and aggressive"),("Humble","not proud or arrogant"),
    ("Innocent","not guilty"),("Juvenile","young or immature"),
    ("Keen","eager or enthusiastic"),("Loyal","faithful and devoted"),
    ("Modest","not boastful"),("Naive","lacking experience"),
    ("Obedient","willing to follow rules"),("Patient","able to wait calmly"),
    ("Reluctant","unwilling or hesitant"),("Sincere","genuine and honest"),
    ("Urgent","requiring immediate action"),("Vivid","bright and intense"),
    ("Weary","very tired"),("Zealous","showing great enthusiasm"),
    ("Adequate","enough or sufficient"),("Beneficial","helpful or useful"),
    ("Chronic","lasting a long time"),("Deficient","lacking something needed"),
    ("Eligible","qualified to participate"),("Feasible","possible to do"),
    ("Gratitude","feeling of thankfulness"),("Hazardous","dangerous or risky"),
    ("Impartial","fair and unbiased"),("Jeopardize","put at risk"),
    ("Legitimate","lawful or valid"),("Negligible","too small to matter"),
    ("Obsolete","no longer in use"),("Plausible","seeming reasonable"),
    ("Relevant","closely connected to the topic"),("Substantial","large in amount"),
    ("Trivial","of little importance"),("Unanimous","fully in agreement"),
    ("Versatile","able to adapt to many functions"),("Wholesome","good for health or character"),
    ("Adjacent","next to or near"),("Compulsory","required by law or rule"),
    ("Deliberate","done on purpose"),("Exempt","free from an obligation"),
]

EXTRA_EASY_CONTEXT_SHIFTS = [
    ("Dry","boring","humor","lacking moisture","weather"),
    ("Raw","inexperienced","skill","uncooked","food"),
    ("Steep","excessive","price","sharply angled","hill"),
    ("Stiff","formal","manner","rigid","material"),
    ("Tender","young","age","soft","texture"),
    ("Thick","close","friendship","wide","measurement"),
    ("Thin","weak","argument","narrow","width"),
    ("Wild","uncontrolled","behavior","untamed","animal"),
    ("Narrow","limited","view","thin","width"),
    ("Broad","general","topic","wide","road"),
    ("Clean","honest","record","free of dirt","surface"),
    ("Dirty","unfair","trick","covered in dirt","clothes"),
    ("Fresh","new","idea","recently made","bread"),
    ("Gross","disgusting","behavior","total before deductions","income"),
    ("Hollow","insincere","promise","empty inside","tree"),
    ("Solid","reliable","evidence","firm","ground"),
    ("Straight","honest","answer","not curved","line"),
    ("Crooked","dishonest","politician","not straight","path"),
]

EXTRA_EASY_ASSOCIATIONS = [
    ("Stethoscope","doctor"),("Wrench","mechanic"),("Spatula","chef"),
    ("Chalk","teacher"),("Badge","police officer"),("Helmet","firefighter"),
    ("Trowel","gardener"),("Needle","tailor"),("Lens","photographer"),
    ("Microphone","singer"),("Easel","painter"),("Chisel","sculptor"),
    ("Keyboard","typist"),("Hose","firefighter"),("Whistle","coach"),
    ("Apron","baker"),("Drill","dentist"),("Saw","carpenter"),
    ("Net","fisherman"),("Loom","weaver"),
]

EXTRA_MEDIUM_DEFINITIONS = [
    ("Ambivalent","having mixed feelings"),("Benevolent","well-meaning and kindly"),
    ("Complacent","smugly self-satisfied"),("Deference","respectful submission"),
    ("Eloquent","fluent and persuasive in speech"),("Fortuitous","happening by chance"),
    ("Gratuitous","uncalled for or unwarranted"),("Hegemony","dominance of one group"),
    ("Impervious","unable to be affected"),("Juxtapose","place side by side for comparison"),
    ("Kinetic","relating to motion"),("Lucid","clear and easy to understand"),
    ("Malleable","easily influenced or shaped"),("Nefarious","wicked or criminal"),
    ("Ostensible","appearing to be true but not necessarily"),("Pernicious","having harmful effect"),
    ("Quintessential","representing the most perfect example"),("Repudiate","refuse to accept"),
    ("Superfluous","more than what is needed"),("Tangible","able to be touched or felt"),
    ("Unilateral","done by one side only"),("Vicarious","experienced through another"),
    ("Wanton","deliberate and unprovoked"),("Xenophobia","fear of foreigners"),
    ("Zealot","fanatical supporter"),("Acumen","ability to make good judgments"),
    ("Brevity","concise expression"),("Candor","quality of being open and honest"),
    ("Duplicity","deceitfulness"),("Efficacy","ability to produce desired result"),
]

EXTRA_MEDIUM_CONTEXT = [
    ("Mature","fully developed","investment","grown up","person"),
    ("Liquid","easily converted to cash","assets","fluid","water"),
    ("Volatile","likely to change rapidly","market","explosive","chemical"),
    ("Elastic","responsive to change","demand","stretchy","material"),
    ("Toxic","harmful to organization","workplace","poisonous","substance"),
    ("Organic","natural growth without force","business growth","carbon-based","chemistry"),
    ("Leverage","use borrowed capital","finance","mechanical advantage","physics"),
    ("Inflation","general price increase","economics","expansion with air","balloon"),
    ("Depression","economic downturn","economics","deep sadness","psychology"),
    ("Bubble","unsustainable price rise","market","air in liquid","soap"),
    ("Channel","means of distribution","marketing","waterway","geography"),
    ("Platform","political position statement","politics","raised surface","construction"),
    ("Ceiling","upper limit","regulation","overhead surface","room"),
    ("Foundation","underlying basis","argument","base structure","building"),
    ("Bridge","connection between groups","diplomacy","structure over water","engineering"),
]

EXTRA_HARD_DEFINITIONS = [
    ("Abnegate","renounce or reject"),("Calumny","false and malicious statement"),
    ("Desultory","lacking a plan or purpose"),("Effulgent","shining brightly"),
    ("Fatuous","silly and pointless"),("Garrulous","excessively talkative"),
    ("Harangue","lengthy aggressive speech"),("Ignominious","deserving public disgrace"),
    ("Jejune","naive and simplistic"),("Kowtow","act excessively subservient"),
    ("Lugubrious","looking or sounding sad"),("Malfeasance","wrongdoing by public official"),
    ("Nascent","just beginning to develop"),("Obdurate","stubbornly refusing to change"),
    ("Panacea","solution for all problems"),("Quixotic","extremely idealistic and unrealistic"),
    ("Recondite","little known or obscure"),("Surreptitious","kept secret because improper"),
    ("Truculent","eager to fight or argue"),("Unctuous","excessively flattering"),
    ("Vacillate","waver between different opinions"),("Wistful","having feeling of vague longing"),
    ("Acrimonious","angry and bitter"),("Bellicose","demonstrating aggression"),
    ("Capricious","given to sudden changes of mood"),("Deleterious","causing harm or damage"),
    ("Egregious","outstandingly bad"),("Furtive","attempting to avoid notice"),
    ("Grandiloquent","pompous in language"),("Hubris","excessive pride or self-confidence"),
]


# ---------------------------------------------------------------------------
# Template-based question generators
# ---------------------------------------------------------------------------

def _gen_definition_q(word: str, definition: str, difficulty: str) -> tuple:
    """Generate a definition analogy question from a word-definition pair."""
    # Create distractors based on difficulty
    if difficulty == "Easy":
        distractors = ["Something unrelated", "A type of action", "A physical object"]
    elif difficulty == "Medium":
        distractors = ["Showing indifference", "Related to physical space", "A temporary state"]
    else:
        distractors = ["Pertaining to external form", "Characterized by brevity", "Lacking substance"]

    q = f"{word.upper()} : {definition.upper()} — Which pair follows the same pattern?"
    # We'll use a simpler format for template questions
    correct = f"Word matched to its precise definition"
    choices = [definition.capitalize(), distractors[0], distractors[1], distractors[2]]
    random.shuffle(choices)
    return (
        f"If {word.upper()} means '{definition}', which word-meaning pair follows the same WORD : DEFINITION pattern?",
        choices, definition.capitalize(),
        f"{word.capitalize()} is defined as '{definition}'. The correct answer matches a word to its precise definition.",
        ["word analogy", "definition", "vocabulary"]
    )


def _gen_context_q(word: str, abstract_meaning: str, abstract_domain: str,
                   literal_meaning: str, literal_domain: str, difficulty: str) -> tuple:
    """Generate a context-based meaning question."""
    q = f"{word.upper()} : {abstract_meaning.upper()} :: Which pair shows the same context-based meaning shift?"
    choices = [
        f"A word used in its {abstract_domain} sense",
        f"A word used in its {literal_domain} sense",
        "A direct synonym pair",
        "An antonym relationship"
    ]
    answer = f"A word used in its {abstract_domain} sense"
    return (
        f"{word.upper()} in {abstract_domain} context means '{abstract_meaning}'. Which follows the same pattern?",
        choices, answer,
        f"{word.capitalize()} in {abstract_domain} context means {abstract_meaning} (not {literal_meaning} in {literal_domain} context).",
        ["word analogy", "context", "meaning-shift"]
    )


def _gen_association_q(tool: str, profession: str) -> tuple:
    """Generate a tool-profession association question."""
    distractors = random.sample([
        "Student","Manager","Customer","Scientist","Artist","Engineer",
        "Accountant","Lawyer","Nurse","Driver","Writer","Farmer"
    ], 3)
    # Make sure correct answer isn't in distractors
    distractors = [d for d in distractors if d.lower() != profession.lower()][:3]
    choices = [profession] + distractors
    random.shuffle(choices)
    return (
        f"{tool.upper()} is primarily associated with which profession?",
        choices, profession,
        f"A {tool.lower()} is the primary tool/equipment of a {profession.lower()}.",
        ["word analogy", "association", "tool-profession"]
    )


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def _build_questions(bank: list, difficulty: str, start_id: int) -> list:
    """Convert a raw question bank into formatted question dicts."""
    questions = []
    for i, (question, choices, answer, explanation, tags) in enumerate(bank):
        questions.append({
            "id": start_id + i,
            **B,
            "difficulty": difficulty,
            "question": question,
            "choices": choices,
            "answer": answer,
            "explanation": explanation,
            "tags": tags,
        })
    return questions


def _pad_easy(existing: list) -> list:
    """Pad easy questions to reach 200 using templates."""
    needed = 200 - len(existing)
    extra = []
    idx = 0

    # Generate from definition pairs
    for word, defn in EXTRA_EASY_DEFINITIONS:
        if idx >= needed:
            break
        pair_idx = idx % len(EXTRA_EASY_DEFINITIONS)
        # Create paired questions
        other_word, other_defn = EXTRA_EASY_DEFINITIONS[(pair_idx + 1) % len(EXTRA_EASY_DEFINITIONS)]
        q = f"{word.upper()} : {defn.capitalize()} :: {other_word.upper()} : ?"
        distractors = random.sample([
            "Something unrelated","A physical action","An emotional state",
            "A type of object","A measurement","A location",
            "A time period","A person","A quality"
        ], 3)
        choices = [other_defn.capitalize()] + distractors
        random.shuffle(choices)
        extra.append((
            q, choices, other_defn.capitalize(),
            f"{word.capitalize()} means '{defn}'. {other_word.capitalize()} means '{other_defn}'. Both pairs show word-to-definition relationships.",
            ["word analogy", "definition", "vocabulary"]
        ))
        idx += 1

    # Generate from context shifts
    for word, abstract, a_domain, literal, l_domain in EXTRA_EASY_CONTEXT_SHIFTS:
        if idx >= needed:
            break
        other_idx = idx % len(EXTRA_EASY_CONTEXT_SHIFTS)
        other = EXTRA_EASY_CONTEXT_SHIFTS[(other_idx + 3) % len(EXTRA_EASY_CONTEXT_SHIFTS)]
        q = f"{word.upper()} : {abstract.capitalize()} :: {other[0].upper()} : ?"
        choices = [other[1].capitalize(), other[3].capitalize(), "Unrelated meaning", "Opposite meaning"]
        random.shuffle(choices)
        extra.append((
            q, choices, other[1].capitalize(),
            f"{word.capitalize()} in {a_domain} context means '{abstract}'. {other[0].capitalize()} in {other[2]} context means '{other[1]}'.",
            ["word analogy", "context", "meaning-shift"]
        ))
        idx += 1

    # Generate from associations
    for tool, prof in EXTRA_EASY_ASSOCIATIONS:
        if idx >= needed:
            break
        other_idx = idx % len(EXTRA_EASY_ASSOCIATIONS)
        other_tool, other_prof = EXTRA_EASY_ASSOCIATIONS[(other_idx + 2) % len(EXTRA_EASY_ASSOCIATIONS)]
        q = f"{tool.upper()} : {prof.capitalize()} :: {other_tool.upper()} : ?"
        distractors = random.sample(["Teacher","Driver","Scientist","Manager","Clerk","Nurse"], 3)
        distractors = [d for d in distractors if d.lower() != other_prof.lower()][:3]
        choices = [other_prof.capitalize()] + distractors
        random.shuffle(choices)
        extra.append((
            q, choices, other_prof.capitalize(),
            f"A {tool.lower()} is used by a {prof.lower()}. A {other_tool.lower()} is used by a {other_prof.lower()}.",
            ["word analogy", "association", "tool-profession"]
        ))
        idx += 1

    return extra[:needed]


def _pad_medium(existing: list) -> list:
    """Pad medium questions to reach 200 using templates."""
    needed = 200 - len(existing)
    extra = []
    idx = 0

    for word, defn in EXTRA_MEDIUM_DEFINITIONS:
        if idx >= needed:
            break
        pair_idx = idx % len(EXTRA_MEDIUM_DEFINITIONS)
        other_word, other_defn = EXTRA_MEDIUM_DEFINITIONS[(pair_idx + 1) % len(EXTRA_MEDIUM_DEFINITIONS)]
        q = f"{word.upper()} : {defn.capitalize()} :: {other_word.upper()} : ?"
        distractors = random.sample([
            "Showing physical strength","Related to time","A spatial concept",
            "Pertaining to sound","A numerical value","An emotional response",
            "A social construct","A natural phenomenon","A cognitive process"
        ], 3)
        choices = [other_defn.capitalize()] + distractors
        random.shuffle(choices)
        extra.append((
            q, choices, other_defn.capitalize(),
            f"{word.capitalize()} means '{defn}'. {other_word.capitalize()} means '{other_defn}'. Both pairs show word-to-definition relationships.",
            ["word analogy", "definition", "advanced-vocabulary"]
        ))
        idx += 1

    for word, abstract, a_domain, literal, l_domain in EXTRA_MEDIUM_CONTEXT:
        if idx >= needed:
            break
        other_idx = idx % len(EXTRA_MEDIUM_CONTEXT)
        other = EXTRA_MEDIUM_CONTEXT[(other_idx + 2) % len(EXTRA_MEDIUM_CONTEXT)]
        q = f"{word.upper()} : {abstract.capitalize()} :: {other[0].upper()} : ?"
        choices = [other[1].capitalize(), other[3].capitalize(), "A literal physical meaning", "An unrelated concept"]
        random.shuffle(choices)
        extra.append((
            q, choices, other[1].capitalize(),
            f"{word.capitalize()} in {a_domain} context means '{abstract}'. {other[0].capitalize()} in {other[2]} context means '{other[1]}'.",
            ["word analogy", "context", "meaning-shift"]
        ))
        idx += 1

    return extra[:needed]


def _pad_hard(existing: list) -> list:
    """Pad hard questions to reach 200 using templates."""
    needed = 200 - len(existing)
    extra = []
    idx = 0

    for word, defn in EXTRA_HARD_DEFINITIONS:
        if idx >= needed:
            break
        pair_idx = idx % len(EXTRA_HARD_DEFINITIONS)
        other_word, other_defn = EXTRA_HARD_DEFINITIONS[(pair_idx + 1) % len(EXTRA_HARD_DEFINITIONS)]
        q = f"{word.upper()} : {defn.capitalize()} :: {other_word.upper()} : ?"
        distractors = random.sample([
            "Demonstrating physical prowess","Pertaining to temporal matters",
            "Characterized by spatial awareness","Relating to auditory perception",
            "Exhibiting numerical precision","Manifesting emotional volatility",
            "Concerning social hierarchies","Involving natural processes",
            "Reflecting cognitive limitations"
        ], 3)
        choices = [other_defn.capitalize()] + distractors
        random.shuffle(choices)
        extra.append((
            q, choices, other_defn.capitalize(),
            f"{word.capitalize()} means '{defn}'. {other_word.capitalize()} means '{other_defn}'. Both pairs show advanced word-to-definition relationships.",
            ["word analogy", "definition", "advanced-vocabulary"]
        ))
        idx += 1

    return extra[:needed]


def main() -> None:
    random.seed(42)

    # Build base questions from hand-crafted banks
    easy_base = EASY_QUESTIONS
    medium_base = MEDIUM_QUESTIONS
    hard_base = HARD_QUESTIONS

    # Pad each to 200
    easy_extra = _pad_easy(easy_base)
    medium_extra = _pad_medium(medium_base)
    hard_extra = _pad_hard(hard_base)

    easy_all = easy_base + easy_extra
    medium_all = medium_base + medium_extra
    hard_all = hard_base + hard_extra

    # Shuffle within difficulty
    random.shuffle(easy_all)
    random.shuffle(medium_all)
    random.shuffle(hard_all)

    # Trim to exactly 200 each
    easy_all = easy_all[:200]
    medium_all = medium_all[:200]
    hard_all = hard_all[:200]

    # Build final question list
    all_questions = []
    all_questions.extend(_build_questions(easy_all, "Easy", 1))
    all_questions.extend(_build_questions(medium_all, "Medium", 201))
    all_questions.extend(_build_questions(hard_all, "Hard", 401))

    # Write output
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(all_questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(all_questions)} questions to {OUTPUT}")
    print(f"  Easy: {sum(1 for q in all_questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in all_questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in all_questions if q['difficulty'] == 'Hard')}")


if __name__ == "__main__":
    main()
