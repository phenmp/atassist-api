import time
from texttable import Texttable
from PIL import Image

import constants
from configuration import Configuration

from controllers.game_api import GameApi
from models.card import Card

from utils.cache import Cache
from utils.files import writeToCsvFile, getFullPath


class Deck(object):
    def __init__(self):
        self.config = Configuration()
        self.cache = Cache()
        self.cards = []
        self.name = ""
        self.combos = []
        self.api = GameApi(self.config)

    def updateAsMyDeck(self, context):
        if context.update:
            json = self.api.updateAndGetInitFile(context)
        else:
            json = self.api.getInit(context)

        if not ('active_battle_data' in json):
            return 0

        if str(json['active_battle_data']['host_is_attacker']).lower() == 'true':
            # indices will be below 100
            lower_indice = 1
            upper_indice = 35
        else:
            # indices will be above 100
            lower_indice = 101
            upper_indice = 135

        card_map = json['active_battle_data']['card_map']
        # order = []

        self.name = json['user_data']['name']
        self.getDeckFromCardMap(card_map, lower_indice, upper_indice)
        self.updateDeckFromXML()
        return 1

    def getDeckFromCardMap(self, cardMap, lower, upper):
        self.cards = []
        order = []

        # Get index values of array
        for card in cardMap:
            card_index = int(card)
            if lower <= card_index <= upper:
                order.append(card_index)

        order.sort()

        for index in range(len(order)):
            for card in cardMap:
                if int(card) == order[index]:
                    card_to_add = Card()
                    card_to_add.id = int(cardMap[card]['unit_id'])
                    card_to_add.level = int(cardMap[card]['level'])
                    self.cards.append(card_to_add)

    def updateCardWithXML(self, card, xml):
        found = 0

        for unit in xml.findall('unit'):
            if int(unit.find('id').text) == card.id:
                found = 1
                card.updateWithXML(unit)
                break

        return found

    def updateDeckFromXML(self):
        cards = self.api.getCards()
        mythics = self.api.getMythics()
        pc = self.api.getPC()

        for card in self.cards:
            if self.updateCardWithXML(card, cards):
                continue
            elif self.updateCardWithXML(card, mythics):
                continue
            elif self.updateCardWithXML(card, pc):
                continue

    def updateCombosFromXML(self):
        cards = self.api.getCards()

        for card in self.combos:
            if self.updateCardWithXML(card, cards):
                continue
            else:
                print("{0} not found. Should be an error".format(card.id))

    def getPrintableDeckArray(self):
        rows = [[]]

        for card in self.cards:
            rows.append([
                card.name,
                card.level,
                card.attack,
                card.health,
                card.interpretType(),
                card.getSkillString()
            ])

        return rows

    def printDeck(self, context):
        if context.sort:
            self.cards.sort(key=lambda x: (x.type, x.name, -x.level))

        if context.title == "":
            title = self.name

        rows = [[]]
        deck_size = 0

        rows = self.getPrintableDeckArray()
        deck_size = len(rows) - 1

        tab = Texttable()

        if context.amount:
            del rows[context.amount:]

        header = ['Name', 'Level', 'Attack', 'Health', 'Type', 'Skills']

        tab.add_rows(rows)
        tab.set_cols_align(['r', 'r', 'r', 'r', 'r', 'l'])
        tab.set_cols_width([30, 5, 6, 6, 6, 50])
        tab.header(header)

        deck_output = "{0}\n".format(title)
        deck_output += "Deck Size: {0}\n".format(deck_size)
        deck_output += tab.draw()

        # TODO: Should convert deck response to JSON instead of printable table, no longer command line app

        # write to file
        writeToCsvFile(context.userId, header, rows)

        return deck_output

    def updateAsInventory(self, context):
        self.cards = []

        if context.update:
            json = self.api.updateAndGetInitFile(context)
        else:
            json = self.api.getInit(context)

        card_map = json['user_units']
        self.name = json['user_data']['name'] + "_inventory"

        print('[Deck] inventory for ', self.name)

        for card in card_map:
            card_to_add = Card()
            card_to_add.id = int(card_map[card]['unit_id'])
            card_to_add.level = int(card_map[card]['level'])
            print('[Deck] Adding card - id: {0}, level: {1}'.format(card_to_add.id, card_to_add.level))
            self.cards.append(card_to_add)

        self.updateDeckFromXML()

        print('[Deck] update as inventory - returning')
        return self.cards

    def getCardIndex(self, card_id):
        index = None

        for index in range(len(self.cards)):
            if self.cards[index].id == card_id:
                index = index
                break

        return index

    def addCard(self, card_id=0, level=0, name=""):
        card = Card()
        card.id, card.level, card.name = card_id, level, name
        self.cards.append(card)

    def trimCombos(self):
        self.combos.sort(key=lambda x: (-x.rarity, x.name, -x.combo_power))

        index = 1
        while index < len(self.combos):
            if self.combos[index].name == self.combos[index - 1].name:
                del self.combos[index]
            else:
                index += 1

    def drawAllCards(self, cards):
        for index in range(0, len(cards)):
            print('Creating images... {0}%'.format(float(int(float(index) / float(len(cards)) * 10000)) / 100))
            cache = self.cache.getCardFromCache(cards[index])

            if cache is None:
                cards[index].createCardImage()
                self.cache.saveCardToCache(cards[index])
            else:
                cards[index].setImage(cache)

    def createLargeComboImage(self, name="", width=10, quality=100):
        return self.__createDeckImage(self.combos, name, "_combos", width, quality)

    def createLargeDeckImage(self, name="", width=5, quality=100):
        return self.__createDeckImage(self.cards, name, "", width, quality)

    def compileImages(self, cards, width=5):
        count = len(cards)
        rows = 0
        cols = 0

        if count <= 0:
            return

        img_width, img_height = cards[0].image.size

        if count > width:
            cols = width
        else:
            cols = count
        while count > 0:
            count -= width
            rows += 1

        master = Image.new('RGBA', (img_width * cols, img_height * rows), "white")

        r_count = 0
        c_count = 0

        for index in range(len(cards)):
            print('Compiling images... {0}%'.format(float(int(float(index) / float(len(cards)) * 10000)) / 100))
            master.paste(cards[index].image, (img_width * c_count, img_height * r_count))
            c_count += 1

            if c_count >= width:
                c_count = 0
                r_count += 1

        return master

    def filterTrait(self, trait):
        index = 0

        while index < len(self.cards):
            success = 0
            for j in range(len(self.cards[index].trait)):
                if self.cards[index].trait[j] == trait:
                    success = 1
                    break

            if not success:
                del self.cards[index]
            else:
                index += 1

        self.name += "_" + trait

    def filterShow(self, show):
        index = 0

        while index < len(self.cards):

            if not self.cards[index].show == show:
                del self.cards[index]
            else:
                index += 1

        self.name += "_" + constants.CARD_SHOW[show]

    def filterChar(self):
        index = 0

        while index < len(self.cards):

            if not (self.cards[index].type == constants.CHAR or self.cards[index].type == constants.MYTHIC):
                del self.cards[index]
            else:
                index += 1

        self.name += "_" + "Characters"

    def filterItem(self):
        index = 0

        while index < len(self.cards):

            if self.cards[index].type != constants.ITEM:
                del self.cards[index]
            else:
                index += 1

        self.name += "_" + "Items"

    def filterPC(self):
        index = 0

        while index < len(self.cards):

            if self.cards[index].type != constants.PC:
                del self.cards[index]
            else:
                index += 1

        self.name += "_" + "PC"

    def __createDeckImage(self, cardset, name, suffix="", width=5, quality=100):
        filename = None

        if name == "":
            name = self.name + suffix

        self.cards.sort(key=lambda x: (-x.rarity, x.type, x.name, -x.level))
        start_time = time.time()

        self.drawAllCards(self.combos)
        self.drawAllCards(cardset)
        end_time = time.time()
        print('Created images in {0}'.format(end_time - start_time))

        master = self.compileImages(cardset, width)

        if master is not None:
            print("Saving image...")
            filename = getFullPath(self.config.paths.savePath, "{0}.png".format(name))
            master.save(filename, quality=quality)

        return filename
