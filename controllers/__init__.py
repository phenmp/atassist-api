from flask import Blueprint, request, jsonify

from configuration import Configuration
from controllers.game_api import GameApi
from models.deck import Deck
from models.stats import Stats
from models.card_set import CardSet

import constants

from contexts.deck_context import DeckContext
from contexts.inventory_filter_context import InventoryFilterContext

api = Blueprint("api", __name__)

configuration = Configuration()

apiController = GameApi(configuration)
deckController = Deck()

apiController.updateXMLFiles()


# 1.  Print Deck
@api.route('/api/deck/print-deck', methods=['POST'])
def deck_print():
    context = DeckContext(request)

    shouldUpdateDeck = deckController.updateAsMyDeck(context)

    print('Update Deck: ', shouldUpdateDeck)

    # TODO: need a proper response here
    if not shouldUpdateDeck:
        return "No active battle data. Go attack someone!"

    return jsonify(deckController.printDeck(context))


# 2.  Create Image of Deck
@api.route('/api/deck/create-deck-image', methods=['POST'])
def deck_create_image():
    context = DeckContext(request)

    shouldUpdateDeck = deckController.updateAsMyDeck(context)

    print('Update Deck: ', shouldUpdateDeck)
    # TODO: need a proper response here
    if not shouldUpdateDeck:
        return "No active battle data. Go attack someone!"

    return "Create Deck Image"


# 3. Create Image of Inventory
@api.route('/api/deck/create-inventory-image', methods=['POST'])
def create_inventory_image():
    context = DeckContext(request)

    deckController.updateAsInventory(context)

    filepath = deckController.createLargeDeckImage("", 10)
    return filepath


# 4. Filter Inventory by Trait
@api.route('/api/deck/filter-inventory-trait', methods=['POST'])
def filter_inventory_by_trait():
    context = InventoryFilterContext(request)
    deckController.updateAsInventory(context)
    deckController.filterTrait(context.trait)
    filepath = deckController.createLargeDeckImage("", 10)

    return filepath


# 5. Filter Inventory by Show
@api.route('/api/deck/filter-inventory-show', methods=['POST'])
def filter_inventory_by_show():
    context = InventoryFilterContext(request)
    apiController.updateInitFile(context)

    showUppercase = context.show.upper()

    if context.show.upper() in constants.CARD_SHOW_ABBREVIATION:
        showIndex = constants.CARD_SHOW_ABBREVIATION.index(showUppercase)
        deckController.updateAsInventory(context)
        deckController.filterShow(showIndex)
        return deckController.createLargeDeckImage("", 10)
    else:
        return 'invalid show'


# 6.  Filter Inventory C,I,PC
@api.route('/api/deck/filter-inventory-type', methods=['POST'])
def filter_inventory_by_type():
    context = InventoryFilterContext(request)
    apiController.updateInitFile(context)
    filepath = [None] * 3

    print('Characters')
    deckController.updateAsInventory(context)
    deckController.filterChar()
    filepath[0] = deckController.createLargeDeckImage("", 10)

    print('Items')
    deckController.updateAsInventory(context)
    deckController.filterItem()
    filepath[1] = deckController.createLargeDeckImage("", 10)

    print('Precombos')
    deckController.updateAsInventory(context)
    deckController.filterPC()
    filepath[2] = deckController.createLargeDeckImage("", 10)

    return jsonify({"files": filepath})


# 7.  Run Deck Analysis
@api.route('/api/deck/analyze-deck', methods=['POST'])
def analyze_deck():
    context = DeckContext(request)

    if not deckController.updateAsMyDeck(context):
        print("No active battle data. Go attack someone!")
        return jsonify({"result": "no active battle data"})

    deckController.findCombos()
    deck_path = deckController.createLargeDeckImage()
    combo_path = deckController.createLargeComboImage()

    stats = Stats("Stats", deckController)
    stats.calcStatData()
    stats.getSuggestions()

    if deck_path is None:
        print("No deck results to print.")
    else:
        print("Deck image saved to {0}".format(deck_path))
    if combo_path is None:
        print("No combo results to print.")
    else:
        print("Combo image saved to {0}".format(combo_path))

    return stats.printToTerminal()


# 8.  Create Stone Images
@api.route('/api/cardset/stones-set-image', methods=['POST'])
def get_stones_image():
    return CardSet().createStoneImages()


# 9.  Create Basic Pack Image
@api.route('/api/cardset/basic-set-image', methods=['POST'])
def get_basic_set_image():
    return CardSet().getBasicSet()


# 10.  Create BGE images
@api.route('/api/cards/bge-set-image', methods=['POST'])
def get_bge_set_image():
    # todo: need a new context - include bge selection
    # bgeContext = BGEContext(request)
    return CardSet().getBGEImages("addicted")


# 11.  Create BGE spreadsheets
@api.route('/api/cards/bge-set-sheet', methods=['POST'])
def get_bge_set_spreadsheet():
    # bgeContext = BGEContext(request)
    return CardSet().getBGESpreadsheets("addicted")


# 12.  Create Turd Pack Image
@api.route('/api/cards/bge-turd-pack-image', methods=['POST'])
def get_bge_turd_pack():
    # bgeContext = BGEContext(request)
    return CardSet().getTurdPack("addicted")


# A. Print Enemy Deck
@api.route('/api/enemy/enemy-deck-print', methods=['POST'])
def enemy_deck_print():
    context = DeckContext(request)

    if not deckController.updateAsEnemyDeck(context):
        return jsonify({"result": "no active battle data"})

    deckController.printDeck(context)


# B. Create Enemy Deck Image
@api.route('/api/enemy/create-enemy-deck-image', methods=['POST'])
def create_enemy_deck_image():
    context = DeckContext(request)

    if not deckController.updateAsEnemyDeck(context):
        return jsonify({"result": "no active battle data"})

    return deckController.createLargeDeckImage("enemy_deck")



# E. Run Enemy Deck Analysis
@api.route('/api/enemy/enemy-deck-analysis', methods=['POST'])
def enemy_deck_analyze():
    context = DeckContext(request)

    if not deckController.updateAsEnemyDeck(context):
        print("No active battle data. Go attack someone!")
        return jsonify({"result": "no active battle data"})

    deckController.findCombos()
    deck_path = deckController.createLargeDeckImage()
    combo_path = deckController.createLargeComboImage()

    stats = Stats("Stats", deckController)
    stats.calcStatData()
    stats.getSuggestions()

    if deck_path is None:
        print("No deck results to print.")
        return jsonify({"result": "No deck results to print."})
    else:
        print("Deck image saved to {0}".format(deck_path))

    if combo_path is None:
        print("No combo results to print.")
        return jsonify({"result": "No combo results to print."})
    else:
        print("Combo image saved to {0}".format(combo_path))

    stats.printToTerminal()
    return jsonify({"result": "no active battle data"})


# F.  Update XML files
@api.route('/api/misc/xml-update', methods=['POST'])
def update_xml_files():
    apiController.updateXMLFiles()

    return jsonify({"status": "success"})


# G.  Check for XML updates
@api.route('/api/misc/xml-update-check', methods=['POST'])
def check_for_xml_updates():
    apiController.checkForUpdates()

    return jsonify({"status": "success"})
