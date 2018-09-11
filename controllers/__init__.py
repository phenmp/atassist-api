from flask import Blueprint, request, jsonify

from configuration import Configuration
from controllers.game_api import GameApi
from models.deck import Deck

import constants

from contexts.deck_context import DeckContext
from contexts.inventory_filter_context import InventoryFilterContext

api = Blueprint("api", __name__)

configuration = Configuration()

apiController = GameApi(configuration)
deckController = Deck()


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

# @api.route('/api/deck/analysis', methods=['POST'])
