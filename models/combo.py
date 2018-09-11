import math

import constants
from models.card_basic import CardBasic


class Combo(CardBasic):
    def __init__(self, char=None, item=None, combo_id=0):
        CardBasic.__init__(self, combo_id, constants.COMBO)
        self.char = char
        self.item = item
        self.attack_multiplier = 0.0
        self.health_multiplier = 0.0
        self.combo_power = 0

    def updateWithXML(self, element):
        CardBasic.updateWithXML(self, element)

        self.type = constants.COMBO
        self.attack_multiplier = float(element.find('attack_multiplier').text)
        self.health_multiplier = float(element.find('health_multiplier').text)

        # Get skills
        for the_skill in element.findall('skill'):
            if the_skill.get('p') == '' or the_skill.get('v') == '':
                continue

            ident = the_skill.get('id')
            x = None
            y = None
            p = int(the_skill.get('p'))
            v = float(the_skill.get('v'))

            if 'y' in the_skill.attrib:
                y = the_skill.get('y')
            self.skills.insert(0, [ident, x, y, p, v])

        combo_power = 3 * (self.char.attack + self.item.attack) + (self.char.health + self.item.health)
        # Formulas for skill value/health/attack are appproximated numbers taken from here
        # https://www.reddit.com/r/AnimationThrowdown/comments/5l69n2/do_you_have_any_ideas_how_the_combo_stats_are/?st=j4p6yk8d&sh=09fc7f1f
        self.health = int(math.ceil(1.1 * (self.char.health + self.item.health) * self.health_multiplier))
        self.attack = int(math.ceil(1.1 * (self.char.attack + self.item.attack) * self.attack_multiplier))

        power = 1.1 * (3 * (self.char.attack + self.item.attack) + self.char.health + self.item.health)
        self.rarity = int(math.ceil(float(self.char.rarity + self.item.rarity) / 2.0))

        # Get skills
        for i in range(len(self.skills)):
            p = self.skills[i][3]
            v = self.skills[i][4]
            skill_x = int(math.ceil(((power - p) / 77) * v))
            self.skills[i][1] = skill_x

        for k in range(len(self.skills)):
            self.skills[k][0] = self.interpretSkill(self.skills[k][0])

        # Get card image info
        self.updateStillName()
        self.updateFrameName()

    def equals(self, card):
        equal = 0
        if self.id == card.id and self.char.id == card.char.id and self.item.id == card.item.id:
            if self.char.level == card.char.level and self.item.level == card.item.level:
                equal = 1

        return equal
