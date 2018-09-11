# Constants
CARD_TYPES = ["Mythic", "Char", "Item", "PC", "Combo"]
CARD_SHOW = ["Family Guy", "American Dad", "Bob's Burgers", "King of the Hill", "Futurama", "No Show"]
CARD_SHOW_ABBREVIATION = ["FG", "AD", "BB", "KH", "FT", "Generic"]
RARITY = ["common", "rare", "epic", "legendary", "mythic", "Giggity"]
CATEGORIES = ["Character", "Item", "Precombo", "Combo"]

MYTHIC = 0
CHAR = 1
ITEM = 2
PC = 3
COMBO = 4
GIGGITY = 5

FG, AD, BB, KH, FT, GE = 0, 1, 2, 3, 4, 5

WARSTART = 1501783200  # August 3rd, 6PM GMT
WARCOUNT = 12  # Start of 12th rumble
WARPERIOD = 1814400  # Three weeks
WARDURATION = 518400  # Six days

CARD_SKILLS = {
    "invigorate": "boost",
    "strike": "punch",
    "barrierall": "shieldall",
    "poison": 'gas',
    "outlast": "recover",
    "counter": "payback",
    "barrier": "shield",
    "armored": "sturdy",
    "rallyall": "cheerall",
    "rally": "cheer",
    "berserk": "crazed",
    "weakenall": "crippleall",
    "weaken": "cripple",
    "shrapnel": "bomb",
    "inspire": "motivate",
    "pierce": "jab"
}

CHARACTERS = [
    "Amy", "Bender", "Bill", "Bob", "Bobby", "Boomhauer", "Brian", "Bullock", "Chris", "Chris Griffin", "Dale",
    "Dr. Amy Wong", "Dr. Zoidberg", "Eugene Belcher", "Francine", "Fry", "Gene", "Hank", "Hank Hill", "Hayley",
    "Hermes", "Klaus", "Klaus Heisler", "Leela", "Linda", "Linda Belcher", "Lois", "Louise", "Luanne", "Meg",
    "Mort", "Peggy", "Peter", "Philip J. Fry", "Professor Farnsworth", "Quagmire", "Roger", "Stan", "Stewie",
    "Steve", "Steve Smith", "Teddy", "Tina"]
