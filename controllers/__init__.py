from flask import Blueprint, request, jsonify

from controllers.game_api import GameApi
from models.deck import Deck

from contexts.deck_context import DeckContext
from contexts.inventory_filter_context import InventoryFilterContext

api = Blueprint("api", __name__)

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

# @api.route('/api/deck/filter-inventory-show', methods=['POST'])

# @api.route('/api/deck/analysis', methods=['POST'])
