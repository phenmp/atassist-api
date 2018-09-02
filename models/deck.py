from texttable import Texttable

from controllers.game_api import GameApi
from models.card import Card
from configuration import Configuration

from utils.files import getUserLastDumpFilePath, writeToCsvFile

class Deck(object):
    def __init__(self):
        self.config = Configuration() 
        self.cards = []
        self.name  = ""
        self.combos  = []
        self.api = GameApi(self.config)

    def updateAsMyDeck(self, context):
        if (context.update):
            json = self.api.updateAndGetInitFile(context)
        else:
            json = self.api.getInit(context)
        
        if (not('active_battle_ndata' in json)):
            return 0
        
        if (str(json['active_battle_data']['host_is_attacker']).lower() == 'true'):
            #indices will be below 100
            lowerIndice = 1
            upperIndice = 35
        else:
            #indices will be above 100
            lowerIndice = 101
            upperIndice = 135

        cardMap = json['active_battle_data']['card_map']
        # order = []

        self.name = json['user_data']['name']
        self.getDeckFromCardMap(cardMap, lowerIndice, upperIndice)
        self.updateDeckFromXML()
        return 1

    def getDeckFromCardMap(self, cardMap, lower, upper):
        self.cards = []
        order = []

        #Get index values of array
        for card in cardMap:
            cardIndex = int(card)
            if (cardIndex >= lower and cardIndex <= upper):
                order.append(cardIndex)

        order.sort()

        for index in range(len(order)):
            for card in cardMap:
                if (int(card) == order[index]):
                    cardToAdd = Card()
                    cardToAdd.id = int( cardMap[card]['unit_id'])
                    cardToAdd.level = int( cardMap[card]['level'])
                    self.cards.append(cardToAdd)

    def updateCardWithXML(self, card, xml):
        found = 0

        for unit in xml.findall('unit'):
            if( int(unit.find('id').text) == card.id ):
                found = 1
                card.updateWithXML(unit)
                break

        return found

    def updateDeckFromXML(self):
        cards   = self.api.getCards()
        mythics = self.api.getMythics()
        pc      = self.api.getPC()
        
        for card in self.cards:
            if(self.updateCardWithXML(card, cards)):
                continue
            elif(self.updateCardWithXML(card, mythics)):
                continue
            elif(self.updateCardWithXML(card, pc)):
                continue

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
            ] )

        return rows

    def printDeck(self, context):
        if (context.sort):
            self.cards.sort(key = lambda x : (x.type, x.name, -x.level))
        
        if (context.title==""):
            title = self.name

        rows = [[]]
        deck_size = 0

        rows = self.getPrintableDeckArray()
        deck_size = len(rows) - 1

        tab = Texttable()

        if(context.amount):
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

        if(context.update):
            json = self.api.updateAndGetInitFile(context)
        else:
            json = self.api.getInit(context)

        cardMap = json['user_units']
        self.name = json['user_data']['name'] + "_inventory"

        print('[Deck] inventory for ', self.name)

        for card in cardMap:
            cardToAdd = Card()
            cardToAdd.id    = int( cardMap[card]['unit_id'] )
            cardToAdd.level = int( cardMap[card]['level'])
            print('[Deck] Adding card - id: {0}, level: {1}'.format(cardToAdd.id, cardToAdd.level))
            self.cards.append(cardToAdd)

        self.updateDeckFromXML()

        print('[Deck] update as inventory - returning')
        return self.cards