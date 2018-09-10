from models.card_basic import CardBasic


class Card(CardBasic):
    def __init__(self):
        CardBasic.__init__(self)

    def updateCardSkills(self, skills):
        for the_skill in skills:
            ident = the_skill.get('id')
            x = the_skill.get('x')
            y = None

            if 'y' in the_skill.attrib:
                y = the_skill.get('y')
            self.skills.insert(0, [ident, x, y])

    def updateCardLevel(self, upgrades):
        for upgrade in upgrades:
            if int(upgrade.find('level').text) <= self.level:
                for health in upgrade.findall('health'):
                    self.health = int(health.text)

                for attack in upgrade.findall('attack'):
                    self.attack = int(attack.text)

                for skill in upgrade.findall('skill'):
                    found = 0
                    for k in range(len(self.skills)):  # Check if card already has the skill
                        if self.skills[k][0] == skill.get('id'):
                            found = 1
                            i = self.skills[k][0]
                            x = skill.get('x')
                            y = ""

                            if 'y' in skill.attrib:
                                y = skill.get('y')

                            self.skills[k] = [i, x, y]
                        if found:
                            break
                    if not (found):  # If new skill, then add it to the list
                        id = skill.get('id')
                        x = skill.get('x')
                        y = ""

                        if 'y' in skill.attrib:
                            y = skill.get('y')

                        self.skills.append([id, x, y])

    def updateWithXML(self, element):
        CardBasic.updateWithXML(self, element)

        health = element.find('health')
        attack = element.find('attack')

        if not (health is None):
            self.health = int(health.text)

        if not (attack is None):
            self.attack = int(attack.text)

        # Get skills
        self.updateCardSkills(element.findall('skill'))

        # Upgrade the card to the appropriate level
        self.updateCardLevel(element.findall('upgrade'))

        for skillIndex in range(len(self.skills)):
            self.skills[skillIndex] = (self.interpretSkill(self.skills[skillIndex][0]),
                                       self.skills[skillIndex][1],
                                       self.skills[skillIndex][2])

        # Get card image info
        self.updateStillName()
        self.updateFrameName()

    def createCardImage(self):
        CardBasic.createCardImage(self)
