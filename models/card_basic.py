import os
from PIL import Image, ImageFont, ImageDraw

from configuration import Configuration
from utils.files import getFullPath

import constants


class CardBasic:
    config = Configuration()
    stills = os.listdir(config.paths.stillsPath)

    def __init__(self, card_id=0, card_type=1):
        self.id = card_id
        self.name = ""
        self.trait = []
        self.level = 0
        self.attack = 0
        self.health = 0
        self.skills = []
        self.picture = ""
        self.rarity = 1
        self.type = card_type
        self.show = 0
        self.still = ""
        self.frame = ""
        self.levelUp = ""
        self.image = None

    def getName(self):
        return self.name

    def getTrait(self):
        return self.trait

    def getLevel(self):
        return self.level

    def getAttack(self):
        return self.attack

    def getHealth(self):
        return self.health

    def getSkills(self):
        return self.skills

    def getPicture(self):
        return self.picture

    def getRarity(self):
        return self.rarity

    def getCardType(self):
        return self.type

    def getShow(self):
        return self.show

    def getStill(self):
        return self.still

    def getFrame(self):
        return self.frame

    def getLevelUp(self):
        return self.levelUp

    def getImage(self):
        return self.image

    def getSkillString(self):
        result = ""

        for skill in constants.CARD_SKILLS:
            result += str(skill[0]) + ": "
            result += str(skill[1])

            if skill[2] == "" or skill[2] is None:
                result += " "
            elif len(skill[2]) == 1:
                result += " show "
            else:
                result += " trait "

        return result

    def setName(self, name):
        self.name = name

    def setTrait(self, trait):
        self.trait = trait

    def setLevel(self, level):
        self.level = level

    def setAttack(self, attack):
        self.attack = attack

    def setHealth(self, health):
        self.health = health

    def setSkills(self, skills):
        self.skills = skills

    def setPicture(self, picture):
        self.picture = picture

    def setRarity(self, rarity):
        self.rarity = rarity

    def setCardType(self):
        if self.id > 1000000:
            self.type = constants.MYTHIC
        elif self.id >= 100000:
            if self.id == 100000 or self.id == 100001 or self.id == 100002:
                self.type = constants.GIGGITY
            else:
                self.type = constants.PC
        else:
            if self.isCharacter():
                self.type = constants.CHAR
            else:
                self.type = constants.ITEM

    def setShow(self):
        if self.id > 1000000:
            show = self.id - 1000000
            show /= 100000
        elif self.id >= 100000:
            show = self.id - 100000
            show /= 10000
        else:
            show = self.id / 10000

        self.show = int(show - 1)

    def setStill(self, still):
        self.still = still

    def setFrame(self, frame):
        self.frame = frame

    def setLevelUp(self, levelUp):
        self.levelUp = levelUp

    def setImage(self, image):
        self.image = image

    def interpretType(self):
        return constants.CARD_TYPES[self.type]

    def interpretSkill(self, skill):
        if skill in constants.CARD_SKILLS:
            return constants.CARD_SKILLS[skill]

        return skill

    def isCharacter(self):
        if self.name in constants.CHARACTERS:
            return 1
        else:
            return 0

    def equals(self, card):
        equal = 0
        if self.id == card.id:
            if self.level == card.level:
                equal = 1
        return equal
