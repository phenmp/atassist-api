class CardBasic:
    # Constants
    CARD_TYPES = [ "Mythic", "Char", "Item", "PC", "Combo" ]
    CARD_SHOW = [ "Family Guy", "American Dad", "Bob's Burgers", "King of the Hill", "Futurama", "No Show" ]
    CARD_SHOW_ABBREVIATION = ["FG", "AD", "BB", "KH", "FT", "Generic" ]
    RARITY = [ "common", "rare", "epic", "legendary", "mythic", "Giggity" ]
    MYTHIC = 0
    CHAR   = 1
    ITEM   = 2
    PC     = 3
    COMBO  = 4
    GIGGITY= 5
    FG,AD,BB,KH,FT,GE = 0,1,2,3,4,5
    CARD_SKILLS = { 
        "invigorate" : "boost",
        "strike" : "punch",
        "barrierall" : "shieldall",
        "poison" : 'gas',
        "outlast" : "recover",
        "counter" : "payback",
        "barrier" : "shield",
        "armored" : "sturdy",
        "rallyall" : "cheerall",
        "rally" : "cheer",
        "berserk" : "crazed",
        "weakenall" : "crippleall",
        "weaken" : "cripple",
        "shrapnel" : "bomb",
        "inspire" : "motivate",
        "pierce" : "jab"
    }

    def __init__(self,card_id=0,card_type=1):
        self.id      = card_id
        self.name    = ""
        self.trait   = []
        self.level   = 0
        self.attack  = 0
        self.health  = 0
        self.skills  = []
        self.picture = ""
        self.rarity  = 1
        self.type    = card_type
        self.show    = 0
        self.still   = ""
        self.frame   = ""
        self.levelup = ""
        self.image   = None

    def interpretType(self):
        return self.CARD_TYPES[self.type]

    def interpretSkill(self, skill):
        if skill in self.CARD_SKILLS:
            return self.CARD_SKILLS[skill]

        return skill

    def getSkillString(self):
        result = ""

        for skill in self.skills:
            result += str(skill[0]) + ": "
            result += str(skill[1])

            if (skill[2] == "" or skill[2] == None):
                result += " "
            elif( len(skill[2]) == 1 ):
                result += " show "
            else:
                result += " trait "
                
        return result