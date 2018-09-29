from utils.files import getFullPath

import constants

from models.card_basic import CardBasic
from models.deck import Deck
from models.combo import Combo

from controllers.game_api import GameApi

from configuration import Configuration


class CardSet(object):
    def __init__(self):
        config = Configuration()
        self.api = GameApi(config)

        self.savePath = config.paths.savePath
        self.stills = config.stills

    # returns list of ids for cards that match constraints
    def searchXML(self, xml_files="", musthave=[], mustnothave=[]):
        the_list = []

        for xml in xml_files:
            for unit in xml.findall('unit'):
                success = 1

                for i in range(len(musthave)):
                    item, value = musthave[i]
                    attributes = unit.findall(item)

                    if len(attributes) == 1:
                        if not (attributes[0].text.lower() == value.lower()):
                            success = 0
                            break
                    else:  # xml with 2 values (ie traits)
                        attr_success = 0
                        for a in attributes:
                            if a.text.lower() == value.lower():
                                attr_success = 1
                                break
                        if not attr_success:
                            success = 0

                if success:
                    for i in range(len(mustnothave)):
                        item, value = mustnothave[i]
                        attributes = unit.findall(item)

                        if len(attributes) == 1:
                            if attributes[0].text.lower() == value.lower():
                                success = 0
                                break
                        else:  # xml with 2 values (ie traits)
                            attr_success = 0
                            for a in attributes:
                                if a.text.lower() == value.lower():
                                    attr_success = 1
                                    break
                            if attr_success:
                                success = 0

                if success:
                    value = int(unit.find('id').text)
                    the_list.append(value)

        return the_list

    def createStoneImages(self):
        # Legendaries from Nixons
        cards = self.api.getCards()
        pc = self.api.getPC()

        bas_leg = self.searchXML(xml_files=[cards], musthave=[('set', '1'), ('rarity', '4')])
        exp_leg = self.searchXML(xml_files=[cards], musthave=[('set', '3'), ('rarity', '4')])
        bas_epi = self.searchXML(xml_files=[cards], musthave=[('set', '1'), ('rarity', '3')])
        exp_epi = self.searchXML(xml_files=[cards], musthave=[('set', '3'), ('rarity', '3')])
        power = self.searchXML(xml_files=[pc], musthave=[('set', '3002'), ('rarity', '3')])

        deck_names = ["Nixon Legendary", "Legendary Stones", "Epic Stones", "Power Stones"]
        decks = [None] * len(deck_names)

        decks[0], filepath = self.createImageFromList(deck_names[0], [bas_leg])
        decks[1], filepath = self.createImageFromList(deck_names[1], [bas_leg, exp_leg])
        decks[2], filepath = self.createImageFromList(deck_names[2], [bas_epi, exp_epi])
        decks[3], filepath = self.createImageFromList(deck_names[3], [power])

        for i in range(len(decks)):
            decks[i].printDeck()

    def getTurdPack(self, bge):
        cards = self.api.getCards()
        combos = self.api.getCombos()
        pc = self.api.getPC()

        # Gets all non-combo bge cards
        bge_pc = self.searchXML(xml_files=[pc], musthave=[('trait', bge)], mustnothave=[('set', '9999')])
        input_cards = self.searchXML(xml_files=[cards],
                                     musthave=[('trait', bge), ('rarity', '3')],
                                     mustnothave=[('set', '1001'), ('set', '1002'), ('set', '9999')])
        b = self.searchXML(xml_files=[cards],
                           musthave=[('trait', bge), ('rarity', '4')],
                           mustnothave=[('set', '1001'), ('set', '1002'), ('set', '9999')])
        input_cards.extend(b)
        input_cards.extend(bge_pc)

        # combo_deck.combos.sort(key=lambda x : (-x.rarity, x.name, -x.combo_power))
        input_cards, input_path = self.createImageFromList("{0}_turd_pack".format(bge), [input_cards])
        pc, pc_path = self.createImageFromList("{0}_pc".format(bge), [bge_pc])

        # print("Deck image saved as {0}".format(input_path))

        input_cards.printDeck()

    def getBGEImages(self, bge="athletic"):
        cards = self.api.getCards()
        combos = self.api.getCombos()
        pc = self.api.getPC()

        # Gets all non-combo bge cards
        bge_pc = self.searchXML(xml_files=[pc], musthave=[('trait', bge)])
        input_cards = self.searchXML(xml_files=[cards],
                                     musthave=[('trait', bge)],
                                     mustnothave=[('set', '1001'), ('set', '1002')])

        # Gets all combo bge cards
        combo_list = self.searchXML(xml_files=[cards], musthave=[('trait', bge), ('set', '1001')])
        exp_two_list = self.searchXML(xml_files=[cards], musthave=[('trait', bge), ('set', '1002')])
        combo_list.extend(exp_two_list)

        combo_deck = Deck()

        input_list = []
        for card_id in combo_list:
            for card in combos.findall('combo'):
                if int(card.find('card_id').text) == card_id:
                    cards = card.find('cards')
                    if cards.get('card1') == '' or cards.get('card2') == '':
                        continue

                    card_one_id = int(cards.get('card1'))
                    card_two_id = int(cards.get('card2'))

                    one_index = combo_deck.getCardIndex(card_one_id)
                    two_index = combo_deck.getCardIndex(card_two_id)

                    if one_index is None:
                        one_index = len(combo_deck.cards)
                        combo_deck.addCard(card_id=card_one_id)

                    if two_index is None:
                        two_index = len(combo_deck.cards)
                        combo_deck.addCard(card_id=card_two_id)

                    new_combo = Combo(combo_deck.cards[one_index], combo_deck.cards[two_index], card_id)
                    combo_deck.combos.append(new_combo)

        combo_deck.updateDeckFromXML()
        combo_deck.updateCombosFromXML()
        combo_deck.trimCombos()

        # combo_deck.combos.sort(key=lambda x : (-x.rarity, x.name, -x.combo_power))
        combo_path = combo_deck.createLargeComboImage(bge + "_combos", 10)
        input_cards, input_path = self.createImageFromList(bge + "_input_cards", [input_cards])
        pc, pc_path = self.createImageFromList(bge + "_pc", [bge_pc])

        # print("Deck image saved as {0}".format(combo_path))
        # print("Deck image saved as {0}".format(input_path))
        # print("Deck image saved as {0}".format(pc_path))

        combo_deck.printCombosToTerminal()
        input_cards.printDeckToTerminal()
        pc.printDeckToTerminal()

    def getBGESpreadsheets(self, bge="athletic"):
        cards = self.api.getCards()
        combos = self.api.getCombos()

        # Gets all combo bge cards
        combo_list = self.searchXML(xml_files=[cards], musthave=[('trait', bge), ('set', '1001')])
        exp_two_list = self.searchXML(xml_files=[cards], musthave=[('trait', bge), ('set', '1002')])
        combo_list.extend(exp_two_list)

        combo_deck = Deck()

        input_list = []
        for card_id in combo_list:
            for card in combos.findall('combo'):
                if int(card.find('card_id').text) == card_id:
                    cards = card.find('cards')

                    if cards.get('card1') == '' or cards.get('card2') == '':
                        continue

                    card_one_id = int(cards.get('card1'))
                    card_two_id = int(cards.get('card2'))

                    # Skip mythics
                    if card_one_id > 1000000:
                        continue

                    one_index = combo_deck.getCardIndex(card_one_id)
                    two_index = combo_deck.getCardIndex(card_two_id)

                    if one_index is None:
                        one_index = len(combo_deck.cards)
                        combo_deck.addCard(card_id=card_one_id)

                    if two_index is None:
                        two_index = len(combo_deck.cards)
                        combo_deck.addCard(card_id=card_two_id)

                    new_combo = Combo(combo_deck.cards[one_index], combo_deck.cards[two_index], card_id)
                    combo_deck.combos.append(new_combo)

        if len(combo_deck.combos) <= 0:
            # print("No combos found for {0}".format(bge))
            return

        combo_deck.updateDeckFromXML()
        combo_deck.updateCombosFromXML()

        # Create 2d array of items on left and chars on top
        combo_deck.cards.sort(key=lambda x: (x.type, -x.rarity, x.name))

        # Count columns and rows
        col_count = 0
        row_count = 0

        while col_count < len(combo_deck.cards) and \
                (combo_deck.cards[col_count].type == constants.CHAR or
                 combo_deck.cards[col_count].type == constants.MYTHIC):
            col_count += 1

        while col_count + row_count < len(combo_deck.cards) and \
                combo_deck.cards[row_count + col_count].type == constants.ITEM:
            row_count += 1

        col_count += 1
        row_count += 1
        arr = [["-"] * col_count for x in range(row_count)]

        m = 1
        while m - 1 < len(combo_deck.cards) and \
                (combo_deck.cards[m - 1].type == constants.CHAR or
                 combo_deck.cards[m - 1].type == constants.MYTHIC):
            arr[0][m] = combo_deck.cards[m - 1].name
            m += 1

        i = 1
        while (i + m - 2) < len(combo_deck.cards) and combo_deck.cards[i + m - 2].type == constants.ITEM:
            arr[i][0] = combo_deck.cards[i + m - 2].name
            i += 1

        for x in range(len(combo_deck.combos)):
            # find column
            a = 1
            while arr[0][a].lower() != combo_deck.combos[x].char.name.lower():
                a += 1

            # find row
            b = 1
            while arr[b][0].lower() != combo_deck.combos[x].item.name.lower():
                b += 1

            arr[b][a] = combo_deck.combos[x].name

        # Write combos to file

        target = open(getFullPath(self.savePath, "{0}_combos_table.csv".format(bge)), 'w')
        target.truncate()

        for i in range(len(arr)):
            for j in range(len(arr[i])):
                target.write("\"" + arr[i][j] + "\", ")
            target.write("\n")
        target.close()

        target = open(getFullPath(self.savePath, "{0}_combos_list.csv".format(bge)), 'w')
        target.truncate()

        for i in range(len(combo_deck.combos)):
            target.write(
                "\"" + combo_deck.combos[i].char.name + "\", " + "\"" + combo_deck.combos[i].item.name + "\", " + "\"" +
                combo_deck.combos[i].name + "\", \n")
        target.close()

    def getBasicSet(self):
        cards = self.api.getCards()
        set_one = bas_leg = self.searchXML(xml_files=[cards], musthave=[('set', '1')])
        deck, filepath = self.createImageFromList("Basic Set", [set_one], 10)

        if filepath is not None:
            # print("Deck image saved as {0}".format(filepath))
            deck.printDeckToTerminal()

    def countCombos(self):
        combos = self.api.getCombos()
        count = 0
        lst = []
        for combo in combos.findall('combo'):
            count += 1
            new_id = combo.find('card_id').text
            lst.append(new_id)
        lst.sort()
        i = 0

        while i < len(lst) - 1:
            if lst[i] == lst[i + 1]:
                del lst[i + 1]
            else:
                i += 1

        # print("Total combos in game: {0}".format(count))
        # print("Total unique combos in game: {0}".format(i))

    def countCards(self):
        cards = self.api.getCards()
        count = 0
        lst = []

        for card in cards.findall('unit'):
            new_id = card.find('id').text
            the_set = card.find('set').text

            if the_set == '9999' or the_set == '5000' or the_set == '6000' or the_set == '9000':
                continue

            count += 1
            lst.append(new_id)

        lst.sort()
        i = 0

        while i < len(lst) - 1:
            if lst[i] == lst[i + 1]:
                del lst[i + 1]
            else:
                i += 1

        # print("Total cards in game: {0}".format(count))
        # print("Total unique cards in game: {0}".format(i))

    def createImageFromList(self, name="default", card_ids=[], width=5):
        full_list = []

        for i in range(len(card_ids)):
            full_list.extend(card_ids[i])

        deck = Deck(name=name)
        deck.addListOfIds(full_list)
        deck.updateDeckFromXML()
        filepath = deck.createLargeDeckImage(name, width=width)

        return deck, filepath

    def findCombos(self, chars, threshold, search="ITEMS"):
        if search == "ITEMS":
            card1, card2, check, against = 'card1', 'card2', "items", "characters"
        else:  # search characters based on items
            card1, card2, check, against = 'card2', 'card1', "characters", "items"

        combos = self.api.getCombos()
        cards = self.api.getCards()

        mix_tot = 0
        items = []

        # use first character to create list of items
        for combo in combos.findall('combo'):
            the_card = combo.find('cards')
            if the_card.get(card2) == "" or the_card.get(card1) == "":
                continue
            item = int(the_card.get(card2))
            if int(the_card.get(card1)) == chars[0].id:
                items.append(the_card.get(card2))

        # print("Items to test")
        # print(items)

        # check if list of items is compatible with other characters, if no, delete
        for i in range(1, len(chars)):
            # print('Looking for {0} that mix with your {1}... {2}%'.format(check, against, float(
            #     int(float(i) / float(len(chars)) * 10000)) / 100))
            j = 0
            while j < len(items):
                success = 0

                for combo in combos.findall('combo'):
                    the_card = combo.find('cards')
                    if the_card.get(card2) == "" or the_card.get(card1) == "":
                        continue

                    if int(the_card.get(card1)) == chars[i].id and the_card.get(card2) == items[j]:
                        success = 1
                        break

                if not success:
                    del items[j]
                else:
                    j += 1

        if len(items):
            item_deck = Deck()
            item_deck.addListOfIds(items)
            item_deck.updateDeckFromXML()
        else:
            item_deck = None

        return item_deck

    def printMissingStills(self):
        cards = self.api.getCards()

        for card in cards.findall('unit'):
            name = card.find('name').text
            card_id = int(card.find('id').text)

            picture = name.replace("'", "")
            picture = picture.replace("!", "")
            picture = picture.replace("-", "")
            picture = picture.replace(":", "")
            picture = picture.replace(" ", "")
            picture = picture.replace(".", "")
            picture = picture.replace("\"", "")

            if card_id > 1000000:
                show = card_id - 1000000
                show /= 100000
            elif card_id >= 100000:
                show = card_id - 100000
                show /= 10000
            else:
                show = card_id / 10000

            show = show - 1
            if card_id > 1000000:
                picture += "Mythic"

            picture = constants.CARD_SHOW[show] + "_" + picture + ".png"
            success = 0
            for i in range(len(self.stills)):
                if self.stills[i].lower() == picture.lower():
                    success = 1
                    break

            if not success:
                print(picture)

    def printSkillTypes(self):
        skills = self.api.getCards()
        holder = []
        for skill in skills.findall('skillType'):
            holder.append([skill.find('name').text, int(skill.find('power').text)])

        holder.sort(key=lambda x: x[1])
        # for i in range(len(holder)):
        #     print('Skill: {0},\tPower: {1}'.format(holder[i][0], holder[i][1]))
