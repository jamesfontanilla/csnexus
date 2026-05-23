"""
Generate 600 symbolic, characteristic, and location relationship questions.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/analytical-ability/word-analogy/
        symbolic-characteristic-and-location-relationships/questions.json
"""
import json
import random
from pathlib import Path

OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions" / "analytical-ability"
    / "word-analogy" / "symbolic-characteristic-and-location-relationships"
    / "questions.json"
)

B = {
    "subtest": "Analytical Ability",
    "module": "Word Analogy",
    "subtopic": "Symbolic, Characteristic, and Location Relationships",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}

# fmt: off
# ============================================================================
# DATA BANKS
# Each tuple: (first_pair_a, first_pair_b, answer_a, answer_b)
# Question format: "A : B :: C : ?"  answer is D
# ============================================================================

# --- SYMBOL-AND-MEANING pairs ---
EASY_SYMBOLS = [
    ("dove","peace","heart","love"),
    ("heart","love","dove","peace"),
    ("crown","royalty","flag","patriotism"),
    ("skull","death","heart","love"),
    ("flag","patriotism","crown","royalty"),
    ("heart","love","ring","commitment"),
    ("dove","peace","crown","royalty"),
    ("crown","royalty","skull","death"),
    ("ring","commitment","heart","love"),
    ("skull","death","dove","peace"),
    ("heart","love","skull","death"),
    ("dove","peace","flag","patriotism"),
    ("flag","patriotism","dove","peace"),
    ("crown","royalty","heart","love"),
    ("ring","commitment","dove","peace"),
    ("skull","death","crown","royalty"),
    ("heart","love","flag","patriotism"),
    ("dove","peace","ring","commitment"),
    ("flag","patriotism","skull","death"),
    ("crown","royalty","ring","commitment"),
    ("dove","peace","skull","death"),
    ("skull","death","ring","commitment"),
    ("flag","patriotism","heart","love"),
    ("ring","commitment","crown","royalty"),
    ("heart","love","crown","royalty"),
    ("crown","royalty","dove","peace"),
    ("flag","patriotism","ring","commitment"),
    ("ring","commitment","flag","patriotism"),
    ("skull","death","flag","patriotism"),
    ("dove","peace","star","excellence"),
    ("star","excellence","dove","peace"),
    ("star","excellence","heart","love"),
    ("heart","love","star","excellence"),
    ("star","excellence","crown","royalty"),
    ("crown","royalty","star","excellence"),
    ("star","excellence","flag","patriotism"),
    ("flag","patriotism","star","excellence"),
    ("star","excellence","skull","death"),
    ("skull","death","star","excellence"),
    ("star","excellence","ring","commitment"),
]

EASY_SIGNS = [
    ("red light","stop","green light","go"),
    ("green light","go","red light","stop"),
    ("siren","emergency","alarm","danger"),
    ("alarm","danger","siren","emergency"),
    ("red light","stop","siren","emergency"),
    ("green light","go","alarm","danger"),
    ("siren","emergency","red light","stop"),
    ("alarm","danger","green light","go"),
    ("red light","stop","alarm","danger"),
    ("green light","go","siren","emergency"),
    ("siren","emergency","green light","go"),
    ("alarm","danger","red light","stop"),
    ("red light","stop","whistle","attention"),
    ("whistle","attention","red light","stop"),
    ("horn","warning","siren","emergency"),
    ("whistle","attention","green light","go"),
    ("green light","go","whistle","attention"),
    ("horn","warning","red light","stop"),
    ("red light","stop","horn","warning"),
    ("whistle","attention","alarm","danger"),
    ("alarm","danger","whistle","attention"),
    ("horn","warning","green light","go"),
    ("green light","go","horn","warning"),
    ("horn","warning","alarm","danger"),
    ("alarm","danger","horn","warning"),
    ("siren","emergency","whistle","attention"),
    ("whistle","attention","siren","emergency"),
    ("horn","warning","whistle","attention"),
    ("whistle","attention","horn","warning"),
    ("siren","emergency","horn","warning"),
    ("horn","warning","bell","alert"),
    ("bell","alert","horn","warning"),
    ("bell","alert","siren","emergency"),
    ("siren","emergency","bell","alert"),
    ("bell","alert","alarm","danger"),
    ("alarm","danger","bell","alert"),
    ("bell","alert","red light","stop"),
    ("red light","stop","bell","alert"),
    ("bell","alert","green light","go"),
    ("green light","go","bell","alert"),
]

EASY_QUALITIES = [
    ("ice","cold","fire","hot"),
    ("fire","hot","ice","cold"),
    ("sugar","sweet","lemon","sour"),
    ("lemon","sour","sugar","sweet"),
    ("feather","light","rock","heavy"),
    ("rock","heavy","feather","light"),
    ("ice","cold","sugar","sweet"),
    ("sugar","sweet","ice","cold"),
    ("fire","hot","feather","light"),
    ("feather","light","fire","hot"),
    ("rock","heavy","ice","cold"),
    ("ice","cold","rock","heavy"),
    ("cotton","soft","rock","hard"),
    ("rock","hard","cotton","soft"),
    ("honey","sweet","vinegar","sour"),
    ("vinegar","sour","honey","sweet"),
    ("silk","smooth","sandpaper","rough"),
    ("sandpaper","rough","silk","smooth"),
    ("ice","cold","cotton","soft"),
    ("fire","hot","rock","hard"),
    ("cotton","soft","silk","smooth"),
    ("silk","smooth","cotton","soft"),
    ("honey","sweet","sugar","sweet"),
    ("lemon","sour","vinegar","sour"),
    ("feather","light","cotton","soft"),
    ("cotton","soft","feather","light"),
    ("rock","hard","ice","cold"),
    ("ice","cold","silk","smooth"),
    ("fire","hot","honey","sweet"),
    ("honey","sweet","fire","hot"),
    ("sandpaper","rough","rock","hard"),
    ("rock","hard","sandpaper","rough"),
    ("vinegar","sour","lemon","sour"),
    ("lemon","sour","ice","cold"),
    ("ice","cold","lemon","sour"),
    ("sugar","sweet","cotton","soft"),
    ("cotton","soft","sugar","sweet"),
    ("fire","hot","silk","smooth"),
    ("silk","smooth","fire","hot"),
    ("feather","light","sugar","sweet"),
]

EASY_TRAITS = [
    ("lion","bravery","fox","cunning"),
    ("fox","cunning","lion","bravery"),
    ("owl","wisdom","lion","bravery"),
    ("lion","bravery","owl","wisdom"),
    ("ant","industry","lion","bravery"),
    ("lion","bravery","ant","industry"),
    ("fox","cunning","owl","wisdom"),
    ("owl","wisdom","fox","cunning"),
    ("lamb","innocence","lion","bravery"),
    ("lion","bravery","lamb","innocence"),
    ("snake","deceit","dove","gentleness"),
    ("dove","gentleness","snake","deceit"),
    ("peacock","vanity","ant","industry"),
    ("ant","industry","peacock","vanity"),
    ("turtle","patience","fox","cunning"),
    ("fox","cunning","turtle","patience"),
    ("eagle","strength","owl","wisdom"),
    ("owl","wisdom","eagle","strength"),
    ("lamb","innocence","fox","cunning"),
    ("snake","deceit","lamb","innocence"),
    ("peacock","vanity","lion","bravery"),
    ("lion","bravery","peacock","vanity"),
    ("turtle","patience","owl","wisdom"),
    ("owl","wisdom","turtle","patience"),
    ("eagle","strength","fox","cunning"),
    ("fox","cunning","eagle","strength"),
    ("ant","industry","lamb","innocence"),
    ("lamb","innocence","ant","industry"),
    ("snake","deceit","owl","wisdom"),
    ("owl","wisdom","snake","deceit"),
    ("peacock","vanity","fox","cunning"),
    ("fox","cunning","peacock","vanity"),
    ("turtle","patience","ant","industry"),
    ("ant","industry","turtle","patience"),
    ("eagle","strength","lamb","innocence"),
    ("lamb","innocence","eagle","strength"),
    ("snake","deceit","ant","industry"),
    ("ant","industry","snake","deceit"),
    ("peacock","vanity","turtle","patience"),
    ("turtle","patience","peacock","vanity"),
]

EASY_PLACES = [
    ("book","library","fish","ocean"),
    ("fish","ocean","book","library"),
    ("teacher","classroom","doctor","hospital"),
    ("doctor","hospital","teacher","classroom"),
    ("bird","sky","fish","ocean"),
    ("fish","ocean","bird","sky"),
    ("book","library","teacher","classroom"),
    ("teacher","classroom","book","library"),
    ("car","garage","airplane","airport"),
    ("airplane","airport","car","garage"),
    ("student","classroom","patient","hospital"),
    ("patient","hospital","student","classroom"),
    ("book","library","car","garage"),
    ("car","garage","book","library"),
    ("fish","ocean","teacher","classroom"),
    ("doctor","hospital","fish","ocean"),
    ("bird","nest","fish","ocean"),
    ("airplane","airport","ship","harbor"),
    ("ship","harbor","airplane","airport"),
    ("chef","kitchen","teacher","classroom"),
    ("chef","kitchen","doctor","hospital"),
    ("doctor","hospital","chef","kitchen"),
    ("student","classroom","fish","ocean"),
    ("fish","ocean","student","classroom"),
    ("bird","sky","car","garage"),
    ("car","garage","bird","sky"),
    ("airplane","airport","doctor","hospital"),
    ("doctor","hospital","airplane","airport"),
    ("ship","harbor","book","library"),
    ("book","library","ship","harbor"),
    ("chef","kitchen","car","garage"),
    ("car","garage","chef","kitchen"),
    ("patient","hospital","book","library"),
    ("book","library","patient","hospital"),
    ("bird","nest","car","garage"),
    ("car","garage","bird","nest"),
    ("ship","harbor","chef","kitchen"),
    ("chef","kitchen","ship","harbor"),
    ("student","classroom","airplane","airport"),
    ("airplane","airport","student","classroom"),
]

EASY_CAPITALS = [
    ("Philippines","Manila","Japan","Tokyo"),
    ("Japan","Tokyo","Philippines","Manila"),
    ("France","Paris","Japan","Tokyo"),
    ("Japan","Tokyo","France","Paris"),
    ("Philippines","Manila","France","Paris"),
    ("France","Paris","Philippines","Manila"),
    ("United Kingdom","London","France","Paris"),
    ("France","Paris","United Kingdom","London"),
    ("Japan","Tokyo","United Kingdom","London"),
    ("United Kingdom","London","Japan","Tokyo"),
    ("Philippines","Manila","United Kingdom","London"),
    ("United Kingdom","London","Philippines","Manila"),
    ("Italy","Rome","France","Paris"),
    ("France","Paris","Italy","Rome"),
    ("Spain","Madrid","Italy","Rome"),
    ("Italy","Rome","Spain","Madrid"),
    ("Germany","Berlin","France","Paris"),
    ("France","Paris","Germany","Berlin"),
    ("Philippines","Manila","Germany","Berlin"),
    ("Japan","Tokyo","Italy","Rome"),
    ("Germany","Berlin","Japan","Tokyo"),
    ("Japan","Tokyo","Germany","Berlin"),
    ("Spain","Madrid","France","Paris"),
    ("France","Paris","Spain","Madrid"),
    ("Italy","Rome","Japan","Tokyo"),
    ("Japan","Tokyo","Spain","Madrid"),
    ("Spain","Madrid","Japan","Tokyo"),
    ("Germany","Berlin","Italy","Rome"),
    ("Italy","Rome","Germany","Berlin"),
    ("Spain","Madrid","Philippines","Manila"),
    ("Philippines","Manila","Spain","Madrid"),
    ("Germany","Berlin","United Kingdom","London"),
    ("United Kingdom","London","Germany","Berlin"),
    ("Spain","Madrid","United Kingdom","London"),
    ("United Kingdom","London","Spain","Madrid"),
    ("Italy","Rome","Philippines","Manila"),
    ("Philippines","Manila","Italy","Rome"),
    ("Germany","Berlin","Spain","Madrid"),
    ("Spain","Madrid","Germany","Berlin"),
    ("Italy","Rome","United Kingdom","London"),
]

# --- MEDIUM DATA BANKS ---

MEDIUM_SYMBOLS = [
    ("scales","justice","torch","knowledge"),
    ("torch","knowledge","scales","justice"),
    ("olive branch","peace","laurel wreath","victory"),
    ("laurel wreath","victory","olive branch","peace"),
    ("white flag","surrender","olive branch","peace"),
    ("gavel","authority","scales","justice"),
    ("scales","justice","gavel","authority"),
    ("torch","knowledge","white flag","surrender"),
    ("anchor","stability","compass","direction"),
    ("compass","direction","anchor","stability"),
    ("candle","hope","anchor","stability"),
    ("anchor","stability","candle","hope"),
    ("handshake","agreement","white flag","surrender"),
    ("white flag","surrender","handshake","agreement"),
    ("badge","authority","seal","authenticity"),
    ("seal","authenticity","badge","authority"),
    ("fist","resistance","handshake","agreement"),
    ("handshake","agreement","fist","resistance"),
    ("ballot","democracy","gavel","authority"),
    ("gavel","authority","ballot","democracy"),
    ("ribbon","awareness","candle","hope"),
    ("candle","hope","ribbon","awareness"),
    ("torch","knowledge","laurel wreath","victory"),
    ("laurel wreath","victory","torch","knowledge"),
    ("scales","justice","white flag","surrender"),
    ("white flag","surrender","scales","justice"),
    ("olive branch","peace","handshake","agreement"),
    ("handshake","agreement","olive branch","peace"),
    ("compass","direction","torch","knowledge"),
    ("torch","knowledge","compass","direction"),
    ("anchor","stability","scales","justice"),
    ("scales","justice","anchor","stability"),
    ("gavel","authority","torch","knowledge"),
    ("badge","authority","gavel","authority"),
]

MEDIUM_SIGNS = [
    ("yellow light","caution","red light","stop"),
    ("smoke","fire","red light","stop"),
    ("skull and crossbones","poison","red cross","medical aid"),
    ("red cross","medical aid","skull and crossbones","poison"),
    ("thumbs up","approval","thumbs down","disapproval"),
    ("thumbs down","disapproval","thumbs up","approval"),
    ("nod","agreement","shrug","uncertainty"),
    ("shrug","uncertainty","nod","agreement"),
    ("smoke","fire","fever","illness"),
    ("fever","illness","smoke","fire"),
    ("dark clouds","storm","smoke","fire"),
    ("smoke","fire","dark clouds","storm"),
    ("yellow light","caution","dark clouds","storm"),
    ("dark clouds","storm","yellow light","caution"),
    ("flashing lights","emergency","yellow light","caution"),
    ("yellow light","caution","flashing lights","emergency"),
    ("knock","visitor","ring","call"),
    ("ring","call","knock","visitor"),
    ("wink","secret","nod","agreement"),
    ("nod","agreement","wink","secret"),
    ("tears","sadness","smile","happiness"),
    ("smile","happiness","tears","sadness"),
    ("applause","approval","boo","disapproval"),
    ("boo","disapproval","applause","approval"),
    ("smoke","fire","tremor","earthquake"),
    ("tremor","earthquake","smoke","fire"),
    ("red flag","warning","green flag","safety"),
    ("green flag","safety","red flag","warning"),
    ("sweat","exertion","yawn","fatigue"),
    ("yawn","fatigue","sweat","exertion"),
    ("blush","embarrassment","tears","sadness"),
    ("tears","sadness","blush","embarrassment"),
    ("thunder","storm","smoke","fire"),
    ("smoke","fire","thunder","storm"),
]

MEDIUM_QUALITIES = [
    ("diamond","hard","rubber","elastic"),
    ("rubber","elastic","diamond","hard"),
    ("sponge","absorbent","diamond","hard"),
    ("diamond","hard","sponge","absorbent"),
    ("steel","strong","glass","fragile"),
    ("glass","fragile","steel","strong"),
    ("mercury","liquid","ice","solid"),
    ("ice","solid","mercury","liquid"),
    ("velvet","soft","sandpaper","rough"),
    ("sandpaper","rough","velvet","soft"),
    ("chili","spicy","sugar","sweet"),
    ("sugar","sweet","chili","spicy"),
    ("snow","white","coal","black"),
    ("coal","black","snow","white"),
    ("honey","viscous","water","fluid"),
    ("water","fluid","honey","viscous"),
    ("thunder","loud","whisper","quiet"),
    ("whisper","quiet","thunder","loud"),
    ("desert","dry","ocean","wet"),
    ("ocean","wet","desert","dry"),
    ("night","dark","day","bright"),
    ("day","bright","night","dark"),
    ("iron","magnetic","wood","non-magnetic"),
    ("glass","transparent","wall","opaque"),
    ("wall","opaque","glass","transparent"),
    ("gold","malleable","glass","brittle"),
    ("glass","brittle","gold","malleable"),
    ("helium","light","lead","heavy"),
    ("lead","heavy","helium","light"),
    ("diamond","hard","chalk","soft"),
    ("chalk","soft","diamond","hard"),
    ("oil","slippery","sandpaper","rough"),
    ("sandpaper","rough","oil","slippery"),
    ("acid","corrosive","water","neutral"),
]

MEDIUM_TRAITS = [
    ("judge","fairness","soldier","discipline"),
    ("soldier","discipline","judge","fairness"),
    ("nurse","compassion","judge","fairness"),
    ("judge","fairness","nurse","compassion"),
    ("teacher","patience","soldier","discipline"),
    ("soldier","discipline","teacher","patience"),
    ("diplomat","tact","judge","fairness"),
    ("judge","fairness","diplomat","tact"),
    ("scholar","intelligence","artist","creativity"),
    ("artist","creativity","scholar","intelligence"),
    ("hero","courage","coward","timidity"),
    ("coward","timidity","hero","courage"),
    ("monk","humility","hero","courage"),
    ("hero","courage","monk","humility"),
    ("miser","greed","philanthropist","generosity"),
    ("philanthropist","generosity","miser","greed"),
    ("leader","confidence","diplomat","tact"),
    ("diplomat","tact","leader","confidence"),
    ("guardian","protection","rebel","defiance"),
    ("rebel","defiance","guardian","protection"),
    ("scientist","curiosity","artist","creativity"),
    ("artist","creativity","scientist","curiosity"),
    ("firefighter","bravery","nurse","compassion"),
    ("nurse","compassion","firefighter","bravery"),
    ("accountant","precision","engineer","problem-solving"),
    ("engineer","problem-solving","accountant","precision"),
    ("lawyer","logic","doctor","dedication"),
    ("doctor","dedication","lawyer","logic"),
    ("journalist","truthfulness","diplomat","tact"),
    ("diplomat","tact","journalist","truthfulness"),
    ("architect","vision","scientist","curiosity"),
    ("scientist","curiosity","architect","vision"),
    ("counselor","empathy","teacher","patience"),
    ("teacher","patience","counselor","empathy"),
]

MEDIUM_PLACES = [
    ("pilot","cockpit","judge","courtroom"),
    ("judge","courtroom","pilot","cockpit"),
    ("scientist","laboratory","librarian","library"),
    ("librarian","library","scientist","laboratory"),
    ("mechanic","garage","chef","kitchen"),
    ("chef","kitchen","mechanic","garage"),
    ("prisoner","jail","patient","hospital"),
    ("patient","hospital","prisoner","jail"),
    ("artifact","museum","book","library"),
    ("book","library","artifact","museum"),
    ("athlete","stadium","actor","theater"),
    ("actor","theater","athlete","stadium"),
    ("farmer","field","miner","mine"),
    ("miner","mine","farmer","field"),
    ("sailor","ship","pilot","cockpit"),
    ("pilot","cockpit","sailor","ship"),
    ("cashier","counter","teller","bank"),
    ("teller","bank","cashier","counter"),
    ("worshipper","church","student","classroom"),
    ("student","classroom","worshipper","church"),
    ("camel","desert","penguin","Antarctica"),
    ("penguin","Antarctica","camel","desert"),
    ("cactus","desert","coral","reef"),
    ("coral","reef","cactus","desert"),
    ("whale","ocean","eagle","mountain"),
    ("eagle","mountain","whale","ocean"),
    ("bear","forest","camel","desert"),
    ("camel","desert","bear","forest"),
    ("surgeon","operating room","pharmacist","pharmacy"),
    ("pharmacist","pharmacy","surgeon","operating room"),
    ("curator","museum","warden","prison"),
    ("warden","prison","curator","museum"),
    ("referee","field","conductor","orchestra pit"),
    ("conductor","orchestra pit","referee","field"),
]

MEDIUM_CAPITALS = [
    ("Thailand","Bangkok","Vietnam","Hanoi"),
    ("Vietnam","Hanoi","Thailand","Bangkok"),
    ("Cambodia","Phnom Penh","Laos","Vientiane"),
    ("Laos","Vientiane","Cambodia","Phnom Penh"),
    ("Indonesia","Jakarta","Malaysia","Kuala Lumpur"),
    ("Malaysia","Kuala Lumpur","Indonesia","Jakarta"),
    ("South Korea","Seoul","China","Beijing"),
    ("China","Beijing","South Korea","Seoul"),
    ("India","New Delhi","Russia","Moscow"),
    ("Russia","Moscow","India","New Delhi"),
    ("Egypt","Cairo","South Korea","Seoul"),
    ("South Korea","Seoul","Egypt","Cairo"),
    ("Thailand","Bangkok","Cambodia","Phnom Penh"),
    ("Cambodia","Phnom Penh","Thailand","Bangkok"),
    ("Vietnam","Hanoi","Indonesia","Jakarta"),
    ("Indonesia","Jakarta","Vietnam","Hanoi"),
    ("Malaysia","Kuala Lumpur","Thailand","Bangkok"),
    ("Thailand","Bangkok","Malaysia","Kuala Lumpur"),
    ("China","Beijing","India","New Delhi"),
    ("India","New Delhi","China","Beijing"),
    ("Russia","Moscow","Egypt","Cairo"),
    ("Egypt","Cairo","Russia","Moscow"),
    ("South Korea","Seoul","Vietnam","Hanoi"),
    ("Vietnam","Hanoi","South Korea","Seoul"),
    ("Cambodia","Phnom Penh","Indonesia","Jakarta"),
    ("Indonesia","Jakarta","Cambodia","Phnom Penh"),
    ("Laos","Vientiane","Thailand","Bangkok"),
    ("Thailand","Bangkok","Laos","Vientiane"),
    ("Malaysia","Kuala Lumpur","Cambodia","Phnom Penh"),
    ("Cambodia","Phnom Penh","Malaysia","Kuala Lumpur"),
    ("China","Beijing","Russia","Moscow"),
    ("Russia","Moscow","China","Beijing"),
    ("India","New Delhi","Egypt","Cairo"),
    ("Egypt","Cairo","India","New Delhi"),
]

# --- HARD DATA BANKS ---

HARD_SYMBOLS = [
    ("caduceus","medicine","scales","justice"),
    ("scales","justice","caduceus","medicine"),
    ("phoenix","rebirth","ouroboros","eternity"),
    ("ouroboros","eternity","phoenix","rebirth"),
    ("labyrinth","complexity","crossroads","decision"),
    ("crossroads","decision","labyrinth","complexity"),
    ("hourglass","mortality","phoenix","rebirth"),
    ("phoenix","rebirth","hourglass","mortality"),
    ("lighthouse","guidance","compass","direction"),
    ("compass","direction","lighthouse","guidance"),
    ("mask","deception","mirror","truth"),
    ("mirror","truth","mask","deception"),
    ("seed","potential","phoenix","rebirth"),
    ("phoenix","rebirth","seed","potential"),
    ("web","interconnection","bridge","connection"),
    ("bridge","connection","web","interconnection"),
    ("hourglass","mortality","candle","hope"),
    ("candle","hope","hourglass","mortality"),
    ("labyrinth","complexity","web","interconnection"),
    ("web","interconnection","labyrinth","complexity"),
    ("crossroads","decision","lighthouse","guidance"),
    ("lighthouse","guidance","crossroads","decision"),
    ("mask","deception","labyrinth","complexity"),
    ("labyrinth","complexity","mask","deception"),
    ("caduceus","medicine","torch","knowledge"),
    ("torch","knowledge","caduceus","medicine"),
    ("ouroboros","eternity","hourglass","mortality"),
    ("hourglass","mortality","ouroboros","eternity"),
    ("mirror","truth","lighthouse","guidance"),
    ("lighthouse","guidance","mirror","truth"),
    ("seed","potential","hourglass","mortality"),
    ("hourglass","mortality","seed","potential"),
    ("phoenix","rebirth","labyrinth","complexity"),
    ("labyrinth","complexity","phoenix","rebirth"),
]

HARD_SIGNS = [
    ("semaphore","naval communication","morse code","telegraphy"),
    ("morse code","telegraphy","semaphore","naval communication"),
    ("double yellow line","no passing","broken white line","passing allowed"),
    ("broken white line","passing allowed","double yellow line","no passing"),
    ("black flag","disqualification","checkered flag","race finish"),
    ("checkered flag","race finish","black flag","disqualification"),
    ("raised eyebrow","skepticism","crossed arms","defensiveness"),
    ("crossed arms","defensiveness","raised eyebrow","skepticism"),
    ("white smoke","new pope elected","black smoke","no decision"),
    ("black smoke","no decision","white smoke","new pope elected"),
    ("tolling bell","death","ringing bell","celebration"),
    ("ringing bell","celebration","tolling bell","death"),
    ("half-mast flag","mourning","raised flag","sovereignty"),
    ("raised flag","sovereignty","half-mast flag","mourning"),
    ("red card","ejection","yellow card","warning"),
    ("yellow card","warning","red card","ejection"),
    ("gavel strike","order","standing ovation","acclaim"),
    ("standing ovation","acclaim","gavel strike","order"),
    ("white coat","medical profession","black robe","judiciary"),
    ("black robe","judiciary","white coat","medical profession"),
    ("laurel crown","victory","thorny crown","suffering"),
    ("thorny crown","suffering","laurel crown","victory"),
    ("broken chain","liberation","locked gate","imprisonment"),
    ("locked gate","imprisonment","broken chain","liberation"),
    ("olive branch","peace offering","drawn sword","declaration of war"),
    ("drawn sword","declaration of war","olive branch","peace offering"),
    ("raised fist","solidarity","open palm","peace"),
    ("open palm","peace","raised fist","solidarity"),
    ("red carpet","honor","cold shoulder","rejection"),
    ("cold shoulder","rejection","red carpet","honor"),
    ("tipped hat","respect","turned back","disrespect"),
    ("turned back","disrespect","tipped hat","respect"),
    ("slow clap","sarcasm","standing ovation","genuine praise"),
    ("standing ovation","genuine praise","slow clap","sarcasm"),
]

HARD_QUALITIES = [
    ("obsidian","brittle","diamond","hard"),
    ("diamond","hard","obsidian","brittle"),
    ("graphene","strong","aerogel","light"),
    ("aerogel","light","graphene","strong"),
    ("mercury","volatile","gold","stable"),
    ("gold","stable","mercury","volatile"),
    ("platinum","inert","sodium","reactive"),
    ("sodium","reactive","platinum","inert"),
    ("titanium","corrosion-resistant","iron","rust-prone"),
    ("iron","rust-prone","titanium","corrosion-resistant"),
    ("asbestos","heat-resistant","ice","cold"),
    ("ice","cold","asbestos","heat-resistant"),
    ("kevlar","bulletproof","glass","fragile"),
    ("glass","fragile","kevlar","bulletproof"),
    ("teflon","non-stick","glue","adhesive"),
    ("glue","adhesive","teflon","non-stick"),
    ("granite","durable","chalk","crumbly"),
    ("chalk","crumbly","granite","durable"),
    ("bamboo","flexible","oak","rigid"),
    ("oak","rigid","bamboo","flexible"),
    ("quicksilver","fluid","amber","solid"),
    ("amber","solid","quicksilver","fluid"),
    ("obsidian","sharp","pumice","porous"),
    ("pumice","porous","obsidian","sharp"),
    ("tungsten","dense","cork","buoyant"),
    ("cork","buoyant","tungsten","dense"),
    ("quartz","piezoelectric","rubber","insulating"),
    ("rubber","insulating","quartz","piezoelectric"),
    ("graphite","conductive","rubber","insulating"),
    ("rubber","insulating","graphite","conductive"),
    ("marble","veined","obsidian","glassy"),
    ("obsidian","glassy","marble","veined"),
    ("balsa","lightweight","ebony","dense"),
    ("ebony","dense","balsa","lightweight"),
]

HARD_TRAITS = [
    ("Machiavelli","cunning","Solomon","wisdom"),
    ("Solomon","wisdom","Machiavelli","cunning"),
    ("Sisyphus","futility","Prometheus","defiance"),
    ("Prometheus","defiance","Sisyphus","futility"),
    ("Midas","greed","Atlas","endurance"),
    ("Atlas","endurance","Midas","greed"),
    ("Narcissus","vanity","Achilles","vulnerability"),
    ("Achilles","vulnerability","Narcissus","vanity"),
    ("Hercules","strength","Odysseus","resourcefulness"),
    ("Odysseus","resourcefulness","Hercules","strength"),
    ("Judas","betrayal","Job","patience"),
    ("Job","patience","Judas","betrayal"),
    ("Cassandra","prophecy","Pandora","curiosity"),
    ("Pandora","curiosity","Cassandra","prophecy"),
    ("Icarus","recklessness","Daedalus","ingenuity"),
    ("Daedalus","ingenuity","Icarus","recklessness"),
    ("Scrooge","miserliness","Robin Hood","generosity"),
    ("Robin Hood","generosity","Scrooge","miserliness"),
    ("Don Quixote","idealism","Hamlet","indecision"),
    ("Hamlet","indecision","Don Quixote","idealism"),
    ("Sherlock Holmes","deduction","Machiavelli","cunning"),
    ("Machiavelli","cunning","Sherlock Holmes","deduction"),
    ("Mother Teresa","selflessness","Florence Nightingale","compassion"),
    ("Florence Nightingale","compassion","Mother Teresa","selflessness"),
    ("Einstein","genius","Da Vinci","versatility"),
    ("Da Vinci","versatility","Einstein","genius"),
    ("Gandhi","nonviolence","Mandela","perseverance"),
    ("Mandela","perseverance","Gandhi","nonviolence"),
    ("Confucius","wisdom","Socrates","inquiry"),
    ("Socrates","inquiry","Confucius","wisdom"),
    ("Nero","tyranny","Caligula","madness"),
    ("Caligula","madness","Nero","tyranny"),
    ("Croesus","wealth","Midas","greed"),
    ("Midas","greed","Croesus","wealth"),
]

HARD_PLACES = [
    ("stalactite","cave","coral","reef"),
    ("coral","reef","stalactite","cave"),
    ("barrister","court","surgeon","operating room"),
    ("surgeon","operating room","barrister","court"),
    ("sommelier","restaurant","curator","museum"),
    ("curator","museum","sommelier","restaurant"),
    ("plankton","ocean surface","lichen","rock"),
    ("lichen","rock","plankton","ocean surface"),
    ("stalagmite","cave floor","barnacle","hull"),
    ("barnacle","hull","stalagmite","cave floor"),
    ("orchid","canopy","moss","forest floor"),
    ("moss","forest floor","orchid","canopy"),
    ("lava","volcano","glacier","mountain"),
    ("glacier","mountain","lava","volcano"),
    ("oasis","desert","geyser","volcanic area"),
    ("geyser","volcanic area","oasis","desert"),
    ("delta","river mouth","fjord","coastline"),
    ("fjord","coastline","delta","river mouth"),
    ("permafrost","tundra","mangrove","estuary"),
    ("mangrove","estuary","permafrost","tundra"),
    ("diplomat","embassy","consul","consulate"),
    ("consul","consulate","diplomat","embassy"),
    ("senator","senate","representative","congress"),
    ("representative","congress","senator","senate"),
    ("magistrate","lower court","justice","supreme court"),
    ("justice","supreme court","magistrate","lower court"),
    ("archivist","archive","registrar","registry"),
    ("registrar","registry","archivist","archive"),
    ("actuary","insurance firm","auditor","accounting firm"),
    ("auditor","accounting firm","actuary","insurance firm"),
    ("docent","gallery","usher","theater"),
    ("usher","theater","docent","gallery"),
    ("hermit","cave","nomad","steppe"),
    ("nomad","steppe","hermit","cave"),
]

HARD_CAPITALS = [
    ("Australia","Canberra","Turkey","Ankara"),
    ("Turkey","Ankara","Australia","Canberra"),
    ("Brazil","Brasilia","Nigeria","Abuja"),
    ("Nigeria","Abuja","Brazil","Brasilia"),
    ("Myanmar","Naypyidaw","Vietnam","Hanoi"),
    ("Vietnam","Hanoi","Myanmar","Naypyidaw"),
    ("Switzerland","Bern","New Zealand","Wellington"),
    ("New Zealand","Wellington","Switzerland","Bern"),
    ("Canada","Ottawa","Australia","Canberra"),
    ("Australia","Canberra","Canada","Ottawa"),
    ("South Africa","Pretoria","Nigeria","Abuja"),
    ("Nigeria","Abuja","South Africa","Pretoria"),
    ("Myanmar","Naypyidaw","Turkey","Ankara"),
    ("Turkey","Ankara","Myanmar","Naypyidaw"),
    ("Brazil","Brasilia","Canada","Ottawa"),
    ("Canada","Ottawa","Brazil","Brasilia"),
    ("New Zealand","Wellington","Australia","Canberra"),
    ("Australia","Canberra","New Zealand","Wellington"),
    ("Switzerland","Bern","Canada","Ottawa"),
    ("Canada","Ottawa","Switzerland","Bern"),
    ("Turkey","Ankara","Brazil","Brasilia"),
    ("Brazil","Brasilia","Turkey","Ankara"),
    ("Nigeria","Abuja","Myanmar","Naypyidaw"),
    ("Myanmar","Naypyidaw","Nigeria","Abuja"),
    ("South Africa","Pretoria","Switzerland","Bern"),
    ("Switzerland","Bern","South Africa","Pretoria"),
    ("New Zealand","Wellington","Turkey","Ankara"),
    ("Turkey","Ankara","New Zealand","Wellington"),
    ("Australia","Canberra","Brazil","Brasilia"),
    ("Brazil","Brasilia","Australia","Canberra"),
    ("Canada","Ottawa","Nigeria","Abuja"),
    ("Nigeria","Abuja","Canada","Ottawa"),
    ("Myanmar","Naypyidaw","Switzerland","Bern"),
    ("Switzerland","Bern","Myanmar","Naypyidaw"),
]
# fmt: on


# ============================================================================
# DISTRACTOR BANKS (wrong answers by category)
# ============================================================================

SYMBOL_DISTRACTORS = [
    "fear", "anger", "war", "silence", "noise", "color", "weight", "speed",
    "cloth", "wind", "metal", "stone", "water", "fire", "earth", "air",
    "bird", "animal", "plant", "food", "tool", "weapon", "building", "road",
    "happiness", "sadness", "strength", "weakness", "beauty", "ugliness",
    "freedom", "power", "truth", "honor", "glory", "shame", "pride",
    "danger", "safety", "health", "wealth", "poverty", "wisdom", "folly",
]

SIGN_DISTRACTORS = [
    "color", "sound", "light", "noise", "speed", "size", "weight", "shape",
    "car", "road", "street", "building", "machine", "device", "tool",
    "run", "walk", "drive", "fly", "swim", "jump", "climb", "fall",
    "morning", "evening", "night", "day", "summer", "winter", "spring",
    "loud", "quiet", "bright", "dark", "fast", "slow", "heavy", "light",
]

QUALITY_DISTRACTORS = [
    "red", "blue", "green", "yellow", "white", "black", "brown", "gray",
    "big", "small", "tall", "short", "wide", "narrow", "thick", "thin",
    "round", "square", "flat", "curved", "straight", "pointed", "smooth",
    "old", "new", "young", "ancient", "modern", "fresh", "stale",
    "fast", "slow", "quick", "rapid", "gentle", "fierce", "calm",
    "wet", "dry", "warm", "cool", "damp", "moist", "frozen", "melted",
]

TRAIT_DISTRACTORS = [
    "tall", "short", "old", "young", "rich", "poor", "fast", "slow",
    "red", "blue", "green", "large", "small", "heavy", "light",
    "house", "car", "book", "school", "office", "garden", "forest",
    "running", "walking", "eating", "sleeping", "reading", "writing",
    "morning", "evening", "summer", "winter", "spring", "autumn",
    "happiness", "sadness", "anger", "fear", "surprise", "disgust",
]

PLACE_DISTRACTORS = [
    "big", "small", "old", "new", "fast", "slow", "hot", "cold",
    "red", "blue", "green", "white", "black", "yellow", "brown",
    "happy", "sad", "angry", "calm", "brave", "shy", "kind", "mean",
    "run", "walk", "fly", "swim", "drive", "climb", "jump", "fall",
    "morning", "evening", "night", "day", "summer", "winter",
    "food", "water", "air", "fire", "earth", "metal", "wood", "stone",
]

CAPITAL_DISTRACTORS = {
    "Japan": ["Osaka", "Kyoto", "Yokohama"],
    "Philippines": ["Quezon City", "Cebu", "Davao"],
    "France": ["Marseille", "Lyon", "Nice"],
    "United Kingdom": ["Manchester", "Birmingham", "Edinburgh"],
    "Italy": ["Milan", "Venice", "Florence"],
    "Spain": ["Barcelona", "Seville", "Valencia"],
    "Germany": ["Munich", "Hamburg", "Frankfurt"],
    "Thailand": ["Chiang Mai", "Phuket", "Pattaya"],
    "Vietnam": ["Ho Chi Minh City", "Da Nang", "Hue"],
    "Cambodia": ["Siem Reap", "Battambang", "Sihanoukville"],
    "Laos": ["Luang Prabang", "Savannakhet", "Pakse"],
    "Indonesia": ["Surabaya", "Bali", "Bandung"],
    "Malaysia": ["Penang", "Johor Bahru", "Malacca"],
    "South Korea": ["Busan", "Incheon", "Daegu"],
    "China": ["Shanghai", "Guangzhou", "Shenzhen"],
    "India": ["Mumbai", "Kolkata", "Chennai"],
    "Russia": ["St. Petersburg", "Novosibirsk", "Vladivostok"],
    "Egypt": ["Alexandria", "Luxor", "Giza"],
    "Australia": ["Sydney", "Melbourne", "Brisbane"],
    "Turkey": ["Istanbul", "Izmir", "Antalya"],
    "Brazil": ["Rio de Janeiro", "Sao Paulo", "Salvador"],
    "Nigeria": ["Lagos", "Kano", "Ibadan"],
    "Myanmar": ["Yangon", "Mandalay", "Bagan"],
    "Switzerland": ["Zurich", "Geneva", "Basel"],
    "New Zealand": ["Auckland", "Christchurch", "Queenstown"],
    "Canada": ["Toronto", "Vancouver", "Montreal"],
    "South Africa": ["Johannesburg", "Cape Town", "Durban"],
    "United States": ["New York", "Los Angeles", "Chicago"],
}


# ============================================================================
# QUESTION GENERATION LOGIC
# ============================================================================

def _pick_distractors(answer: str, pool: list[str], count: int = 3) -> list[str]:
    """Pick `count` distractors from pool that are not the answer."""
    candidates = [d for d in pool if d.lower() != answer.lower()]
    random.shuffle(candidates)
    return candidates[:count]


def _make_choices(answer: str, distractors: list[str]) -> list[str]:
    """Create a 4-choice list with the answer in a random position."""
    choices = distractors[:3] + [answer]
    random.shuffle(choices)
    return choices


def _capitalize(s: str) -> str:
    """Capitalize first letter of each word for display."""
    return s.title() if len(s) > 3 else s.capitalize()


def _build_question(pair_a: str, pair_b: str, pair_c: str) -> str:
    """Build the analogy question string."""
    return f"{pair_a.upper()} : {pair_b.upper()} :: {pair_c.upper()} : ?"


RELATIONSHIP_EXPLANATIONS = {
    "symbol": "Both pairs are symbol-and-meaning relationships where the first word symbolizes the second.",
    "sign": "Both pairs are sign-and-interpretation relationships where the first word signals the second.",
    "quality": "Both pairs are object-and-quality relationships where the object is characterized by the quality.",
    "trait": "Both pairs are person/figure-and-trait relationships where the figure is known for the trait.",
    "place": "Both pairs are object-and-place relationships where the first is found at the second.",
    "capital": "Both pairs are country-and-capital relationships.",
}


def generate_category(data_bank, category_key, distractor_pool, difficulty, count):
    """Generate questions from a data bank."""
    questions = []
    used = set()

    for item in data_bank:
        if len(questions) >= count:
            break

        pair_a, pair_b, pair_c, pair_d = item
        q_key = (pair_a, pair_b, pair_c, pair_d)
        if q_key in used:
            continue
        used.add(q_key)

        question_text = _build_question(pair_a, pair_b, pair_c)

        if category_key == "capital":
            # Use country-specific distractors
            country = pair_c
            if country in CAPITAL_DISTRACTORS:
                distractors = CAPITAL_DISTRACTORS[country][:3]
            else:
                distractors = _pick_distractors(pair_d, list(distractor_pool), 3)
        else:
            distractors = _pick_distractors(pair_d, distractor_pool, 3)

        # Ensure we have exactly 3 distractors
        while len(distractors) < 3:
            distractors.append("None of the above")

        answer_display = _capitalize(pair_d)
        choices = [_capitalize(d) for d in distractors[:3]] + [answer_display]
        random.shuffle(choices)

        explanation = (
            f"{_capitalize(pair_a)} relates to {pair_b} in the same way "
            f"{_capitalize(pair_c)} relates to {pair_d}. "
            f"{RELATIONSHIP_EXPLANATIONS[category_key]}"
        )

        questions.append({
            "difficulty": difficulty,
            "question": question_text,
            "choices": choices,
            "answer": answer_display,
            "explanation": explanation,
            "tags": ["word analogy", category_key, f"{category_key} relationships"],
        })

    return questions


def main():
    random.seed(42)  # Reproducible output

    all_questions = []

    # --- EASY (200 total) ---
    easy = []
    easy += generate_category(EASY_SYMBOLS, "symbol", SYMBOL_DISTRACTORS, "Easy", 40)
    easy += generate_category(EASY_SIGNS, "sign", SIGN_DISTRACTORS, "Easy", 40)
    easy += generate_category(EASY_QUALITIES, "quality", QUALITY_DISTRACTORS, "Easy", 40)
    easy += generate_category(EASY_TRAITS, "trait", TRAIT_DISTRACTORS, "Easy", 40)
    easy += generate_category(EASY_PLACES, "place", PLACE_DISTRACTORS, "Easy", 40)
    easy += generate_category(EASY_CAPITALS, "capital", [], "Easy", 40)

    # Trim or pad to exactly 200
    easy = easy[:200]
    all_questions += easy

    # --- MEDIUM (200 total) ---
    medium = []
    medium += generate_category(MEDIUM_SYMBOLS, "symbol", SYMBOL_DISTRACTORS, "Medium", 34)
    medium += generate_category(MEDIUM_SIGNS, "sign", SIGN_DISTRACTORS, "Medium", 34)
    medium += generate_category(MEDIUM_QUALITIES, "quality", QUALITY_DISTRACTORS, "Medium", 34)
    medium += generate_category(MEDIUM_TRAITS, "trait", TRAIT_DISTRACTORS, "Medium", 34)
    medium += generate_category(MEDIUM_PLACES, "place", PLACE_DISTRACTORS, "Medium", 34)
    medium += generate_category(MEDIUM_CAPITALS, "capital", [], "Medium", 34)

    medium = medium[:200]
    all_questions += medium

    # --- HARD (200 total) ---
    hard = []
    hard += generate_category(HARD_SYMBOLS, "symbol", SYMBOL_DISTRACTORS, "Hard", 34)
    hard += generate_category(HARD_SIGNS, "sign", SIGN_DISTRACTORS, "Hard", 34)
    hard += generate_category(HARD_QUALITIES, "quality", QUALITY_DISTRACTORS, "Hard", 34)
    hard += generate_category(HARD_TRAITS, "trait", TRAIT_DISTRACTORS, "Hard", 34)
    hard += generate_category(HARD_PLACES, "place", PLACE_DISTRACTORS, "Hard", 34)
    hard += generate_category(HARD_CAPITALS, "capital", [], "Hard", 34)

    hard = hard[:200]
    all_questions += hard

    # Assign sequential IDs
    for idx, q in enumerate(all_questions, start=1):
        q["id"] = idx
        q["subtest"] = B["subtest"]
        q["module"] = B["module"]
        q["subtopic"] = B["subtopic"]
        q["category"] = B["category"]
        q["language"] = B["language"]

    # Write output
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(all_questions)} questions")
    print(f"  Easy: {sum(1 for q in all_questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in all_questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in all_questions if q['difficulty'] == 'Hard')}")
    print(f"Output: {OUTPUT}")


main()
