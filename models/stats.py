from texttable import Texttable

import constants

from configuration import Configuration
from controllers import GameApi
from models.card_basic import CardBasic
from models.card_set import CardSet


class Stats:
    def __init__(self, name="", deck=None):
        self.configuration = Configuration()
        self.api = GameApi(self.configuration)

        self.name = name
        self.item_count = []
        self.char_count = []
        self.combo_count = []
        self.trait_count = []
        self.show_count = []
        self.skill_count = []
        self.show_stats = []
        self.trait_stats = []
        self.skill_stats = []
        self.combo_list = []
        self.unique_combos = []
        self.char_suggest = None
        self.item_suggest = None

        if not deck is None:
            self.updateWithDeck(deck)
        else:
            self.combos = []
            self.chars = []
            self.items = []
            self.pc = []

    def updateWithDeck(self, deck):
        self.combos = deck.combos
        self.chars = []
        self.items = []
        self.pc = []

        for i in range(len(deck.cards)):
            if deck.cards[i].type == constants.CHAR or deck.cards[i].type == constants.MYTHIC:
                self.chars.append(deck.cards[i])
            elif deck.cards[i].type == constants.ITEM:
                self.items.append(deck.cards[i])
            elif deck.cards[i].type == constants.PC:
                self.pc.append(deck.cards[i])

        self.chars.sort(key=lambda x: x.name)
        self.items.sort(key=lambda x: x.name)
        self.pc.sort(key=lambda x: x.name)
        self.char_count = [0] * len(self.chars)
        self.item_count = [0] * len(self.items)
        self.combo_count = [0] * len(self.combos)

    def calcStatData(self):
        # Tally up all char/item/combo counts
        for c in range(len(self.combos)):
            for k in range(len(self.chars)):
                for i in range(len(self.items)):
                    if self.combos[c].char.id == self.chars[k].id and self.combos[c].item.id == self.items[i].id:
                        self.char_count[k] += 1
                        self.item_count[i] += 1
                        self.combo_count[c] += 1

        self.show_stats = []
        self.trait_stats = []
        self.skill_stats = []
        self.combo_list = []
        self.unique_combos = []

        # Tally up all combos
        for i in range(len(self.combos)):
            new_entry = [self.combos[i].name, self.combos[i].char.name, self.combos[i].item.name, self.combo_count[i]]
            self.combo_list.append(new_entry)

        # Tally up unique combos
        for i in range(len(self.combos)):
            self.tallyItem(self.unique_combos, self.combos[i].name, self.combo_count[i], 0, 1)

        blanks = len(constants.CATEGORIES)

        # Tally up shows
        for k in range(len(self.chars)):
            self.tallyItem(self.show_stats, constants.CARD_SHOW[self.chars[k].show], 1, constants.CHAR, blanks)

        for k in range(len(self.items)):
            self.tallyItem(self.show_stats, constants.CARD_SHOW[self.items[k].show], 1, constants.ITEM, blanks)

        for k in range(len(self.pc)):
            self.tallyItem(self.show_stats, constants.CARD_SHOW[self.pc[k].show], 1, constants.PC, blanks)

        for k in range(len(self.combos)):
            self.tallyItem(self.show_stats, constants.CARD_SHOW[self.combos[k].show], self.combo_count[k],
                           constants.COMBO, blanks)

        # Tally up Traits
        for k in range(len(self.chars)):
            for t in range(len(self.chars[k].trait)):
                self.tallyItem(self.trait_stats, self.chars[k].trait[t], 1, constants.CHAR, blanks)
        for k in range(len(self.items)):
            for t in range(len(self.items[k].trait)):
                self.tallyItem(self.trait_stats, self.items[k].trait[t], 1, constants.ITEM, blanks)
        for k in range(len(self.pc)):
            for t in range(len(self.pc[k].trait)):
                self.tallyItem(self.trait_stats, self.pc[k].trait[t], 1, constants.PC, blanks)
        for k in range(len(self.combos)):
            for t in range(len(self.combos[k].trait)):
                self.tallyItem(self.trait_stats, self.combos[k].trait[t], self.combo_count[k], constants.COMBO, blanks)

        # Tally up Skills
        for k in range(len(self.chars)):
            for s in range(len(self.chars[k].skills)):
                self.tallyItem(self.skill_stats, self.chars[k].skills[s][0], 1, constants.CHAR, blanks)
        for k in range(len(self.items)):
            for s in range(len(self.items[k].skills)):
                self.tallyItem(self.skill_stats, self.items[k].skills[s][0], 1, constants.ITEM, blanks)
        for k in range(len(self.pc)):
            for s in range(len(self.pc[k].skills)):
                self.tallyItem(self.skill_stats, self.pc[k].skills[s][0], 1, constants.PC, blanks)
        for k in range(len(self.combos)):
            for s in range(len(self.combos[k].skills)):
                self.tallyItem(self.skill_stats, self.combos[k].skills[s][0], self.combo_count[k], constants.COMBO,
                               blanks)

    def getSuggestions(self):
        card_set = CardSet()
        self.item_suggest = card_set.findCombos(self.chars, .8, "ITEMS")
        self.char_suggest = card_set.findCombos(self.items, .8, "CHARS")

        if not self.item_suggest is None:
            self.item_suggest.cards.sort(key=lambda x: -x.rarity)
        if not self.char_suggest is None:
            self.char_suggest.cards.sort(key=lambda x: -x.rarity)

    def printTableToTerminal(self, rows, header, row_widths, alignment):
        rows.insert(0, [])
        tab = Texttable()
        tab.add_rows(rows)
        tab.set_cols_align(alignment)
        tab.set_cols_width(row_widths)
        tab.header(header)
        print(tab.draw())

    def tallyItem(self, table, item, inc, category, blanks):
        col_index = category + 1
        row_index = 0
        found = 0

        for index in range(len(table)):
            if table[index][0] == item:
                row_index = index
                found = 1
                break

        if found:
            table[row_index][col_index] += inc
        else:
            new_entry = [0] * blanks
            new_entry.insert(0, item)
            new_entry[col_index] = inc
            table.append(new_entry)

    def printToTerminal(self):
        # Chars mix with items
        print("")
        for i in range(len(self.chars)):
            if i - 1 >= 0 and self.chars[i - 1].id == self.chars[i].id:
                continue
            print("{0} combos with {1} out of {2} items ({3}%)"
                  .format(self.chars[i].name, self.char_count[i],
                          len(self.items),
                          float(int((float(self.char_count[i]) / float(len(self.items))) * 10000)) / 100))
        print("")

        # Items mix with chars
        for i in range(len(self.items)):
            if i - 1 >= 0 and self.items[i - 1].id == self.items[i].id:
                continue
            print("{0} combos with {1} out of {2} Characters ({3}%)"
                  .format(self.items[i].name, self.item_count[i],
                          len(self.items),
                          float(int((float(self.item_count[i]) / float(len(self.chars))) * 10000)) / 100))
        print("")
        print("Characters       : {0}".format(len(self.chars)))
        print("Items            : {0}".format(len(self.items)))
        print("Precombos        : {0}".format(len(self.pc)))
        print("Unique Combos    : {0}".format(len(self.combos)))

        self.show_stats.sort(key=lambda x: -x[4])
        self.trait_stats.sort(key=lambda x: -x[4])
        self.skill_stats.sort(key=lambda x: -x[4])
        self.combo_list.sort(key=lambda x: -x[3])
        self.unique_combos.sort(key=lambda x: -x[1])
        header = []

        for i in range(len(constants.CATEGORIES)):
            header.append(constants.CATEGORIES[i])

        header.insert(0, "")
        row_widths = [20, 10, 10, 10, 10]
        alignment = ['r', 'r', 'r', 'r', 'r']

        self.printTableToTerminal(self.show_stats, header, row_widths, alignment)
        self.printTableToTerminal(self.trait_stats, header, row_widths, alignment)
        self.printTableToTerminal(self.skill_stats, header, row_widths, alignment)
        self.printTableToTerminal(self.combo_list,
                                  ['Combo Name', 'Character', 'Item', 'Frequency'],
                                  [30, 30, 30, 12],
                                  ['r', 'r', 'r', 'r'])
        self.printTableToTerminal(self.unique_combos, ['Combo Name', 'Frequency'], [30, 12], ['r', 'r'])

        if not self.item_suggest is None:
            print("Items that mix with 100% of your characters")
            for i in range(len(self.item_suggest.cards)):
                print(self.item_suggest.cards[i].name)
        else:
            print("No items found")

        if not self.char_suggest is None:
            print("")
            print("Characters that mix with 100% of your items")
            for i in range(len(self.char_suggest.cards)):
                print(self.char_suggest.cards[i].name)
        else:
            print("No characters found")
